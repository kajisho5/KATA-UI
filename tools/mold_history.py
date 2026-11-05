"""Freeze every recorded tokens.css declaration change; builds need no git history."""
import argparse,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()

def declarations(text):
    text=re.sub(r'/\*.*?\*/','',text,flags=re.S)
    result={}
    for name,value in re.findall(r'(--k-[\w-]+)\s*:\s*([^;{}]+)',text):
        value=re.sub(r'\s+',' ',value).strip()
        if value not in result.setdefault(name,[]):result[name].append(value)
    return result

# Newest first. The v2 notes stay in tools/mold_release.changelog_html.
RELEASES=[
    {'version':4,'date':'2026-11-06','summary':'Complete spacing, text and leading scales for T3. Added --k-space-px (1px), --k-space-0-5 (2px), --k-space-5 (20px), --k-space-7 (28px), --k-space-10 (40px), --k-text-md (14px) and --k-text-display (44px) from tokens.json, --k-text-lead (15px), --k-lh-tight (1), --k-lh-card (1.35) and --k-lh-small (1.6). The scales are now generated from system/tokens.json. No existing value changes; parts that use a new token require mold v4.'},
    {'version':3,'date':'2026-11-06','summary':'Focus visibility. --k-ring is a 2px page-colored gap plus a 2px ink ring, and the tokens.css focus floor is a 2px ink outline with a 2px offset; both replace sub-3:1 values (a 12% tint and the #33a6b8 accent, 2.88:1 on white). Parts that use --k-ring require mold v3. Measured with tools/verify_focus_ring.py.'},
]

def generate(ref):
    commits=git('log','--reverse','--format=%H',ref,'--','tokens.css').splitlines();previous={};events=[];introduced={};introduced_versions={};baseline={}
    for sha in commits:
        raw=git('show',sha+':tokens.css');current=declarations(raw)
        stamp=re.search(r'^/\* KATA mold v(\d+)',raw)
        for name in current:
            introduced.setdefault(name,sha)
            introduced_versions.setdefault(name,int(stamp[1]) if stamp else 1 if not previous else 2)
        changes=[{'token':name,'before':previous.get(name,[]),'after':current.get(name,[]),'kind':'added' if name not in previous else 'removed' if name not in current else 'value'} for name in sorted(set(previous)|set(current)) if previous.get(name)!=current.get(name)]
        if changes:events.append({'commit':sha,'date':git('show','-s','--format=%cs',sha),'subject':git('show','-s','--format=%s',sha),'changes':changes})
        if not baseline:baseline=current.copy()
        previous=current
    current_version=json.loads((ROOT/'system/tokens.json').read_text())['moldVersion']
    versions={name:introduced_versions[name] for name in previous};versions['--k-mold']=current_version
    def last_value_change(token):
        return next((e['commit'] for e in reversed(events) for c in e['changes'] if c['token']==token and c['kind']=='value'),None)
    ring_commit=last_value_change('--k-ring')
    audits=[]
    for sha in git('log','--first-parent','--reverse','--format=%H',ref).splitlines():
        result=subprocess.run(['git','show',sha+':mold-results.json'],cwd=ROOT,text=True,capture_output=True)
        if result.returncode:continue
        summary=json.loads(result.stdout).get('summary',{})
        if 'passed' in summary and (not audits or audits[-1]['passed']!=summary['passed']):audits.append({'commit':sha,'passed':summary['passed'],'total':summary['total']})
    return {'auditMilestones':audits,'schemaVersion':1,'throughCommit':git('rev-parse',ref),'baselineCommit':commits[0],
      'evidenceGap':'The owner identifies the 2026-11-01 release as v1. Git has no November 1 source snapshot; its earliest tokens.css is November 2. The earliest surviving snapshot is the conservative v1 evidence baseline, not a verified copy of the November 1 publication. Later additions require v2.',
      'v1EvidenceVerified':False,'v1':baseline,'v2':previous,'introduced':introduced,'tokenVersions':versions,
      'semanticVersions':{'--k-dur-1':2,'--k-dur-2':2,'--k-dur-3':2,'--k-mscale':2,**({'--k-ring':3} if ring_commit and current_version>=3 else {})},
      'semanticChanges':[
        {'tokens':['--k-dur-1','--k-dur-2','--k-dur-3'],'commit':git('rev-parse','fd010dc'),'reason':'Numbered durations now alias scaled fast/base/slow values. Remove an extra multiplier at call sites.'},
        {'tokens':['--k-mscale'],'commit':git('rev-parse','fd010dc'),'reason':'The external multiplier now has a shared default of 1; reduced motion sets it to zero. Scoped loop ownership was included in the merged PR.'}]
        +([{'tokens':['--k-ring'],'commit':ring_commit,'reason':'Keyboard focus ring changed from a 3px 12% tint (about 1.3:1 on white) to a 2px page-colored gap plus a 2px ink ring, which reaches 3:1 in both themes. It is now 4px wide instead of 3px; check rings inside overflow-clipped containers.'}] if ring_commit and current_version>=3 else []),
      'deprecations':[
        {'name':'.btn-asagi','replacement':'.btn-accent (deprecated alias retained)','commit':git('rev-parse','6f06c46')},
        {'name':'--k-ease-out','replacement':'--k-ease-in-out (deprecated alias retained)','commit':git('rev-parse','fd010dc')}],
      'releases':[r for r in RELEASES if r['version']<=current_version],
      'events':events}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--ref',default='HEAD');a=p.parse_args();(ROOT/'system/mold-history.json').write_text(json.dumps(generate(a.ref),indent=2,ensure_ascii=False)+'\n')
