"""Real DOM checks for independent Pricing, Site Header and Use Cases blocks."""
import tempfile
import unittest
from pathlib import Path
try:
    from tools.verify_blocks_instances import run
except ImportError:
    run=None


@unittest.skipIf(run is None or not Path('/usr/bin/chromium').exists(),'Playwright/Chromium unavailable')
class BlocksInstances(unittest.TestCase):
    def test_three_instances_keyboard_and_dismissal(self):
        with tempfile.TemporaryDirectory() as output:
            run(Path(output))
