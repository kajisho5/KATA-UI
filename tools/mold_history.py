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

def generate(ref):
    commits=git('log','--reverse','--format=%H',ref,'--','tokens.css').splitlines();previous={};events=[];introduced={};baseline={}
    for sha in commits:
        raw=git('show',sha+':tokens.css');current=declarations(raw)
        for name in current:introduced.setdefault(name,sha)
        changes=[{'token':name,'before':previous.get(name,[]),'after':current.get(name,[]),'kind':'added' if name not in previous else 'removed' if name not in current else 'value'} for name in sorted(set(previous)|set(current)) if previous.get(name)!=current.get(name)]
        if changes:events.append({'commit':sha,'date':git('show','-s','--format=%cs',sha),'subject':git('show','-s','--format=%s',sha),'changes':changes})
        if not baseline:baseline=current.copy()
        previous=current
    versions={name:(1 if name in baseline else 2) for name in previous};versions['--k-mold']=2
    audits=[]
    for sha in git('log','--first-parent','--reverse','--format=%H',ref).splitlines():
        result=subprocess.run(['git','show',sha+':mold-results.json'],cwd=ROOT,text=True,capture_output=True)
        if result.returncode:continue
        summary=json.loads(result.stdout).get('summary',{})
        if 'passed' in summary and (not audits or audits[-1]['passed']!=summary['passed']):audits.append({'commit':sha,'passed':summary['passed'],'total':summary['total']})
    return {'auditMilestones':audits,'schemaVersion':1,'throughCommit':git('rev-parse',ref),'baselineCommit':commits[0],
      'evidenceGap':'The owner identifies the 2026-11-01 release as v1. Git has no November 1 source snapshot; its earliest tokens.css is November 2. The earliest surviving snapshot is the conservative v1 evidence baseline, not a verified copy of the November 1 publication. Later additions require v2.',
      'v1EvidenceVerified':False,'v1':baseline,'v2':previous,'introduced':introduced,'tokenVersions':versions,
      'semanticVersions':{'--k-dur-1':2,'--k-dur-2':2,'--k-dur-3':2,'--k-mscale':2},
      'semanticChanges':[
        {'tokens':['--k-dur-1','--k-dur-2','--k-dur-3'],'commit':git('rev-parse','fd010dc'),'reason':'Numbered durations now alias scaled fast/base/slow values. Remove an extra multiplier at call sites.'},
        {'tokens':['--k-mscale'],'commit':git('rev-parse','fd010dc'),'reason':'The external multiplier now has a shared default of 1; reduced motion sets it to zero. Scoped loop ownership was included in the merged PR.'}],
      'deprecations':[
        {'name':'.btn-asagi','replacement':'.btn-accent (deprecated alias retained)','commit':git('rev-parse','6f06c46')},
        {'name':'--k-ease-out','replacement':'--k-ease-in-out (deprecated alias retained)','commit':git('rev-parse','fd010dc')}],
      'events':events}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--ref',default='HEAD');a=p.parse_args();(ROOT/'system/mold-history.json').write_text(json.dumps(generate(a.ref),indent=2,ensure_ascii=False)+'\n')
