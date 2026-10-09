"""The daily run: a failing store keeps yesterday's offers and never affects the others."""
import json
from datetime import datetime

from scraper import run as runmod
from scraper.model import TZ, Offer

NOW = datetime(2026, 10, 9, 6, 0, tzinfo=TZ)


def fake_module(offers=None, error=None):
    class M:
        @staticmethod
        def fetch():
            if error:
                raise error
            return offers

        @staticmethod
        def normalize(raw, today=None):
            return raw
    return M


def mk(store, n, **kw):
    return [Offer(id=f"{store}:{i}", store=store, name=f"Mleko {i}", price_cents=100 + i,
                  valid_from="2026-10-08", valid_to="2026-10-14", **kw) for i in range(n)]


def test_failed_store_keeps_old_offers(tmp_path, monkeypatch):
    old = [o.to_json() for o in mk("spar", 3)]
    (tmp_path / "offers.json").write_text(json.dumps(old))
    (tmp_path / "meta.json").write_text(json.dumps({"stores": {"spar": {"ok": True, "count": 3}}}))
    monkeypatch.setattr(runmod, "MODULES", {
        "lidl": fake_module(mk("lidl", 4)),
        "spar": fake_module(error=TimeoutError("timed out")),
    })
    code = runmod.run(["lidl", "spar"], tmp_path, NOW)
    assert code == 1
    offers = json.loads((tmp_path / "offers.json").read_text())
    assert sum(o["store"] == "spar" for o in offers) == 3
    assert sum(o["store"] == "lidl" for o in offers) == 4
    meta = json.loads((tmp_path / "meta.json").read_text())
    assert meta["stores"]["spar"]["ok"] is False and "timed out" in meta["stores"]["spar"]["error"]
    assert meta["stores"]["lidl"]["ok"] is True
    assert (tmp_path / "history" / "2026-10-09.json").exists()


def test_collapse_keeps_old_offers(tmp_path, monkeypatch):
    (tmp_path / "offers.json").write_text(json.dumps([o.to_json() for o in mk("lidl", 10)]))
    (tmp_path / "meta.json").write_text(json.dumps({"stores": {"lidl": {"ok": True, "count": 10}}}))
    monkeypatch.setattr(runmod, "MODULES", {"lidl": fake_module(mk("lidl", 2))})
    assert runmod.run(["lidl"], tmp_path, NOW) == 1
    assert len(json.loads((tmp_path / "offers.json").read_text())) == 10


def test_expired_and_far_future_offers_are_dropped(tmp_path, monkeypatch):
    offers = mk("lidl", 3)
    offers[0].valid_to = "2026-10-08"     # expired yesterday
    offers[1].valid_from = "2026-10-20"   # starts in 11 days
    monkeypatch.setattr(runmod, "MODULES", {"lidl": fake_module(offers)})
    assert runmod.run(["lidl"], tmp_path, NOW) == 0
    ids = [o["id"] for o in json.loads((tmp_path / "offers.json").read_text())]
    assert ids == ["lidl:2"]
    hist = json.loads((tmp_path / "history" / "2026-10-09.json").read_text())
    assert set(hist[0]) <= {"id", "price", "regular_price", "valid_from", "valid_to"}
    meta = json.loads((tmp_path / "meta.json").read_text())
    assert len(meta["categories"]) == 16
