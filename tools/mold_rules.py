"""Conservative static checks; runtime selector/cascade coverage is tested separately."""
import json, re
from html.parser import HTMLParser
from tools.token_values import Values, kinds_for

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
    meta_path = directory / 'meta.json'
    try:
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}
    except (ValueError, OSError):
        meta = {}  # The existing metadata contract reports malformed metadata.
    profile = 'lab' if meta.get('category') in config['lab_categories'] else 'ui'
    prefixes = {directory.name}
    if meta.get('prefix'):
        if isinstance(meta['prefix'], str):
            prefixes.add(meta['prefix'].removeprefix('--').removeprefix('k-').strip('-'))
    forbidden = sorted({name for name in re.findall(r'(--k-[\w-]+)\s*:', token_source)
                        if any(name.startswith('--k-' + prefix + '-') for prefix in prefixes if prefix)})
    record('shared-token-scope', forbidden)
    shared = set(re.findall(r'(--[\w-]+)\s*:', token_source))
    sources = [(str(css_path.relative_to(root)), declarations(body)) for _, body in rules(css)]
    dependency_css = []
    for f, doc in docs:
        for embedded in re.findall(r'<style[^>]*>(.*?)</style>', f.read_text(), re.S | re.I):
            sources.extend((str(f.relative_to(root)), declarations(body)) for _, body in rules(embedded))
        for node in doc.nodes:
            attrs = node['attrs']
            if 'style' in attrs: sources.append((str(f.relative_to(root)), declarations(attrs['style'])))
            href = attrs.get('href') or ''
            if node['tag'] == 'link' and href.endswith('.css'):
                target = root / href.lstrip('/') if href.startswith('/') else (f.parent / href).resolve()
                if target.is_file() and target.is_relative_to(root):dependency_css.append(target.read_text())
    local = {}
    for _, decls in sources:
        for prop, value in decls:
            if prop.startswith('--'):local.setdefault(prop, []).append(value)
    for dep in dependency_css:
        for _, body in rules(dep):
            for prop, value in declarations(body):
                if prop.startswith('--'):local.setdefault(prop, []).append(value)
    evaluator = Values(shared, local, config, profile)
    results = {'token-values': [], 'spacing-values': [], 'type-values': []}
    details = {key: [] for key in results}
    for path, decls in sources:
        for prop, value in decls:
            if not prop.startswith('--'):prop = prop.lower()
            for kind in kinds_for(prop.lower(), value):
                if kind not in config['profiles'][profile]['required'] and kind not in ('spacing','type'):continue
                target = 'spacing-values' if kind == 'spacing' else ('type-values' if kind == 'type' else 'token-values')
                problems, _ = evaluator.check(value, kind, prop)
                allowed = any(a.get('path') == path and a.get('property') == prop and a.get('value') == value and a.get('reason') for a in config['raw_value_allowlist'])
                if problems and not allowed:
                    results[target].append(f"{path}: {prop}: {value} [{kind}] — " + '; '.join(problems))
                    details[target].append({'path':path,'property':prop,'value':value,'kind':kind,'reasons':problems})
    for key in results:
        record(key, results[key], 'error' if key == 'token-values' else 'warning')
        checks[-1]['profile'] = profile
        checks[-1]['details'] = details[key]
        checks[-1]['by_kind'] = {kind:sum(d['kind'] == kind for d in details[key]) for kind in sorted({d['kind'] for d in details[key]})}
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
    record('js-single-instance',re.findall(r'document\s*\.\s*querySelector\s*\(\s*[\'\"]\[data-[^\'\"]+',js))
    # Lexical approximation: remove comments/strings before counting block depth.
    clean=re.sub(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`',lambda m:'\n'*m[0].count('\n'),js,flags=re.S)
    depth=0;warnings=[]
    for m in re.finditer(r'[{}]|\b(?:const|let)\s+([\w$]+)',clean):
        if m[0]=='{':depth+=1
        elif m[0]=='}':depth=max(0,depth-1)
        elif depth==0:warnings.append(m[0])
    record('js-global-bindings',warnings)
    return checks
