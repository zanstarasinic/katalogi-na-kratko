"""Rule-based categorization: store mapping first, then name keywords, then 'drugo'."""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

from .model import Offer

DIR = Path(__file__).parent / "categories"
FALLBACK = "drugo"


def categories() -> list[dict]:
    return json.loads((DIR / "categories.json").read_text("utf-8"))


# A product the store shelves with alcohol but that is itself non-alcoholic.
NON_ALCOHOLIC = re.compile(r"\bbrezalkohol|\b0[,.]0\s*%", re.IGNORECASE)


@lru_cache
def _store_rules(store: str) -> list[tuple[re.Pattern, str]]:
    """Store-path rules match at a word start, so "alkoholne pijače" never hits "brezalkoholne pijače"."""
    path = DIR / f"{store}.json"
    if not path.exists():
        return []
    rules = json.loads(path.read_text("utf-8"))["rules"]
    return [(re.compile((r"(?<!\w)" if p[:1].isalnum() else "") + re.escape(p.lower())), c) for p, c in rules]


@lru_cache
def _keyword_rules() -> list[tuple[re.Pattern, str]]:
    rules = json.loads((DIR / "keywords.json").read_text("utf-8"))["rules"]
    return [(re.compile(rf"\b(?:{p})", re.IGNORECASE), c) for p, c in rules]


def categorize(offer: Offer) -> str:
    cat = _categorize(offer)
    if cat == "alkohol" and NON_ALCOHOLIC.search(offer.name):
        return "pijace"
    return cat


def _categorize(offer: Offer) -> str:
    if offer.store_category:
        path = offer.store_category.lower()
        for regex, cat in _store_rules(offer.store):
            if regex.search(path):
                return cat
    for regex, cat in _keyword_rules():
        if regex.search(offer.name):
            return cat
    return FALLBACK


def apply(offers: list[Offer]) -> list[Offer]:
    known = {c["id"] for c in categories()}
    for o in offers:
        o.category = categorize(o)
        assert o.category in known, f"unknown category {o.category}"
    return offers
