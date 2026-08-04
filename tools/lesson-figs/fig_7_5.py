"""7.5 Intercepts and Standard Forms.

Two bands. The top band draws one line and marks where it crosses each axis, with
the two intercepts arriving one at a time so the reader sees which coordinate is set
to zero for each. Below a near-black rule, the two named forms sit in flat pills.
"""
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import (Fig, BLUE, BLUE_DEEP, GOLD_MID, GOLD_DEEP, SLATE,
                        HAIRLINE, GREY_LINE, WHITE, INK, SURFACE)

XI, YI = 5, 3                      # the two intercepts; appear in no problem
W, H = 580, 500
PPU = 50.0
FW, FH = W / PPU, H / PPU
U = 44.0 / PPU

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "Two bands. In the top band, a coordinate plane with one straight line falling to "
    "the right. A dashed guide runs along the horizontal axis to the point where the "
    "line crosses it at five, then a second dashed guide runs up the vertical axis to "
    "where it crosses at three, each crossing marked with a gold dot. Below a "
    "near-black rule, two flat pills give the two standard ways of writing a line."))


def sp(x, y):
    return np.array([(x - W / 2) / PPU, (H / 2 - y) / PPU, 0.0])


plane = NumberPlane(
    x_range=[-4, 8, 1], y_range=[-3, 5, 1], x_length=12 * U, y_length=8 * U,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2.4, "stroke_opacity": 1},
    axis_config={"stroke_color": INK, "stroke_width": 4.4, "include_tip": True,
                 "tip_width": 0.22, "tip_height": 0.26},
).move_to(sp(W / 2, 196))
plane.background_lines.set_stroke(HAIRLINE, 2.4)
f.add(plane)

M = -YI / XI                                     # the line through both intercepts
f.add(Line(plane.c2p(-2.2, M * -2.2 + YI), plane.c2p(7.6, M * 7.6 + YI),
           color=BLUE, stroke_width=6))
f.label(sp(42, 24), "where it meets each axis", size=13, weight=700, color=INK, anchor="start")
f.label(plane.c2p(8, 0), "x", size=16, weight=700, color=INK, italic=True, dx=7, dy=15)
f.label(plane.c2p(0, 5), "y", size=16, weight=700, color=INK, italic=True, dx=-14, dy=-4)


def reveal(t):
    """First the x-intercept with y set to 0, then the y-intercept with x set to 0."""
    mobs, labs = [], []
    ease = lambda u: u * u * (3 - 2 * u)
    if t < 0.46:
        u = ease(min(1.0, t / 0.40))
        mobs.append(DashedLine(plane.c2p(0, 0), plane.c2p(XI * u, 0),
                               color=GOLD_MID, stroke_width=4, dash_length=0.12))
        if u > 0.97:
            mobs += [Dot(plane.c2p(XI, 0), radius=0.135, color=INK, stroke_width=0),
                     Dot(plane.c2p(XI, 0), radius=0.105, color=GOLD_MID, stroke_width=0)]
            labs.append(f.mklabel(plane.c2p(XI, 0), "y = 0 here", size=12, weight=700,
                                  color=GOLD_DEEP, dy=26))
    else:
        u = ease(min(1.0, (t - 0.46) / 0.40))
        mobs += [Dot(plane.c2p(XI, 0), radius=0.135, color=INK, stroke_width=0),
                 Dot(plane.c2p(XI, 0), radius=0.105, color=GOLD_MID, stroke_width=0)]
        labs.append(f.mklabel(plane.c2p(XI, 0), "y = 0 here", size=12, weight=700,
                              color=GOLD_DEEP, dy=26))
        mobs.append(DashedLine(plane.c2p(0, 0), plane.c2p(0, YI * u),
                               color=GOLD_MID, stroke_width=4, dash_length=0.12))
        if u > 0.97:
            mobs += [Dot(plane.c2p(0, YI), radius=0.135, color=INK, stroke_width=0),
                     Dot(plane.c2p(0, YI), radius=0.105, color=GOLD_MID, stroke_width=0)]
            labs.append(f.mklabel(plane.c2p(0, YI), "x = 0 here", size=12, weight=700,
                                  color=GOLD_DEEP, anchor="start", dx=14))
    return mobs, labs


f.frames(reveal, n=30, dur=7.0)

f.rule(374)
f.label(sp(42, 392), "two ways to write the same line", size=13, weight=700, color=INK, anchor="start")
for cx, form in ((176, "y = mx + b"), (404, "Ax + By = C")):
    f.pill(cx, 442, 210, 58)
    f.label(sp(cx, 442), form, size=18, weight=700, color=BLUE_DEEP, italic=True)
print(f.write(str(pathlib.Path(__file__).parent / "fig_7_5.svg")))
