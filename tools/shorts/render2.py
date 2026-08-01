"""
Quantica short #2  "One 18 inch pizza beats two 12 inch pizzas"

  18 in across -> r = 9, area 81pi.   two 12 in -> r = 6, 36pi each, 72pi total.
  81pi > 72pi, the gap is 9pi, which is exactly 1/9 of the big pizza.
  1.5^2 = 2.25, so one big equals 2.25 smalls.
  The pour line is the chord cutting off exactly 9pi, solved numerically at h = 3.0295 in.

Beats are pinned to the narration schedule in lines.py, which was written to sound natural
and then measured. The pictures move to fit the speech, never the other way round.
"""
import os, math
from PIL import Image, ImageDraw
from qkit import *
from render import grot, LIME, LIME_I, AMBER, AMBER_I, CORAL, CORAL_I

OUT = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(OUT, "frames2")

# ---- pizza palette
CRUST   = (214, 158, 90)
CRUST_D = (176, 118, 56)
CHEESE  = (245, 199, 74)
SAUCE   = (223, 132, 62)
PEP     = (183, 58, 46)
PEP_D   = (146, 42, 33)

R_BIG = 210
R_SML = int(round(R_BIG*6/9))          # 140, the exact 6/9 ratio
BIG   = (W//2, 660)
SML_L = (W//2-172, 1150)
SML_R = (W//2+172, 1150)
CAP_Y = 1380
TOP_Y = 372

# pepperoni laid out in polar coords, fixed so every render is identical
PEPS = [(0.10, 0.62), (0.24, 0.30), (0.38, 0.72), (0.52, 0.46),
        (0.63, 0.78), (0.74, 0.22), (0.86, 0.58), (0.95, 0.36),
        (0.44, 0.08), (0.18, 0.86)]


def _pour_h():
    def area(h):
        r = 9.0
        return r*r*math.acos((r-h)/r)-(r-h)*math.sqrt(2*r*h-h*h)
    lo, hi = 0.0, 9.0
    for _ in range(200):
        m = (lo+hi)/2
        if area(m) < 9*math.pi: lo = m
        else: hi = m
    return lo
POUR_IN = _pour_h()
POUR_PX = POUR_IN/9.0*R_BIG


def pizza(d, c, r, a, n_pep=10, eaten=False):
    """A pizza that looks like a pizza. Crust ring, cheese, pepperoni."""
    if a <= 0.004: return
    x, y = c
    d.ellipse([x-r, y-r, x+r, y+r], fill=mix(BG, CRUST, a), outline=mix(BG, CRUST_D, a), width=max(3, r//48))
    ri = r*0.855
    d.ellipse([x-ri, y-ri, x+ri, y+ri], fill=mix(BG, CHEESE, a))
    pr = max(5, int(r*0.108))
    for i, (t, rad) in enumerate(PEPS[:n_pep]):
        ang = t*2*math.pi
        px = x+math.cos(ang)*rad*ri*0.86
        py = y+math.sin(ang)*rad*ri*0.86
        d.ellipse([px-pr, py-pr, px+pr, py+pr], fill=mix(BG, PEP, a), outline=mix(BG, PEP_D, a), width=2)


def arrow2(d, p0, p1, col, a, width=5, head=15):
    """Double-headed measurement arrow."""
    if a <= 0.004: return
    c = mix(BG, col, a)
    d.line([p0, p1], fill=c, width=width)
    for (tip, other) in ((p1, p0), (p0, p1)):
        ang = math.atan2(tip[1]-other[1], tip[0]-other[0])
        for s in (-0.42, 0.42):
            d.line([tip, (tip[0]-head*math.cos(ang+s), tip[1]-head*math.sin(ang+s))], fill=c, width=width)


def pizza_partial(img, d, c, r, a, frac_y):
    """The big pizza as an empty crust ring, filled with pizza only below frac_y.
    Reads as 'this much of the pan is covered', which is what pouring the smalls in does."""
    x, y = c
    d.ellipse([x-r, y-r, x+r, y+r], outline=mix(BG, CRUST_D, a), width=max(4, r//40))
    if frac_y is None: return d
    lay = Image.new("RGB", (W, H), BG)
    ld = ImageDraw.Draw(lay)
    pizza(ld, c, r, a)
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rectangle([0, int(frac_y), W, H], fill=255)
    img.paste(lay, (0, 0), m)
    d2 = ImageDraw.Draw(img)
    d2.ellipse([x-r, y-r, x+r, y+r], outline=mix(BG, CRUST_D, a), width=max(4, r//40))
    return d2


def render(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ================= hook   L0 0.30-4.67
    if t < 5.15:
        a = ease(seg(t, 0.0, 0.32))*(1-ease(seg(t, 4.75, 5.15)))
        pizza(d, (W//2, 640), 190, ease(seg(t, 0.30, 0.90))*a)
        pizza(d, (W//2-150, 1010), 127, ease(seg(t, 1.10, 1.70))*a, n_pep=6)
        pizza(d, (W//2+150, 1010), 127, ease(seg(t, 1.10, 1.70))*a, n_pep=6)
        text(d, (W//2, 1250), "one 18 inch", disp(74), INK, alpha=ease(seg(t, 2.20, 2.70))*a)
        text(d, (W//2, 1350), "beats two 12 inch", disp(74), GREEN, alpha=ease(seg(t, 3.00, 3.50))*a)

    # ================= measured across   L1 - L2
    if 5.0 < t < 12.1:
        fo = 1-ease(seg(t, 11.60, 12.05))
        pa = ease(seg(t, 5.20, 5.80))*fo
        pizza(d, BIG, R_BIG, pa)
        sp = ease(seg(t, 5.90, 6.50))*fo
        pizza(d, SML_L, R_SML, sp, n_pep=6)
        pizza(d, SML_R, R_SML, sp, n_pep=6)
        # the diameter arrow sits below each pizza, never across it
        da = ease(seg(t, 6.60, 7.10))*fo
        ay = BIG[1]+R_BIG+38
        arrow2(d, (BIG[0]-R_BIG, ay), (BIG[0]+R_BIG, ay), INK, da)
        text(d, (BIG[0], ay+40), "18 inches across", disp(50), INK, alpha=da)
        sa2 = ease(seg(t, 8.00, 8.50))*fo
        for C in (SML_L, SML_R):
            y2 = C[1]+R_SML+30
            arrow2(d, (C[0]-R_SML, y2), (C[0]+R_SML, y2), INK, sa2, width=4, head=11)
            text(d, (C[0], y2+34), "12", disp(44), INK, alpha=sa2)
        # L2, the belief being struck. words, not a symbol nobody reads.
        sa = ease(seg(t, 9.20, 9.70))*fo
        text(d, (W//2, TOP_Y), "area follows the diameter", disp(60), DIM, alpha=sa)
        p = ease_out(seg(t, 10.30, 10.85))
        if p > 0 and sa > 0.01:
            wd, _ = measure(d, "area follows the diameter", disp(60))
            d.line([W//2-wd//2-20, TOP_Y, W//2-wd//2-20+(wd+40)*p, TOP_Y],
                   fill=mix(BG, RED, sa), width=10)

    # ================= what proportional means   L3 - L4
    if 12.0 < t < 21.3:
        fo = 1-ease(seg(t, 20.80, 21.25))
        text(d, (W//2, 330), "proportional means", grot(50, "Medium"), DIM,
             alpha=ease(seg(t, 12.20, 12.70))*fo)
        text(d, (W//2, 425), "double one, the other doubles", disp(56), INK,
             alpha=ease(seg(t, 12.90, 13.40))*fo)
        text(d, (W//2, 545), "area does not do that", disp(56), RED,
             alpha=ease(seg(t, 14.60, 15.10))*fo)
        # one pizza, then double the width, then the four that equal it.
        # laid out from measured widths so the row is centred and the gaps match.
        r1, gap, eqw = 62, 60, 40
        total = 2*r1 + gap + 4*r1 + gap + eqw + gap + 4*r1
        x0 = (W-total)//2
        ax = x0+r1
        bx = x0+2*r1+gap+2*r1
        ex = (x0+2*r1+gap+4*r1 + x0+2*r1+gap+4*r1+gap+eqw+gap)//2 + 2   # midpoint of the
        # rendered gap; the +2 accounts for the pizza outline stroke on the right group
        cx = x0+2*r1+gap+4*r1+gap+eqw+gap+2*r1
        ROW_Y = 900
        a1 = ease(seg(t, 16.10, 16.60))*fo
        pizza(d, (ax, ROW_Y), r1, a1, n_pep=4)
        text(d, (ax, ROW_Y+r1+52), "width 1", grot(36, "Bold"), DIM, alpha=a1)
        a2 = ease(seg(t, 17.30, 17.90))*fo
        pizza(d, (bx, ROW_Y), 2*r1, a2)
        text(d, (bx, ROW_Y+2*r1+52), "width 2", grot(36, "Bold"), DIM, alpha=a2)
        a3 = ease(seg(t, 18.80, 19.40))*fo
        text(d, (ex, ROW_Y), "=", disp(66), DIM, alpha=a3)
        for dx, dy in ((-r1, -r1), (r1, -r1), (-r1, r1), (r1, r1)):
            pizza(d, (cx+dx, ROW_Y+dy), r1, a3, n_pep=3)
        text(d, (cx, ROW_Y+2*r1+52), "four of them", grot(36, "Bold"), DIM, alpha=a3)
        text(d, (W//2, CAP_Y), "double the width, four times the pizza",
             grot(46, "Medium"), CORAL_I, alpha=ease(seg(t, 19.60, 20.10))*fo)

    # ================= radius, then areas   L5 - L8
    if 21.2 < t < 39.9:
        fo = (1-ease(seg(t, 39.40, 39.85)))*ease(seg(t, 21.35, 21.85))
        text(d, (W//2, TOP_Y), "area follows the radius, squared", disp(56), GREEN,
             alpha=ease(seg(t, 21.60, 22.10))*fo)
        pizza(d, BIG, R_BIG, fo)
        pizza(d, SML_L, R_SML, fo, n_pep=6)
        pizza(d, SML_R, R_SML, fo, n_pep=6)
        ra = ease(seg(t, 24.30, 24.80))*(1-ease(seg(t, 30.20, 30.65)))*fo
        if ra > 0.004:
            d.line([BIG, (BIG[0]+R_BIG, BIG[1])], fill=mix(BG, BLUE, ra), width=7)
            d.ellipse([BIG[0]-10, BIG[1]-10, BIG[0]+10, BIG[1]+10], fill=mix(BG, BLUE, ra))
            text(d, (BIG[0]+R_BIG//2, BIG[1]-46), "9", disp(58), BLUE, alpha=ra)
        rs = ease(seg(t, 27.10, 27.60))*(1-ease(seg(t, 30.20, 30.65)))*fo
        if rs > 0.004:
            for C in (SML_L, SML_R):
                d.line([C, (C[0]+R_SML, C[1])], fill=mix(BG, BLUE, rs), width=5)
                text(d, (C[0]+R_SML//2, C[1]-38), "6", disp(46), BLUE, alpha=rs)
        text(d, (W//2, CAP_Y), "the radius is half the diameter", grot(46, "Medium"), DIM,
             alpha=ease(seg(t, 25.30, 25.80))*(1-ease(seg(t, 28.60, 29.00)))*fo)
        text(d, (W//2, CAP_Y), "nine, and six", grot(48, "Medium"), BLUE,
             alpha=ease(seg(t, 29.10, 29.55))*(1-ease(seg(t, 30.20, 30.65)))*fo)
        # areas printed beside each pizza, never on top of the pepperoni
        text(d, (W//2, CAP_Y), "area = π r²", disp(64), INK,
             alpha=ease(seg(t, 30.80, 31.30))*(1-ease(seg(t, 34.40, 34.85)))*fo)
        text(d, (BIG[0]+R_BIG+58, BIG[1]), "81π", disp(74), GREEN, anchor="lm",
             alpha=ease(seg(t, 32.30, 32.80))*fo)
        a36 = ease(seg(t, 35.10, 35.60))*fo
        text(d, (SML_L[0]-R_SML-26, SML_L[1]), "36π", disp(48), CRUST_D, anchor="rm", alpha=a36)
        text(d, (SML_R[0]+R_SML+26, SML_R[1]), "36π", disp(48), CRUST_D, anchor="lm", alpha=a36)
        text(d, (W//2, CAP_Y), "two smalls make only 72π", grot(48, "Medium"), CORAL_I,
             alpha=ease(seg(t, 37.00, 37.50))*fo)

    # ================= the pour   L9 - L11
    F0, F1 = 53.20, 53.80
    if 39.8 < t < F1+0.2:
        fo = ease(seg(t, 39.95, 40.45))*(1-ease(seg(t, F0, F1)))
        pour = ease(seg(t, 40.40, 42.40))
        y_end = BIG[1]-R_BIG+POUR_PX
        fill_y = BIG[1]+R_BIG-(BIG[1]+R_BIG-y_end)*pour if pour > 0.003 else None
        d = pizza_partial(img, d, BIG, R_BIG, fo, fill_y)
        if pour > 0.97:
            d.line([BIG[0]-R_BIG+16, y_end, BIG[0]+R_BIG-16, y_end],
                   fill=mix(BG, RED, fo), width=4)
        sa = (1-pour)*fo
        pizza(d, SML_L, R_SML, sa, n_pep=6)
        pizza(d, SML_R, R_SML, sa, n_pep=6)
        text(d, (W//2, CAP_Y), "pour both smalls in", grot(48, "Medium"), DIM,
             alpha=ease(seg(t, 40.05, 40.55))*(1-ease(seg(t, 42.70, 43.15))))
        text(d, (W//2, TOP_Y), "it still does not fill", disp(66), INK,
             alpha=ease(seg(t, 42.10, 42.60))*(1-ease(seg(t, F0, F1))))
        ca = ease(seg(t, 43.50, 44.00))*(1-ease(seg(t, F0, F1)))
        if ca > 0.004:
            crest_y = BIG[1]-R_BIG+POUR_PX//2
            d.line([(BIG[0]+R_BIG-20, crest_y), (BIG[0]+R_BIG+70, 990)],
                   fill=mix(BG, RED, ca), width=3)
            text(d, (BIG[0]+R_BIG+72, 1024), "9π short", disp(50), RED, anchor="mm", alpha=ca)
        text(d, (W//2, CAP_Y), "exactly one ninth of the big one", grot(46, "Medium"), CORAL_I,
             alpha=ease(seg(t, 44.80, 45.30))*(1-ease(seg(t, 48.60, 49.05))))
        text(d, (W//2, 1180), "81π  vs  72π", disp(60), GREEN,
             alpha=ease(seg(t, 46.60, 47.10))*(1-ease(seg(t, F0, F1))))
        text(d, (W//2, CAP_Y), "1.5² = 2.25", disp(62), INK,
             alpha=ease(seg(t, 49.40, 49.90))*(1-ease(seg(t, F0, F1))))
        text(d, (W//2, 1268), "one big = 2.25 smalls", grot(44, "Medium"), DIM,
             alpha=ease(seg(t, 51.10, 51.60))*(1-ease(seg(t, F0, F1))))

    # ================= endcard   L12 53.82-56.42
    if t > 53.7:
        text(d, (W//2, 760), "Width grew by half.", disp(78), INK, alpha=ease(seg(t, 53.90, 54.40)))
        text(d, (W//2, 872), "Area squares that.", disp(78), GREEN, alpha=ease(seg(t, 54.70, 55.20)))
        text(d, (W//2, 1010), "one big = 2.25 smalls", ser(56), DIM, alpha=ease(seg(t, 55.50, 56.00)))
        text(d, (W//2, 1200), "quanticaedu.com", disp(62), GREEN, alpha=ease(seg(t, 56.30, 56.80)))
        text(d, (W//2, 1278), "prealgebra 11.7, free", sans(40), DIM, alpha=ease(seg(t, 56.85, 57.35)))
    brand(img, d)
    return img


DUR = 58.6

if __name__ == "__main__":
    import sys
    from fractions import Fraction as F
    assert F(9)**2 == 81 and F(6)**2 == 36 and 2*36 == 72 and 81-72 == 9
    assert F(9, 81) == F(1, 9) and F(3, 2)**2 == F(9, 4) and F(9, 4)*36 == 81
    assert F(2, 1)**2 == 4          # double the width, four times the area
    print("  check: 81pi vs 72pi, gap 9pi = 1/9, 1.5^2 = 2.25, 2^2 = 4")
    if "--check" in sys.argv:
        w, bad = dead_air(render, DUR)
        print(f"  duration {DUR}s | worst static {w}s | over-2.5s: {bad or 'none'}")
    else:
        render_all(render, DUR, os.path.join(OUT, "quantica-02-pizza.mp4"), FR)
