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
        motion=tokens['motion']
        result[motion['multiplier']]=str(motion['defaultMultiplier'])
        for name,value in motion['durationsMs'].items():result['--k-dur-'+name]=f'calc({value}ms * var({motion["multiplier"]}))'
        for name,target in motion['aliases'].items():result['--k-dur-'+name]='var(--k-dur-'+target+')'
        result['--k-ease']=motion['easing']
        for name,value in motion['easings'].items():result['--k-ease-'+name]=value
        radii=tokens['radiusPx'];base=radii['md']
        result['--k-radius']=f'{base:g}px'
        for name,value in radii.items():
            result['--k-radius-'+name]=(f'{value:g}px' if name=='full' else 'var(--k-radius)' if name=='md' else f'calc(var(--k-radius) * {value/base:g})')
    for name,value in tokens['elevation']['rings'].items():result['--k-ring-'+name]=value
    for name,target in tokens['elevation']['aliases'].items():result['--k-shadow-'+name]='var(--k-shadow-'+target+')'
    theme='light' if mode=='root' else mode
    for name,pair in tokens['elevation']['shadows'].items():result['--k-shadow-'+name]=pair[theme]
    result['--k-backdrop']=tokens['elevation']['backdrop'][theme]
    result.update(tokens.get('semanticColors',{}).get(theme,{}))
    return result


def sync(root=ROOT,check=False):
    tokens=json.loads((root/'system/tokens.json').read_text());path=root/'tokens.css';old=path.read_text();new=old
    for mode in ('root','dark','light'):
        start=f'/* shape-tokens:{mode}:start */';end=f'/* shape-tokens:{mode}:end */'
        if new.count(start)!=1 or new.count(end)!=1:raise ValueError('Missing/duplicate shape adapter region: '+mode)
        content='\n'.join('  '+name+':'+value+';' for name,value in values(tokens,mode).items())
        new=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:start+'\n'+content+'\n  '+end,new,flags=re.S)
    if 'contrast' in tokens:
        start='/* relative-color-roles:start */';end='/* relative-color-roles:end */'
        if new.count(start)!=1 or new.count(end)!=1:raise ValueError('Missing relative color adapter region')
        new=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda _:start+'\n'+relative_css(tokens['contrast'])+'\n'+end,new,flags=re.S)
    if old!=new:
        if check:raise ValueError('tokens.css shape adapter is stale; run python3 -m tools.sync_shape_tokens')
        path.write_text(new)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();sync(check=args.check)
