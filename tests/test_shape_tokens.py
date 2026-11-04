"""Keep the canonical JSON and the committed runtime adapter in sync in CI."""
import unittest
from tools.sync_shape_tokens import sync


class ShapeAdapter(unittest.TestCase):
    def test_committed_adapter_matches_canonical_foundations(self):
        sync(check=True)
