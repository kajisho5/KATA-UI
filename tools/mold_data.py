"""Narrow HTML data-color exception shared by legacy and provenance checks."""
from html.parser import HTMLParser
import re
from tools.token_values import kinds_for


def is_color_data(filename, attrs, config):
    policy=config['inline_color_data']
    return filename in policy['files'] and any(name in attrs for name in policy['attributes'])


def mask_color_data(text, filename, config):
    """Mask only eligible inline color declarations, preserving all other source text."""
    class Mask(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if not is_color_data(filename,dict(attrs),config):return
            raw=self.get_starttag_text();line,col=self.getpos()
            offset=sum(len(x) for x in text.splitlines(keepends=True)[:line-1])+col
            for style in re.finditer(r'\bstyle\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))',raw,re.I):
                group=next(i for i in (1,2,3) if style[i] is not None)
                for decl in re.finditer(r'(?:^|;)\s*([\w-]+)\s*:\s*([^;]+)',style[group]):
                    if 'color' in kinds_for(decl[1],decl[2]):
                        start=offset+style.start(group)+decl.start(2)
                        spans.append((start,start+len(decl[2])))
        handle_startendtag=handle_starttag
    spans=[];Mask(convert_charrefs=True).feed(text)
    for start,end in sorted(spans,reverse=True):text=text[:start]+' '*(end-start)+text[end:]
    return text
