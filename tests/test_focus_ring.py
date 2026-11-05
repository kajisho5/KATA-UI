"""Fixtures for the focus-ring measurement: none, weak, visible and clipped."""
import unittest
from pathlib import Path
try:
    from playwright.sync_api import sync_playwright
    from tools.verify_focus_ring import load, measure, page_html
except ImportError:
    sync_playwright=None

CASES = {
    # outline removed with no replacement: nothing changes on focus
    'none': '<button type="button" class="t" style="outline:none">A</button>',
    # the current shared --k-ring value: 12% black, below 3:1 on white
    'weak': '<button type="button" class="t" style="outline:none" onfocus="this.style.boxShadow=\'0 0 0 3px rgba(24,24,27,.12)\'" onblur="this.style.boxShadow=\'\'">A</button>',
    'visible': '<button type="button" class="t" style="outline:none" onfocus="this.style.boxShadow=\'0 0 0 3px #18181b\'" onblur="this.style.boxShadow=\'\'">A</button>',
}
# A visually hidden radio shows focus on its label, as Rating does.
LABELLED = '<input type="radio" id="r" name="r" style="position:absolute;width:1px;height:1px;opacity:0"><label for="r" class="t">Star</label><style>#r:focus-visible+label{outline:2px solid #18181b;outline-offset:2px}</style>'
CLIPPED = '<div style="overflow:hidden;display:inline-block"><button type="button" style="outline:none;display:block" onfocus="this.style.boxShadow=\'0 0 0 3px #18181b\'" onblur="this.style.boxShadow=\'\'">A</button></div>'
HEAD = '<style>:root{--k-bg:#fff;--k-ink:#18181b;--k-font:sans-serif;--k-space-6:24px}.t{padding:8px 16px;border:1px solid #ccc;background:#fff}</style>'


@unittest.skipIf(sync_playwright is None or not Path('/usr/bin/chromium').exists(),'Playwright/Chromium unavailable')
class FocusRing(unittest.TestCase):
    def test_levels_and_clipping(self):
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            page=browser.new_page(viewport={'width':800,'height':600})
            for level,html in CASES.items():
                load(page,page_html(HEAD,html));records=measure(page,'light')
                self.assertEqual([r['level'] for r in records],[level],(level,records))
                self.assertIsNone(records[0]['clipped'])
            load(page,page_html(HEAD,LABELLED));records=measure(page,'light')
            self.assertEqual((records[0]['level'],records[0].get('measured')),('visible','label'),records)
            load(page,page_html(HEAD,CLIPPED));records=measure(page,'light')
            self.assertEqual(records[0]['clipped']['cut'],3.0)
            browser.close()
