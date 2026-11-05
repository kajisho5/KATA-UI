"""Canonical WCAG color-role math and generated CSS recipes (no component exceptions)."""


def rgb(value):
    value=value.lstrip('#')
    return [int(value[i:i+2],16)/255 for i in (0,2,4)]


def linear(c):return c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4

def encoded(c):return 12.92*c if c<=.0031308 else 1.055*max(0,c)**(1/2.4)-.055

def luminance(value):return sum(linear(c)*w for c,w in zip(rgb(value),(.2126,.7152,.0722)))

def contrast(a,b):
    low,high=sorted((luminance(a),luminance(b)))
    return (high+.05)/(low+.05)


def on_accent(accent,config):
    y=luminance(accent)
    if y<config['switchLuminance']:return config['lightText']
    target=max(0,min(luminance(config['darkText']),(y+.05)/config['preferredMinimum']-.05))
    scale=target/luminance(config['darkText'])
    channels=[round(max(0,min(1,encoded(linear(c)*scale)))*255) for c in rgb(config['darkText'])]
    return '#'+''.join(f'{c:02x}' for c in channels)


def relative_css(config):
    # A neutral linear-sRGB carrier stores the exact WCAG Y; OKLCH L alone cannot
    # represent the same luminance threshold for every chromatic hue.
    y='calc(r * 0.2126 + g * 0.7152 + b * 0.0722)'
    carrier='color(from var(--k-accent) srgb-linear '+ ' '.join([y]*3)+')'
    switch=f"clamp(0, calc(({config['switchLuminance']} - r) * 10000000000), 1)"
    ink_y=luminance(config['darkText']);channels=[]
    for c in rgb(config['darkText']):
        channel=linear(c);ratio=channel/ink_y
        dark=f"min({channel:.12g}, calc(max(0, calc((r + 0.05) / {config['preferredMinimum']} - 0.05)) * {ratio:.12g}))"
        channels.append(f'max({switch}, {dark})')
    on='color(from var(--k-accent-luminance) srgb-linear '+' '.join(channels)+')'
    inverse=f'calc(1 - {switch})'
    surface='color(from var(--k-accent-luminance) srgb-linear '+' '.join([inverse]*3)+')'
    return '\n'.join([
        '@supports (color: oklch(from red l c h)) {',
        '  :root,[data-theme="light"],[data-theme="dark"] {',
        '    --k-accent-luminance:'+carrier+';',
        '    --k-on-accent:'+on+';',
        '    --k-accent-contrast-surface:'+surface+';',
        '  }',
        '  :root,[data-theme="light"] {--k-accent-ink:oklch(from var(--k-accent) min(l, '+str(config['accentInkLightMaxL'])+') c h);}',
        '  [data-theme="dark"] {--k-accent-ink:oklch(from var(--k-accent) max(l, '+str(config['accentInkDarkMinL'])+') c h);}',
        '}',
    ])


def accent_ink(accent,mode,config):
    """Static sRGB fallback: preserve hue with the smallest black/white mix for AA."""
    channels=rgb(accent);target=0 if mode=='light' else 1
    def mixed(t):return '#'+''.join(f'{round((c+(target-c)*t)*255):02x}' for c in channels)
    def passes(value):return all(contrast(value,bg)>=config['preferredMinimum'] for bg in config['backgrounds'][mode])
    if passes(accent):return accent
    lo,hi=0,1
    for _ in range(24):
        mid=(lo+hi)/2
        if passes(mixed(mid)):hi=mid
        else:lo=mid
    return mixed(hi)


def theme_css(accent,config):
    on=on_accent(accent,config);surface='#ffffff' if luminance(accent)>=config['switchLuminance'] else '#000000'
    weight=config['hoverAccentPercent']/100
    hover='#'+''.join(f'{round((a*weight+b*(1-weight))*255):02x}' for a,b in zip(rgb(accent),rgb(surface)))
    channels=','.join(str(round(c*255)) for c in rgb(accent))
    lines=['/* KATA theme: static WCAG color roles. Load after tokens.css. */']
    for mode,selector in [('light',':root,[data-theme="light"]'),('dark','[data-theme="dark"]')]:
        values={'--k-accent':accent,'--k-on-accent':on,'--k-accent-ink':accent_ink(accent,mode,config),'--k-accent-contrast-surface':surface,'--k-accent-hover':hover,'--k-accent-bg':f'rgba({channels},.08)','--k-accent-bg-strong':f'rgba({channels},.1)','--k-accent-line':f'rgba({channels},.18)'}
        lines.append(selector+'{\n'+''.join('  '+k+':'+v+';\n' for k,v in values.items())+'}')
    return '\n'.join(lines)+'\n'
