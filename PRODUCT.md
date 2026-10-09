# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Slovene household shoppers planning the week's shop, mostly on a phone. They ask "where is
coffee / meat / detergent cheapest this week?", scan many offers quickly, and settle on one or
two stores to visit.

## Product Purpose
Katalogi na kratko shows every current discount at Lidl, Spar, Eurospin and Hofer on one page,
refreshed daily, with filters by store, category, price and discount. Success: a shopper finds
this week's relevant deals across all chains in a minute, without opening four flyers or apps.

## Positioning
All stores, one honest list. Four chains side by side; the discount is computed from the real
regular and sale prices, never copied from store marketing; prices that need a loyalty card are
clearly flagged; no ads; free.

## Operating Context
- Data comes from the stores' websites once a day (static JSON, no backend). A store can be
  stale; the page must say so.
- Offers are either discounts (regular + sale price, computed %) or single-price "Posebna ponudba".
- Offers can be valid now or start within 7 days ("Od" date).
- Typical session: open on phone, narrow by category or search, compare prices, maybe favourite.

## Capabilities and Constraints
- Single page, Vue 3 + Vite + TypeScript, plain CSS, GitHub Pages hosting, zero running cost.
- Filters and sort live in the URL (shareable). Favourites are browser-only.
- ~1,400 offers today; grid loads 60 at a time.
- Hofer is currently disabled (source blocked); Spar data is SPAR Online only.
- Undecided: own domain.

## Brand Commitments
- Name: "Katalogi na kratko" (keep). Logo is to be designed.
- UI language: Slovene only.
- Store brand colours appear only as small tags; the page must never look like any one chain.
- Light mode only for v1.

## Evidence on Hand
- Real daily data in `data/offers.json` and `data/meta.json` (product names, prices, images
  linked from store CDNs, dates).
- No testimonials, user counts, savings totals or press. Do not invent them.

## Product Principles
1. Price first: the number a shopper pays is always the most visible thing.
2. Honest by construction: computed discounts, flagged card prices, visible data freshness.
3. Fast scanning over decoration: many offers per screen, one-hand phone use.
4. Neutral between chains: no store is favoured visually.
