"""Parsers run against saved responses (captured 9 Oct 2026), never the live stores."""
import json
from datetime import date
from pathlib import Path

from scraper.stores import eurospin, lidl, spar

SAMPLES = Path(__file__).parent / "samples"
TODAY = date(2026, 10, 9)


def by_id(offers):
    return {o.id: o for o in offers}


# --- Lidl -----------------------------------------------------------------

def lidl_offers():
    return lidl.normalize([json.loads((SAMPLES / "lidl_page0.json").read_text("utf-8"))], TODAY)


def test_lidl_parses_whole_page():
    offers = lidl_offers()
    assert len(offers) == 60
    assert all(o.price_cents > 0 and o.name for o in offers)


def test_lidl_card_price_wins():
    o = by_id(lidl_offers())["lidl:11000046"]
    assert o.requires_card is True
    assert (o.price_cents, o.regular_price_cents, o.discount_pct) == (489, 699, 30)
    assert o.brand == "SPORTYFEEL"
    assert o.package == "200 g" and o.unit_price == "1 kg = 24,45 €"
    assert o.ean == "4335619267763"
    assert (o.valid_from, o.valid_to) == ("2026-10-12", "2026-10-17")
    assert o.product_url.startswith("https://www.lidl.si/p/")


def test_lidl_card_and_normal_price_both_present():
    offers = [o for o in lidl_offers() if o.requires_card]
    assert offers, "sample has Lidl Plus prices"
    page = json.loads((SAMPLES / "lidl_page0.json").read_text("utf-8"))
    both = [i for i in page["items"] if {"currentPrice", "currentLidlPlusPrice"} <= set(i["gridbox"]["data"]["regionsPrices"]["1"])]
    o = lidl.normalize_item(both[0])
    assert o.requires_card is True


def test_lidl_single_price_is_special():
    o = by_id(lidl_offers())["lidl:11000328"]
    assert o.regular_price_cents is None and o.kind == "special"


# --- Eurospin -------------------------------------------------------------

def euro_offers():
    raw = {
        "main": (SAMPLES / "eurospin_akcije.html").read_text("utf-8"),
        "categories": {"mleČni izdelki": (SAMPLES / "eurospin_cat_mlecni.html").read_text("utf-8")},
    }
    return eurospin.normalize(raw, TODAY)


def test_eurospin_parses_items_with_both_prices():
    offers = euro_offers()
    assert len(offers) == 172
    o = by_id(offers)["eurospin:900281301:2026-10-08"]
    assert o.name == "KRANJSKA KLOBASA"
    assert (o.price_cents, o.regular_price_cents, o.discount_pct) == (449, 599, 25)
    assert (o.package, o.unit_price) == ("460 g", "9,77 €/kg")
    assert (o.valid_from, o.valid_to) == ("2026-10-08", "2026-10-14")
    assert o.image_url.endswith("/900281301.jpg")


def test_eurospin_single_price_and_brand():
    offers = by_id(euro_offers())
    assert offers["eurospin:900628601:2026-10-08"].kind == "special"
    assert offers["eurospin:900495601:2026-10-08"].brand == "LAND"


def test_eurospin_category_from_filtered_page():
    tagged = [o for o in euro_offers() if o.store_category == "mlečni izdelki"]
    assert len(tagged) == 11


def test_eurospin_year_rollover():
    assert eurospin._dates("29.12 - 4.1", date(2026, 12, 28)) == ("2026-12-29", "2027-01-04")


# --- Spar -----------------------------------------------------------------

def spar_offers():
    return spar.normalize([(SAMPLES / "spar_iz_letaka_p1.html").read_text("utf-8")], TODAY)


def test_spar_decodes_flight_products():
    page = (SAMPLES / "spar_iz_letaka_p1.html").read_text("utf-8")
    assert len(spar.products(page)) == 50


def test_spar_promotions():
    offers = by_id(spar_offers())
    assert len(offers) == 48  # 2 of the 50 have no active promotion
    o = offers["spar:502850"]
    assert (o.price_cents, o.regular_price_cents, o.discount_pct) == (259, 416, 37)
    assert (o.valid_from, o.valid_to) == ("2026-10-07", "2026-10-13")
    assert o.package == "265 g"
    assert o.store_category.startswith("/SHRAMBA")
    assert o.product_url == "https://online.spar.si/p/majoneza-thomy-265g-502850"
