"""Render audit facts from mold-results.json into tracked documentation."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]


def label(report):
    summary=report['summary'];profiles=summary['by_profile']
    return (f"Mold Verified {summary['passed']} / {summary['total']}"
            f" · UI {profiles['ui']['passed']} / {profiles['ui']['total']}"
            f" · Lab {profiles['lab']['passed']} / {profiles['lab']['total']}")


def metadata(report):
    return {'label':label(report),'url':'https://kata-ui.dev/audit/','updated_at':report['updated_at'],'summary':report['summary']}


def summary_block(report):
    return (f"[{label(report)}](https://kata-ui.dev/audit/)\n\n"
            f"{report['summary']['total']} parts. Static checks only. Updated {report['updated_at']} (Asia/Tokyo).\n"
            "Read the audit for each part's pass, fail and warning results. Browser behavior needs separate testing.")


def roadmap_block(report):
    kinds=Counter()
    for item in report['items']:
        kinds.update(next(c['by_kind'] for c in item['checks'] if c['id']=='token-values'))
    out=[summary_block(report),'','| Remaining check findings | Count |','|---|---:|']
    for kind in ('radius','duration','shadow','border','color','easing'):out.append(f'| token-values: {kind} | {kinds[kind]} |')
    for key in ('spacing-values','type-values'):out.append(f"| {key} (warn) | {report['summary']['findings'][key]} |")
    for key in ('focus-visible','js-single-instance','js-global-bindings','shared-token-scope','accessible-label'):
        out.append(f"| {key} | {report['summary']['findings'][key]} |")
    return '\n'.join(out)


def region(text,name,content):
    start=f'<!-- {name}:start -->';end=f'<!-- {name}:end -->'
    if start not in text or end not in text:raise ValueError('Missing generated region: '+name)
    return re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:start+'\n'+content+'\n'+end,text,flags=re.S)


def sync(root,report,check=False):
    updates={'README.md':('mold-summary',summary_block(report)),
             'skill/SKILL.md':('mold-summary',summary_block(report)),
             'docs/ROADMAP.md':('mold-snapshot',roadmap_block(report))}
    stale=[]
    for name,(marker,content) in updates.items():
        path=root/name;old=path.read_text();new=region(old,marker,content)
        if old!=new:
            if check:stale.append(name)
            else:path.write_text(new)
    if stale:raise ValueError('Stale generated audit facts: '+', '.join(stale))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--report',default=str(ROOT/'mold-results.json'));parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    try:sync(ROOT,json.loads(Path(args.report).read_text()),args.check)
    except (ValueError,OSError,KeyError) as error:print(error,file=sys.stderr);return 1
    return 0

if __name__=='__main__':sys.exit(main())
