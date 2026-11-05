"""Browser regression for three independent instances of each JS component."""
import tempfile
import unittest
from pathlib import Path
try:
    from tools.verify_command_context_date import run
except ImportError:
    run = None


@unittest.skipIf(run is None or not Path('/usr/bin/chromium').exists(), 'Playwright/Chromium unavailable')
class CommandContextDateInstances(unittest.TestCase):
    def test_keyboard_independence_and_zero_motion(self):
        with tempfile.TemporaryDirectory() as output:
            run(Path(output))
