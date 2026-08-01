"""
Quantica short #3  "1, 2, 4, 8, 16, and then it breaks"

Put n dots on a circle, join every pair, count the regions inside.
  n = 1..6  ->  1, 2, 4, 8, 16, 31   (not 32)
  regions = C(n,4) + C(n,2) + 1, valid when no three chords meet at one interior point
  n = 6 in general position: 15 chords, 15 crossings, 1 + 15 + 15 = 31

The region counts drawn on screen are NOT typed in. Each figure is rasterised and the
enclosed areas are flood filled and counted, so the picture proves its own number.
"""
import os, math
from itertools import combinations
from PIL import Image, ImageDraw
from qkit import *
from render import grot

OUT = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(OUT, "frames3")

CX, CY = W//2, 812
RAD = 250

# dot angles. jittered off the regular polygon so no three chords ever concur,
# which is exactly the general-position condition the count needs.
def angles(n):
    return [(-math.pi/2)+2*math.pi*i/n+(0.0 if n < 4 else 0.15*math.sin(i*2.7)) for i in range(n)]

def pts(n, r=RAD, c=(CX, CY)):
    return [(c[0]+r*math.cos(a), c[1]+r*math.sin(a)) for a in angles(n)]


def region_count(n, r=170):
    """Rasterise the figure and flood fill, so the number comes from the picture."""
    S = 2*r+40
    im = Image.new("L", (S, S), 255)
    d = ImageDraw.Draw(im)
    c = (S//2, S//2)
    d.ellipse([c[0]-r, c[1]-r, c[0]+r, c[1]+r], outline=0, width=2)
    P = pts(n, r, c)
    for a, b in combinations(range(n), 2):
        d.line([P[a], P[b]], fill=0, width=2)
    px = im.load()
    seen = [[False]*S for _ in range(S)]
    cnt = 0
    for y in range(S):
        for x in range(S):
            if px[x, y] != 255 or seen[y][x]:
                continue
            # flood fill this blob, note whether it touches the border (outside the circle)
            stack = [(x, y)]; seen[y][x] = True; outside = False; size = 0
            while stack:
                a, b = stack.pop(); size += 1
                if a == 0 or b == 0 or a == S-1 or b == S-1: outside = True
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    u, v = a+da, b+db
                    if 0 <= u < S and 0 <= v < S and not seen[v][u] and px[u, v] == 255:
                        seen[v][u] = True; stack.append((u, v))
            if not outside and size > 12:
                cnt += 1
    return cnt

COUNTS = {}     # filled at import, printed by --check


def draw_figure(d, n, a, chords=1.0, r=RAD, c=(CX, CY), dots=True):
    """Circle with n dots and `chords` fraction of the chords drawn."""
    if a <= 0.003: return
    col = mix(BG, INK, a)
    d.ellipse([c[0]-r, c[1]-r, c[0]+r, c[1]+r], outline=col, width=5)
    P = pts(n, r, c)
    ch = list(combinations(range(n), 2))
    show = chords*len(ch)
    for i, (x, y) in enumerate(ch):
        f = clamp(show-i)
        if f <= 0.01: break
        p0, p1 = P[x], P[y]
        p1 = (p0[0]+(p1[0]-p0[0])*ease_out(f), p0[1]+(p1[1]-p0[1])*ease_out(f))
        d.line([p0, p1], fill=mix(BG, BLUE_M, a*0.85), width=4)
    if dots:
        for p in P:
            d.ellipse([p[0]-11, p[1]-11, p[0]+11, p[1]+11],
                      fill=mix(BG, GREEN, a), outline=mix(BG, BG, a), width=3)


def render(t):
    """Beats pinned to the narration schedule in lines.py, measured not guessed."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ================================ the sequence   L0 - L3, 0.30 - 7.04
    if t < 7.35:
        a = ease(seg(t, 0.0, 0.3))*(1-ease(seg(t, 6.95, 7.35)))
        seqf = disp(96)
        toks = ["1", "2", "4", "8", "16"]
        widths = [measure(d, s, seqf)[0] for s in toks]
        gap = 46
        x = W//2-(sum(widths)+gap*(len(toks)-1))//2
        for i, (s, wd) in enumerate(zip(toks, widths)):
            text(d, (x+wd//2, 640), s, seqf, INK,
                 alpha=ease(seg(t, 0.30+i*0.34, 0.62+i*0.34))*a)
            x += wd+gap
        text(d, (W//2, 810), "say the next number out loud", grot(50, "Medium"), DIM,
             alpha=ease(seg(t, 2.50, 3.00))*a)                       # L1
        text(d, (W//2, 1010), "32", disp(126), DIM,
             alpha=ease(seg(t, 4.30, 4.70))*a)                       # L2
        p = ease_out(seg(t, 5.35, 5.85))
        if p > 0:
            wd, _ = measure(d, "32", disp(126))
            d.line([W//2-wd//2-26, 1010, W//2-wd//2-26+(wd+52)*p, 1010],
                   fill=mix(BG, RED, a), width=12)
        text(d, (W//2, 1180), "it is 31", disp(104), GREEN,
             alpha=ease(seg(t, 6.15, 6.55))*a)                       # L3

    # ================================ what the numbers count   L4 - L10
    F0, F1 = 25.90, 26.50
    if 7.3 < t < F1+0.2:
        fo = 1-ease(seg(t, F0, F1))
        # L4 names what the numbers are, L5 describes the construction, so build it live:
        # an empty circle, then dots on its edge, then every pair joined.
        text(d, (W//2, 372), "these count regions inside a circle", grot(50, "Medium"), DIM,
             alpha=ease(seg(t, 7.55, 8.05))*(1-ease(seg(t, 10.35, 10.80)))*fo)   # L4
        text(d, (W//2, 372), "dots on the edge, join every pair", grot(50, "Medium"), DIM,
             alpha=ease(seg(t, 10.55, 11.05))*(1-ease(seg(t, 12.40, 12.85)))*fo) # L5
        demo = ease(seg(t, 8.60, 9.10))*(1-ease(seg(t, 12.35, 12.80)))*fo
        if demo > 0.003:
            dr = 176
            c = (W//2, 812)
            d.ellipse([c[0]-dr, c[1]-dr, c[0]+dr, c[1]+dr], outline=mix(BG, INK, demo), width=5)
            P = pts(4, dr, c)
            dots = ease(seg(t, 10.60, 11.20))
            for i, p in enumerate(P):
                da = demo*clamp(dots*4-i)
                if da > 0.01:
                    d.ellipse([p[0]-11, p[1]-11, p[0]+11, p[1]+11], fill=mix(BG, GREEN, da))
            join = seg(t, 11.50, 12.30)
            ch = list(combinations(range(4), 2))
            for i, (x, y) in enumerate(ch):
                f = clamp(join*len(ch)-i)
                if f <= 0.01: break
                p0, p1 = P[x], P[y]
                p1 = (p0[0]+(p1[0]-p0[0])*ease_out(f), p0[1]+(p1[1]-p0[1])*ease_out(f))
                d.line([p0, p1], fill=mix(BG, BLUE_M, demo*0.85), width=4)

        row_y = 812
        if t < 19.6:
            sr = 92
            xs = [W//2-424, W//2-212, W//2, W//2+212, W//2+424]
            # L6 introduces dots 1 and 2, L7 introduces 3, 4 and 5
            ins = [12.90, 14.20, 16.10, 17.20, 18.30]
            for i, n in enumerate([1, 2, 3, 4, 5]):
                aa = ease(seg(t, ins[i], ins[i]+0.45))*(1-ease(seg(t, 19.10, 19.55)))*fo
                draw_figure(d, n, aa, 1.0, sr, (xs[i], row_y))
                text(d, (xs[i], row_y+sr+58), str(COUNTS[n]), disp(58), GREEN, alpha=aa)
                text(d, (xs[i], row_y-sr-48), f"{n} dot" + ("" if n == 1 else "s"),
                     sans(32), DIM, alpha=aa)

        # L8 "now six dots, that's fifteen chords"
        big = ease(seg(t, 19.75, 20.25))*fo
        if big > 0.003:
            draw_figure(d, 6, big, seg(t, 20.10, 22.00))
            text(d, (W//2, 372), "six dots", grot(50, "Medium"), DIM,
                 alpha=ease(seg(t, 19.95, 20.45))*fo)
            text(d, (W//2, CY+RAD+92), "15 chords", disp(56), BLUE,
                 alpha=ease(seg(t, 20.90, 21.40))*(1-ease(seg(t, 23.40, 23.90)))*fo)
            text(d, (W//2, CY+RAD+188), "count them", grot(44, "Medium"), DIM,
                 alpha=ease(seg(t, 22.20, 22.70))*(1-ease(seg(t, 23.40, 23.90)))*fo)  # L9
            text(d, (W//2, CY+RAD+92), f"{COUNTS[6]} regions, not 32", disp(60), GREEN,
                 alpha=ease(seg(t, 23.90, 24.40))*fo)                                  # L10

    # ================================ why   L11 - L14, 26.14 - 35.20
    if 26.0 < t < 35.85:
        fo = 1-ease(seg(t, 35.30, 35.80))
        text(d, (W//2, 470), "start with one region", grot(50, "Medium"), DIM,
             alpha=ease(seg(t, 27.70, 28.20))*fo)                    # L12
        text(d, (W//2, 600), "every chord adds one", grot(50, "Medium"), BLUE,
             alpha=ease(seg(t, 29.00, 29.50))*fo)
        text(d, (W//2, 730), "every crossing adds one more", grot(50, "Medium"), GOLD_I,
             alpha=ease(seg(t, 30.70, 31.20))*fo)                    # L13
        rows = [("1", "the disc", INK, 33.10), ("15", "chords", BLUE, 33.60),
                ("15", "crossings", GOLD_I, 34.10)]
        for i, (num, lab, col, t0) in enumerate(rows):               # L14
            aa = ease(seg(t, t0, t0+0.35))*fo
            y = 900+i*88
            text(d, (W//2-120, y), num, disp(58), col, alpha=aa)
            text(d, (W//2+70, y), lab, sans(44), DIM, alpha=aa)
        text(d, (W//2, 1220), "1 + 15 + 15 = 31", disp(70), GREEN,
             alpha=ease(seg(t, 34.60, 35.10))*fo)

    # ================================ endcard   L15 spans 35.62 - 37.16
    if t > 35.8:
        text(d, (W//2, 800), "Five terms is not a proof.", disp(78), INK,
             alpha=ease(seg(t, 35.95, 36.45)))
        text(d, (W//2, 940), "A pattern you cannot explain\nowes you nothing.", ser(56), DIM,
             alpha=ease(seg(t, 36.90, 37.40)), spacing=18)
        text(d, (W//2, 1210), "quanticaedu.com", disp(62), GREEN,
             alpha=ease(seg(t, 38.20, 38.70)))
        text(d, (W//2, 1288), "prealgebra 12.1, free", sans(40), DIM,
             alpha=ease(seg(t, 38.75, 39.25)))
    brand(img, d)
    return img


DUR = 40.6

for _n in (1, 2, 3, 4, 5, 6):
    COUNTS[_n] = region_count(_n)

if __name__ == "__main__":
    import sys
    from math import comb
    print("  flood-filled region counts vs the formula C(n,4)+C(n,2)+1:")
    for n in (1, 2, 3, 4, 5, 6):
        f = comb(n, 4)+comb(n, 2)+1
        print(f"    n={n}  drawn={COUNTS[n]:3}  formula={f:3}  {'ok' if COUNTS[n]==f else 'MISMATCH'}")
    if "--check" in sys.argv:
        w, bad = dead_air(render, DUR)
        print(f"  duration {DUR}s | worst static {w}s | over-2.5s: {bad or 'none'}")
    else:
        render_all(render, DUR, os.path.join(OUT, "quantica-03-regions.mp4"), FR)
