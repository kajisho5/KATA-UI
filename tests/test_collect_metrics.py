"""tools/collect_metrics.py builds a dated record from the two public APIs, and every stored month has the four metrics."""
import datetime as dt
import json
import unittest
from pathlib import Path
from unittest import mock

from tools import collect_metrics as cm

ROOT = Path(__file__).resolve().parents[1]


def fake_fetch(url):
    if url.startswith('https://api.github.com/'):
        return {'stargazers_count': 12, 'forks_count': 3}
    if url.startswith('https://api.npmjs.org/downloads/range/'):
        return {'start': '2026-10-01', 'end': '2026-10-31', 'downloads': [{'downloads': 5}, {'downloads': 7}]}
    raise AssertionError(url)


class CollectMetrics(unittest.TestCase):
    def test_month_range_stops_at_today(self):
        self.assertEqual(cm.month_range('2026-11', dt.date(2026, 11, 12)), (dt.date(2026, 11, 1), dt.date(2026, 11, 12)))
        self.assertEqual(cm.month_range('2026-10', dt.date(2026, 11, 12)), (dt.date(2026, 10, 1), dt.date(2026, 10, 31)))
        self.assertEqual(cm.month_range('2028-02', dt.date(2028, 3, 1))[1], dt.date(2028, 2, 29))

    def test_record_shape_and_owner_fields(self):
        with mock.patch.object(cm, 'fetch', side_effect=fake_fetch) as fetch:
            record = cm.collect('2026-10', dt.date(2026, 11, 12))
        self.assertTrue(record['complete'])
        self.assertEqual(record['github']['stars'], 12)
        self.assertEqual({v['total'] for v in record['npm']['downloads'].values()}, {12})
        self.assertIn('https://api.npmjs.org/downloads/range/2026-10-01:2026-10-31/' + cm.PACKAGES[0],
                      [c.args[0] for c in fetch.call_args_list])
        self.assertIsNone(record['llmsTxt']['requests'])
        self.assertEqual(record['pro'], {'revenueUsd': None, 'state': 'not on sale'})
        with mock.patch.object(cm, 'fetch', side_effect=fake_fetch):
            partial = cm.collect('2026-11', dt.date(2026, 11, 12), llms=40, llms_source='owner, dashboard')
        self.assertFalse(partial['complete'])
        self.assertEqual(partial['llmsTxt'], {'requests': 40, 'source': 'owner, dashboard'})

    def test_stored_months_have_all_four_metrics(self):
        files = sorted((ROOT / 'docs' / 'metrics').glob('*.json'))
        self.assertTrue(files)
        for path in files:
            record = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(record['month'], path.stem)
            self.assertTrue({'github', 'npm', 'llmsTxt', 'pro'} <= set(record), path.name)
            self.assertIsInstance(record['github']['stars'], int)


if __name__ == '__main__':
    unittest.main()
