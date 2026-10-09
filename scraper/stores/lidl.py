"""Lidl: the search endpoint behind lidl.si offer pages returns JSON, 60 items per page."""
from __future__ import annotations

import json

from .. import http
from ..model import Offer, local_date, to_cents

SOURCE = "https://www.lidl.si"
API = SOURCE + "/q/api/search?assortment=SI&locale=sl_SI&version=v2.0.0&fetchsize={size}&offset={offset}"
PAGE = 60
MAX_PAGES = 40


def fetch() -> list[dict]:
    pages, offset = [], 0
    for _ in range(MAX_PAGES):
        page = json.loads(http.get(API.format(size=PAGE, offset=offset)))
        pages.append(page)
        offset += len(page.get("items") or [])
        if not page.get("items") or offset >= page.get("numFound", 0):
            break
    return pages


def _pick_price(data: dict) -> tuple[dict | None, bool]:
    """Card price wins over the normal price (spec rule). Returns (price object, requires_card)."""
    region = (data.get("regionsPrices") or {}).get("1") or {}
    card = (region.get("currentLidlPlusPrice") or {}).get("price")
    if card and card.get("price"):
        return card, True
    normal = region.get("currentPrice") or data.get("price")
    if normal and normal.get("price"):
        return normal, False
    return None, False


def _later(*dates):
    vals = [d for d in dates if d]
    return max(vals) if vals else None


def _earlier(*dates):
    vals = [d for d in dates if d]
    return min(vals) if vals else None


def normalize_item(item: dict) -> Offer | None:
    if item.get("type") != "product":
        return None
    grid = item.get("gridbox") or {}
    data = grid.get("data") or {}
    price, requires_card = _pick_price(data)
    if not price:
        return None
    discount = price.get("discount") or {}
    regular = discount.get("deletedPrice") or price.get("oldPrice")
    keyfacts = data.get("keyfacts") or {}
    brand = (data.get("brand") or {}).get("name") or None
    base = (price.get("basePrice") or {}).get("text")
    pid = data.get("productId") or data.get("erpNumber") or item.get("code")
    url = data.get("canonicalUrl")
    return Offer(
        id=f"lidl:{pid}",
        store="lidl",
        name=keyfacts.get("title") or data.get("title") or data.get("fullTitle"),
        brand=brand,
        price_cents=to_cents(price["price"]),
        regular_price_cents=to_cents(regular),
        requires_card=requires_card,
        package=(price.get("packaging") or {}).get("text") or None,
        unit_price=f"{base} €" if base else None,
        # Price objects carry publish time as startDate; the in-store window is storeStartDate.
        valid_from=_later(local_date(data.get("storeStartDate")), local_date(price.get("startDate"))),
        valid_to=_earlier(local_date(data.get("storeEndDate")), local_date(price.get("endDate"))),
        store_category=keyfacts.get("wonCategoryPrimary") or data.get("category"),
        image_url=data.get("image"),
        product_url=SOURCE + url if url else None,
        ean=(grid.get("meta") or {}).get("ean"),
    )


def normalize(pages: list[dict], today=None) -> list[Offer]:
    seen, out = set(), []
    for page in pages:
        for item in page.get("items") or []:
            offer = normalize_item(item)
            if offer and offer.id not in seen:
                seen.add(offer.id)
                out.append(offer)
    return out
