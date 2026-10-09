"""Eurospin: the Akcija page is plain HTML. Categories come from one filtered page each."""
from __future__ import annotations

import html as htmllib
import re
import urllib.parse
from datetime import date

from .. import http
from ..model import Offer, to_cents

PAGE = "https://www.eurospin.si/akcije/"

_ITEM = re.compile(r'class="sn_promo_grid_item_ct">(.*?)</a>', re.S)
_CATEGORY = re.compile(r'akcije/\?category_filter=([^"]+)"')


def _text(block: str, cls: str) -> str | None:
    m = re.search(rf'class="{cls}[^"]*"[^>]*>(.*?)</', block, re.S)
    if not m:
        return None
    t = htmllib.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))
    t = re.sub(r"\s+", " ", t.replace("\xa0", " ")).strip()
    return t or None


def _dates(text: str | None, today: date) -> tuple[str | None, str | None]:
    """'8.10 - 14.10' -> ISO dates. The year is inferred from today (handles New Year)."""
    if not text:
        return None, None
    found = re.findall(r"(\d{1,2})\.(\d{1,2})\.?(\d{4})?", text)

    def to_iso(d, m, y):
        year = int(y) if y else today.year
        if not y and int(m) < today.month - 6:
            year += 1
        elif not y and int(m) > today.month + 6:
            year -= 1
        return date(year, int(m), int(d)).isoformat()

    isos = [to_iso(*f) for f in found]
    if not isos:
        return None, None
    return isos[0], isos[-1] if len(isos) > 1 else None


def _price_info(text: str | None) -> tuple[str | None, str | None]:
    """'460 g - za kg 9,77 €' -> ('460 g', '9,77 €/kg')."""
    if not text:
        return None, None
    parts = [p.strip() for p in text.split(" - ")]
    package, unit = parts[0] or None, None
    for p in parts[1:]:
        m = re.match(r"za\s+(\S+)\s+([\d.,]+)\s*€?", p)
        if m:
            unit = f"{m.group(2)} €/{m.group(1)}"
    return package, unit


def parse_items(page: str, today: date) -> list[Offer]:
    out = []
    for block in _ITEM.findall(page):
        name = _text(block, "i_title")
        sale = re.search(r'itemprop="price">([^<]+)<', block)
        if not name or not sale:
            continue
        price_block = re.search(r'class="i_price">(.*?)<meta', block, re.S)
        regular = to_cents(htmllib.unescape(price_block.group(1))) if price_block else None
        img = re.search(r'class="i_image"[^>]*src="([^"]+)"|src="([^"]+)"[^>]*class="i_image"', block)
        image = (img.group(1) or img.group(2)) if img else None
        valid_from, valid_to = _dates(_text(block, "date_current_promo"), today)
        package, unit = _price_info(_text(block, "i_price_info"))
        code = re.search(r"/([\w-]+)\.\w+$", image or "")
        key = code.group(1) if code else re.sub(r"\W+", "-", name.lower()).strip("-")
        desc = _text(block, "i_descrizione")
        out.append(Offer(
            id=f"eurospin:{key}:{valid_from or ''}",
            store="eurospin",
            name=name,
            brand=_text(block, "i_brand"),
            price_cents=to_cents(sale.group(1)),
            regular_price_cents=regular,
            package=package,
            unit_price=unit,
            valid_from=valid_from,
            valid_to=valid_to,
            image_url=image,
            product_url=PAGE,
            description=desc,
        ))
    return out


def fetch() -> dict:
    main = http.get(PAGE, accept="text/html")
    cats = {}
    for raw in dict.fromkeys(_CATEGORY.findall(main)):
        value = htmllib.unescape(urllib.parse.unquote(raw))
        cats[value] = http.get(PAGE + "?category_filter=" + urllib.parse.quote(value), accept="text/html")
    return {"main": main, "categories": cats}


def normalize(raw: dict, today: date) -> list[Offer]:
    offers = {o.id: o for o in parse_items(raw["main"], today)}
    for cat, page in raw.get("categories", {}).items():
        for o in parse_items(page, today):
            offers.setdefault(o.id, o).store_category = cat.lower()
    return list(offers.values())
