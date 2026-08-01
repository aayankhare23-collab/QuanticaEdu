"""
Quantica short #8  "No square number ends in 7, and none ever will."

The last digit of n^2 depends only on the last digit of n, so ten cases settle every
integer there is. Endings that occur: 0 1 4 5 6 9. Never: 2 3 7 8.
The grid below is generated, not typed, so the picture cannot drift from the arithmetic.
"""
import os
from PIL import Image, ImageDraw
from qkit import *
from render import grot, LIME, LIME_I, AMBER, AMBER_I, CORAL, CORAL_I

OUT = os.path.dirname(os.path.abspath(__file__)); FR = os.path.join(OUT, "frames8")

SQ = [(n, n*n, (n*n) % 10) for n in range(10)]
HITS = sorted({e for _, _, e in SQ})
MISS = sorted(set(range(10))-set(HITS))
COLS, CW, GX, GY, RH = 5, 190, 70, 700, 130


def render(t):
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)

    # hook  L0 0.30-2.34, L1 2.76-3.88
    if t < 4.30:
        a = ease(seg(t, 0.0, 0.32))*(1-ease(seg(t, 3.90, 4.30)))
        text(d, (W//2, 720), "No square number", disp(84), INK, alpha=ease(seg(t, 0.30, 0.75))*a)
        text(d, (W//2, 830), "ends in 7.", disp(84), INK, alpha=ease(seg(t, 1.10, 1.55))*a)
        text(d, (W//2, 1000), "and none ever will", grot(52, "Medium"), RED,
             alpha=ease(seg(t, 2.90, 3.35))*a)

    # the ten cases  L2 - L7
    F0, F1 = 27.40, 27.95
    if 4.2 < t < F1+0.2:
        fo = 1-ease(seg(t, F0, F1))
        text(d, (W//2, 470), "the last digit is all that matters", grot(46, "Medium"), DIM,
             alpha=ease(seg(t, 4.50, 5.00))*(1-ease(seg(t, 11.20, 11.65)))*fo)    # L2
        # under L2, two numbers with the same last digit landing on the same ending
        ea = ease(seg(t, 5.90, 6.40))*(1-ease(seg(t, 11.20, 11.65)))*fo
        text(d, (W//2, 700), "13² = 169", disp(72), INK, alpha=ea)
        text(d, (W//2, 820), "123² = 15129", disp(72), INK,
             alpha=ease(seg(t, 7.10, 7.60))*(1-ease(seg(t, 11.20, 11.65)))*fo)
        text(d, (W//2, 950), "both end in 9", grot(50, "Medium"), GREEN,
             alpha=ease(seg(t, 8.00, 8.50))*(1-ease(seg(t, 11.20, 11.65)))*fo)
        text(d, (W//2, 470), "so only ten cases exist", grot(46, "Medium"), DIM,
             alpha=ease(seg(t, 9.30, 9.80))*(1-ease(seg(t, 11.20, 11.65)))*fo)    # L3

        # the grid, one square every 0.44s under L4 (11.45 - 16.28)
        for i, (n, sqr, e) in enumerate(SQ):
            aa = ease(seg(t, 11.50+i*0.44, 11.85+i*0.44))*fo
            if aa <= 0.003: continue
            cx = GX+CW//2+(i % COLS)*CW
            cy = GY+(i//COLS)*RH
            text(d, (cx, cy), f"{n}² = {sqr}", grot(44, "Bold"), INK, alpha=aa)
            hot = ease(seg(t, 19.45, 19.95))*fo
            col = mix(INK, GREEN, hot) if e in HITS else INK
            text(d, (cx, cy+52), f"ends {e}", sans(34), col, alpha=aa)

        # L5/L6 the endings that do occur
        text(d, (W//2, 1080), "endings a square can have", grot(46, "Medium"), DIM,
             alpha=ease(seg(t, 16.90, 17.40))*fo)
        text(d, (W//2, 1180), "  ".join(str(x) for x in HITS), disp(84), GREEN,
             alpha=ease(seg(t, 19.45, 19.95))*fo)                                 # L6
        # L7 the ones that never do
        ma = ease(seg(t, 22.00, 22.50))*fo
        text(d, (W//2, 1300), "  ".join(str(x) for x in MISS), disp(76), DIM, alpha=ma)
        p = ease_out(seg(t, 22.70, 23.30))
        if p > 0 and ma > 0.01:
            wd, _ = measure(d, "  ".join(str(x) for x in MISS), disp(76))
            d.line([W//2-wd//2-22, 1300, W//2-wd//2-22+(wd+44)*p, 1300],
                   fill=mix(BG, RED, ma), width=10)
        text(d, (W//2, 1400), "never, for any number at all", grot(44, "Medium"), RED,
             alpha=ease(seg(t, 24.50, 25.00))*fo)                                 # L8

    # endcard
    if t > 27.9:
        text(d, (W//2, 800), "Ten cases.", disp(90), INK, alpha=ease(seg(t, 28.10, 28.60)))
        text(d, (W//2, 920), "Every number covered.", disp(76), GREEN, alpha=ease(seg(t, 28.90, 29.40)))
        text(d, (W//2, 1140), "quanticaedu.com", disp(62), GREEN, alpha=ease(seg(t, 30.10, 30.60)))
        text(d, (W//2, 1218), "prealgebra 3.2, free", sans(40), DIM, alpha=ease(seg(t, 30.65, 31.15)))
    brand(img, d); return img


DUR = 32.0

if __name__ == "__main__":
    import sys
    assert HITS == [0, 1, 4, 5, 6, 9] and MISS == [2, 3, 7, 8]
    assert not any((n*n) % 10 == 7 for n in range(200000))
    print(f"  check: endings {HITS}, never {MISS}, brute forced to 200000")
    if "--check" in sys.argv:
        w, bad = dead_air(render, DUR); print(f"  {DUR}s | worst {w}s | over-2.5s: {bad or 'none'}")
    else:
        render_all(render, DUR, os.path.join(OUT, "quantica-08-squares.mp4"), FR)
