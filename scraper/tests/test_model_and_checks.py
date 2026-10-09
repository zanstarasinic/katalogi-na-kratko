from scraper import categorize
from scraper.checks import CheckFailed, check_store, sane_items
from scraper.model import Offer, discount_pct, local_date, to_cents

import pytest


def offer(**kw):
    base = dict(id="x:1", store="lidl", name="Test", price_cents=100)
    base.update(kw)
    return Offer(**base)


@pytest.mark.parametrize("value,cents", [
    (4.89, 489), (0.1 + 0.2, 30), ("5,99 €", 599), ("5,99\xa0", 599), ("1.234", 123), (None, None), ("", None),
])
def test_to_cents(value, cents):
    assert to_cents(value) == cents


def test_discount_is_computed_and_floored():
    assert discount_pct(489, 699) == 30
    assert discount_pct(79, 109) == 27
    assert discount_pct(100, 100) is None
    assert discount_pct(100, None) is None


def test_discount_below_one_percent_is_no_discount():
    o = offer(price_cents=995, regular_price_cents=1000)  # 0.5 %
    j = o.to_json()
    assert o.discount_pct is None
    assert j["kind"] == "special"
    assert "regular_price" not in j and "discount_pct" not in j


def test_single_price_is_special_offer():
    j = offer().to_json()
    assert j["kind"] == "special"
    assert j["price"] == 1.0


def test_discount_json_shape():
    j = offer(price_cents=489, regular_price_cents=699, requires_card=True).to_json()
    assert j == {**j, "kind": "discount", "price": 4.89, "regular_price": 6.99, "discount_pct": 30, "requires_card": True}


def test_local_date_uses_ljubljana_time():
    # 21:59:59Z on 18 Oct is 23:59:59 in Ljubljana (CEST) -> still the 18th
    assert local_date("2026-10-18T21:59:59Z") == "2026-10-18"
    # 22:00Z on 6 Oct is midnight 7 Oct in Ljubljana
    assert local_date("2026-10-06T22:00:00.000+00:00") == "2026-10-07"
    assert local_date(1791756000) == "2026-10-12"


def test_sane_items_drops_bad_prices():
    good = offer()
    zero = offer(id="x:2", price_cents=0)
    inverted = offer(id="x:3", price_cents=500, regular_price_cents=400)
    kept, dropped = sane_items([good, zero, inverted])
    assert kept == [good] and dropped == 2


def test_check_store_empty_and_collapse():
    with pytest.raises(CheckFailed):
        check_store([], 10)
    with pytest.raises(CheckFailed):
        check_store([offer()] * 4, 10)
    check_store([offer()] * 5, 10)  # exactly half is fine
    check_store([offer()], 0)  # first run


def test_categorize_store_mapping_then_keywords_then_drugo():
    assert categorize.categorize(offer(store_category="Svetovi potreb/Hrana in bližnja hrana/Vino/Rdeče vino")) == "alkohol"
    assert categorize.categorize(offer(store="eurospin", name="EDAMEC")) == "mlecni-jajca"
    assert categorize.categorize(offer(name="Nekaj čisto neznanega")) == "drugo"
    # keyword stems match at word start only: 'sirup' must not be cheese
    assert categorize.categorize(offer(name="Sirup bazilika")) == "drugo"


def test_every_mapping_target_is_a_known_category():
    known = {c["id"] for c in categorize.categories()}
    assert len(known) == 16
    for store in ("lidl", "spar", "eurospin"):
        for _, cat in categorize._store_rules(store):
            assert cat in known, (store, cat)
    for _, cat in categorize._keyword_rules():
        assert cat in known


def test_soft_drinks_are_not_alcohol():
    # "BREZALKOHOLNE PIJAČE" contains "alkoholne pijače"; rules must match whole words.
    for path in ("/PIJAČE/BREZALKOHOLNE PIJAČE/VODE", "/PIJAČE/BREZALKOHOLNE PIJAČE/SADNI SOKOVI",
                 "/PIJAČE/BREZALKOHOLNE PIJAČE/GAZIRANE PIJAČE"):
        assert categorize.categorize(offer(store="spar", name="Herbalna voda meta", store_category=path)) == "pijace"
    assert categorize.categorize(offer(store="spar", name="Pivo pittinger", store_category="/PIJAČE/PIVO & CIDER/SVETLO PIVO")) == "alkohol"
    assert categorize.categorize(offer(store="spar", name="Rdeče vino", store_category="/PIJAČE/VINO/DOMAČA RDEČA VINA")) == "alkohol"


def test_non_alcoholic_products_leave_alcohol_shelves():
    # Stores shelve these under alcohol; the product itself is not alcoholic.
    assert categorize.categorize(offer(store="eurospin", name="BREZALKOHOLNI RADLER, LIMONA", store_category="alkoholne pijače")) == "pijace"
    assert categorize.categorize(offer(store="spar", name="SVETLO BREZALKOHOLNO PIVO UNION, 0,5L", store_category="/PIJAČE/PIVO & CIDER/BREZALKOHOLNO PIVO")) == "pijace"
    assert categorize.categorize(offer(store="spar", name="BREZALKOHOLNI APERITIV ARANCIA, RAMAZZOTTI",
                                       store_category="/PIJAČE/ŽGANE IN DRUGE ALKOHOLNE PIJAČE/OSTALE ALKOHOLNE PIJAČE, COCKTAILI")) == "pijace"


@pytest.mark.parametrize("store,path,name,expected", [
    ("spar", "/VSE ZA MALE ŽIVALI/HRANA IN PRIBOLJŠKI/PASJA HRANA IN PRIBOLJŠKI", "Pasja hrana z govedino", "ljubljencki"),
    ("spar", "/VSE ZA MALE ŽIVALI/HRANA IN PRIBOLJŠKI/MAČJA HRANA IN PRIBOLJŠKI", "Mačja hrana piščanec", "ljubljencki"),
    ("spar", "/GOSPODINJSKI APARATI/MESOREZNICE, SALAMOREZNICE", "Mesoreznica", "dom-vrt-orodje"),
    ("spar", "/ZAMRZNJENI IZDELKI/SADJE IN ZELENJAVA/ZELENJAVA", "Grah", "zamrznjeno"),
    ("spar", "/VRT IN PROSTI ČAS/KNJIGE/OTROŠKE, MLADINSKE KNJIGE", "Knjiga za otroke", "otroci"),
    ("spar", "/OSEBNA NEGA/HIGIENSKI DODATKI IN TOALETNI PAPIR/TOALETNI PAPIR IN VATA", "Toaletni papir", "cistila-gospodinjstvo"),
    ("spar", "/SVEŽE MESO, MESNI IZDELKI IN RIBE/RIBE/RIBE", "Losos", "meso-ribe"),
    ("lidl", "Svetovi potreb/Hrana in bližnja hrana/Zamrznjena hrana (Zamrznjena hrana)/Zamrznjeno sadje in zelenjava", "Grah", "zamrznjeno"),
    ("lidl", "Svetovi potreb/Hrana in bližnja hrana/Zaloga hrane/Konzervirano sadje in zelenjava", "Koruza", "shramba"),
    ("eurospin", None, "GOBA ZA IKEBANO", "dom-vrt-orodje"),
    ("eurospin", None, "GOBE ŠAMPINJONI", "sadje-zelenjava"),
])
def test_store_paths_map_to_the_right_crate(store, path, name, expected):
    assert categorize.categorize(offer(store=store, name=name, store_category=path)) == expected
