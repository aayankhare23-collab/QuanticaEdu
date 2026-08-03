"""7.6 The picture chapter 5 was promised: the three solution counts of a 2x2 linear system.
Carries no digits at all, so it cannot collide with any problem."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig, BLUE, GOLD_MID, GOLD_DEEP, SLATE, HAIRLINE, GREY_LINE, WHITE

FW, FH = 15.0, 6.4
f = Fig(width=580, frame_width=FW, frame_height=FH, aria=(
    "Three panels of axes side by side. In the first, two lines cross at a single marked point, "
    "labelled one solution. In the second, two parallel lines never meet, labelled no solution. "
    "In the third, one line is drawn twice with a dashed stroke over a solid one, labelled "
    "infinitely many."))

R = 1.95                      # panel half-size
CENTRES = (-5.0, 0.0, 5.0)
Y0 = 0.55                     # panels sit above their labels


def axes_at(cx):
    g = VGroup()
    g.add(Arrow([cx - R, Y0, 0], [cx + R, Y0, 0], buff=0, color=SLATE,
                stroke_width=2.6, max_tip_length_to_length_ratio=0.09, tip_length=0.17))
    g.add(Arrow([cx, Y0 - R, 0], [cx, Y0 + R, 0], buff=0, color=SLATE,
                stroke_width=2.6, max_tip_length_to_length_ratio=0.09, tip_length=0.17))
    return g


def seg(cx, m, b, colour, width=4.6, dashed=False):
    """The part of y = m*x + b inside the panel, clipped to the panel box."""
    xs, ys = [], []
    lo, hi = -R * 0.88, R * 0.88
    for x in (lo, hi):
        y = m * x + b
        if abs(y) <= R * 0.88:
            xs.append(x); ys.append(y)
    for y in (-R * 0.88, R * 0.88):
        if m != 0:
            x = (y - b) / m
            if abs(x) <= R * 0.88:
                xs.append(x); ys.append(y)
    pts = sorted(zip(xs, ys))
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    a = [cx + x1, Y0 + y1, 0]
    z = [cx + x2, Y0 + y2, 0]
    if dashed:
        return DashedLine(a, z, color=colour, stroke_width=width, dash_length=0.16)
    return Line(a, z, color=colour, stroke_width=width)


# panel one, two lines crossing once
f.add(axes_at(CENTRES[0]))
f.add(seg(CENTRES[0], 0.85, -0.25, BLUE), seg(CENTRES[0], -0.8, 0.6, GOLD_MID))
xc = (0.6 - -0.25) / (0.85 - -0.8)
f.add(Dot([CENTRES[0] + xc, Y0 + 0.85 * xc - 0.25, 0], radius=0.13, color=WHITE, stroke_width=0),
      Dot([CENTRES[0] + xc, Y0 + 0.85 * xc - 0.25, 0], radius=0.095, color=GOLD_DEEP, stroke_width=0))

# panel two, parallel, never meeting
f.add(axes_at(CENTRES[1]))
f.add(seg(CENTRES[1], 0.85, 0.62, BLUE), seg(CENTRES[1], 0.85, -0.68, GOLD_MID))

# panel three, one line drawn twice
f.add(axes_at(CENTRES[2]))
f.add(seg(CENTRES[2], 0.85, 0.1, BLUE, width=6.4))
f.add(seg(CENTRES[2], 0.85, 0.1, GOLD_MID, width=3.0, dashed=True))

for cx, word in zip(CENTRES, ("one solution", "no solution", "infinitely many")):
    f.label([cx, Y0 - R - 0.62, 0], word, size=14, weight=700, color=SLATE)

print(f.write(str(pathlib.Path(__file__).parent / "fig_7_6.svg")))
