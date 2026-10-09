---
name: Katalogi na kratko
description: Every current supermarket offer in Slovenia on one page, set out like price stakes on a market stall.
colors:
  slate-900: "#1d2421"
  slate-700: "#3a4540"
  slate-500: "#5c6761"
  stone-300: "#c9cfc9"
  stone-150: "#e2e6e1"
  stone-50: "#eef0ec"
  paper: "#ffffff"
  bar-well: "#2c3531"
  paprika: "#d6311f"
  yolk: "#f7c51e"
  fresh-green: "#4cc26b"
  notice-cream: "#fff3cc"
  notice-rule: "#ecd27a"
  notice-ink: "#4a3b06"
  crate-sadje-zelenjava: "#2f8a45"
  crate-meso-ribe: "#a8322d"
  crate-mlecni-jajca: "#f2c230"
  crate-kruh-pekovski: "#c98a3d"
  crate-shramba: "#ef7d1a"
  crate-zamrznjeno: "#3a8fc9"
  crate-sladko-slano: "#8a4b2f"
  crate-pijace: "#1f9a9a"
  crate-alkohol: "#6a2c5e"
  crate-nega-zdravje: "#c2417a"
  crate-cistila-gospodinjstvo: "#4a6fd1"
  crate-otroci: "#ff8fa3"
  crate-ljubljencki: "#7b8f2a"
  crate-dom-vrt-orodje: "#5b6b73"
  crate-oblacila: "#7a5cc9"
  crate-drugo: "#9aa39d"
  store-lidl: "#0050aa"
  store-spar: "#d8232a"
  store-eurospin: "#1a3e8c"
  store-hofer: "#f39200"
typography:
  display:
    fontFamily: "Archivo Variable, system-ui, sans-serif"
    fontSize: "2rem"
    fontWeight: 900
    lineHeight: 1
    letterSpacing: "-0.01em"
    fontFeature: "tnum"
    fontVariation: "'wdth' 70"
  discount:
    fontFamily: "Archivo Variable, system-ui, sans-serif"
    fontSize: "1.3rem"
    fontWeight: 900
    lineHeight: 1
    letterSpacing: "-0.01em"
    fontFeature: "tnum"
    fontVariation: "'wdth' 78"
  wordmark:
    fontFamily: "Archivo Variable, system-ui, sans-serif"
    fontSize: "1.32rem"
    fontWeight: 860
    letterSpacing: "-0.015em"
    fontVariation: "'wdth' 82"
  headline:
    fontFamily: "Archivo Variable, system-ui, sans-serif"
    fontSize: "1.35rem"
    fontWeight: 860
    fontVariation: "'wdth' 85"
  title:
    fontFamily: "Archivo Variable, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 900
    fontFeature: "tnum"
    fontVariation: "'wdth' 80"
  body:
    fontFamily: "Archivo Variable, system-ui, sans-serif"
    fontSize: "0.9rem"
    fontWeight: 650
    lineHeight: 1.28
    fontFeature: "tnum"
  body-small:
    fontFamily: "Archivo Variable, system-ui, sans-serif"
    fontSize: "0.76rem"
    fontWeight: 400
    fontFeature: "tnum"
  label:
    fontFamily: "Archivo Variable, system-ui, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 800
    letterSpacing: "0.07em"
  count:
    fontFamily: "Archivo Variable, system-ui, sans-serif"
    fontSize: "0.82em"
    fontWeight: 600
    fontFeature: "tnum"
rounded:
  swatch: "3px"
  tab: "6px"
  sm: "8px"
  md: "10px"
  lg: "12px"
  corner: "14px"
  sheet: "18px"
  pill: "999px"
spacing:
  xs: "6px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "24px"
  2xl: "32px"
  section: "72px"
