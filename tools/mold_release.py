"""Mold compatibility metadata, requirements and provenance-backed release notes."""
import html,json,re
from functools import lru_cache
from pathlib import Path
from tools.mold_history import declarations
ROOT=Path(__file__).resolve().parents[1]
INSTRUCTION='Before copying a part, check the tokens.css mold header against requiresMold; update the mold before using newer parts. Unversioned tokens.css is legacy v1.'


@lru_cache(maxsize=None)
def config(root=ROOT):return json.loads((root/'system/tokens.json').read_text())

@lru_cache(maxsize=None)
def history(root=ROOT):return json.loads((root/'system/mold-history.json').read_text())

def requires_component(kind,name,root=ROOT,seen=None):
    seen=set() if seen is None else seen;key=kind+'/'+name
    if key in seen:return 1
    seen.add(key);folder=root/kind/name
    if not (folder/'meta.json').exists():return 1
    meta=json.loads((folder/'meta.json').read_text());source='\n'.join(p.read_text() for p in folder.iterdir() if p.suffix in ('.css','.js','.html'))
    data=history(root);versions=data['tokenVersions'];semantics=data['semanticVersions']
    refs=set(re.findall(r'--k-[\w-]+',re.sub(r'/\*.*?\*/','',source,flags=re.S)))
    # Local component properties are not mold API. Registered shared properties determine compatibility.
    result=max([1]+[max(versions[token],semantics.get(token,1)) for token in refs if token in versions])
    if refs.intersection(versions) and not data.get('v1EvidenceVerified',False):result=max(result,2)
    deps=[('components',v) for field in ('deps','uses') for v in meta.get(field,[])]+[('blocks',v) for v in meta.get('blocks',[])]
    deps.extend((group,slug) for group,slug in re.findall(r'/(components|blocks|templates)/([\w-]+)/',source))
    for group,slug in deps:
        if not (root/group/slug/'meta.json').exists() and group=='components' and (root/'blocks'/slug/'meta.json').exists():group='blocks'
        result=max(result,requires_component(group,slug,root,seen))
    return result


def version_line(root=ROOT):return f"moldVersion: {config(root)['moldVersion']}. "+INSTRUCTION


def sync_docs(root=ROOT,check=False):
    metadata={'moldVersion':config(root)['moldVersion'],'instruction':INSTRUCTION,'changelog':'https://kata-ui.dev/docs/mold-changelog/'}
    target=root/'mcp/mold.json';text=json.dumps(metadata,indent=2)+'\n'
    if not target.exists() or target.read_text()!=text:
        if check:raise ValueError('Stale MCP mold metadata')
        target.write_text(text)
    for filename in ('README.md','skill/SKILL.md'):
        path=root/filename;old=path.read_text();block='<!-- mold-version:start -->\n'+version_line(root)+'\n<!-- mold-version:end -->'
        if '<!-- mold-version:start -->' in old:new=re.sub(r'<!-- mold-version:start -->.*?<!-- mold-version:end -->',lambda _:block,old,flags=re.S)
        else:
            match=re.search(r'^# .+$',old,re.M);new=old[:match.end()]+'\n\n'+block+old[match.end():]
        if old!=new:
            if check:raise ValueError('Stale mold metadata: '+filename)
            path.write_text(new)


def release_sections(root=ROOT):
    data=history(root);first=data['v1'];current=data['v2'];events=data['events']
    added=[(name,', '.join(current[name]),data['introduced'][name]) for name in sorted(current.keys()-first.keys())]
    values=[(c['token'],' | '.join(c['before']),' | '.join(c['after']),e['commit']) for e in events[1:] for c in e['changes'] if c['kind']=='value']
    removed=[(c['token'],' | '.join(c['before']),e['commit']) for e in events[1:] for c in e['changes'] if c['kind']=='removed']
    # List transient additions too; these include removed combo/toast mold properties.
    transient=[(c['token'],' | '.join(c['after']),e['commit']) for e in events[1:] for c in e['changes'] if c['kind']=='added' and c['token'] not in current]
    return [('Added tokens',('Token','Current values (theme/conditional alternatives)','First recorded commit'),added),
      ('Transient additions (subsequently removed)',('Token','Added value','Commit'),transient),
      ('Every recorded value change',('Token','Before','After','Commit'),values),
      ('Removed declarations',('Token','Removed values','Commit'),removed),
      ('Meaning changes',('Tokens','Reason','Commit'),[(', '.join(x['tokens']),x['reason'],x['commit']) for x in data['semanticChanges']]),
      ('Deprecated APIs',('Name','Replacement','Commit'),[(x['name'],x['replacement'],x['commit']) for x in data['deprecations']])]


def changelog_html(root=ROOT):
    data=history(root);out=['<section><h2>Mold v2 — 2026-11-05</h2><p>v1 is the owner-designated November 1 release. '+html.escape(data['evidenceGap'])+'</p><p>Values below include light, dark and conditional alternatives. Each change is linked to the recorded commit. Local component properties are not removed APIs; combo/toast values moved to component roots. The v1 compatibility map uses the earliest surviving snapshot; later additions require v2. Since the November 1 snapshot is unavailable, shared-token users conservatively require v2 until v1 evidence can be verified. Changes of meaning can also raise a requirement.</p><p><a href="/docs/update-mold/">Update your tokens.css</a></p></section>']
    for title,headers,rows in release_sections(root):
        out.append('<section><h2>'+title+'</h2><table><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>')
        for row in rows:
            out.append('<tr>'+''.join('<td><code>'+html.escape(str(cell))+'</code></td>' if n<len(row)-1 else f'<td><a href="https://github.com/kajisho5/KATA-UI/commit/{cell}">{str(cell)[:7]}</a></td>' for n,cell in enumerate(row))+'</tr>')
        out.append('</tbody></table></section>')
    return ''.join(out)
