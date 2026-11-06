"""Every Avatar sample is either decorative (aria-hidden) or a named image (role="img" + aria-label).

Initials next to a visible name were read twice ("AK Aoi Kimura"); a bare aria-label on a span is not
allowed by ARIA for generic elements, so a named avatar needs role="img".
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AVATAR = re.compile(r'<span class="k-avatar(?:s)?"[^>]*>')


class AvatarNames(unittest.TestCase):
    def test_samples_are_hidden_or_named_images(self):
        problems = []
        files = [*ROOT.glob('components/*/*.html'), *ROOT.glob('blocks/*/*.html'), *ROOT.glob('templates/*/*.html')]
        for path in files:
            text = path.read_text()
            for tag in AVATAR.findall(text):
                if 'class="k-avatars"' in tag:
                    if 'role="img"' in tag and 'aria-label=' not in tag:
                        problems.append(f'{path.relative_to(ROOT)}: {tag}')
                    continue
                named = 'role="img"' in tag and 'aria-label="' in tag
                hidden = 'aria-hidden="true"' in tag
                inside_named_stack = False
                if not (named or hidden):
                    # An avatar inside a stack that is itself a named image is presentational.
                    start = text.find(tag)
                    stack = text.rfind('<span class="k-avatars"', 0, start)
                    inside_named_stack = stack != -1 and 'role="img"' in text[stack:text.find('>', stack)] and text.find('</span>\n', stack) > start
                if not (named or hidden or inside_named_stack):
                    problems.append(f'{path.relative_to(ROOT)}: {tag}')
        self.assertEqual(problems, [])


if __name__ == '__main__':
    unittest.main()
