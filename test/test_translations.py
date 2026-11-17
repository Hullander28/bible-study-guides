#!/usr/bin/env python3
"""Mobile viewport tests for the translation picker. Run from the repo root:

    python3 test/test_translations.py
"""
from __future__ import annotations

import http.server
import os
import socketserver
import sys
import threading
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = Path(__file__).resolve().parent / "screenshots"
PORT = 0
BASE = None

# Known texts for Genesis 1:1
TEXTS = {
    "BSB": "In the beginning God created the heavens and the earth.",
    "NIV": "In the beginning God created the heavens and the earth.",
    "KJV": "In the beginning God created the heaven and the earth.",
    "ESV": "In the beginning, God created the heavens and the earth.",
}
LSV_NOTICE = "Literal Standard Version (LSV) © 2020 Covenant Press"
NIV_NOTICE = "Biblica, Inc."
ESV_NOTICE = "English Standard Version®"
VIEWPORTS = {
    "iphone": {
        "name": "iPhone 13",
        # Playwright device if present; fallback below.
        "fallback": {
            "viewport": {"width": 390, "height": 844},
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "device_scale_factor": 3,
            "is_mobile": True,
            "has_touch": True,
        },
    },
    "android": {
        "name": "Pixel 7",
        "fallback": {
            "viewport": {"width": 412, "height": 915},
            "user_agent": "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
            "device_scale_factor": 2.625,
            "is_mobile": True,
            "has_touch": True,
        },
    },
}


def start_server():
    os.chdir(ROOT)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

    httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
    httpd.allow_reuse_address = True
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    global PORT, BASE
    PORT = httpd.server_address[1]
    BASE = f"http://127.0.0.1:{PORT}"
    return httpd


def ctx_kwargs(pw, key):
    spec = VIEWPORTS[key]
    if spec["name"] in pw.devices:
        d = dict(pw.devices[spec["name"]])
        d.pop("default_browser_type", None)
        return d
    return dict(spec["fallback"])


def collect_errors(page):
    errors = []
    page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
    page.on("console", lambda msg: errors.append(f"console.{msg.type}: {msg.text}") if msg.type == "error" else None)
    return errors


def wait_ready(page):
    page.goto(BASE + "/", wait_until="domcontentloaded")
    page.wait_for_function("() => document.querySelectorAll('#trPick option').length >= 14", timeout=15000)
    page.wait_for_selector(".votd, .today, h1", timeout=15000)


def genesis_quote(page):
    loc = page.locator(".card blockquote").first
    loc.wait_for(timeout=10000)
    return loc.inner_text()


def set_header_tr(page, code):
    page.locator("#trPick").select_option(code)
    page.wait_for_timeout(200)


