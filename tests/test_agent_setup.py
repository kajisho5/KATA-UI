"""Installation gating and failure tolerance without changing the host environment."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class AgentSetup(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        (self.root/'tools').mkdir();(self.root/'cli').mkdir();self.bin=self.root/'bin';self.bin.mkdir()
        shutil.copy(ROOT/'tools/agent-setup.sh',self.root/'tools/agent-setup.sh')
        (self.root/'tools/agent-requirements.txt').write_text('playwright\nPillow\n')
        (self.root/'cli/package.json').write_text('{"version":"1.0.0"}')
        self.log=self.root/'calls'
        self.env={**os.environ,'PATH':str(self.bin),'FAKE_ROOT':str(self.root),'LOG':str(self.log),'FAKE_UID':'1000','CLAUDE_CODE_REMOTE':'false','AGENT_SETUP':'0'}
        for name,source in [('bash','/bin/bash'),('dirname','/usr/bin/dirname')]:
            (self.bin/name).symlink_to(source)
        self.executable('id','printf "%s\\n" "$FAKE_UID"')
        self.executable('node','printf "node %s\\n" "$*" >> "$LOG"; exit 0')
        self.executable('npm','printf "npm %s\\n" "$*" >> "$LOG"; if [ "${FAKE_FAIL:-0}" = 1 ]; then exit 9; fi')
        self.executable('python3',r'''
printf 'python %s\n' "$*" >> "$LOG"
case "$*" in
  '-m venv '*) /usr/bin/mkdir -p "$3/bin"; /usr/bin/cp "$FAKE_ROOT/bin/python3" "$3/bin/python" ;;
  '-m pip install '*) if [ "${FAKE_FAIL:-0}" = 1 ]; then exit 9; fi; /usr/bin/touch "$FAKE_ROOT/deps" ;;
  '-m playwright install '*) if [ "${FAKE_FAIL:-0}" = 1 ]; then exit 9; fi; /usr/bin/touch "$FAKE_ROOT/browser" ;;
  *'assert Path(p.chromium.executable_path)'*) [ -f "$FAKE_ROOT/browser" ] ;;
  *'import playwright.sync_api'*) [ -f "$FAKE_ROOT/deps" ] ;;
  *) exit 0 ;;
esac
''')

    def executable(self,name,body):
        path=self.bin/name;path.write_text('#!/bin/bash\n'+body+'\n');path.chmod(0o755)

    def tearDown(self):self.temp.cleanup()

    def run_setup(self,**changes):
        result=subprocess.run(['/bin/bash',str(self.root/'tools/agent-setup.sh')],env={**self.env,**changes},text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        return result.stdout

    def calls(self):return self.log.read_text()

    def test_default_inspects_without_installing_or_creating_state(self):
        output=self.run_setup()
        self.assertIn('Inspection only',output)
        self.assertNotIn('-m pip install',self.calls());self.assertNotIn('-m playwright install',self.calls());self.assertNotIn('npm --cache',self.calls())
        self.assertFalse((self.root/'.agent').exists())

    def test_remote_nonroot_installs_once_then_reuses_dependencies(self):
        self.run_setup(CLAUDE_CODE_REMOTE='true');first=self.calls()
        self.assertIn('-m pip install',first);self.assertIn('-m playwright install chromium',first)
        self.assertNotIn('--with-deps',first)
        self.run_setup(CLAUDE_CODE_REMOTE='true');second=self.calls()
        self.assertEqual(second.count('-m pip install'),1);self.assertEqual(second.count('-m playwright install'),1)

    def test_root_optin_is_the_only_case_using_with_deps(self):
        self.run_setup(AGENT_SETUP='1',FAKE_UID='0')
        self.assertIn('-m playwright install --with-deps chromium',self.calls())

    def test_failed_installs_report_reasons_but_do_not_block_session(self):
        output=self.run_setup(AGENT_SETUP='1',FAKE_FAIL='1')
        self.assertIn('Python dependency install failed',output)
        self.assertIn('Chromium installation failed',output)
        self.assertIn('CLI npm dependency installation failed',output)
        self.assertIn('Agent setup completed',output)
