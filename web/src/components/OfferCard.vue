<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Offer } from '../types'
import { storeById } from '../stores'
import { crate } from '../theme'
import { shortDate } from '../format'
import Icon from './Icon.vue'

const props = defineProps<{ offer: Offer; today: string; favourite: boolean; vt?: string }>()
defineEmits<{ toggleFav: [] }>()

const store = computed(() => storeById[props.offer.store])
const upcoming = computed(() => !!props.offer.valid_from && props.offer.valid_from > props.today)
const endsToday = computed(() => props.offer.valid_to === props.today)
const shape = computed(() => upcoming.value ? 'later' : props.offer.kind === 'discount' ? 'discount' : 'special')
const imgFailed = ref(false)

const euros = computed(() => Math.floor(props.offer.price))
const cents = computed(() => String(Math.round((props.offer.price - euros.value) * 100)).padStart(2, '0'))
// Some stores shout in capitals; show those names in sentence case.
const name = computed(() => {
  const n = props.offer.name.trim()
  return n === n.toUpperCase() && /[A-ZČŠŽ]{3}/.test(n) ? n.charAt(0) + n.slice(1).toLowerCase() : n
})
// Spar uses "Ostalo" ("other") as a placeholder brand; it is not a brand.
const showBrand = computed(() => {
  const b = props.offer.brand?.trim()
  return !!b && b.toLowerCase() !== 'ostalo' && !props.offer.name.toLowerCase().includes(b.toLowerCase())
})
const regular = computed(() => props.offer.regular_price?.toFixed(2).replace('.', ','))
</script>

<template>
  <article class="offer" :style="{ '--crate': crate(offer.category), viewTransitionName: vt }">
    <div class="photo">
      <img
        v-if="offer.image_url && !imgFailed"
        :src="offer.image_url"
        alt=""
        loading="lazy"
        decoding="async"
        referrerpolicy="no-referrer"
        @error="imgFailed = true"
      />
      <span v-else class="photo-empty" aria-hidden="true">{{ store.label }}</span>

      <span v-if="offer.kind === 'discount'" class="pct" :aria-label="`Popust ${offer.discount_pct} odstotkov`">
        −{{ offer.discount_pct }}<small>%</small>
      </span>

      <button
        class="fav"
        :class="{ on: favourite }"
        type="button"
        :aria-pressed="favourite"
        :aria-label="favourite ? 'Odstrani iz priljubljenih' : 'Shrani med priljubljene'"
        @click="$emit('toggleFav')"
      >
        <Icon name="heart" :size="17" />
      </button>

      <div class="stake" :class="shape">
        <span v-if="offer.requires_card" class="tab">z {{ store.card }}</span>
        <span v-else-if="offer.min_quantity > 1" class="tab">ob nakupu {{ offer.min_quantity }}</span>
        <span class="price" :aria-label="`Cena ${euros},${cents} evra`">
          {{ euros }}<span class="cents">,{{ cents }}</span><span class="eur">€</span>
        </span>
      </div>
    </div>

    <div class="body">
      <div class="line">
        <span class="store" :style="{ '--store': store.color }">{{ store.label }}</span>
        <s v-if="regular" class="was" :aria-label="`Redna cena ${regular} evra`">{{ regular }} €</s>
        <span v-else-if="!upcoming" class="kind">posebna ponudba</span>
      </div>
      <h3 class="name" :title="name">
        <span v-if="showBrand" class="brand">{{ offer.brand }}</span>
        {{ name }}
      </h3>
      <p class="meta">
        <template v-if="offer.package">{{ offer.package }}</template>
        <template v-if="offer.package && offer.unit_price"> · </template>
        <template v-if="offer.unit_price">{{ offer.unit_price }}</template>
      </p>
      <div class="card-foot">
        <span v-if="upcoming" class="when later">od {{ shortDate(offer.valid_from) }}</span>
        <span v-else-if="endsToday" class="when last">samo še danes</span>
        <span v-else-if="offer.valid_to" class="when">do {{ shortDate(offer.valid_to) }}</span>
        <span v-else />
        <a
          v-if="offer.product_url"
          :href="offer.product_url"
          target="_blank"
          rel="noopener noreferrer"
          class="go"
          :aria-label="`${offer.name} na strani ${store.label}`"
        >{{ store.label }}<Icon name="external" :size="13" /></a>
      </div>
    </div>
  </article>
</template>

<style scoped>
.offer {
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--paper);
  border: 1px solid var(--stone-300);
  border-top: 0;
  border-radius: 12px;
  overflow: hidden;
  contain: layout paint;
}
/* the crate edge */
.offer::before {
  content: "";
  height: 6px;
  background: var(--crate);
  flex-shrink: 0;
}

