"""7.3 Slope. The slope triangle slides along the line and grows as it goes, and the
ratio it reports never moves. That IS the derivation, so it is animated.

The triangle is emitted once and carried by an SVG transform whose keyframes manim
computed. Because the slope is constant, growing the triangle is a pure SCALE about
its own corner, so the animation is a similarity transform, which is exactly the
mathematical claim: the ratio is invariant under it.
"""
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import (Fig, BLUE, GOLD_MID, GOLD_DEEP, SLATE, HAIRLINE,
                        GREY_LINE, WHITE, INK)

M, B = 0.5, 1.0                      # the drawn line, y = x/2 + 1; in no problem
FW, FH = 14.0, 8.0
DUR = 8.0

f = Fig(width=580, frame_width=FW, frame_height=FH, aria=(
    "One straight line rising to the right across a coordinate plane. A right "
    "triangle sits under the line with its horizontal leg labelled run and its "
    "vertical leg labelled rise. The triangle slides along the line and grows and "
    "shrinks as it travels, and the rise stays half the run however large it gets."))

plane = NumberPlane(
    x_range=[-7, 7, 1], y_range=[-3, 5, 1], x_length=11.2, y_length=6.4,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2.4, "stroke_opacity": 1},
    axis_config={"stroke_color": INK, "stroke_width": 4.4, "include_tip": True,
                 "tip_width": 0.22, "tip_height": 0.26})
f.add(plane)
f.add(Line(plane.c2p(-6.7, M * -6.7 + B), plane.c2p(6.7, M * 6.7 + B),
           color=BLUE, stroke_width=6))
f.label(plane.c2p(7, 0), "x", size=16, weight=700, color=INK, italic=True, dx=6, dy=15)
f.label(plane.c2p(0, 5), "y", size=16, weight=700, color=INK, italic=True, dx=-14, dy=-3)

# The triangle at its reference size, anchored at x0. Everything after is a transform.
X0, RUN0 = -6.0, 2.4
y0 = M * X0 + B
corner = plane.c2p(X0 + RUN0, y0)
tri = [
    Line(plane.c2p(X0, y0), corner, color=GOLD_MID, stroke_width=4.6),
    Line(corner, plane.c2p(X0 + RUN0, y0 + M * RUN0), color=GOLD_MID, stroke_width=4.6),
    Dot(plane.c2p(X0, y0), radius=0.095, color=INK, stroke_width=0),
    Dot(plane.c2p(X0 + RUN0, y0 + M * RUN0), radius=0.095, color=INK, stroke_width=0),
]
tri_labels = [
    f.mklabel(plane.c2p(X0 + RUN0 / 2, y0), "run", size=12, weight=700,
              color=GOLD_DEEP, dy=16),
    f.mklabel(plane.c2p(X0 + RUN0, y0 + M * RUN0 / 2), "rise", size=12, weight=700,
              color=GOLD_DEEP, anchor="start", dx=8),
]

# Manim computes where the triangle sits and how big it is at each keyframe. Scaling
# about the anchor keeps the far vertex on the line, since the line through the
# anchor with slope M is invariant under a scale centred there.
KEYS, LKEYS = [], []
for i in range(13):
    t = i / 12
    s = 1.0 + 1.15 * math.sin(math.pi * t) ** 2          # grows, then shrinks back
    x = X0 + t * 9.4
    dx, dy = x - X0, M * (x - X0)                        # travel ALONG the line
    KEYS.append((dx, dy, s))
    # the labels sit at the legs' midpoints, which move as the triangle grows, but
    # the text itself must not scale, so they get their own translate-only track
    LKEYS.append((dx + RUN0 * (s - 1) / 2, dy))
f.motion(tri, KEYS, dur=DUR, labels=tri_labels, label_keys=LKEYS,
         about=plane.c2p(X0, y0))

print(f.write(str(pathlib.Path(__file__).parent / "fig_7_3.svg")))
