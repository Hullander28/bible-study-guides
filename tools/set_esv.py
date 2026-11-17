#!/usr/bin/env python3
"""Turn the ESV_ENABLED build flag on (web) or off (App Store / Google Play).

  python3 tools/set_esv.py --off   # store builds: hide ESV, do not ship ESV text
  python3 tools/set_esv.py --on    # web / GitHub Pages: include ESV
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "js" / "config.js"
SW = ROOT / "sw.js"
ESV_DATA = ROOT / "data" / "verses-esv.json"
ESV_SRC = ROOT / "tools" / "esv-quotes.json"
ESV_SW_ENTRY = '"data/verses-esv.json"'


def set_flag(on: bool) -> None:
    text = CONFIG.read_text()
    new, n = re.subn(
        r"ESV_ENABLED:\s*(true|false)",
        f"ESV_ENABLED: {'true' if on else 'false'}",
        text,
    )
    if n != 1:
        raise SystemExit("Could not find a single ESV_ENABLED flag in js/config.js")
    CONFIG.write_text(new)


def sw_has_esv(text: str) -> bool:
    return ESV_SW_ENTRY in text


def set_sw(on: bool) -> None:
    text = SW.read_text()
    has = sw_has_esv(text)
    if on and not has:
        # Insert after data/verses.json if present, otherwise before the closing ]; of CORE
        if '"data/verses.json"' in text:
            text = text.replace('"data/verses.json"', '"data/verses.json", "data/verses-esv.json"', 1)
        else:
            raise SystemExit("sw.js CORE is missing data/verses.json")
        SW.write_text(text)
    elif (not on) and has:
        text = text.replace(', "data/verses-esv.json"', "").replace('"data/verses-esv.json", ', "")
        SW.write_text(text)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--on", action="store_true", help="Enable ESV for the web build")
    g.add_argument("--off", action="store_true", help="Disable ESV for store builds")
    args = p.parse_args()
    on = args.on
    set_flag(on)
    set_sw(on)
    if on:
        if not ESV_SRC.is_file():
            raise SystemExit(f"Missing {ESV_SRC}")
        ESV_DATA.write_text(ESV_SRC.read_text())
        print("ESV_ENABLED is true. data/verses-esv.json is in the bundle and in sw.js CORE.")
    else:
        if ESV_DATA.exists():
            ESV_DATA.unlink()
        print("ESV_ENABLED is false. data/verses-esv.json was removed and dropped from sw.js CORE.")
        print("The picker now shows Hidden Word's 13 translations only. Default is BSB.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
