"""Replace raw spacing and type values in UI-profile parts with mold v4 tokens (HANDOFF T3).

Mappings follow the owner decisions recorded in docs/token-migration.md (T3):
spacing snaps to the 4px grid, ties go to the smaller step, 1px and 2px have
tokens; font sizes snap to the text steps; line heights follow KATA.md 0.5.
Only declarations that check.py reports are rewritten, in the file it names
(component CSS or an inline style in a preview HTML file).

    python3 -m tools.t3_migrate spacing [--dry-run]
    python3 -m tools.t3_migrate font-size [--dry-run]
    python3 -m tools.t3_migrate line-height [--dry-run]
"""
import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPACE = {1: 'px', 2: '0-5', 4: '1', 8: '2', 12: '3', 16: '4', 20: '5', 24: '6', 28: '7', 32: '8', 40: '10', 48: '12', 64: '16'}
TEXT = [(11, 'xs'), (12.5, 'sm'), (13.5, 'base'), (14, 'md'), (15, 'lead'), (16.5, 'lg'), (19, 'xl'), (24, '2xl'), (30, '3xl'), (44, 'display')]
# Font sizes that sit between two steps, as listed in the owner's chosen option.
TEXT_FIXED = {12: 'sm', 13: 'base', 11.5: 'xs', 14.5: 'lead', 15.5: 'lead', 16: 'lg', 17: 'lg'}
LEADING = {1: 'tight', 1.1: 'display', 1.12: 'display', 1.25: 'heading', 1.3: 'heading', 1.35: 'card', 1.4: 'card',
           1.5: 'small', 1.55: 'small', 1.6: 'small', 1.65: 'body', 1.7: 'body', 1.75: 'body', 1.8: 'loose', 1.85: 'loose'}
LENGTH = re.compile(r'(?<![\w.#-])(-?)(\d*\.?\d+)px\b')


def space_token(px):
    """4px grid, ties to the smaller step; 1px and 2px keep their own tokens; 3px goes to 4px."""
    if px in SPACE:
        return f'var(--k-space-{SPACE[px]})'
    if px < 4:
        return 'var(--k-space-1)'
    low = int(px // 4) * 4
    target = low if px - low <= 4 - (px - low) else low + 4
    if target in SPACE:
        return f'var(--k-space-{SPACE[target]})'
    return f'calc(var(--k-space-1) * {target // 4})'


def spacing_value(value):
    def swap(m):
        sign, number = m[1], float(m[2])
        if number == 0:
            return m[0]
        token = space_token(number)
        return f'calc({token} * -1)' if sign else token
    return LENGTH.sub(swap, value)


def text_token(px):
    if px in TEXT_FIXED:
        return f'var(--k-text-{TEXT_FIXED[px]})'
    size, name = min(TEXT, key=lambda step: (abs(step[0] - px), step[0]))
    return f'var(--k-text-{name})'


def font_size_value(value):
    return LENGTH.sub(lambda m: m[0] if float(m[2]) == 0 else text_token(float(m[2])), value)


def line_height_value(value):
    number = value.strip()
    try:
        key = float(number)
    except ValueError:
        return None
    return f'var(--k-lh-{LEADING[key]})' if key in LEADING else None


def findings():
    out = subprocess.run([sys.executable, 'check.py', '--json', '-'], cwd=ROOT, capture_output=True, text=True)
    if out.returncode > 1:
        raise SystemExit(out.stderr)
    data = json.loads(out.stdout)
    for item in data['items']:
        if item['profile'] != 'ui':
            continue
        for check in item['checks']:
            if check['id'] in ('spacing-values', 'type-values'):
                for detail in check.get('details', []):
                    yield check['id'], detail


def plan(category):
    edits, skipped = collections.defaultdict(list), []
    for check, d in findings():
        prop, value = d['property'], d['value']
        if category == 'spacing' and check == 'spacing-values':
            new = spacing_value(value)
        elif category == 'font-size' and check == 'type-values' and prop == 'font-size':
            new = font_size_value(value)
        elif category == 'line-height' and check == 'type-values' and prop == 'line-height':
            new = line_height_value(value)
        else:
            continue
        if not new or new == value:
            # A part-local custom property carries the raw value; rewrite its definition.
            names = re.findall(r'var\((--[\w-]+)\)', value)
            source = (ROOT / d['path']).read_text()
            done = False
            for name in names:
                m = re.search(r'(?<![\w-])' + re.escape(name) + r'\s*:\s*([^;}]+)', source)
                if m and convert(category, prop, m[1].strip()) not in (None, m[1].strip()):
                    edits[d['path']].append((name, m[1].strip(), convert(category, prop, m[1].strip()))); done = True
            if not done:
                skipped.append((d['path'], prop, value))
            continue
        edits[d['path']].append((prop, value, new))
    return edits, skipped


def convert(category, prop, value):
    if category == 'spacing':
        return spacing_value(value)
    if category == 'font-size':
        return font_size_value(value)
    return line_height_value(value)


def apply(edits, dry_run):
    changed = 0
    for path, items in sorted(edits.items()):
        file = ROOT / path
        text = original = file.read_text()
        for prop, value, new in dict.fromkeys(items):
            # The exact declaration as written, ending at ; } " or ' (CSS rule or inline style).
            pattern = re.compile(r'(?<![\w-])(' + re.escape(prop) + r'\s*:\s*)' + re.escape(value) + r'(?=\s*(?:!important\s*)?[;}"\'])')
            text, count = pattern.subn(lambda m: m[1] + new, text)
            if not count:
                print(f'NOT FOUND {path}: {prop}: {value}', file=sys.stderr)
            changed += count
        if text != original and not dry_run:
            file.write_text(text)
    return changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('category', choices=('spacing', 'font-size', 'line-height'))
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    edits, skipped = plan(args.category)
    total = apply(edits, args.dry_run)
    print(f'{args.category}: {total} declarations in {len(edits)} files' + (' (dry run)' if args.dry_run else ''))
    for row in skipped:
        print('SKIPPED', *row)