components:
  top-bar:
    backgroundColor: "{colors.slate-900}"
    textColor: "{colors.paper}"
    height: "64px"
    padding: "10px 24px"
  search-field:
    backgroundColor: "{colors.bar-well}"
    textColor: "{colors.paper}"
    rounded: "{rounded.md}"
    height: "44px"
    padding: "0 8px 0 14px"
  search-field-focus:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.slate-900}"
  offer-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.slate-900}"
    rounded: "{rounded.lg}"
    padding: "30px 12px 12px"
  stake-discount:
    backgroundColor: "{colors.slate-900}"
    textColor: "{colors.paper}"
    typography: "{typography.display}"
    rounded: "{rounded.sm}"
    padding: "6px 11px 7px 10px"
  stake-special:
    backgroundColor: "{colors.yolk}"
    textColor: "{colors.slate-900}"
    typography: "{typography.display}"
    rounded: "{rounded.pill}"
    padding: "6px 14px 7px 14px"
  stake-later:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.slate-900}"
    typography: "{typography.display}"
    rounded: "{rounded.sm}"
    padding: "6px 11px 7px 10px"
  stake-tab:
    backgroundColor: "{colors.yolk}"
    textColor: "{colors.slate-900}"
    rounded: "{rounded.tab}"
    padding: "3px 7px 4px"
  discount-corner:
    backgroundColor: "{colors.paprika}"
    textColor: "{colors.paper}"
    typography: "{typography.discount}"
    rounded: "{rounded.corner}"
    padding: "7px 10px 8px 12px"
  button:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.slate-900}"
    rounded: "{rounded.md}"
    height: "40px"
    padding: "0 16px"
  button-solid:
    backgroundColor: "{colors.slate-900}"
    textColor: "{colors.paper}"
    rounded: "{rounded.md}"
    height: "40px"
    padding: "0 16px"
  button-solid-hover:
    backgroundColor: "{colors.slate-700}"
  button-badge:
    backgroundColor: "{colors.paprika}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
    height: "20px"
    padding: "0 6px"
  crate-chip:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.slate-900}"
    rounded: "{rounded.pill}"
    height: "36px"
    padding: "0 12px"
  crate-chip-on:
    backgroundColor: "{colors.slate-900}"
    textColor: "{colors.paper}"
  store-chip:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.slate-900}"
    rounded: "{rounded.sm}"
    height: "34px"
    padding: "0 6px"
  filter-row:
    backgroundColor: "transparent"
    textColor: "{colors.slate-900}"
    rounded: "{rounded.sm}"
    padding: "7px 8px"
  filter-row-hover:
    backgroundColor: "{colors.stone-150}"
  filter-row-on:
    backgroundColor: "{colors.slate-900}"
    textColor: "{colors.paper}"
  active-pill:
    backgroundColor: "{colors.slate-900}"
    textColor: "{colors.paper}"
    rounded: "{rounded.pill}"
    height: "30px"
    padding: "0 9px 0 11px"
  segmented:
    backgroundColor: "{colors.stone-150}"
    textColor: "{colors.slate-700}"
    rounded: "{rounded.md}"
    padding: "3px"
  segmented-on:
    backgroundColor: "{colors.slate-900}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    height: "34px"
  price-field:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.slate-900}"
    rounded: "{rounded.md}"
    height: "40px"
    padding: "0 10px"
  notice:
    backgroundColor: "{colors.notice-cream}"
    textColor: "{colors.notice-ink}"
    rounded: "{rounded.md}"
    padding: "10px 14px"
  filter-sheet:
    backgroundColor: "{colors.stone-50}"
    textColor: "{colors.slate-900}"
    rounded: "{rounded.sheet}"
    padding: "0 20px"
---

# Design System: Katalogi na kratko

## Overview

**Creative North Star: "Tržnica"**

The page is a Ljubljana market stall seen from the aisle. A slate header and slate price boards sit over a cool limestone ground, and every offer is a crate whose painted top edge tells you what is inside. The price you pay is chalk-white on slate, condensed and black, planted half on the photo and half on the card. Everything else steps back: hairline stone borders, small type for the store and dates, and colour kept in narrow strips and dots so a phone screen can carry many offers at once.

The system is dense and practical. It is built for scanning with one hand, so the order of attention is fixed: price stake first, then the paprika discount corner, then the product name, then store and dates. Slate does double duty as ink and as the "chosen" state. Selected crates, stores, segments and filter pills all go slate with white text, which makes the stall's boards and the visitor's choices one family. Yolk is the market's chalk-highlight: it marks the wordmark's second half, loyalty-card tabs, the round coin for single-price offers, and the knobs of sliders and switches.

The world rejects the generic offer-aggregator card (white tile, pink percentage pill) and any look that leans toward one chain's livery. Store colours are borrowed marks and appear only as tiny dots.

