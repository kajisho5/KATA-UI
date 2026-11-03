"""Conservative static checks; runtime selector/cascade coverage is tested separately."""
import re
from html.parser import HTMLParser

class Markup(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.nodes = []; self.stack = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attrs': dict(attrs), 'parents': list(self.stack)}
        self.nodes.append(node)
        if tag not in ('input','img','br','hr','meta','link','source','area','wbr','embed'):
            self.stack.append(node)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i]['tag'] == tag:
                self.stack = self.stack[:i]; break

def strip_comments(css):
    return re.sub(r'/\*.*?\*/', '', css, flags=re.S)

def rules(css):
    # Flatten leaf declaration blocks, including rules inside media/keyframes.
    return [(m[1].strip(), m[2]) for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', strip_comments(css))]

def declarations(text):
    return re.findall(r'(?:^|;)\s*([\w-]+)\s*:\s*([^;]+)', text)

def inspect(directory, root, config):
    checks = []
    def record(name, issues, severity='error'):
        checks.append({'id': name, 'status': ('warn' if severity=='warning' else 'fail') if issues else 'pass', 'severity':severity, 'findings':issues})
    css_path = directory / (directory.name + '.css')
    css = css_path.read_text() if css_path.exists() else ''
    html_files = sorted(directory.glob('*.html'))
    docs = [(f, Markup(f.read_text())) for f in html_files]
    token_source = strip_comments((root / 'tokens.css').read_text()) if (root / 'tokens.css').exists() else ''
    prefixes = {directory.name}
    first = re.search(r'\.([a-zA-Z][\w-]*)\s*\{', strip_comments(css))
    if first: prefixes.add(re.sub(r'^k-', '', first[1]))
    forbidden = sorted({name for name in re.findall(r'(--k-[\w-]+)\s*:', token_source)
                        if any(name.startswith('--k-' + prefix + '-') for prefix in prefixes)})
    record('shared-token-scope', forbidden)
    raw = []
    def scan(text, path):
        for prop, value in declarations(text):
            if prop.startswith('--'): continue  # Component-root custom properties are local definitions.
            relevant = any(x in prop for x in ('radius','shadow','duration','color')) or prop in ('background','border','animation','transition','fill','stroke')
            if not relevant: continue
            # Ignore URL fragments and quoted strings, but retain var() fallbacks.
            clean = re.sub(r'url\([^)]*\)|["\'][^"\']*["\']', '', value)
            clean = re.sub(r'--[\w-]+', '', clean)
            bad = re.search(r'#[\da-fA-F]{3,8}\b|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch)\s*\(|(?<![\w-])(?:\d*\.)?\d+(?:px|rem|em|ms|s)\b', clean)
            # Named CSS colors also count, while semantic/currentColor keywords do not.
            named = re.search(r'\b(?:white|black|red|blue|green|gray|grey|yellow|orange|purple|pink|navy|teal|lime|aqua|fuchsia|silver|maroon|olive)\b', clean, re.I)
            if not (bad or named): continue
            if prop == 'border' and re.fullmatch(r'1px\s+solid\s+(?:transparent|currentColor|var\(--[\w-]+\))',value): continue
            allowed = any(a.get('path')==path and a.get('property')==prop and a.get('value')==value and a.get('reason') for a in config['raw_value_allowlist'])
            if not allowed: raw.append(f'{path}: {prop}: {value}')
    for _,body in rules(css): scan(body,str(css_path.relative_to(root)))
    for f,doc in docs:
        for embedded in re.findall(r'<style[^>]*>(.*?)</style>', f.read_text(), re.S | re.I):
            for _, body in rules(embedded): scan(body, str(f.relative_to(root)))
        for n in doc.nodes:
            if 'style' in n['attrs']:scan(n['attrs']['style'],str(f.relative_to(root)))
    record('token-values',raw)
    types=[];labels=[];focus=[]
    related_css=css
    for f,doc in docs:
        for n in doc.nodes:
            href=n['attrs'].get('href','') or ''
            if n['tag']=='link' and href.endswith('.css'):
                target=(root/href.lstrip('/')) if href.startswith('/') else (f.parent/href).resolve()
                if target.is_file() and target.is_relative_to(root):related_css+='\n'+target.read_text()
        ids={n['attrs']['id'] for n in doc.nodes if n['attrs'].get('id')}
        fors={n['attrs'].get('for') for n in doc.nodes if n['tag']=='label' and n['attrs'].get('for')}
        for n in doc.nodes:
            a=n['attrs'];tag=n['tag'];identity=f'{f.name}: <{tag}> '+str(a.get('class',a.get('id','')))
            if tag=='button' and not a.get('type'):types.append(identity)
            if tag in ('input','select','textarea') and a.get('type') not in ('hidden','button','submit','reset','image'):
                named=bool(a.get('aria-label','').strip()) or bool(a.get('aria-labelledby') and all(x in ids for x in a['aria-labelledby'].split()))
                if not (named or (a.get('id') and a.get('id') in fors) or any(p['tag']=='label' for p in n['parents'])):labels.append(identity)
            interactive=tag in ('button','input','select','textarea','summary') or (tag=='a' and 'href' in a) or 'tabindex' in a or a.get('role') in ('button','combobox','slider','switch','checkbox','radio','tab')
            if not interactive or a.get('type')=='hidden':continue
            classes=a.get('class','').split()
            candidates=[sel for sel,_ in rules(related_css) if ':focus-visible' in sel]
            # Require a relevant selector, not merely any focus rule in the file.
            if not any(any(re.search(r'\.'+re.escape(c)+r'(?![\w-])',sel) for c in classes) or re.search(r'(?<![\w.-])'+tag+r'(?=[:\s>+~.#\[])',sel) or '[tabindex]' in sel or ('[role='+str(a.get('role'))+']') in sel for sel in candidates):focus.append(identity)
    record('button-type',types);record('accessible-label',labels);record('focus-visible',focus)
    color_selectors=[]
    for selector,body in rules(css):
        if ':' in selector or '@' in selector:continue
        if not any(p in ('color','background','background-color') for p,_ in declarations(body)):continue
        for name in re.findall(r'\.([\w-]+)',selector):
            if name.startswith('btn-'):color_selectors.append(name)
    missing=[name for name in sorted(set(color_selectors)) if not any(':hover' in sel and re.search(r'\.'+re.escape(name)+r'(?![\w-])',sel) for sel,_ in rules(css))]
    record('variant-hover',missing)
    animated=any(p in ('animation','animation-name') and v not in ('none','initial','inherit') for _,body in rules(css) for p,v in declarations(body))
    record('reduced-motion',['Animation without a local reduced-motion rule'] if animated and not re.search(r'@media\s*\([^)]*prefers-reduced-motion\s*:\s*reduce',css) else [])
    js_path=directory/(directory.name+'.js');js=js_path.read_text() if js_path.exists() else ''
    record('js-single-instance',re.findall(r'document\s*\.\s*querySelector\s*\(\s*[\'\"]\[data-[^\'\"]+',js),'warning')
    # Lexical approximation: remove comments/strings before counting block depth.
    clean=re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`',lambda m:'\n'*m[0].count('\n'),js,flags=re.S)
    depth=0;warnings=[]
    for m in re.finditer(r'[{}]|\b(?:const|let)\s+([\w$]+)',clean):
        if m[0]=='{':depth+=1
        elif m[0]=='}':depth=max(0,depth-1)
        elif depth==0:warnings.append(m[0])
    record('js-global-bindings',warnings,'warning')
    return checks
