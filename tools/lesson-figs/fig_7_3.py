"""7.3 Slope. The slope triangle slides along the line and changes size, and the
ratio it reports never moves. That IS the derivation, so it is animated rather
than drawn twice."""
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig, BLUE, GOLD_MID, GOLD_DEEP, SLATE, HAIRLINE, GREY_LINE, WHITE

M, B = 0.5, 1.0            # the drawn line, y = x/2 + 1; appears in no problem
FW, FH = 14.0, 8.0

f = Fig(width=580, frame_width=FW, frame_height=FH, aria=(
    "One straight line rising to the right across a coordinate plane. A right "
    "triangle sits under the line with its horizontal leg labelled run and its "
    "vertical leg labelled rise. The triangle slides along the line and grows and "
    "shrinks as it goes, and the rise is always half the run however large the "
    "triangle becomes."))

plane = NumberPlane(
    x_range=[-7, 7, 1], y_range=[-3, 5, 1], x_length=11.2, y_length=6.4,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2, "stroke_opacity": 1},
    axis_config={"stroke_color": SLATE, "stroke_width": 3.2, "include_tip": True,
                 "tip_width": 0.19, "tip_height": 0.23})
f.add(plane)
f.add(Line(plane.c2p(-6.7, M * -6.7 + B), plane.c2p(6.7, M * 6.7 + B),
           color=BLUE, stroke_width=5))

f.label(plane.c2p(7, 0), "x", size=15, weight=700, color=SLATE, italic=True, dx=6, dy=15)
f.label(plane.c2p(0, 5), "y", size=15, weight=700, color=SLATE, italic=True, dx=-14, dy=-3)


def triangle(t):
    """The slope triangle at phase t. It travels left to right and breathes."""
    span = 2.2 + 2.6 * math.sin(math.pi * t) ** 2      # run, 2.2 up to 4.8
    x1 = -6.0 + t * (10.6 - span)
    x2 = x1 + span
    y1, y2 = M * x1 + B, M * x2 + B
    corner = plane.c2p(x2, y1)
    mobs = [
        Line(plane.c2p(x1, y1), corner, color=GOLD_MID, stroke_width=4),
        Line(corner, plane.c2p(x2, y2), color=GOLD_MID, stroke_width=4),
        Line(plane.c2p(x1, y1), plane.c2p(x2, y2), color=GOLD_DEEP, stroke_width=2.2),
        Dot(plane.c2p(x1, y1), radius=0.085, color=BLUE, stroke_width=0),
        Dot(plane.c2p(x2, y2), radius=0.085, color=BLUE, stroke_width=0),
    ]
    labs = [
        f.mklabel(plane.c2p((x1 + x2) / 2, y1), "run", size=12, weight=700,
                  color=GOLD_DEEP, dy=15),
        f.mklabel(plane.c2p(x2, (y1 + y2) / 2), "rise", size=12, weight=700,
                  color=GOLD_DEEP, anchor="start", dx=8),
    ]
    return mobs, labs


f.frames(triangle, n=34, dur=7.5)
print(f.write(str(pathlib.Path(__file__).parent / "fig_7_3.svg")))
