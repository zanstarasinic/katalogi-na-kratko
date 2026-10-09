"""Hofer: not active yet.

As of 9 Oct 2026, hofer.si answers plain HTTP clients with 403 (Akamai "Access Denied"),
and the before-and-after price source is still an open question (spec, build step 6).
fetch() raises, so the daily run marks Hofer as failed and keeps whatever data it had
(none yet) without affecting the other stores. Once a usable source is found, implement
fetch()/normalize() here and add a saved sample + test; nothing else needs to change.
"""
from __future__ import annotations

from ..model import Offer

ENABLED = False
SOURCE = "https://www.hofer.si/posebna-ponudba"


class NotAvailable(Exception):
    pass


def fetch():
    raise NotAvailable("Hofer source not configured (hofer.si blocks non-browser clients)")


def normalize(raw, today=None) -> list[Offer]:
    return []
