"""
Quantica short #6  "PEMDAS taught you to multiply before you divide. That rule doesn't exist."

  48 / 2 x 3   worked left to right   = 72
  multiplying first would give        = 8
Multiplication and division are one rank, because dividing by 2 is multiplying by 1/2.
Same for addition and subtraction. Six letters, four levels.
"""
import os
from PIL import Image, ImageDraw
from qkit import *
from render import grot, LIME, LIME_I, AMBER, AMBER_I, CORAL, CORAL_I

OUT = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(OUT, "frames6")

LETTERS = ["P", "E", "M", "D", "A", "S"]


def render(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ============ hook   L0 0.30-2.62, L1 3.04-5.36
    if t < 5.85:
        a = ease(seg(t, 0.0, 0.32))*(1-ease(seg(t, 5.45, 5.85)))
        text(d, (W//2, 720), "48 ÷ 2 × 3", disp(118), INK, alpha=ease(seg(t, 0.30, 0.75))*a)
        a2 = ease(seg(t, 3.15, 3.55))*a
        text(d, (W//2, 900), "8", disp(110), DIM, alpha=a2)
        p = ease_out(seg(t, 4.05, 4.55))
        if p > 0:
            wd, _ = measure(d, "8", disp(110))
            d.line([W//2-wd//2-30, 900, W//2-wd//2-30+(wd+60)*p, 900],
                   fill=mix(BG, RED, a), width=12)
        text(d, (W//2, 1070), "PEMDAS lied to you", grot(52, "Medium"), RED,
             alpha=ease(seg(t, 4.70, 5.15))*a)

    # ============ the letters, then the merge   L2 - L4
    F0, F1 = 16.40, 17.00
    if 5.7 < t < F1+0.2:
        fo = 1-ease(seg(t, F0, F1))
        # six letters across, then M+D and A+S each pull into one tile
        merge = ease(seg(t, 10.20, 11.60))          # L3 "not two ranks, they are one"
        f = disp(78)
        xs = [W//2-430+i*172 for i in range(6)]
        pairs = {2: 3, 4: 5}                        # M<-D, A<-S
        for i, L in enumerate(LETTERS):
            aa = ease(seg(t, 5.95+i*0.28, 6.30+i*0.28))*fo
            x = xs[i]
            if i in (3, 5):                          # D and S slide onto their partner
                x = xs[i]+(xs[i-1]-xs[i])*merge
                aa *= (1-merge*0.55)
            elif i in (2, 4):
                x = xs[i]+(xs[i+1]-xs[i])*merge*0.5
            col = INK
            if merge > 0.05 and i in (2, 3): col = mix(INK, LIME_I, merge)
            if merge > 0.05 and i in (4, 5): col = mix(INK, AMBER_I, merge)
            text(d, (x, 700), L, f, col, alpha=aa)
        text(d, (W//2, 830), "six letters, so six steps?", grot(46, "Medium"), DIM,
             alpha=ease(seg(t, 8.00, 8.50))*(1-ease(seg(t, 10.10, 10.60)))*fo)   # L2
        text(d, (W//2, 830), "M and D are one rank. A and S are one rank.",
             grot(44, "Medium"), CORAL_I,
             alpha=ease(seg(t, 11.30, 11.80))*fo)                                # L3
        # L4, the reason
        text(d, (W//2, 1010), "÷ 2   is   × ½", disp(80), INK,
             alpha=ease(seg(t, 13.25, 13.75))*fo)
        text(d, (W//2, 1140), "same operation, written twice",
             grot(44, "Medium"), DIM,
             alpha=ease(seg(t, 14.60, 15.10))*fo)

    # ============ worked left to right   L5 - L7
    if 16.8 < t < 25.9:
        fo = 1-ease(seg(t, 25.40, 25.85))
        text(d, (W//2, 620), "left to right", disp(72), INK,
             alpha=ease(seg(t, 17.00, 17.50))*fo)                                # L5
        text(d, (W//2, 800), "48 ÷ 2 = 24", disp(84), INK,
             alpha=ease(seg(t, 18.60, 19.10))*fo)
        text(d, (W//2, 930), "24 × 3 = 72", disp(84), GREEN,
             alpha=ease(seg(t, 21.00, 21.50))*fo)                                # L6
        text(d, (W//2, 1120), "10 - 3 + 2 = 9,  not 5", disp(62), AMBER_I,
             alpha=ease(seg(t, 23.55, 24.05))*fo)                                # L7
        text(d, (W//2, 1240), "plus and minus work the same way",
             grot(44, "Medium"), DIM,
             alpha=ease(seg(t, 24.20, 24.70))*fo)

    # ============ endcard   L8 25.67-27.11
    if t > 25.8:
        text(d, (W//2, 780), "Four levels.", disp(90), INK,
             alpha=ease(seg(t, 25.95, 26.45)))
        text(d, (W//2, 900), "Not six.", disp(90), GREEN,
             alpha=ease(seg(t, 26.70, 27.20)))
        text(d, (W//2, 1050), "grouping, powers,\nthen × ÷, then + −", ser(52), DIM,
             alpha=ease(seg(t, 27.60, 28.10)), spacing=16)
        text(d, (W//2, 1240), "quanticaedu.com", disp(62), GREEN,
             alpha=ease(seg(t, 28.80, 29.30)))
        text(d, (W//2, 1318), "algebra I 1.2, free", sans(40), DIM,
             alpha=ease(seg(t, 29.35, 29.85)))
    brand(img, d)
    return img


DUR = 31.8

if __name__ == "__main__":
    import sys
    assert 48/2*3 == 72 and 48/(2*3) == 8 and 10-3+2 == 9
    print("  check: 48/2x3 = 72 left to right, 8 if you multiply first, 10-3+2 = 9")
    if "--check" in sys.argv:
        w, bad = dead_air(render, DUR)
        print(f"  duration {DUR}s | worst static {w}s | over-2.5s: {bad or 'none'}")
    else:
        render_all(render, DUR, os.path.join(OUT, "quantica-06-pemdas.mp4"), FR)
