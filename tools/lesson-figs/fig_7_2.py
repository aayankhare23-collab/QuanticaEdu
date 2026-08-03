"""7.2 Graphing Linear Equations. The graph IS the set of points that satisfy the equation."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig, BLUE, GOLD_MID, GOLD_DEEP, SLATE, HAIRLINE, WHITE

M, B = 2, -1                       # the drawn line, y = 2x - 1
PTS = [(-1, -3), (1, 1), (3, 5)]   # three of its points; must appear in no problem
FW, FH = 14.0, 8.4

f = Fig(width=580, frame_width=FW, frame_height=FH, aria=(
    "A single straight line rising steeply to the right across a coordinate plane, with three of "
    "its points marked as dots and each labelled with its pair of coordinates, and the equation "
    "y equals two x minus one written once beside the line."))

plane = NumberPlane(
    x_range=[-5, 5, 1], y_range=[-5, 6, 1], x_length=10.2, y_length=7.1,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2, "stroke_opacity": 1},
    axis_config={"stroke_color": SLATE, "stroke_width": 3.2, "include_tip": True,
                 "tip_width": 0.19, "tip_height": 0.23})
f.add(plane)

lo, hi = -1.9, 3.4
f.add(Line(plane.c2p(lo, M * lo + B), plane.c2p(hi, M * hi + B), color=BLUE, stroke_width=5))
for (x, y) in PTS:
    f.add(Dot(plane.c2p(x, y), radius=0.115, color=WHITE, stroke_width=0),
          Dot(plane.c2p(x, y), radius=0.095, color=GOLD_MID, stroke_width=0))
    f.label(plane.c2p(x, y), f"({x}, {y})".replace("-", "−"), size=13, weight=700,
            color=GOLD_DEEP, anchor="start", dx=13, dy=2)

f.label(plane.c2p(-2.2, 1.9), "y = 2x − 1", size=15, weight=700, color=BLUE,
        anchor="end", dx=-2)
f.label(plane.c2p(5, 0), "x", size=15, weight=700, color=SLATE, italic=True, dx=6, dy=15)
f.label(plane.c2p(0, 6), "y", size=15, weight=700, color=SLATE, italic=True, dx=-14, dy=-3)
print(f.write(str(pathlib.Path(__file__).parent / "fig_7_2.svg")))
