#!/usr/bin/env python3
"""Turn the ESV_ENABLED build flag on or off.

ESV is on for the website and for store builds (Crossway standard-use rule).
Use --off only if ESV ever has to be pulled from a build.

  python3 tools/set_esv.py --off   # hide ESV, do not ship ESV text
  python3 tools/set_esv.py --on    # include ESV (default)

Pass --root DIR to operate on a copy. Do not point --off at the git checkout
if you intend to commit.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
ESV_SW_ENTRY = '"data/verses-esv.json"'


def paths(root: Path) -> dict[str, Path]:
    return {
        "root": root,
        "config": root / "js" / "config.js",
        "sw": root / "sw.js",
        "esv_data": root / "data" / "verses-esv.json",
        "esv_src": root / "tools" / "esv-quotes.json",
    }


def set_flag(config: Path, on: bool) -> None:
    text = config.read_text()
    new, n = re.subn(
        r"ESV_ENABLED:\s*(true|false)",
        f"ESV_ENABLED: {'true' if on else 'false'}",
        text,
    )
    if n != 1:
        raise SystemExit(f"Could not find a single ESV_ENABLED flag in {config}")
    config.write_text(new)


def sw_has_esv(text: str) -> bool:
    return ESV_SW_ENTRY in text


def set_sw(sw: Path, on: bool) -> None:
    if not sw.is_file():
        if on:
            raise SystemExit(f"Missing {sw}")
        return
    text = sw.read_text()
    has = sw_has_esv(text)
    if on and not has:
        if '"data/verses.json"' in text:
            text = text.replace('"data/verses.json"', '"data/verses.json", "data/verses-esv.json"', 1)
        else:
            raise SystemExit("sw.js CORE is missing data/verses.json")
        sw.write_text(text)
    elif (not on) and has:
        text = text.replace(', "data/verses-esv.json"', "").replace('"data/verses-esv.json", ', "")
        sw.write_text(text)


def apply(root: Path, on: bool) -> None:
    p = paths(root)
    set_flag(p["config"], on)
    set_sw(p["sw"], on)
    if on:
        if not p["esv_src"].is_file():
            raise SystemExit(f"Missing {p['esv_src']}")
        p["esv_data"].parent.mkdir(parents=True, exist_ok=True)
        p["esv_data"].write_text(p["esv_src"].read_text())
        print("ESV_ENABLED is true. data/verses-esv.json is in the bundle and in sw.js CORE.")
    else:
        if p["esv_data"].exists():
            p["esv_data"].unlink()
        print("ESV_ENABLED is false. data/verses-esv.json was removed and dropped from sw.js CORE.")
        print("The picker now shows the other 14 translations (BSB default, NIV included).")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--on", action="store_true", help="Enable ESV (default for web and store builds)")
    g.add_argument("--off", action="store_true", help="Disable ESV")
    p.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Project root to modify (default: the repo that contains this script)",
    )
    args = p.parse_args()
    root = (args.root or DEFAULT_ROOT).resolve()
    apply(root, on=args.on)
    return 0


if __name__ == "__main__":
    sys.exit(main())
