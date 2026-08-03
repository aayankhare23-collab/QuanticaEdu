"""7.5 Intercepts and Standard Forms. The two intercepts as the two quickest points to plot."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig, BLUE, GOLD_MID, GOLD_DEEP, SLATE, HAIRLINE, GREY_LINE, WHITE

XI, YI = 5, 3               # the two intercepts; must appear in no problem
FW, FH = 14.0, 8.0

f = Fig(width=580, frame_width=FW, frame_height=FH, aria=(
    "A coordinate plane with one straight line falling to the right, crossing the horizontal axis "
    "at five and the vertical axis at three. Each crossing is marked with a dot, labelled with "
    "its value and with the words x-intercept and y-intercept in lowercase."))

plane = NumberPlane(
    x_range=[-7, 7, 1], y_range=[-3, 5, 1], x_length=11.2, y_length=6.4,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2, "stroke_opacity": 1},
    axis_config={"stroke_color": SLATE, "stroke_width": 3.2, "include_tip": True,
                 "tip_width": 0.19, "tip_height": 0.23})
f.add(plane)

M = -YI / XI
f.add(Line(plane.c2p(-4.4, M * -4.4 + YI), plane.c2p(XI + 3.6, M * (XI + 3.6) + YI),
           color=BLUE, stroke_width=5))
for pt, word, anch, dx, dy in (((XI, 0), "x-intercept", "middle", 0, 24),
                               ((0, YI), "y-intercept", "start", 14, -2)):
    f.add(Dot(plane.c2p(*pt), radius=0.115, color=WHITE, stroke_width=0),
          Dot(plane.c2p(*pt), radius=0.095, color=GOLD_MID, stroke_width=0))
    f.label(plane.c2p(*pt), word, size=12, weight=700, color=GOLD_DEEP,
            anchor=anch, dx=dx, dy=dy)
f.label(plane.c2p(XI, 0), str(XI), size=13, weight=700, color=SLATE, anchor="start", dx=8, dy=-12)
f.label(plane.c2p(0, YI), str(YI), size=13, weight=700, color=SLATE, anchor="end", dx=-17, dy=-1)
f.label(plane.c2p(7, 0), "x", size=15, weight=700, color=SLATE, italic=True, dx=6, dy=15)
f.label(plane.c2p(0, 5), "y", size=15, weight=700, color=SLATE, italic=True, dx=-14, dy=-3)
print(f.write(str(pathlib.Path(__file__).parent / "fig_7_5.svg")))
