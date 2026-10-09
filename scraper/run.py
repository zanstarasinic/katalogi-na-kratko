"""Daily run: fetch -> normalize -> check -> categorize -> merge -> export.

    python -m scraper.run                 # all stores
    python -m scraper.run --stores lidl   # just one (e.g. from the Raspberry Pi)

Exit code 1 when any store failed (after everything was written), so GitHub emails you.
"""
from __future__ import annotations

import argparse
import json
import sys
import traceback
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

from . import categorize, checks
from .model import STORES, TZ, Offer
from .stores import eurospin, hofer, lidl, spar

MODULES = {"lidl": lidl, "spar": spar, "eurospin": eurospin, "hofer": hofer}
SOURCES = {
    "lidl": "https://www.lidl.si",
    "spar": "https://online.spar.si",
    "eurospin": "https://www.eurospin.si/akcije/",
    "hofer": "https://www.hofer.si",
}
UPCOMING_DAYS = 7
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def _read_json(path: Path, default):
    try:
        return json.loads(path.read_text("utf-8"))
    except (FileNotFoundError, ValueError):
        return default


def _write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n", "utf-8")


def is_current(offer: dict, today: date) -> bool:
    """Valid today, or starting within UPCOMING_DAYS. Expired offers are dropped."""
    horizon = (today + timedelta(days=UPCOMING_DAYS)).isoformat()
    t = today.isoformat()
    if offer.get("valid_to") and offer["valid_to"] < t:
        return False
    if offer.get("valid_from") and offer["valid_from"] > horizon:
        return False
    return True


def scrape_store(store: str, today: date, previous_count: int) -> tuple[list[Offer], int]:
    """Run one store end to end. Raises on any store-level failure."""
    mod = MODULES[store]
    raw = mod.fetch()
    offers = mod.normalize(raw, today)
    offers, dropped = checks.sane_items(offers)
    offers = [o for o in offers if is_current(o.to_json(), today)]
    checks.check_store(offers, previous_count)
    categorize.apply(offers)
    return offers, dropped


def run(stores: list[str], data_dir: Path = DATA, now: datetime | None = None) -> int:
    now = now or datetime.now(TZ)
    today = now.date()
    old_offers = _read_json(data_dir / "offers.json", [])
    old_meta = _read_json(data_dir / "meta.json", {"stores": {}})
    by_store: dict[str, list[dict]] = {s: [] for s in STORES}
    for o in old_offers:
        by_store.setdefault(o["store"], []).append(o)

    meta_stores = dict(old_meta.get("stores", {}))
    failed = []
    for store in stores:
        prev = meta_stores.get(store, {})
        try:
            offers, dropped = scrape_store(store, today, prev.get("count", 0))
        except Exception as exc:  # one store never takes the others down
            traceback.print_exc()
            failed.append(store)
            meta_stores[store] = {**prev, "ok": False, "error": f"{type(exc).__name__}: {exc}"[:300],
                                  "attempted_at": now.isoformat(timespec="seconds")}
            print(f"[{store}] FAILED, keeping previous offers ({len(by_store.get(store, []))})", file=sys.stderr)
            continue
        by_store[store] = [o.to_json() for o in offers]
        unmatched = sum(1 for o in offers if o.category == categorize.FALLBACK)
        meta_stores[store] = {
            "ok": True,
            "count": len(offers),
            "updated_at": now.isoformat(timespec="seconds"),
            "dropped_insane": dropped,
            "uncategorized": unmatched,
            "source": SOURCES[store],
        }
        print(f"[{store}] {len(offers)} offers, {unmatched} in 'drugo', {dropped} dropped as insane")

    all_offers = [o for s in by_store.values() for o in s if is_current(o, today)]
    all_offers.sort(key=lambda o: (o["store"], o["id"]))
    for store, entry in meta_stores.items():
        entry["count_published"] = sum(1 for o in all_offers if o["store"] == store)
        entry.setdefault("source", SOURCES.get(store))

    _write_json(data_dir / "offers.json", all_offers)
    _write_json(data_dir / "meta.json", {
        "generated_at": now.isoformat(timespec="seconds"),
        "count": len(all_offers),
        "stores": meta_stores,
        "categories": categorize.categories(),
    })
    history = [
        {k: o[k] for k in ("id", "price", "regular_price", "valid_from", "valid_to") if k in o}
        for o in all_offers
    ]
    _write_json(data_dir / "history" / f"{today.isoformat()}.json", history)

    print(f"Wrote {len(all_offers)} offers. Per category: {dict(Counter(o['category'] for o in all_offers))}")
    if failed:
        print(f"Failed stores: {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    enabled = [s for s in STORES if getattr(MODULES[s], "ENABLED", True)]
    parser.add_argument("--stores", nargs="*", default=enabled, choices=STORES)
    parser.add_argument("--data", type=Path, default=DATA)
    args = parser.parse_args()
    sys.exit(run(args.stores, args.data))


if __name__ == "__main__":
    main()
