#!/usr/bin/env python3
"""Extract the verses this app quotes into static JSON for offline use.

Public-domain / CC BY-SA text is copied, unmodified, from Hidden Word's bundled
Bible files (the same data under bible-memory-v2/public/bible/). Only the
references used as key verses or memory verses are stored — not full Bibles.

Usage:
  python3 tools/build_verses.py --bible /path/to/bible-memory-v2/public/bible

Writes:
  data/verses.json       — quoted text in BSB, NIV, KJV, WEB, MSB, LSV, FBV, ASV,
                           RV, YLT, DBY, WBS, BBE, GNV (no ESV). NIV is merged
                           from tools/niv-quotes.json.
  data/verses-esv.json   — existing short ESV quotations (for web builds)
  tools/esv-quotes.json  — same ESV quotations, kept as the source for
                           tools/set_esv.py --on
  js/memory.js           — memory-verse list with refs only (no ESV text)

Prints a report of how many references were converted and any that could
not be matched in a translation.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
MEMORY_JS = ROOT / "js" / "memory.js"
TRS = ["BSB", "KJV", "WEB", "MSB", "LSV", "FBV", "ASV", "RV", "YLT", "DBY", "WBS", "BBE", "GNV"]
SINGLE_CHAPTER = {"Obadiah", "Philemon", "Jude", "2 John", "3 John"}
REF_RE = re.compile(
    r"^((?:[1-3] )?[A-Za-z]+(?: [A-Za-z]+)*)\s+(\d+)(?::(\d+)(?:[\u2013\-](\d+))?)?$"
)


def load_books(bible: Path) -> list[dict]:
    return json.loads((bible / "books.json").read_text())


def book_index(books: list[dict], name: str) -> int:
    if name == "Psalm":
        name = "Psalms"
    for i, b in enumerate(books, 1):
        if b["n"] == name:
            return i
    raise KeyError(f"Unknown book name: {name}")


def parse_ref(ref: str) -> tuple[str, int, int, int]:
    m = REF_RE.match(ref.strip())
    if not m:
        raise ValueError(f"Unparseable reference: {ref}")
    book, a, b, c = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    if b is None:
        if book not in SINGLE_CHAPTER:
            raise ValueError(f"Chapter:verse missing for {ref}")
        return book, 1, a, a
    v1 = int(b)
    v2 = int(c) if c else v1
    if v2 < v1:
        raise ValueError(f"Inverted range: {ref}")
    return book, a, v1, v2


def collect_quotes() -> OrderedDict[str, list[str]]:
    """ref -> list of ESV short quotations (usually one; Zephaniah 3:17 has two)."""
    out: OrderedDict[str, list[str]] = OrderedDict()
    for path in sorted(DATA.glob("*.json")):
        if path.name.startswith("verses"):
            continue
        guide = json.loads(path.read_text())
        for item in guide.get("keyVerses") or []:
            ref = item["ref"]
            quote = item.get("quote")
            if not quote:
                continue
            out.setdefault(ref, [])
            # Keep distinct excerpts for the same ref; skip exact dupes.
            if quote not in out[ref]:
                out[ref].append(quote)
    return out


def collect_memory() -> list[dict]:
    text = MEMORY_JS.read_text()
    # Support both the original {b, ref, t} shape and the slim {b, ref} shape.
    entries = re.findall(
        r'\{\s*"b":\s*"([^"]+)",\s*"ref":\s*"([^"]+)"(?:,\s*"t":\s*"((?:\\.|[^"\\])*)")?',
        text,
    )
    if not entries:
        raise SystemExit("Could not parse js/memory.js")
    return [{"b": b, "ref": r, "t": t or ""} for b, r, t in entries]


def load_tr_book(bible: Path, tr: str, bi: int) -> list:
    path = bible / tr.lower() / f"{bi:02d}.json"
    return json.loads(path.read_text())


def lookup(bible: Path, cache: dict, tr: str, bi: int, ch: int, v1: int, v2: int) -> tuple[str | None, str | None]:
    key = (tr, bi)
    if key not in cache:
        cache[key] = load_tr_book(bible, tr, bi)
    book = cache[key]
    if ch < 1 or ch > len(book):
        return None, f"missing chapter {ch}"
    chapter = book[ch - 1] or []
    parts = []
    for v in range(v1, v2 + 1):
        if v < 1 or v > len(chapter) or not chapter[v - 1]:
            return None, f"missing verse {ch}:{v}"
        parts.append(chapter[v - 1])
    return " ".join(parts), None


def write_memory(entries: list[dict]) -> None:
    lines = [
        "// Curated memory verses (two per book). Verse text is looked up from",
        "// data/verses.json (and data/verses-esv.json when ESV is enabled) so the",
        "// chosen translation can be shown offline.",
        "window.MEMORY = [",
    ]
    for i, e in enumerate(entries):
        comma = "," if i < len(entries) - 1 else ""
        lines.append(f'{{"b": "{e["b"]}", "ref": "{e["ref"]}"}}{comma}')
    lines.append("];")
    lines.append("")
    MEMORY_JS.write_text("\n".join(lines))


def strip_quotes_from_guides() -> int:
    changed = 0
    for path in sorted(DATA.glob("*.json")):
        if path.name.startswith("verses"):
            continue
        orig = path.read_text()
        guide = json.loads(orig)
        kvs = guide.get("keyVerses") or []
        if not kvs:
            continue
        new_kvs = [{"ref": item["ref"]} for item in kvs]
        if new_kvs == kvs:
            continue
        guide["keyVerses"] = new_kvs
        path.write_text(json.dumps(guide, indent=1, ensure_ascii=False))
        changed += 1
    return changed


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--bible",
        type=Path,
        default=Path("/workspace/bible-memory-v2/public/bible"),
        help="Path to Hidden Word public/bible directory",
    )
    p.add_argument("--skip-strip", action="store_true", help="Do not rewrite guide JSON or memory.js")
    args = p.parse_args()
    bible = args.bible.resolve()
    if not (bible / "books.json").is_file():
        print(f"Bible data not found at {bible}", file=sys.stderr)
        return 1

    books = load_books(bible)
    esv_quotes = collect_quotes()
    memory = collect_memory()

    # Union of key-verse and memory refs, in a stable order (guides then memory-only).
    refs: list[str] = list(esv_quotes.keys())
    for e in memory:
        if e["ref"] not in esv_quotes and e["ref"] not in refs:
            refs.append(e["ref"])

    # If quotes were already stripped, fall back to refs-only from guides + existing esv file.
    if not esv_quotes:
        existing = ROOT / "tools" / "esv-quotes.json"
        if existing.is_file():
            esv_quotes = json.loads(existing.read_text(), object_pairs_hook=OrderedDict)
        for path in sorted(DATA.glob("*.json")):
            if path.name.startswith("verses"):
                continue
            guide = json.loads(path.read_text())
            for item in guide.get("keyVerses") or []:
                if item["ref"] not in refs:
                    refs.append(item["ref"])

    cache: dict = {}
    verses: dict[str, dict[str, str]] = {}
    unmatched: list[str] = []
    missing_tr: list[str] = []
    converted = 0

    for ref in refs:
        try:
            book, ch, v1, v2 = parse_ref(ref)
            bi = book_index(books, book)
        except (ValueError, KeyError) as e:
            unmatched.append(f"{ref}: {e}")
            continue
        row: dict[str, str] = {}
        ok = True
        for tr in TRS:
            text, err = lookup(bible, cache, tr, bi, ch, v1, v2)
            if err:
                missing_tr.append(f"{ref} [{tr}]: {err}")
                if tr == "BSB":
                    ok = False
                continue
            row[tr] = text
        if not ok:
            unmatched.append(f"{ref}: not found in BSB (book {book} {ch}:{v1}-{v2})")
            continue
        verses[ref] = row
        converted += 1

    niv_path = ROOT / "tools" / "niv-quotes.json"
    if niv_path.is_file():
        niv = json.loads(niv_path.read_text())
        niv_missing = []
        for ref, row in verses.items():
            text = (niv.get(ref) or "").strip()
            if not text:
                niv_missing.append(ref)
                continue
            # Keep BSB first, then NIV, then the other bundled translations.
            ordered = {"BSB": row["BSB"], "NIV": text}
            for k, v in row.items():
                if k not in ordered:
                    ordered[k] = v
            verses[ref] = ordered
        if niv_missing:
            print(f"WARNING: {len(niv_missing)} refs have no NIV text in {niv_path}")
        else:
            print(f"Merged NIV quotations for {len(verses)} refs from {niv_path}.")
    else:
        print(f"No {niv_path}; verses.json will not include NIV.")

    DATA.mkdir(exist_ok=True)
    (DATA / "verses.json").write_text(json.dumps(verses, ensure_ascii=False, separators=(",", ":")))

    # ESV file: string when one excerpt, list when a ref has multiple short quotes.
    esv_out: OrderedDict[str, str | list[str]] = OrderedDict()
    for ref, quotes in esv_quotes.items():
        esv_out[ref] = quotes[0] if len(quotes) == 1 else quotes
    esv_text = json.dumps(esv_out, indent=2, ensure_ascii=False) + "\n"
    (DATA / "verses-esv.json").write_text(esv_text)
    (ROOT / "tools" / "esv-quotes.json").write_text(esv_text)

    if not args.skip_strip:
        n = strip_quotes_from_guides()
        write_memory(memory)
        print(f"Stripped ESV quote fields from {n} guide JSON files and rewrote js/memory.js.")

    print(f"Unique references: {len(refs)}")
    print(f"Converted (found in BSB and written): {converted}")
    print(f"ESV short quotations stored: {sum(len(v) if isinstance(v, list) else 1 for v in esv_out.values())} across {len(esv_out)} refs")
    print(f"Memory verses: {len(memory)}")
    if unmatched:
        print("\nUNMATCHED REFERENCES:")
        for line in unmatched:
            print("  " + line)
    else:
        print("All references matched in BSB.")
    if missing_tr:
        print(f"\nMissing in a non-BSB translation ({len(missing_tr)}):")
        for line in missing_tr:
            print("  " + line)
    else:
        print("Every translation had every quoted verse.")
    return 1 if unmatched else 0


if __name__ == "__main__":
    sys.exit(main())
