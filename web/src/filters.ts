// Pure filter / sort / URL logic. No Vue here, so it is easy to test.
import type { Offer, StoreId } from './types'

export type Sort = 'food' | 'discount' | 'price' | 'ending' | 'store'
export type When = 'all' | 'today' | 'soon'

export interface Filters {
  q: string
  stores: StoreId[]
  cats: string[]
  min: number | null
  max: number | null
  disc: number
  when: When
  nocard: boolean
  onlydisc: boolean
  fav: boolean
  sort: Sort
}

export const DEFAULTS: Filters = {
  q: '', stores: [], cats: [], min: null, max: null, disc: 0,
  when: 'all', nocard: false, onlydisc: false, fav: false, sort: 'food',
}

const SORTS: Sort[] = ['food', 'discount', 'price', 'ending', 'store']

/** Grocery crates: the weekly shop. The default order puts these first. */
export const FOOD = new Set(['sadje-zelenjava', 'meso-ribe', 'mlecni-jajca', 'kruh-pekovski', 'shramba',
  'zamrznjeno', 'sladko-slano', 'pijace', 'alkohol'])
const WHENS: When[] = ['all', 'today', 'soon']

/** Today as YYYY-MM-DD in Ljubljana, the same calendar the scraper uses. */
export function todayLjubljana(now = new Date()): string {
  return new Intl.DateTimeFormat('sv-SE', { timeZone: 'Europe/Ljubljana' }).format(now)
}

/** Lower-case and strip diacritics so "cokolada" finds "Čokolada". */
export function fold(s: string): string {
  return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
}

export function searchText(o: Offer): string {
  return fold(`${o.name} ${o.brand ?? ''} ${o.package ?? ''}`)
}

type Facet = 'stores' | 'cats' | null

/** Valid today (or undated), as opposed to an offer that starts later. */
export function isStarted(o: Offer, today: string): boolean {
  return !o.valid_from || o.valid_from <= today
}

/** Apply every filter except `skip` (used to compute facet counts). */
export function matches(o: Offer, f: Filters, today: string, favs: Set<string>, skip: Facet = null, text?: string): boolean {
  if (skip !== 'stores' && f.stores.length && !f.stores.includes(o.store)) return false
  if (skip !== 'cats' && f.cats.length && !f.cats.includes(o.category)) return false
  if (f.min != null && o.price < f.min) return false
  if (f.max != null && o.price > f.max) return false
  if (f.disc > 0 && (o.discount_pct ?? 0) < f.disc) return false
  if (f.onlydisc && o.kind !== 'discount') return false
  if (f.nocard && o.requires_card) return false
  if (f.fav && !favs.has(o.id)) return false
  const started = isStarted(o, today)
  if (f.when === 'today' && !started) return false
  if (f.when === 'soon' && started) return false
  if (f.q.trim()) {
    const hay = text ?? searchText(o)
    for (const word of fold(f.q).split(/\s+/).filter(Boolean)) if (!hay.includes(word)) return false
  }
  return true
}

const STORE_ORDER: Record<string, number> = { lidl: 0, spar: 1, eurospin: 2, hofer: 3 }

/** Every sort keeps offers valid today ahead of those that start later. */
export function compare(sort: Sort, today: string): (a: Offer, b: Offer) => number {
  const by = within(sort)
  return (a, b) => Number(isStarted(b, today)) - Number(isStarted(a, today)) || by(a, b)
}

function within(sort: Sort): (a: Offer, b: Offer) => number {
  const byDiscount = (a: Offer, b: Offer) => (b.discount_pct ?? 0) - (a.discount_pct ?? 0) || a.price - b.price
  switch (sort) {
    case 'price': return (a, b) => a.price - b.price || byDiscount(a, b)
    case 'ending': return (a, b) => (a.valid_to ?? '9999').localeCompare(b.valid_to ?? '9999') || byDiscount(a, b)
    case 'store': return (a, b) => STORE_ORDER[a.store] - STORE_ORDER[b.store] || byDiscount(a, b)
    case 'food': return (a, b) => Number(FOOD.has(b.category)) - Number(FOOD.has(a.category)) || byDiscount(a, b)
    default: return byDiscount
  }
}

/** Filters <-> query string. Defaults are omitted so URLs stay short. */
export function toQuery(f: Filters): string {
  const p = new URLSearchParams()
  if (f.q.trim()) p.set('q', f.q.trim())
  if (f.stores.length) p.set('trgovine', f.stores.join(','))
  if (f.cats.length) p.set('kategorije', f.cats.join(','))
  if (f.min != null) p.set('od', String(f.min))
  if (f.max != null) p.set('do', String(f.max))
  if (f.disc > 0) p.set('popust', String(f.disc))
  if (f.when !== 'all') p.set('kdaj', f.when === 'today' ? 'danes' : 'kmalu')
  if (f.nocard) p.set('brez-kartice', '1')
  if (f.onlydisc) p.set('samo-popusti', '1')
  if (f.fav) p.set('priljubljeni', '1')
  if (f.sort !== 'food') p.set('razvrsti', { price: 'cena', ending: 'konec', store: 'trgovina', discount: 'popust', food: 'zivila' }[f.sort])
  const s = p.toString()
  return s ? `?${s}` : ''
}

function num(v: string | null): number | null {
  if (v == null || v === '') return null
  const n = Number(v.replace(',', '.'))
  return Number.isFinite(n) && n >= 0 ? n : null
}

export function fromQuery(search: string): Filters {
  const p = new URLSearchParams(search)
  const list = (k: string) => (p.get(k) ?? '').split(',').map(s => s.trim()).filter(Boolean)
  const sortMap: Record<string, Sort> = { cena: 'price', konec: 'ending', trgovina: 'store', popust: 'discount', zivila: 'food' }
  const whenMap: Record<string, When> = { danes: 'today', kmalu: 'soon' }
  const sort = sortMap[p.get('razvrsti') ?? ''] ?? 'food'
  const when = whenMap[p.get('kdaj') ?? ''] ?? 'all'
  return {
    q: p.get('q') ?? '',
    stores: list('trgovine') as StoreId[],
    cats: list('kategorije'),
    min: num(p.get('od')),
    max: num(p.get('do')),
    disc: Math.min(90, Math.max(0, Math.round(num(p.get('popust')) ?? 0))),
    when: WHENS.includes(when) ? when : 'all',
    nocard: p.get('brez-kartice') === '1',
    onlydisc: p.get('samo-popusti') === '1',
    fav: p.get('priljubljeni') === '1',
    sort: SORTS.includes(sort) ? sort : 'food',
  }
}

export function activeCount(f: Filters): number {
  return [f.stores.length > 0, f.cats.length > 0, f.min != null, f.max != null, f.disc > 0,
    f.when !== 'all', f.nocard, f.onlydisc, f.fav].filter(Boolean).length
}
