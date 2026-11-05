"""Check the built compatibility surfaces without network access or git history."""
import json,re
from pathlib import Path
from tools.mold_release import config,requires_component,sync_docs
ROOT=Path(__file__).resolve().parents[1]


def verify(root=ROOT):
    dist=root/'dist';settings=config(root);version=settings['moldVersion'];registry=json.loads((dist/'registry.json').read_text())
    assert registry['moldVersion']==version
    header=f"/* KATA mold v{version} — {settings['moldDate']} — kata-ui.dev/docs/mold-changelog */"
    assert (dist/'tokens.css').read_text().splitlines()[0]==header
    assert f'--k-mold:{version};' in (dist/'tokens.css').read_text()
    count=0
    for item in registry['items']:
        kind={'registry:component':'components','registry:block':'blocks','registry:page':'templates'}.get(item['type'])
        if not kind:continue
        requirement=requires_component(kind,item['name'],root);assert item['requiresMold']==requirement,item['name'];count+=1
        for file in item['files']:
            if not file['path'].endswith(('.css','.js')):continue
            marker='requires mold >= '+str(requirement)
            assert marker in file['content'].splitlines()[0],file['path']
            assert marker in (dist/file['path']).read_text().splitlines()[0],file['path']
    for path in ['llms.txt','llms-full.txt','skill/SKILL.md']:
        assert f'moldVersion: {version}' in (dist/path).read_text(),path
        assert 'Before copying a part' in (dist/path).read_text(),path
    assert json.loads((dist/'mcp/mold.json').read_text())['moldVersion']==version
    for slug in ['mold-changelog','update-mold']:
        assert (dist/'docs'/slug/'index.html').is_file(),slug
    sync_docs(root,check=True)
    print(f'{count} part requirements/headers, mold v{version}, AI metadata and release/update pages agree')

if __name__=='__main__':verify()