.photo {
  position: relative;
  aspect-ratio: 5 / 4;
  min-height: 0;
  background: #fff;
  display: grid;
  place-items: center;
  border-bottom: 1px solid var(--stone-150);
}
.photo img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 12px 12px 24px;
}
.photo-empty {
  font-weight: 800;
  font-stretch: 80%;
  font-size: 1.1rem;
  color: var(--stone-300);
  text-transform: uppercase;
  letter-spacing: .04em;
}

/* paprika discount corner */
.pct {
  position: absolute;
  top: 0;
  right: 0;
  background: var(--paprika);
  color: #fff;
  font-weight: 900;
  font-stretch: 78%;
  font-size: 1.3rem;
  line-height: 1;
  padding: 7px 10px 8px 12px;
  border-radius: 0 0 0 14px;
  letter-spacing: -.01em;
}
.pct small { font-size: .7em; margin-left: 1px; }

.fav {
  position: absolute;
  top: 8px;
  left: 8px;
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border: 1px solid var(--stone-150);
  border-radius: 50%;
  background: rgb(255 255 255 / .92);
  color: var(--slate-500);
  cursor: pointer;
  transition: color .15s, transform .2s cubic-bezier(.22, 1, .36, 1);
}
.fav:hover { color: var(--slate-900); }
.fav:active { transform: scale(.88); }
.fav.on { color: var(--paprika); }
.fav.on :deep(path) { fill: currentColor; }

/* the price stake */
.stake {
  position: absolute;
  left: 10px;
  bottom: 0;
  transform: translateY(50%);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  z-index: 1;
}
.price {
  display: flex;
  align-items: baseline;
  background: var(--slate-900);
  color: #fff;
  font-weight: 900;
  font-stretch: 70%;
  font-size: 2rem;
  line-height: 1;
  letter-spacing: -.01em;
  padding: 6px 11px 7px 10px;
  border-radius: 8px;
}
.cents { font-size: .62em; align-self: flex-start; margin-top: .12em; letter-spacing: 0; }
.eur { font-size: .5em; font-weight: 700; margin-left: 3px; color: var(--stone-300); }

/* notch: a discount stake has its top-right corner bitten off */
.discount .price {
  clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 0 100%);
}
/* special offer: a round yellow coin */
.special .price {
  background: var(--yolk);
  color: var(--slate-900);
  border-radius: 999px;
  padding-inline: 14px;
}
.special .eur { color: var(--slate-700); }
/* starts later: a dashed outline stake */
.later .price {
  background: #fff;
  color: var(--slate-900);
  outline: 2px dashed var(--slate-900);
  outline-offset: -2px;
}
.later .eur { color: var(--slate-500); }

.tab {
  background: var(--yolk);
  color: var(--slate-900);
  font-size: .68rem;
  font-weight: 800;
  padding: 3px 7px 4px;
  border-radius: 6px 6px 0 0;
  margin-left: 6px;
  letter-spacing: .01em;
  white-space: nowrap;
}

.body {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 30px 12px 12px;
  flex: 1;
}
.line { display: flex; justify-content: space-between; align-items: baseline; gap: 6px; }
.store {
  font-size: .7rem;
  font-weight: 800;
  letter-spacing: .07em;
  text-transform: uppercase;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}
.store::before {
  content: "";
  width: 7px;
  height: 7px;
  border-radius: 2px;
  background: var(--store);
}
.was {
  color: var(--slate-500);
  font-size: .82rem;
  font-weight: 600;
  text-decoration-thickness: 1.5px;
  text-decoration-color: var(--paprika);
}
.kind { font-size: .7rem; font-weight: 700; color: var(--slate-500); }
.name {
  margin: 0;
  font-size: .9rem;
  font-weight: 650;
  line-height: 1.28;
  height: calc(1.28em * 2);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-wrap: pretty;
}
.brand { font-weight: 800; margin-right: .25em; }
.meta {
  margin: 0;
  min-height: 1.3em;
  font-size: .76rem;
  color: var(--slate-500);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.card-foot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 6px;
  margin-top: auto;
  padding-top: 6px;
  border-top: 1px solid var(--stone-150);
  font-size: .76rem;
}
.when { font-weight: 700; color: var(--slate-700); }
.when.later { color: var(--slate-900); background: var(--stone-150); padding: 1px 6px; border-radius: 5px; }
.when.last { color: var(--paprika); }
.go {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--slate-700);
  font-weight: 700;
  text-decoration: none;
  padding: 4px 0;
}
.go:hover { color: var(--slate-900); text-decoration: underline; text-underline-offset: 3px; }

@media (max-width: 520px) {
  .photo img { padding: 8px 8px 20px; }
  .price { font-size: 1.7rem; padding: 5px 9px 6px 8px; }
  .pct { font-size: 1.15rem; padding: 6px 8px 7px 10px; }
  .stake { left: 8px; }
  .body { padding: 26px 10px 10px; }
  .name { font-size: .84rem; }
  .fav { width: 32px; height: 32px; top: 6px; left: 6px; }
  .go { font-size: 0; gap: 0; }
  .go :deep(svg) { width: 16px; height: 16px; }
}
</style>