def test_device(pw, browser, key, results):
    label = VIEWPORTS[key]["name"]
    errors = []
    context = browser.new_context(**ctx_kwargs(pw, key), service_workers="block")
    page = context.new_page()
    errors = collect_errors(page)
    wait_ready(page)

    # Default is BSB
    assert page.locator("#trPick").input_value() == "BSB", f"{label}: default is not BSB"
    opts = page.locator("#trPick option").evaluate_all("els => els.map(e => e.value)")
    assert opts[0] == "ESV" and "BSB" in opts and "NIV" in opts and "KJV" in opts and "WEB" in opts, f"{label}: picker options {opts}"
    assert opts[1] == "BSB" and opts[2] == "NIV", f"{label}: expected BSB then NIV after ESV, got {opts}"
    assert len(opts) == 15, f"{label}: expected 15 options (ESV + BSB + NIV + 12), got {len(opts)} {opts}"

    # Header picker is visible and inside the viewport
    box = page.locator("#trPick").bounding_box()
    vp = page.viewport_size
    assert box and box["y"] >= 0 and box["x"] >= 0, f"{label}: picker not visible"
    assert box["x"] + box["width"] <= vp["width"] + 1, f"{label}: picker overflows width"
    assert box["y"] + box["height"] <= vp["height"] + 1, f"{label}: picker overflows height"

    SHOTS.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(SHOTS / f"picker-{key}-home.png"), full_page=False)

    # Open Genesis key verses and check text swaps
    page.goto(BASE + "/#/b/genesis/t/verses", wait_until="domcontentloaded")
    page.wait_for_selector("blockquote", timeout=10000)
    body = genesis_quote(page)
    assert TEXTS["BSB"] in body, f"{label}: BSB Genesis 1:1 missing in {body!r}"

    set_header_tr(page, "KJV")
    page.wait_for_selector("blockquote", timeout=10000)
    body = genesis_quote(page)
    assert TEXTS["KJV"] in body, f"{label}: KJV Genesis 1:1 missing in {body!r}"
    assert "BibleGateway (KJV)" in page.content() or "version=KJV" in page.content()

    set_header_tr(page, "NIV")
    page.wait_for_selector("blockquote", timeout=10000)
    body = genesis_quote(page)
    assert TEXTS["NIV"] in body, f"{label}: NIV Genesis 1:1 missing in {body!r}"
    foot = page.locator(".foot").inner_text()
    assert NIV_NOTICE in foot and "New International Version" in foot, f"{label}: NIV footer missing: {foot!r}"
    assert "BibleGateway (NIV)" in page.content() or "version=NIV" in page.content()

    set_header_tr(page, "ESV")
    page.wait_for_selector("blockquote", timeout=10000)
    body = genesis_quote(page)
    assert TEXTS["ESV"] in body, f"{label}: ESV Genesis 1:1 missing in {body!r}"
    foot = page.locator(".foot").inner_text()
    assert "Crossway" in foot and "ESV" in foot, f"{label}: ESV footer missing: {foot!r}"

    set_header_tr(page, "LSV")
    page.wait_for_selector("blockquote", timeout=10000)
    foot = page.locator(".foot").inner_text()
    assert LSV_NOTICE in foot, f"{label}: LSV attribution missing: {foot!r}"

    set_header_tr(page, "BSB")
    page.screenshot(path=str(SHOTS / f"picker-{key}-verses.png"), full_page=False)

    # Settings picker
    page.goto(BASE + "/#/settings", wait_until="domcontentloaded")
    page.wait_for_selector("#trSel", timeout=10000)
    assert page.locator("#trSel").input_value() == "BSB"
    note = page.locator("#trNote").inner_text()
    assert "Berean Standard Bible" in note
    settings_opts = page.locator("#trSel option").evaluate_all("els => els.map(e => e.value)")
    assert "NIV" in settings_opts and settings_opts[0] == "ESV"
    page.screenshot(path=str(SHOTS / f"picker-{key}-settings.png"), full_page=False)

    # No console/page errors
    # Filter benign noise if any
    real = [e for e in errors if "favicon" not in e.lower()]
    assert not real, f"{label}: JS errors: {real}"

    context.close()
    results.append(f"{label}: ok")


def test_offline(pw, browser, results):
    """Service worker is allowed so a reload works with the network dropped."""
    context = browser.new_context(**ctx_kwargs(pw, "iphone"))
    page = context.new_page()
    errors = collect_errors(page)
    wait_ready(page)
    page.goto(BASE + "/#/b/genesis/t/verses", wait_until="networkidle")
    page.wait_for_selector("blockquote", timeout=10000)
    page.wait_for_function(
        """async () => {
          if (!navigator.serviceWorker) return false;
          const r = await navigator.serviceWorker.ready;
          if (!r) return false;
          const keys = await caches.keys();
          const cache = keys.length ? await caches.open(keys[0]) : null;
          if (!cache) return false;
          const hit = await cache.match('data/verses.json') || await cache.match('/data/verses.json');
          return !!hit;
        }""",
        timeout=30000,
    )
    context.set_offline(True)
    page.reload(wait_until="domcontentloaded")
    page.wait_for_function("() => document.querySelectorAll('#trPick option').length >= 13 || document.querySelector('blockquote') || document.querySelector('h1')", timeout=15000)
    page.wait_for_selector("h1, blockquote", timeout=15000)
    # Navigate around offline
    page.goto(BASE + "/#/memory", wait_until="domcontentloaded")
    page.wait_for_selector("blockquote, h1", timeout=10000)
    assert "Genesis 1:1" in page.content() or page.locator("blockquote").count() > 0
    page.goto(BASE + "/#/b/genesis/t/verses", wait_until="domcontentloaded")
    page.wait_for_selector("blockquote", timeout=10000)
    body = genesis_quote(page)
    assert TEXTS["BSB"] in body, f"offline Genesis 1:1 missing in {body!r}"
    real = [e for e in errors if "favicon" not in e.lower() and "failed to load" not in e.lower()]
    # Offline reload may log a failed network fetch before the SW answers; allow those.
    real = [e for e in real if "ERR_INTERNET_DISCONNECTED" not in e and "Failed to fetch" not in e and "net::ERR" not in e]
    assert not real, f"offline JS errors: {real}"
    context.close()
    results.append("offline: ok")


