"""8.2 Which Is Bigger.

Transitivity as a picture. Three points on one line, a well left, b well right, and a
chosen m between them. The band above the hairline carries the two comparisons that
actually get made, each one against m. The band below carries the comparison that
falls out, a against b, which was never made directly.

The lower bracket's arms rise toward the hairline at exactly the x of a and b, and two
dotted threads cross the rule at those same positions, so the wide span reads as
inherited from the two points above rather than floating on its own.

Static, and letters only, no digits anywhere, which makes it collision-proof against
every problem in the lesson. Built on the same Fig kit and the same ink baseline,
DoubleArrow and haloed points as 8.1, so the two chapter figures read as siblings.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import (Fig, BLUE, BLUE_DEEP, GOLD_MID, GOLD_DEEP, SLATE,
                        HAIRLINE, INK)

W, H = 580, 248
PPU = 50.0
FW, FH = W / PPU, H / PPU

# canvas x of the three points, and the y of the line they sit on
XA, XM, XB = 118, 300, 470
YLINE = 72
YRULE = 136

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "A horizontal number line with three marked points. Point a sits well to the "
    "left, point m sits between them, and point b sits well to the right. A bracket "
    "under the left gap is labelled a less than m, a bracket under the right gap is "
    "labelled m less than b, and a wider bracket beneath both spans a to b and is "
    "labelled a less than b."))

sp = f.sp

# ---- the line -------------------------------------------------------------
f.add(DoubleArrow(sp(44, YLINE), sp(536, YLINE), buff=0, color=INK, stroke_width=3.4,
                  max_tip_length_to_length_ratio=0.03, tip_length=0.2))

# the middle point gets a tick through the line, since it is the one being chosen.
# it has to clear the dot's own radius (0.135 units) or it is invisible behind it
f.add(Line(sp(XM, YLINE) + UP * 0.30, sp(XM, YLINE) + DOWN * 0.30,
           color=GOLD_MID, stroke_width=3.4))

for x, colour in ((XA, BLUE), (XB, BLUE), (XM, GOLD_MID)):
    f.add(Dot(sp(x, YLINE), radius=0.135, color=INK, stroke_width=0))
    f.add(Dot(sp(x, YLINE), radius=0.105, color=colour, stroke_width=0))

f.label(sp(XA, 42), "a", size=16, weight=700, color=SLATE)
f.label(sp(XM, 42), "m", size=16, weight=700, color=GOLD_DEEP)
f.label(sp(XB, 42), "b", size=16, weight=700, color=SLATE)


DUR = 8.0
T1, T2, T3 = 0.26, 0.26, 0.30    # first comparison, second, then the conclusion


def brace(x0, x1, y_top, y_run, colour, width=2.4):
    """A square underbrace. Arms rise from the horizontal run back toward the line."""
    m = VMobject(stroke_color=colour, stroke_width=width, fill_opacity=0)
    m.set_points_as_corners([sp(x0, y_top), sp(x0, y_run),
                             sp(x1, y_run), sp(x1, y_top)])
    return m


def bracket(x0, x1, y_top, y_run, colour, width=2.4):
    f.add(brace(x0, x1, y_top, y_run, colour, width))


# ---- band one: the two comparisons that are made --------------------------
# a gap at m, wide enough to clear the dot, so the pair reads as two separate
# comparisons rather than one span broken in the middle
# Each comparison is drawn in turn, then the conclusion falls out of the pair. The
# order is the argument, so it is animated rather than presented all at once.
f.draw([brace(XA, XM - 12, 84, 96, BLUE)], dur=DUR, span=T1,
       labels=[f.mklabel(sp((XA + XM - 12) / 2, 118), "a &lt; m", size=13, weight=700,
                         color=BLUE)], label_at=T1)
f.draw([brace(XM + 12, XB, 84, 96, BLUE)], dur=DUR, begin=T1, span=T2,
       labels=[f.mklabel(sp((XM + 12 + XB) / 2, 118), "m &lt; b", size=13, weight=700,
                         color=BLUE)], label_at=T2)

# ---- the hairline ---------------------------------------------------------
f.add(Line(sp(0, YRULE), sp(W, YRULE), color=HAIRLINE, stroke_width=1.6))

# ---- band two: the comparison that falls out ------------------------------
# two dotted threads carry a and b down across the rule, so the wide bracket is
# visibly the SAME two points and not a new pair
f.draw([DashedLine(sp(x, 104), sp(x, 152), color="#9fb4d6", stroke_width=1.6,
                   dash_length=0.05, dashed_ratio=0.42) for x in (XA, XB)],
       dur=DUR, begin=T1 + T2, span=0.10)
f.draw([brace(XA, XB, 152, 168, GOLD_DEEP)],
       dur=DUR, begin=T1 + T2 + 0.10, span=T3,
       labels=[f.mklabel(sp((XA + XB) / 2, 188), "a &lt; b", size=14, weight=700,
                         color=GOLD_DEEP)], label_at=T3)

f.label(sp(26, 220), "neither outer comparison was made directly", size=13,
        weight=700, color=BLUE_DEEP, anchor="start")

print(f.write(str(pathlib.Path(__file__).parent / "fig_8_2.svg")))
