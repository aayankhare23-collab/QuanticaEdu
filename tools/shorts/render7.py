"""
Quantica short #7  "(2x)^3 is not 2x^3"

  (2x)^3 = 2x . 2x . 2x = (2.2.2)(x.x.x) = 8x^3
Writing 2x^3 puts a 2 where an 8 belongs, so the answer comes out 4 times too small.
  at x = 5:  (2.5)^3 = 1000   but   2.5^3 = 250
"""
import os
from PIL import Image, ImageDraw
from qkit import *
from render import grot, LIME, LIME_I, AMBER, AMBER_I, CORAL, CORAL_I

OUT = os.path.dirname(os.path.abspath(__file__)); FR = os.path.join(OUT, "frames7")


def render(t):
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)

    # hook  L0 0.30-3.27, L1 3.69-6.76
    if t < 7.15:
        a = ease(seg(t, 0.0, 0.32))*(1-ease(seg(t, 6.75, 7.15)))
        text(d, (W//2, 660), "(2x)³", disp(140), INK, alpha=ease(seg(t, 0.30, 0.75))*a)
        text(d, (W//2, 860), "2x³", disp(110), DIM, alpha=ease(seg(t, 1.90, 2.35))*a)
        p = ease_out(seg(t, 3.85, 4.40))
        if p > 0:
            wd, _ = measure(d, "2x³", disp(110))
            d.line([W//2-wd//2-28, 860, W//2-wd//2-28+(wd+56)*p, 860],
                   fill=mix(BG, RED, a), width=12)
        text(d, (W//2, 1040), "the cube lands on the 2 as well",
             grot(48, "Medium"), RED, alpha=ease(seg(t, 5.10, 5.55))*a)

    # the expansion  L2 - L4
    F0, F1 = 16.20, 16.75
    if 7.0 < t < F1+0.2:
        fo = 1-ease(seg(t, F0, F1))
        # L2 names three copies, so bring them in one at a time
        f2 = disp(86)
        parts = ["2x", " · ", "2x", " · ", "2x"]
        ts2 = [7.40, 8.30, 8.45, 9.35, 9.50]
        ws = [measure(d, p, f2)[0] for p in parts]
        x0 = W//2-sum(ws)//2
        for p, t0, wd in zip(parts, ts2, ws):
            text(d, (x0+wd//2, 620), p, f2, INK, alpha=ease(seg(t, t0, t0+0.35))*fo)
            x0 += wd
        text(d, (W//2, 790), "(2 · 2 · 2)", disp(76), LIME_I,
             alpha=ease(seg(t, 11.05, 11.55))*fo)                    # L3
        text(d, (W//2, 900), "(x · x · x)", disp(76), BLUE,
             alpha=ease(seg(t, 12.40, 12.90))*fo)
        text(d, (W//2, 1080), "8", disp(96), LIME_I,
             alpha=ease(seg(t, 13.20, 13.70))*fo)
        text(d, (W//2, 1250), "8x³", disp(120), GREEN,
             alpha=ease(seg(t, 14.70, 15.20))*fo)                    # L4

    # the check at x = 5   L5 - L8
    if 16.6 < t < 30.0:
        fo = 1-ease(seg(t, 29.50, 29.95))
        text(d, (W//2, 560), "put x = 5", disp(78), INK,
             alpha=ease(seg(t, 16.90, 17.40))*fo)                    # L5
        text(d, (W//2, 760), "(2 · 5)³  =  10³", disp(64), LIME_I,
             alpha=ease(seg(t, 19.40, 19.90))*(1-ease(seg(t, 21.30, 21.60)))*fo)   # L6
        text(d, (W//2, 760), "(2 · 5)³  =  10³  =  1000", disp(64), LIME_I,
             alpha=ease(seg(t, 21.50, 22.00))*fo)
        text(d, (W//2, 900), "2 · 5³  =  2 · 125  =  250", disp(64), CORAL_I,
             alpha=ease(seg(t, 23.25, 23.75))*fo)                    # L7
        ba = ease(seg(t, 25.10, 25.60))*fo
        if ba > 0.003:
            d.rounded_rectangle([300, 1020, 780, 1140], 14,
                                fill=mix(BG, CORAL, ba*0.5), outline=mix(BG, CORAL_I, ba), width=4)
            text(d, (540, 1080), "4 times too small", grot(46, "Bold"), CORAL_I, alpha=ba)
        text(d, (W//2, 1250), "the 2 never got cubed", grot(48, "Medium"), RED,
             alpha=ease(seg(t, 26.80, 27.30))*fo)                    # L8

    # endcard
    if t > 30.0:
        text(d, (W//2, 800), "An exponent outside", disp(76), INK, alpha=ease(seg(t, 30.20, 30.70)))
        text(d, (W//2, 900), "hits everything inside.", disp(76), GREEN, alpha=ease(seg(t, 30.95, 31.45)))
        text(d, (W//2, 1120), "quanticaedu.com", disp(62), GREEN, alpha=ease(seg(t, 32.10, 32.60)))
        text(d, (W//2, 1198), "algebra I 1.5, free", sans(40), DIM, alpha=ease(seg(t, 32.65, 33.15)))
    brand(img, d); return img


DUR = 34.0

if __name__ == "__main__":
    import sys, sympy as sp
    x = sp.Symbol('x')
    assert sp.expand((2*x)**3) == 8*x**3 and (2*5)**3 == 1000 and 2*5**3 == 250
    assert (2*5)**3 // (2*5**3) == 4
    print("  check: (2x)^3 = 8x^3; at x=5, 1000 vs 250, ratio 4")
    if "--check" in sys.argv:
        w, bad = dead_air(render, DUR); print(f"  {DUR}s | worst {w}s | over-2.5s: {bad or 'none'}")
    else:
        render_all(render, DUR, os.path.join(OUT, "quantica-07-cube.mp4"), FR)
