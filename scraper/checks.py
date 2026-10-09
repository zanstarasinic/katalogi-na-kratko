"""Per-store checks. Store-level failures keep yesterday's offers; bad items are dropped."""
from __future__ import annotations

from .model import Offer


class CheckFailed(Exception):
    pass


def sane_items(offers: list[Offer]) -> tuple[list[Offer], int]:
    """Drop items with a zero/negative price or a regular price below the sale price."""
    kept = [
        o for o in offers
        if o.price_cents > 0 and (o.regular_price_cents is None or o.regular_price_cents >= o.price_cents)
    ]
    return kept, len(offers) - len(kept)


def check_store(offers: list[Offer], previous_count: int) -> None:
    """Raise CheckFailed when the store result must not replace yesterday's data."""
    if not offers:
        raise CheckFailed("ni izdelkov (0 items returned)")
    if previous_count and len(offers) < previous_count / 2:
        raise CheckFailed(f"count collapsed: {len(offers)} vs {previous_count} yesterday")