def test_set_esv_script(results):
    import tempfile, shutil, subprocess, json, re
    tmp = Path(tempfile.mkdtemp(prefix="bsg-esv-"))
    try:
        for rel in [
            "js/config.js",
            "sw.js",
            "data/verses-esv.json",
            "tools/esv-quotes.json",
            "tools/set_esv.py",
        ]:
            dest = tmp / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dest)
        env = dict(os.environ)
        r = subprocess.run([sys.executable, str(tmp / "tools/set_esv.py"), "--off"], cwd=tmp, check=True, capture_output=True, text=True)
        cfg = (tmp / "js/config.js").read_text()
        assert "ESV_ENABLED: false" in cfg
        assert "verses-esv.json" not in (tmp / "sw.js").read_text()
        assert not (tmp / "data/verses-esv.json").exists()
        subprocess.run([sys.executable, str(tmp / "tools/set_esv.py"), "--on"], cwd=tmp, check=True, capture_output=True, text=True)
        assert "ESV_ENABLED: true" in (tmp / "js/config.js").read_text()
        assert "verses-esv.json" in (tmp / "sw.js").read_text()
        esv = json.loads((tmp / "data/verses-esv.json").read_text())
        assert "Genesis 1:1" in esv
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    results.append("set_esv.py --off/--on: ok")


def test_store_www_flags(results):
    """Store copy: ESV + NIV verse text bundled, pdf/ omitted, PDF button flag off."""
    import importlib.util, tempfile, shutil
    spec = importlib.util.spec_from_file_location("bsw", ROOT / "tools" / "build_store_www.py")
    bsw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bsw)
    assert "pdf" not in bsw.COPY_DIRS
    tmp = Path(tempfile.mkdtemp(prefix="bsg-www-"))
    try:
        for rel in bsw.COPY_DIRS:
            shutil.copytree(ROOT / rel, tmp / rel)
        bsw.disable_pdf(tmp)
        bsw.assert_store_www(tmp)
        import json
        esv = json.loads((tmp / "data/verses-esv.json").read_text())
        ver = json.loads((tmp / "data/verses.json").read_text())
        assert set(esv) == set(ver), "ESV keys differ from verses.json keys"
        assert all(row.get("NIV") for row in ver.values()), "NIV missing for some verses"
        assert "PDF_ENABLED: true" in (ROOT / "js/config.js").read_text(), "repo config must keep PDFs on for the website"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    results.append("store www: ESV + NIV bundled, no pdf/, PDF button off: ok")


def main():
    httpd = start_server()
    time.sleep(0.2)
    results = []
    failed = []
    try:
        test_set_esv_script(results)
        test_store_www_flags(results)
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, channel='chrome')
            for key in ("iphone", "android"):
                try:
                    test_device(pw, browser, key, results)
                except Exception as e:
                    failed.append(f"{VIEWPORTS[key]['name']}: {e}")
            try:
                test_offline(pw, browser, results)
            except Exception as e:
                failed.append(f"offline: {e}")
            browser.close()
    finally:
        httpd.shutdown()
    for line in results:
        print("PASS", line)
    if failed:
        for line in failed:
            print("FAIL", line)
        sys.exit(1)
    print("All translation tests passed.")
    print("Screenshots:")
    for p in sorted(SHOTS.glob("picker-*.png")):
        print(" ", p)


if __name__ == "__main__":
    main()
