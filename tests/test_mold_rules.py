import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('mold_rules', ROOT/'tools/mold_rules.py')
rules = importlib.util.module_from_spec(spec); spec.loader.exec_module(rules)

class RulesTest(unittest.TestCase):
    def inspect(self, css, html, js=''):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); d=root/'components'/'sample'; d.mkdir(parents=True)
            (d/'sample.css').write_text(css); (d/'preview.html').write_text(html); (d/'sample.js').write_text(js)
            return {c['id']:c for c in rules.inspect(d,root,json.loads((ROOT/'check.config.json').read_text()))}
    def test_failures(self):
        r=self.inspect('.btn-red{color:red;border-radius:8px;box-shadow:0 1px 2px rgba(0,0,0,.2);transition:color .2s;animation:spin 1s}', '<button class="btn-red">Go</button><input>', "const x=document.querySelector('[data-one]');")
        for name in ('token-values','button-type','accessible-label','focus-visible','variant-hover','reduced-motion'):self.assertEqual(r[name]['status'],'fail',name)
        for name in ('js-single-instance','js-global-bindings'):self.assertEqual(r[name]['status'],'warn')
    def test_valid_and_aliases(self):
        r=self.inspect('.btn-accent,.btn-asagi{color:var(--k-ink);border:1px solid var(--k-line)}.btn-accent:hover,.btn-asagi:hover{color:var(--k-ink-2)}.btn:focus-visible,input:focus-visible{box-shadow:var(--k-ring)}', '<button type="button" class="btn btn-accent">Go</button><label for="name">Name</label><input id="name">', "(()=>{const x=1;})();")
        self.assertTrue(all(c['status']=='pass' for c in r.values()),r)
    def test_shared_token_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);d=root/'components'/'sample';d.mkdir(parents=True)
            (root/'tokens.css').write_text(':root{--k-sample-width:3px;--k-space-1:4px}')
            (d/'sample.css').write_text('.sample{--sample-width:3px;width:var(--sample-width)}')
            result={c['id']:c for c in rules.inspect(d,root,{'raw_value_allowlist':[]})}
            self.assertEqual(result['shared-token-scope']['status'],'fail')
            self.assertEqual(result['shared-token-scope']['findings'],['--k-sample-width'])
    def test_token_name_is_not_a_named_color(self):
        r=self.inspect('.a{color:var(--k-red)}','')
        self.assertEqual(r['token-values']['status'],'pass')
    def test_unrelated_focus_does_not_pass(self):
        r=self.inspect('.other:focus-visible{outline:none}', '<button type="button" class="target">Go</button>')
        self.assertEqual(r['focus-visible']['status'],'fail')
    def test_var_fallback_and_comments(self):
        r=self.inspect('/* color:red */ .a{color:var(--x,#fff)}','')
        self.assertEqual(len(r['token-values']['findings']),1)

if __name__=='__main__':unittest.main()
