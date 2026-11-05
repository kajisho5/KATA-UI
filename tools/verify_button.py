"""Button variant × state contrast table (HANDOFF T4, Button).

    python3 -m tools.verify_button [--output DIR] [--check]

Opens tests/button-multi.html in Chromium at --k-mscale 0. For the five color
variants (Primary, Secondary, Ghost, Accent, Danger) in each of the three sets,
including the RTL set, it captures the button in five states (default, hover,
pressed, keyboard focus, disabled) in light and dark. Text contrast is read
from pixels: the most common pixel in the button is its background and the
pixel with the highest contrast against it is its text (anti-aliasing can only
lower this, so the value is a ceiling of what an edge pixel shows and the
painted glyph core). Disabled text is recorded but exempt (WCAG 1.4.3).
--check fails when an enabled state is below 4.5:1 or a set differs from set 1.
"""
import argparse
import collections
import http.server
import io
import json
import os
import threading
from functools import partial
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
from tools.verify_focus_ring import Quiet, _lum

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ['pri', 'sec', 'ghost', 'accent', 'danger']
STATES = ['default', 'hover', 'pressed', 'focus', 'disabled']
MIN = 4.5


def ratio(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def text_contrast(png):
    image = Image.open(io.BytesIO(png)).convert('RGB')
    w, h = image.size
    # Ignore a 3px edge so borders, the focus ring and rounded corners are not the background.
    inner = image.crop((3, 3, max(4, w - 3), max(4, h - 3)))
    pixels = list(inner.get_flattened_data() if hasattr(inner, 'get_flattened_data') else inner.getdata())
    bg = collections.Counter(pixels).most_common(1)[0][0]
    fg = max(pixels, key=lambda p: ratio(p, bg))
    return round(ratio(fg, bg), 2), '#%02x%02x%02x' % bg, '#%02x%02x%02x' % fg


def measure(page, theme):
    page.evaluate('(t)=>{document.documentElement.dataset.theme=t;document.documentElement.style.setProperty("--k-mscale","0")}', theme)
    rows = []
    for index in range(3):
        section = page.locator('section').nth(index)
        for variant in VARIANTS:
            button = section.locator('.btn-' + variant).first
            row = {'theme': theme, 'set': index + 1, 'rtl': index == 2, 'variant': variant}
            for state in STATES:
                page.mouse.move(0, 0)
                page.evaluate('document.activeElement && document.activeElement.blur()')
                if state == 'hover':
                    button.hover()
                elif state == 'pressed':
                    button.hover(); page.mouse.down()
                elif state == 'focus':
                    page.keyboard.press('Shift'); button.focus()
                elif state == 'disabled':
                    button.evaluate('(e)=>e.disabled=true')
                page.wait_for_timeout(30)
                value, bg, fg = text_contrast(button.screenshot())
                row[state] = {'contrast': value, 'background': bg, 'text': fg}
                if state == 'pressed':
                    page.mouse.up()
                if state == 'disabled':
                    button.evaluate('(e)=>e.disabled=false')
            rows.append(row)
    return rows


def run(output=None):
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'), args=['--no-sandbox'])
            page = browser.new_page(viewport={'width': 1100, 'height': 800})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.goto(f'http://127.0.0.1:{server.server_port}/tests/button-multi.html')
            rows = measure(page, 'light') + measure(page, 'dark')
            browser.close()
    finally:
        server.shutdown(); server.server_close()
    result = {'rows': rows, 'console_errors': errors}
    if output:
        out = Path(output); out.mkdir(parents=True, exist_ok=True)
        (out / 'button-states.json').write_text(json.dumps(result, indent=1) + '\n')
    return result


def problems(result):
    found = [f'console: {e}' for e in result['console_errors']]
    first = {(r['theme'], r['variant']): r for r in result['rows'] if r['set'] == 1}
    for r in result['rows']:
        for state in STATES[:-1]:
            if r[state]['contrast'] < MIN:
                found.append(f"{r['theme']} set {r['set']} {r['variant']} {state}: {r[state]['contrast']}:1 < {MIN}:1")
        ref = first[(r['theme'], r['variant'])]
        if any(abs(r[s]['contrast'] - ref[s]['contrast']) > 0.05 for s in STATES):
            found.append(f"{r['theme']} set {r['set']} {r['variant']}: differs from set 1")
    return found


def table(result):
    names = {'pri': 'Primary', 'sec': 'Secondary', 'ghost': 'Ghost', 'accent': 'Accent', 'danger': 'Danger'}
    lines = ['| Theme | Variant | ' + ' | '.join(STATES) + ' |', '|---|---|' + '---:|' * len(STATES)]
    for r in result['rows']:
        if r['set'] == 1:
            lines.append(f"| {r['theme']} | {names[r['variant']]} | " + ' | '.join(f"{r[s]['contrast']}" for s in STATES) + ' |')
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
    print(f"{len(result['rows'])} variant rows, {len(found)} problems, {len(result['console_errors'])} console errors")
    if args.check and found:
        raise SystemExit(1)
