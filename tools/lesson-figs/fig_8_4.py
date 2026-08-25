"""8.4 Graphing Inequalities. One convention, shown in both dimensions at once.

The lesson's hinge is that the open circle and the filled circle on a number line ARE
the dashed line and the solid line in the plane, one dimension apart. So the figure is
built as a 2x2 whose columns carry the meaning and whose rows carry the dimension.

    left column   boundary NOT a solution     dashed line   ·   open circle
    right column  boundary IS a solution      solid line    ·   filled circle

Both planes draw the SAME boundary at the SAME angle shading the SAME side. The only
difference anywhere in the top band is the dash. That is deliberate: if the two panels
differed in slope or in which side was shaded, a reader could attribute the excluded
boundary to one of those instead, and the figure would teach nothing. Same for the two
number lines, which differ only in whether the circle is hollow.

Style follows the marketing page's hero and manim/brand.py rather than the retired
blue-and-gold figure kit: near-black outlines at a real weight, flat unmodulated fills,
square corners (--radius is 0 on every Quantica surface), Space Grotesk labels. It is
static on purpose; the reasoning is at the bottom of this file.

No digits anywhere, letters only, so the figure cannot pre-solve a problem in the lesson.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig

# ── palette ────────────────────────────────────────────────────────────────────
# Ink is the marketing hero's own near-black. The fill is its sky. Both columns take
# the SAME fill on purpose, so the eye reads the dash and not the colour.
INK = "#0a0a0a"
SKY = "#7cc7ff"
PAPER = "#ffffff"
FAINT = "#5b6b7a"

W, H = 580, 412
PPU = 50.0
FW, FH = W / PPU, H / PPU

LX, RX = 152, 428            # centres of the two columns
PW, PH = 96, 92              # half-width and half-height of a plane panel
CY = 156                     # y of each plane's origin
NLY = 344                    # y of the number lines
NLR = 100                    # half-length of a number line

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "Four panels in two columns. The left column is headed excluded and the right "
    "column is headed included. In the top row, two identical coordinate planes each "
    "carry the same straight boundary line with the whole region below it filled in. "
    "The left plane draws that boundary as a dashed line, so its own points are not "
    "solutions, and the right plane draws the same boundary as a solid line, so its "
    "points are solutions. In the bottom row, two number lines carry the same "
    "distinction one dimension down. The left one has a hollow circle with everything "
    "to its right shaded, and the right one has a solid filled circle with everything "
    "to its left shaded. Reading down a column, a dashed line and a hollow circle mean "
    "the same thing, and a solid line and a filled circle mean the same thing."))


def sp(x, y):
    return f.sp(x, y)


def tip(x, y, dx, dy, size=7.0, color=INK):
    """A small solid arrowhead pointing along (dx, dy), which is a unit vector."""
    px, py = -dy, dx
    return Polygon(sp(x, y),
                   sp(x - dx * size * 1.9 + px * size * 0.72,
                      y - dy * size * 1.9 + py * size * 0.72),
                   sp(x - dx * size * 1.9 - px * size * 0.72,
                      y - dy * size * 1.9 - py * size * 0.72),
                   color=color, fill_color=color, fill_opacity=1, stroke_width=0)


# ── the boundary, identical in both planes ─────────────────────────────────────
# Chosen to rise to the right and to miss the origin, so neither panel accidentally
# says anything about a boundary through the origin, which the lesson tests later.
# The wash goes BELOW the line. The audit caught the alternative: P5, two blocks
# after this figure, asks above-or-below on a rising boundary and its answer is
# above, so an above-washed figure would be a picture of that answer.
SLOPE = -0.64                # in pixel space, so negative pixel-y is up and to the right
BY0 = -1.5                   # pixel-y offset of the line at the panel centre


def bline(cx, t):
    """Point on the boundary at horizontal offset t from the panel centre."""
    return cx + t, CY + BY0 + SLOPE * t


for cx, dashed in ((LX, True), (RX, False)):
    xa, ya = bline(cx, -PW)
    xb, yb = bline(cx, PW)

    # 1. The half-plane, flat and unmodulated, painted first so the axes sit on top
    #    of it. It runs from the boundary down to the panel edge, which is how the
    #    picture says the region keeps going.
    f.add(Polygon(sp(xa, ya), sp(xb, yb), sp(cx + PW, CY + 96),
                  sp(cx - PW, CY + 96),
                  color=SKY, fill_color=SKY, fill_opacity=1, stroke_width=0))

    # 2. Axes, drawn over the fill so the frame of reference never disappears.
    f.add(Line(sp(cx - PW, CY), sp(cx + PW - 9, CY), color=INK, stroke_width=2.6))
    f.add(Line(sp(cx, CY + PH), sp(cx, CY - PH + 9), color=INK, stroke_width=2.6))
    f.add(tip(cx + PW, CY, 1, 0), tip(cx, CY - PH, 0, -1))
    f.label(sp(cx + PW - 2, CY + 17), "x", size=15, weight=700, color=INK, italic=True)
    f.label(sp(cx + 15, CY - PH + 4), "y", size=15, weight=700, color=INK, italic=True)

    # 3. The boundary, and the only thing the two panels do not share. It is drawn
    #    last so it sits above both the fill and the axes.
    f.add(DashedLine(sp(xa, ya), sp(xb, yb), color=INK, stroke_width=4.4,
                     dash_length=0.19, dashed_ratio=0.56)
          if dashed else
          Line(sp(xa, ya), sp(xb, yb), color=INK, stroke_width=4.4))


# ── the two number lines, differing only in the circle ─────────────────────────
DOT = 8.2
for cx, filled in ((LX, False), (RX, True)):
    mark = cx - 26 if not filled else cx + 26
    end = cx + NLR if not filled else cx - NLR

    # The bare line first, complete with both arrowheads, then the solution set as a
    # thick band laid OVER it in the same fill the region above uses. Painting the
    # band under the line instead leaves the ink stroke splitting it lengthwise, which
    # reads as a line with blue edges rather than as a stretch that is shaded.
    f.add(Line(sp(cx - NLR + 8, NLY), sp(cx + NLR - 8, NLY), color=INK, stroke_width=2.6))
    f.add(tip(cx + NLR, NLY, 1, 0, size=6.2), tip(cx - NLR, NLY, -1, 0, size=6.2))
    f.add(Line(sp(mark, NLY), sp(end - (14 if not filled else -14), NLY),
               color=SKY, stroke_width=13))
    f.add(Circle(radius=DOT / PPU, color=INK, stroke_width=2.8,
                 fill_color=(INK if filled else PAPER), fill_opacity=1)
          .move_to(sp(mark, NLY)))


# ── the rule between the bands, and the words ──────────────────────────────────
f.add(Line(sp(40, 288), sp(W - 40, 288), color=INK, stroke_width=2.6))
f.add(Line(sp(W / 2, 62), sp(W / 2, 262), color="#c3d2e0", stroke_width=2.0))
f.add(Line(sp(W / 2, 312), sp(W / 2, 392), color="#c3d2e0", stroke_width=2.0))

f.label(sp(LX, 36), "excluded", size=17, weight=700, color=INK)
f.label(sp(RX, 36), "included", size=17, weight=700, color=INK)
f.label(sp(LX, 266), "dashed", size=14, weight=500, color=FAINT)
f.label(sp(RX, 266), "solid", size=14, weight=500, color=FAINT)
f.label(sp(LX, 386), "open", size=14, weight=500, color=FAINT)
f.label(sp(RX, 386), "filled", size=14, weight=500, color=FAINT)


# ── why nothing moves here ─────────────────────────────────────────────────────
# This figure is deliberately static, unlike the chapter's other three. It is a
# side-by-side comparison, and the whole argument is that all four panels are on
# screen together: dashed sits above open, solid sits above filled, and the reader
# checks the columns against each other. An earlier cut had each boundary stroke
# draw on, staggered, which meant the right column was empty for the first stretch
# of every loop and a reader glancing at the wrong moment saw half an argument. A
# reveal also has the fill arriving before its own boundary, which is backwards from
# how the region is actually found. There is no motion here that teaches, so there
# is none.

print(f.write(str(pathlib.Path(__file__).parent / "fig_8_4.svg")))
