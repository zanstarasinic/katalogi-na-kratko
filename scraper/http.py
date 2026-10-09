"""Tiny polite HTTP client: one request per second at most, identifies itself."""
from __future__ import annotations

import time
import urllib.request

USER_AGENT = "Mozilla/5.0 (compatible; akcije-na-enem-mestu/1.0; +https://github.com/)"
TIMEOUT = 30
_last = 0.0


def get(url: str, accept: str = "*/*") -> str:
    global _last
    wait = 1.0 - (time.monotonic() - _last)
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": accept,
        "Accept-Language": "sl-SI,sl;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode("utf-8", "replace")
    finally:
        _last = time.monotonic()
