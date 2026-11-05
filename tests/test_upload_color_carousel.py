"""Real DOM checks for independent file uploads, color pickers and carousels."""
import tempfile
import unittest
from pathlib import Path
try:
    from tools.verify_upload_color_carousel import run
except ImportError:
    run=None


@unittest.skipIf(run is None or not Path('/usr/bin/chromium').exists(),'Playwright/Chromium unavailable')
class UploadColorCarousel(unittest.TestCase):
    def test_three_instances_keyboard_and_motion(self):
        with tempfile.TemporaryDirectory() as output:
            run(Path(output))
