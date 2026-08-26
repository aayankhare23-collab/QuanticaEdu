"""9.5 Factoring in Action. Renaming the repeated piece.

Two rows holding the SAME skeleton. The top row is an expression in which one
piece appears twice, both copies sitting in a filled slot. The bottom row is the
identical line with a single letter in those same two slots, and the shape left
behind is plainly a quadratic.

Everything that is not the repeated piece is drawn at identical coordinates in
both rows, because that is the claim being made. Nothing changes except the name
of the piece, so the reader can see that the second line is a quadratic and infer
that the first one already was. The slots are the same size in both rows rather
than shrinking to fit their contents, which keeps the two lines in register and
makes the substitution read as a swap into a fixed position.

Letters only, apart from the exponent and the zero on the right, so nothing here
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
    "Two rows showing the same expression. In the top row the piece x plus h "
    "appears twice, each copy inside a filled blue slot, once squared and once "
    "multiplied by b, with c added and the whole thing set equal to zero. Two "
    "arrows lead down to the bottom row, which is the identical line with the "
    "single letter u in both slots, so the shape underneath is plainly a "
    "quadratic in u."))


def sp(x, y):
    return f.sp(x, y)


def slot(cx, cy, text, w=104, h=46):
    """One filled slot holding the repeated piece. Square corners, ink outline."""
    f.add(Rectangle(width=w / PPU, height=h / PPU, fill_color=SKY, fill_opacity=1,
                    stroke_color=INK, stroke_width=2.4).move_to(sp(cx, cy)))
    f.label(sp(cx, cy), text, size=25, weight=700, color=INK, italic=True)


def arrow(x, y0, y1):
    f.add(Line(sp(x, y0), sp(x, y1 - 9), color=INK, stroke_width=2.6))
    f.add(Polygon(sp(x, y1), sp(x - 6.5, y1 - 13), sp(x + 6.5, y1 - 13),
                  color=INK, fill_color=INK, fill_opacity=1, stroke_width=0))


# Every glyph outside the two slots is placed once, from this table, and drawn at
# the same x in both rows. If a coordinate ever differs between the rows the
# figure stops making its own argument.
A, B = 132, 322                       # the two slot centres
TOP, BOT = 76, 232                    # the two row baselines
# x, glyph, size, italic, dy, colour. Operators are faint so the expression's own
# symbols carry; the exponent is part of the expression, not an operator.
REST = [(194, "2", 16, False, -13, INK),
        (225, "+", 22, False, 0, FAINT),
        (254, "b", 26, True, 0, INK),
        (392, "+", 22, False, 0, FAINT),
        (421, "c", 26, True, 0, INK),
        (456, "=", 22, False, 0, FAINT),
        (487, "0", 26, False, 0, INK)]

for y in (TOP, BOT):
    for x, t, size, ital, dy, col in REST:
        f.label(sp(x, y + dy), t, size=size, weight=700 if col is INK else 500,
                color=col, italic=ital)

slot(A, TOP, "(x + h)")
slot(B, TOP, "(x + h)")
slot(A, BOT, "u")
slot(B, BOT, "u")

arrow(A, TOP + 34, BOT - 34)
arrow(B, TOP + 34, BOT - 34)
f.label(sp(227, (TOP + BOT) / 2), "rename", size=17, weight=700, color=INK)

print(f.write(str(pathlib.Path(__file__).parent / "fig_9_5.svg")))
