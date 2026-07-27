"""Quantica figure kit — the component vocabulary of the new standard.

Design language (from the reference):
  - each idea lives in its own soft rounded band card on near-white
  - the band is introduced by a filled circular BADGE (an operator glyph), never an all-caps label
  - quantities are rounded TILES with a soft tint and a hairline border
  - groupings are drawn with thin square BRACES that carry a small label
  - the outcome sits in a white RESULT CARD with a coloured border and two sparkles
  - one accent hue per band: blue for the first idea, green for the second
"""
BLUE   = dict(ink='#1d4ed8', mid='#2f6fe0', soft='#dbe8fd', line='#bfd6fb', badge='#2563eb')
GREEN  = dict(ink='#15803d', mid='#16a34a', soft='#dcfce7', line='#bbf7d0', badge='#16a34a')
GOLD   = dict(soft='#fde68a', line='#f0c14b', ink='#8a5a08', mid='#d9a521', badge='#d9a521')
GREY   = dict(soft='#eef1f6', line='#dbe1ea', ink='#64748b')
PAPER  = '#ffffff'
CARDBG = '#fbfcfe'
CARDLN = '#eceff4'
FONT   = 'Space Grotesk, system-ui, sans-serif'

def head(w, h, label):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{label}" font-family="{FONT}">'
            '<defs>'
            '<filter id="qtile" x="-40%" y="-40%" width="180%" height="180%">'
            '<feDropShadow dx="0" dy="2" stdDeviation="2.2" flood-color="#334155" flood-opacity="0.16"/></filter>'
            '<filter id="qcard" x="-30%" y="-30%" width="160%" height="160%">'
            '<feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#1e293b" flood-opacity="0.10"/></filter>'
            '</defs>')

def band(x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{CARDBG}" '
            f'stroke="{CARDLN}" stroke-width="1.5"/>')

def badge(cx, cy, glyph, pal, r=23):
    """Filled circle carrying an operator glyph. Replaces the old all-caps band label."""
    g = ''
    if glyph == '+':
        g = (f'<path d="M{cx-9} {cy} H{cx+9} M{cx} {cy-9} V{cy+9}" fill="none" stroke="#fff" '
             f'stroke-width="4.2" stroke-linecap="round"/>')
    elif glyph == '-':
        g = (f'<path d="M{cx-9} {cy} H{cx+9}" fill="none" stroke="#fff" '
             f'stroke-width="4.2" stroke-linecap="round"/>')
    elif glyph == 'x':
        d = 6.6
        g = (f'<path d="M{cx-d} {cy-d} L{cx+d} {cy+d} M{cx+d} {cy-d} L{cx-d} {cy+d}" fill="none" stroke="#fff" '
             f'stroke-width="4.2" stroke-linecap="round"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{pal["badge"]}"/>{g}'

def tile(x, y, txt, pal, s=54, fs=24):
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="13" fill="{pal["soft"]}" '
            f'stroke="{pal["line"]}" stroke-width="1.5" filter="url(#qtile)"/>'
            f'<text x="{x+s/2}" y="{y+s/2+fs*0.35}" text-anchor="middle" font-size="{fs}" '
            f'font-weight="700" fill="{pal["ink"]}">{txt}</text>')

def tilerow(x, y, n, txt, pal, s=54, gap=10, fs=24):
    return ''.join(tile(x + i*(s+gap), y, txt, pal, s, fs) for i in range(n))

def rowwidth(n, s=54, gap=10):
    return n*s + (n-1)*gap

def brace_up(x1, x2, y, label, colour, depth=11, fs=17):
    """Square brace opening upward, with the label above it."""
    mid = (x1+x2)/2
    return (f'<path d="M{x1} {y} V{y-depth} H{x2} V{y}" fill="none" stroke="{colour}" '
            f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<text x="{mid}" y="{y-depth-9}" text-anchor="middle" font-size="{fs}" '
            f'font-weight="700" fill="{colour}">{label}</text>')

def brace_down(x1, x2, y, label, colour, depth=11, fs=19):
    mid = (x1+x2)/2
    return (f'<path d="M{x1} {y} V{y+depth} H{x2} V{y}" fill="none" stroke="{colour}" '
            f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<text x="{mid}" y="{y+depth+21}" text-anchor="middle" font-size="{fs}" '
            f'font-weight="700" fill="{colour}">{label}</text>')

