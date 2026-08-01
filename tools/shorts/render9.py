"""
Quantica short #9  "Down 20% then up 20% leaves you down 4%"

  100 -> 80 -> 96.   0.8 x 1.2 = 0.96 exactly, and 1.2 x 0.8 is the same, so order
  does not matter. The rise is 16, not 20, because it grew from 80 rather than 100.
"""
import os
from PIL import Image, ImageDraw
from qkit import *
from render import grot, LIME, LIME_I, AMBER, AMBER_I, CORAL, CORAL_I

OUT = os.path.dirname(os.path.abspath(__file__)); FR = os.path.join(OUT, "frames9")

BX, BW, BH = 150, 780, 96      # 780px represents 100
Y1, Y2, Y3 = 700, 870, 1040


def bar(d, y, val, p, col, ink, lab, alpha):
    if alpha <= 0.003: return
    w = BW*val/100*clamp(p)
    if w > 4:
        d.rounded_rectangle([BX, y, BX+w, y+BH], 10, fill=mix(BG, col, alpha),
                            outline=mix(BG, ink, alpha), width=4)
    if p > 0.97:
        text(d, (BX+w+26, y+BH//2), lab, disp(56), ink, anchor="lm", alpha=alpha)


def render(t):
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)

    # hook  L0 0.30-2.67, L1 3.09-5.04
    if t < 5.45:
        a = ease(seg(t, 0.0, 0.32))*(1-ease(seg(t, 5.05, 5.45)))
        text(d, (W//2, 700), "Down 20%", disp(104), INK, alpha=ease(seg(t, 0.30, 0.75))*a)
        text(d, (W//2, 830), "then up 20%", disp(104), INK, alpha=ease(seg(t, 1.30, 1.75))*a)
        text(d, (W//2, 1020), "you are not back", grot(52, "Medium"), RED,
             alpha=ease(seg(t, 3.25, 3.70))*a)

    # the three bars  L2 - L6
    F0, F1 = 21.40, 21.95
    if 5.3 < t < F1+0.2:
        fo = 1-ease(seg(t, F0, F1))
        bar(d, Y1, 100, seg(t, 5.60, 6.30), LINE, INK, "100", ease(seg(t, 5.55, 6.05))*fo)
        bar(d, Y2, 80, seg(t, 6.90, 7.60), AMBER, AMBER_I, "80", ease(seg(t, 6.85, 7.35))*fo)
        text(d, (W//2, 1240), "20% off 100 is 20", grot(46, "Medium"), AMBER_I,
             alpha=ease(seg(t, 7.10, 7.60))*(1-ease(seg(t, 10.10, 10.55)))*fo)   # L2

        text(d, (W//2, 1360), "now add 20% of 80, not of 100", grot(44, "Medium"), CORAL_I,
             alpha=ease(seg(t, 8.60, 9.10))*(1-ease(seg(t, 10.10, 10.55)))*fo)

        # L3/L4, the rise measured against 80
        text(d, (W//2, 1240), "20% of 80 is 16, not 20", grot(48, "Medium"), CORAL_I,
             alpha=ease(seg(t, 10.45, 10.95))*(1-ease(seg(t, 13.90, 14.35)))*fo)
        bar(d, Y3, 96, seg(t, 12.35, 13.10), LIME, LIME_I, "96", ease(seg(t, 12.30, 12.80))*fo)
        text(d, (W//2, 1240), "4% down", disp(76), RED,
             alpha=ease(seg(t, 14.20, 14.70))*(1-ease(seg(t, 18.90, 19.35)))*fo) # L6

        # L7 why, L8 order does not matter
        text(d, (W//2, 1360), "the rise grew from a smaller number",
             grot(44, "Medium"), DIM,
             alpha=ease(seg(t, 15.95, 16.45))*(1-ease(seg(t, 18.90, 19.35)))*fo)
        text(d, (W//2, 1240), "0.8 × 1.2 = 0.96", disp(70), INK,
             alpha=ease(seg(t, 19.40, 19.90))*fo)
        text(d, (W//2, 1360), "1.2 × 0.8 = 0.96 too", grot(46, "Medium"), GREEN,
             alpha=ease(seg(t, 20.30, 20.80))*fo)                                # L8

    # endcard
    if t > 21.9:
        text(d, (W//2, 800), "Percent changes", disp(84), INK, alpha=ease(seg(t, 22.10, 22.60)))
        text(d, (W//2, 910), "multiply.", disp(84), GREEN, alpha=ease(seg(t, 22.85, 23.35)))
        text(d, (W//2, 1050), "They never cancel.", ser(58), DIM, alpha=ease(seg(t, 23.70, 24.20)))
        text(d, (W//2, 1230), "quanticaedu.com", disp(62), GREEN, alpha=ease(seg(t, 24.80, 25.30)))
        text(d, (W//2, 1308), "prealgebra 9.3, free", sans(40), DIM, alpha=ease(seg(t, 25.35, 25.85)))
    brand(img, d); return img


DUR = 26.6

if __name__ == "__main__":
    import sys
    from fractions import Fraction as F
    assert F(8, 10)*F(12, 10) == F(96, 100) == F(12, 10)*F(8, 10)
    assert 100*F(8, 10) == 80 and 80*F(12, 10) == 96
    print("  check: 100 -> 80 -> 96, and 0.8x1.2 = 1.2x0.8 = 0.96")
    if "--check" in sys.argv:
        w, bad = dead_air(render, DUR); print(f"  {DUR}s | worst {w}s | over-2.5s: {bad or 'none'}")
    else:
        render_all(render, DUR, os.path.join(OUT, "quantica-09-down20up20.mp4"), FR)
