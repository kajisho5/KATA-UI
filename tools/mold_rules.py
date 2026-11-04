"""Conservative static checks; runtime selector/cascade coverage is tested separately."""
import json, re
from html.parser import HTMLParser
from tools.token_values import Values, kinds_for, split_top, lex, NUMBER
from tools.mold_data import is_color_data

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

def dependency_styles(directory, root, seen=None):
    """Use the same link/parts declarations as the builder, plus metadata deps."""
    seen=set() if seen is None else seen
    directory=directory.resolve()
    if directory in seen:return []
    seen.add(directory);out=[]
    try:meta=json.loads((directory/'meta.json').read_text())
    except (ValueError,OSError):meta={}
    names=[]
    for key in ('deps','uses','blocks'):
        declared=meta.get(key,[])
        names.extend([declared] if isinstance(declared,str) else declared if isinstance(declared,list) else [])
    for html in directory.glob('*.html'):
        text=html.read_text()
        for declaration in re.findall(r'<!--\s*parts:\s*(.*?)\s*-->',text,re.S):names.extend(declaration.split(','))
        for node in Markup(text).nodes:
            href=node['attrs'].get('href') or ''
            if node['tag']=='link' and href.endswith('.css'):
                target=(root/href.lstrip('/') if href.startswith('/') else html.parent/href).resolve()
                if target.is_file() and target.is_relative_to(root.resolve()):
                    out.append(target.read_text());out.extend(dependency_styles(target.parent,root,seen))
    for name in names:
        if not isinstance(name,str):continue
        name=name.strip()
        if not re.fullmatch(r'[a-z0-9-]+',name):continue
        for group in ('components','blocks'):
            folder=root/group/name;css=folder/(name+'.css')
            if css.is_file():
                out.append(css.read_text());out.extend(dependency_styles(folder,root,seen));break
    return out


def focus_matches(node, selector, body, config):
    """Static selector evidence only; P7 must measure the rendered focus ring."""
    if ':focus-visible' not in selector:return False
    attrs=node['attrs'];tag=node['tag'];classes=attrs.get('class','').split()
    declarations_=dict(declarations(body))
    # The existing outline-only safety net is not the shared ring contract.
    global_ring=any(token in declarations_.get('box-shadow','') for token in config['global_focus_ring_tokens'])
    # Expand :where/:is subject alternatives without splitting function arguments.
    branches=[]
    for branch in split_top(selector):
        match=re.search(r':(?:where|is)\(([^()]*)\)',branch)
        if match:
            branches.extend(branch[:match.start()]+part+branch[match.end():] for part in split_top(match[1]))
        else:branches.append(branch)
    for branch in branches:
        if ':focus-visible' not in branch:continue
        subject=branch.split(':focus-visible',1)[0]
        # Dependency rules scoped to another host must not cover every input.
        ancestry=re.split(r'[>+~\s]+',subject.strip())[:-1]
        ancestors=list(reversed(node.get('parents',[])))
        matched=True
        for ancestor in reversed(ancestry):
            if not ancestor:continue
            needed=set(re.findall(r'\.([\w-]+)',ancestor))
            ancestor_tag=re.match(r'^([a-z][\w-]*)',ancestor)
            index=next((i for i,p in enumerate(ancestors) if needed.issubset(p['attrs'].get('class','').split()) and (not ancestor_tag or ancestor_tag[1]==p['tag'])),None)
            if index is None:matched=False;break
            ancestors=ancestors[index+1:]
        if not matched:continue
        # Ignore ancestor classes: .parent .other:focus-visible cannot cover .parent.
        subject=re.split(r'[>+~\s]+',subject.strip())[-1]
        required=re.findall(r'\.([\w-]+)',subject)
        if required and not set(required).issubset(classes):continue
        tag_match=re.match(r'^([a-z][\w-]*)',subject)
        if tag_match and tag_match[1]!=tag:continue
        roles=re.findall(r'\[role=[\"\']?([\w-]+)',subject)
        if roles and attrs.get('role') not in roles:continue
        if '[tabindex]' in subject and 'tabindex' not in attrs:continue
        relevant=bool(required or tag_match or roles or '[tabindex]' in subject)
        if relevant:return True
        if global_ring and re.fullmatch(r'(?:\*|:where\(|:is\(|)',subject):return True
    return False


def contains_drop_shadow(value, local, seen=()):
    for token,name,args in lex(value):
        if token!='function':continue
        if name.lower()=='drop-shadow':return True
        if name.lower()=='var':
            parts=split_top(args);variable=parts[0]
            if any(contains_drop_shadow(part,local,seen) for part in parts[1:]):return True
            if variable not in seen and any(contains_drop_shadow(v,local,seen+(variable,)) for v in local.get(variable,[])):return True
    return False


