"""Real DOM checks for independent split panels, re-ranking lists and follow frames."""
import tempfile
import unittest
from pathlib import Path
try:
    from tools.verify_split_reorder_follow import run
except ImportError:
    run=None


@unittest.skipIf(run is None or not Path('/usr/bin/chromium').exists(),'Playwright/Chromium unavailable')
class SplitReorderFollow(unittest.TestCase):
    def test_three_instances_keyboard_and_motion(self):
        with tempfile.TemporaryDirectory() as output:
            run(Path(output))
