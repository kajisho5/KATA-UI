"""Real DOM regression for independent overlays, native focus and cancelled exit events."""
import tempfile,unittest
from pathlib import Path
try:
    from tools.verify_overlay_instances import run
except ImportError:
    run=None


@unittest.skipIf(run is None or not Path('/usr/bin/chromium').exists(),'Playwright/Chromium unavailable')
class OverlayInstances(unittest.TestCase):
    def test_multi_instance_keyboard_and_zero_motion(self):
        with tempfile.TemporaryDirectory() as output:run(Path(output))