def brace_left(y1, y2, x, label, colour, depth=11, fs=19):
    mid = (y1+y2)/2
    return (f'<path d="M{x} {y1} H{x-depth} V{y2} H{x}" fill="none" stroke="{colour}" '
            f'stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<text x="{x-depth-13}" y="{mid+7}" text-anchor="middle" font-size="{fs}" '
            f'font-weight="700" fill="{colour}">{label}</text>')

def arrow(x1, x2, y, colour, w=3):
    return (f'<path d="M{x1} {y} H{x2-9}" fill="none" stroke="{colour}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{x2-13} {y-7} L{x2} {y} L{x2-13} {y+7}" fill="none" stroke="{colour}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

def sparkle(cx, cy, r, colour, op=0.9):
    """Four-point star with concave sides, the reference's accent mark."""
    k = r * 0.26
    return (f'<path d="M{cx} {cy-r} C{cx+k} {cy-k} {cx+k} {cy-k} {cx+r} {cy} '
            f'C{cx+k} {cy+k} {cx+k} {cy+k} {cx} {cy+r} '
            f'C{cx-k} {cy+k} {cx-k} {cy+k} {cx-r} {cy} '
            f'C{cx-k} {cy-k} {cx-k} {cy-k} {cx} {cy-r} Z" fill="{colour}" opacity="{op}"/>')

def result(x, y, w, h, pal, base, exp=None, fs=32):
    """White card, coloured border, two sparkles. exp=None renders plain text."""
    cx, cy = x + w / 2, y + h / 2
    if exp is None:
        body = (f'<text x="{cx}" y="{cy + fs * 0.34}" text-anchor="middle" font-size="{fs}" '
                f'font-weight="700" fill="{pal["ink"]}">{base}</text>')
    else:
        body = (f'<text x="{cx}" y="{cy + fs * 0.34}" text-anchor="middle" font-size="{fs}" '
                f'font-weight="700" fill="{pal["ink"]}">{base}'
                f'<tspan font-size="{int(fs * 0.62)}" dy="-{int(fs * 0.42)}">{exp}</tspan></text>')
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{PAPER}" '
            f'stroke="{pal["mid"]}" stroke-width="2" filter="url(#qcard)"/>'
            + sparkle(x + 22, y + 21, 7.5, pal['mid'])
            + sparkle(x + w - 20, y + h - 19, 6, pal['mid'], 0.75)
            + body)

def dot(cx, cy, colour, r=4.5):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{colour}"/>'

def label(x, y, txt, colour, fs=22, anchor='middle', weight=700):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" '
            f'font-weight="{weight}" fill="{colour}">{txt}</text>')

def pw(x, y, base, exp, colour, fs=26, anchor='middle'):
    """base^exp as text."""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" font-weight="700" '
            f'fill="{colour}">{base}<tspan font-size="{int(fs*0.62)}" dy="-{int(fs*0.40)}">{exp}</tspan></text>')


# ── extra components for the Algebra I set ──────────────────────────────────
GREYPAL = dict(ink='#94a3b8', mid='#aab4c2', soft='#eef1f6', line='#dbe1ea', badge='#94a3b8')

def card(x, y, w, h, txt, pal, fs=27, sub=None):
    """White card holding an expression."""
    cx, cy = x + w / 2, y + h / 2
    t = (f'<text x="{cx}" y="{cy + fs*0.34}" text-anchor="middle" font-size="{fs}" '
         f'font-weight="700" fill="{pal["ink"]}">{txt}</text>')
    if sub:
        t = (f'<text x="{cx}" y="{cy + fs*0.10}" text-anchor="middle" font-size="{fs}" '
             f'font-weight="700" fill="{pal["ink"]}">{txt}</text>'
             f'<text x="{cx}" y="{cy + fs*0.10 + 22}" text-anchor="middle" font-size="14" '
             f'font-weight="600" fill="{pal["mid"]}">{sub}</text>')
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="17" fill="{PAPER}" '
            f'stroke="{pal["mid"]}" stroke-width="2" filter="url(#qcard)"/>' + t)

def arrowl(x1, x2, y, colour, w=3):
    """Arrow pointing left, from x2 back to x1."""
    return (f'<path d="M{x2} {y} H{x1+9}" fill="none" stroke="{colour}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{x1+13} {y-7} L{x1} {y} L{x1+13} {y+7}" fill="none" stroke="{colour}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

def strike(x1, y1, x2, y2, colour, w=3):
    return (f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{colour}" '
            f'stroke-width="{w}" stroke-linecap="round"/>')

def pill(x, y, w, h, pal, r=None):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r or h/2}" '
            f'fill="{pal["soft"]}" stroke="{pal["line"]}" stroke-width="1.5"/>')

