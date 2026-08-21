"""
The Pythagorean theorem by area, with Milo narrating from the corner.

This is the proof that was in ``pythagorean_with_milo.py``, rebuilt. Four copies of
one right triangle are pinwheeled inside a square of side a + b. The whole square is
(a + b)². The four triangles come to 4(½ab), and the hole they leave is c². Setting
those equal and multiplying out, the 2ab on each side cancels and a² + b² = c² is
what remains.

The identity is asserted at import in ``_check_geometry()``, so the picture cannot
drift out of agreement with the algebra it is standing for.

Render:
    .venv/bin/manim -ql scenes/pythagoras.py PythagorasWithMilo

Layout stills, no audio:
    .venv/bin/manim -sql scenes/pythagoras.py LayoutCheck
    .venv/bin/manim -sql scenes/pythagoras.py LayoutCheckAlgebra
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from manim import *

from milo_scene import (
    CAPTION_CENTER,
    CAPTION_SIZE,
    CAPTION_WIDTH,
    DIAGRAM_CENTER,
    EQUATION_Y,
    MILO_ANCHOR,
    MILO_HEIGHT,
    TITLE_Y,
    MiloVoiceoverScene,
    apply_vertical_format,
    as_written,
    for_speech,
)
from milo_actor import MiloActor
from typeset import (
    DARK,
    LIGHT,
    brand_text,
    caption_block,
    centre_lines,
    math_run,
    panel,
    wrap,
)

THEME = LIGHT  # swap to DARK for the inverted cut
apply_vertical_format(THEME)

# ---------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------

SIDE = 5.9  # the big square, in scene units
LEG_A = SIDE * 4 / 7  # a 3-4-5 triangle, so c comes out visibly clean
LEG_B = SIDE * 3 / 7
HYP = SIDE * 5 / 7


# Each triangle is written right-angle vertex first, then the end of leg a, then the
# end of leg b, in square-local coordinates on [0, SIDE]^2. Keeping that order means
# the four are genuinely congruent copies.
A, B, S = LEG_A, LEG_B, SIDE
TRIANGLES = [
    [(0, 0), (A, 0), (0, B)],
    [(S, 0), (S, A), (A, 0)],
    [(S, S), (B, S), (S, A)],
    [(0, S), (0, B), (B, S)],
]

# The tilted square the pinwheel leaves in the middle. Every edge is a hypotenuse.
HOLE = [(A, 0), (S, A), (B, S), (0, B)]


def _check_geometry():
    """The picture has to be true before a single frame is drawn."""
    assert abs(HYP**2 - (LEG_A**2 + LEG_B**2)) < 1e-9, "not a right triangle"

    def edge(p, q):
        return float(np.hypot(q[0] - p[0], q[1] - p[1]))

    for corner, a_end, b_end in TRIANGLES:
        assert abs(edge(corner, a_end) - A) < 1e-9
        assert abs(edge(corner, b_end) - B) < 1e-9
        assert abs(edge(a_end, b_end) - HYP) < 1e-9

    for i in range(4):
        p, q, r = HOLE[i - 1], HOLE[i], HOLE[(i + 1) % 4]
        assert abs(edge(q, r) - HYP) < 1e-9, "hole edge is not c"
        u = (p[0] - q[0], p[1] - q[1])
        v = (r[0] - q[0], r[1] - q[1])
        assert abs(u[0] * v[0] + u[1] * v[1]) < 1e-9, "hole corner is not square"

    # The proof itself: whole square = four triangles + the hole.
    whole = (A + B) ** 2
    pieces = 4 * (0.5 * A * B) + HYP**2
    assert abs(whole - pieces) < 1e-9, "(a+b)^2 does not equal 4(ab/2) + c^2"
    # and what that reduces to once 2ab is taken off both sides
    assert abs((A**2 + B**2) - HYP**2) < 1e-9


_check_geometry()


def pt(x, y):
    """Square-local coordinates to scene coordinates."""
    return DIAGRAM_CENTER + np.array([x - S / 2, y - S / 2, 0.0])


def corner_mark(prev_p, corner, next_p, size=0.2, **kw):
    """A small square drawn inside the angle at ``corner``."""
    u = normalize(prev_p - corner)
    v = normalize(next_p - corner)
    mark = VMobject(**kw)
    mark.set_points_as_corners(
        [corner + u * size, corner + (u + v) * size, corner + v * size]
    )
    return mark


def edge_tick(p, q, size=0.13, **kw):
    """A single hatch across the middle of an edge, the usual 'these are equal' mark."""
    mid = (p + q) / 2
    normal = normalize(rotate_vector(q - p, PI / 2))
    return Line(mid - normal * size, mid + normal * size, **kw)


# ---------------------------------------------------------------------------
# the figure
# ---------------------------------------------------------------------------


class Figure:
    """Builds every mobject the proof needs, so the scene body stays about timing."""

    def __init__(self, theme):
        self.th = theme

        # A gesture, not a fixture. It traces the container once and then gets out of
        # the way, because the boundary of the big square is already drawn by the
        # triangles' own a and b legs, and an outline on top of those would hide
        # exactly the colours the proof is carrying.
        self.outline = Polygon(
            *[pt(x, y) for x, y in [(0, 0), (S, 0), (S, S), (0, S)]],
            stroke_color=theme.ink,
            stroke_width=5,
            fill_opacity=0,
        )
        # Held just outside the tiles. Drawn flush it would sit exactly on the a and
        # b legs and hide the two colours that are doing the explaining.
        self.outline.scale(1.03, about_point=DIAGRAM_CENTER)

        self.triangles = VGroup(*[self._triangle(tri) for tri in TRIANGLES])

        # The one surface that matters, so it gets the lime.
        self.hole = Polygon(
            *[pt(x, y) for x, y in HOLE],
            stroke_color=theme.ink,
            stroke_width=6,
            fill_color=theme.lime,
            fill_opacity=0,
        )
        # These are drawn on top of the filled hole, not on the pale triangles, so
        # they take the background colour. Every hole edge sits right where a
        # triangle wants to put its own "½ab", and the hole interior is the only
        # place near that boundary that is reliably free.
        self.hole_marks = VGroup(
            *[
                corner_mark(
                    pt(*HOLE[(i - 1) % 4]),
                    pt(*HOLE[i]),
                    pt(*HOLE[(i + 1) % 4]),
                    size=0.19,
                    stroke_color=theme.ink,
                    stroke_width=3.5,
                )
                for i in range(4)
            ]
        )
        self.hole_ticks = VGroup(
            *[
                edge_tick(
                    pt(*HOLE[i]),
                    pt(*HOLE[(i + 1) % 4]),
                    stroke_color=theme.ink,
                    stroke_width=5,
                )
                for i in range(4)
            ]
        )

        self.label_c2 = brand_text("c²", size=54, color=theme.ink, slant=ITALIC)
        self.label_c2.move_to(Polygon(*[pt(x, y) for x, y in HOLE]).get_center())

        # One "½ab" sitting in each triangle. These are what 4(½ab) is counting.
        self.area_labels = VGroup()
        for corner, a_end, b_end in TRIANGLES:
            centroid = sum(np.array(pt(*p)) for p in (corner, a_end, b_end)) / 3
            label = brand_text("½ab", size=26, color=theme.ink, slant=ITALIC)
            label.move_to(centroid)
            self.area_labels.add(label)

    def _triangle(self, tri):
        """One triangle: a solid slate tile behind a near-black editorial rule.

        The landing page runs on two surfaces and one rule, so the figure does too.
        Slate is the ordinary surface and lime is the surface that matters, which is
        what makes the c square read as the payoff without importing a third and
        fourth accent colour the brand does not use anywhere.
        """
        th = self.th
        corner, a_end, b_end = (pt(*p) for p in tri)

        body = Polygon(
            corner,
            a_end,
            b_end,
            stroke_width=0,
            fill_color=th.slate,
            fill_opacity=1,
        )
        leg_a = Line(corner, a_end, stroke_color=th.ink, stroke_width=6)
        leg_b = Line(corner, b_end, stroke_color=th.ink, stroke_width=6)
        hyp = Line(a_end, b_end, stroke_color=th.ink, stroke_width=6)
        square = corner_mark(
            a_end, corner, b_end, size=0.21, stroke_color=th.ink, stroke_width=3
        )

        return VGroup(body, leg_a, leg_b, hyp, square)

    # -- the opening hero triangle -----------------------------------------

    def hero(self, scale=1.3):
        """Triangle one, blown up and centred, for the opening beats."""
        shape = self.triangles[0].copy()
        labels = self._hero_labels()
        group = VGroup(shape, labels)
        group.scale(scale, about_point=DIAGRAM_CENTER)
        group.move_to(DIAGRAM_CENTER)
        return group, shape, labels

    def _hero_labels(self):
        th = self.th
        corner, a_end, b_end = (pt(*p) for p in TRIANGLES[0])
        la = brand_text("a", size=44, color=th.ink, slant=ITALIC)
        la.next_to(Line(corner, a_end), DOWN, buff=0.2)
        lb = brand_text("b", size=44, color=th.ink, slant=ITALIC)
        lb.next_to(Line(corner, b_end), LEFT, buff=0.2)
        lc = brand_text("c", size=44, color=th.ink, slant=ITALIC)
        lc.next_to(Line(a_end, b_end).get_center(), UR, buff=0.12)
        return VGroup(la, lb, lc)

    def side_braces(self):
        th = self.th
        brace_a = Brace(Line(pt(0, 0), pt(A, 0)), DOWN, buff=0.14, color=th.ink)
        brace_b = Brace(Line(pt(A, 0), pt(S, 0)), DOWN, buff=0.14, color=th.ink)
        label_a = brand_text("a", size=38, color=th.ink, slant=ITALIC)
        label_a.next_to(brace_a, DOWN, buff=0.1)
        label_b = brand_text("b", size=38, color=th.ink, slant=ITALIC)
        label_b.next_to(brace_b, DOWN, buff=0.1)
        return VGroup(brace_a, label_a), VGroup(brace_b, label_b)

    def hole_side_label(self):
        """A "c" just inside the lower-right edge of the hole."""
        th = self.th
        label = brand_text("c", size=40, color=th.ink, slant=ITALIC)
        label.move_to((np.array(pt(*HOLE[0])) + np.array(pt(*HOLE[1]))) / 2)
        label.shift(UL * 0.34)
        return label


# ---------------------------------------------------------------------------
# the three equation states
# ---------------------------------------------------------------------------


def eq_setup(theme, size=44):
    """(a + b)² = 4(½ab) + c², coloured by which part of the picture each piece is."""
    return math_run(
        [
            ("(a + b)²", theme.ink),
            ("=", theme.ink),
            ("4(½ab)", theme.ink),
            ("+", theme.ink),
            ("c²", theme.ink),
        ],
        size=size,
        buff=0.2,
    )


def eq_expanded(theme, size=44):
    """a² + 2ab + b² = 2ab + c². The two 2ab go grey, they are on their way out."""
    return math_run(
        [
            ("a²", theme.ink),
            ("+", theme.ink),
            ("2ab", theme.gray),
            ("+", theme.ink),
            ("b²", theme.ink),
            ("=", theme.ink),
            ("2ab", theme.gray),
            ("+", theme.ink),
            ("c²", theme.ink),
        ],
        size=size,
        buff=0.18,
    )


def eq_result(theme, size=58):
    return math_run(
        [
            ("a²", theme.ink),
            ("+", theme.ink),
            ("b²", theme.ink),
            ("=", theme.ink),
            ("c²", theme.ink),
        ],
        size=size,
        buff=0.22,
    )


def eq_header(theme, size=42):
    """The claim, parked at the top of the frame in full-strength ink."""
    return math_run(
        [
            ("a²", theme.ink),
            ("+", theme.ink),
            ("b²", theme.ink),
            ("=", theme.ink),
            ("c²", theme.ink),
        ],
        size=size,
        buff=0.2,
    )


# ---------------------------------------------------------------------------
# the scene
# ---------------------------------------------------------------------------



class PythagorasWithMilo(MiloVoiceoverScene):
    theme = THEME


    def construct(self):
        th = self.theme
        fig = Figure(th)

        self.open_with_milo()

        claim = eq_result(th, size=64).move_to(DIAGRAM_CENTER)
        header = eq_header(th).move_to(UP * TITLE_Y)

        # ---- 1. the claim ------------------------------------------------
        with self.say(
            "Everyone memorises {a} squared plus b squared equals c squared.",
            caption="Everyone memorises *a² + b² = c²*.",
        ) as t:
            self.play(
                LaggedStart(*[FadeIn(m, shift=UP * 0.25) for m in claim], lag_ratio=0.14),
                self.milo.pose("happy"),
                run_time=min(2.9, t.duration * 0.78),
            )

        with self.say(
            "Almost nobody gets shown why it is true.",
            caption="Almost nobody is shown *why*.",
        ) as t:
            self.play(
                Transform(claim, header),
                self.milo.pose("thinking"),
                run_time=min(1.7, t.duration * 0.75),
            )

        # ---- 2. one triangle ---------------------------------------------
        hero, hero_shape, hero_labels = fig.hero()
        body, leg_a, leg_b, hyp, right_angle = hero_shape

        with self.say(
            "Start with a right triangle.",
            caption="Start with a *right triangle*.",
        ) as t:
            self.play(
                DrawBorderThenFill(body, run_time=t.duration * 0.6),
                self.milo.pose("neutral"),
            )
            self.play(Create(right_angle), run_time=min(0.5, t.duration * 0.25))

        with self.say(
            "Its two short sides are {a} and b. The long one is c.",
            caption="Short sides *a* and *b*. Long side *c*.",
        ) as t:
            step = t.duration / 3.5
            self.play(Create(leg_a), FadeIn(hero_labels[0], shift=UP * 0.2), run_time=step)
            self.play(Create(leg_b), FadeIn(hero_labels[1], shift=RIGHT * 0.2), run_time=step)
            self.play(Create(hyp), FadeIn(hero_labels[2], shift=DL * 0.2), run_time=step)

        # ---- 3. four copies ----------------------------------------------
        with self.say(
            "Now take four identical copies of it.",
            caption="Take *four identical copies*.",
        ) as t:
            self.play(
                Transform(hero_shape, fig.triangles[0]),
                FadeOut(hero_labels, scale=0.8),
                self.milo.pose("happy"),
                run_time=t.duration * 0.5,
            )
            # Each of the other three is this one turned a quarter turn further about
            # the middle of the square, which is why they interlock.
            spun = VGroup()
            for _ in (1, 2, 3):
                copy = fig.triangles[0].copy()
                spun.add(copy)
                self.add(copy)
            self.play(
                LaggedStart(
                    *[
                        Rotate(copy, angle=i * PI / 2, about_point=DIAGRAM_CENTER)
                        for i, copy in zip((1, 2, 3), spun)
                    ],
                    lag_ratio=0.22,
                ),
                run_time=max(1.2, t.duration * 0.45),
            )

        on_screen = VGroup(hero_shape, *spun)

        brace_a, brace_b = fig.side_braces()
        with self.say(
            "They fit exactly inside a square whose side is {a} plus b.",
            caption="They fill a square of side *a + b*.",
        ) as t:
            self.play(Create(fig.outline), run_time=t.duration * 0.38)
            self.play(
                FadeIn(brace_a, shift=UP * 0.2),
                FadeIn(brace_b, shift=UP * 0.2),
                FadeOut(fig.outline),
                run_time=t.duration * 0.36,
            )

        # ---- 4. name the three areas --------------------------------------
        equation = eq_setup(th).move_to(UP * EQUATION_Y)
        assert equation.width < 8.2, f"setup equation overflows ({equation.width:.2f})"
        whole, eq_sign, four_tri, plus_sign, hole_area = equation

        with self.say(
            "So the area of the whole square is {a} plus b, all squared.",
            caption="Whole square = *(a + b)²*",
        ) as t:
            # A pulse of the whole figure, so "the whole square" is a gesture before
            # it is a term.
            self.play(
                on_screen.animate(rate_func=there_and_back).scale(1.03),
                self.milo.pose("neutral"),
                run_time=t.duration * 0.35,
            )
            # The braces sit directly above the equation slot, so they leave as the
            # term arrives rather than after it.
            self.play(
                FadeIn(whole, shift=UP * 0.25),
                FadeOut(brace_a, shift=DOWN * 0.2),
                FadeOut(brace_b, shift=DOWN * 0.2),
                run_time=t.duration * 0.45,
            )

        # The hole is named before the triangles are counted, so the "c" edge label
        # is gone by the time the four "½ab" labels land in the triangles. They
        # otherwise share the bottom-right corner.
        c_side = fig.hole_side_label()
        with self.say(
            "The hole they leave is a square of side c, so its area is c squared.",
            caption="The hole is a square of side *c*.",
        ) as t:
            self.play(
                Create(fig.hole),
                self.milo.pose("surprised"),
                run_time=t.duration * 0.25,
            )
            self.play(
                fig.hole.animate.set_fill(opacity=0.95),
                run_time=t.duration * 0.15,
            )
            self.play(
                LaggedStart(*[GrowFromCenter(m) for m in fig.hole_ticks], lag_ratio=0.1),
                LaggedStart(*[Create(m) for m in fig.hole_marks], lag_ratio=0.1),
                FadeIn(c_side),
                run_time=t.duration * 0.3,
            )
            self.play(
                FadeOut(fig.hole_ticks),
                FadeOut(fig.hole_marks),
                ReplacementTransform(c_side, fig.label_c2),
                run_time=t.duration * 0.2,
            )

        with self.say(
            "And each of the four triangles has area one half {a} b.",
            caption="Each triangle is *½ab*.",
        ) as t:
            self.play(
                LaggedStart(
                    *[FadeIn(m, scale=0.7) for m in fig.area_labels], lag_ratio=0.22
                ),
                self.milo.pose("happy"),
                run_time=t.duration * 0.8,
            )

        # ---- 5. the equation, assembled out of the picture -----------------
        with self.say(
            "The whole square is exactly those four triangles plus that hole.",
            caption="Whole = *four triangles* + *the hole*.",
        ) as t:
            self.play(FadeIn(eq_sign), run_time=t.duration * 0.15)
            # Each side of the equation flies out of the thing it is counting.
            self.play(
                TransformFromCopy(fig.area_labels, four_tri),
                self.milo.pose("wink"),
                run_time=t.duration * 0.35,
            )
            self.play(FadeIn(plus_sign), run_time=t.duration * 0.12)
            # c² carries the lime of the hole it came out of, on the landing page's
            # own panel, so the term and the region read as one thing.
            hole_panel = panel(hole_area, th)
            self.play(
                TransformFromCopy(fig.hole, hole_panel),
                TransformFromCopy(fig.label_c2, hole_area),
                run_time=t.duration * 0.3,
            )

        # ---- 6. the algebra ------------------------------------------------
        expanded = eq_expanded(th).move_to(UP * EQUATION_Y)
        assert expanded.width < 8.2, f"expanded equation overflows ({expanded.width:.2f})"
        expanded_panel = panel(expanded[8], th)

        # The pieces were added one at a time, so swap the loose submobjects for the
        # group before transforming, or both would end up drawn.
        self.remove(*equation.submobjects)
        self.add(equation)

        with self.say(
            "Multiply both sides out.",
            caption="Multiply *both sides* out.",
        ) as t:
            self.play(
                TransformMatchingShapes(equation, expanded),
                Transform(hole_panel, expanded_panel),
                run_time=min(1.8, t.duration * 0.85),
            )

        with self.say(
            "Two {a} b turns up on both sides, so it cancels.",
            caption="*2ab* is on both sides. It *cancels*.",
        ) as t:
            left_2ab, right_2ab = expanded[2], expanded[6]
            strikes = VGroup(
                *[
                    Line(
                        term.get_left() + LEFT * 0.05,
                        term.get_right() + RIGHT * 0.05,
                        stroke_color=th.ink,
                        stroke_width=6,
                    )
                    for term in (left_2ab, right_2ab)
                ]
            )
            self.play(
                LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.25),
                self.milo.pose("wink"),
                run_time=t.duration * 0.4,
            )
            self.play(
                FadeOut(strikes),
                FadeOut(left_2ab, shift=UP * 0.4),
                FadeOut(right_2ab, shift=UP * 0.4),
                FadeOut(expanded[1]),
                FadeOut(expanded[7]),
                run_time=t.duration * 0.35,
            )

        result = eq_result(th).move_to(UP * EQUATION_Y)
        result_panel = panel(result[4], th)
        remaining = VGroup(expanded[0], expanded[3], expanded[4], expanded[5], expanded[8])

        with self.say(
            "And what is left is the theorem.",
            caption="What is left is *a² + b² = c²*.",
        ) as t:
            self.play(
                TransformMatchingShapes(remaining, result),
                Transform(hole_panel, result_panel),
                self.milo.pose("excited"),
                run_time=min(1.6, t.duration * 0.7),
            )
            self.play(
                VGroup(result, hole_panel).animate(rate_func=there_and_back).scale(1.08),
                run_time=t.duration * 0.25,
            )

        with self.say(
            "Nothing to memorise. You can see where it comes from.",
            caption="Nothing to memorise. You can *see* it.",
        ) as t:
            self.play(
                result.animate(rate_func=there_and_back).scale(1.06),
                run_time=t.duration * 0.22,
            )
            self.milo.celebrate(self, run_time=t.duration * 0.5)

        # ---- 7. endcard -----------------------------------------------------
        self.play(
            FadeOut(on_screen),
            FadeOut(fig.hole),
            FadeOut(fig.label_c2),
            FadeOut(fig.area_labels),
            FadeOut(claim),
            VGroup(result, hole_panel).animate.scale(1.2).move_to(UP * 2.5),
            run_time=0.9,
        )

        closing_text = wrap(
            "At Quantica you don't memorise the result. You build it.", 21
        )
        closing = brand_text(
            closing_text,
            size=40,
            color=th.ink,
            line_spacing=0.85,
        )
        centre_lines(closing, closing_text.count("\n") + 1)
        closing.move_to(UP * 0.1)
        assert closing.width < 8.4, f"closing card overflows ({closing.width:.2f})"

        url = brand_text("quanticaedu.com", size=38, color=th.ink)
        url.move_to(DOWN * 2.1)
        url_panel = panel(url, th, pad_x=0.34, pad_y=0.17)

        self.clear_caption()
        self.remove(self.wordmark)

        # The endcard is silent. The words are on screen and the proof has already
        # landed, so a spoken sign-off would only read as an ad. Run times are
        # explicit here rather than fractions of a tracker, since there is no line to
        # size them against. The hold is long enough to read both lines and the URL.
        self.play(FadeIn(closing, shift=UP * 0.2), run_time=0.85)
        self.play(FadeIn(url_panel, scale=0.9), FadeIn(url, scale=0.9), run_time=0.55)
        self.wait(2.3)


# ---------------------------------------------------------------------------
# layout checks
# ---------------------------------------------------------------------------


class _LayoutBase(Scene):
    """Every zone populated at once, so a single still shows up any collision."""

    equation_state = "setup"

    def construct(self):
        th = THEME
        self.camera.background_color = th.bg
        fig = Figure(th)
        fig.hole.set_fill(opacity=0.95)

        equation = {
            "setup": eq_setup,
            "expanded": eq_expanded,
        }[self.equation_state](th).move_to(UP * EQUATION_Y)

        caption = caption_block(
            "The hole is a square of side *c*, so its area is *c²*.",
            th,
            size=CAPTION_SIZE,
            max_width=CAPTION_WIDTH,
        ).move_to(CAPTION_CENTER)

        wordmark = brand_text("quanticaedu.com", size=26, color=th.gray)
        wordmark.move_to([-2.55, -7.35, 0])

        # Milo is checked in his widest pose. "excited" throws his arms up and sits
        # taller in its own crop than "neutral" does, so it is the one that decides
        # whether he reaches the caption.
        milo = MiloActor(MILO_ANCHOR, body_height=MILO_HEIGHT, pose="excited")

        self.add(
            fig.hole,
            fig.triangles,
            fig.area_labels,
            fig.label_c2,
            fig.hole_side_label(),
            equation,
            panel(equation[-1], th),
            eq_header(th).move_to(UP * TITLE_Y),
            caption,
            wordmark,
            milo,
        )

        gaps = [
            ("header -> figure", eq_header(th).move_to(UP * TITLE_Y).get_bottom()[1] - fig.triangles.get_top()[1]),
            ("figure -> equation", fig.triangles.get_bottom()[1] - equation.get_top()[1]),
            ("equation -> caption", equation.get_bottom()[1] - caption.get_top()[1]),
            ("caption -> milo", caption.get_bottom()[1] - milo.get_top()[1]),
        ]
        print(f"[layout] equation width {equation.width:.2f} (limit 8.2)")
        print(f"[layout] caption width {caption.width:.2f} (limit {CAPTION_WIDTH})")
        for name, gap in gaps:
            flag = "  <-- COLLISION" if gap < 0 else ""
            print(f"[layout] {name:22s} {gap:+.2f}{flag}")


class LayoutCheck(_LayoutBase):
    equation_state = "setup"


class LayoutCheckAlgebra(_LayoutBase):
    equation_state = "expanded"
