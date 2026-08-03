"""7.4 Finding the Equation of a Line. One point plus one slope pins the whole line."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig, BLUE, GOLD_MID, GOLD_DEEP, SLATE, HAIRLINE, GREY_LINE, WHITE

PX, PY_, M = -1, 2, 0.75      # the known point and the slope; must appear in no problem
FW, FH = 14.0, 8.0

f = Fig(width=580, frame_width=FW, frame_height=FH, aria=(
    "A coordinate plane with one marked point, a small right triangle drawn from that point "
    "showing a run of four to the right and a rise of three upward, and a single straight line "
    "drawn through the point and the triangle in both directions."))

plane = NumberPlane(
    x_range=[-7, 7, 1], y_range=[-3, 5, 1], x_length=11.2, y_length=6.4,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2, "stroke_opacity": 1},
    axis_config={"stroke_color": SLATE, "stroke_width": 3.2, "include_tip": True,
                 "tip_width": 0.19, "tip_height": 0.23})
f.add(plane)

def y_at(x):
    return M * (x - PX) + PY_

f.add(DashedLine(plane.c2p(-6.7, y_at(-6.7)), plane.c2p(PX, PY_),
                 color=BLUE, stroke_width=4, dash_length=0.15))
f.add(DashedLine(plane.c2p(PX + 4, y_at(PX + 4)), plane.c2p(6.6, y_at(6.6)),
                 color=BLUE, stroke_width=4, dash_length=0.15))
f.add(Line(plane.c2p(PX, PY_), plane.c2p(PX + 4, y_at(PX + 4)), color=BLUE, stroke_width=5.4))
f.add(Line(plane.c2p(PX, PY_), plane.c2p(PX + 4, PY_), color=GOLD_MID, stroke_width=3.4),
      Line(plane.c2p(PX + 4, PY_), plane.c2p(PX + 4, y_at(PX + 4)), color=GOLD_MID, stroke_width=3.4))
f.label(plane.c2p(PX + 2, PY_), "run", size=12, weight=700, color=GOLD_DEEP, dy=15)
f.label(plane.c2p(PX + 4, (PY_ + y_at(PX + 4)) / 2), "rise", size=12, weight=700,
        color=GOLD_DEEP, anchor="start", dx=8)

f.add(Dot(plane.c2p(PX, PY_), radius=0.115, color=WHITE, stroke_width=0),
      Dot(plane.c2p(PX, PY_), radius=0.095, color=GOLD_DEEP, stroke_width=0))
f.label(plane.c2p(PX, PY_), "the known point", size=12, weight=700, color=SLATE,
        anchor="end", dx=-12, dy=-6)
f.label(plane.c2p(7, 0), "x", size=15, weight=700, color=SLATE, italic=True, dx=6, dy=15)
f.label(plane.c2p(0, 5), "y", size=15, weight=700, color=SLATE, italic=True, dx=-14, dy=-3)
print(f.write(str(pathlib.Path(__file__).parent / "fig_7_4.svg")))
