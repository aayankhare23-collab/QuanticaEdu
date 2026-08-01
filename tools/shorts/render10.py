"""
Quantica short #10  "A 20% pay cut takes a 25% raise to undo"

  50000 -> 40000 after the cut.
  a 20% raise on 40000 gives 48000, still short.
  you need 10000 back on top of 40000, and 10000/40000 = 25% exactly.
  0.8 x 1.25 = 1.
"""
import os
from PIL import Image, ImageDraw
from qkit import *
from render import grot, LIME, LIME_I, AMBER, AMBER_I, CORAL, CORAL_I

OUT = os.path.dirname(os.path.abspath(__file__)); FR = os.path.join(OUT, "frames10")

BX, BW, BH = 150, 760, 92      # 760px represents 50k
ROWS = [720, 880, 1040]


def bar(d, y, k, p, col, ink, lab, alpha):
    if alpha <= 0.003: return
    w = BW*k/50*clamp(p)
    if w > 4:
        d.rounded_rectangle([BX, y, BX+w, y+BH], 10, fill=mix(BG, col, alpha),
                            outline=mix(BG, ink, alpha), width=4)
    if p > 0.97:
        text(d, (BX+w+24, y+BH//2), lab, disp(50), ink, anchor="lm", alpha=alpha)


def render(t):
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)

    # hook  L0 0.30-4.20, L1 4.62-5.36
    if t < 5.80:
        a = ease(seg(t, 0.0, 0.32))*(1-ease(seg(t, 5.40, 5.80)))
        text(d, (W//2, 680), "A 20% pay cut", disp(96), INK, alpha=ease(seg(t, 0.30, 0.75))*a)
        text(d, (W//2, 800), "needs a 25% raise", disp(96), GREEN, alpha=ease(seg(t, 1.90, 2.40))*a)
        text(d, (W//2, 920), "to undo.", disp(96), GREEN, alpha=ease(seg(t, 3.00, 3.45))*a)
        a2 = ease(seg(t, 4.70, 5.10))*a
        text(d, (W//2, 1090), "not 20%", disp(76), RED, alpha=a2)

    # the pay bars  L2 - L7
    F0, F1 = 22.80, 23.35
    if 5.6 < t < F1+0.2:
        fo = 1-ease(seg(t, F0, F1))
        bar(d, ROWS[0], 50, seg(t, 5.95, 6.60), LINE, INK, "50k", ease(seg(t, 5.90, 6.40))*fo)
        bar(d, ROWS[1], 40, seg(t, 8.10, 8.80), CORAL, CORAL_I, "40k", ease(seg(t, 8.05, 8.55))*fo)
        text(d, (W//2, 1240), "the cut takes 10k", grot(46, "Medium"), CORAL_I,
             alpha=ease(seg(t, 9.30, 9.80))*(1-ease(seg(t, 11.50, 11.95)))*fo)   # L3

        # L4/L5, a 20% raise on the reduced number falls short
        bar(d, ROWS[2], 48, seg(t, 12.10, 12.85), AMBER, AMBER_I, "48k",
            ease(seg(t, 12.05, 12.55))*fo)
        text(d, (W//2, 1240), "20% of 40k is only 8k", grot(46, "Medium"), AMBER_I,
             alpha=ease(seg(t, 12.90, 13.40))*(1-ease(seg(t, 16.90, 17.35)))*fo)
        text(d, (W//2, 1360), "48k, still short", disp(60), RED,
             alpha=ease(seg(t, 15.30, 15.80))*(1-ease(seg(t, 16.90, 17.35)))*fo) # L5

        # L6/L7, what actually closes the gap
        text(d, (W//2, 1240), "you need 10k on top of 40k", grot(46, "Medium"), DIM,
             alpha=ease(seg(t, 17.55, 18.05))*fo)                                # L6
        ta = ease(seg(t, 19.10, 19.60))*fo
        if ta > 0.003:
            x0 = BX+BW*40//50
            x1 = BX+BW*50//50
            d.rounded_rectangle([x0, ROWS[1], x1, ROWS[1]+BH], 10,
                                fill=mix(BG, LIME, ta), outline=mix(BG, LIME_I, ta), width=4)
            text(d, ((x0+x1)//2, ROWS[1]-42), "+10k", grot(42, "Bold"), LIME_I, alpha=ta)
        text(d, (W//2, 1360), "10 ÷ 40 = 25%", disp(70), GREEN,
             alpha=ease(seg(t, 20.90, 21.40))*fo)                                # L7

    # endcard  L8 23.16-26.23
    if t > 23.3:
        text(d, (W//2, 760), "0.8 × 1.25 = 1", disp(92), GREEN, alpha=ease(seg(t, 23.50, 24.00)))
        text(d, (W//2, 910), "The cut and the raise", ser(58), DIM, alpha=ease(seg(t, 24.40, 24.90)))
        text(d, (W//2, 985), "measure different numbers.", ser(58), DIM, alpha=ease(seg(t, 25.00, 25.50)))
        text(d, (W//2, 1180), "quanticaedu.com", disp(62), GREEN, alpha=ease(seg(t, 26.40, 26.90)))
        text(d, (W//2, 1258), "prealgebra 9.3, free", sans(40), DIM, alpha=ease(seg(t, 26.95, 27.45)))
    brand(img, d); return img


DUR = 31.0

if __name__ == "__main__":
    import sys
    from fractions import Fraction as F
    assert F(8, 10)*F(125, 100) == 1
    assert 50000*F(8, 10) == 40000 and 40000*F(12, 10) == 48000
    assert F(10000, 40000) == F(1, 4)
    print("  check: 50k -> 40k, a 20% raise gives 48k, and 10/40 = 25%. 0.8 x 1.25 = 1")
    if "--check" in sys.argv:
        w, bad = dead_air(render, DUR); print(f"  {DUR}s | worst {w}s | over-2.5s: {bad or 'none'}")
    else:
        render_all(render, DUR, os.path.join(OUT, "quantica-10-paycut.mp4"), FR)
