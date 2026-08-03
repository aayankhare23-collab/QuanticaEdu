"""7.3 Slope. Two slope triangles on ONE line, so the ratio visibly does not depend on the pair."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig, BLUE, GOLD_MID, GOLD_DEEP, SLATE, HAIRLINE, GREY_LINE, WHITE

M, B = 0.5, 1.0            # the drawn line, y = x/2 + 1; must appear in no problem
TRI = [(-6, -2), (2, 6)]   # the two runs, as x-intervals
FW, FH = 14.0, 8.0

f = Fig(width=580, frame_width=FW, frame_height=FH, aria=(
    "One straight line rising to the right on a coordinate plane, with two right triangles drawn "
    "beneath it on different stretches of the same line. The smaller triangle has a run of four "
    "and a rise of two, the larger a run of eight and a rise of four, so both give the same "
    "ratio."))

plane = NumberPlane(
    x_range=[-7, 7, 1], y_range=[-3, 5, 1], x_length=11.2, y_length=6.4,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2, "stroke_opacity": 1},
    axis_config={"stroke_color": SLATE, "stroke_width": 3.2, "include_tip": True,
                 "tip_width": 0.19, "tip_height": 0.23})
f.add(plane)
f.add(Line(plane.c2p(-6.7, M * -6.7 + B), plane.c2p(6.7, M * 6.7 + B),
           color=BLUE, stroke_width=5))

for (x1, x2), col in zip(TRI, (GOLD_MID, GOLD_MID)):
    y1, y2 = M * x1 + B, M * x2 + B
    f.add(Line(plane.c2p(x1, y1), plane.c2p(x2, y1), color=col, stroke_width=3.4),
          Line(plane.c2p(x2, y1), plane.c2p(x2, y2), color=col, stroke_width=3.4))
    f.add(Dot(plane.c2p(x1, y1), radius=0.075, color=BLUE, stroke_width=0),
          Dot(plane.c2p(x2, y2), radius=0.075, color=BLUE, stroke_width=0))
    f.label(plane.c2p((x1 + x2) / 2, y1), "run", size=12, weight=700, color=GOLD_DEEP, dy=15)
    f.label(plane.c2p(x2, (y1 + y2) / 2), "rise", size=12, weight=700, color=GOLD_DEEP,
            anchor="start", dx=8)

f.label(plane.c2p(7, 0), "x", size=15, weight=700, color=SLATE, italic=True, dx=6, dy=15)
f.label(plane.c2p(0, 5), "y", size=15, weight=700, color=SLATE, italic=True, dx=-14, dy=-3)
print(f.write(str(pathlib.Path(__file__).parent / "fig_7_3.svg")))
