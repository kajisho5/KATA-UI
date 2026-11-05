"""Do not mistake non-rendered form values for text or fake disabled classes for exemptions."""
import unittest
from pathlib import Path
try:
    from playwright.sync_api import sync_playwright
    from tools.capture_text_contrast import rows
except ImportError:
    sync_playwright=None


@unittest.skipIf(sync_playwright is None or not Path('/usr/bin/chromium').exists(),'Playwright/Pillow/Chromium unavailable')
class ContrastMetrics(unittest.TestCase):
    def test_only_painted_text_and_actual_disabled_controls(self):
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
            page=browser.new_page()
            page.set_content('<style>body{background:white;color:black}.hidden{opacity:0}</style><input type="checkbox"><input type="range" value="60"><input value="Visible"><label><input disabled value="Inactive">Inactive label</label><span class="disabled">Fake disabled</span><div class="hidden">Unpainted</div>')
            measured=rows(page);texts=[row['text'] for row in measured]
            self.assertNotIn('on',texts);self.assertNotIn('60',texts);self.assertNotIn('Unpainted',texts)
            self.assertIn('Visible',texts)
            self.assertTrue(next(row['disabled'] for row in measured if row['text']=='Inactive label'))
            self.assertFalse(next(row['disabled'] for row in measured if row['text']=='Fake disabled'))
            browser.close()
