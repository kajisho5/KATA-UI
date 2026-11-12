"""Record the Phase 6 metrics for one month in docs/metrics/<YYYY-MM>.json.

Usage: python3 -m tools.collect_metrics [--month YYYY-MM]
       [--llms-requests N --llms-source TEXT] [--pro-revenue-usd N]

Collected automatically (public, unauthenticated APIs):
  GitHub stars and forks  https://api.github.com/repos/kajisho5/KATA-UI
  npm downloads           https://api.npmjs.org/downloads/range/<start>:<end>/<package>
                          for every package name in PACKAGES, over the calendar month
                          (to today while the month is still running)

Entered by the owner (no public API; null until given):
  llms.txt requests       Cloudflare dashboard request count for /llms.txt in the month,
                          with --llms-source naming the dashboard view used
  Pro revenue             --pro-revenue-usd; Pro is not on sale, so the file records
                          "not on sale" until a value is given

npm counts every tarball download, including CI, mirrors and bots; the number is a
download count, not a user count.
"""
import argparse
import calendar
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'kajisho5/KATA-UI'
PACKAGES = [json.loads((ROOT / 'cli' / 'package.json').read_text(encoding='utf-8'))['name']]


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'kata-ui-metrics', 'Accept': 'application/json'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))


def month_range(month, today):
    year, number = (int(x) for x in month.split('-'))
    start = dt.date(year, number, 1)
    end = dt.date(year, number, calendar.monthrange(year, number)[1])
    return start, min(end, today)


def collect(month, today, llms=None, llms_source=None, revenue=None):
    start, end = month_range(month, today)
    repo = fetch(f'https://api.github.com/repos/{REPO}')
    downloads = {}
    for name in PACKAGES:
        data = fetch(f'https://api.npmjs.org/downloads/range/{start}:{end}/{name}')
        downloads[name] = {'total': sum(d['downloads'] for d in data.get('downloads', [])),
                           'start': data.get('start'), 'end': data.get('end')}
    return {
        'month': month,
        'measured': today.isoformat(),
        'complete': end == month_range(month, dt.date.max)[1],
        'github': {'repo': REPO, 'stars': repo['stargazers_count'], 'forks': repo['forks_count'],
                   'source': f'https://api.github.com/repos/{REPO}'},
        'npm': {'downloads': downloads, 'source': 'https://api.npmjs.org/downloads/range/'},
        'llmsTxt': {'requests': llms, 'source': llms_source or 'owner: Cloudflare dashboard (not entered)'},
        'pro': {'revenueUsd': revenue, 'state': 'on sale' if revenue is not None else 'not on sale'},
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--month')
    parser.add_argument('--llms-requests', type=int)
    parser.add_argument('--llms-source')
    parser.add_argument('--pro-revenue-usd', type=float)
    args = parser.parse_args(argv)
    today = dt.date.today()
    month = args.month or today.strftime('%Y-%m')
    record = collect(month, today, args.llms_requests, args.llms_source, args.pro_revenue_usd)
    out = ROOT / 'docs' / 'metrics' / f'{month}.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(out.relative_to(ROOT), json.dumps({k: record[k] for k in ('github', 'npm')}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
