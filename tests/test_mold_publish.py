import copy
import json
from pathlib import Path
import tempfile
import unittest
from tools.mold_publish import label,metadata,region,sync
from tools.verify_template import verify

ROOT=Path(__file__).resolve().parents[1]

class PublishTests(unittest.TestCase):
    def test_counts_follow_report(self):
        report=json.loads((ROOT/'mold-results.json').read_text())
        report=copy.deepcopy(report);report['summary']['passed']=2
        report['summary']['by_profile']['ui']['passed']=1;report['summary']['by_profile']['lab']['passed']=1
        self.assertTrue(label(report).startswith('Mold Verified 2 / '))
        self.assertEqual(metadata(report)['summary'],report['summary'])
    def test_missing_region_fails(self):
        with self.assertRaises(ValueError):region('manual content','mold-summary','new')
    def test_region_preserves_manual_content(self):
        old='before\n<!-- a:start -->old<!-- a:end -->\nafter'
        self.assertEqual(region(old,'a','new'),'before\n<!-- a:start -->\nnew\n<!-- a:end -->\nafter')
    def test_template_is_ui_with_no_warnings_and_removed(self):
        before=set((ROOT/'components').iterdir());report=verify()
        self.assertEqual(report['summary']['passed'],1)
        self.assertEqual(report['summary']['warnings'],0)
        self.assertEqual(report['items'][0]['profile'],'ui')
        self.assertEqual(before,set((ROOT/'components').iterdir()))
