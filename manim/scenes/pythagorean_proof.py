"""A visual proof of a² + b² = c², presented by Milo. Silent scene, no narration.

Ported from milo_manim/pythagorean_with_milo.py. The structure, geometry, timings and
on-screen wording are the reference's; what changed is the foundation underneath:

- Type is Chillax through typeset.brand_text. The reference set everything in the Pango
  default face with weight=BOLD; Chillax ships as a single Semibold that already carries
  the landing page's weight, so no weight is requested anywhere.
- Colours go through the AdTheme roles. The reference's four accent triangles (lavender,
  sky, mint, coral) collapse onto tri_fill, because the brand runs on two surfaces and
  one rule: slate for the ordinary surface, lime for the surface that matters (the inner
  c² square and the payoff cards), ink for every rule and all text.
- Corners are square. Every RoundedRectangle is a Rectangle, and the cancel box drops
  its corner radius.
- The old milo.Milo actor was not ported into this repo; this scene stands on MiloActor,
  which normalises the pose PNGs to one body height and breathes on its own. The old
  idle_bob calls become plain waits of the same length, since the breathing updater
  already supplies the motion; scene time is unchanged.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from manim import *

from milo_actor import MiloActor
from milo_scene import apply_vertical_format
from typeset import LIGHT, brand_text

THEME = LIGHT
apply_vertical_format(THEME)


# ------------------------------------------------------------
# MILO PLACEMENT
#
# The reference sized Milo by full image height (2.45, then a 0.96 shrink) and parked
# him with to_corner(DR). MiloActor stands on an anchor at his feet and head centre and
# normalises every pose to one body height, so these constants reproduce the reference
# placement: the feet row and head centre the old neutral pose actually landed on, and a
# body height in the middle of the range the old per-pose scaling displayed (neutral
# came out at 1.26, the speaking poses near 1.40).
# ------------------------------------------------------------

MILO_BODY = 1.35
MILO_START = np.array([3.42, -7.47, 0.0])
MILO_TUCKED_BODY = MILO_BODY * 0.96
MILO_TUCKED = np.array([3.49, -7.52, 0.0])


def milo_glide(milo, anchor, body_height, run_time):
    """Animate the actor's anchor and size.

    The reference moved Milo with .animate.scale().to_corner(). MiloActor rewrites its
    sprite from (anchor, body_height) every frame, so an ordinary transform would be
    overwritten; driving the two parameters through the updater is the equivalent move.
    """
    a0, h0 = milo.anchor.copy(), milo.body_height
    a1 = np.array(anchor, dtype=float)

    def drive(_, alpha):
        milo.anchor = a0 + (a1 - a0) * alpha
        milo.body_height = h0 + (body_height - h0) * alpha

    return UpdateFromAlphaFunc(Mobject(), drive, run_time=run_time, rate_func=smooth)


def equation_box(text, color, width=1.55, height=1.0):
    box = Rectangle(
        width=width,
        height=height,
        fill_color=color,
        fill_opacity=1,
        stroke_color=THEME.ink,
        stroke_width=4,
    )

    label = brand_text(
        text,
        size=40,
        color=THEME.ink,
    ).move_to(box)

    assert label.width < width - 0.1 and label.height < height - 0.1, (
        f"equation_box label {text!r} ({label.width:.2f}x{label.height:.2f}) "
        f"does not fit its {width}x{height} box"
    )

    return VGroup(box, label)


def speech_bubble(text, anchor, width=4.7):
    label = brand_text(
        text,
        size=28,
        color=THEME.ink,
        line_spacing=0.9,
    )

    bubble = Rectangle(
        width=width,
        height=label.height + 0.65,
        fill_color=THEME.surface,
        fill_opacity=1,
        stroke_color=THEME.ink,
        stroke_width=3,
    )

    label.move_to(bubble)

    group = VGroup(bubble, label)
    group.next_to(anchor, LEFT, buff=0.28)

    assert label.width <= width - 0.2, (
        f"bubble text {text!r} is {label.width:.2f} wide against a {width} bubble"
    )
    assert group.get_left()[0] > -config.frame_width / 2, (
        f"bubble {text!r} runs off the left edge at {group.get_left()[0]:.2f}"
    )

    return group


class PythagoreanProofWithMilo(Scene):
    def _check_geometry(self, outer_square, inner_square, milo):
        """Chillax metrics moved the type, so confirm the figure still stands clear."""
        frame_x = config.frame_width / 2

        assert outer_square.get_right()[0] < frame_x - 0.5, "square crowds the right edge"
        assert outer_square.get_left()[0] > -frame_x + 0.5, "square crowds the left edge"

        # The inner square's vertices sit on the outer square's sides.
        left, right = outer_square.get_left()[0], outer_square.get_right()[0]
        bottom, top = outer_square.get_bottom()[1], outer_square.get_top()[1]
        for v in inner_square.get_vertices():
            on_x = np.isclose(v[0], left) or np.isclose(v[0], right)
            on_y = np.isclose(v[1], bottom) or np.isclose(v[1], top)
            assert on_x or on_y, f"inner square vertex {v} left the outer square"

        # The figure never reaches Milo's corner.
        assert outer_square.get_bottom()[1] > milo.get_top()[1] + 0.3, (
            "the diagram overlaps Milo"
        )

    def construct(self):

        # ----------------------------------------------------
        # Milo enters, larger, with a fixed open-mouth speaking pose
        # ----------------------------------------------------

        milo = MiloActor(
            MILO_START,
            body_height=MILO_BODY,
            pose="neutral",
        )

        milo.set_z_index(20)
        milo.enter(self, run_time=0.65)

        intro_bubble = speech_bubble(
            "Don’t memorize it.\nLet’s see why it works.",
            milo,
            width=4.9,
        )
        intro_bubble.shift(UP * 0.35)
        intro_bubble.set_z_index(19)

        self.play(
            FadeIn(intro_bubble, shift=RIGHT * 0.2),
            run_time=0.5,
        )
        self.play(milo.pose("happy", run_time=0.18))
        self.wait(1.1)  # was milo.idle_bob; MiloActor breathes on its own
        self.wait(0.35)
        self.play(milo.pose("neutral", run_time=0.18))
        self.wait(0.35)

        self.play(
            FadeOut(intro_bubble, shift=RIGHT * 0.2),
            milo_glide(milo, MILO_TUCKED, MILO_TUCKED_BODY, run_time=0.5),
            run_time=0.5,
        )

        # ----------------------------------------------------
        # OPENING TITLE
        # ----------------------------------------------------

        title_line = brand_text(
            "A visual proof of",
            size=42,
            color=THEME.ink,
        )

        highlight = Rectangle(
            width=6.8,
            height=1.2,
            fill_color=THEME.lime,
            fill_opacity=1,
            stroke_width=0,
        )

        highlight_text = brand_text(
            "a² + b² = c²",
            size=54,
            color=THEME.ink,
        ).move_to(highlight)

        assert highlight_text.width < highlight.width - 0.3, "title outgrew its band"

        title = VGroup(
            title_line,
            VGroup(highlight, highlight_text),
        ).arrange(DOWN, buff=0.25)

        title.move_to(UP * 4.95)

        self.play(FadeIn(title_line, shift=UP * 0.2))
        self.play(
            GrowFromCenter(highlight),
            FadeIn(highlight_text),
        )

        self.play(milo.pose("wink", run_time=0.18))
        self.wait(0.55)
        self.play(milo.pose("neutral", run_time=0.18))

        self.play(FadeOut(title, shift=UP * 0.25))

        # ----------------------------------------------------
        # BUILD THE DIAGRAM
        # ----------------------------------------------------

        section_title = brand_text(
            "Start with four identical right triangles",
            size=31,
            color=THEME.ink,
        ).to_edge(UP, buff=0.55)

        self.play(FadeIn(section_title, shift=DOWN * 0.2))

        a = 3.0
        b = 2.0
        side_length = a + b

        center = UP * 1.55
        half = side_length / 2

        bottom_left = center + np.array([-half, -half, 0])
        bottom_right = center + np.array([half, -half, 0])
        top_right = center + np.array([half, half, 0])
        top_left = center + np.array([-half, half, 0])

        outer_square = Square(
            side_length=side_length,
            stroke_color=THEME.ink,
            stroke_width=5,
        ).move_to(center)

        self.play(Create(outer_square), run_time=0.9)

        triangle_1 = Polygon(
            bottom_left,
            bottom_left + RIGHT * a,
            bottom_left + UP * b,
        )

        triangle_2 = Polygon(
            bottom_right,
            bottom_right + UP * a,
            bottom_right + LEFT * b,
        )

        triangle_3 = Polygon(
            top_right,
            top_right + LEFT * a,
            top_right + DOWN * b,
        )

        triangle_4 = Polygon(
            top_left,
            top_left + DOWN * a,
            top_left + RIGHT * b,
        )

        triangles = VGroup(
            triangle_1,
            triangle_2,
            triangle_3,
            triangle_4,
        )

        # The reference gave each triangle its own accent colour. The brand has two
        # ordinary surfaces and one rule, so the triangles alternate between them; a
        # single shared fill would read as a solid ring here, because every triangle
        # edge lies on the outer or inner square. Lime stays reserved for the c² square.
        triangle_fills = [
            THEME.tri_fill,
            THEME.surface,
            THEME.tri_fill,
            THEME.surface,
        ]

        for triangle, fill in zip(triangles, triangle_fills):
            triangle.set_fill(fill, opacity=1)
            triangle.set_stroke(THEME.tri_stroke, width=4)

        self.play(
            LaggedStart(
                *[
                    FadeIn(triangle, scale=0.88)
                    for triangle in triangles
                ],
                lag_ratio=0.16,
            ),
            run_time=1.65,
        )

        self.wait(1.1)  # was milo.idle_bob

        # ----------------------------------------------------
        # LABEL a AND b
        # ----------------------------------------------------

        a_label = brand_text(
            "a",
            size=36,
            color=THEME.ink,
        ).move_to(
            bottom_left + RIGHT * (a / 2) + DOWN * 0.26
        )

        b_label = brand_text(
            "b",
            size=36,
            color=THEME.ink,
        ).move_to(
            bottom_left + UP * (b / 2) + LEFT * 0.25
        )

        self.play(FadeIn(a_label), FadeIn(b_label))

        label_bubble = speech_bubble(
            "Each triangle has\nlegs a and b.",
            milo,
            width=3.7,
        )
        label_bubble.shift(UP * 0.3)

        self.play(FadeIn(label_bubble))
        self.play(milo.pose("happy", run_time=0.18))
        self.wait(1.1)  # was milo.idle_bob
        self.wait(0.25)
        self.play(milo.pose("neutral", run_time=0.18))
        self.play(FadeOut(label_bubble))

        # ----------------------------------------------------
        # REVEAL THE INNER SQUARE
        # ----------------------------------------------------

        inner_bottom = bottom_left + RIGHT * a
        inner_right = bottom_right + UP * a
        inner_top = top_right + LEFT * a
        inner_left = top_left + DOWN * a

        inner_square = Polygon(
            inner_bottom,
            inner_right,
            inner_top,
            inner_left,
            fill_color=THEME.lime,
            fill_opacity=1,
            stroke_color=THEME.ink,
            stroke_width=5,
        )

        self._check_geometry(outer_square, inner_square, milo)

        self.play(Create(inner_square), run_time=1.25)

        c_label = brand_text(
            "c",
            size=36,
            color=THEME.ink,
        ).move_to(
            (inner_bottom + inner_right) / 2
            + DOWN * 0.22
            + RIGHT * 0.18
        )

        inner_area = brand_text(
            "c²",
            size=54,
            color=THEME.ink,
        ).move_to(center)

        self.play(
            FadeIn(c_label),
            GrowFromCenter(inner_area),
        )

        self.play(milo.pose("surprised", run_time=0.18))

        reveal_bubble = speech_bubble(
            "The middle is a square\nwith side length c.",
            milo,
            width=4.75,  # was 4.3; Chillax sets the line wider
        )
        reveal_bubble.shift(UP * 0.25)

        self.play(FadeIn(reveal_bubble))
        self.play(milo.pose("happy", run_time=0.18))
        self.wait(1.1)  # was milo.idle_bob
        self.wait(0.25)
        self.play(milo.pose("neutral", run_time=0.18))
        self.wait(0.3)
        self.play(FadeOut(reveal_bubble))
        self.play(milo.pose("neutral", run_time=0.18))

        # ----------------------------------------------------
        # EXPLAIN TOTAL AREA
        # ----------------------------------------------------

        self.play(
            FadeOut(section_title),
            FadeOut(a_label),
            FadeOut(b_label),
            FadeOut(c_label),
        )

        explanation = brand_text(
            "The whole square has side length a + b",
            size=29,
            color=THEME.ink,
        ).next_to(outer_square, DOWN, buff=0.42)

        self.play(Write(explanation))

        whole_area = brand_text(
            "Whole area = (a + b)²",
            size=36,
            color=THEME.ink,
        ).next_to(explanation, DOWN, buff=0.35)

        self.play(FadeIn(whole_area, shift=UP * 0.15))

        self.play(milo.pose("thinking", run_time=0.18))
        self.wait(1.1)  # was milo.idle_bob

        # ----------------------------------------------------
        # SHOW TRIANGLE AREAS
        # ----------------------------------------------------

        triangle_area = brand_text(
            "Each triangle has area ½ab",
            size=29,
            color=THEME.ink,
        ).move_to(explanation)

        self.play(
            ReplacementTransform(explanation, triangle_area),
        )

        triangle_area_labels = VGroup()

        for triangle in triangles:
            label = brand_text(
                "½ab",
                size=24,
                color=THEME.ink,
            ).move_to(triangle.get_center())

            triangle_area_labels.add(label)

        self.play(
            LaggedStart(
                *[
                    FadeIn(label, scale=0.75)
                    for label in triangle_area_labels
                ],
                lag_ratio=0.12,
            )
        )

        # ----------------------------------------------------
        # BUILD AREA EQUATION
        # ----------------------------------------------------

        equation_1 = brand_text(
            "(a + b)² = 4(½ab) + c²",
            size=35,
            color=THEME.ink,
        ).move_to(whole_area)

        self.play(
            ReplacementTransform(whole_area, equation_1),
        )

        self.play(
            FadeOut(triangle_area),
            FadeOut(triangle_area_labels),
        )

        equation_2 = brand_text(
            "a² + 2ab + b² = 2ab + c²",
            size=31,
            color=THEME.ink,
        ).move_to(equation_1)

        self.play(
            ReplacementTransform(equation_1, equation_2),
            run_time=1.2,
        )

        self.play(milo.pose("thinking", run_time=0.18))

        thinking_bubble = speech_bubble(
            "Now subtract 2ab\nfrom both sides.",
            milo,
            width=4.0,
        )
        thinking_bubble.shift(UP * 0.25)

        self.play(FadeIn(thinking_bubble))
        self.play(milo.pose("happy", run_time=0.18))
        self.wait(1.1)  # was milo.idle_bob
        self.wait(0.25)
        self.play(milo.pose("neutral", run_time=0.18))

        # The reference stroked this in coral; ink is the rule colour here.
        cancel_box = SurroundingRectangle(
            equation_2,
            color=THEME.ink,
            buff=0.12,
        )

        self.play(Create(cancel_box))
        self.wait(0.5)
        self.play(
            FadeOut(cancel_box),
            FadeOut(thinking_bubble),
        )

        # ----------------------------------------------------
        # FINAL REVEAL
        # ----------------------------------------------------

        self.play(
            FadeOut(equation_2),
            FadeOut(inner_area),
            FadeOut(triangles),
            FadeOut(inner_square),
            FadeOut(outer_square),
        )

        final_title = brand_text(
            "So the areas must satisfy:",
            size=33,
            color=THEME.ink,
        ).move_to(UP * 2.55)

        self.play(FadeIn(final_title))

        # The leg boxes echo the two triangle surfaces; the c² box keeps the lime.
        a_box = equation_box("a²", THEME.slate)
        plus = brand_text(
            "+",
            size=46,
            color=THEME.ink,
        )
        b_box = equation_box("b²", THEME.surface)
        equals = brand_text(
            "=",
            size=46,
            color=THEME.ink,
        )
        c_box = equation_box("c²", THEME.lime)

        final_equation = VGroup(
            a_box,
            plus,
            b_box,
            equals,
            c_box,
        ).arrange(RIGHT, buff=0.16)

        final_equation.move_to(UP * 0.7)

        self.play(
            LaggedStart(
                GrowFromCenter(a_box),
                FadeIn(plus),
                GrowFromCenter(b_box),
                FadeIn(equals),
                GrowFromCenter(c_box),
                lag_ratio=0.13,
            ),
            run_time=1.75,
        )

        self.play(milo.pose("excited", run_time=0.18))
        milo.celebrate(self, run_time=1.1)

        conclusion = brand_text(
            "Now you understand it.",
            size=41,
            color=THEME.ink,
        )

        conclusion_box = Rectangle(
            width=7.0,  # was 6.1; Chillax sets the line wider
            height=1.1,
            fill_color=THEME.lime,
            fill_opacity=1,
            stroke_width=0,
        )

        assert conclusion.width < conclusion_box.width - 0.3, (
            "conclusion outgrew its card"
        )

        conclusion.move_to(conclusion_box)
        conclusion_group = VGroup(
            conclusion_box,
            conclusion,
        ).next_to(final_equation, DOWN, buff=0.9)

        self.play(
            GrowFromCenter(conclusion_box),
            FadeIn(conclusion),
        )

        self.play(
            final_equation.animate.scale(1.07),
            run_time=0.35,
            rate_func=there_and_back,
        )

        self.wait(2)
