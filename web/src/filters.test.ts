import { describe, expect, it } from 'vitest'
import { izdelkov } from './format'
import { compare, DEFAULTS, fold, fromQuery, matches, toQuery, todayLjubljana, type Filters } from './filters'
import type { Offer } from './types'

const o = (x: Partial<Offer>): Offer => ({
  id: 'lidl:1', store: 'lidl', name: 'Mleko', kind: 'special', price: 1, requires_card: false,
  min_quantity: 1, category: 'mlecni-jajca', ...x,
})
const F = (x: Partial<Filters> = {}): Filters => ({ ...structuredClone(DEFAULTS), ...x })
const T = '2026-10-09'
const none = new Set<string>()

describe('matches', () => {
  it('filters by store and category, skipping the facet being counted', () => {
    const f = F({ stores: ['spar'], cats: ['alkohol'] })
    expect(matches(o({}), f, T, none)).toBe(false)
    expect(matches(o({ store: 'spar', category: 'alkohol' }), f, T, none)).toBe(true)
    expect(matches(o({ category: 'alkohol' }), f, T, none, 'stores')).toBe(true)
  })
  it('search ignores case and diacritics, all words must match', () => {
    const x = o({ name: 'Čokolada mlečna', brand: 'Milka' })
    expect(matches(x, F({ q: 'cokolada milka' }), T, none)).toBe(true)
    expect(matches(x, F({ q: 'cokolada temna' }), T, none)).toBe(false)
  })
  it('price range, min discount, discounts only, card', () => {
    const d = o({ kind: 'discount', price: 2, regular_price: 4, discount_pct: 50, requires_card: true })
    expect(matches(d, F({ min: 3 }), T, none)).toBe(false)
    expect(matches(d, F({ max: 2 }), T, none)).toBe(true)
    expect(matches(d, F({ disc: 55 }), T, none)).toBe(false)
    expect(matches(o({}), F({ onlydisc: true }), T, none)).toBe(false)
    expect(matches(d, F({ nocard: true }), T, none)).toBe(false)
  })
  it('valid today vs starts soon', () => {
    const now = o({ valid_from: '2026-10-08' })
    const later = o({ valid_from: '2026-10-12' })
    expect(matches(now, F({ when: 'today' }), T, none)).toBe(true)
    expect(matches(later, F({ when: 'today' }), T, none)).toBe(false)
    expect(matches(later, F({ when: 'soon' }), T, none)).toBe(true)
  })
  it('favourites', () => {
    expect(matches(o({}), F({ fav: true }), T, new Set(['lidl:1']))).toBe(true)
    expect(matches(o({}), F({ fav: true }), T, none)).toBe(false)
  })
})

describe('sort', () => {
  it('highest discount first, special offers last', () => {
    const list = [o({ id: 'a' }), o({ id: 'b', discount_pct: 10 }), o({ id: 'c', discount_pct: 40 })]
    expect(list.sort(compare('discount')).map(x => x.id)).toEqual(['c', 'b', 'a'])
  })
  it('default puts grocery crates first, then by discount', () => {
    const list = [o({ id: 'book', category: 'drugo', discount_pct: 60 }), o({ id: 'milk', discount_pct: 10 }), o({ id: 'pear', category: 'sadje-zelenjava', discount_pct: 30 })]
    expect(list.sort(compare('food')).map(x => x.id)).toEqual(['pear', 'milk', 'book'])
  })
  it('ending soonest puts undated last', () => {
    const list = [o({ id: 'a' }), o({ id: 'b', valid_to: '2026-10-12' }), o({ id: 'c', valid_to: '2026-10-10' })]
    expect(list.sort(compare('ending')).map(x => x.id)).toEqual(['c', 'b', 'a'])
  })
})

describe('URL', () => {
  it('round-trips and omits defaults', () => {
    expect(toQuery(F())).toBe('')
    const f = F({ q: 'kava', stores: ['lidl', 'spar'], cats: ['pijace'], min: 1, max: 5.5, disc: 20, when: 'soon', nocard: true, onlydisc: true, fav: true, sort: 'price' })
    expect(fromQuery(toQuery(f))).toEqual(f)
  })
  it('ignores junk', () => {
    expect(fromQuery('?razvrsti=x&kdaj=y&popust=abc&od=-3')).toEqual(F())
  })
})

it('fold and Ljubljana date', () => {
  expect(fold('ŠČŽ ćđ')).toBe('scz cđ')
  expect(todayLjubljana(new Date('2026-10-08T22:30:00Z'))).toBe('2026-10-09')
})

it('Slovene plural, nominative and accusative', () => {
  expect([1, 2, 3, 5, 101, 103, 104].map(n => izdelkov(n))).toEqual(['1 izdelek', '2 izdelka', '3 izdelki', '5 izdelkov', '101 izdelek', '103 izdelki', '104 izdelki'])
  expect(izdelkov(103, 'acc')).toBe('103 izdelke')
  expect(izdelkov(105, 'acc')).toBe('105 izdelkov')
})
