"""9.1 Meet the Quadratic. The area model for a two-binomial product.

One rectangle with its top side split into lengths a and b and its left side split
into lengths c and d, cut into four cells. Each cell is one of the four products,
ac, bc, ad, bd, and the whole rectangle is their sum, which is the entire content of
"every term of the first multiplies every term of the second". The two splits are
deliberately uneven so the four cells read as four different products rather than
as a symmetric grid.

Each cell takes a different flat fill from the marketing hero's accent set, the same
four-color language as the landing page's Pythagoras animation, over ink grid lines.
Static on purpose. The decomposition IS the figure, all four cells at once, and there
is no sequence to perform. Letters only, no digits, collision-proof by construction.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig

INK = "#0a0a0a"
LAV = "#c9b8ff"
MINT = "#9fe8d8"
AMBER = "#ffc84d"
SKY = "#7cc7ff"

W, H = 580, 380
PPU = 50.0
FW, FH = W / PPU, H / PPU

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "A rectangle whose top side is split into a longer length a and a shorter "
    "length b, and whose left side is split into a taller length c and a shorter "
    "length d. The two splits cut the rectangle into four cells, each in its own "
    "flat color and labelled with its own product, ac and bc across the top row, "
    "ad and bd across the bottom row. The whole rectangle is the sum of the four "
    "cells, which is why every term of the first factor multiplies every term of "
    "the second."))


def sp(x, y):
    return f.sp(x, y)


# rectangle 150..510 x 74..334, split at x=372 (a|b) and y=224 (c|d)
X0, X1, XS = 150, 510, 372
Y0, Y1, YS = 74, 334, 224

cells = [
    (X0, Y0, XS, YS, LAV,  "ac"),   # top-left,     a wide, c tall
    (XS, Y0, X1, YS, AMBER, "bc"),  # top-right
    (X0, YS, XS, Y1, MINT, "ad"),   # bottom-left
    (XS, YS, X1, Y1, SKY,  "bd"),   # bottom-right
]
for x0, y0, x1, y1, fill, name in cells:
    f.add(Polygon(sp(x0, y0), sp(x1, y0), sp(x1, y1), sp(x0, y1),
                  color=fill, fill_color=fill, fill_opacity=1, stroke_width=0))
    f.label(sp((x0 + x1) / 2, (y0 + y1) / 2), name, size=19, weight=700,
            color=INK, italic=True)

# ink grid over the fills, outer frame heavier than the two inner cuts
for x0, y0, x1, y1 in [(X0, Y0, X1, Y1)]:
    for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                 ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        f.add(Line(sp(*p), sp(*q), color=INK, stroke_width=4.0))
f.add(Line(sp(XS, Y0), sp(XS, Y1), color=INK, stroke_width=2.6))
f.add(Line(sp(X0, YS), sp(X1, YS), color=INK, stroke_width=2.6))

# side labels: spans a, b along the top, c, d down the left, with small end ticks
def brace(x0, x1, y, label):
    f.add(Line(sp(x0 + 3, y), sp(x1 - 3, y), color=INK, stroke_width=2.0))
    f.add(Line(sp(x0 + 3, y - 5), sp(x0 + 3, y + 5), color=INK, stroke_width=2.0))
    f.add(Line(sp(x1 - 3, y - 5), sp(x1 - 3, y + 5), color=INK, stroke_width=2.0))
    f.label(sp((x0 + x1) / 2, y - 16), label, size=16, weight=700, color=INK, italic=True)

def vbrace(y0, y1, x, label):
    f.add(Line(sp(x, y0 + 3), sp(x, y1 - 3), color=INK, stroke_width=2.0))
    f.add(Line(sp(x - 5, y0 + 3), sp(x + 5, y0 + 3), color=INK, stroke_width=2.0))
    f.add(Line(sp(x - 5, y1 - 3), sp(x + 5, y1 - 3), color=INK, stroke_width=2.0))
    f.label(sp(x - 17, (y0 + y1) / 2), label, size=16, weight=700, color=INK, italic=True)

brace(X0, XS, 48, "a")
brace(XS, X1, 48, "b")
vbrace(Y0, YS, 122, "c")
vbrace(YS, Y1, 122, "d")

print(f.write(str(pathlib.Path(__file__).parent / "fig_9_1.svg")))
