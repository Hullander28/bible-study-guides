#!/usr/bin/env python3
"""Build mobile/www for App Store / Google Play.

Copies the site into a temporary directory, runs `tools/set_esv.py --off` on
that copy only, then writes the result to mobile/www. The git checkout (and
GitHub Pages / main) is never modified. mobile/www is gitignored and must not
be committed.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOBILE = ROOT / "mobile"
WWW = MOBILE / "www"
SET_ESV = ROOT / "tools" / "set_esv.py"

# Paths to copy into the store bundle (relative to repo root).
COPY_FILES = [
    "index.html",
    "manifest.webmanifest",
    "privacy.html",
    ".nojekyll",
]
# Do not copy pdf/. Those printable guides still quote ESV, and Crossway
# has not licensed ESV for store builds. The website keeps the existing PDFs.
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


def assert_esv_off(www: Path) -> None:
    cfg = (www / "js" / "config.js").read_text()
    if "ESV_ENABLED: false" not in cfg:
        raise SystemExit("Store www still has ESV enabled")
    if (www / "data" / "verses-esv.json").exists():
        raise SystemExit("Store www still contains data/verses-esv.json")
    if (www / "pdf").exists():
        raise SystemExit("Store www still contains pdf/ (ESV printable guides)")
    sw = www / "sw.js"
    if sw.is_file() and "verses-esv.json" in sw.read_text():
        raise SystemExit("Store www sw.js still lists verses-esv.json")
    # Safety: the source checkout must still be the web (ESV-on) build.
    src_cfg = (ROOT / "js" / "config.js").read_text()
    if "ESV_ENABLED: true" not in src_cfg:
        raise SystemExit("Repo js/config.js is not ESV-on; aborting so main is not left off")
    if not (ROOT / "data" / "verses-esv.json").is_file():
        raise SystemExit("Repo data/verses-esv.json is missing; aborting")


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
    if not SET_ESV.is_file():
        raise SystemExit(f"Missing {SET_ESV}")
    with tempfile.TemporaryDirectory(prefix="bsg-store-www-") as tmp:
        tmp_path = Path(tmp)
        for rel in COPY_FILES:
            src = ROOT / rel
            if src.is_file():
                dest = tmp_path / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
        for rel in COPY_DIRS:
            src = ROOT / rel
            if src.is_dir():
                copy_tree(src, tmp_path / rel)
        # set_esv.py --on needs tools/esv-quotes.json; --off only deletes data and edits js/sw.
        # Copy set_esv + quotes so --root is sufficient and the script can be run standalone.
        tools = tmp_path / "tools"
        tools.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SET_ESV, tools / "set_esv.py")
        quotes = ROOT / "tools" / "esv-quotes.json"
        if quotes.is_file():
            shutil.copy2(quotes, tools / "esv-quotes.json")
        if (ROOT / "sw.js").is_file():
            shutil.copy2(ROOT / "sw.js", tmp_path / "sw.js")

        subprocess.run(
            [sys.executable, str(SET_ESV), "--off", "--root", str(tmp_path)],
            check=True,
        )
        # Do not copy tools/ into www.
        if tools.exists():
            shutil.rmtree(tools)

        if WWW.exists():
            shutil.rmtree(WWW)
        copy_tree(tmp_path, WWW)

    inject_native_script(WWW / "index.html")
    bundle_native(WWW)
    assert_esv_off(WWW)
    print(f"Wrote store www to {WWW} (ESV off, source checkout unchanged).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