**Key Characteristics:**
- Slate (#1d2421) header, footer, price stakes and every selected state; limestone (#eef0ec) ground.
- One cool slate-to-stone neutral ramp in six steps, plus white paper for cards and fields.
- Sixteen produce-crate hues, each living only on a 6px card edge or an 11px swatch.
- Archivo Variable with narrow, black, tabular numerals for prices and counts.
- Stake shape tells the offer type: notched board for discounts, yolk coin for single-price offers, dashed board for offers that start later.
- Flat hairline surfaces; the phone filter sheet is the only thing lifted.
- Sorting and filtering re-plant the cards through a View Transition.

## Colors

A cool, nearly colourless stall (slate and limestone) carrying two hot accents and a box of small produce hues.

### Primary
- **Market Slate** (slate-900): Header bar, footer, price-stake boards, solid buttons, and the fill of every selected chip, row, segment and active-filter pill. It is also body ink and the focus-ring colour on light ground. `theme-color` and the favicon tile use it too.

### Secondary
- **Paprika** (paprika): The discount corner on each card. It also carries small loss or urgency marks: the line through the regular price, "samo še danes" (last day), the filled heart of a saved offer, the filter-count badge, and the text caret. It never fills a surface larger than the discount corner.

### Tertiary
- **Yolk** (yolk): The highlight that reads on slate. Used for "na kratko" in the wordmark, the loyalty-card and multi-buy tab above a stake, the round coin of a "posebna ponudba", the slider thumb, the checked switch knob, text selection, and the focus ring inside the dark bar and footer.

### Neutral
- **Slate 700** (slate-700): Secondary text, filter group headings, segment labels, hover fill for solid buttons.
- **Slate 500** (slate-500): Tertiary text: counts, struck regular price, package and unit-price meta, placeholders, the euro sign on later stakes.
- **Stone 300** (stone-300): The hairline. Card, chip, button and field borders; the euro sign on slate stakes; counts inside a selected row; the default swatch.
- **Stone 150** (stone-150): Inner dividers (photo base, card foot, filter blocks), row hover fill, segmented-control track, slider track, the "od" date chip.
- **Limestone** (stone-50): The page ground and the filter sheet's surface.
- **Paper** (paper): Card bodies, photo wells, chips, buttons and fields. All text on slate is paper white.
- **Bar Well** (bar-well): The search field at rest inside the slate bar; it turns paper white on focus.

### Crate hues
One produce-market hue per category (`crate-*`, keyed by category id), from leaf green for fruit and veg to plum for alcohol. They appear only as the 6px crate edge at the top of a card, the 11px rounded swatch in category rows, chips and pills, and nowhere else.

### Store marks
Lidl, Spar, Eurospin and Hofer colours (`store-*`) are the chains' own. They appear only as a 7px square before the store name on a card and an 8–11px dot in the store filters.

### Status
- **Fresh Green** (fresh-green): The single "data is fresh" dot in the header.
- **Notice Cream / Rule / Ink** (notice-cream, notice-rule, notice-ink): The one stale-data notice strip above the grid.

### Named Rules
**The Slate Means Chosen Rule.** Any selected state is a slate fill with white text, and a selected swatch or dot gets a 2px white ring. No other colour signals selection.

**The Crate Edge Rule.** Category hues are strips and swatches, never fields, text or backgrounds. If a crate colour covers more than a 6px edge or an 11px square, it is wrong.

**The Borrowed Livery Rule.** Store colours stay at dot size. No chain's colour ever tints a card, header or button, so no store looks favoured.

**The Paprika Bite Rule.** Paprika is the discount corner plus small marks of loss or urgency. It is never a button, a background or a heading colour.

## Typography

**Display Font:** Archivo Variable (with system-ui, sans-serif), self-hosted, weight 100–900, width 62–125%
**Body Font:** Archivo Variable (same family)

**Character:** One grotesque used across its width axis. Numbers and the wordmark are pulled narrow (70–85% width) and set very heavy, like hand-lettered stall boards. Reading text stays at normal width and medium weight. Tabular figures are on everywhere from `:root`.

### Hierarchy
- **Display / Price stake** (900, 2rem, line-height 1, width 70%): The price on every card. Cents sit raised at 0.62em; the euro sign is 0.5em at weight 700 in a quieter colour. On phones it drops to 1.7rem.
- **Discount corner** (900, 1.3rem, width 78%): "−NN%" in the paprika corner, with the % at 0.7em.
- **Wordmark** (860, 1.32rem, width 82%, −0.015em): "Katalogi *na kratko*" in header and footer, the second half in yolk. 1.12rem on small phones.
- **Headline** (860, 1.3–1.35rem, width 85%): Empty and error state headings, the filter sheet title.
- **Title / Result count** (900, 1.5rem, width 80%): The number in "N izdelkov"; the word after it is 0.95rem slate-700.
- **Body / Offer name** (650, 0.9rem, line-height 1.28): Product names, clamped to two lines with a fixed two-line height so cards align; the brand is weight 800. Filter rows use 0.9–0.95rem at 560–750.
- **Body small / Meta** (400–700, 0.76rem): Package, unit price, validity dates, the store link.
- **Label** (800, 0.7–0.78rem, 0.07em tracking, uppercase): Filter group headings ("TRGOVINE") and the store name on cards. Uppercase is used only for these.
- **Count** (600, 0.82em, slate-500): Trailing counts in chips and rows.

### Named Rules
**The Narrow Numerals Rule.** Prices, percentages and totals are condensed (70–80% width) and black (900). Running text is never condensed.

**The Price Wins Rule.** On any card the price stake is the largest, heaviest type. Nothing else on the card goes above 1.3rem.

## Layout

Desktop is a 1400px max-width shell with 24px gutters: a sticky 268px filter column and a fluid offer grid, 32px apart. The grid auto-fills columns of at least 208px with an 18px row gap and 16px column gap. The 64px slate bar is sticky and holds brand, a search field up to 620px wide, and the freshness line on the right.

At 1023px and below the shell collapses to one column with 16px gutters. The search drops to its own row under the brand. A horizontally scrolling crate-chip rail and a store strip appear under the bar so category and store choices stay on the first screen, and the filter column becomes a bottom sheet behind a "Filtri" button. At 520px and below the grid is always two columns (14px rows, 10px columns), and the count, Filtri and sort controls rearrange into a two-column tool grid.

Spacing is small and steady: 6–8px inside chips and rows, 12px card padding, 16px between filter blocks, 24px gutters, 72px before the footer. Cards are sized for density: many offers per screen beats air.

## Elevation & Depth

The stall is flat. Surfaces sit on limestone, separated by 1px stone hairlines and by tone (paper on limestone, slate on everything). Depth comes from overlap instead: the price stake straddles the line between photo and card body, translated 50% down.

### Shadow Vocabulary
- **Lifted sheet** (`box-shadow: 0 -12px 40px rgb(29 36 33 / .22)`): The phone filter sheet only, over a slate scrim at 45%.
- **Selection ring** (`box-shadow: 0 0 0 2px #fff`): A white ring around a swatch or dot inside a selected slate control. It is a ring, not a shadow.

### Named Rules
**The Lifted Sheet Rule.** Only the filter sheet casts a shadow. Cards, chips, buttons and the bar never do.

## Shapes

Corners are soft and graded by size: 3px swatches, 6px tabs, 8px stakes and filter rows, 10px buttons, fields and controls, 12px cards, 18px for the top of the sheet, and full pills for chips and active-filter tags. Borders are 1px stone-300; the card drops its top border so the 6px crate edge forms its lid.

Shape encodes offer kind on the price stake:
- **Notched board**, a discount: the top-right corner is clipped off by 10px.
- **Round yellow coin**, a single-price "posebna ponudba": yolk fill, fully rounded.
- **Dashed board**, starts later: white fill with a 2px dashed slate outline.

The paprika corner is the mirror shape: square to the card's top-right, rounded 14px on the bottom-left only. The logo is the same stake object, a notched board on a post with a geometric %.

### Named Rules
**The Shape Encodes Kind Rule.** Notch, coin and dash are the only stake variants, and each means one offer type. Never use them as decoration.

## Components

### Buttons
Plain and firm, like a stall-keeper's chalkboard.
- **Shape:** gently rounded (10px), 40px tall (48px in the sheet footer).
- **Default:** paper fill, 1px stone-300 border, slate text at 750 weight; hover darkens the border to slate-500. Disabled drops to transparent with slate-500 text.
- **Solid:** slate fill, white text; hover lifts to slate-700. Used for "Pokaži N izdelkov", "Počisti filtre".
- **Badge:** a paprika 20px pill holding the active filter count on the Filtri button.
- **Icon button:** a 40px square with the same border, used to close the sheet.

### Chips
- **Crate chip (phone rail):** 36px pill, paper with stone border, swatch + label + count. Selected: slate fill, white text, ringed swatch. Empty categories fade to 40% opacity.
- **Store chip (phone strip):** 34px, 8px radius, store dot + label + count. A store not yet live has a dashed border, transparent fill and "kmalu".
- **Active-filter pill:** 30px slate pill with an optional swatch and a 12px close icon; "Počisti vse" is a bare underlined text pill.

### Cards / Containers
- **Offer card:** 12px corners, paper body, 1px stone-300 border with no top border, and a 6px crate-colour edge as the lid. The photo well is 5:4, white, image contained with extra bottom padding so the stake never covers the product. A 34px translucent-white round heart sits top-left; it turns paprika and fills when saved.
- **Card body:** store label and struck regular price (paprika strike line) on one row, two-line name, one-line meta, then a hairline-topped foot with the validity date and an external-link to the store page (icon only on phones).
- **Notice:** the stale-data strip, cream with a straw hairline, 10px radius.
- **Loading:** shimmering ghost cards (0.64 aspect, 12px corners, a 6px stone lid).
- **Empty / error state:** centred logo in slate, condensed headline, one line of slate-700 text, a solid button.

### Inputs / Fields
- **Search (in the bar):** 44px, 10px radius, bar-well fill, muted grey text. On focus it turns paper white with slate text and a 2px yolk outline.
- **Price range:** two 40px paper fields with a stone border and a trailing "€"; focus thickens to a 2px slate border via an inset ring.
- **Discount slider:** 6px track, slate fill to the value, stone-150 beyond; a 22px yolk thumb with a 3px slate border.
- **Segmented control:** stone-150 track with 3px padding, three 34px options; the chosen one is slate.
- **Switch:** 36×22 stone-300 track; checked turns slate with a yolk knob, sliding on `cubic-bezier(.22, 1, .36, 1)`.
- **Sort select:** 40px bordered field, native select restyled, sort icon and chevron.

### Navigation
- **Top bar:** sticky slate, logo stake + wordmark, search, and a freshness line with a green dot and "Posodobljeno **danes ob …**". Focus rings inside the bar are yolk.
- **Filter column / sheet:** grouped blocks (Trgovine, Kategorije, Cena, Najmanj popusta, Veljavnost, toggles) divided by stone-150 hairlines under uppercase labels. Rows are 8px-radius buttons with dot or swatch, label and count; hover is stone-150, selected is slate. On phones the same panel is a bottom sheet (18px top corners, sticky title and footer, slides up in 0.34s).
- **Footer:** slate, wordmark, short honest notes about data sources, white underlined links.

### Price Stake (signature)
The slate board holding the price, pinned 10px from the card's left edge and half over the photo's lower border. Euros are full size; cents are raised and smaller; the euro sign is small and muted. A yolk tab can sit on top of it ("z Lidl Plus", "ob nakupu 2"), squared at the bottom so it reads as part of the board. The notched, coin and dashed variants are described under Shapes.

### Re-plant motion
When filters or sort change, the grid updates inside a View Transition: cards move 0.44s on `cubic-bezier(.22, 1, .36, 1)`, new cards drop in from 14px above at 96% scale, removed cards shrink out in 0.2s. Search typing does not animate, and reduced motion turns it all off.

## Do's and Don'ts

### Do:
- **Do** put every selected state in slate (#1d2421) with white text, and ring its swatch or dot in 2px white.
- **Do** set prices, percentages and totals in Archivo at weight 900 and 70–80% width with tabular figures.
- **Do** keep the price stake the largest element on a card, half over the photo's lower border.
- **Do** choose the stake shape by offer kind: notched for discounts, yolk coin for single-price, dashed for later.
- **Do** separate surfaces with 1px stone hairlines and tone, on a limestone (#eef0ec) ground.
- **Do** use yolk for highlights and focus rings on slate.

### Don't:
- **Don't** use crate hues outside the 6px card edge and the 11px swatch.
- **Don't** let a store colour grow beyond a dot or small square, or tint any surface.
- **Don't** use paprika for buttons, backgrounds or headings; it is the discount corner and small urgency marks only.
- **Don't** add shadows to cards, chips, buttons or the bar; only the phone filter sheet lifts.
- **Don't** condense running text or product names; narrow widths are for numbers and the wordmark.
- **Don't** use the generic aggregator look: a plain white tile with a pink percentage pill.
- **Don't** add a dark theme; the stall is light only.
