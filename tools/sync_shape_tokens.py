"""Generate the radius/elevation/semantic-color CSS adapter from canonical system/tokens.json."""
import argparse
import json
from pathlib import Path
import re
from tools.color_roles import relative_css

ROOT=Path(__file__).resolve().parents[1]


def values(tokens,mode):
    result={}
    if mode=='root':
        if 'moldVersion' in tokens:result['--k-mold']=str(tokens['moldVersion'])
        result.update({'--k-'+name:value for name,value in tokens['color'].get('fixed',{}).items()})
        motion=tokens['motion']
        result[motion['multiplier']]=str(motion['defaultMultiplier'])
        for name,value in motion['durationsMs'].items():result['--k-dur-'+name]=f'calc({value}ms * var({motion["multiplier"]}))'
        for name,target in motion['aliases'].items():result['--k-dur-'+name]='var(--k-dur-'+target+')'
        result['--k-ease']=motion['easing']
        for name,value in motion['easings'].items():result['--k-ease-'+name]=value
        # Deprecated public names keep working; all first-party consumers use canonical names.
        for name,target in motion.get('deprecatedEasingAliases',{}).items():result['--k-ease-'+name]='var(--k-ease-'+target+')'
        radii=tokens['radiusPx'];base=radii['md']
        result['--k-radius']=f'{base:g}px'
        for name,value in radii.items():
            result['--k-radius-'+name]=(f'{value:g}px' if name=='full' else 'var(--k-radius)' if name=='md' else f'calc(var(--k-radius) * {value/base:g})')
    # Declared in every theme block, like the other rings: var() resolves where the
    # property is declared, so a nested [data-theme] needs its own copy.
    if 'focus' in tokens['elevation']:result['--k-ring']=tokens['elevation']['focus']
    for name,value in tokens['elevation']['rings'].items():result['--k-ring-'+name]=value
    for name,target in tokens['elevation']['aliases'].items():result['--k-shadow-'+name]='var(--k-shadow-'+target+')'
    theme='light' if mode=='root' else mode
    for name,pair in tokens['elevation']['shadows'].items():result['--k-shadow-'+name]=pair[theme]
    result['--k-backdrop']=tokens['elevation']['backdrop'][theme]
    result.update(tokens.get('semanticColors',{}).get(theme,{}))
    return result


def _num(value, unit=''):
    """CSS number text as tokens.css writes it: 12.5px, .012em, -.025em."""
    text=f'{float(value):g}'
    text=text.replace('0.','.',1) if text.startswith('0.') else text.replace('-0.','-.',1) if text.startswith('-0.') else text
    return text+unit


def scale_css(tokens):
    """Spacing, text, tracking and leading scales, one line per family (KATA.md 0.5)."""
    font=tokens['font']
    kebab=lambda name:re.sub(r'([A-Z])',lambda m:'-'+m[1].lower(),name)
    rows=[' '.join(f'--k-space-{k}:{_num(v,"px")};' for k,v in tokens['spacePx'].items()),
      ' '.join(f'--k-text-{k}:{_num(v,"px")};' for k,v in tokens['typeScalePx'].items()),
      '/* type tracking & leading — the table in KATA.md §0.5 */',
      ' '.join(f'--k-ls-{kebab(k)}:{_num(v.replace("em",""),"em")};' for k,v in font['trackingScale'].items()),
      ' '.join(f'--k-lh-{k}:{_num(v)};' for k,v in font['leadingScale'].items())]
    return '\n'.join('  '+row for row in rows)


def sync(root=ROOT,check=False):
    tokens=json.loads((root/'system/tokens.json').read_text());path=root/'tokens.css';old=path.read_text();new=old
    for mode in ('root','dark','light'):
        start=f'/* shape-tokens:{mode}:start */';end=f'/* shape-tokens:{mode}:end */'
        if new.count(start)!=1 or new.count(end)!=1:raise ValueError('Missing/duplicate shape adapter region: '+mode)
        content='\n'.join('  '+name+':'+value+';' for name,value in values(tokens,mode).items())
        new=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:start+'\n'+content+'\n  '+end,new,flags=re.S)
    if 'spacePx' in tokens:
        start='/* scale-tokens:start */';end='/* scale-tokens:end */'
        if new.count(start)!=1 or new.count(end)!=1:raise ValueError('Missing/duplicate scale region')
        new=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:start+'\n'+scale_css(tokens)+'\n  '+end,new,flags=re.S)
    outline=tokens['elevation'].get('focusOutline')
    if outline:
        start='/* focus-floor:start */';end='/* focus-floor:end */'
        if new.count(start)!=1 or new.count(end)!=1:raise ValueError('Missing/duplicate focus floor region')
        # Zero specificity: any component rule replaces the floor, but nothing has to declare it.
        rule=f":where(:focus-visible){{outline:{outline['width']} solid {outline['color']};outline-offset:{outline['offset']}}}"
        new=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:start+'\n'+rule+'\n'+end,new,flags=re.S)
    if 'contrast' in tokens:
        start='/* relative-color-roles:start */';end='/* relative-color-roles:end */'
        if new.count(start)!=1 or new.count(end)!=1:raise ValueError('Missing relative color adapter region')
        new=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:start+'\n'+relative_css(tokens['contrast'])+'\n'+end,new,flags=re.S)
    if 'moldVersion' in tokens:
        header=f"/* KATA mold v{tokens['moldVersion']} — {tokens['moldDate']} — kata-ui.dev/docs/mold-changelog */"
        new=re.sub(r'^/\* KATA mold v[^\n]+\*/\n','',new)
        new=header+'\n'+new
    if old!=new:
        if check:raise ValueError('tokens.css shape adapter is stale; run python3 -m tools.sync_shape_tokens')
        path.write_text(new)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();sync(check=args.check)
