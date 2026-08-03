"""7.1 The Cartesian Plane. The reference picture of the plane."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig, BLUE, GOLD_MID, GOLD_DEEP, SLATE, HAIRLINE, GREY_LINE, WHITE

PT = (3, 2)          # the plotted point; must appear in no problem
FW, FH = 12.0, 8.4

f = Fig(width=580, frame_width=FW, frame_height=FH, aria=(
    "A coordinate plane with the x-axis and y-axis crossing at the origin, the "
    "four quadrants labelled one, two, three and four counterclockwise from the "
    "upper right, and one point plotted three to the right and two up, with "
    "dashed guides running from the point to each axis."))

plane = NumberPlane(
    x_range=[-5, 5, 1], y_range=[-3.5, 3.5, 1], x_length=10.4, y_length=7.28,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2, "stroke_opacity": 1},
    axis_config={"stroke_color": SLATE, "stroke_width": 3.4, "include_tip": True,
                 "tip_width": 0.20, "tip_height": 0.24},
)
plane.background_lines.set_stroke(HAIRLINE, 2)
f.add(plane)

o = plane.c2p(0, 0)
p = plane.c2p(*PT)
# dashed guides from the point down to each axis
f.add(DashedLine(plane.c2p(PT[0], 0), p, color=GREY_LINE, stroke_width=2.4, dash_length=0.11),
      DashedLine(plane.c2p(0, PT[1]), p, color=GREY_LINE, stroke_width=2.4, dash_length=0.11))
f.add(Dot(p, radius=0.115, color=WHITE, stroke_width=0),
      Dot(p, radius=0.095, color=GOLD_MID, stroke_width=0))
f.add(Dot(o, radius=0.075, color=SLATE, stroke_width=0))

# ticks worth naming, sparse
def num(v):
    return str(v).replace("-", "\u2212")  # a real minus sign, not a hyphen

for xv in (-4, -2, 2, 4):
    f.label(plane.c2p(xv, 0), num(xv), size=12, weight=400, color=GREY_LINE, dy=15)
for yv in (-2, 2):
    f.label(plane.c2p(0, yv), num(yv), size=12, weight=400, color=GREY_LINE, dx=-12)

f.label(plane.c2p(5, 0), "x", size=15, weight=700, color=SLATE, italic=True, dx=6, dy=15)
f.label(plane.c2p(0, 3.5), "y", size=15, weight=700, color=SLATE, italic=True, dx=-14, dy=-4)
f.label(o, "origin", size=12, weight=500, color=SLATE, anchor="end", dx=-11, dy=16)
f.label(p, "(3, 2)", size=15, weight=700, color=GOLD_DEEP, anchor="start", dx=12, dy=-7)

for pos, word in (((2.9, 2.9), "one"), ((-2.9, 2.9), "two"),
                  ((-2.9, -2.9), "three"), ((2.9, -2.9), "four")):
    f.label(plane.c2p(*pos), word, size=13, weight=700, color=BLUE)

print(f.write(str(pathlib.Path(__file__).parent / "fig_7_1.svg")))
