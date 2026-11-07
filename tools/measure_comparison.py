"""Measure the ten-screen comparison drafts (docs/design/ai-comparison.md).

Usage: python3 -m tools.measure_comparison [--check]

Each comparison/<screen>/ holds prompt.md, direct.html (A) and kata.html (B), kept
exactly as the agent first wrote them. Both drafts get the same measurements:

  focusInvisible   Tab stops whose outline, shadow, border and background do not
                   change on focus and whose pixels do not change either
                   (the tools/verify_focus_ring rule)
  unnamed          focusable controls with an empty accessible name (Chromium AX tree)
  buttonNoType     <button> elements without a type attribute
  lowContrast      text below 4.5:1 against its composited background, disabled
                   controls and the unpainted value of checkbox/radio-like inputs
                   excluded (the tools/capture_text_contrast metric)
  colors           distinct computed text, background and border colors
  spacings         distinct non-zero margin, padding and gap values
  overflow         visible elements that extend past a 390px viewport with
                   dark scheme and dir=rtl (inside scrollers excluded)
  consoleErrors    page errors and console errors on load (the automatic
                   favicon.ico request is ignored)
  bytes            file size

Screenshots go to comparison/shots/. --check re-measures and fails when the
numbers differ from comparison/results.json.
"""
import functools
import http.server
import json
import os
import re
import shutil
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'comparison'
SHOTS = DIR / 'shots'
CHROMIUM = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or '/usr/bin/chromium'
SCREENS = ['sign-in', 'sign-up', 'settings', 'pricing', 'dashboard',
           'data-table', 'checkout', 'inbox', 'empty-state', 'delete-confirm']
DRAFTS = {'direct': 'direct.html', 'kata': 'kata.html'}
MAX_STOPS = 400
ROLES = {'button', 'link', 'textbox', 'searchbox', 'checkbox', 'radio', 'combobox', 'switch',
         'slider', 'spinbutton', 'menuitem', 'tab', 'listbox', 'option', 'menuitemcheckbox',
         'menuitemradio', 'treeitem'}

STYLE = r'''e => {
  const pick = n => { if (!n) return ''; const s = getComputedStyle(n);
    return [s.outlineStyle, s.outlineWidth, s.outlineColor, s.boxShadow, s.borderTopColor, s.borderInlineStartColor, s.backgroundColor].join('|'); };
  const label = (e.labels && e.labels[0]) || null;
  return [pick(e), pick(label), pick(e.parentElement), pick(e.parentElement && e.parentElement.parentElement)].join('#');
}'''

VALUES = r'''() => {
  const colors = new Set(), spaces = new Set();
  for (const e of document.querySelectorAll('body, body *')) {
    const r = e.getBoundingClientRect(), s = getComputedStyle(e);
    if (!r.width || !r.height || s.display === 'none' || s.visibility === 'hidden') continue;
    const add = c => { if (c && !/^rgba\(\d+, \d+, \d+, 0\)$/.test(c) && c !== 'transparent') colors.add(c); };
    add(s.color); add(s.backgroundColor);
    for (const side of ['Top', 'Right', 'Bottom', 'Left'])
      if (parseFloat(s['border' + side + 'Width']) > 0) add(s['border' + side + 'Color']);
    for (const p of ['marginTop','marginRight','marginBottom','marginLeft','paddingTop','paddingRight','paddingBottom','paddingLeft','rowGap','columnGap']) {
      const v = s[p]; if (v && v !== 'normal' && parseFloat(v) !== 0) spaces.add(v);
    }
  }
  return [colors.size, spaces.size];
}'''

OVERFLOW = r'''() => {
  const vw = document.documentElement.clientWidth; let n = 0;
  const clips = s => s.overflowX !== 'visible' || s.overflowY !== 'visible';
  for (const e of document.querySelectorAll('body *')) {
    const s = getComputedStyle(e), r = e.getBoundingClientRect();
    if (!r.width || !r.height || s.display === 'none' || s.visibility === 'hidden' || s.position === 'fixed') continue;
    let inside = false;
    for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) if (clips(getComputedStyle(a))) { inside = true; break; }
    if (inside) continue;
    if (r.right > vw + 1 || r.left < -1) n++;
  }
  return n;
}'''


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def focus_invisible(page):
    from tools.verify_torture import pixel_focus_change
    page.mouse.click(1, 1)
    seen, hidden = set(), 0
    for _ in range(MAX_STOPS):
        page.keyboard.press('Tab')
        el = page.evaluate_handle('() => document.activeElement').as_element()
        if el is None or el.evaluate('e => e === document.body || e === document.documentElement'):
            break
        key = el.evaluate('e => { if (!e.dataset.cmpKey) e.dataset.cmpKey = String(Math.random()); return e.dataset.cmpKey }')
        if key in seen:
            break
        seen.add(key)
        focused = el.evaluate(STYLE)
        el.evaluate('e => e.blur()')
        blurred = el.evaluate(STYLE)
        if focused == blurred and not pixel_focus_change(page, el):
            hidden += 1
        page.keyboard.press('Shift')
        el.focus()
    return hidden, len(seen)


