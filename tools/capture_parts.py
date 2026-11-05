"""Capture part previews in light and dark for before/after review (HANDOFF T3, T4).

    python3 -m tools.capture_parts OUT_DIR [part ...]

Renders each registry part with its dependencies (as tools/verify_focus_ring.py
does) at 900px wide, --k-mscale 0, and writes OUT_DIR/<part>-<theme>.png.
Run `python3 build.py` first; the registry comes from dist/registry.json.
"""
import argparse
import http.server
import os
import threading
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright
from tools.verify_focus_ring import Quiet, load, registry_pages

ROOT = Path(__file__).resolve().parents[1]
MAIN = ['button', 'input', 'field', 'textarea', 'select', 'checkbox', 'radio', 'switch', 'modal', 'dropdown', 'popover', 'tooltip']


def capture(out, parts=MAIN):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    pages = {item['name']: (html, scripts) for item, html, scripts in registry_pages(parts)}
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'), args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 900, 'height': 600}, device_scale_factor=2)
            page.goto(f'http://127.0.0.1:{server.server_port}/tokens.css')
            for name in parts:
                for theme in ('light', 'dark'):
                    load(page, *pages[name])
                    page.evaluate('(t)=>{document.documentElement.dataset.theme=t;document.documentElement.style.setProperty("--k-mscale","0");document.getElementById("kata-focus-start").remove()}', theme)
                    page.wait_for_timeout(80)
                    page.locator('#kata-focus-part').screenshot(path=str(out / f'{name}-{theme}.png'))
            browser.close()
    finally:
        server.shutdown(); server.server_close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('out'); parser.add_argument('parts', nargs='*')
    args = parser.parse_args()
    capture(args.out, args.parts or MAIN)
    print('captured', len(args.parts or MAIN), 'parts x 2 themes into', args.out)
