"""7.6 Parallel, Perpendicular, and Comparing Lines. The three solution counts, drawn.

Two bands. The top band sets three small panels of axes side by side, one pair of
lines in each, so the only three ways a pair can sit read at a glance. Below a
full-width hairline, the same three cases as a sampled row of points, gold where a
point lies on both lines and grey where it does not, so the count is the picture.

The figure carries no digits at all, so it cannot collide with any problem in the
lesson or pre-solve one.
"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig, BLUE, SLATE, HAIRLINE, GREY_MID, WHITE, INK

GOLD_LINE = "#e0a52a"          # the gold stroke of the house palette
GOLD_FILL = "#fcd76a"

W, H = 580, 366
PPU = 44.0                     # svg pixels per scene unit
SW = 100.0 / PPU               # manim stroke_width that renders as one pixel

f = Fig(width=W, frame_width=W / PPU, frame_height=H / PPU, aria=(
    "Two bands. In the top band, three small panels of axes sit side by side. In the "
    "first, two lines of different slopes cross at a single marked point, labelled one "
    "solution. In the second, two lines of equal slope run parallel and never meet, "
    "labelled no solution. In the third, a dashed line lies directly over a thicker "
    "line so the two read as one line, labelled infinitely many. Below a hairline, a row "
    "of sampled points sits under each panel, gold where a point lies on both lines and "
    "grey where it does not. One point is gold under the first panel, none under the "
    "second, and every point is gold under the third."))

R = 76.0                       # panel half-size, in svg pixels
K = 0.86                       # lines are clipped to this fraction of the panel box
CX = (100.0, 290.0, 480.0)     # the three panel centres
CY = 106.0
ROW_Y, ROW_STEP, ROW_N = 330.0, 17.0, 9
FADE = (0.40, 0.72, 1.0, 1.0, 1.0, 1.0, 1.0, 0.72, 0.40)   # the row runs off both ends


def P(cx, x, y):
    """A point in panel-local coordinates, where 1 is the panel half-size."""
    return f.sp(cx + x * R, CY - y * R)


def axes(cx):
    for a, z in (((-1, 0), (1, 0)), ((0, -1), (0, 1))):
        f.add(Arrow(P(cx, *a), P(cx, *z), buff=0, color=SLATE, stroke_width=5.0,
                    max_tip_length_to_length_ratio=0.09, tip_length=0.17))


def ends(m, b):
    """Where y = mx + b leaves the panel box, in panel-local coordinates."""
    pts = []
    for x in (-K, K):
        y = m * x + b
        if abs(y) <= K + 1e-9:
            pts.append((round(x, 6), round(y, 6)))
    if m:
        for y in (-K, K):
            x = (y - b) / m
            if abs(x) <= K + 1e-9:
                pts.append((round(x, 6), round(y, 6)))
    pts = sorted(set(pts))
    return pts[0], pts[-1]


def seg(cx, m, b, colour, sw, dashed=False):
    (x1, y1), (x2, y2) = ends(m, b)
    a, z = P(cx, x1, y1), P(cx, x2, y2)
    if dashed:
        return DashedLine(a, z, color=colour, stroke_width=sw, dash_length=0.15)
    return Line(a, z, color=colour, stroke_width=sw)


def marker(point, r=0.15):
    """A gold point with a white halo, so it reads on top of whatever it sits on."""
    return (Circle(radius=r * 1.42, fill_color=WHITE, fill_opacity=1, stroke_width=0)
            .move_to(point),
            Circle(radius=r, fill_color=GOLD_FILL, fill_opacity=1,
                   stroke_color=GOLD_LINE, stroke_width=6).move_to(point))


# ---- band one, the three panels -----------------------------------------
# panel one, different slopes, one crossing
M1, B1, M2, B2 = 1.5, -0.2, -0.7, 0.5
axes(CX[0])
f.add(seg(CX[0], M1, B1, BLUE, 7.0), seg(CX[0], M2, B2, GOLD_LINE, 7.0))
xc = (B2 - B1) / (M1 - M2)
f.add(*marker(P(CX[0], xc, M1 * xc + B1)))

# panel two, equal slopes, never meeting
axes(CX[1])
f.add(seg(CX[1], 0.9, 0.45, BLUE, 7.0), seg(CX[1], 0.9, -0.45, GOLD_LINE, 7.0))

# panel three, one line drawn twice
axes(CX[2])
f.add(seg(CX[2], 0.85, 0.12, BLUE, 10.0))
f.add(seg(CX[2], 0.85, 0.12, GOLD_LINE, 4.6, dashed=True))

f.label(f.sp(26, 22), "the three ways two lines can sit", size=13, weight=700,
        color=INK, anchor="start")
for cx, word in zip(CX, ("one solution", "no solution", "infinitely many")):
    f.label(f.sp(cx, 212), word, size=14, weight=700, color=INK)

# ---- the near-black editorial rule between the bands ---------------------
f.rule(250, x0_px=26)

# ---- band two, the shared points -----------------------------------------
f.label(f.sp(26, 284), "points on both lines", size=13, weight=700,
        color=INK, anchor="start")


def row(cx, shared):
    """One sampled row of points. Gold where the point lies on both lines.

    Flat fills with no stroke on purpose. Cairo flattens a fill-only path to device
    space and needs half the beziers, so a stroked ring on each of these would about
    double the whole figure for nothing the colour is not already saying.
    """
    for i, a in enumerate(FADE):
        at = f.sp(cx + (i - (ROW_N - 1) / 2) * ROW_STEP, ROW_Y)
        f.add(Circle(radius=5.0 / PPU, fill_opacity=a, stroke_width=0,
                     fill_color=GOLD_LINE if i in shared else GREY_MID).move_to(at))


row(CX[0], {4})                     # exactly one shared point
row(CX[1], set())                   # none
row(CX[2], set(range(ROW_N)))       # every point of the line

# Cairo writes six decimals, which is a tenth of a millionth of a pixel. Three is
# already under a thousandth of a pixel and takes a third off the file.
out = re.sub(r'-?\d+\.\d{4,}',
             lambda m: f'{float(m.group(0)):.3f}'.rstrip('0').rstrip('.'), f.svg())
path = pathlib.Path(__file__).parent / "fig_7_6.svg"
path.write_text(out, encoding="utf-8")
print(path, len(out), "bytes")