def unnamed(page):
    client = page.context.new_cdp_session(page)
    nodes = client.send('Accessibility.getFullAXTree')['nodes']
    count = 0
    for node in nodes:
        if node.get('ignored'):
            continue
        role = (node.get('role') or {}).get('value')
        name = ((node.get('name') or {}).get('value') or '').strip()
        if role in ROLES and not name:
            count += 1
    client.detach()
    return count


def low_contrast(page):
    from tools.capture_shape_migration import CONTRAST_METRICS
    from tools.capture_toast_tokens import contrast
    # The shared metric reads an input's value as its text; checkbox, radio and other
    # non-text inputs carry a value ("on") that is never painted, so skip them.
    hidden_values = set(page.evaluate('''() => [...document.body.querySelectorAll('*')].map((e, i) =>
      e.matches('input:is([type=checkbox],[type=radio],[type=range],[type=color],[type=hidden],[type=file])') ? i : -1).filter(i => i >= 0)'''))
    low = 0
    for row in page.evaluate(CONTRAST_METRICS):
        if row.get('disabled') or (row['index'] in hidden_values and row['kind'] == 'text'):
            continue
        fg = 'rgb(' + ','.join(str(n) for n in row['foreground']) + ')'
        bg = 'rgb(' + ','.join(str(n) for n in row['background']) + ')'
        if contrast(fg, bg) < 4.5:
            low += 1
    return low


def measure(browser, base, screen, draft):
    path = DIR / screen / DRAFTS[draft]
    html = path.read_text(encoding='utf-8')
    out = {'bytes': path.stat().st_size,
           'buttonNoType': len([m for m in re.finditer(r'<button\b[^>]*>', html, re.I) if not re.search(r'\btype\s*=', m.group(0), re.I)])}
    url = f'{base}/comparison/{screen}/{DRAFTS[draft]}'
    errors = []
    page = browser.new_page(viewport={'width': 1280, 'height': 900}, color_scheme='light', reduced_motion='reduce')
    page.on('pageerror', lambda e: errors.append(str(e)))
    # The local test server has no favicon; the browser's automatic favicon request is not the draft's.
    page.on('console', lambda m: m.type == 'error' and 'favicon.ico' not in (m.location or {}).get('url', '') and errors.append(m.text))
    page.goto(url)
    page.wait_for_timeout(400)
    out['consoleErrors'] = len(errors)
    page.screenshot(path=str(SHOTS / f'{screen}-{draft}-light.png'))
    out['colors'], out['spacings'] = page.evaluate(VALUES)
    out['lowContrast'] = low_contrast(page)
    out['unnamed'] = unnamed(page)
    out['focusInvisible'], out['tabStops'] = focus_invisible(page)
    page.close()
    page = browser.new_page(viewport={'width': 1280, 'height': 900}, color_scheme='dark', reduced_motion='reduce')
    page.goto(url)
    page.wait_for_timeout(400)
    page.screenshot(path=str(SHOTS / f'{screen}-{draft}-dark.png'))
    out['lowContrastDark'] = low_contrast(page)
    page.close()
    page = browser.new_page(viewport={'width': 390, 'height': 844}, color_scheme='dark', reduced_motion='reduce')
    page.goto(url)
    page.evaluate('() => document.documentElement.setAttribute("dir", "rtl")')
    page.wait_for_timeout(300)
    out['overflow'] = page.evaluate(OVERFLOW)
    page.close()
    return out


def run():
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(parents=True, exist_ok=True)
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    screens = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                for screen in SCREENS:
                    title = (DIR / screen / 'prompt.md').read_text(encoding='utf-8').splitlines()[0].lstrip('# ').strip()
                    screens.append({'slug': screen, 'title': title,
                                    **{d: measure(browser, base, screen, d) for d in DRAFTS}})
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    return {'agent': 'Claude (Anthropic) via Claude Code', 'generated': '2026-11-07', 'screens': screens}


def main(argv):
    data = run()
    target = DIR / 'results.json'
    if '--check' in argv:
        known = json.loads(target.read_text(encoding='utf-8'))
        differ = [(a['slug'], d, k) for a, b in zip(data['screens'], known['screens'])
                  for d in DRAFTS for k in a[d] if a[d][k] != b[d].get(k)]
        for item in differ:
            print('DIFF', *item)
        return 1 if differ else 0
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    for s in data['screens']:
        print(s['slug'], {d: {k: v for k, v in s[d].items() if k != 'bytes'} for d in DRAFTS})
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
