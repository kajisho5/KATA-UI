"""Every install command names the package in cli/package.json, and the stated Node version matches its engines field.

The npm migration plan (docs/npm-migration.md) changes the package name in one place;
this test then lists every command that still names the old package.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = json.loads((ROOT / 'cli' / 'package.json').read_text(encoding='utf-8'))
NAME = PACKAGE['name']
NODE = re.fullmatch(r'>=\s*(\d+)', PACKAGE['engines']['node']).group(1)
# Current-state sources: site generator, READMEs, the AI Skill and the publish workflow.
SOURCES = ['build.py', 'README.md', 'cli/README.md', 'skill/SKILL.md', '.github/workflows/publish-npm.yml']


PATTERNS = [(r'\bnpx\s+(@?[\w.-]+(?:/[\w.-]+)?)', 'npx '),
            (r'npmjs\.com/package/(@?[\w.-]+(?:/[\w.-]+)?)', 'npmjs.com/package/'),
            (r'npm view "(@?[\w.-]+(?:/[\w.-]+)?)@', 'npm view ')]


def other_names(text, name=NAME):
    """Package references in text that name a package other than `name`."""
    return [prefix + found for pattern, prefix in PATTERNS for found in re.findall(pattern, text) if found != name]


class CliPackageName(unittest.TestCase):
    def test_install_commands_use_the_package_name(self):
        wrong = [(rel, ref) for rel in SOURCES for ref in other_names((ROOT / rel).read_text(encoding='utf-8'))]
        self.assertEqual(wrong, [])
        self.assertIn('npx ' + NAME, (ROOT / 'build.py').read_text(encoding='utf-8'))

    def test_detector_flags_a_renamed_package(self):
        text = 'npx @kata-ui/cli add button; see npmjs.com/package/kata-ui; npm view "@kata-ui/cli@1.2.0" version'
        self.assertEqual(other_names(text, '@kata-ui/cli'), ['npmjs.com/package/kata-ui'])
        self.assertEqual(len(other_names(text, '@kajisho5/kataui')), 3)

    def test_stated_node_version_matches_engines(self):
        stated = [(rel, n) for rel in SOURCES
                  for n in re.findall(r'\bNode\s+(\d+)\+', (ROOT / rel).read_text(encoding='utf-8'))]
        self.assertTrue(stated)
        self.assertEqual([s for s in stated if s[1] != NODE], [])


if __name__ == '__main__':
    unittest.main()
