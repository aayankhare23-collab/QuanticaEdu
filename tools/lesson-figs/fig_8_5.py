"""8.5 Optimization. Only the corners need checking, so check them all.

One first-quadrant region bounded by straight edges, five corners, each marked with a
dot. Four dots are plain and one is gold, labelled "best here". The animation is a ring
that draws around each corner in turn, in boundary order, reaching the gold one last,
so the figure performs the lesson's method: evaluate at every corner and keep the best.

The base figure is complete before anything moves. The region, its edges, all five
dots and the gold pick are static, and the rings only add emphasis, so a reader who
catches the figure mid-cycle, or with motion switched off, still sees the whole
argument. That is the lesson 8.4's static figure taught about animating comparisons,
applied in the other direction, since here there IS a motion that teaches, the
one-at-a-time visit that "check every corner" literally is.

The region has FIVE corners on purpose. Dots can be counted, so the spec pins P6's
answer and every other stated region in the lesson away from five, which makes the
count in the picture useless as an answer.

Style per the current brand (marketing hero + manim/brand.py): near-black ink
outlines, one flat sky fill, hero amber for the pick, square corners, Space Grotesk,
lowercase labels, no digits anywhere.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig

INK = "#0a0a0a"
SKY = "#7cc7ff"
AMBER = "#ffc84d"
PAPER = "#ffffff"
FAINT = "#5b6b7a"

W, H = 580, 400
PPU = 50.0
FW, FH = W / PPU, H / PPU

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "A first-quadrant coordinate region shaded solid, bounded below and on the left "
    "by the axes and above and to the right by three straight edges. Each of its five "
    "corners carries a dot. Four dots are plain and the corner highest up and to the "
    "right is gold and labelled best here. A ring draws itself around each corner in "
    "turn along the boundary, reaching the gold corner last, the way the best value "
    "is found by checking every corner and keeping the best."))


def sp(x, y):
    return f.sp(x, y)


def tip(x, y, dx, dy, size=7.0):
    px, py = -dy, dx
    return Polygon(sp(x, y),
                   sp(x - dx * size * 1.9 + px * size * 0.72,
                      y - dy * size * 1.9 + py * size * 0.72),
                   sp(x - dx * size * 1.9 - px * size * 0.72,
                      y - dy * size * 1.9 - py * size * 0.72),
                   color=INK, fill_color=INK, fill_opacity=1, stroke_width=0)


# ── the region ─────────────────────────────────────────────────────────────────
# Origin of the plane in pixels, and the five corners in boundary order. C is the
# pick. Convex, three non-axis edges, nothing parallel to anything obvious.
OX, OY = 96, 330
O = (OX, OY)
A = (430, OY)          # on the x-axis
B = (500, 236)         # up the right-hand slant
C = (392, 96)          # the best corner
D = (OX, 168)          # on the y-axis
corners = [O, A, B, C, D]

f.add(Polygon(*[sp(*p) for p in corners],
              color=SKY, fill_color=SKY, fill_opacity=1, stroke_width=0))

# the three edges that are not axes, ink over the wash
for p, q in ((A, B), (B, C), (C, D)):
    f.add(Line(sp(*p), sp(*q), color=INK, stroke_width=4.4))

# axes, drawn after the wash so they stay crisp along the region's other two edges
f.add(Line(sp(OX - 14, OY), sp(548, OY), color=INK, stroke_width=2.6))
f.add(Line(sp(OX, OY + 14), sp(OX, 44), color=INK, stroke_width=2.6))
f.add(tip(556, OY, 1, 0), tip(OX, 36, 0, -1))
f.label(sp(548, OY + 18), "x", size=15, weight=700, color=INK, italic=True)
f.label(sp(OX + 16, 42), "y", size=15, weight=700, color=INK, italic=True)

# ── the corner dots ────────────────────────────────────────────────────────────
DOT = 8.0
for p in corners:
    if p is C:
        continue
    f.add(Circle(radius=DOT / PPU, color=INK, stroke_width=2.8,
                 fill_color=PAPER, fill_opacity=1).move_to(sp(*p)))
f.add(Circle(radius=(DOT + 1.5) / PPU, color=INK, stroke_width=2.8,
             fill_color=AMBER, fill_opacity=1).move_to(sp(*C)))
f.label(sp(C[0] + 14, C[1] - 20), "best here", size=14, weight=700, color=INK,
        anchor="start")

# ── the edge letters ───────────────────────────────────────────────────────────
# The caption names the five boundary lines a through e, one per edge, in boundary
# order starting from the bottom. Each letter sits just OUTSIDE the region beside
# its edge's midpoint, so none of them reads as a point label.
f.label(sp(263, 350), "a", size=14, weight=700, color=INK, italic=True)   # O-A, on the x-axis
f.label(sp(482, 294), "b", size=14, weight=700, color=INK, italic=True)   # A-B
f.label(sp(466, 166), "c", size=14, weight=700, color=INK, italic=True)   # B-C
f.label(sp(244, 112), "d", size=14, weight=700, color=INK, italic=True)   # C-D
f.label(sp(78, 249), "e", size=14, weight=700, color=INK, italic=True)    # D-O, on the y-axis

# ── the one moving part: a ring visits each corner, the gold one last ──────────
# The visit order runs along the boundary and ends on the pick, so the emphasis
# lands where the answer is. All rings ride one shared clock (the kit bakes the
# stagger into keyTimes), and the still base already carries the whole figure.
DUR = 7.5
order = [O, A, B, D, C]
# Visited rings stay on for the rest of the cycle, so by the end every corner
# shows its check mark. They are kept light so the accumulated trail reads as
# emphasis rather than clutter, and the pick's ring is the only saturated one.
for i, p in enumerate(order):
    ring = Circle(radius=14.0 / PPU,
                  color=(AMBER if p is C else "#b9cbdc"), stroke_width=3.2,
                  fill_opacity=0).move_to(sp(*p))
    f.draw([ring], dur=DUR, begin=0.06 + i * 0.13, span=0.10)

print(f.write(str(pathlib.Path(__file__).parent / "fig_8_5.svg")))
