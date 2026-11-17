#!/usr/bin/env python3
"""Fetch NIV (2011) text for the 310 Study Guides references from BibleGateway.

Polite, resumable, rate-limited.
"""
from __future__ import annotations

import json
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / "niv-quotes.json"
LOG = ROOT / "tools" / "niv-fetch.log"
UA = (
    "CreedOfInkStudyGuides/1.0 "
    "(nonprofit Bible study app; contact hullanderink@gmail.com; "
    "+https://hullander28.github.io/bible-study-guides/)"
)
DELAY = 1.6


def log(msg: str) -> None:
    line = msg.rstrip() + "\n"
    with LOG.open("a") as f:
        f.write(line)
    print(msg, flush=True)


def extract(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    spans = soup.select(".passage-text span.text, .passage-content span.text")
    parts: list[str] = []
    for sp in spans:
        parent = sp.parent
        parent_name = parent.name if parent is not None else ""
        # Section titles are span.text inside h3 (or h1/h2).
        # Keep h4 psalm superscriptions and all verse / poetry lines.
        if parent_name in ("h1", "h2", "h3"):
            continue
        for sc in list(sp.select("span.small-caps")):
            sc.replace_with(sc.get_text().upper())
        for bad in sp.select(
            ".footnote, .footnoteref, .crossreference, "
            "sup.versenum, span.chapternum, sup.crossreference"
        ):
            bad.decompose()
        t = " ".join(sp.get_text(" ", strip=True).split())
        t = re.sub(r" +([,.;:!?])", r"\1", t)
        t = re.sub(r" +([”’\"\'])", r"\1", t)
        if t:
            parts.append(t)
    seen: set[str] = set()
    uniq: list[str] = []
    for part in parts:
        if part not in seen:
            seen.add(part)
            uniq.append(part)
    return " ".join(uniq).strip()


def fetch(ref: str) -> str:
    q = urllib.parse.quote(ref.replace("\u2013", "-"))
    url = f"https://www.biblegateway.com/passage/?search={q}&version=NIV"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    last_err = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status != 200:
                    raise urllib.error.HTTPError(url, r.status, "bad status", r.headers, None)
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last_err = e
            wait = DELAY * (2 ** attempt) + random.random()
            log(f"retry {attempt+1} for {ref}: {e}; sleeping {wait:.1f}s")
            time.sleep(wait)
    raise RuntimeError(f"failed to fetch {ref}: {last_err}")


def main() -> int:
    verses = json.loads((ROOT / "data" / "verses.json").read_text())
    refs = list(verses.keys())
    data: dict[str, str] = {}
    if OUT.exists():
        data = json.loads(OUT.read_text())
    missing = [r for r in refs if not (isinstance(data.get(r), str) and data[r].strip())]
    log(f"total={len(refs)} already={len(refs)-len(missing)} to_fetch={len(missing)}")
    for i, ref in enumerate(missing, 1):
        html = fetch(ref)
        text = extract(html)
        if not text:
            log(f"EMPTY {ref}")
            raise SystemExit(f"empty text for {ref}")
        data[ref] = text
        if i % 10 == 0 or i == len(missing):
            OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
            log(f"saved {i}/{len(missing)} last={ref} chars={len(text)}")
        time.sleep(DELAY + random.random() * 0.4)
    ordered = {r: data[r] for r in refs}
    if set(ordered) != set(refs) or any(not v.strip() for v in ordered.values()):
        raise SystemExit("incomplete NIV set")
    OUT.write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n")
    log(f"done {len(ordered)} verses -> {OUT}")
    g11 = ordered["Genesis 1:1"]
    j316 = ordered["John 3:16"]
    c118 = ordered["1 Corinthians 1:18"]
    log(f"CHECK Genesis 1:1={g11}")
    log(f"CHECK John 3:16={j316}")
    log(f"CHECK 1 Cor 1:18={c118}")
    if g11 != "In the beginning God created the heavens and the earth.":
        raise SystemExit(f"Genesis 1:1 unexpected: {g11!r}")
    if "For God so loved the world" not in j316:
        raise SystemExit("John 3:16 unexpected")
    if "The Beginning" in g11 or "Christ Crucified" in c118:
        raise SystemExit("heading leaked")
    if "foolishness to those who are perishing" not in c118:
        raise SystemExit("1 Cor 1:18 incomplete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