def lab_shadow_issues(value, evaluator, prop, stack=(), mixing=False):
    """Lab owns glow geometry; shared-token paint provenance remains mandatory."""
    if len(stack)>128:return ['variable chain exceeds analysis limit']
    issues=[];value=re.sub(r'\s*!important\s*$','',value,flags=re.I).strip()
    allowed={v.lower() for v in evaluator.config['allowed_values']['global']+evaluator.config['allowed_values']['shadow']}
    for token,text,args in lex(value):
        if token=='ident' and NUMBER.fullmatch(text):token='number'
        low=text.lower()
        if token=='function' and low=='var':
            parts=split_top(args);name=parts[0]
            if name in stack:issues.append('cycle: '+' -> '.join(stack+(name,)));continue
            if name in evaluator.local:
                for definition in evaluator.local[name]:
                    issues.extend(name+' -> '+v for v in lab_shadow_issues(definition,evaluator,prop,stack+(name,),mixing))
            elif not (name.startswith('--k-') and name in evaluator.shared):issues.append('unresolved shared paint/geometry variable: '+name)
            if len(parts)>1:issues.extend(lab_shadow_issues(','.join(parts[1:]),evaluator,prop,stack,mixing))
        elif token=='function':
            if low=='color-mix':issues.extend(lab_shadow_issues(args,evaluator,prop,stack,True))
            elif low in evaluator.config['shadow_functions'] or low in evaluator.config['arithmetic_functions']:
                issues.extend(lab_shadow_issues(args,evaluator,prop,stack,mixing))
            elif prop in ('filter','backdrop-filter') and low in evaluator.config['filter_geometry_functions']:
                issues.extend(lab_shadow_issues(args,evaluator,prop,stack,mixing))
            else:issues.append('raw/unsupported shadow paint: '+text+'('+args+')')
        elif token=='number':
            if mixing and not re.fullmatch(r'[-+]?(?:\d*\.\d+|\d+)%',text):issues.append('invalid color-mix weight: '+text)
        elif token=='ident':
            if low in allowed:continue
            if mixing and low in evaluator.config['paint_keywords']:continue
            issues.append('raw shadow color/unsupported keyword: '+text)
        elif token=='color':issues.append('raw shadow color: '+text)
        elif token not in ('operator',):issues.append('unresolved shadow syntax: '+text)
    return list(dict.fromkeys(issues))


def finding_kind(value, kind, evaluator, config, seen=()):
    expanded=value
    for name in re.findall(r'var\(\s*(--[\w-]+)',value):
        if name in evaluator.local and name not in seen:
            nested=' '.join(evaluator.local[name])
            classified=finding_kind(nested,kind,evaluator,config,seen+(name,))
            if classified!=kind:return classified
            expanded+=' '+nested
    if kind=='radius' and any(float(n)>=config['pill_radius_min_px'] for n in re.findall(r'(?<![\w.-])(\d+(?:\.\d+)?)px\b',expanded,re.I)):
        return 'radius-full'
    if kind=='shadow' and re.search(r'(?:^|,)\s*(?:inset\s+)?0\s+0\s+0\s+(?:\d*\.\d+|\d+)px\s+',expanded,re.I):
        return 'shadow-ring'
    return kind

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
    sources = [(str(css_path.relative_to(root)), declarations(body), False) for _, body in rules(css)]
    dependency_css = dependency_styles(directory,root)
    for f, doc in docs:
        for embedded in re.findall(r'<style[^>]*>(.*?)</style>', f.read_text(), re.S | re.I):
            sources.extend((str(f.relative_to(root)), declarations(body), False) for _, body in rules(embedded))
        for node in doc.nodes:
            attrs = node['attrs']
            if 'style' in attrs: sources.append((str(f.relative_to(root)), declarations(attrs['style']), is_color_data(f.name,attrs,config)))
    local = {}
    for _, decls, _ in sources:
        for prop, value in decls:
            if prop.startswith('--'):local.setdefault(prop, []).append(value)
    for dep in dependency_css:
        for _, body in rules(dep):
            for prop, value in declarations(body):
                if prop.startswith('--'):local.setdefault(prop, []).append(value)
    evaluator = Values(shared, local, config, profile)
    results = {'token-values': [], 'spacing-values': [], 'type-values': []}
    details = {key: [] for key in results}
    for path, decls, color_data in sources:
        for prop, value in decls:
            if not prop.startswith('--'):prop = prop.lower()
            kinds=kinds_for(prop.lower(),value)
            if prop in ('filter','backdrop-filter') and contains_drop_shadow(value,local):kinds=['shadow']
            for kind in kinds:
                if kind=='color' and color_data:continue
                if kind not in config['profiles'][profile]['required'] and kind not in ('spacing','type'):continue
                target = 'spacing-values' if kind == 'spacing' else ('type-values' if kind == 'type' else 'token-values')
                problems, _ = evaluator.check(value, kind, prop)
                if profile=='lab' and kind=='shadow':problems=lab_shadow_issues(value,evaluator,prop)
                reported_kind = 'shadow' if profile=='lab' and kind=='shadow' else finding_kind(value,kind,evaluator,config)
                allowed = any(a.get('path') == path and a.get('property') == prop and a.get('value') == value and a.get('reason') for a in config['raw_value_allowlist'])
                if problems and not allowed:
                    results[target].append(f"{path}: {prop}: {value} [{reported_kind}] — " + '; '.join(problems))
                    details[target].append({'path':path,'property':prop,'value':value,'kind':reported_kind,'reasons':problems})
    for key in results:
        record(key, results[key], 'error' if key == 'token-values' else 'warning')
        checks[-1]['profile'] = profile
        checks[-1]['details'] = details[key]
        checks[-1]['by_kind'] = {kind:sum(d['kind'] == kind for d in details[key]) for kind in sorted({d['kind'] for d in details[key]})}
    types=[];labels=[];focus=[]
    focus_details={}
    candidates=rules(css+'\n'+'\n'.join(dependency_css)) + rules(token_source)
    for f,doc in docs:
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
            if not any(focus_matches(n,sel,body,config) for sel,body in candidates):
                signature=' '.join(sorted(set(a.get('class','').split()))) or a.get('role','')
                key=(str(f.relative_to(root)),tag,signature)
                if key not in focus_details:focus_details[key]={'path':key[0],'tag':tag,'class_or_role':signature,'occurrences':0}
                focus_details[key]['occurrences']+=1
    focus=[f"{path}: <{tag}> {signature}" for path,tag,signature in focus_details]
    record('button-type',types);record('accessible-label',labels);record('focus-visible',focus)
    checks[-1]['details']=list(focus_details.values())
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
