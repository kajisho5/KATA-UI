import copy
import contextlib
import io
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from tools import mold_ratchet
import unittest
from tools.mold_ratchet import compare,snapshot


def report(passes):
    items=[{'id':name,'profile':'ui','passed':passed,'checks':[{'status':'pass' if passed else 'fail'}]} for name,passed in passes.items()]
    return {'summary':{'passed':sum(passes.values()),'total':len(items)},'items':items}

class RatchetTests(unittest.TestCase):
    def test_equal(self):
        current=report({'a':True,'b':False});self.assertEqual(compare(current,snapshot(current)),([],False))
    def test_count_decrease(self):
        self.assertTrue(compare(report({'a':False}),snapshot(report({'a':True})))[0])
    def test_swapped_pass_is_regression(self):
        self.assertTrue(compare(report({'a':False,'b':True}),snapshot(report({'a':True,'b':False})))[0])
    def test_missing_pass_is_regression(self):
        self.assertTrue(compare(report({'b':True}),snapshot(report({'a':True,'b':False})))[0])
    def test_improvement_requests_update(self):
        self.assertEqual(compare(report({'a':True,'b':True}),snapshot(report({'a':True,'b':False}))),([],True))
    def test_invalid_summary_rejected(self):
        current=report({'a':True});current['summary']['passed']=0
        with self.assertRaises(ValueError):snapshot(current)

    def test_trusted_baseline_blocks_candidate_downgrade(self):
        current=report({'a':False,'b':True})
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'report.json').write_text(json.dumps(current));(root/'base.json').write_text(json.dumps(snapshot(current)))
            args=['ratchet','--report',str(root/'report.json'),'--baseline',str(root/'base.json'),'--reference-ref','a'*40]
            with patch('sys.argv',args),patch.object(mold_ratchet,'trusted_baseline',return_value=snapshot(report({'a':True,'b':False}))),contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(mold_ratchet.main(),1)

    def test_cli_improvement_notice(self):
        current=report({'a':True,'b':True})
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'report.json').write_text(json.dumps(current));(root/'base.json').write_text(json.dumps(snapshot(report({'a':True,'b':False}))))
            args=['ratchet','--report',str(root/'report.json'),'--baseline',str(root/'base.json')]
            with patch('sys.argv',args),contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(mold_ratchet.main(),0)
            self.assertIn('mold-baseline.json を更新してください',output.getvalue())
