"""
Quantica short #5  "0.999... is not almost 1. It is 1."

The algebraic proof, laid out a line at a time:
    x  = 0.999...
  10x  = 9.999...
  10x - x = 9.999... - 0.999...   the tails cancel exactly
   9x  = 9
    x  = 1
Then the real reason. Two distinct reals always have a real strictly between them.
No such number can be named here, so there are not two numbers.
"""
import os
from PIL import Image, ImageDraw
from qkit import *
from render import grot, LIME, LIME_I, AMBER, AMBER_I, CORAL, CORAL_I

OUT = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(OUT, "frames5")

LX = 300                    # shared '=' column, so the proof aligns like real working
ROW = [720, 830, 960, 1070, 1180]


def eq(d, i, lhs, rhs, alpha, rhs_col=INK, f=None):
    if alpha <= 0.003: return
    f = f or disp(66)
    y = ROW[i]
    text(d, (LX, y), lhs, f, INK, anchor="rm", alpha=alpha)
    text(d, (LX+34, y), "=", f, DIM, anchor="mm", alpha=alpha)
    text(d, (LX+70, y), rhs, f, rhs_col, anchor="lm", alpha=alpha)


def render(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ============ hook   L0 0.30-2.90, L1 3.32-5.97
    if t < 6.45:
        a = ease(seg(t, 0.0, 0.32))*(1-ease(seg(t, 6.05, 6.45)))
        text(d, (W//2, 720), "0.999...", disp(126), INK, alpha=ease(seg(t, 0.30, 0.70))*a)
        text(d, (W//2, 880), "is not almost 1", disp(78), DIM, alpha=ease(seg(t, 1.30, 1.75))*a)
        text(d, (W//2, 1030), "it is 1", disp(110), GREEN, alpha=ease(seg(t, 3.45, 3.90))*a)
        text(d, (W//2, 1180), "same number, two spellings", grot(48, "Medium"), RED,
             alpha=ease(seg(t, 4.60, 5.05))*a)

    # ============ the proof   L2 - L5
    F0, F1 = 19.60, 20.20
    if 6.3 < t < F1+0.2:
        fo = 1-ease(seg(t, F0, F1))
        eq(d, 0, "x", "0.999...", ease(seg(t, 7.60, 8.10))*fo)                 # L2
        text(d, (W//2, 1310), "the nines never stop", grot(46, "Medium"), CORAL_I,
             alpha=ease(seg(t, 9.00, 9.50))*(1-ease(seg(t, 12.90, 13.35)))*fo)
        eq(d, 1, "10x", "9.999...", ease(seg(t, 10.65, 11.15))*fo)             # L3
        # L4, the subtraction, with the cancelling tails called out
        sa = ease(seg(t, 13.25, 13.75))*fo
        eq(d, 2, "10x - x", "9.999... - 0.999...", sa, f=disp(52))
        text(d, (W//2, 1265), "the tails cancel exactly", grot(44, "Medium"), CORAL_I,
             alpha=ease(seg(t, 14.60, 15.10))*(1-ease(seg(t, 17.00, 17.50)))*fo)
        eq(d, 3, "9x", "9", ease(seg(t, 15.60, 16.10))*fo)
        eq(d, 4, "x", "1", ease(seg(t, 17.10, 17.60))*fo, rhs_col=GREEN)       # L5

    # ============ the real reason   L6 - L8
    if 19.9 < t < 29.4:
        fo = 1-ease(seg(t, 28.90, 29.35))
        text(d, (W//2, 630), "two different numbers", disp(70), INK,
             alpha=ease(seg(t, 20.10, 20.60))*fo)
        text(d, (W//2, 735), "always have one in between", disp(64), INK,
             alpha=ease(seg(t, 21.40, 21.90))*fo)                              # L6
        # the number line, with nothing to put in the gap
        la = ease(seg(t, 22.60, 23.10))*fo
        if la > 0.003:
            y = 930
            d.line([220, y, 860, y], fill=mix(BG, INK, la), width=5)
            for x, lab in ((300, "0.999..."), (780, "1")):
                d.ellipse([x-13, y-13, x+13, y+13], fill=mix(BG, GREEN, la))
                text(d, (x, y+64), lab, grot(40, "Bold"), INK, alpha=la)
            text(d, (540, y-70), "?", disp(80), CORAL_I,
                 alpha=ease(seg(t, 24.15, 24.65))*fo)                          # L7
        text(d, (W//2, 1150), "name it. you can't.", disp(72), CORAL_I,
             alpha=ease(seg(t, 24.70, 25.20))*fo)
        text(d, (W//2, 1290), "no gap, so not two numbers", grot(48, "Medium"), GREEN,
             alpha=ease(seg(t, 26.10, 26.60))*fo)                              # L8

    # ============ endcard
    if t > 29.4:
        text(d, (W//2, 820), "0.999... = 1", disp(104), GREEN,
             alpha=ease(seg(t, 29.60, 30.10)))
        text(d, (W//2, 960), "Not close. Equal.", ser(62), DIM,
             alpha=ease(seg(t, 30.50, 31.00)))
        text(d, (W//2, 1180), "quanticaedu.com", disp(62), GREEN,
             alpha=ease(seg(t, 31.50, 32.00)))
        text(d, (W//2, 1258), "prealgebra 5.5, free", sans(40), DIM,
             alpha=ease(seg(t, 32.05, 32.55)))
    brand(img, d)
    return img


DUR = 33.4

if __name__ == "__main__":
    import sys
    from fractions import Fraction as F
    assert F(1, 3)*3 == 1 and F(9, 9) == 1
    print("  check: 1/3 x 3 = 1, and 9x = 9 gives x = 1")
    if "--check" in sys.argv:
        w, bad = dead_air(render, DUR)
        print(f"  duration {DUR}s | worst static {w}s | over-2.5s: {bad or 'none'}")
    else:
        render_all(render, DUR, os.path.join(OUT, "quantica-05-repeating.mp4"), FR)
