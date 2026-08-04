"""7.4 Finding the Equation of a Line.

Two bands. The top band sweeps many lines through ONE fixed point, then settles on
the one with the given slope, which is the lesson's whole claim: a point alone does
not pin a line, a point and a slope do. The bottom band names the two inputs in flat
pills, separated from the plane by a near-black editorial rule.
"""
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import (Fig, BLUE, BLUE_DEEP, GOLD_MID, GOLD_DEEP, SLATE,
                        HAIRLINE, GREY_LINE, WHITE, INK, SURFACE)

PT = (-2, -1)                     # the known point; appears in no problem.
                                  # Chosen so a run of 4 keeps the rise inside the box.
M = 0.75                          # the settled slope, 3/4
W, H = 580, 500
PPU = 50.0
FW, FH = W / PPU, H / PPU
U = 44.0 / PPU

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "Two bands. In the top band, a coordinate plane with one marked point, through "
    "which many faint lines sweep at different slopes before settling on a single "
    "bold line of slope three quarters, with a small right triangle on it showing a "
    "run of four and a rise of three. Below a near-black rule, two flat pills name "
    "the two inputs, the point and the slope."))


def sp(x, y):
    return np.array([(x - W / 2) / PPU, (H / 2 - y) / PPU, 0.0])


plane = NumberPlane(
    x_range=[-5, 5, 1], y_range=[-3, 3, 1], x_length=10 * U, y_length=6 * U,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2.4, "stroke_opacity": 1},
    axis_config={"stroke_color": INK, "stroke_width": 4.4, "include_tip": True,
                 "tip_width": 0.22, "tip_height": 0.26},
).move_to(sp(W / 2, 196))
plane.background_lines.set_stroke(HAIRLINE, 2.4)
f.add(plane)
P = plane.c2p(*PT)

f.label(sp(42, 24), "one point, one slope", size=13, weight=700, color=INK, anchor="start")
f.label(plane.c2p(5, 0), "x", size=16, weight=700, color=INK, italic=True, dx=7, dy=15)
f.label(plane.c2p(0, 3), "y", size=16, weight=700, color=INK, italic=True, dx=-14, dy=-4)


def clip(slope):
    """The chord of y - 2 = slope(x + 1) inside the plane box."""
    xs = []
    for x in (-4.7, 4.7):
        y = PT[1] + slope * (x - PT[0])
        if abs(y) <= 2.8: xs.append((x, y))
    for y in (-2.8, 2.8):
        if slope != 0:
            x = PT[0] + (y - PT[1]) / slope
            if abs(x) <= 4.7: xs.append((x, y))
    pts = sorted(xs)
    return plane.c2p(*pts[0]), plane.c2p(*pts[-1])


def sweep(t):
    """Fan through slopes, then hold the answer with its slope triangle."""
    mobs, labs = [], []
    if t < 0.62:
        u = t / 0.62
        for k in range(7):                      # a fan of candidates, all through P
            s = math.tan((-1.15 + 2.3 * ((k + 1) / 8)) * (0.35 + 0.65 * u))
            a, b = clip(s)
            mobs.append(Line(a, b, color=BLUE, stroke_width=2.2).set_opacity(0.32))
        s_now = math.tan(-1.0 + 1.0 * u)
        a, b = clip(s_now)
        mobs.append(Line(a, b, color=BLUE, stroke_width=5))
    else:
        a, b = clip(M)
        mobs.append(Line(a, b, color=BLUE, stroke_width=6))
        x2 = PT[0] + 4
        corner = plane.c2p(x2, PT[1])
        mobs += [Line(P, corner, color=GOLD_MID, stroke_width=4.2),
                 Line(corner, plane.c2p(x2, PT[1] + M * 4), color=GOLD_MID, stroke_width=4.2)]
        labs += [f.mklabel(plane.c2p(PT[0] + 2.7, PT[1]), "run", size=12, weight=700,
                           color=GOLD_DEEP, dy=17),
                 f.mklabel(plane.c2p(x2, PT[1] + M * 2), "rise", size=12, weight=700,
                           color=GOLD_DEEP, anchor="start", dx=9)]
    mobs += [Dot(P, radius=0.135, color=INK, stroke_width=0),
             Dot(P, radius=0.105, color=GOLD_MID, stroke_width=0)]
    return mobs, labs


f.frames(sweep, n=32, dur=7.5)

f.rule(374)
f.label(sp(42, 392), "what pins it", size=13, weight=700, color=INK, anchor="start")
for cx, head, sub in ((176, "(−2, −1)", "a point on it"), (404, "3/4", "its slope")):
    f.pill(cx, 442, 200, 62)
    f.label(sp(cx, 430), head, size=18, weight=700, color=BLUE_DEEP)
    f.label(sp(cx, 455), sub, size=13, weight=700, color=INK)
print(f.write(str(pathlib.Path(__file__).parent / "fig_7_4.svg")))
