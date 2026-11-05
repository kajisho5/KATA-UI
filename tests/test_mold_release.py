"""Version requirements follow shared APIs, aliases and recursive dependencies, not file names."""
import json,tempfile,unittest,subprocess,shutil
from pathlib import Path
from tools.mold_release import requires_component,history,config,ROOT
from tools.mold_history import declarations

class MoldRelease(unittest.TestCase):
    def test_verified_versions_local_properties_and_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'system').mkdir();(root/'system/mold-history.json').write_text(json.dumps({'tokenVersions':{'--k-old':1,'--k-new':2,'--k-duration':1},'semanticVersions':{'--k-duration':2},'v1EvidenceVerified':True}))
            for name,css,meta in [('old','.old{--k-local:7px;color:var(--k-old);gap:var(--k-local)}',{}),('new','.new{color:var(--k-new)}',{}),('semantic','.x{transition:var(--k-duration)}',{}),('parent','.x{color:var(--k-old)}',{'deps':['new']})]:
                p=root/'components'/name;p.mkdir(parents=True);(p/'meta.json').write_text(json.dumps(meta));(p/(name+'.css')).write_text(css)
            self.assertEqual(requires_component('components','old',root),1)
            for name in ['new','semantic','parent']:self.assertEqual(requires_component('components',name,root),2)

    def test_unverified_v1_is_conservative(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'system').mkdir();(root/'system/mold-history.json').write_text(json.dumps({'tokenVersions':{'--k-old':1},'semanticVersions':{},'v1EvidenceVerified':False}));p=root/'components/plain';p.mkdir(parents=True);(p/'meta.json').write_text('{}');(p/'plain.css').write_text('.x{color:var(--k-old)}');self.assertEqual(requires_component('components','plain',root),2)

    def test_every_current_token_is_registered(self):
        self.assertLessEqual(set(declarations((ROOT/'tokens.css').read_text())),set(history(ROOT)['tokenVersions']))
        self.assertGreaterEqual(config(ROOT)['moldVersion'],2)

    @unittest.skipIf(shutil.which('node') is None,'Node unavailable')
    def test_mcp_initialization_and_component_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'registry.json';path.write_text(json.dumps({'moldVersion':2,'moldInstruction':'Check tokens.css before copying.','items':[{'name':'test','requiresMold':2,'files':[]}]}))
            requests=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{}},{'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'get_component','arguments':{'name':'test'}}}]
            result=subprocess.run(['node',str(ROOT/'mcp/kata-ui-mcp.mjs'),'--registry',str(path)],input='\n'.join(json.dumps(x) for x in requests)+'\n',text=True,capture_output=True,timeout=10,check=True)
            replies={x['id']:x for x in map(json.loads,result.stdout.splitlines())}
            self.assertEqual(replies[1]['result']['_meta']['kata-ui/moldVersion'],2)
            self.assertIn('Check tokens.css',replies[1]['result']['instructions'])
            part=json.loads(replies[2]['result']['content'][0]['text']);self.assertEqual(part['requiresMold'],2);self.assertEqual(part['moldVersion'],2)
