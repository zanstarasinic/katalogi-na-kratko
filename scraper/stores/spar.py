"""Spar: SPAR Online (Next.js) embeds product data in the page as React flight rows.

Category pages are paged with ?currentPage=N (50 products each). Only SPAR Online is
read, so some in-store-only leaflet deals are missing; the site says so.
"""
from __future__ import annotations

import json
import re

from .. import http
from ..model import Offer, local_date, to_cents

SOURCE = "https://online.spar.si"
# Promo categories under "Aktualno". Add more paths here if they turn out to miss promotions.
CATEGORIES = [
    "/ca/aktualno/iz-letaka/S17/S17-1",
    "/ca/aktualno/akcije-dom-in-prosti-cas/S17/S17-2",
]
MAX_PAGES = 40

_PUSH = re.compile(r'self\.__next_f\.push\(\[1,"((?:[^"\\]|\\.)*)"\]\)')
_ROW = re.compile(r"([0-9a-f]+):")
_REF = re.compile(r"\$[0-9a-f]+")


def decode_flight(page: str) -> dict[str, object]:
    """Turn the concatenated flight payload into {row id: parsed JSON}."""
    data = "".join(json.loads(f'"{m}"') for m in _PUSH.findall(page))
    rows: dict[str, object] = {}
    i = 0
    while i < len(data):
        m = _ROW.match(data, i)
        if not m:
            j = data.find("\n", i)
            i = len(data) if j < 0 else j + 1
            continue
        key, i = m.group(1), m.end()
        if data.startswith("T", i):  # text row: T<hex byte length>,<text>
            comma = data.index(",", i)
            length = int(data[i + 1:comma], 16)
            text = data[comma + 1:].encode()[:length].decode("utf-8", "ignore")
            rows[key] = text
            i = comma + 1 + len(text)
            continue
        j = data.find("\n", i)
        j = len(data) if j < 0 else j
        try:
            rows[key] = json.loads(data[i:j])
        except ValueError:
            rows[key] = data[i:j]
        i = j + 1
    return rows


def _resolve(value, rows, depth=0):
    if depth > 8:
        return value
    if isinstance(value, str) and _REF.fullmatch(value):
        return _resolve(rows.get(value[1:]), rows, depth + 1)
    if isinstance(value, dict):
        return {k: _resolve(v, rows, depth + 1) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve(v, rows, depth + 1) for v in value]
    return value


def products(page: str) -> list[dict]:
    rows = decode_flight(page)
    return [
        _resolve(r, rows) for r in rows.values()
        if isinstance(r, dict) and "sku" in r and "price" in r and "slug" in r
    ]


def _store_category(p: dict) -> str | None:
    """Deepest category outside the 'AKTUALNO' promo tree, e.g. '/SHRAMBA/JUHE IN JUŠNI DODATKI/JUHE'."""
    cats = [c for c in p.get("categoriesData") or [] if isinstance(c, dict)]
    real = [c for c in cats if not str(c.get("path", "")).startswith("/S17")]
    best = max(real or cats, key=lambda c: c.get("level") or 0, default=None)
    return best.get("categoryNamesPath") if best else None


def _unit_price(p: dict, promo_unit) -> str | None:
    value = promo_unit or p.get("pricePerSubUnit")
    unit = (p.get("subUnit") or "").lower()
    if not value or not unit:
        return None
    return f"{value:.2f}".replace(".", ",") + f" €/{unit}"


_PACKAGE = re.compile(r"(\d+(?:[.,]\d+)?\s?(?:X\s?\d+(?:[.,]\d+)?\s?)?(?:KG|G|ML|L|KOS))\b", re.IGNORECASE)


def _package(name: str) -> str | None:
    """Pack size from the product name: 'MAJONEZA THOMY, 265G' -> '265 g'."""
    found = _PACKAGE.findall(name or "")
    if not found:
        return None
    text = re.sub(r"\s*x\s*", " x ", found[-1].lower())
    return re.sub(r"(\d)\s?(kg|g|ml|l|kos)\b", r"\1 \2", text)


def normalize_product(p: dict) -> Offer | None:
    promo = p.get("promotion")
    if not isinstance(promo, dict) or not promo.get("isActive"):
        return None
    conds = [c for c in promo.get("conditions") or [] if isinstance(c, dict) and c.get("price")]
    if not conds:
        return None
    cond = conds[0]
    eans = p.get("ean") if isinstance(p.get("ean"), list) else []
    photos = p.get("photosUrl") if isinstance(p.get("photosUrl"), list) else []
    return Offer(
        id=f"spar:{p['sku']}",
        store="spar",
        name=p.get("name"),
        brand=p.get("brand") or None,
        price_cents=to_cents(cond["price"]),
        regular_price_cents=to_cents(p.get("price")),
        min_quantity=max(1, int(cond.get("quantity") or 1)),
        package=_package(p.get("name")),
        unit_price=_unit_price(p, p.get("promotionPricePerSubUnit")),
        valid_from=local_date(promo.get("startDateTime")),
        valid_to=local_date(promo.get("endDateTime")),
        store_category=_store_category(p),
        image_url=photos[0] if photos else None,
        product_url=f"{SOURCE}/p/{p['slug']}",
        ean=eans[0] if eans else None,
    )


def fetch() -> list[str]:
    pages = []
    for path in CATEGORIES:
        seen: set[str] = set()
        for n in range(1, MAX_PAGES + 1):
            page = http.get(f"{SOURCE}{path}?currentPage={n}", accept="text/html")
            skus = {str(p["sku"]) for p in products(page)}
            if not skus or skus <= seen:
                break
            seen |= skus
            pages.append(page)
    return pages


def normalize(pages: list[str], today=None) -> list[Offer]:
    out: dict[str, Offer] = {}
    for page in pages:
        for p in products(page):
            offer = normalize_product(p)
            if offer:
                out.setdefault(offer.id, offer)
    return list(out.values())
