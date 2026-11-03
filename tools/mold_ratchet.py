"""Compare complete checker JSON against committed and trusted base snapshots."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


def validate(snapshot, baseline=False):
    items=snapshot['items'];seen=set()
    if type(snapshot['summary']['passed']) is not int or type(snapshot['summary']['total']) is not int:raise ValueError('Summary counts must be integers')
    for item in items:
        if item['id'] in seen:raise ValueError('Duplicate target: '+item['id'])
        seen.add(item['id'])
        if type(item['passed']) is not bool:raise ValueError('passed must be boolean')
        if item['profile'] not in ('ui','lab'):raise ValueError('Unknown profile')
    passed=sum(i['passed'] for i in items)
    if snapshot['summary']['passed']!=passed or snapshot['summary']['total']!=len(items):raise ValueError('Summary does not match targets')
    if not baseline:
        for item in items:
            if item['passed'] != (not any(c['status']=='fail' for c in item['checks'])):raise ValueError('Verdict does not match checks')
    return {i['id']:i for i in items}


def snapshot(report):
    validate(report)
    return {'schema_version':1,'summary':{'passed':report['summary']['passed'],'total':report['summary']['total']},
            'items':[{'id':i['id'],'passed':i['passed'],'profile':i['profile']} for i in report['items']]}


def compare(report, baseline):
    current=validate(report);previous=validate(baseline,True);errors=[]
    if report['summary']['passed']<baseline['summary']['passed']:errors.append('Passing count decreased')
    for name,item in previous.items():
        if item['passed'] and (name not in current or not current[name]['passed']):errors.append('Previously passing target regressed: '+name)
    return errors,report['summary']['passed']>baseline['summary']['passed']


def trusted_baseline(root, ref):
    if not ref or not ref.strip('0'):return None
    if not re.fullmatch(r'[a-fA-F0-9]{40,64}',ref):raise ValueError('Reference must be a full commit SHA')
    subprocess.run(['git','cat-file','-e',ref+'^{commit}'],cwd=root,check=True,capture_output=True)
    file=subprocess.run(['git','show',ref+':mold-baseline.json'],cwd=root,text=True,capture_output=True)
    if file.returncode:
        tree=subprocess.run(['git','ls-tree','--name-only',ref,'mold-baseline.json'],cwd=root,text=True,capture_output=True,check=True)
        if not tree.stdout.strip():return None  # First introduction of the baseline.
        raise ValueError('Cannot read trusted baseline')
    return json.loads(file.stdout)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--report',required=True)
    parser.add_argument('--baseline',default='mold-baseline.json')
    parser.add_argument('--reference-ref')
    args=parser.parse_args()
    try:
        report=json.loads(Path(args.report).read_text());base=json.loads(Path(args.baseline).read_text())
        references=[('committed baseline',base)]
        trusted=trusted_baseline(Path.cwd(),args.reference_ref)
        if trusted is not None:references.append(('trusted base commit',trusted))
        errors=[];improved=False
        for label,baseline in references:
            found,gain=compare(report,baseline);errors += [label+': '+f for f in found];improved |= gain
        if errors:
            print('\n'.join(errors),file=sys.stderr);return 1
        print(f"Ratchet passed: {report['summary']['passed']} / {report['summary']['total']}")
        if improved:print('mold-baseline.json を更新してください')
        return 0
    except (KeyError,ValueError,OSError,subprocess.SubprocessError) as error:
        print('Ratchet input error: '+str(error),file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
