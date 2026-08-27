"""BayesPositive. A 97% accurate test, and a positive result that is almost always wrong.

The hook is the whole ad: a test is 97% accurate, you test positive, do you have it. Almost
everyone answers 97 percent. It is about 3. The answer lands by four seconds rather than at
the end, because a cold viewer decides in two and the payoff has to arrive before the
explanation, not after it.

The argument is carried by natural frequencies, not by the formula. P(A|B) notation is what
makes this feel like a trick; 3,094 squares with 97 of them lime is the same statement and
needs no notation at all. Per 100,000 people at a prevalence of 1 in 1,000:

    100 sick    -> 97 true positives
    99,900 well -> 3% of them wrong = 2,997 false positives
    positives   =  97 + 2,997 = 3,094, of which 97 are real
    97 / 3094   =  3.135...%

Silent on purpose. Feed and Reels autoplay muted, so every claim is on screen as type; there
is nothing here that a soundtrack would carry. That also keeps it off the ElevenLabs cache,
which only holds lines that were actually recorded.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from manim import (DOWN, LEFT, RIGHT, UP, FadeIn, FadeOut, GrowFromEdge, Line, Square,
                   Text, VGroup, Write)

from base import QuanticaScene
from brand import HONEY, SAGE

# Frame is 9.0 scene units wide. Type that overruns it is not clipped by manim, it just
# renders off-canvas, which is how the first cut shipped a headline missing both ends.
# 7.6 of the 9.0 leaves the same generous side margin the landing page uses. 8.1 put the
# hook's widest line hard against both edges.
MAX_W = 7.6

# ---- the arithmetic, computed once and then drawn ---------------------------
POP = 100_000
SICK = POP // 1000            # 100
TP = SICK * 97 // 100         # 97
WELL = POP - SICK             # 99,900
FP = WELL * 3 // 100          # 2,997
POS = TP + FP                 # 3,094

COLS, ROWS = 61, 51           # 3,111 cells, so every positive has a square and 17 sit empty
assert COLS * ROWS >= POS > COLS * (ROWS - 1)


class BayesPositive(QuanticaScene):
    format_name = "reel"
    theme_name = "dark"

    def construct(self):
        t = self.theme
        fd, fb = self.f_display, self.f_body

        def disp(s, size, color=None, weight=None):
            return Text(s, font=fd, font_size=size, color=color or t.ink)

        def body(s, size, color=None):
            return Text(s, font=fb, font_size=size, color=color or t.muted)

        def fit(m, w=MAX_W):
            """Scale a mobject down if it is wider than the frame. Never scales up."""
            if m.width > w:
                m.scale(w / m.width)
            return m

        # ---- hook, on screen inside two seconds --------------------------------
        l1 = disp("A test is", 62)
        l2 = disp("97% accurate.", 92, t.pop)
        l3 = disp("You test positive.", 62)
        l4 = disp("Do you have it?", 62)
        for _m in (l1, l2, l3, l4): fit(_m)
        hook = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.34)
        hook.move_to([0, 1.2, 0])

        self.play(FadeIn(l1, shift=UP * 0.15), run_time=0.35)
        self.play(Write(l2), run_time=0.55)
        self.play(FadeIn(l3, shift=UP * 0.12), run_time=0.32)
        self.play(FadeIn(l4, shift=UP * 0.12), run_time=0.32)

        # the wrong answer, named and struck, which is the tension the ad is built on
        guess = body("Most people say 97%", 44, t.faint)
        guess.next_to(hook, DOWN, buff=0.85)
        strike = Line(guess.get_left() + LEFT * 0.12, guess.get_right() + RIGHT * 0.12,
                      color=HONEY, stroke_width=6)
        self.play(FadeIn(guess), run_time=0.3)
        self.play(Write(strike), run_time=0.3)

        answer = disp("It's about 3%.", 88, t.pop)
        answer.move_to(guess.get_center() + DOWN * 0.55)
        self.play(FadeOut(guess), FadeOut(strike), run_time=0.25)
        self.play(Write(answer), run_time=0.6)
        self.wait(0.7)
        self.play(FadeOut(hook), FadeOut(answer), run_time=0.35)

        # ---- why: every positive result, drawn ---------------------------------
        head = fit(disp(f"{POS:,} people test positive", 50))
        head.move_to([0, 4.55, 0])

        # stroke_width 0 on purpose. 3,094 stroked squares is a lot of geometry for cairo to
        # walk every frame, and at this size the outline is sub-pixel anyway.
        cell = 0.096
        grid = VGroup(*[
            Square(side_length=cell, stroke_width=0,
                   fill_opacity=(1.0 if i < TP else 0.55),
                   fill_color=(t.pop if i < TP else SAGE))
            for i in range(POS)
        ]).arrange_in_grid(rows=ROWS, cols=COLS, buff=cell * 0.30)
        fit(grid, 7.5)
        grid.move_to([0, 0.30, 0])

        self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.4)
        # Growing from the top edge reads as the queue filling up rather than as a picture
        # fading in, and it costs nothing extra to render.
        self.play(GrowFromEdge(grid, UP), run_time=1.5)
        self.wait(0.3)

        # Name both groups under the grid. A left-hand brace needed horizontal room the
        # 9-unit frame does not have, and ran off the canvas in the first cut.
        key_sick = fit(disp(f"{TP} are sick", 46, t.pop))
        key_false = fit(body(f"{FP:,} are false alarms", 42, SAGE))
        keys = VGroup(key_sick, key_false).arrange(DOWN, buff=0.22)
        keys.next_to(grid, DOWN, buff=0.45)
        self.play(FadeIn(key_sick, shift=DOWN * 0.1), run_time=0.35)
        self.play(FadeIn(key_false, shift=DOWN * 0.1), run_time=0.35)
        self.wait(0.4)

        result = fit(disp(f"{TP} / {POS:,} = 3.1%", 62, t.pop))
        result.next_to(keys, DOWN, buff=0.40)
        self.play(Write(result), run_time=0.7)
        self.wait(0.9)

        self.play(FadeOut(VGroup(head, grid, keys, result)), run_time=0.45)

        # ---- the point ---------------------------------------------------------
        p1 = disp("The disease is rare.", 62)
        p2 = body("1 in 1,000", 76, t.pop)
        p3 = body("That matters as much", 44, t.muted)
        p4 = body("as the accuracy.", 44, t.muted)
        for _m in (p1, p2, p3, p4): fit(_m)
        end = VGroup(p1, p2, p3, p4).arrange(DOWN, buff=0.36)
        end.move_to([0, 1.1, 0])
        self.play(FadeIn(p1, shift=UP * 0.12), run_time=0.4)
        self.play(Write(p2), run_time=0.5)
        self.play(FadeIn(p3), FadeIn(p4), run_time=0.45)
        self.wait(0.8)

        mark = self.wordmark(size=52)
        url = body("quanticaedu.com", 36, t.faint)
        sig = VGroup(mark, url).arrange(DOWN, buff=0.22)
        sig.move_to([0, self.safe_bottom + 0.7, 0])
        self.play(FadeIn(sig, shift=UP * 0.15), run_time=0.5)
        self.wait(1.1)
