"""7.1 The Cartesian Plane. The reference picture of the plane.

Two bands. Top: the plane itself, arrowheaded axes, the origin marked, the four
quadrants named in lowercase words, and one point at (3, 2) with dashed guides to
each axis. Below a full-width hairline, the two axis cases, which reinforce the key
idea the figure directly follows.

Band two deliberately does NOT carry the sign-to-quadrant table. That table would
pre-solve P5, whose whole task is reading a quadrant off two signs, and it would
take the content the outline assigns to imp3.
"""
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import (Fig, BLUE, BLUE_DEEP, GOLD_MID, GOLD_DEEP, SLATE,
                        HAIRLINE, GREY_LINE, WHITE, INK, SURFACE)

PT = (3, 2)                       # the plotted point; must appear in no problem
W, H = 580, 500                   # canvas in px
PPU = 50.0                        # px per scene unit
FW, FH = W / PPU, H / PPU         # 11.6 x 10.0
U = 46.0 / PPU                    # one grid step, 46 px


def sp(x, y):
    """px on the 580x500 canvas -> scene coordinates."""
    return np.array([(x - W / 2) / PPU, (H / 2 - y) / PPU, 0.0])


def num(v):
    return str(v).replace("-", "−")   # a real minus sign, not a hyphen


f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "Two bands. In the top band, a coordinate plane on a faint grid, the x-axis "
    "and y-axis arrowheaded and crossing at a marked origin, the four quadrants "
    "labelled one, two, three and four counterclockwise from the upper right, and "
    "and a gold point that travels from the origin three units along the x-axis "
    "and then two units up, arriving at the point labelled 3 comma 2. Below a "
    "full-width hairline, "
    "two pills give the two axis cases, x equals zero on the y-axis and y equals "
    "zero on the x-axis."))

# ---- band one, the plane -------------------------------------------------
plane = NumberPlane(
    x_range=[-5, 5, 1], y_range=[-3.5, 3.5, 1], x_length=10 * U, y_length=7 * U,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2.4,
                           "stroke_opacity": 1},
    axis_config={"stroke_color": INK, "stroke_width": 4.4, "include_tip": True,
                 "tip_width": 0.22, "tip_height": 0.26},
).move_to(sp(W / 2, 208))
plane.background_lines.set_stroke(HAIRLINE, 2.4)
f.add(plane)

o, p = plane.c2p(0, 0), plane.c2p(*PT)
f.add(Dot(o, radius=0.085, color=INK, stroke_width=0))


# The pair (3, 2) IS this walk: 3 along the x-axis, then 2 up. The two legs draw on
# in sequence and the dot glides, all interpolated by the browser, so the motion is
# smooth rather than the ~4 fps a flipbook of manim frames would give at this size.
DUR = 7.0
LEG1, LEG2 = 0.40, 0.40                       # fractions of the cycle per leg

f.draw([Line(o, plane.c2p(PT[0], 0), color=GOLD_MID, stroke_width=6)],
       dur=DUR, span=LEG1,
       labels=[f.mklabel(plane.c2p(PT[0] / 2, 0), "along", size=12, weight=700,
                         color=GOLD_DEEP, dy=32)], label_at=LEG1 * 0.55)
f.draw([Line(plane.c2p(PT[0], 0), p, color=GOLD_MID, stroke_width=6)],
       dur=DUR, begin=LEG1 * DUR, span=LEG2,
       labels=[f.mklabel(plane.c2p(PT[0], PT[1] / 2), "up", size=12, weight=700,
                         color=GOLD_DEEP, anchor="start", dx=9)], label_at=LEG2 * 0.55)

# the travelling dot, along the same two legs
DOT_KEYS = []
for i in range(17):
    t = i / 16
    if t <= LEG1:
        DOT_KEYS.append((PT[0] * (t / LEG1), 0.0, 1.0))
    elif t <= LEG1 + LEG2:
        DOT_KEYS.append((PT[0], PT[1] * ((t - LEG1) / LEG2), 1.0))
    else:
        DOT_KEYS.append((PT[0], PT[1], 1.0))
f.motion([Dot(o, radius=0.135, color=INK, stroke_width=0),
          Dot(o, radius=0.105, color=GOLD_MID, stroke_width=0)],
         DOT_KEYS, dur=DUR, about=o)

# the pair is named only once the walk arrives
f.draw([], dur=DUR, span=1.0,
       labels=[f.mklabel(p, "(3, 2)", size=15, weight=700, color=GOLD_DEEP,
                         anchor="start", dx=13, dy=-8)], label_at=LEG1 + LEG2)

f.label(sp(42, 24), "the plane", size=13, weight=700, color=INK, anchor="start")

for xv in (-4, -2, 2, 4):                       # ticks named sparsely
    f.label(plane.c2p(xv, 0), num(xv), size=12, weight=400, color=GREY_LINE, dy=15)
for yv in (-2, 2):
    f.label(plane.c2p(0, yv), num(yv), size=12, weight=400, color=GREY_LINE, dx=-12)

f.label(plane.c2p(5, 0), "x", size=16, weight=700, color=INK, italic=True, dx=7, dy=15)
f.label(plane.c2p(0, 3.5), "y", size=16, weight=700, color=INK, italic=True, dx=-14, dy=-4)
f.label(o, "origin", size=12, weight=700, color=INK, anchor="end", dx=-11, dy=16)

for pos, word in (((4.3, 3.05), "one"), ((-4.3, 3.05), "two"),
                  ((-4.3, -3.05), "three"), ((4.3, -3.05), "four")):
    f.label(plane.c2p(*pos), word, size=14, weight=700, color=BLUE_DEEP)

# ---- the hairline, full width -------------------------------------------
f.rule(396)

# ---- band two, the two axis cases ---------------------------------------
# NOT the sign-to-quadrant table. That table pre-solves P5, whose whole task is to
# read a quadrant off two signs, and it steals the content the outline assigns to
# imp3, which is meant to earn the sign patterns only AFTER those problems. This
# band reinforces imp2 instead, the block the figure directly follows.
f.label(sp(42, 414), "on an axis", size=13, weight=700, color=INK, anchor="start")

for cx, eq, word in ((176, "x = 0", "the y-axis"), (404, "y = 0", "the x-axis")):
    f.pill(cx, 458, 196, 58)
    f.label(sp(cx - 52, 458), eq, size=18, weight=700, color=BLUE_DEEP, italic=True)
    f.label(sp(cx + 44, 458), word, size=14, weight=700, color=INK)

print(f.write(str(pathlib.Path(__file__).parent / "fig_7_1.svg")))