def tag(x, y, txt, pal, fs=13):
    """Small outlined tag, sentence case (never all caps)."""
    w = max(52, 10 + len(txt) * fs * 0.58)
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="9" fill="{PAPER}" '
            f'stroke="{pal["mid"]}" stroke-width="1.6"/>'
            f'<text x="{x + w/2:.0f}" y="{y+18}" text-anchor="middle" font-size="{fs}" '
            f'font-weight="700" fill="{pal["ink"]}">{txt}</text>')

def caption(x, y, txt, colour, fs=17, anchor='start'):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" '
            f'font-weight="600" fill="{colour}">{txt}</text>')

def numline(x, y, w, ticks, colour, marks=(), below=False):
    """Horizontal axis with ticks; marks = [(fraction 0..1, label, dotcolour)]."""
    o = [f'<path d="M{x} {y} H{x+w}" fill="none" stroke="{colour}" stroke-width="2.5" stroke-linecap="round"/>']
    for i in range(ticks + 1):
        tx = x + w * i / ticks
        o.append(f'<path d="M{tx:.1f} {y-7} V{y+7}" fill="none" stroke="{colour}" stroke-width="2" stroke-linecap="round"/>')
    for frac, lab, dc in marks:
        tx = x + w * frac
        o.append(f'<circle cx="{tx:.1f}" cy="{y}" r="9" fill="{dc}"/>')
        ly = y + 34 if below else y - 20
        o.append(f'<text x="{tx:.1f}" y="{ly}" text-anchor="middle" font-size="18" '
                 f'font-weight="700" fill="{dc}">{lab}</text>')
    return ''.join(o)

def frac(cx, cy, num, den, colour, fs=25, half=52):
    """Stacked fraction centred on (cx, cy)."""
    return (f'<text x="{cx}" y="{cy-11}" text-anchor="middle" font-size="{fs}" font-weight="700" '
            f'fill="{colour}">{num}</text>'
            f'<path d="M{cx-half} {cy} H{cx+half}" fill="none" stroke="{colour}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<text x="{cx}" y="{cy+fs+4}" text-anchor="middle" font-size="{fs}" font-weight="700" '
            f'fill="{colour}">{den}</text>')


def arc(x1, x2, y, colour, label='', up=True, lift=54, fs=15):
    """Curved arrow from x1 to x2, bowing above (up) or below the baseline."""
    mid = (x1 + x2) / 2
    cy = y - lift if up else y + lift
    d = f'M{x1} {y} Q{mid} {cy} {x2} {y}'
    # arrowhead at the x2 end, pointing along the tangent
    sgn = 1 if x2 > x1 else -1
    ay = y - 11 if up else y + 11
    head = (f'<path d="M{x2 - sgn*13} {ay} L{x2} {y} L{x2 - sgn*13} {y + (11 if up else -11)}" '
            f'fill="none" stroke="{colour}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    lab = (f'<text x="{mid}" y="{cy - 8 if up else cy + 20}" text-anchor="middle" font-size="{fs}" '
           f'font-weight="700" fill="{colour}">{label}</text>') if label else ''
    return (f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="2.6" stroke-linecap="round"/>'
            + head + lab)

def cells(x, y, w, h, n, pal, label=None, fs=15):
    """A bar split into n equal cells."""
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{pal["soft"]}" '
         f'stroke="{pal["line"]}" stroke-width="1.8"/>']
    for i in range(1, n):
        cx = x + w * i / n
        o.append(f'<path d="M{cx:.1f} {y} V{y+h}" fill="none" stroke="{pal["line"]}" stroke-width="1.5"/>')
    if label:
        o.append(f'<text x="{x + w/2}" y="{y - 10}" text-anchor="middle" font-size="{fs}" '
                 f'font-weight="700" fill="{pal["ink"]}">{label}</text>')
    return ''.join(o)

def eqrow(x, y, left, right, pal, fs=21, w=300):
    """One row of an equation ladder: left = right."""
    return (f'<text x="{x}" y="{y}" font-size="{fs}" font-weight="700" fill="{pal["ink"]}">{left}</text>'
            f'<text x="{x+w*0.62:.0f}" y="{y}" font-size="{fs}" font-weight="700" fill="{pal["mid"]}">=</text>'
            f'<text x="{x+w:.0f}" y="{y}" text-anchor="end" font-size="{fs}" font-weight="700" '
            f'fill="{pal["ink"]}">{right}</text>')
