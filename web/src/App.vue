<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, shallowRef, watch } from 'vue'
import OfferCard from './components/OfferCard.vue'
import Logo from './components/Logo.vue'
import Icon from './components/Icon.vue'
import { loadMeta, loadOffers } from './data'
import { activeCount, compare, DEFAULTS, fromQuery, isStarted, matches, searchText, toQuery, todayLjubljana, type Filters, type Sort } from './filters'
import { izdelkov, price } from './format'
import { STORES } from './stores'
import { crate } from './theme'
import type { Meta, Offer, StoreId } from './types'

const PAGE = 60
const STALE_HOURS = 36
const FAV_KEY = 'knk:priljubljeni'
const VT_LIMIT = 24 // cards that morph in the re-plant transition; the rest just appear

const SORTS: { id: Sort; label: string }[] = [
  { id: 'food', label: 'Najprej živila' },
  { id: 'discount', label: 'Največji popust' },
  { id: 'price', label: 'Najnižja cena' },
  { id: 'ending', label: 'Kmalu poteče' },
  { id: 'store', label: 'Po trgovini' },
]

const offers = shallowRef<Offer[]>([])
const meta = ref<Meta | null>(null)
const error = ref('')
const loading = ref(true)
const today = todayLjubljana()

const clone = (x: Filters): Filters => JSON.parse(JSON.stringify(x))
const f = reactive<Filters>(fromQuery(location.search)) // what the controls edit
const view = ref<Filters>(clone(f)) // what the grid shows (committed, possibly via a view transition)
const searchInput = ref(f.q)
const shown = ref(PAGE)
const sheetOpen = ref(false)

// ---- favourites: browser only ------------------------------------------
function readFavs(): Set<string> {
  try { return new Set(JSON.parse(localStorage.getItem(FAV_KEY) || '[]')) } catch { return new Set() }
}
const favs = ref(readFavs())
function toggleFav(id: string) {
  const next = new Set(favs.value)
  next.has(id) ? next.delete(id) : next.add(id)
  favs.value = next
  try { localStorage.setItem(FAV_KEY, JSON.stringify([...next])) } catch { /* private mode */ }
}

