"""Extract public selectors without treating comments/declaration strings as CSS."""
import re

def css_surface(css):
    clean = re.sub(r'/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', css, flags=re.S)
    selectors = '\n'.join(m[1] for m in re.finditer(r'([^{}]+)\{', clean))
    classes = list(dict.fromkeys(re.findall(r'\.([a-zA-Z][\w-]*)', selectors)))
    data = list(dict.fromkeys(re.findall(r'\[\s*(data-[\w-]+)', selectors)))
    return classes, data
