"""8.3 Solving Linear Inequalities. Where in a solve the direction can change.

Two ladders run the same two steps side by side. Both subtract b, which never touches
the direction. They differ in exactly one thing, the sign of the divisor, and the
figure's whole job is to make that the only visible difference so the reversal cannot
be read as caused by anything else.

That is why the right ladder prints (c - b) / (-a) rather than -(c - b) / a. The two
are equal, but the second moves the minus sign from the divisor into the numerator in
the same step the symbol flips, which gives a student a second candidate cause. The
band label says "divide by -a", so the divisor is where the minus has to stay.

8.1 already owns the WHY of the reversal, a number line where two points cross as they
are multiplied by a negative. This figure deliberately does not repeat that. It answers
the different question of WHERE in a worked solve the crossing shows up.

The last row animates: the two symbols land after the divisions, the gold one arriving
flipped, so the eye is drawn to the single step that differs.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import (Fig, BLUE, BLUE_DEEP, GOLD_MID, GOLD_DEEP, SLATE,
                        HAIRLINE, GREY_LINE, WHITE, INK, SURFACE)

W, H = 580, 300
PPU = 50.0
FW, FH = W / PPU, H / PPU

LX, RX = 152, 428          # centres of the two ladders
ROW = (96, 152, 226)       # y of the three rungs
SYM_DX = 4                 # symbol sits at the ladder centre

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "Two solution ladders side by side, separated by a vertical hairline. Both start "
    "from a x plus b compared with c, and both subtract b in the middle step, which "
    "leaves the direction alone. The left ladder is headed divide by a and its last "
    "step divides by a positive number, so the greater-than symbol is unchanged. The "
    "right ladder is headed divide by minus a and its last step divides by a negative "
    "number, so the symbol reverses to less-than and is highlighted in gold. The two "
    "ladders differ only in the sign of the divisor and in that final symbol."))

# ---- the divider and the two band headings ------------------------------------
f.add(Line(f.sp(290, 30), f.sp(290, 268), color=HAIRLINE, stroke_width=2.0))
f.label(f.sp(LX, 44), "divide by a", size=13, weight=700, color=BLUE)
f.label(f.sp(RX, 44), "divide by −a", size=13, weight=700, color=BLUE)


def rung(cx, y, left, sym, right, sym_color=SLATE, sym_weight=400):
    """One line of a ladder: expression, comparison symbol, expression."""
    f.label(f.sp(cx - 13, y), left, size=19, weight=400, color=SLATE, anchor="end")
    f.label(f.sp(cx + SYM_DX, y), sym, size=19, weight=sym_weight, color=sym_color)
    f.label(f.sp(cx + 21, y), right, size=19, weight=400, color=SLATE, anchor="start")


# ---- rows one and two, identical in shape on both sides ------------------------
rung(LX, ROW[0], "ax + b", ">", "c")
rung(RX, ROW[0], "−ax + b", ">", "c")
rung(LX, ROW[1], "ax", ">", "c − b")
rung(RX, ROW[1], "−ax", ">", "c − b")

# ---- row three, the only step that differs -------------------------------------
# Left: divisor positive, symbol survives. Right: divisor negative, symbol reverses.
for cx, denom, sym, col, wt in ((LX, "a", ">", BLUE_DEEP, 700),
                                (RX, "−a", "<", GOLD_DEEP, 700)):
    # sits further left than the rows above, so the gold highlight pill on the right
    # ladder has clear air around it instead of touching the x
    f.label(f.sp(cx - 26, ROW[2]), "x", size=19, weight=400, color=BLUE_DEEP, anchor="end")
    # the fraction: numerator, bar, denominator. Identical numerator on both sides.
    f.label(f.sp(cx + 58, ROW[2] - 13), "c − b", size=16, weight=400, color=BLUE_DEEP)
    f.add(Line(f.sp(cx + 30, ROW[2] + 1), f.sp(cx + 86, ROW[2] + 1),
               color=GREY_LINE, stroke_width=1.8))
    f.label(f.sp(cx + 58, ROW[2] + 20), denom, size=16, weight=400, color=BLUE_DEEP)

# The reversed symbol is the payload, so it lands last and lands highlighted.
f.pill(RX + SYM_DX, ROW[2], 44, 32, fill="#fcd76a", stroke="#e0a52a", width=2.0, r=11)
f.label(f.sp(LX + SYM_DX, ROW[2]), ">", size=19, weight=700, color=BLUE_DEEP)
f.label(f.sp(RX + SYM_DX, ROW[2]), "<", size=19, weight=700, color=GOLD_DEEP)

# ---- the one moving part: an arrow down each ladder, gold one arriving second ---
DUR = 5.5
for cx, col, begin in ((LX, BLUE, 0.10), (RX, GOLD_MID, 0.40)):
    f.draw([Line(f.sp(cx - 96, ROW[0] + 14), f.sp(cx - 96, ROW[2] - 12),
                 color=col, stroke_width=4.0)], dur=DUR, begin=begin, span=0.34)

print(f.write(str(pathlib.Path(__file__).parent / "fig_8_3.svg")))
