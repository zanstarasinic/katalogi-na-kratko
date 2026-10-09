"""The shared offer record. Every store is normalized into this shape."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import Optional
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Ljubljana")
STORES = ("lidl", "spar", "eurospin", "hofer")


def to_cents(value) -> Optional[int]:
    """Parse a price (float, int or Slovene text like '5,99 €') into integer cents."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return round(float(value) * 100)
    text = str(value).replace("\xa0", " ").replace("€", "").strip()
    m = re.search(r"\d+(?:[.,]\d+)?", text.replace(" ", ""))
    if not m:
        return None
    return round(float(m.group(0).replace(",", ".")) * 100)


def discount_pct(price_cents: int, regular_cents: Optional[int]) -> Optional[int]:
    """Whole-number discount computed from both prices. Below 1% counts as no discount."""
    if not regular_cents or regular_cents <= price_cents:
        return None
    pct = (regular_cents - price_cents) * 100 // regular_cents
    return pct if pct >= 1 else None


def local_date(value) -> Optional[str]:
    """Unix seconds, ISO datetime or date -> 'YYYY-MM-DD' in Ljubljana time."""
    if value is None or value == "":
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value, TZ)
    else:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return dt.date().isoformat()
        dt = dt.astimezone(TZ)
    return dt.date().isoformat()


@dataclass
class Offer:
    id: str
    store: str
    name: str
    price_cents: int
    regular_price_cents: Optional[int] = None
    brand: Optional[str] = None
    requires_card: bool = False
    min_quantity: int = 1
    package: Optional[str] = None
    unit_price: Optional[str] = None
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    category: str = "Drugo"
    store_category: Optional[str] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None
    description: Optional[str] = None
    ean: Optional[str] = None
    _extra: dict = field(default_factory=dict, repr=False)

    @property
    def discount_pct(self) -> Optional[int]:
        return discount_pct(self.price_cents, self.regular_price_cents)

    @property
    def kind(self) -> str:
        return "discount" if self.discount_pct else "special"

    def to_json(self) -> dict:
        """Public record as specified: prices in EUR, discount computed by us."""
        d = asdict(self)
        d.pop("_extra")
        price = d.pop("price_cents")
        regular = d.pop("regular_price_cents")
        pct = self.discount_pct
        out = {
            "id": d.pop("id"),
            "store": d.pop("store"),
            "name": d.pop("name"),
            "brand": d.pop("brand"),
            "kind": self.kind,
            "price": price / 100,
            # A sub-1% "discount" is no discount: drop the crossed-out price too.
            "regular_price": regular / 100 if pct else None,
            "discount_pct": pct,
        }
        out.update(d)
        return {k: v for k, v in out.items() if v is not None}
