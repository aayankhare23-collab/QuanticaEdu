"""9.5 Factoring in Action. Renaming the repeated piece.

Two rows holding the SAME skeleton. The top row is an equation in which one piece
appears twice, both copies sitting in a filled slot, once squared and once
multiplied by b. The bottom row is the identical line with a single letter in
those same two slots, and what is left reads au^2+bu+c=0.

The piece in the top row is x^2 rather than a binomial, because that is the case
where the picture has something to say. With x^2 in the slots the top row is
degree four and the bottom row is degree two, so the renaming visibly turns a
quartic into a quadratic. With a binomial in the slots both rows are already
degree two and nothing appears to happen.

Everything that is not the repeated piece is drawn at identical coordinates in
both rows, because that is the claim being made. The slots are the same size in
both rows rather than shrinking to fit, which keeps the two lines in register and
makes the substitution read as a swap into a fixed position.

Letters only, apart from the exponents and the zero on the right, so nothing here
can pre-solve a problem. Static: the two rows are one comparison and both halves
have to be on screen together.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig

INK = "#0a0a0a"
SKY = "#7cc7ff"
FAINT = "#5b6b7a"

W, H = 580, 300
PPU = 50.0

f = Fig(width=W, frame_width=W / PPU, frame_height=H / PPU, aria=(
    "The same equation on two rows, with two filled boxes standing where one "
    "repeated piece belongs. The top row reads a, times the first box squared, "
    "plus b times the second box, plus c, equals zero, and both boxes hold x "
    "squared, so the equation has degree four. The bottom row is identical "
    "outside the boxes and both boxes hold the single letter u, so what is left "
    "reads a u squared plus b u plus c equals zero."))


def sp(x, y):
    return f.sp(x, y)


SLOT_W, SLOT_H = 62, 46


def slot(cx, cy, text, sup=None):
    """One filled slot holding the repeated piece. Square corners, ink outline."""
    f.add(Rectangle(width=SLOT_W / PPU, height=SLOT_H / PPU, fill_color=SKY, fill_opacity=1,
                    stroke_color=INK, stroke_width=2.4).move_to(sp(cx, cy)))
    dx = -7 if sup else 0
    f.label(sp(cx + dx, cy), text, size=26, weight=700, color=INK, italic=True)
    if sup:
        f.label(sp(cx + dx + 15, cy - 12), sup, size=15, weight=700, color=INK)


def arrow(x, y0, y1):
    f.add(Line(sp(x, y0), sp(x, y1 - 9), color=INK, stroke_width=2.6))
    f.add(Polygon(sp(x, y1), sp(x - 6.5, y1 - 13), sp(x + 6.5, y1 - 13),
                  color=INK, fill_color=INK, fill_opacity=1, stroke_width=0))


# Every glyph outside the two slots is placed once, from this table, and drawn at
# the same x in both rows. If a coordinate ever differs between the rows the
# figure stops making its own argument.
A, B = 166, 308                       # the two slot centres
TOP, BOT = 76, 232                    # the two row baselines
# x, glyph, size, italic, dy, colour. Operators are faint so the expression's own
# symbols carry; the exponent is part of the expression, not an operator.
REST = [(120, "a", 26, True, 0, INK),
        (206, "2", 15, False, -22, INK),   # the exponent ON the slot, outside it
        (234, "+", 22, False, 0, FAINT),
        (262, "b", 26, True, 0, INK),
        (366, "+", 22, False, 0, FAINT),
        (394, "c", 26, True, 0, INK),
        (428, "=", 22, False, 0, FAINT),
        (460, "0", 26, False, 0, INK)]

for y in (TOP, BOT):
    for x, t, size, ital, dy, col in REST:
        f.label(sp(x, y + dy), t, size=size, weight=700 if col is INK else 500,
                color=col, italic=ital)

slot(A, TOP, "x", sup="2")
slot(B, TOP, "x", sup="2")
slot(A, BOT, "u")
slot(B, BOT, "u")

arrow(A, TOP + 34, BOT - 34)
arrow(B, TOP + 34, BOT - 34)
f.label(sp(237, (TOP + BOT) / 2), "rename", size=17, weight=700, color=INK)

print(f.write(str(pathlib.Path(__file__).parent / "fig_9_5.svg")))
