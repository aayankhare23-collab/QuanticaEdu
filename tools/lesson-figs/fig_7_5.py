"""7.5 Intercepts and Standard Forms. The two intercepts are the two cheapest points.

Two bands. Top: a coordinate plane with a marked origin, the line 3x + 5y = 15, and
its two crossings marked as gold dots labelled with their values and with the
lowercase words x-intercept and y-intercept. Below a full-width hairline, the two
substitutions that produce those values, each one division.

Three deliberate choices:

* The top band is ANIMATED in three beats, using the same Fig.frames mechanism as
  fig_7_3. Beat one is the bare plane, beat two puts the two dots on the axes, beat
  three grows the line through them. A static picture shows two dots sitting on a
  line that is already there, which reads as the dots being consequences of the line.
  The claim is the reverse, two points first and the line second, and it cannot be
  written as text inside the SVG. Drawing it in that order is the only way to say it.
* The hairline background grid stays rather than becoming sparse ticks. fig_7_1,
  fig_7_2, fig_7_3 and fig_7_4 all carry it, it is the lightest element on the card,
  and it is what lets a reader read 5 and 3 straight off the axes. A bespoke tick
  system would make 7.5 the one figure in the chapter with a different grammar for
  the same information.
* Frame width stays 14.0 and a grid square stays 32 px, so every stroke width and dot
  radius inherited from the rest of chapter 7 is unchanged. Only the frame HEIGHT
  grows, to make room for band two.

The line 3x + 5y = 15, its intercepts 5 and 3, and its slope -3/5 appear in no problem
and in no review item of 7.5. The only value the figure prints at or above 12 is 15, and
check_lesson.py's collision rule needs two or more shared values at or above 12 to fire.
"""
import collections, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from manim import *
from manim_figs import (Fig, BLUE, BLUE_DEEP, GOLD, GOLD_MID, GOLD_DEEP, SLATE,
                        HAIRLINE, WHITE)

A_, B_, C_ = 3, 5, 15             # the line 3x + 5y = 15; appears in no problem
XI, YI = C_ // A_, C_ // B_       # 5 and 3, the two intercepts
M = -A_ / B_                      # -3/5

W = 580                           # canvas width in px
PPU = W / 14.0                    # px per scene unit, 41.43, same as 7.1 to 7.4
H = 506                           # canvas height in px
FW, FH = W / PPU, H / PPU         # 14.0 x 12.214
STEP = 32.0 / PPU                 # one grid square, 32 px

GOLD_EDGE = "#e0a52a"
PILL = "#eaf1ff"
PILL_EDGE = "#cdddf7"


def sp(x, y):
    """px on the 580x506 canvas -> scene coordinates."""
    return np.array([(x - W / 2) / PPU, (H / 2 - y) / PPU, 0.0])


f = Fig(width=W, frame_width=FW, frame_height=FH, aria=(
    "Two bands. In the top band, a coordinate plane with a marked origin and the line "
    "three x plus five y equals fifteen, which falls to the right. Two gold dots are "
    "placed on the axes first, one on the horizontal axis at five and one on the "
    "vertical axis at three, each labelled with its value and with the lowercase words "
    "x-intercept and y-intercept, and then the blue line is drawn through both of them. "
    "Below a full-width hairline, the two substitutions that gave those values. Setting "
    "y to zero leaves three x equals fifteen, so x is five, and setting x to zero leaves "
    "five y equals fifteen, so y is three."))

# ---- band one, the line and its two crossings ---------------------------
f.label(sp(48, 20), "two crossings", size=13, weight=700, color=BLUE, anchor="start")

plane = NumberPlane(
    x_range=[-6, 8, 1], y_range=[-2, 6, 1], x_length=14 * STEP, y_length=8 * STEP,
    background_line_style={"stroke_color": HAIRLINE, "stroke_width": 2, "stroke_opacity": 1},
    axis_config={"stroke_color": SLATE, "stroke_width": 3.2, "include_tip": True,
                 "tip_width": 0.19, "tip_height": 0.23}).move_to(sp(290, 176))
f.add(plane)

f.add(Dot(plane.c2p(0, 0), radius=0.09, color=SLATE, stroke_width=0))
f.label(plane.c2p(0, 0), "0", size=12, weight=500, color=SLATE,
        anchor="end", dx=-9, dy=15)
f.label(plane.c2p(8, 0), "x", size=15, weight=700, color=SLATE, italic=True, dx=6, dy=15)
f.label(plane.c2p(0, 6), "y", size=15, weight=700, color=SLATE, italic=True, dx=-14, dy=-3)
f.label(plane.c2p(-5.4, 2.0), "3x + 5y = 15", size=15, weight=700, color=BLUE_DEEP,
        anchor="start")

# the line, clipped to the grid; it exits through the top edge and the right edge
SX, SY = -4.95, M * -4.95 + YI
EX, EY = 7.90, M * 7.90 + YI


