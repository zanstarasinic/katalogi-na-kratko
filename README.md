# Katalogi na kratko

Every current discount at Lidl, Spar, Eurospin and Hofer on one page, with filters by
store, category, price and discount. A Python job refreshes the data once a day, and a
static Vue site reads it. There is no server and no database, and it costs nothing to run
(GitHub Actions + GitHub Pages on a public repository).

```
scraper/
  stores/        one module per store: fetch() + normalize()
  categories/    categories.json (our 16) + one mapping file per store + keywords.json
  model.py       the shared offer record (money handled as integer cents internally)
  checks.py      store-level and item-level checks
  categorize.py  store mapping → name keywords → "drugo"
  run.py         runs the daily steps
  tests/         saved sample responses per store + parser/rule tests
web/             Vue 3 + Vite + TypeScript site, plain CSS
data/            offers.json, meta.json, history/YYYY-MM-DD.json
.github/workflows/daily.yml
```

## Run locally

```bash
# scraper (Python 3.11+, standard library only)
pip install -r requirements-dev.txt
python -m pytest -q scraper/tests      # parsers against saved samples, no network
python -m scraper.run                  # all enabled stores → data/
python -m scraper.run --stores lidl    # one store (e.g. from the Raspberry Pi)

# site
cd web
npm install
npm run dev        # http://localhost:5173, serves ../data/ as /data/
npm test
npm run build      # dist/ including dist/data/{offers,meta}.json
```

## Publish on GitHub Pages

1. Create a **public** repository and push this folder to `main`.
2. Settings → Pages → Source: **GitHub Actions**.
3. Actions → *daily* → *Run workflow* once. After that it runs every morning.

The workflow tests the parsers, scrapes, commits `data/`, builds the site with the
base path GitHub Pages reports (`/` on a custom domain, `/<repo>/` otherwise) and deploys it. If any store fails, the job still publishes (with
that store's previous offers) and then fails, so GitHub emails you.
Custom domain: kataloginakratko.si (set in Settings → Pages; DNS A records to GitHub Pages).

## Data rules

- `discount_pct` is computed by us from the two prices (floored), never copied from the store.
- A discount below 1 % counts as none; one-price items are `kind: "special"` ("Posebna ponudba").
- When a store gives both a normal and a card price, the card price is the offer and `requires_card` is true.
- Items with a zero/negative price, or a regular price below the sale price, are dropped.
- A store that is unreachable, returns nothing, or drops by more than half keeps yesterday's offers;
  `meta.json` marks it `ok: false` and the site shows a stale-data notice.
- `offers.json` holds offers valid today or starting within 7 days. Dates are Ljubljana time.
- `history/` keeps only id, prices and dates per day, for the later "is it worth it" score.

## Store status (checked 9 Oct 2026)

| Store | Source | Status |
|---|---|---|
| Lidl | `lidl.si/q/api/search` JSON, 60 per page, paged with `offset` | ✅ ~460 current offers. Note: the endpoint returns 401 if `Accept: application/json` is sent with a non-browser UA, so the fetcher sends the default `Accept`. |
| Spar | SPAR Online category pages; products are in the Next.js flight data | ✅ ~790 promotions from *Aktualno → Iz letaka* and *Akcije dom in prosti čas*. Paging is `?currentPage=N` (50 per page). Whether these categories hold **every** promotion is still open; add paths to `CATEGORIES` in `stores/spar.py` if not. |
| Eurospin | `eurospin.si/akcije/` plain HTML | ✅ ~170 offers. Image addresses **are** present. Categories come from one `?category_filter=` page per category (≈24 requests/day). |
| Hofer | `hofer.si/posebna-ponudba/…` | ⛔ Disabled (`ENABLED = False`). hofer.si answers plain HTTP clients with an Akamai 403, and the before-and-after price source is still unknown. See `stores/hofer.py`. |

## Adding or fixing a store

Save a fresh response into `scraper/tests/samples/`, adjust the parser until the tests pass,
and add mapping rules to `scraper/categories/<store>.json`. The daily log prints how many
items landed in "drugo", so mappings can be improved over time. The frontend never changes.

Prices come from the stores' websites and may differ in a given shop. Images are linked,
not copied. Each store's terms of use should be read before the site is promoted.
