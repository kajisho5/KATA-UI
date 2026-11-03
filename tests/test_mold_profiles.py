"""Policy fixtures exercise the real checker using isolated temporary repositories."""
import json
from pathlib import Path
import tempfile
import unittest
from tools.mold_rules import inspect

ROOT = Path(__file__).resolve().parents[1]

class ProfileFixtures(unittest.TestCase):
    def test_cases(self):
        config=json.loads((ROOT/'check.config.json').read_text())
        for case in json.loads((ROOT/'tests/mold/cases.json').read_text()):
            with self.subTest(case=case['name']), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);slug=case.get('slug','sample');d=root/'components'/slug;d.mkdir(parents=True)
                (root/'tokens.css').write_text((ROOT/'tokens.css').read_text()+case.get('shared_extra',''))
                meta={'category':case['category']}
                if 'prefix' in case:meta['prefix']=case['prefix']
                (d/'meta.json').write_text(json.dumps(meta))
                (d/(slug+'.css')).write_text(case['css'])
                (d/(slug+'.js')).write_text(case.get('js',''))
                (d/'preview.html').write_text(case.get('html',''))
                result={check['id']:check for check in inspect(d,root,config)}
                for name,status in case['expected'].items():self.assertEqual(result[name]['status'],status,result[name])
                if 'expected_kinds' in case:self.assertEqual(sorted(result['token-values']['by_kind']),case['expected_kinds'])
                self.assertEqual(result['token-values']['profile'],'lab' if case['category'] in ('Motion','KATAYABURI') else 'ui')
