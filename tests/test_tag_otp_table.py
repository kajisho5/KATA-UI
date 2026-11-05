"""Real DOM checks for independent tags, OTP groups and data tables."""
import tempfile
import unittest
from pathlib import Path
try:
    from tools.verify_tag_otp_table import run
except ImportError:
    run=None


@unittest.skipIf(run is None or not Path('/usr/bin/chromium').exists(),'Playwright/Chromium unavailable')
class TagOtpTable(unittest.TestCase):
    def test_three_instances_keyboard_and_motion(self):
        with tempfile.TemporaryDirectory() as output:
            run(Path(output))
