"""HTML audit views; all numeric facts come from a checker report."""
from collections import Counter
from html import escape
import json
from tools.mold_publish import label


def checks(item):
    sections=[]
    for status,title in [('pass','Passed'),('fail','Failed'),('warn','Warnings')]:
        matches=[c for c in item['checks'] if c['status']==status]
        entries=''.join('<li>'+escape(c['id'])+(f" ({len(c['findings'])})" if c['findings'] else '')+'</li>' for c in matches)
        sections.append('<details><summary>'+title+f' ({len(matches)})</summary><ul>'+entries+'</ul></details>')
    return '<section class="doc mold-checks"><h2>Static check results</h2><p>Profile: '+escape(item['profile'])+'. <a href="/audit/#'+escape(item['id'])+'">Full audit</a>.</p>'+''.join(sections)+'</section>'


def audit(report,root):
    rows=[]
    for item in report['items']:
        meta=json.loads((root/item['id']/'meta.json').read_text())
        failed=[c for c in item['checks'] if c['status']=='fail']
        problems=''.join('<details><summary>'+escape(c['id'])+f" ({len(c['findings'])})"+'</summary><ul>'+''.join('<li>'+escape(str(f))+'</li>' for f in c['findings'])+'</ul></details>' for c in failed)
        warns=sum(len(c['findings']) for c in item['checks'] if c['status']=='warn')
        rows.append('<tr id="'+escape(item['id'])+'"><th scope="row"><a href="/'+escape(item['id'])+'/">'+escape(meta['title'])+'</a><br><small>'+escape(item['id'])+'</small></th><td>'+escape(item['profile'])+'</td><td>'+escape(meta.get('status','unknown'))+'</td><td>'+('Pass' if item['passed'] else 'Fail')+'</td><td>'+(problems or 'None')+'</td><td>'+str(warns)+'</td></tr>')
    levels={c['id']:c['severity'] for item in report['items'] for c in item['checks']}
    remaining=''.join('<tr><th scope="row">'+escape(name)+'</th><td>'+escape(levels[name])+'</td><td>'+str(number)+'</td></tr>' for name,number in sorted(report['summary']['findings'].items()))
    kinds=Counter()
    for item in report['items']:kinds.update(next(c['by_kind'] for c in item['checks'] if c['id']=='token-values'))
    kind_rows=''.join('<tr><th scope="row">'+escape(k)+'</th><td>'+str(v)+'</td></tr>' for k,v in sorted(kinds.items()))
    style='<style>.audit-page{padding-block:var(--k-space-6);font-size:var(--k-text-base);line-height:var(--k-lh-body)}.audit-page h1{margin-block-end:var(--k-space-3)}.audit-page h2{margin-block-start:var(--k-space-6);margin-block-end:var(--k-space-2);font-size:var(--k-text-xl)}.audit-page p{margin-block-end:var(--k-space-3)}.audit-scroll{overflow:auto}.audit-table{width:100%;border-collapse:collapse}.audit-table th,.audit-table td{text-align:start;vertical-align:top;padding:var(--k-space-2);border-bottom:1px solid var(--k-line)}.audit-table td{overflow-wrap:anywhere}.audit-table ul{padding-inline-start:var(--k-space-4)}.audit-table small{white-space:nowrap}</style>'
    return style+'<main class="wrap dc audit-page"><h1>Audit</h1><p><a href="/audit/">'+escape(label(report))+'</a></p><p>Updated <time datetime="'+escape(report['updated_at'])+'">'+escape(report['updated_at'])+'</time> (Asia/Tokyo).</p><p>Static checks only. Test browser, keyboard, IME and screen-reader behavior separately. <a href="/mold-results.json">JSON</a> · <a href="/ROADMAP.md">Roadmap</a></p><h2>Remaining findings by check</h2><table class="audit-table"><thead><tr><th scope="col">Check</th><th scope="col">Level</th><th scope="col">Findings</th></tr></thead><tbody>'+remaining+'</tbody></table><h2>Token findings by kind</h2><table class="audit-table"><tbody>'+kind_rows+'</tbody></table><h2>Targets</h2><div class="audit-scroll"><table class="audit-table"><thead><tr><th scope="col">Name</th><th scope="col">Profile</th><th scope="col">Release status</th><th scope="col">Checks</th><th scope="col">Failed checks</th><th scope="col">Warning findings</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div></main>'
