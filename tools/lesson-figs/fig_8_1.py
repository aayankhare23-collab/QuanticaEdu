"""8.1 The Basics of Inequality.

The one rule that changes: multiplying both sides by a negative reverses the sign.
Two points sit on a number line with a left of b. Multiplying both by a negative
sends them to the other side of zero, and they CROSS on the way, so a ends up right
of b. The crossing is the reversal, so it is animated rather than drawn twice.

Letters only, no digits, which makes the figure collision-proof against every problem.
"""
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import (Fig, BLUE, BLUE_DEEP, GOLD_MID, GOLD_DEEP, SLATE,
                        HAIRLINE, GREY_LINE, WHITE, INK, SURFACE)

A, B = 2.0, 4.0            # a < b, both right of zero
K = -1.5                   # the negative multiplier
W, H = 580, 300
PPU = 50.0
FW, FH = W / PPU, H / PPU
DUR = 8.0

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "A number line with zero marked. Two gold points labelled a and b sit to the "
    "right of zero, with a nearer zero than b. Both points then travel left across "
    "zero to the positions they reach after multiplication by a negative number, "
    "crossing each other on the way, and finish with the image of a to the right of "
    "the image of b, so their order has reversed."))


def sp(x, y):
    return np.array([(x - W / 2) / PPU, (H / 2 - y) / PPU, 0.0])


UNIT = 44.0 / PPU          # scene units per number-line step
Y = sp(W / 2, 150)[1]


def at(v):
    return np.array([v * UNIT, Y, 0.0])


f.label(sp(26, 26), "multiplying both sides by a negative", size=13, weight=700,
        color=INK, anchor="start")

# the line itself, with arrowheads and zero marked
# a number line points both ways
f.add(DoubleArrow(at(-7.2), at(7.2), buff=0, color=INK, stroke_width=3.4,
                  max_tip_length_to_length_ratio=0.03, tip_length=0.2))
f.add(Line(at(0) + UP * 0.16, at(0) + DOWN * 0.16, color=INK, stroke_width=3.4))
f.label(at(0), "zero", size=12, weight=700, color=SLATE, dy=30)

# a faint marker at each endpoint of the journey, so the destinations read as places
for v in (K * A, K * B):
    f.add(Line(at(v) + UP * 0.10, at(v) + DOWN * 0.10, color=GREY_LINE, stroke_width=2.4))


def travel(start, end, colour, name):
    """One point sliding from its own value to its image, with its label riding along."""
    keys, lkeys = [], []
    for i in range(13):
        t = i / 12
        e = t * t * (3 - 2 * t)                     # ease in and out
        hold = 0.0 if t < 0.12 else (1.0 if t > 0.88 else (e - 0.12) / 0.76)
        hold = min(1.0, max(0.0, hold))
        d = (end - start) * hold * UNIT
        keys.append((d, 0.0, 1.0))
        lkeys.append((d, 0.0))
    dot = [Dot(at(start), radius=0.135, color=INK, stroke_width=0),
           Dot(at(start), radius=0.105, color=colour, stroke_width=0)]
    lab = [f.mklabel(at(start), name, size=16, weight=700, color=GOLD_DEEP, dy=-24)]
    f.motion(dot, keys, dur=DUR, labels=lab, label_keys=lkeys, about=at(start))


travel(A, K * A, GOLD_MID, "a")
travel(B, K * B, GOLD_MID, "b")

f.label(sp(26, 262), "a starts left of b and lands right of it", size=13,
        weight=700, color=BLUE_DEEP, anchor="start")
print(f.write(str(pathlib.Path(__file__).parent / "fig_8_1.svg")))
