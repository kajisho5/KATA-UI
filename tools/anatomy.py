"""Extract public selectors without treating comments/declaration strings as CSS."""
import re

def css_surface(css):
    clean = re.sub(r'/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', css, flags=re.S)
    selectors = '\n'.join(m[1] for m in re.finditer(r'([^{}]+)\{', clean))
    classes = list(dict.fromkeys(re.findall(r'\.([a-zA-Z][\w-]*)', selectors)))
    data = list(dict.fromkeys(re.findall(r'\[\s*(data-[\w-]+)', selectors)))
    return classes, data


def aria_surface(markup):
    from html.parser import HTMLParser
    class Attributes(HTMLParser):
        def __init__(self):
            super().__init__(); self.svg_depth = 0; self.names = []
        def handle_starttag(self, tag, attrs):
            if tag == 'svg': self.svg_depth += 1
            if not self.svg_depth:
                for name, _ in attrs:
                    if name.startswith('aria-') and name not in self.names: self.names.append(name)
        def handle_endtag(self, tag):
            if tag == 'svg': self.svg_depth = max(0, self.svg_depth - 1)
    parser = Attributes(); parser.feed(markup)
    return parser.names
