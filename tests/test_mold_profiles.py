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
        for case in [case for path in sorted((ROOT/'tests/mold').glob('*.json')) for case in json.loads(path.read_text())]:
            with self.subTest(case=case['name']), tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);slug=case.get('slug','sample');d=root/'components'/slug;d.mkdir(parents=True)
                (root/'tokens.css').write_text((ROOT/'tokens.css').read_text()+case.get('shared_extra',''))
                meta={'category':case['category'],**case.get('meta',{})}
                if 'prefix' in case:meta['prefix']=case['prefix']
                (d/'meta.json').write_text(json.dumps(meta))
                (d/(slug+'.css')).write_text(case['css'])
                (d/(slug+'.js')).write_text(case.get('js',''))
                (d/'preview.html').write_text(case.get('html',''))
                for filename,content in case.get('files',{}).items():
                    target=root/filename;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content)
                result={check['id']:check for check in inspect(d,root,config)}
                if 'expected_focus_count' in case:self.assertEqual(len(result['focus-visible']['findings']),case['expected_focus_count'])
                if 'expected_focus_occurrences' in case:self.assertEqual(sorted(x['occurrences'] for x in result['focus-visible']['details']),case['expected_focus_occurrences'])
                if 'expected_legacy_hex' in case:
                    from tools.mold_data import mask_color_data
                    import re
                    text=''.join(mask_color_data(path.read_text(),path.name,config) for path in d.glob('*.html') if path.name in ('preview.html','examples.html'))
                    self.assertEqual(len(re.findall(r'#[0-9a-fA-F]{3,8}\b',text)),case['expected_legacy_hex'])
                for name,status in case['expected'].items():self.assertEqual(result[name]['status'],status,result[name])
                if 'expected_kinds' in case:self.assertEqual(sorted(result['token-values']['by_kind']),case['expected_kinds'])
                self.assertEqual(result['token-values']['profile'],'lab' if case['category'] in ('Motion','KATAYABURI') else 'ui')
