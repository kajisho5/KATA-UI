"""Create one temporary catalog target, check it, and always remove it."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]


def verify(root=ROOT):
    with tempfile.TemporaryDirectory(prefix='mold-template-',dir=root/'components') as temp:
        target=Path(temp);slug=target.name
        shutil.copytree(root/'template',target,dirs_exist_ok=True)
        for extension in ('css','js'):
            source=target/('template.'+extension)
            if source.exists():source.rename(target/(slug+'.'+extension))
        result=target/'check-result.json'
        check=subprocess.run([sys.executable,'-W','error::SyntaxWarning',str(root/'check.py'),slug,'--json',str(result)],cwd=root,text=True,capture_output=True)
        if check.returncode:raise RuntimeError(check.stdout+check.stderr)
        report=json.loads(result.read_text())
        if report['summary']['total']!=1 or report['items'][0]['profile']!='ui' or any(c['status']!='pass' for c in report['items'][0]['checks']):raise RuntimeError('Template has non-passing checks')
    if target.exists():raise RuntimeError('Temporary target was not removed')
    return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--json');args=parser.parse_args()
    try:report=verify()
    except (OSError,ValueError,RuntimeError) as error:print(error,file=sys.stderr);return 1
    if args.json:Path(args.json).write_text(json.dumps(report,indent=2)+'\n')
    print('Template probe: 1 / 1; profile ui; all checks pass; 0 warnings; temporary target removed')
    return 0

if __name__=='__main__':sys.exit(main())
