"""Run the Torture Test matrix over tests/torture.html.

Usage:
  python3 -m tools.verify_torture            # run all 8 conditions, rewrite docs/review/torture/
  python3 -m tools.verify_torture --check    # run and fail only on failures not in results.json

Conditions: direction (ltr, rtl) x theme (light, dark) x zoom (100% = 1280px wide,
200% = 640px wide, the usual reflow stand-in for browser zoom).

Checks per condition:
  A errors        page errors and console errors
  B page-overflow the document scrolls sideways
  C part-overflow content sticks out of an instance stage (clipped scrollers excluded)
  D keyboard      Tab reaches the end of the page without a trap
  E focus-visible every Tab stop changes outline, shadow, border or background on focus
  F parity        the three instances of a part have the same number of Tab stops

E is a style-change check. The pixel and 3:1 contrast check stays in tools/verify_focus_ring.
"""
import functools
import os
import http.server
import json
import shutil
import sys
import threading
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'review' / 'torture'
CHROMIUM = os.environ.get('CHROMIUM_PATH') or shutil.which('chromium') or '/usr/bin/chromium'
WIDTHS = {'100': 1280, '200': 640}
CONDITIONS = [f'{d}-{t}-{z}' for d in ('ltr', 'rtl') for t in ('light', 'dark') for z in ('100', '200')]
CHECKS = {'A': 'errors', 'B': 'page-overflow', 'C': 'part-overflow', 'D': 'keyboard', 'E': 'focus-visible', 'F': 'parity'}
MAX_STOPS = 1500

OVERFLOW = r'''() => {
  const out = [];
  const clips = s => s.overflowX !== 'visible' || s.overflowY !== 'visible' || s.clipPath !== 'none';
  document.querySelectorAll('.tt-stage').forEach(stage => {
    const box = stage.getBoundingClientRect();
    let worst = 0, who = '';
    stage.querySelectorAll('*').forEach(el => {
      if (!el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) return;
      const s = getComputedStyle(el);
      if (s.position === 'fixed') return;
      for (let a = el.parentElement; a && a !== stage; a = a.parentElement) {
        if (clips(getComputedStyle(a))) return;   // inside a scroller or clip: cannot stick out
        if (getComputedStyle(a).position === 'fixed') return;
      }
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      const over = Math.max(box.left - r.left, r.right - box.right);
      if (over > worst) { worst = over; who = el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/)[0] : ''); }
    });
    if (worst > 1) out.push({ stage: stage.getAttribute('aria-label'), part: stage.closest('article').id.slice(5), px: Math.round(worst), element: who });
  });
  return out;
}'''

STYLE = r'''e => {
  const pick = n => { if (!n) return ''; const s = getComputedStyle(n);
    return [s.outlineStyle, s.outlineWidth, s.outlineColor, s.boxShadow, s.borderTopColor, s.borderInlineStartColor, s.backgroundColor].join('|'); };
  const label = (e.labels && e.labels[0]) || null;
  return [pick(e), pick(label), pick(e.parentElement), pick(e.parentElement && e.parentElement.parentElement)].join('#');
}'''

WHERE = r'''e => {
  const stage = e.closest('.tt-stage'), part = e.closest('article.tt-part');
  return { stage: stage ? stage.getAttribute('aria-label') : '', part: part ? part.id.slice(5) : '',
    label: (e.getAttribute('aria-label') || e.textContent || e.getAttribute('placeholder') || e.value || '').trim().replace(/\s+/g, ' ').slice(0, 40),
    tag: e.tagName.toLowerCase() };
}'''


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def pixel_focus_change(page, el):
    """Focused vs blurred crop around one control, judged like tools/verify_focus_ring."""
    import io
    from PIL import Image
    from tools.verify_focus_ring import MARGIN, VISIBLE, changed
    el.scroll_into_view_if_needed()
    page.keyboard.press('Shift')
    el.focus()
    x, y, w, h = el.evaluate('e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.width, r.height] }')
    vw, vh = page.viewport_size['width'], page.viewport_size['height']
    clip = {'x': max(0, x - MARGIN), 'y': max(0, y - MARGIN)}
    clip['width'] = min(vw, x + w + MARGIN) - clip['x']
    clip['height'] = min(vh, y + h + MARGIN) - clip['y']
    if clip['width'] < 1 or clip['height'] < 1:
        return False
    page.wait_for_timeout(20)
    focused = Image.open(io.BytesIO(page.screenshot(clip=clip)))
    el.evaluate('e => e.blur()')
    page.wait_for_timeout(20)
    blurred = Image.open(io.BytesIO(page.screenshot(clip=clip)))
    inner = (round(x - clip['x']), round(y - clip['y']), round(x - clip['x'] + w), round(y - clip['y'] + h))
    return changed(focused, blurred, inner)[1] >= VISIBLE


