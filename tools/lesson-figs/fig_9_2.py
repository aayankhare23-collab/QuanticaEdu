"""9.2 Factoring x^2+bx+c. The area model read inside out.

The reverse of 9.1's figure, deliberately the same rectangle in the same four hero
fills so the two lessons read as one picture used in both directions. In 9.1 the
sides were given and the cells were the four products. Here the CELLS are given,
x squared, rx, sx and rs, the expansion's inside, and the two whole side lengths,
x plus r and x plus s, are picked out in gold brackets as the unknowns factoring
recovers. The expanded form is the inside of the rectangle, the factors are its
sides.

The one non-letter glyph is the superscript two in the x squared cell label. It
names the cell and can pre-solve nothing, since every problem's numbers live in
r and s.

Static, like 9.1's. The decomposition is the whole argument and there is no
sequence to perform. Current brand: ink outlines, flat hero fills, square corners,
Space Grotesk, lowercase labels.
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

W, H = 580, 430
PPU = 50.0
FW, FH = W / PPU, H / PPU

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "The area model read inside out. A rectangle is cut into four cells labelled "
    "with the parts of an expanded quadratic, x squared in the largest cell, the "
    "two cross terms r x and s x beside and below it, and r s in the smallest. "
    "The top side carries spans x and r, the left side spans x and s, and two "
    "gold brackets pick out the whole side lengths, x plus r along the top and "
    "x plus s down the left, the factors that factoring recovers from the inside."))


def sp(x, y):
    return f.sp(x, y)


X0, X1, XS = 168, 518, 396
Y0, Y1, YS = 112, 362, 290

cells = [
    (X0, Y0, XS, YS, LAV,  "x²"),
    (XS, Y0, X1, YS, AMBER, "rx"),
    (X0, YS, XS, Y1, MINT, "sx"),
    (XS, YS, X1, Y1, SKY,  "rs"),
]
for x0, y0, x1, y1, fill, name in cells:
    f.add(Polygon(sp(x0, y0), sp(x1, y0), sp(x1, y1), sp(x0, y1),
                  color=fill, fill_color=fill, fill_opacity=1, stroke_width=0))
    f.label(sp((x0 + x1) / 2, (y0 + y1) / 2), name, size=19, weight=700,
            color=INK, italic=True)

for p, q in (((X0, Y0), (X1, Y0)), ((X1, Y0), (X1, Y1)),
             ((X1, Y1), (X0, Y1)), ((X0, Y1), (X0, Y0))):
    f.add(Line(sp(*p), sp(*q), color=INK, stroke_width=4.0))
f.add(Line(sp(XS, Y0), sp(XS, Y1), color=INK, stroke_width=2.6))
f.add(Line(sp(X0, YS), sp(X1, YS), color=INK, stroke_width=2.6))


def brace(x0, x1, y, label, color=INK, width=2.0, size=15):
    f.add(Line(sp(x0 + 3, y), sp(x1 - 3, y), color=color, stroke_width=width))
    f.add(Line(sp(x0 + 3, y - 5), sp(x0 + 3, y + 5), color=color, stroke_width=width))
    f.add(Line(sp(x1 - 3, y - 5), sp(x1 - 3, y + 5), color=color, stroke_width=width))
    f.label(sp((x0 + x1) / 2, y - 15), label, size=size, weight=700, color=INK, italic=True)


def vbrace(y0, y1, x, label, color=INK, width=2.0, size=15):
    f.add(Line(sp(x, y0 + 3), sp(x, y1 - 3), color=color, stroke_width=width))
    f.add(Line(sp(x - 5, y0 + 3), sp(x + 5, y0 + 3), color=color, stroke_width=width))
    f.add(Line(sp(x - 5, y1 - 3), sp(x + 5, y1 - 3), color=color, stroke_width=width))
    f.label(sp(x - 16, (y0 + y1) / 2), label, size=size, weight=700, color=INK, italic=True)


# the sub-spans in ink, close to the rectangle
brace(X0, XS, 88, "x")
brace(XS, X1, 88, "r")
vbrace(Y0, YS, 142, "x")
vbrace(YS, Y1, 142, "s")

# the whole sides in gold, one step out, the two factors being recovered
brace(X0, X1, 46, "x + r", color=AMBER, width=3.6)
vbrace(Y0, Y1, 96, "x + s", color=AMBER, width=3.6)

print(f.write(str(pathlib.Path(__file__).parent / "fig_9_2.svg")))
