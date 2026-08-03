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
                        HAIRLINE, GREY_LINE, WHITE)

PT = (3, 2)                       # the plotted point; must appear in no problem
W, H = 580, 500                   # canvas in px
PPU = 50.0                        # px per scene unit
FW, FH = W / PPU, H / PPU         # 11.6 x 10.0
U = 46.0 / PPU                    # one grid step, 46 px
PILL = "#eaf1ff"
PILL_EDGE = "#cdddf7"


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
    axis_config={"stroke_color": SLATE, "stroke_width": 4.0, "include_tip": True,
                 "tip_width": 0.20, "tip_height": 0.24},
).move_to(sp(W / 2, 208))
plane.background_lines.set_stroke(HAIRLINE, 2.4)
f.add(plane)

o, p = plane.c2p(0, 0), plane.c2p(*PT)
f.add(Dot(o, radius=0.075, color=SLATE, stroke_width=0))


def walk(t):
    """The pair (3, 2) IS this walk: 3 along the x-axis, then 2 up. Animating it
    says what the notation means better than a finished dot with two guides."""
    ease = lambda u: u * u * (3 - 2 * u)              # smoothstep, no jerky start
    mobs, labs = [], []
    if t < 0.42:                                       # along the x-axis
        x = PT[0] * ease(t / 0.42)
        y = 0.0
        mobs.append(Line(o, plane.c2p(x, 0), color=GOLD_MID, stroke_width=5))
        if x > 0.35:
            labs.append(f.mklabel(plane.c2p(x / 2, 0), "along", size=12, weight=700,
                                  color=GOLD_DEEP, dy=32))
    else:                                              # then up
        u = min(1.0, (t - 0.42) / 0.42)
        x, y = PT[0], PT[1] * ease(u)
        mobs.append(Line(o, plane.c2p(PT[0], 0), color=GOLD_MID, stroke_width=5))
        mobs.append(Line(plane.c2p(PT[0], 0), plane.c2p(x, y), color=GOLD_MID, stroke_width=5))
        labs.append(f.mklabel(plane.c2p(PT[0] / 2, 0), "along", size=12, weight=700,
                              color=GOLD_DEEP, dy=32))
        if y > 0.3:
            labs.append(f.mklabel(plane.c2p(PT[0], y / 2), "up", size=12, weight=700,
                                  color=GOLD_DEEP, anchor="start", dx=9))
    mobs += [Dot(plane.c2p(x, y), radius=0.125, color=WHITE, stroke_width=0),
             Dot(plane.c2p(x, y), radius=0.105, color=GOLD_MID, stroke_width=0)]
    if t > 0.86:                                       # arrived, so name it
        labs.append(f.mklabel(p, "(3, 2)", size=15, weight=700, color=GOLD_DEEP,
                              anchor="start", dx=13, dy=-8))
    return mobs, labs


f.frames(walk, n=32, dur=7.0, hold=0.0)

f.label(sp(42, 24), "the plane", size=13, weight=700, color=BLUE, anchor="start")

for xv in (-4, -2, 2, 4):                       # ticks named sparsely
    f.label(plane.c2p(xv, 0), num(xv), size=12, weight=400, color=GREY_LINE, dy=15)
for yv in (-2, 2):
    f.label(plane.c2p(0, yv), num(yv), size=12, weight=400, color=GREY_LINE, dx=-12)

f.label(plane.c2p(5, 0), "x", size=15, weight=700, color=SLATE, italic=True, dx=7, dy=15)
f.label(plane.c2p(0, 3.5), "y", size=15, weight=700, color=SLATE, italic=True, dx=-14, dy=-4)
f.label(o, "origin", size=12, weight=500, color=SLATE, anchor="end", dx=-11, dy=16)

for pos, word in (((4.3, 3.05), "one"), ((-4.3, 3.05), "two"),
                  ((-4.3, -3.05), "three"), ((4.3, -3.05), "four")):
    f.label(plane.c2p(*pos), word, size=13, weight=700, color=BLUE)

# ---- the hairline, full width -------------------------------------------
f.add(Line(sp(42, 396), sp(538, 396), color=HAIRLINE, stroke_width=3.0))

# ---- band two, the two axis cases ---------------------------------------
# NOT the sign-to-quadrant table. That table pre-solves P5, whose whole task is to
# read a quadrant off two signs, and it steals the content the outline assigns to
# imp3, which is meant to earn the sign patterns only AFTER those problems. This
# band reinforces imp2 instead, the block the figure directly follows.
f.label(sp(42, 414), "on an axis", size=13, weight=700, color=BLUE, anchor="start")

for cx, eq, word in ((176, "x = 0", "the y-axis"), (404, "y = 0", "the x-axis")):
    f.add(RoundedRectangle(corner_radius=16 / PPU, width=196 / PPU, height=56 / PPU,
                           fill_color=PILL, fill_opacity=1, stroke_color=PILL_EDGE,
                           stroke_width=3.0).move_to(sp(cx, 458)))
    f.label(sp(cx - 52, 458), eq, size=17, weight=700, color=BLUE_DEEP, italic=True)
    f.label(sp(cx + 44, 458), word, size=14, weight=500, color=SLATE)

print(f.write(str(pathlib.Path(__file__).parent / "fig_7_1.svg")))
