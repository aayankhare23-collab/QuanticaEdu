"""
Quantica short #4  "Out at 30, back at 70. Your average speed is not 50."

210 miles each way, chosen so both legs are whole hours.
  out   210 / 30 = 7 hours
  back  210 / 70 = 3 hours
  total 420 miles in 10 hours = 42 mph exactly
The bars are drawn proportional to TIME, so the asymmetry is the argument.
"""
import os
from PIL import Image, ImageDraw
from qkit import *
from render import grot, LIME, LIME_I, AMBER, AMBER_I, CORAL, CORAL_I, bar_shadow

OUT = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(OUT, "frames4")

HOUR = 84                      # px per hour
BX = 150
Y_OUT, Y_BACK = 840, 1010
BH = 92


def leg(d, y, hours, p, col, ink, label, hrs_text, alpha, show_hours=True):
    """One journey leg. Bar length is time, not distance."""
    if alpha <= 0.003: return
    w = HOUR*hours*clamp(p)
    if w > 4:
        d.rounded_rectangle([BX, y, BX+w, y+BH], 10, fill=mix(BG, col, alpha),
                            outline=mix(BG, ink, alpha), width=4)
    text(d, (BX-18, y+BH//2), label, grot(40, "Bold"), ink, anchor="rm", alpha=alpha)
    if show_hours and p > 0.97:
        text(d, (BX+w+26, y+BH//2), hrs_text, disp(50), ink, anchor="lm", alpha=alpha)


def render(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ============ hook   L0 0.30-3.78, L1 4.20-6.25
    if t < 6.75:
        a = ease(seg(t, 0.0, 0.32))*(1-ease(seg(t, 6.35, 6.75)))
        text(d, (W//2, 700), "Out at 30.", disp(104), INK, alpha=ease(seg(t, 0.30, 0.70))*a)
        text(d, (W//2, 830), "Back at 70.", disp(104), INK, alpha=ease(seg(t, 1.60, 2.00))*a)
        a2 = ease(seg(t, 4.30, 4.70))*a
        text(d, (W//2, 1010), "average 50", disp(96), DIM, alpha=a2)
        p = ease_out(seg(t, 5.10, 5.60))
        if p > 0:
            wd, _ = measure(d, "average 50", disp(96))
            d.line([W//2-wd//2-24, 1010, W//2-wd//2-24+(wd+48)*p, 1010],
                   fill=mix(BG, RED, a), width=12)
        text(d, (W//2, 1170), "it is not 50", grot(50, "Medium"), RED,
             alpha=ease(seg(t, 5.75, 6.15))*a)

    # ============ the two legs   L2 - L7
    F0, F1 = 27.90, 28.50
    if 6.6 < t < F1+0.2:
        fo = 1-ease(seg(t, F0, F1))
        text(d, (W//2, 560), "210 miles each way", disp(72), INK,
             alpha=ease(seg(t, 6.80, 7.30))*(1-ease(seg(t, 21.90, 22.40)))*fo)

        # the round trip itself, under L2
        ra = ease(seg(t, 8.20, 8.70))*(1-ease(seg(t, 9.70, 10.20)))*fo
        if ra > 0.003:
            y = 700
            d.line([BX, y, BX+700, y], fill=mix(BG, INK, ra), width=5)
            for x0, x1, col in ((BX+40, BX+300, LIME_I), (BX+660, BX+400, AMBER_I)):
                d.line([x0, y-46, x1, y-46], fill=mix(BG, col, ra), width=5)
                dx = 1 if x1 > x0 else -1
                d.line([(x1, y-46), (x1-dx*22, y-58)], fill=mix(BG, col, ra), width=5)
                d.line([(x1, y-46), (x1-dx*22, y-34)], fill=mix(BG, col, ra), width=5)
            text(d, (BX+350, y+52), "210 miles", grot(42, "Bold"), DIM, alpha=ra)

        pa = ease(seg(t, 9.90, 10.40))*fo
        leg(d, Y_OUT, 7, seg(t, 10.00, 11.60), LIME, LIME_I, "out", "7 hours", pa)
        pb = ease(seg(t, 12.55, 13.05))*fo
        leg(d, Y_BACK, 3, seg(t, 12.65, 13.90), AMBER, AMBER_I, "back", "3 hours", pb)

        # L5, the asymmetry named
        text(d, (W//2, 1230), "seven hours slow, three hours fast",
             grot(46, "Medium"), CORAL_I,
             alpha=ease(seg(t, 15.40, 15.90))*(1-ease(seg(t, 18.80, 19.30)))*fo)

        text(d, (W//2, 1360), "the slow bar is more than twice as long",
             grot(42, "Medium"), DIM,
             alpha=ease(seg(t, 17.10, 17.60))*(1-ease(seg(t, 18.80, 19.30)))*fo)

        # L6 the totals, L7 the answer
        text(d, (W//2, 1230), "420 miles in 10 hours", disp(60), INK,
             alpha=ease(seg(t, 19.20, 19.70))*(1-ease(seg(t, 22.30, 22.80)))*fo)
        text(d, (W//2, 560), "420 ÷ 10", disp(72), INK,
             alpha=ease(seg(t, 22.50, 23.00))*fo)
        text(d, (W//2, 1230), "42 miles an hour", disp(76), GREEN,
             alpha=ease(seg(t, 22.55, 23.05))*fo)

        # L8 why
        text(d, (W//2, 1360), "the slow half eats more of the clock",
             grot(44, "Medium"), CORAL_I,
             alpha=ease(seg(t, 24.30, 24.80))*fo)

        ba = ease(seg(t, 26.40, 26.90))*fo
        if ba > 0.003:
            y = 700
            d.line([260, y, 820, y], fill=mix(BG, LINE, ba), width=4)
            for x, lab, col in ((260, "30", LIME_I), (820, "70", AMBER_I), (428, "42", GREEN)):
                d.ellipse([x-11, y-11, x+11, y+11], fill=mix(BG, col, ba))
                text(d, (x, y-52), lab, grot(42, "Bold"), col, alpha=ba)
            text(d, (540, y+62), "42 sits nearer the slow one", grot(40, "Medium"), DIM, alpha=ba)

    # ============ endcard   after L8 ends 28.23
    if t > 28.6:
        text(d, (W//2, 800), "Speeds do not average.", disp(80), INK,
             alpha=ease(seg(t, 28.80, 29.30)))
        text(d, (W//2, 930), "Time does.", disp(80), GREEN,
             alpha=ease(seg(t, 29.70, 30.20)))
        text(d, (W//2, 1180), "quanticaedu.com", disp(62), GREEN,
             alpha=ease(seg(t, 30.80, 31.30)))
        text(d, (W//2, 1258), "prealgebra 7.3, free", sans(40), DIM,
             alpha=ease(seg(t, 31.35, 31.85)))
    brand(img, d)
    return img


DUR = 32.6

if __name__ == "__main__":
    import sys
    from fractions import Fraction as F
    print("  check:", 210/30, "h out,", 210/70, "h back,", 420/10, "mph average")
    assert F(420, 10) == 42
    if "--check" in sys.argv:
        w, bad = dead_air(render, DUR)
        print(f"  duration {DUR}s | worst static {w}s | over-2.5s: {bad or 'none'}")
    else:
        render_all(render, DUR, os.path.join(OUT, "quantica-04-avgspeed.mp4"), FR)
