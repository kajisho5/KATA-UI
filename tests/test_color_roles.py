"""Shared role regressions: foreground/surface separation and adaptive custom accents."""
import json
import unittest
from pathlib import Path
from tools.color_roles import contrast,on_accent,accent_ink,theme_css
ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'system/tokens.json').read_text())['contrast']
try:
    from playwright.sync_api import sync_playwright
    from tools.capture_text_contrast import rows
except ImportError:
    sync_playwright=None


class StaticRoles(unittest.TestCase):
    def test_custom_palette_aa_and_switch(self):
        for accent in ('#1f3a5f','#ffd166','#33a6b8','#ff0000','#777777'):
            with self.subTest(accent=accent):
                self.assertGreaterEqual(contrast(on_accent(accent,CONFIG),accent),4.5)
                for mode in ('light','dark'):
                    for bg in CONFIG['backgrounds'][mode]:self.assertGreaterEqual(contrast(accent_ink(accent,mode,CONFIG),bg),4.5)
        self.assertEqual(on_accent('#1f3a5f',CONFIG),'#ffffff')
        self.assertEqual(on_accent('#ffd166',CONFIG),'#18181b')

    def test_danger_on_both_surfaces(self):
        tokens=json.loads((ROOT/'system/tokens.json').read_text())
        for mode in ('light','dark'):
            for bg in CONFIG['backgrounds'][mode]:self.assertGreaterEqual(contrast(tokens['semanticColors'][mode]['--k-danger-ink'],bg),4.5)


@unittest.skipIf(sync_playwright is None or not Path('/usr/bin/chromium').exists(),'Playwright/Chromium unavailable')
class RenderedRoles(unittest.TestCase):
    def test_manual_css_and_static_export_without_relative_support(self):
        css=(ROOT/'tokens.css').read_text();buttons=(ROOT/'components/button/button.css').read_text()
        begin=css.index('/* relative-color-roles:start */');end=css.index('/* relative-color-roles:end */')+len('/* relative-color-roles:end */')
        fallback=css[:begin]+css[end:]
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            page=browser.new_page()
            for mode in ('light','dark'):
                for accent in ('#1f3a5f','#ffd166','#33a6b8','#777777','#ff0000'):
                    for base in (css,fallback+theme_css(accent,CONFIG)):
                        page.set_content('<html data-theme="'+mode+'"><style>'+base+buttons+' *{transition:none!important;animation:none!important}</style><button type="button" class="btn btn-accent">Accent</button>')
                        page.evaluate('(color)=>document.documentElement.style.setProperty("--k-accent",color)',accent)
                        self.assertGreaterEqual(rows(page)[0]['ratio'],4.5,(mode,accent))
                        page.locator('button').hover()
                        self.assertGreaterEqual(rows(page)[0]['ratio'],4.5,(mode,accent,'hover'))
            browser.close()
