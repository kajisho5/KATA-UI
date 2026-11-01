"""Build KATA Display (v0.1) from glyphs.py stroke data.
Each stroke is drawn as round-cap capsules on a 1000-upm grid:
1 grid unit = 68 units, cap height 680, stroke width 88 (radius 44).
Overlapping contours use nonzero fill, like a stencil cast in one mold."""
import math, sys
sys.path.insert(0, '/home/hatch/workspace/kata-ui/font')
from glyphs import G
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

SCALE = 68
R = 44  # capsule radius

def capsule(pen, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L < 0.01:
        # dot: circle of radius R
        pts = [(x1 + R * math.cos(a), y1 + R * math.sin(a)) for a in [i * math.pi / 6 for i in range(12)]]
    else:
        ux, uy = dx / L, dy / L
        px, py = -uy * R, ux * R
        pts = []
        for cx, cy, base in ((x2, y2, math.atan2(uy, ux)), (x1, y1, math.atan2(-uy, -ux))):
            for i in range(7):
                a = base - math.pi / 2 + i * (math.pi / 6)
                pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    pen.moveTo(pts[0])
    for p in pts[1:]:
        pen.lineTo(p)
    pen.closePath()

def glyph_pen(adv_grid, strokes):
    pen = TTGlyphPen(None)
    for stroke in strokes:
        pts = [(x * SCALE, y * SCALE) for x, y in stroke]
        if len(pts) == 1:
            capsule(pen, *pts[0], *pts[0])
        for a, b in zip(pts, pts[1:]):
            capsule(pen, *a, *b)
    return pen

names = ['.notdef', 'space']
cmap = {0x20: 'space'}
adv = {'space': 320, '.notdef': 560}
glyf = {}
hmtx = {}
pen0 = TTGlyphPen(None)
pen0.moveTo((40, 0)); pen0.lineTo((40, 680)); pen0.lineTo((520, 680)); pen0.lineTo((520, 0)); pen0.closePath()
pen0.moveTo((100, 60)); pen0.lineTo((100, 620)); pen0.lineTo((460, 620)); pen0.lineTo((460, 60)); pen0.closePath()
glyf['.notdef'] = pen0.glyph()
hmtx['.notdef'] = (560, 40)
glyf['space'] = TTGlyphPen(None).glyph()
hmtx['space'] = (320, 0)
for ch, (adv_g, strokes) in G.items():
    name = f'uni{ord(ch):04X}'
    names.append(name)
    cmap[ord(ch)] = name
    width = int(adv_g * SCALE)
    glyf[name] = glyph_pen(adv_g, strokes).glyph()
    hmtx[name] = (width, 0)

fb = FontBuilder(1000, isTTF=True)
fb.setupGlyphOrder(names)
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyf)
fb.setupHorizontalMetrics(hmtx)
fb.setupHorizontalHeader(ascent=760, descent=-240)
fb.setupNameTable({
    'familyName': 'KATA Display', 'styleName': 'Regular',
    'uniqueFontIdentifier': 'KATA Display 0.1',
    'fullName': 'KATA Display', 'psName': 'KATADisplay-Regular',
    'version': 'Version 0.1',
})
fb.setupOS2(sTypoAscender=760, sTypoDescender=-240, usWinAscent=760, usWinDescent=240)
fb.setupPost()
fb.setupMaxp()
out = '/home/hatch/workspace/kata-ui/font/KATA-Display'
fb.save(out + '.ttf')
fb.font.flavor = 'woff2'
fb.save(out + '.woff2')
print('built', out + '.ttf/.woff2', '-', len(names), 'glyphs')
