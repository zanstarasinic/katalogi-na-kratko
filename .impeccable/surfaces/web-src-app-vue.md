---
version: 1
slug: "web-src-app-vue"
primary_target: "web/src/App.vue"
related_targets: ["web/src/components/OfferCard.vue","web/src/style.css"]
---

# Surface brief: offer browser (web/src/App.vue)

Scope: the single-page offer browser. Visitor mode: Operate.
Audience/job: Slovene weekly planners on phones finding this week's cheapest offers across Lidl, Spar, Eurospin (Hofer later).
Constraints: light only, Slovene only, store colours only as small tags, price is always the most visible element.

## Direction contract

THESIS: Every offer is a market-stall price stake: the price you pay set chalk-white on slate, planted on the photo's edge, inside a crate coloured by category. It refuses the category's anonymous white cards with a pink % pill.

OWN-WORLD: Slate #1d2421 header, price stakes, and active states; cool limestone ground #eef0ec; one six-step slate-to-stone neutral ramp; paprika #e5372b reserved for the discount corner; sixteen produce crate hues, used only on the crate edge and the chip swatch. Type: Archivo (variable width), with condensed black tabular numerals for prices. One-pixel hairlines, no shadows except the lifted sheet.

STORY: The visitor understands "all chains, this week, honest %", narrows by crate (category) or search, compares stakes, favourites, leaves.

FIRST VIEWPORT: Slate header with the logo stake, wordmark, freshness and search; crate-colour chip rail; store toggles with counts; a count line plus Filtri; two-column cards, each with a 6px crate edge, photo, slate price stake overlapping the photo's bottom-left, the paprika % corner at top-right, store and struck regular price, name clamped to two lines, unit price, and date.

FORM: Tržnica (Ljubljana market stall), position 3 of 7 on the grounded list, seed ba7aff7c. Signature move: stakes re-plant through a View Transition when sorting or filtering. Shape encodes kind: notched stake = discount, round yellow coin = Posebna ponudba, dashed stake = starts later.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
