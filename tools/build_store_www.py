#!/usr/bin/env python3
"""Build mobile/www for App Store / Google Play.

Copies the site into a temporary directory, turns off the website-only PDF
download on that copy (pdf/ is never copied), then writes the result to
mobile/www. Verse text for all 15 translations, including NIV and ESV
quotations (data/verses.json, data/verses-esv.json), is bundled. The git
checkout (and GitHub Pages / main) is never modified. mobile/www is gitignored
and must not be committed.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOBILE = ROOT / "mobile"
WWW = MOBILE / "www"

# Paths to copy into the store bundle (relative to repo root).
COPY_FILES = [
    "index.html",
    "manifest.webmanifest",
    "privacy.html",
    ".nojekyll",
]
# Do not copy pdf/. The printable guides are website-only; store builds ship
# only the quoted verse text.
COPY_DIRS = [
    "css",
    "js",
    "data",
    "icons",
]

# Never ship these in the native www folder.
EXCLUDE_NAMES = {".git", "__pycache__"}


def copy_tree(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.name in EXCLUDE_NAMES:
            continue
        target = dest / item.name
        if item.is_dir():
            copy_tree(item, target)
        else:
            shutil.copy2(item, target)


def inject_native_script(index: Path) -> None:
    text = index.read_text()
    tag = '<script src="native.js"></script>\n'
    if "native.js" in text:
        return
    needle = '<script src="js/app.js"></script>'
    if needle not in text:
        raise SystemExit("index.html is missing js/app.js script tag")
    index.write_text(text.replace(needle, tag + needle, 1))


def disable_pdf(www: Path) -> None:
    cfg = www / "js" / "config.js"
    text = cfg.read_text()
    new, n = re.subn(r"PDF_ENABLED:\s*(true|false)", "PDF_ENABLED: false", text)
    if n != 1:
        raise SystemExit("Could not find a single PDF_ENABLED flag in js/config.js")
    cfg.write_text(new)


def assert_store_www(www: Path) -> None:
    cfg = (www / "js" / "config.js").read_text()
    if "ESV_ENABLED: true" not in cfg:
        raise SystemExit("Store www has ESV disabled; expected ESV quotations on")
    if "PDF_ENABLED: false" not in cfg:
        raise SystemExit("Store www still shows the Download PDF button")
    if (www / "pdf").exists():
        raise SystemExit("Store www contains pdf/ (website-only printable guides)")
    for rel in ("data/verses.json", "data/verses-esv.json"):
        if not (www / rel).is_file():
            raise SystemExit(f"Store www is missing {rel}")
    if (www / "tools").exists():
        raise SystemExit("Store www contains tools/")


def bundle_native(www: Path) -> None:
    src = MOBILE / "src" / "native.js"
    if not src.is_file():
        raise SystemExit(f"Missing {src}")
    outfile = www / "native.js"
    cmd = [
        "npx",
        "esbuild",
        str(src),
        "--bundle",
        "--format=iife",
        "--minify",
        "--outfile=" + str(outfile),
    ]
    subprocess.run(cmd, cwd=MOBILE, check=True)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="bsg-store-www-") as tmp:
        tmp_path = Path(tmp)
        for rel in COPY_FILES + ["sw.js"]:
            src = ROOT / rel
            if src.is_file():
                dest = tmp_path / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
        for rel in COPY_DIRS:
            src = ROOT / rel
            if src.is_dir():
                copy_tree(src, tmp_path / rel)
        disable_pdf(tmp_path)

        if WWW.exists():
            shutil.rmtree(WWW)
        copy_tree(tmp_path, WWW)

    inject_native_script(WWW / "index.html")
    bundle_native(WWW)
    assert_store_www(WWW)
    print(f"Wrote store www to {WWW} (ESV + NIV quotations, no pdf/, source checkout unchanged).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