def beat(t):
    """Three beats. Bare axes, then the two dots, then the line grown through them."""
    mobs, labs = [], []
    show_x = t >= 0.13                       # x-intercept, from setting y = 0
    show_y = t >= 0.25                       # y-intercept, from setting x = 0
    grow = min(1.0, max(0.0, (t - 0.39) / 0.42))

    if grow > 0.02:                          # drawn first, so the dots sit on top
        mobs.append(Line(plane.c2p(SX, SY),
                         plane.c2p(SX + grow * (EX - SX), SY + grow * (EY - SY)),
                         color=BLUE, stroke_width=5))

    if show_x:
        mobs += [Dot(plane.c2p(XI, 0), radius=0.115, color=WHITE, stroke_width=0),
                 Dot(plane.c2p(XI, 0), radius=0.095, color=GOLD_MID, stroke_width=0)]
        labs += [f.mklabel(plane.c2p(XI, 0), "x-intercept", size=12, weight=700,
                           color=GOLD_DEEP, anchor="end", dx=-8, dy=22),
                 f.mklabel(plane.c2p(XI, 0), str(XI), size=13, weight=700, color=SLATE,
                           anchor="start", dx=9, dy=-14)]
    if show_y:
        mobs += [Dot(plane.c2p(0, YI), radius=0.115, color=WHITE, stroke_width=0),
                 Dot(plane.c2p(0, YI), radius=0.095, color=GOLD_MID, stroke_width=0)]
        labs += [f.mklabel(plane.c2p(0, YI), "y-intercept", size=12, weight=700,
                           color=GOLD_DEEP, anchor="start", dx=14, dy=-16),
                 f.mklabel(plane.c2p(0, YI), str(YI), size=13, weight=700, color=SLATE,
                           anchor="end", dx=-14, dy=6)]
    return mobs, labs


f.frames(beat, n=30, dur=7.0)

# ---- the hairline, full width -------------------------------------------
f.add(Line(sp(42, 344), sp(538, 344), color=HAIRLINE, stroke_width=3.0))

# ---- band two, each crossing as one division ----------------------------
f.label(sp(48, 368), "one division each", size=13, weight=700, color=BLUE, anchor="start")


def pill(cx, cy, w, fill, edge):
    return RoundedRectangle(corner_radius=15 / PPU, width=w / PPU, height=44 / PPU,
                            fill_color=fill, fill_opacity=1, stroke_color=edge,
                            stroke_width=3.0).move_to(sp(cx, cy))


def row(cy, sub, left, out):
    f.add(pill(140, cy, 96, GOLD, GOLD_EDGE), pill(444, cy, 96, PILL, PILL_EDGE))
    f.label(sp(140, cy), sub, size=16, weight=700, color=GOLD_DEEP)
    f.add(Arrow(sp(200, cy), sp(236, cy), buff=0, color=BLUE, stroke_width=3.6,
                tip_length=0.20, max_tip_length_to_length_ratio=0.5))
    f.label(sp(292, cy), left, size=17, weight=700, color=SLATE)
    f.add(Arrow(sp(348, cy), sp(384, cy), buff=0, color=BLUE, stroke_width=3.6,
                tip_length=0.20, max_tip_length_to_length_ratio=0.5))
    f.label(sp(444, cy), out, size=16, weight=700, color=BLUE_DEEP)


row(412, "y = 0", f"{A_}x = {C_}", f"x = {XI}")
row(468, "x = 0", f"{B_}y = {C_}", f"y = {YI}")


# ---- shrink ------------------------------------------------------------
# Fig.frames emits every frame as a full redraw, so the two dots and their four
# labels are written out thirty times over, at cairo's full precision. That is
# 90 KB for a picture with one moving part. Neither of the two passes below
# changes a rendered pixel by more than a hundredth of a px. They belong in
# manim_figs.py eventually; they live here so that applying 7.5 does not silently
# rewrite the already-shipped 7.3 figure.

def shrink(svg, uid, places=3):
    """Round coordinates, then hoist repeated elements into defs and reuse them.

    The <style> block is held out of the rounding. Its keyframe stops are 3.3333%
    and 3.3334%, one hundred-thousandth of a percent apart on purpose, and rounding
    collapses them onto each other, which turns each frame's hard cut into a fade
    across its whole slot.
    """
    cut = svg.index('</style>') + len('</style>') if '</style>' in svg else 0
    head, body = svg[:cut], svg[cut:]
    body = re.sub(r'\d+\.\d{4,}',
                  lambda m: f'{float(m.group()):.{places}f}'.rstrip('0').rstrip('.'), body)
    svg = head + body
    dup = collections.Counter(
        re.findall(r'<path\b[^>]*/>|<text\b[^>]*>[^<]*</text>', svg))
    defs = []
    for el, n in dup.items():
        if n < 3:
            continue
        eid = f'{uid}r{len(defs)}'
        cut = el.index('/>') if el.endswith('/>') else el.index('>')
        defs.append(el[:cut] + f' id="{eid}"' + el[cut:])
        svg = svg.replace(el, f'<use href="#{eid}"/>')
    if defs:
        head = svg.index('>') + 1
        svg = svg[:head] + '<defs>' + ''.join(defs) + '</defs>' + svg[head:]
    return svg.replace('\n', '')      # cairo's one-path-per-line, no label spans one


out = pathlib.Path(__file__).parent / "fig_7_5.svg"
small = shrink(f.svg(), f.uid)
out.write_text(small, encoding="utf-8")
print(out, len(small), "bytes")
