"""BayesPositive. A 99% accurate test whose positive result is a coin flip.

Visual first. The crowd carries the argument and the type stays small and out of the way,
because the previous cut explained everything in captions and the pictures were decoration.

    1% of 100 people have it        ->  1 person is sick
    the test is 99% accurate        ->  that 1 sick person tests positive
    1% of the 99 healthy are flagged->  1 healthy person also tests positive
    so 2 test positive, 1 is real   ->  1/2

The answer is EXACTLY one half, not approximately. Sensitivity and specificity are both 99%
and prevalence is 1%, so the true-positive weight 0.01 x 0.99 and the false-positive weight
0.99 x 0.01 are the same number. That symmetry is the whole reason this version of the
problem is the one worth animating: the punchline is a coin flip, not a decimal.

Palette is typeset.LIGHT, the same one the Pythagoras and circle-area reels use: cream
ground, ink type, and lime as a highlighter SURFACE rather than as type. Lime on cream has
too little contrast to be read as a letterform, which is why the payoff figure is a lime
fill behind an ink outline instead of lime text.

NARRATION. This is an organic piece rather than a cold ad, so it is narrated, and the
voiceover drives the timing: each beat sits inside a self.voiceover() block and the visuals
are held until the line finishes. Every line here is NEW, so it is not in manim/voiceovers/
and the first render needs ELEVENLABS_API_KEY exported once. After that the takes are cached
and committed and no further render needs a key. QUANTICA_VOICE=macos renders a keyless
local-voice version for checking pacing; those takes are keyed by provider so they can never
overwrite the ElevenLabs ones.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from manim import (DOWN, LEFT, PI, RIGHT, UP, Circle, FadeIn, FadeOut, Indicate, Sector,
                   Square, Text, VGroup, Write)
from manim_voiceover import VoiceoverScene

from base import QuanticaScene
from voice import QuanticaVoice
from brand import HONEY, INK, LIME, SAGE
from typeset import LIGHT as AD

MAX_W = 7.6

N = 100                 # the whole population, drawn
SICK_AT = 34            # mid-crowd, so it does not read as a special first slot
FALSE_AT = 71
PREV, ACC = 1, 99       # percent
SICK = N * PREV // 100                      # 1
WELL = N - SICK                             # 99
FALSE_POS = round(WELL * (100 - ACC) / 100)  # 1
POSITIVES = SICK + FALSE_POS                # 2

assert (SICK, FALSE_POS, POSITIVES) == (1, 1, 2)

# Narration. These strings ARE the voiceover cache keys, byte for byte, so editing one
# invalidates its take and the next render needs ELEVENLABS_API_KEY again. Numbers are
# spelled out because the engine reads "99%" as "ninety nine percent sign" often enough
# to matter, and a stray symbol in a cache key is hard to spot later.
SAY = [
    "Suppose one percent of people have a disease, and there is a test for it that is "
    "ninety nine percent accurate.",
    "You take the test and it comes back positive. Are you ninety nine percent sure you "
    "have it?",
    "Let's line up a hundred people and find out.",
    "One percent of them, so one person, actually has the disease.",
    "The test is ninety nine percent accurate, so it catches them.",
    "But ninety nine percent accurate cuts both ways. One in every hundred healthy people "
    "gets flagged by mistake.",
    "So one of the ninety nine healthy people tests positive too.",
    "Now look at everyone the test flagged. Two people, and only one of them is sick.",
    "Your odds are one in two. A coin flip, not ninety nine percent.",
    "The test did not lie. Almost nobody had the disease to begin with, so the handful of "
    "false alarms is just as big as the real cases.",
]



def person(color, opacity=1.0, outline=None, sw=0):
    """A circular head over domed shoulders.

    On the cream ground a plain lime fill washes out, so the two people who matter get an
    ink outline and the crowd does not. That is the same figure/ground trick the Milo reels
    use: lime is a surface, ink is the edge.
    """
    body = Sector(radius=0.50, angle=PI, start_angle=0)
    body.set_fill(color, opacity).set_stroke(outline or color, sw)
    head = Circle(radius=0.30).set_fill(color, opacity).set_stroke(outline or color, sw)
    head.move_to([0, 0.89, 0])
    return VGroup(body, head)


class BayesPositive(QuanticaScene, VoiceoverScene):
    """QuanticaScene first in the MRO, so its frame sizing, theme and font registration win.

    VoiceoverScene contributes voiceover() and the speech service. It defines no setup() of
    its own, so QuanticaScene.setup is called explicitly and the service attached after it.
    """

    format_name = "reel"
    theme_name = "light"

    def setup(self):
        QuanticaScene.setup(self)
        self.set_speech_service(QuanticaVoice())

    def construct(self):
        t = self.theme
        fd, fb = self.f_display, self.f_body

        def disp(s, size, color=None):
            return Text(s, font=fd, font_size=size, color=color or AD.ink)

        # Captions are deliberately small and muted. The crowd is the argument; type that
        # competes with it is what made the previous cut read as a slide deck.
        def note(s, size=38, color=None):
            return Text(s, font=fb, font_size=size, color=color or AD.gray)

        def fit(m, w=MAX_W):
            if m.width > w:
                m.scale(w / m.width)
            return m

        def show(m, rt=0.4, shift=UP * 0.1):
            self.play(FadeIn(m, shift=shift), run_time=rt)

        def marker(fig, color):
            """Square outline, because the brand has no rounded corners anywhere."""
            r = Square(side_length=fig.height * 1.18, stroke_width=6, color=color)
            r.set_fill(opacity=0).move_to(fig.get_center())
            return r

        # ---- 1. the hook -------------------------------------------------------
        h = VGroup(
            fit(disp("1% of people", 58)),
            fit(disp("have a disease.", 58)),
        ).arrange(DOWN, buff=0.22).move_to([0, 3.1, 0])
        with self.voiceover(text=SAY[0]):
            for m in h:
                show(m, 0.4)

        h2 = VGroup(
            fit(disp("A test for it is", 58)),
            fit(disp("99% accurate.", 84, AD.ink)),
        ).arrange(DOWN, buff=0.26)
        h2.next_to(h, DOWN, buff=0.75)
        show(h2[0], 0.4)
        self.play(Write(h2[1]), run_time=0.6)

        h3 = VGroup(
            fit(disp("You test positive.", 58)),
            fit(disp("Are you 99% sure?", 62, HONEY)),
        ).arrange(DOWN, buff=0.26)
        h3.next_to(h2, DOWN, buff=0.85)
        with self.voiceover(text=SAY[1]):
            show(h3[0], 0.4)
            show(h3[1], 0.45)
        self.play(FadeOut(h), FadeOut(h2), FadeOut(h3), run_time=0.45)

        # ---- 2. the crowd ------------------------------------------------------
        cap = note("100 people", 40)
        cap.move_to([0, self.safe_top - 0.4, 0])
        show(cap, 0.4, DOWN * 0.1)

        people = VGroup(*[person(AD.slate, 0.40) for _ in range(N)])
        people.arrange_in_grid(cols=10, buff=0.20)
        people.scale(7.6 / people.height)          # sized by height; ten rows are tall
        if people.width > 6.6:
            people.scale(6.6 / people.width)
        people.next_to(cap, DOWN, buff=0.5)
        with self.voiceover(text=SAY[2]):
            self.play(FadeIn(people, lag_ratio=0.006), run_time=1.6)

        # ---- 3. one of them is actually sick -----------------------------------
        sick = people[SICK_AT]
        c1 = note("1 actually has it", 38, AD.ink)
        c1.next_to(people, DOWN, buff=0.45)
        with self.voiceover(text=SAY[3]):
            self.play(sick.animate.set_fill(LIME, 1.0), run_time=0.7)
            self.play(Indicate(sick, scale_factor=1.35, color=LIME), run_time=0.8)
            show(c1, 0.4, DOWN * 0.1)

        # ---- 4. run the test ---------------------------------------------------
        self.play(FadeOut(c1), run_time=0.3)
        c2 = note("the test flags them", 38)
        c2.next_to(people, DOWN, buff=0.45)
        m_sick = marker(sick, INK)
        with self.voiceover(text=SAY[4]):
            show(c2, 0.35, DOWN * 0.1)
            self.play(Write(m_sick), run_time=0.6)

        # the 1% that is easy to forget: 1 in every 100 healthy people is flagged too
        self.play(FadeOut(c2), run_time=0.3)
        c3 = VGroup(note("but 99% accurate also means", 34),
                    note("1 in 100 healthy people is flagged", 34, HONEY)
                    ).arrange(DOWN, buff=0.16)
        c3.next_to(people, DOWN, buff=0.42)
        with self.voiceover(text=SAY[5]):
            show(c3, 0.45, DOWN * 0.1)

        false_p = people[FALSE_AT]
        m_false = marker(false_p, HONEY)
        with self.voiceover(text=SAY[6]):
            self.play(false_p.animate.set_fill(HONEY, 1.0), run_time=0.4)
            self.play(Write(m_false), run_time=0.6)
            self.play(Indicate(false_p, scale_factor=1.35, color=HONEY), run_time=0.8)

        # ---- 5. pull the two positives out of the crowd ------------------------
        self.play(FadeOut(c3), run_time=0.3)
        rest = VGroup(*[p for i, p in enumerate(people) if i not in (SICK_AT, FALSE_AT)])
        self.play(rest.animate.set_opacity(0.12), FadeOut(cap), run_time=0.9)

        pair = VGroup(VGroup(sick, m_sick), VGroup(false_p, m_false))
        self.play(FadeOut(rest), run_time=0.5)
        # Placed at explicit x, not by arrange(buff=...). The captions are wider than the
        # icons, so the spacing that matters is caption-to-caption, and two guesses at a buff
        # both put "false alarm" off the right edge. Half-separation 1.55 leaves each label
        # (about 2.6 units at this size) comfortably inside the 4.5-unit half frame.
        self.play(pair.animate.scale(2.1), run_time=0.8)
        self.play(pair[0].animate.move_to([-1.8, 1.7, 0]),
                  pair[1].animate.move_to([1.8, 1.7, 0]), run_time=0.9)

        lab = VGroup(fit(note("really sick", 34, AD.ink), 3.0),
                     fit(note("false alarm", 34, AD.gray), 3.0))
        for l, grp in zip(lab, pair):
            l.next_to(grp, DOWN, buff=0.45)
        with self.voiceover(text=SAY[7]):
            self.play(FadeIn(lab[0], shift=DOWN * 0.1), run_time=0.4)
            self.play(FadeIn(lab[1], shift=DOWN * 0.1), run_time=0.4)

        # ---- 6. the answer -----------------------------------------------------
        two = fit(disp("2 test positive.", 56))
        one = fit(disp("1 is sick.", 56))
        tg = VGroup(two, one).arrange(DOWN, buff=0.22)
        tg.next_to(lab, DOWN, buff=0.95)
        fifty = fit(disp("50%", 130, AD.ink))
        fifty.next_to(tg, DOWN, buff=0.55)
        with self.voiceover(text=SAY[8]):
            show(two, 0.4)
            show(one, 0.4)
            self.play(Write(fifty), run_time=0.8)

        # ---- 7. the point ------------------------------------------------------
        self.play(FadeOut(VGroup(pair, lab, tg, fifty)), run_time=0.5)
        e = VGroup(fit(disp("A coin flip.", 76, AD.ink)),
                   fit(note("Because almost nobody", 42, AD.gray)),
                   fit(note("has it in the first place.", 42, AD.gray))
                   ).arrange(DOWN, buff=0.34).move_to([0, 1.5, 0])
        with self.voiceover(text=SAY[9]):
            self.play(Write(e[0]), run_time=0.7)
            show(e[1], 0.4)
            show(e[2], 0.4)

        sig = VGroup(disp("Quantica", 52, AD.ink), note("quanticaedu.com", 36)
                     ).arrange(DOWN, buff=0.22)
        sig.move_to([0, self.safe_bottom + 0.7, 0])
        show(sig, 0.5, UP * 0.15)
        self.wait(1.3)
