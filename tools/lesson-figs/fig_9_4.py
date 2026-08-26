"""9.4 Roots, Sums, and Products. Coefficients in, two root facts out.

The quadratic sits at the top with each of its three coefficients underlined in
its own color. Two arrows leave it. The left one carries a and b down to the sum,
the right one carries a and c down to the product. The roots appear nowhere,
which is the entire claim of the lesson: both facts are read off the coefficients
without ever finding a root.

The minus sign on the sum is drawn oversized and in amber, alone among the
glyphs. The sum of the roots is -b/a and not b/a, and that sign is the most
common error in this material, so the picture is built to make the minus the
first thing the eye lands on rather than a detail inside a formula.

Letters only, no digits except the squared exponent naming the term, so nothing
here can pre-solve a problem. Static: the two readings are simultaneous facts
about one expression, not a sequence.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig

INK = "#0a0a0a"
LAV = "#c9b8ff"
AMBER = "#ffc84d"
SKY = "#7cc7ff"
FAINT = "#5b6b7a"

W, H = 580, 316
PPU = 50.0
FW, FH = W / PPU, H / PPU

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "The quadratic a x squared plus b x plus c sits at the top, with each of its "
    "three coefficients underlined in its own color. Two arrows lead down from it. "
    "The left arrow ends at minus b over a, labelled sum, with the minus sign drawn "
    "large and in gold. The right arrow ends at c over a, labelled product. No root "
    "appears anywhere in the picture, because both facts are read off the "
    "coefficients without finding the roots."))


def sp(x, y):
    return f.sp(x, y)


def tip(x, y, dx, dy, size=7.0, color=INK):
    n = (dx * dx + dy * dy) ** 0.5
    dx, dy = dx / n, dy / n
    px, py = -dy, dx
    return Polygon(sp(x, y),
                   sp(x - dx * size * 1.9 + px * size * 0.7,
                      y - dy * size * 1.9 + py * size * 0.7),
                   sp(x - dx * size * 1.9 - px * size * 0.7,
                      y - dy * size * 1.9 - py * size * 0.7),
                   color=color, fill_color=color, fill_opacity=1, stroke_width=0)


# ── the quadratic, with each coefficient underlined in its own colour ──────────
QY = 74
terms = [(214, "a", LAV), (296, "b", AMBER), (368, "c", SKY)]
f.label(sp(224, QY), "ax", size=28, weight=700, color=INK, italic=True)
f.label(sp(243, QY - 11), "2", size=16, weight=700, color=INK)
f.label(sp(266, QY), "+", size=22, weight=500, color=FAINT)
f.label(sp(298, QY), "bx", size=28, weight=700, color=INK, italic=True)
f.label(sp(336, QY), "+", size=22, weight=500, color=FAINT)
f.label(sp(366, QY), "c", size=28, weight=700, color=INK, italic=True)

for cx, _, col in ((214, "a", LAV), (292, "b", AMBER), (366, "c", SKY)):
    f.add(Line(sp(cx - 11, QY + 22), sp(cx + 11, QY + 22), color=col, stroke_width=5.0))

# ── the two arrows out ────────────────────────────────────────────────────────
LX, RX, TY = 158, 424, 214
f.add(Line(sp(266, QY + 40), sp(LX + 22, TY - 52), color=INK, stroke_width=2.8))
f.add(tip(LX + 14, TY - 44, -1, 1.35, color=INK))
f.add(Line(sp(322, QY + 40), sp(RX - 22, TY - 52), color=INK, stroke_width=2.8))
f.add(tip(RX - 14, TY - 44, 1, 1.35, color=INK))


def fraction(cx, cy, num, den, num_color=INK):
    f.label(sp(cx, cy - 19), num, size=25, weight=700, color=num_color, italic=True)
    f.add(Line(sp(cx - 19, cy + 1), sp(cx + 19, cy + 1), color=INK, stroke_width=2.8))
    f.label(sp(cx, cy + 23), den, size=25, weight=700, color=INK, italic=True)


# left: the sum. The minus sits INSIDE the numerator rather than outside the
# fraction. Set beside the fraction it reads as a second fraction bar, since it
# lands at exactly the bar's height; set on the numerator it can only be a sign.
# It is drawn as a stroke rather than set as a glyph, at the same amber and the
# same weight as b's underline in the expression above, so the sign reads as the
# mark b picks up on its way down rather than as punctuation. A glyph at this
# size is the faintest thing in the picture, which is backwards for the one
# detail the lesson exists to defend.
f.add(Line(sp(LX - 21, TY - 19), sp(LX - 1, TY - 19), color=AMBER, stroke_width=5.0))
f.label(sp(LX + 15, TY - 19), "b", size=25, weight=700, color=INK, italic=True)
f.add(Line(sp(LX - 22, TY + 1), sp(LX + 22, TY + 1), color=INK, stroke_width=2.8))
f.label(sp(LX, TY + 23), "a", size=25, weight=700, color=INK, italic=True)
f.label(sp(LX, TY + 62), "sum", size=17, weight=700, color=INK)

# right: the product
fraction(RX, TY, "c", "a")
f.label(sp(RX, TY + 62), "product", size=17, weight=700, color=INK)

print(f.write(str(pathlib.Path(__file__).parent / "fig_9_4.svg")))