// ---- data ----------------------------------------------------------------
const texts = new Map<string, string>()
onMounted(async () => {
  try {
    const [o, m] = await Promise.all([loadOffers(), loadMeta()])
    for (const x of o) texts.set(x.id, searchText(x))
    offers.value = o
    meta.value = m
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
})

const categories = computed(() => meta.value?.categories ?? [])
const storeRows = computed(() => STORES.map(s => ({ ...s, live: !!meta.value?.stores[s.id]?.count_published })))

const match = (o: Offer, skip: 'stores' | 'cats' | null = null) =>
  matches(o, view.value, today, favs.value, skip, texts.get(o.id))

const results = computed(() => offers.value.filter(o => match(o)).sort(compare(view.value.sort, today)))
const visible = computed(() => results.value.slice(0, shown.value))
// Offers that start later sort last; a heading marks where they begin.
const firstLater = computed(() => results.value.findIndex(o => !isStarted(o, today)))
const laterCount = computed(() => firstLater.value < 0 ? 0 : results.value.length - firstLater.value)

function countBy(key: 'store' | 'category', skip: 'stores' | 'cats') {
  const c: Record<string, number> = {}
  for (const o of offers.value) if (match(o, skip)) c[o[key]] = (c[o[key]] ?? 0) + 1
  return c
}
const storeCounts = computed(() => countBy('store', 'stores'))
const catCounts = computed(() => countBy('category', 'cats'))
const allInCats = computed(() => Object.values(catCounts.value).reduce((a, b) => a + b, 0))

const freshness = computed(() => {
  if (!meta.value) return ''
  const d = new Date(meta.value.generated_at)
  const day = todayLjubljana(d)
  const time = new Intl.DateTimeFormat('sl-SI', { hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Ljubljana' }).format(d)
  if (day === today) return `danes ob ${time}`
  if (day === todayLjubljana(new Date(Date.now() - 864e5))) return `včeraj ob ${time}`
  return `${Number(day.slice(8))}. ${Number(day.slice(5, 7))}. ob ${time}`
})

const staleStores = computed(() => {
  if (!meta.value) return []
  const now = Date.now()
  return STORES.flatMap(s => {
    const m = meta.value!.stores[s.id]
    if (!m) return []
    const age = m.updated_at ? (now - new Date(m.updated_at).getTime()) / 36e5 : Infinity
    if (m.ok && age < STALE_HOURS) return []
    const when = m.updated_at ? new Intl.DateTimeFormat('sl-SI', { day: 'numeric', month: 'numeric' }).format(new Date(m.updated_at)) : null
    return [`${s.label}: ${when ? `zadnja uspešna posodobitev ${when}` : 'še ni podatkov'}`]
  })
})

// ---- filter actions ------------------------------------------------------
function toggle<T>(list: T[], v: T) {
  const i = list.indexOf(v)
  i >= 0 ? list.splice(i, 1) : list.push(v)
}
const toggleStore = (id: StoreId) => toggle(f.stores, id)
const toggleCat = (id: string) => toggle(f.cats, id)
function reset() {
  Object.assign(f, clone(DEFAULTS))
  searchInput.value = ''
}
const filterCount = computed(() => activeCount(f))
const catLabel = (id: string) => categories.value.find(c => c.id === id)?.label ?? id

function priceModel(key: 'min' | 'max') {
  return computed({
    get: () => f[key] ?? '',
    set: (v: string | number) => {
      const n = typeof v === 'number' ? v : parseFloat(String(v).replace(',', '.'))
      f[key] = Number.isFinite(n) && n >= 0 ? n : null
    },
  })
}
const minPrice = priceModel('min')
const maxPrice = priceModel('max')

let debounce: number | undefined
watch(searchInput, v => {
  clearTimeout(debounce)
  debounce = window.setTimeout(() => { f.q = v }, 160)
})

// ---- commit: the stakes re-plant ---------------------------------------
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)')
type VTDoc = Document & { startViewTransition?: (cb: () => Promise<void> | void) => unknown }

function commit(animate: boolean) {
  const apply = async () => {
    view.value = clone(f)
    shown.value = PAGE
    await nextTick()
  }
  const doc = document as VTDoc
  if (animate && doc.startViewTransition && !reduceMotion.matches && !loading.value) doc.startViewTransition(apply)
  else apply()
}

// Filters live in the address so a view can be bookmarked or shared.
watch(f, () => {
  const searchOnly = f.q !== view.value.q
  commit(!searchOnly)
  const url = `${location.pathname}${toQuery(f)}`
  if (url !== `${location.pathname}${location.search}`) history.replaceState(null, '', url)
}, { deep: true })

function onPopState() {
  Object.assign(f, fromQuery(location.search))
  searchInput.value = f.q
}

const vtName = (o: Offer, i: number) => (i < VT_LIMIT ? `o-${o.id.replace(/[^a-z0-9-]/gi, '-')}` : undefined)

// ---- infinite scroll -------------------------------------------------------
const sentinel = ref<HTMLElement | null>(null)
let observer: IntersectionObserver | undefined
onMounted(() => {
  window.addEventListener('popstate', onPopState)
  observer = new IntersectionObserver(entries => {
    if (entries.some(e => e.isIntersecting) && shown.value < results.value.length) shown.value += PAGE
  }, { rootMargin: '900px' })
  watch(sentinel, (el, old) => {
    if (old) observer!.unobserve(old)
    if (el) observer!.observe(el)
  }, { immediate: true })
})
onBeforeUnmount(() => {
  observer?.disconnect()
  window.removeEventListener('popstate', onPopState)
})

watch(sheetOpen, open => document.documentElement.classList.toggle('no-scroll', open))
function onKey(e: KeyboardEvent) { if (e.key === 'Escape') sheetOpen.value = false }
onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>

<template>
  <header class="bar">
    <div class="bar-in">
      <a class="brand" href="./" aria-label="Katalogi na kratko, začetek" @click.prevent="reset">
        <Logo :size="30" />
        <span class="word">Katalogi <em>na kratko</em></span>
      </a>
      <label class="search">
        <Icon name="search" />
        <input v-model="searchInput" type="search" placeholder="Išči izdelek ali znamko" aria-label="Iskanje po akcijah" enterkeyhint="search" />
        <button v-if="searchInput" type="button" class="clear" aria-label="Počisti iskanje" @click="searchInput = ''">
          <Icon name="close" :size="16" />
        </button>
      </label>
      <p v-if="meta" class="fresh">
        <span class="dot" aria-hidden="true" />
        <span>Posodobljeno <b>{{ freshness }}</b></span>
      </p>
    </div>
  </header>

  <!-- phone: quick crate rail -->
  <nav class="rail" aria-label="Kategorije">
    <button type="button" class="crate-chip" :class="{ on: !f.cats.length }" :aria-pressed="!f.cats.length" @click="f.cats.splice(0)">
      Vse <span class="n">{{ allInCats }}</span>
    </button>
    <button
      v-for="c in categories"
      :key="c.id"
      type="button"
      class="crate-chip"
      :class="{ on: f.cats.includes(c.id) }"
      :style="{ '--crate': crate(c.id) }"
      :aria-pressed="f.cats.includes(c.id)"
      :disabled="!catCounts[c.id] && !f.cats.includes(c.id)"
      @click="toggleCat(c.id)"
    >
      <i class="sw" aria-hidden="true" />{{ c.label }} <span class="n">{{ catCounts[c.id] ?? 0 }}</span>
    </button>
  </nav>

  <!-- phone: store toggles stay on the first screen -->
  <div class="store-strip" role="group" aria-label="Trgovine">
    <button
      v-for="s in storeRows"
      :key="s.id"
      type="button"
      class="store-chip"
      :class="{ on: f.stores.includes(s.id) }"
      :style="{ '--store': s.color }"
      :aria-pressed="f.stores.includes(s.id)"
      :disabled="!s.live || (!storeCounts[s.id] && !f.stores.includes(s.id))"
      @click="toggleStore(s.id)"
    >
      <i class="dot" aria-hidden="true" />{{ s.label }} <span class="n">{{ s.live ? (storeCounts[s.id] ?? 0) : 'kmalu' }}</span>
    </button>
  </div>

  <div class="shell">
    <aside class="panel" :class="{ open: sheetOpen }" aria-label="Filtri">
      <div class="sheet-head">
        <h2>Filtri</h2>
        <button type="button" class="icon-btn" aria-label="Zapri filtre" @click="sheetOpen = false"><Icon name="close" /></button>
      </div>

      <section class="block">
        <h3 class="block-h">Trgovine</h3>
        <div class="stores">
          <button
            v-for="s in storeRows"
            :key="s.id"
            type="button"
            class="store-btn"
            :class="{ on: f.stores.includes(s.id) }"
            :style="{ '--store': s.color }"
            :aria-pressed="f.stores.includes(s.id)"
            :disabled="!s.live || (!storeCounts[s.id] && !f.stores.includes(s.id))"
            @click="toggleStore(s.id)"
          >
            <i class="dot" aria-hidden="true" />
            <span class="lbl">{{ s.label }}</span>
            <span class="n">{{ s.live ? (storeCounts[s.id] ?? 0) : 'kmalu' }}</span>
          </button>
        </div>
      </section>

      <section class="block cats-block">
        <h3 class="block-h">Kategorije</h3>
        <ul class="crates">
          <li v-for="c in categories" :key="c.id">
            <button
              type="button"
              class="crate-row"
              :class="{ on: f.cats.includes(c.id) }"
              :style="{ '--crate': crate(c.id) }"
              :aria-pressed="f.cats.includes(c.id)"
              :disabled="!catCounts[c.id] && !f.cats.includes(c.id)"
              @click="toggleCat(c.id)"
            >
              <i class="sw" aria-hidden="true" /><span class="lbl">{{ c.label }}</span><span class="n">{{ catCounts[c.id] ?? 0 }}</span>
            </button>
          </li>
        </ul>
      </section>

      <section class="block">
        <h3 class="block-h">Cena</h3>
        <div class="range">
          <label><span class="sr">Od</span><input v-model="minPrice" type="number" min="0" step="0.5" inputmode="decimal" placeholder="od" /><i>€</i></label>
          <span class="dash" aria-hidden="true" />
          <label><span class="sr">Do</span><input v-model="maxPrice" type="number" min="0" step="0.5" inputmode="decimal" placeholder="do" /><i>€</i></label>
        </div>
      </section>

      <section class="block">
        <h3 class="block-h">Najmanj popusta <output class="out">{{ f.disc ? `${f.disc} %` : 'vseeno' }}</output></h3>
        <input v-model.number="f.disc" class="slider" type="range" min="0" max="70" step="5" aria-label="Najmanjši popust v odstotkih"
          :style="{ '--v': `${(f.disc / 70) * 100}%` }" />
      </section>

      <section class="block">
        <h3 class="block-h">Veljavnost</h3>
        <div class="seg" role="radiogroup" aria-label="Veljavnost">
          <label v-for="w in [['all', 'Vse'], ['today', 'Velja danes'], ['soon', 'Kmalu']]" :key="w[0]" :class="{ on: f.when === w[0] }">
            <input v-model="f.when" type="radio" name="when" :value="w[0]" />{{ w[1] }}
          </label>
        </div>
      </section>

      <section class="block toggles">
        <label class="switch"><input v-model="f.onlydisc" type="checkbox" /><i aria-hidden="true" />Samo popusti, brez posebnih ponudb</label>
        <label class="switch"><input v-model="f.nocard" type="checkbox" /><i aria-hidden="true" />Skrij cene s kartico zvestobe</label>
        <label class="switch"><input v-model="f.fav" type="checkbox" /><i aria-hidden="true" />Samo priljubljeni <span class="n">{{ favs.size }}</span></label>
      </section>

      <div class="sheet-foot">
        <button type="button" class="btn ghost" :disabled="!filterCount && !f.q" @click="reset">Počisti</button>
        <button type="button" class="btn solid" @click="sheetOpen = false">Pokaži {{ izdelkov(results.length, 'acc') }}</button>
      </div>
    </aside>
    <div v-if="sheetOpen" class="scrim" @click="sheetOpen = false" />

    <main class="main">
      <p v-if="staleStores.length" class="notice" role="status">
        <b>Podatki niso povsem sveži.</b> {{ staleStores.join(' · ') }}.
      </p>

      <div class="tools">
        <p class="total" aria-live="polite">
          <template v-if="loading">Nalagam akcije …</template>
          <template v-else><b>{{ results.length.toLocaleString('sl-SI') }}</b> {{ izdelkov(results.length).replace(/^\d+ /, '') }}</template>
        </p>
        <button type="button" class="btn filters-btn" @click="sheetOpen = true">
          <Icon name="filter" :size="16" />Filtri<span v-if="filterCount" class="badge">{{ filterCount }}</span>
        </button>
        <label class="sort">
          <Icon name="sort" :size="16" />
          <span class="sr">Razvrsti</span>
          <select v-model="f.sort">
            <option v-for="s in SORTS" :key="s.id" :value="s.id">{{ s.label }}</option>
          </select>
          <Icon name="chevron" :size="14" />
        </label>
      </div>

      <div v-if="filterCount" class="active">
        <button v-for="s in f.stores" :key="s" type="button" class="pill" @click="toggleStore(s)">{{ STORES.find(x => x.id === s)?.label }}<Icon name="close" :size="12" /></button>
        <button v-for="c in f.cats" :key="c" type="button" class="pill" :style="{ '--crate': crate(c) }" @click="toggleCat(c)"><i class="sw" />{{ catLabel(c) }}<Icon name="close" :size="12" /></button>
        <button v-if="f.min != null" type="button" class="pill" @click="f.min = null">od {{ price(f.min) }}<Icon name="close" :size="12" /></button>
        <button v-if="f.max != null" type="button" class="pill" @click="f.max = null">do {{ price(f.max) }}<Icon name="close" :size="12" /></button>
        <button v-if="f.disc" type="button" class="pill" @click="f.disc = 0">vsaj −{{ f.disc }} %<Icon name="close" :size="12" /></button>
        <button v-if="f.when !== 'all'" type="button" class="pill" @click="f.when = 'all'">{{ f.when === 'today' ? 'velja danes' : 'kmalu' }}<Icon name="close" :size="12" /></button>
        <button v-if="f.onlydisc" type="button" class="pill" @click="f.onlydisc = false">samo popusti<Icon name="close" :size="12" /></button>
        <button v-if="f.nocard" type="button" class="pill" @click="f.nocard = false">brez kartice<Icon name="close" :size="12" /></button>
        <button v-if="f.fav" type="button" class="pill" @click="f.fav = false">priljubljeni<Icon name="close" :size="12" /></button>
        <button type="button" class="pill clear-all" @click="reset">Počisti vse</button>
      </div>

      <div v-if="error" class="state">
        <Logo :size="44" board="#1d2421" ink="#eef0ec" />
        <h2>Akcij trenutno ni mogoče naložiti</h2>
        <p>Preverite povezavo in osvežite stran. ({{ error }})</p>
      </div>
      <div v-else-if="loading" class="grid" aria-hidden="true">
        <div v-for="i in 10" :key="i" class="skeleton-card" />
      </div>
      <div v-else-if="!results.length" class="state">
        <Logo :size="44" board="#1d2421" ink="#eef0ec" />
        <h2>Na tej stojnici je prazno</h2>
        <p v-if="f.fav && !favs.size">Še nimate priljubljenih. Tapnite srček na akciji, da jo shranite.</p>
        <p v-else>Nobena akcija ne ustreza izbranim filtrom{{ f.q ? ` in iskanju »${f.q}«` : '' }}.</p>
        <button type="button" class="btn solid" @click="reset">Počisti filtre</button>
      </div>
      <div v-else class="grid">
        <template v-for="(o, i) in visible" :key="o.id">
          <h2 v-if="i === firstLater" class="group-head">
            <Icon name="clock" :size="16" />Prihaja v naslednjih dneh<span class="n">{{ laterCount }}</span>
          </h2>
          <OfferCard
            :offer="o"
            :today="today"
            :favourite="favs.has(o.id)"
            :vt="vtName(o, i)"
            @toggle-fav="toggleFav(o.id)"
          />
        </template>
      </div>
      <div ref="sentinel" class="sentinel" />
      <p v-if="visible.length && visible.length < results.length" class="more">
        <button type="button" class="btn" @click="shown += PAGE">Pokaži več ({{ results.length - visible.length }})</button>
      </p>
    </main>
  </div>

  <footer class="site-foot">
    <div class="site-foot-in">
      <div class="site-foot-brand">
        <Logo :size="26" />
        <span class="word">Katalogi <em>na kratko</em></span>
      </div>
      <p>
        Vse akcije Lidla, Spara in Eurospina na enem mestu, vsako jutro sveže. Popust izračunamo sami iz redne
        in akcijske cene. Cene so povzete s spletnih strani trgovin in se lahko v posamezni trgovini razlikujejo;
        velja cena na polici.
      </p>
      <p>Spar: podatki iz SPAR Online, zato nekatere akcije iz letaka morda manjkajo. Hofer: kmalu.</p>
      <p class="src">
        Viri:
        <template v-for="(s, i) in STORES.filter(x => meta?.stores[x.id]?.source)" :key="s.id">
          <a :href="meta!.stores[s.id]!.source" target="_blank" rel="noopener noreferrer">{{ s.label }}</a><span v-if="i < STORES.filter(x => meta?.stores[x.id]?.source).length - 1" aria-hidden="true"> · </span>
        </template>
        · Slike so last trgovin.
      </p>
    </div>
  </footer>
</template>
