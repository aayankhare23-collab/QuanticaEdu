"""9.3 Factoring ax^2+bx+c. The cross diagram of the candidate check.

The two binomials stacked as term tokens, px and q above, rx and s below. Three
readings come off the arrangement. The left column multiplies to the leading
coefficient, the right column to the constant, and the two diagonals, picked out
in gold, are the cross products whose SUM must hit the middle coefficient. The
columns are constraints a candidate satisfies by construction, the middle is
where it passes or fails, which is why the diagonals carry the color.

Letters only, no digits, collision-proof by construction. Static, since the
three readings are simultaneous facts about one arrangement, not a sequence.
Current brand: ink strokes and text, hero amber for the diagonals, Space
Grotesk, square corners, no boxes.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from manim import *
from manim_figs import Fig

INK = "#0a0a0a"
AMBER = "#ffc84d"
FAINT = "#5b6b7a"

W, H = 580, 320
PPU = 50.0
FW, FH = W / PPU, H / PPU

f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "The cross diagram for checking one factoring candidate. The terms p x and q "
    "sit in a top row, r x and s below them. The left column's product p r gives "
    "the leading coefficient a, the right column's product q s gives the constant "
    "c, and two gold diagonal strokes cross in the middle, the cross products p s "
    "and q r, whose sum must give the middle coefficient b. The columns hold by "
    "construction and the middle is where a candidate passes or fails."))


def sp(x, y):
    return f.sp(x, y)


LXc, RXc = 178, 402          # the two token columns
TY, BY = 84, 192             # the two rows

# the four term tokens and the plus signs
f.label(sp(LXc, TY), "px", size=27, weight=700, color=INK, italic=True)
f.label(sp(RXc, TY), "q", size=27, weight=700, color=INK, italic=True)
f.label(sp(LXc, BY), "rx", size=27, weight=700, color=INK, italic=True)
f.label(sp(RXc, BY), "s", size=27, weight=700, color=INK, italic=True)
f.label(sp((LXc + RXc) / 2, TY), "+", size=20, weight=500, color=FAINT)
f.label(sp((LXc + RXc) / 2, BY), "+", size=20, weight=500, color=FAINT)

# the two column strokes, plain ink, constraints met by construction
f.add(Line(sp(LXc, TY + 26), sp(LXc, BY - 26), color=INK, stroke_width=3.0))
f.add(Line(sp(RXc, TY + 26), sp(RXc, BY - 26), color=INK, stroke_width=3.0))

# the two diagonals, gold, crossing between the columns
f.add(Line(sp(LXc + 30, TY + 18), sp(RXc - 22, BY - 16), color=AMBER, stroke_width=5.2))
f.add(Line(sp(LXc + 30, BY - 18), sp(RXc - 22, TY + 16), color=AMBER, stroke_width=5.2))

# the three readings
f.label(sp(LXc, BY + 48), "pr = a", size=17, weight=700, color=INK, italic=True)
f.label(sp(RXc, BY + 48), "qs = c", size=17, weight=700, color=INK, italic=True)
f.label(sp((LXc + RXc) / 2, BY + 86), "ps + qr = b", size=18, weight=700, color=INK,
        italic=True)
f.add(Line(sp((LXc + RXc) / 2 - 62, BY + 103), sp((LXc + RXc) / 2 + 62, BY + 103),
           color=AMBER, stroke_width=5.2))

print(f.write(str(pathlib.Path(__file__).parent / "fig_9_3.svg")))
