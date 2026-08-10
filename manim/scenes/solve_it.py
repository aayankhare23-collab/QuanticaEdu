"""Solving 2x + 3 = 11, one step at a time.

This is the lead example and the one to shoot first. It needs no LaTeX, it is the single
most recognisable thing a prealgebra and algebra product sells, and the colour-a-term then
move-it animation is what actually stops a scroll.

The hook has to land in the first two seconds, before anyone has decided to keep watching,
so the equation is on screen immediately rather than after a title card.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from manim import DOWN, FadeIn, FadeOut, TransformMatchingShapes, Write

from base import QuanticaScene
from mathtype import math_run


class SolveIt(QuanticaScene):
    format_name = "reel"
    theme_name = "dark"

    def construct(self):
        t = self.theme
        f = self.f_display

        steps = [
            ["2", "x", " + ", "3", " = ", "11"],
            ["2", "x", " = ", "8"],
            ["x", " = ", "4"],
        ]
        notes = [
            "",
            "subtract 3 from both sides",
            "divide both sides by 2",
        ]

        eq = math_run(steps[0], font=f, size=96, color=t.ink)
        eq.move_to([0, 0, 0])
        self.play(Write(eq), run_time=0.9)
        self.wait(0.5)

        # TransformMatchingShapes, not Transform. Transform morphs submobject by submobject
        # and the steps have different numbers of glyphs, 2x + 3 = 11 against 2x = 8, so it
        # produced an unreadable smear for the whole middle of the animation. Matching on
        # glyph shape carries the 2, the x and the = across and fades only what actually
        # changed, which is also the thing that makes the step legible.
        for step, note in zip(steps[1:], notes[1:]):
            caption = self.caption(note)
            nxt = math_run(step, font=f, size=96, color=t.ink)
            nxt.move_to([0, 0, 0])
            self.play(FadeIn(caption, shift=DOWN * 0.2), run_time=0.35)
            self.play(TransformMatchingShapes(eq, nxt), run_time=0.8)
            eq = nxt
            self.wait(0.45)
            self.play(FadeOut(caption), run_time=0.25)

        # Land on the answer in the brand's own lime, which is the one colour that has
        # survived every regeneration of this palette.
        answer = math_run([("x", t.ink), (" = ", t.ink), ("4", t.pop)], font=f, size=110, color=t.ink)
        answer.move_to([0, 0, 0])
        self.play(TransformMatchingShapes(eq, answer), run_time=0.5)
        eq = answer
        self.wait(0.6)

        mark = self.wordmark(size=44)
        mark.move_to([0, self.safe_bottom, 0])
        self.play(FadeIn(mark, shift=DOWN * 0.15), run_time=0.5)
        self.wait(1.0)
