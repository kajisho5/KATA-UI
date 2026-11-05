"""Token provenance checks. Standard-library lexer; unknown syntax fails closed."""
import re

NUMBER = re.compile(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?(?:[a-zA-Z]+|%)?')
# A CSS identifier never starts with a minus followed by a digit: `-1` and `-4px`
# are numbers (CSS Syntax 3, 4.3.9), so a negated token such as `* -1` is a number.
IDENT = re.compile(r'--[\w-]+|-?[a-zA-Z_][\w-]*')


def split_top(text, delimiter=','):
    out=[];start=0;depth=0;quote=None;escaped=False
    for i,char in enumerate(text):
        if escaped: escaped=False;continue
        if char=='\\':escaped=True;continue
        if quote:
            if char==quote:quote=None
            continue
        if char in ('"', "'"):quote=char;continue
        if char=='(':depth+=1
        elif char==')':depth-=1
        elif char==delimiter and depth==0:out.append(text[start:i].strip());start=i+1
    out.append(text[start:].strip())
    return out


def lex(text):
    result=[];i=0
    while i<len(text):
        char=text[i]
        if text.startswith('/*', i):
            end=text.find('*/',i+2)
            if end<0:return result+[('invalid','unclosed comment',None)]
            i=end+2;continue
        if char.isspace() or char in ',/*':i+=1;continue
        if char in ('"', "'"):
            end=i+1
            while end<len(text):
                if text[end]=='\\':end+=2;continue
                if text[end]==char:break
                end+=1
            result.append(('string',text[i:end+1],None));i=end+1;continue
        m=IDENT.match(text,i)
        # A leading minus may begin either a number or a custom identifier.
        num=NUMBER.match(text,i)
        if num and (not m or len(num[0])>len(m[0])):
            result.append(('number',num[0],None));i=num.end();continue
        if m:
            name=m[0];i=m.end()
            if i<len(text) and text[i]=='(':
                start=i+1;depth=1;quote=None;i+=1
                while i<len(text) and depth:
                    if not quote and text.startswith('/*',i):
                        end=text.find('*/',i+2)
                        if end<0:break
                        i=end+2;continue
                    if text[i]=='\\':i+=2;continue
                    if quote:
                        if text[i]==quote:quote=None
                    elif text[i] in ('"', "'"):quote=text[i]
                    elif text[i]=='(':depth+=1
                    elif text[i]==')':depth-=1
                    i+=1
                if depth:result.append(('invalid','unclosed function',None))
                else:result.append(('function',name,text[start:i-1]))
            else:result.append(('ident',name,None))
            continue
        if char=='#':
            end=i+1
            while end<len(text) and text[end].isalnum():end+=1
            result.append(('color',text[i:end],None));i=end;continue
        if char in '+-':result.append(('operator',char,None))
        elif char not in '()':result.append(('invalid',char,None))
        else:result.append(('operator',char,None))
        i+=1
    return result


def kinds_for(prop, value=""):
    prop=prop.lower()
    if prop.startswith('--'):return []
    if prop=='color-scheme':return []
    if 'radius' in prop:return ['radius']
    if 'shadow' in prop or (prop in ('filter','backdrop-filter') and 'drop-shadow(' in value):return ['shadow']
    if prop.startswith(('margin','padding','inset')) or prop in ('gap','row-gap','column-gap'):return ['spacing']
    if prop in ('font','font-size','line-height'):return ['type']
    if prop.startswith(('animation','transition')):
        if prop.endswith('timing-function'):return ['easing']
        if prop in ('animation','transition'):return ['duration','easing']
        if prop.endswith(('duration','delay')):return ['duration']
        return []
    if prop in ('border-collapse','border-spacing'):return []
    if prop.startswith('border'):
        if prop.endswith('color'):return ['color']
        return ['border','color']
    if 'color' in prop or prop in ('background','background-image','fill','stroke','outline-color'):return ['color']
    return []


class Values:
    def __init__(self, shared, local, config, profile):
        self.shared=shared;self.local=local;self.config=config;self.profile=profile

    def scaled_duration(self, expression):
        """Only a complete time × trusted motion scalar product is controlled motion."""
        factors=split_top(expression, '*')
        if len(factors)!=2:return False
        scalar=self.config['motion_scale_variable']
        if scalar in self.local:return False
        scalar_re=r'var\(\s*'+re.escape(scalar)+r'\s*(?:,\s*[-+]?(?:\d*\.\d+|\d+)\s*)?\)'
        time_re=r'[-+]?(?:\d*\.\d+|\d+)(?:ms|s)'
        def time_factor(value,seen=()):
            if re.fullmatch(time_re,value,re.I):return True
            match=re.fullmatch(r'var\(\s*(--[\w-]+)\s*(?:,\s*(.*?)\s*)?\)',value)
            if not match:return False
            name,fallback=match.groups()
            if name in seen:return False
            if fallback is not None and not time_factor(fallback,seen):return False
            if name in self.local:return all(time_factor(v,seen+(name,)) for v in self.local[name])
            return name in self.shared
        return any(re.fullmatch(scalar_re, factors[i]) and time_factor(factors[1-i]) for i in (0,1))

    def check(self, value, kind, prop, stack=(), arithmetic=False, paint=False):
        if len(stack)>128:return ['variable chain exceeds analysis limit'], False
        value = re.sub(r'\s*!important\s*$', '', value, flags=re.I).strip()
        issues=[];has_token=False
        if not value.strip():return ['empty value'], False
        allowed={x.lower() for x in self.config['allowed_values']['global']+self.config['allowed_values'].get(kind,[])}
        for token,text,args in lex(value):
            low=text.lower()
            if token=='function' and low=='var':
                parts=split_top(args);name=parts[0];fallback=','.join(parts[1:]) if len(parts)>1 else None
                if not re.fullmatch(r'--[\w-]+',name):issues.append('invalid var name');continue
                if name in stack:issues.append('cycle: '+' -> '.join(stack+(name,)));continue
                if name in self.local:
                    for definition in self.local[name]:
                        found,used=self.check(definition,kind,prop,stack+(name,),arithmetic,paint)
                        issues += [name+' -> '+issue for issue in found];has_token |= used
                elif name in self.shared:has_token=True
                elif name in self.config['external_numeric_variables'] and arithmetic:
                    if fallback is None or not re.fullmatch(r'[-+]?\d+(?:\.\d+)?',fallback):issues.append('external scalar requires numeric fallback: '+name)
                elif fallback is None:issues.append('unresolved: '+name)
                # Audit fallbacks even for known tokens: raw fallbacks are still source literals.
                if fallback is not None:
                    if not (name in self.config['external_numeric_variables'] and arithmetic):
                        found,used=self.check(fallback,kind,prop,stack,arithmetic,paint);issues+=found;has_token |= used
                continue
            if token=='function':
                if low=='calc' and kind in ('duration','easing') and self.scaled_duration(args):
                    has_token=True
                    continue
                if low in self.config['arithmetic_functions']:
                    found,used=self.check(args,kind,prop,stack,True,paint)
                    issues+=found;has_token |= used
                    if not used and not found and args.strip() not in allowed:issues.append('arithmetic has no shared token: '+text+'('+args+')')
                elif low in self.config['color_functions']:
                    if kind in ('color','shadow'):issues.append('raw color: '+text+'('+args+')')
                elif low in self.config['paint_functions']:
                    if kind in ('color','shadow'):
                        found,used=self.check(args,'color',prop,stack,False,True);issues+=found;has_token |= used
                elif low in self.config['easing_functions']:
                    if kind=='easing' and low not in self.config['allowed_easing_functions']:issues.append('raw easing: '+text+'('+args+')')
                elif low in self.config['shadow_functions']:
                    found,used=self.check(args,'shadow',prop,stack,arithmetic,paint);issues+=found;has_token |= used
                elif prop in ('filter','backdrop-filter') and low in self.config['filter_geometry_functions']:pass
                elif low=='url':pass  # Image source, not a color literal.
                elif low=='env' and kind=='spacing':
                    # Device geometry (iPhone home indicator, notch) has no token; only the
                    # configured safe-area insets are accepted, and a fallback is still checked.
                    parts=split_top(args)
                    if parts[0].lower() not in self.config['environment_spacing_variables']:issues.append('unsupported env: '+parts[0])
                    if len(parts)>1:
                        found,used=self.check(','.join(parts[1:]),kind,prop,stack,arithmetic,paint);issues+=found;has_token |= used
                else:issues.append('unsupported function: '+text)
                continue
            if low in allowed:continue
            if token=='operator':continue
            if token=='number':
                unit=re.search(r'[a-zA-Z%]+$',text)
                unit=unit[0].lower() if unit else ''
                number=float(text[:-len(unit)] if unit else text)
                if number==0 and '0' in allowed:continue
                if arithmetic and not unit:continue
                if kind=='type' and prop=='font' and low in self.config['font_weight_numbers']:continue
                if kind=='color' and prop in ('background','background-image') and unit in self.config['paint_geometry_units']:continue
                if paint and unit in self.config['paint_geometry_units']:continue  # Configured gradient geometry/mixing grammar.
                if kind in ('duration','easing'):
                    if unit in ('ms','s') and kind=='duration':issues.append('raw duration: '+text)
                    continue
                if kind=='color' and prop.startswith('border'):continue  # Border widths are checked separately.
                exception=self.config['border_width_exception']
                if kind=='border' and prop in exception['properties'] and unit==exception['unit'] and exception['min']<=number<=exception['max']:continue
                issues.append('raw '+kind+': '+text)
                continue
            if token=='ident':
                if paint and low in self.config['paint_keywords']:continue
                if kind=='color' and prop in ('background','background-image') and low in self.config['background_keywords']:continue
                if kind in ('duration','easing'):
                    if low in self.config['easing_keywords'] and kind=='easing':issues.append('raw easing: '+text)
                    # Keyframe/property names and animation keywords are grammar, not token values.
                    continue
                if kind=='color' and prop.startswith('border') and low in self.config['allowed_values']['border']:continue
                if kind=='color' and prop.startswith('border') and low in self.config['border_width_keywords']:continue
                if kind=='border' and low in self.config['allowed_values']['border']:continue
                if kind=='type' and prop=='font':
                    # Font family/style/weight in a shorthand are not font-size or line-height.
                    if low in self.config['font_size_keywords']:issues.append('raw type: '+text)
                    continue
                if kind=='border' and low not in ('thin','medium','thick'):continue  # Colors are checked separately.
                issues.append('raw '+kind+': '+text)
                continue
            if token=='color' and kind not in ('duration','easing','border'):issues.append('raw color: '+text)
            elif token in ('invalid','string') and not (kind=='type' and prop=='font'):issues.append('unresolved syntax: '+text)
        return list(dict.fromkeys(issues)),has_token
