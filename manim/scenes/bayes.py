"""BayesPositive. A 97% accurate test whose positive result is usually wrong.

An educational cut rather than a three-beat ad: it builds the whole mechanism, then runs the
same test against a common disease to show that the test was never the variable.

    RARE, 1 in 1,000, per 100,000 people
        100 sick     ->    97 true positives
        99,900 well  -> 2,997 false positives
        97 / 3,094   =  3.1%,  so about 3 of every 100 positives are real

    COMMON, 1 in 10, per 1,000 people
        100 sick     ->    97 true positives
        900 well     ->    27 false positives
        97 / 124     = 78.2%, so about 78 of every 100 positives are real

Both have exactly 97 true positives, because both have 100 sick people and the same test.
Only the healthy crowd changes size, so the false alarms collapse and the same test goes from
3% right to 78% right. That is the lesson, and the second half exists to show it.

WHY THE PEOPLE ARE DRAWN IN HUNDREDS. The natural-frequency numbers run to 3,094, and 3,094
person icons at this frame width are ten pixels each, which is a smear rather than a crowd.
"Out of every 100 who test positive" is the same statement, is literally what a percentage
means, and puts the figures at a size where a person still reads as a person. The exact
arithmetic is still shown as type; only the drawn crowd is scaled to 100.

Silent on purpose. Feed and Reels autoplay muted, so every claim is on screen as type. That
also keeps it off the ElevenLabs cache, which holds only lines that were actually recorded.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from manim import (DOWN, LEFT, PI, RIGHT, UP, Circle, FadeIn, FadeOut, Line, Sector,
                   Text, VGroup, Write)

from base import QuanticaScene
from brand import HONEY, SAGE

# 7.6 of the 9.0 frame leaves the side margin the landing page uses. manim does not clip
# type that overruns the frame, it draws it off-canvas, so everything gets fit().
MAX_W = 7.6

ACC = 97                                        # percent, sensitivity and specificity alike

RARE_N, RARE_SICK = 100_000, 100                # 1 in 1,000
RARE_WELL = RARE_N - RARE_SICK                  # 99,900
TP = RARE_SICK * ACC // 100                     # 97
RARE_FP = RARE_WELL * (100 - ACC) // 100        # 2,997
RARE_POS = TP + RARE_FP                         # 3,094

COMMON_N, COMMON_SICK = 1_000, 100              # 1 in 10, deliberately the SAME 100 sick
COMMON_WELL = COMMON_N - COMMON_SICK            # 900
COMMON_FP = COMMON_WELL * (100 - ACC) // 100    # 27
COMMON_POS = TP + COMMON_FP                     # 124

assert COMMON_SICK * ACC // 100 == TP, "both scenarios must share their 97 true positives"

# per 100 positive results, which is what the icon grid draws
RARE_IN_100 = round(TP * 100 / RARE_POS)        # 3
COMMON_IN_100 = round(TP * 100 / COMMON_POS)    # 78
assert (RARE_IN_100, COMMON_IN_100) == (3, 78)

GRID_COLS = 10


def person(color, opacity=1.0):
    """One figure: a circular head over a domed pair of shoulders, with a neck gap.

    Two filled mobjects and no stroke, so a hundred of them stay cheap for cairo. Sector
    with angle PI is a half disc whose flat side sits at the bottom, which is the shoulder
    line; building it from an Arc would need closing by hand and fills unreliably.
    """
    body = Sector(radius=0.50, angle=PI, start_angle=0)
    body.set_fill(color, opacity).set_stroke(width=0)
    head = Circle(radius=0.30).set_fill(color, opacity).set_stroke(width=0)
    head.move_to([0, 0.50 + 0.09 + 0.30, 0])
    return VGroup(body, head)


class BayesPositive(QuanticaScene):
    format_name = "reel"
    theme_name = "dark"

    def construct(self):
        t = self.theme
        fd, fb = self.f_display, self.f_body

        def disp(s, size, color=None):
            return Text(s, font=fd, font_size=size, color=color or t.ink)

        def body(s, size, color=None):
            return Text(s, font=fb, font_size=size, color=color or t.muted)

        def fit(m, w=MAX_W):
            if m.width > w:
                m.scale(w / m.width)
            return m

        def show(m, rt=0.4, shift=UP * 0.12):
            self.play(FadeIn(m, shift=shift), run_time=rt)

        def crowd(n=100):
            """Sized by HEIGHT, not width. Ten rows of figures are much taller than they are
            wide, so fitting to the frame width let the top row run up into the headline."""
            g = VGroup(*[person(SAGE, 0.55) for _ in range(n)])
            g.arrange_in_grid(cols=GRID_COLS, buff=0.20)
            g.scale(7.0 / g.height)
            if g.width > 6.6:
                g.scale(6.6 / g.width)
            return g

        # ---- 1. the hook -------------------------------------------------------
        l1 = fit(disp("A test for a disease", 56))
        l2 = fit(disp(f"is {ACC}% accurate.", 84, t.pop))
        l3 = fit(disp("You test positive.", 60))
        l4 = fit(disp("Do you have it?", 60))
        hook = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.36).move_to([0, 1.7, 0])
        show(l1, 0.4, UP * 0.15)
        self.play(Write(l2), run_time=0.6)
        self.wait(0.4)
        show(l3, 0.35)
        show(l4, 0.35)
        self.wait(1.0)

        guess = fit(body("Most people say 97%", 46, t.faint))
        guess.next_to(hook, DOWN, buff=0.85)
        show(guess, 0.35, UP * 0.0)
        self.wait(0.6)
        strike = Line(guess.get_left() + LEFT * 0.14, guess.get_right() + RIGHT * 0.14,
                      color=HONEY, stroke_width=6)
        self.play(Write(strike), run_time=0.35)
        self.wait(0.5)

        answer = fit(disp("It's about 3%.", 88, t.pop))
        answer.move_to(guess.get_center() + DOWN * 0.6)
        self.play(FadeOut(guess), FadeOut(strike), run_time=0.3)
        self.play(Write(answer), run_time=0.7)
        self.wait(1.3)
        self.play(FadeOut(hook), FadeOut(answer), run_time=0.4)

        # ---- 2. the variable the test cannot see -------------------------------
        w = VGroup(fit(disp("The answer depends on", 52)),
                   fit(disp("something the test", 52)),
                   fit(disp("never sees.", 52, t.pop))
                   ).arrange(DOWN, buff=0.3).move_to([0, 1.5, 0])
        for m in w:
            show(m, 0.35)
        self.wait(0.9)

        rare = fit(body("How rare the disease is.", 50, t.ink))
        rare.next_to(w, DOWN, buff=0.85)
        rate = fit(disp("1 in 1,000", 84, t.pop))
        rate.next_to(rare, DOWN, buff=0.42)
        show(rare, 0.4)
        self.play(Write(rate), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(w), FadeOut(rare), FadeOut(rate), run_time=0.4)

        # ---- 3. where the false alarms come from -------------------------------
        pop = fit(disp(f"Test {RARE_N:,} people.", 56))
        pop.move_to([0, 4.4, 0])
        show(pop, 0.45, DOWN * 0.12)
        self.wait(0.5)

        r1 = VGroup(fit(disp(f"{RARE_SICK} have it", 50, t.pop)),
                    fit(body(f"the test catches {TP}", 40))).arrange(DOWN, buff=0.24)
        r2 = VGroup(fit(disp(f"{RARE_WELL:,} do not", 50, SAGE)),
                    fit(body(f"but 3% of them still", 40)),
                    fit(body(f"test positive, and 3% of", 40)),
                    fit(body(f"{RARE_WELL:,} is {RARE_FP:,}", 40, t.ink))).arrange(DOWN, buff=0.2)
        rows = VGroup(r1, r2).arrange(DOWN, buff=0.95).move_to([0, 0.9, 0])
        show(r1, 0.5)
        self.wait(1.1)
        show(r2, 0.5)
        self.wait(1.6)

        pg = VGroup(fit(disp("3% of a huge group beats", 44)),
                    fit(disp(f"{ACC}% of a tiny one.", 44, t.pop))
                    ).arrange(DOWN, buff=0.24)
        pg.next_to(rows, DOWN, buff=0.8)
        for m in pg:
            show(m, 0.4)
        self.wait(1.7)
        self.play(FadeOut(pop), FadeOut(rows), FadeOut(pg), run_time=0.4)

        # ---- 4. every positive result, as people -------------------------------
        sums = VGroup(fit(body(f"{TP} real  +  {RARE_FP:,} false alarms", 44, t.ink)),
                      fit(disp(f"{TP} / {RARE_POS:,} = 3.1%", 62, t.pop))
                      ).arrange(DOWN, buff=0.42).move_to([0, 1.2, 0])
        show(sums[0], 0.45)
        self.wait(0.9)
        self.play(Write(sums[1]), run_time=0.7)
        self.wait(1.5)
        self.play(FadeOut(sums), run_time=0.35)

        head = fit(disp("Of every 100 who", 50))
        head2 = fit(disp("test positive...", 50))
        hg = VGroup(head, head2).arrange(DOWN, buff=0.2)
        hg.move_to([0, self.safe_top - hg.height / 2 - 0.1, 0])
        show(head, 0.4, DOWN * 0.12)
        show(head2, 0.35, DOWN * 0.12)

        people = crowd()
        people.next_to(hg, DOWN, buff=0.45)
        self.play(FadeIn(people, lag_ratio=0.004), run_time=1.8)
        self.wait(0.7)

        lit = VGroup(*people[:RARE_IN_100])
        self.play(*[p.animate.set_fill(t.pop, 1.0) for p in lit], run_time=0.9)
        cap = fit(disp(f"...only {RARE_IN_100} really have it.", 50, t.pop))
        cap.next_to(people, DOWN, buff=0.6)
        show(cap, 0.45, DOWN * 0.12)
        self.wait(2.0)

        # ---- 5. same test, common disease --------------------------------------
        self.play(FadeOut(cap), run_time=0.3)
        swap = VGroup(fit(disp("Same test.", 54)),
                      fit(disp("Now 1 in 10 has it.", 54, t.pop))
                      ).arrange(DOWN, buff=0.24)
        swap.next_to(people, DOWN, buff=0.55)
        for m in swap:
            show(m, 0.4, DOWN * 0.1)
        self.wait(1.3)

        more = VGroup(*people[RARE_IN_100:COMMON_IN_100])
        self.play(*[p.animate.set_fill(t.pop, 1.0) for p in more], run_time=1.5)
        self.wait(0.5)
        cap2 = fit(disp(f"{COMMON_IN_100} really have it.", 54, t.pop))
        cap2.move_to(swap.get_center())
        self.play(FadeOut(swap), run_time=0.3)
        show(cap2, 0.45, DOWN * 0.12)
        self.wait(0.8)

        math2 = fit(body(f"{TP} real, only {COMMON_FP} false alarms  ->  {TP}/{COMMON_POS} = 78%", 36))
        math2.next_to(cap2, DOWN, buff=0.4)
        show(math2, 0.45)
        self.wait(2.0)

        # ---- 6. the point ------------------------------------------------------
        self.play(FadeOut(VGroup(hg, people, cap2, math2)), run_time=0.5)
        e = VGroup(fit(disp("Nothing about the", 54)),
                   fit(disp("test changed.", 54)),
                   fit(body("Only how rare it was.", 46, t.pop))
                   ).arrange(DOWN, buff=0.32).move_to([0, 1.4, 0])
        show(e[0], 0.4)
        show(e[1], 0.35)
        self.wait(0.6)
        show(e[2], 0.5)
        self.wait(1.8)

        sig = VGroup(self.wordmark(size=52), body("quanticaedu.com", 36, t.faint)
                     ).arrange(DOWN, buff=0.22)
        sig.move_to([0, self.safe_bottom + 0.7, 0])
        show(sig, 0.5, UP * 0.15)
        self.wait(1.4)
