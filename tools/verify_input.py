"""Input text contrast and state table (HANDOFF T4, Input).

    python3 -m tools.verify_input [--output DIR] [--check]

Opens tests/input-multi.html in Chromium at --k-mscale 0 and, in light and dark,
measures text contrast from pixels (see tools/verify_button.py) for the label,
typed value, placeholder, hint and error text, and the value in the focused,
invalid, read-only and disabled inputs. Disabled text is recorded but exempt
(WCAG 1.4.3). --check fails when an enabled text is below 4.5:1, a set differs
from set 1, or the console logs an error.
"""
import argparse
import http.server
import json
import os
import threading
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright
from tools.verify_button import text_contrast
from tools.verify_focus_ring import Quiet

ROOT = Path(__file__).resolve().parents[1]
MIN = 4.5
# (name, selector inside a set, state)
TARGETS = [
    ('label', 'label', None),
    ('value', 'input[aria-invalid]', None),
    ('placeholder', 'input[placeholder]', None),
    ('hint', '.hint', None),
    ('error', '.err', None),
    ('focused value', 'input[aria-invalid]', 'focus'),
    ('read-only value', 'input[readonly]', None),
    ('disabled value', 'input[disabled]', None),
]


def measure(page, theme):
    page.evaluate('(t)=>{document.documentElement.dataset.theme=t;document.documentElement.style.setProperty("--k-mscale","0")}', theme)
    rows = []
    for index in range(3):
        section = page.locator('section').nth(index)
        row = {'theme': theme, 'set': index + 1, 'rtl': index == 2}
        for name, selector, state in TARGETS:
            el = section.locator(selector.strip()).first
            page.evaluate('document.activeElement && document.activeElement.blur()')
            if state == 'focus':
                page.keyboard.press('Shift'); el.focus()
            page.wait_for_timeout(30)
            if name == 'label':
                # The label wraps its input; measure only the text line above it.
                box = el.bounding_box()
                png = page.screenshot(clip={'x': box['x'], 'y': box['y'], 'width': box['width'], 'height': 18})
            else:
                png = el.screenshot()
            value, bg, fg = text_contrast(png)
            row[name] = {'contrast': value, 'background': bg, 'text': fg}
        rows.append(row)
    return rows


def run(output=None):
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'), args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1100, 'height': 1400})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.goto(f'http://127.0.0.1:{server.server_port}/tests/input-multi.html')
            rows = measure(page, 'light') + measure(page, 'dark')
            browser.close()
    finally:
        server.shutdown(); server.server_close()
    result = {'rows': rows, 'console_errors': errors}
    if output:
        out = Path(output); out.mkdir(parents=True, exist_ok=True)
        (out / 'input-text.json').write_text(json.dumps(result, indent=1) + '\n')
    return result


def problems(result):
    found = [f'console: {e}' for e in result['console_errors']]
    first = {r['theme']: r for r in result['rows'] if r['set'] == 1}
    for r in result['rows']:
        for name, _, _ in TARGETS:
            if name != 'disabled value' and r[name]['contrast'] < MIN:
                found.append(f"{r['theme']} set {r['set']} {name}: {r[name]['contrast']}:1 < {MIN}:1")
            if abs(r[name]['contrast'] - first[r['theme']][name]['contrast']) > 0.05:
                found.append(f"{r['theme']} set {r['set']} {name}: differs from set 1")
    return found


def table(result):
    lines = ['| Text | Light | Dark |', '|---|---:|---:|']
    rows = {r['theme']: r for r in result['rows'] if r['set'] == 1}
    for name, _, _ in TARGETS:
        lines.append(f"| {name} | {rows['light'][name]['contrast']} | {rows['dark'][name]['contrast']} |")
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run(args.output)
    print(table(result))
    found = problems(result)
    for line in found:
        print('PROBLEM', line)
    print(f"{len(result['rows'])} set rows, {len(found)} problems, {len(result['console_errors'])} console errors")
    if args.check and found:
        raise SystemExit(1)