def run_condition(browser, base, condition):
    direction, theme, zoom = condition.split('-')
    page = browser.new_page(viewport={'width': WIDTHS[zoom], 'height': 900})
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda m: m.type == 'error' and errors.append(m.text))
    page.goto(f'{base}/tests/torture.html?dir={direction}&theme={theme}')
    page.evaluate('() => document.documentElement.style.setProperty("--k-mscale", "0")')
    page.wait_for_timeout(300)
    failures = []
    if errors:
        failures.append({'check': 'A', 'part': '(page)', 'detail': '; '.join(errors)[:300]})
    width = page.evaluate('() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]')
    if width[0] > width[1] + 1:
        failures.append({'check': 'B', 'part': '(page)', 'detail': f'document is {width[0]}px wide in a {width[1]}px viewport'})
    for item in page.evaluate(OVERFLOW):
        failures.append({'check': 'C', 'part': item['part'], 'detail': f"{item['stage']}: {item['element']} sticks out {item['px']}px"})
    # D/E/F: walk Tab stops from the top of the page.
    page.mouse.click(1, 1)
    page.keyboard.press('Shift')
    per_stage, seen, stops, reached_end = Counter(), set(), 0, False
    for _ in range(MAX_STOPS):
        page.keyboard.press('Tab')
        el = page.evaluate_handle('() => document.activeElement').as_element()
        if el is None or el.evaluate('e => e === document.body || e === document.documentElement'):
            reached_end = True
            break
        key = el.evaluate('e => { if (!e.dataset.ttKey) e.dataset.ttKey = String(Math.random()); return e.dataset.ttKey }')
        if key in seen:
            reached_end = True   # wrapped around to an earlier stop: the walk is complete
            break
        seen.add(key)
        stops += 1
        where = el.evaluate(WHERE)
        if where['stage']:
            per_stage[where['stage']] += 1
        focused = el.evaluate(STYLE)
        el.evaluate('e => e.blur()')
        blurred = el.evaluate(STYLE)
        # A focus style drawn on a pseudo-element (the range thumb) leaves computed styles
        # unchanged; fall back to the pixel test from tools/verify_focus_ring for that stop.
        if focused == blurred and not pixel_focus_change(page, el):
            failures.append({'check': 'E', 'part': where['part'] or '(page)',
                             'detail': f"{where['stage'] or 'toolbar'}: <{where['tag']}> \"{where['label']}\" shows no focus change"})
        page.keyboard.press('Shift')
        el.focus()
    if not reached_end:
        failures.append({'check': 'D', 'part': '(page)', 'detail': f'Tab did not reach the end within {MAX_STOPS} stops'})
    groups = defaultdict(dict)
    for stage, count in per_stage.items():
        name, _, n = stage.rpartition(' ')
        groups[name][n] = count
    titles = page.evaluate('() => Object.fromEntries([...document.querySelectorAll("article.tt-part")].map(a => [a.querySelector("h2").textContent, a.id.slice(5)]))')
    for name, counts in groups.items():
        values = [counts.get(str(n), 0) for n in (1, 2, 3)]
        if len(set(values)) > 1:
            failures.append({'check': 'F', 'part': titles.get(name, name), 'detail': f'Tab stops per instance {values}'})
    page.close()
    return {'tab_stops': stops, 'failures': failures}


def run():
    from playwright.sync_api import sync_playwright
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    results = {}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=CHROMIUM, args=['--no-sandbox'])
            try:
                for condition in CONDITIONS:
                    results[condition] = run_condition(browser, base, condition)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()
    return results


def keys(results):
    return {(c, f['part'], f['check']) for c, r in results.items() for f in r['failures']}


def write(results):
    OUT.mkdir(parents=True, exist_ok=True)
    data = {'conditions': CONDITIONS, 'checks': CHECKS, 'results': results}
    (OUT / 'results.json').write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    parts_failing = sorted({(f['part'], f['check']) for r in results.values() for f in r['failures']})
    lines = ['# Torture Test results', '',
             'Generated by `python3 -m tools.verify_torture` over `tests/torture.html` '
             '(40 parts × 3, built by `python3 -m tools.build_torture`). '
             'CI fails only on a failure that is not listed here; fixing one removes it.', '',
             '| Condition | Tab stops | A | B | C | D | E | F |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for c in CONDITIONS:
        count = Counter(f['check'] for f in results[c]['failures'])
        lines.append(f"| {c} | {results[c]['tab_stops']} | " + ' | '.join(str(count.get(k, 0)) for k in CHECKS) + ' |')
    lines += ['', 'Checks: ' + ', '.join(f'{k} {v}' for k, v in CHECKS.items()) + '.', '',
              '## Failing parts', '']
    if not parts_failing:
        lines.append('None.')
    for part, check in parts_failing:
        where = [c for c in CONDITIONS if any(f['part'] == part and f['check'] == check for f in results[c]['failures'])]
        sample = next(f['detail'] for c in where for f in results[c]['failures'] if f['part'] == part and f['check'] == check)
        lines.append(f'- **{part}** — {check} {CHECKS[check]} in {len(where)}/8 ({", ".join(where)}). Example: {sample}')
    lines += ['', '## Not verified', '',
              '- 200% uses a 640px viewport (the reflow stand-in), not real browser zoom.',
              '- E is a style-change check with a pixel fallback; the 3:1 contrast check stays in `tools/verify_focus_ring`.',
              '- Screen readers (VoiceOver, NVDA), Safari, Firefox, touch devices and real IME input.']
    (OUT / 'README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main(argv):
    results = run()
    if '--check' in argv:
        known = json.loads((OUT / 'results.json').read_text(encoding='utf-8'))['results']
        new = sorted(keys(results) - keys(known))
        for c, part, check in new:
            print(f'NEW {c} {part} {check} {CHECKS[check]}')
        print(f'{len(keys(results))} recorded failure keys now, {len(keys(known))} in results.json, {len(new)} new')
        return 1 if new else 0
    write(results)
    print(f'wrote {OUT.relative_to(ROOT)}: ' + ', '.join(f"{c} {len(r['failures'])}" for c, r in results.items()))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
