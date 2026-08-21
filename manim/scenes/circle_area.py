"""
The area of a circle by rearrangement, with Milo narrating from the corner.

A circle of radius r is cut into an even number of equal wedges, which are then laid
out alternately point-up and point-down. Nothing is added and nothing is thrown away,
so the area is unchanged, and the shape that results is almost a rectangle. Its
height is r, because every wedge has two straight sides of length r. Its base is half
the circumference, pi r, because half of the arcs sit along the bottom. Cutting
thinner makes it a true rectangle in the limit, so the area is pi r times r.

The identity is asserted at import in ``_check_geometry()``, so the picture cannot
drift out of agreement with the algebra it stands for.

Render (narration comes from the local voiceover cache, no API key needed):
    manim -ql scenes/circle_area.py CircleAreaWithMilo

Layout stills, no audio:
    manim -sql scenes/circle_area.py LayoutCheckCircle
    manim -sql scenes/circle_area.py LayoutCheckRow
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
)
from milo_actor import MiloActor
from typeset import LIGHT, DARK, brand_text, caption_block, math_run, panel, wrap

THEME = LIGHT  # swap to DARK for the inverted cut
apply_vertical_format(THEME)

# ---------------------------------------------------------------------------
# geometry
# ---------------------------------------------------------------------------

R = 2.25  # circle radius, in scene units

# The unrolled row is pi*R wide, which is the number that decides whether this fits.
# At R = 2.25 that is 7.07, inside the 8.0 the captions already use.
ROW_WIDTH = PI * R

# Wedge counts the video steps through. The first is coarse enough that the sawtooth
# edge is obvious, which is the whole point of the last beat.
COARSE, MID, FINE = 16, 32, 64

CIRCLE_CENTER = DIAGRAM_CENTER
# The row is nudged right so the height brace and its label clear the left edge.
# The circle stays centred, since it has no furniture hanging off its side.
ROW_CENTER = DIAGRAM_CENTER + RIGHT * 0.45


def _check_geometry():
    """The picture has to be true before a single frame is drawn."""
    for n in (COARSE, MID, FINE):
        assert n % 2 == 0, "an odd wedge count cannot alternate up and down"

        step = TAU / n
        # Every wedge is congruent, so the whole circle is n of them.
        wedge_area = 0.5 * step * R**2
        assert abs(n * wedge_area - PI * R**2) < 1e-9, "wedges do not fill the circle"

        # Half the arcs lie along the bottom of the row, so the base is half the
        # circumference. This is the step the video is actually making.
        arc = step * R
        base = (n / 2) * arc
        assert abs(base - PI * R) < 1e-9, "row base is not half the circumference"
        assert abs(base * R - n * wedge_area) < 1e-9, "base times height is not the area"

    assert abs(ROW_WIDTH - PI * R) < 1e-9
    assert ROW_WIDTH < 8.0, f"unrolled row is too wide for the frame ({ROW_WIDTH:.2f})"
    # The height brace and its "r" hang off the left, so that side needs about 0.9
    # of clearance beyond the wedges themselves.
    left_edge = ROW_CENTER[0] - ROW_WIDTH / 2
    assert left_edge - 0.9 > -4.5, f"height brace would run off the left ({left_edge:.2f})"
    assert ROW_CENTER[0] + ROW_WIDTH / 2 < 4.4, "row runs off the right"


_check_geometry()


def rigid_move(mob, angle, apex_from, apex_to):
    """Rotate about the apex and carry the apex to its target, rigid at every frame.

    A plain ``Transform`` between the two positions interpolates each point on a
    straight line, which makes a wedge visibly collapse and re-inflate on its way
    through a large rotation. Rotating about the apex while translating the apex is
    a rigid motion throughout, so the wedge keeps its shape the whole way.
    """
    start = mob.copy()
    shift = apex_to - apex_from

    def update(m, alpha):
        m.become(start.copy())
        m.rotate(angle * alpha, about_point=apex_from)
        m.shift(shift * alpha)

    return UpdateFromAlphaFunc(mob, update)


# ---------------------------------------------------------------------------
# the figure
# ---------------------------------------------------------------------------


class Figure:
    """Builds every mobject the proof needs, so the scene body stays about timing."""

    def __init__(self, theme):
        self.th = theme

        self.outline = Circle(
            radius=R,
            stroke_color=theme.ink,
            stroke_width=6,
            fill_color=theme.slate,
            fill_opacity=1,
        ).move_to(CIRCLE_CENTER)

        # Traced over the outline to call out the circumference, then dropped.
        self.rim = Circle(
            radius=R, stroke_color=theme.lime, stroke_width=10, fill_opacity=0
        ).move_to(CIRCLE_CENTER)

        self.radius_line = Line(
            CIRCLE_CENTER,
            CIRCLE_CENTER + RIGHT * R,
            stroke_color=theme.ink,
            stroke_width=6,
        )
        self.radius_label = brand_text("r", size=44, color=theme.ink, slant=ITALIC)
        self.radius_label.next_to(self.radius_line, UP, buff=0.16)

        self.circumference_label = brand_text(
            "2πr", size=40, color=theme.ink, slant=ITALIC
        )
        self.circumference_label.move_to(CIRCLE_CENTER + UP * (R + 0.52))

    # -- wedges -------------------------------------------------------------

    def wedges(self, n):
        """The circle cut into n equal wedges, still in place.

        Alternating fills are not decoration. Once the wedges are interleaved, the
        alternation is what shows that consecutive wedges ended up pointing opposite
        ways, and that the row really is the same circle rearranged.
        """
        step = TAU / n
        group = VGroup()
        for i in range(n):
            wedge = Sector(
                radius=R,
                start_angle=i * step,
                angle=step,
                stroke_color=self.th.ink,
                stroke_width=2.5 if n <= MID else 1.2,
                fill_color=self.th.lime if i % 2 == 0 else self.th.slate,
                fill_opacity=1,
            )
            wedge.move_arc_center_to(CIRCLE_CENTER)
            group.add(wedge)
        return group

    def _slot(self, i, n):
        """Where wedge i lands in the row, as (bisector target, apex position).

        Even wedges point up with the apex on the bottom line, odd wedges point down
        with the apex on the top line, so their arcs interlock. Half the arcs end up
        along the bottom, which is what makes the base half the circumference.
        """
        arc = (TAU / n) * R
        k = i // 2
        if i % 2 == 0:
            return PI / 2, np.array([k * arc, 0.0, 0.0])
        return -PI / 2, np.array([k * arc + arc / 2, R, 0.0])

    def row(self, n):
        """The same n wedges, laid out as the near-rectangle, centred on ROW_CENTER."""
        step = TAU / n
        group = VGroup()
        for i, wedge in enumerate(self.wedges(n)):
            target, apex = self._slot(i, n)
            bisector = (i + 0.5) * step
            wedge.rotate(target - bisector, about_point=CIRCLE_CENTER)
            wedge.shift(apex - CIRCLE_CENTER)
            group.add(wedge)
        group.move_to(ROW_CENTER)
        return group

    def unroll(self, wedges, n, run_time):
        """Animations carrying each wedge from the circle to its slot in the row."""
        step = TAU / n
        # Build the finished row first so every wedge knows exactly where it lands,
        # including the recentring the group gets at the end.
        target_row = self.row(n)

        moves = []
        for i, wedge in enumerate(wedges):
            target, apex = self._slot(i, n)
            bisector = (i + 0.5) * step
            moves.append(
                rigid_move(
                    wedge,
                    target - bisector,
                    CIRCLE_CENTER,
                    target_row[i].get_arc_center(),
                )
            )
        # Enough lag that the wedges peel off in order rather than all swinging
        # through each other at once.
        return LaggedStart(*moves, lag_ratio=0.055, run_time=run_time)

    # -- labels on the row ---------------------------------------------------

    def row_braces(self, row):
        th = self.th
        height = Brace(row, LEFT, buff=0.16, color=th.ink)
        height_label = brand_text("r", size=40, color=th.ink, slant=ITALIC)
        height_label.next_to(height, LEFT, buff=0.12)

        base = Brace(row, DOWN, buff=0.16, color=th.ink)
        base_label = brand_text("πr", size=40, color=th.ink, slant=ITALIC)
        base_label.next_to(base, DOWN, buff=0.12)

        return VGroup(height, height_label), VGroup(base, base_label)


# ---------------------------------------------------------------------------
# the two equation states
# ---------------------------------------------------------------------------


def eq_setup(theme, size=46):
    """A = πr × r, the rectangle read straight off the picture."""
    return math_run(
        [("A", theme.ink), ("=", theme.ink), ("πr", theme.ink),
         ("×", theme.ink), ("r", theme.ink)],
        size=size,
        buff=0.2,
    )


def eq_result(theme, size=58):
    return math_run(
        [("A", theme.ink), ("=", theme.ink), ("πr²", theme.ink)],
        size=size,
        buff=0.22,
    )


def eq_header(theme, size=42):
    """The claim, parked at the top of the frame in full-strength ink."""
    return math_run(
        [("A", theme.ink), ("=", theme.ink), ("πr²", theme.ink)],
        size=size,
        buff=0.2,
    )


# ---------------------------------------------------------------------------
# the video
# ---------------------------------------------------------------------------


class CircleAreaWithMilo(MiloVoiceoverScene):
    theme = THEME

    def construct(self):
        th = self.theme
        fig = Figure(th)
        self.open_with_milo()

        claim = eq_result(th, size=64).move_to(DIAGRAM_CENTER)
        header = eq_header(th).move_to(UP * TITLE_Y)
        claim_panel = panel(claim[2], th)
        header_panel = panel(header[2], th)

        # ---- 1. the claim ----------------------------------------------------
        with self.say(
            "Everyone memorises area equals {pi} {r} squared.",
            caption="Everyone memorises *A = πr²*.",
        ) as t:
            self.play(
                FadeIn(claim_panel, scale=0.9),
                FadeIn(claim, scale=0.9),
                run_time=t.duration * 0.55,
            )
            self.play(self.milo.pose("happy"), run_time=t.duration * 0.2)

        with self.say(
            "Almost nobody is shown where it comes from.",
            caption="Almost nobody is shown *where it comes from*.",
        ) as t:
            self.play(
                ReplacementTransform(claim, header),
                ReplacementTransform(claim_panel, header_panel),
                self.milo.pose("thinking"),
                run_time=t.duration * 0.7,
            )

        # ---- 2. the circle ---------------------------------------------------
        with self.say(
            "Start with a circle of radius {r}.",
            caption="Start with a circle of radius *r*.",
        ) as t:
            self.play(
                DrawBorderThenFill(fig.outline),
                self.milo.pose("neutral"),
                run_time=t.duration * 0.55,
            )
            self.play(
                Create(fig.radius_line),
                FadeIn(fig.radius_label, shift=UP * 0.15),
                run_time=t.duration * 0.35,
            )

        with self.say(
            "The distance all the way around is two {pi} {r}.",
            caption="All the way around is *2πr*.",
        ) as t:
            self.play(Create(fig.rim), run_time=t.duration * 0.5)
            self.play(
                FadeIn(fig.circumference_label, shift=DOWN * 0.15),
                self.milo.pose("happy"),
                run_time=t.duration * 0.25,
            )
            self.play(FadeOut(fig.rim), run_time=t.duration * 0.15)

        # ---- 3. cut it up ----------------------------------------------------
        wedges = fig.wedges(COARSE)
        with self.say(
            "Now cut it into equal wedges.",
            caption="Cut it into *equal wedges*.",
        ) as t:
            self.play(
                FadeOut(fig.outline),
                FadeOut(fig.radius_line),
                FadeOut(fig.radius_label),
                FadeIn(wedges),
                run_time=t.duration * 0.4,
            )
            self.play(
                LaggedStart(
                    *[
                        w.animate(rate_func=there_and_back).scale(0.93)
                        for w in wedges
                    ],
                    lag_ratio=0.03,
                ),
                run_time=t.duration * 0.5,
            )

        # ---- 4. the rearrangement -------------------------------------------
        with self.say(
            "Lay them out alternately, one up, one down.",
            caption="Lay them out *alternately*, one up, one down.",
        ) as t:
            self.play(
                FadeOut(fig.circumference_label),
                self.milo.pose("surprised"),
                run_time=t.duration * 0.12,
            )
            self.play(fig.unroll(wedges, COARSE, run_time=t.duration * 0.75))

        with self.say(
            "Nothing was added and nothing was thrown away, so the area has not changed.",
            caption="Nothing added, nothing removed. *Same area*.",
        ) as t:
            self.play(
                wedges.animate(rate_func=there_and_back).scale(1.04),
                self.milo.pose("happy"),
                run_time=t.duration * 0.3,
            )
            # Each wedge lifts in turn. Counting them off is the claim being made,
            # so it is worth the time rather than holding on a still frame.
            self.play(
                LaggedStart(
                    *[
                        w.animate(rate_func=there_and_back).scale(1.09)
                        for w in wedges
                    ],
                    lag_ratio=0.05,
                ),
                run_time=t.duration * 0.55,
            )

        # ---- 5. read the rectangle off the picture ---------------------------
        height_brace, base_brace = fig.row_braces(wedges)

        with self.say(
            "Every wedge has two straight sides of length {r}, so the height is {r}.",
            caption="Every wedge has straight sides of length *r*.",
        ) as t:
            # The straight sides are the two radii every wedge kept, so show a few
            # wedges before measuring them.
            self.play(
                LaggedStart(
                    *[
                        w.animate(rate_func=there_and_back).scale(1.09)
                        for w in wedges[:5]
                    ],
                    lag_ratio=0.18,
                ),
                self.milo.pose("neutral"),
                run_time=t.duration * 0.4,
            )
            self.play(GrowFromCenter(height_brace), run_time=t.duration * 0.45)

        with self.say(
            "Half the arcs sit along the bottom, so the base is {pi} {r}.",
            caption="Half the arcs are the base, so it is *πr*.",
        ) as t:
            # The odd wedges are the ones that ended up pointing down, so their arcs
            # are exactly the arcs lying along the bottom.
            self.play(
                LaggedStart(
                    *[
                        w.animate(rate_func=there_and_back).scale(1.09)
                        for w in wedges[1::2]
                    ],
                    lag_ratio=0.07,
                ),
                run_time=t.duration * 0.42,
            )
            self.play(GrowFromCenter(base_brace), run_time=t.duration * 0.43)

        # ---- 6. thinner wedges ----------------------------------------------
        row_mid = fig.row(MID)
        row_fine = fig.row(FINE)

        with self.say(
            "Cut thinner and thinner, and it becomes a true rectangle.",
            caption="Cut thinner and it becomes a *true rectangle*.",
        ) as t:
            self.play(
                ReplacementTransform(wedges, row_mid),
                self.milo.pose("excited"),
                run_time=t.duration * 0.35,
            )
            self.play(
                ReplacementTransform(row_mid, row_fine),
                run_time=t.duration * 0.35,
            )

        # ---- 7. the algebra --------------------------------------------------
        equation = eq_setup(th).move_to(UP * EQUATION_Y)
        assert equation.width < 8.2, f"equation overflows ({equation.width:.2f})"

        with self.say(
            "Area is base times height. So {pi} {r} times {r}.",
            caption="Area = base × height = *πr × r*.",
        ) as t:
            self.play(FadeIn(equation[0]), FadeIn(equation[1]), run_time=t.duration * 0.2)
            # Each side of the product flies out of the brace that measured it.
            self.play(
                TransformFromCopy(base_brace[1], equation[2]),
                run_time=t.duration * 0.3,
            )
            self.play(FadeIn(equation[3]), run_time=t.duration * 0.12)
            self.play(
                TransformFromCopy(height_brace[1], equation[4]),
                run_time=t.duration * 0.3,
            )

        result = eq_result(th).move_to(UP * EQUATION_Y)
        result_panel = panel(result[2], th)

        self.remove(*equation.submobjects)
        self.add(equation)

        with self.say(
            "Which is {pi} {r} squared.",
            caption="Which is *πr²*.",
        ) as t:
            self.play(
                TransformMatchingShapes(equation, result),
                FadeIn(result_panel),
                run_time=t.duration * 0.6,
            )
            self.play(
                VGroup(result, result_panel).animate(rate_func=there_and_back).scale(1.08),
                run_time=t.duration * 0.3,
            )

        with self.say(
            "Nothing to memorise. You can see where it comes from.",
            caption="Nothing to memorise. You can *see* it.",
        ) as t:
            self.play(
                VGroup(result, result_panel).animate(rate_func=there_and_back).scale(1.05),
                run_time=t.duration * 0.2,
            )
            self.milo.celebrate(self, run_time=t.duration * 0.55)

        # ---- 8. endcard ------------------------------------------------------
        self.play(
            FadeOut(row_fine),
            FadeOut(height_brace),
            FadeOut(base_brace),
            FadeOut(header),
            FadeOut(header_panel),
            VGroup(result, result_panel).animate.scale(1.2).move_to(UP * 2.5),
            run_time=0.9,
        )

        closing_text = wrap(
            "At Quantica you don't memorise the result. You build it.", 21
        )
        closing = brand_text(
            closing_text, size=40, color=th.ink, line_spacing=0.85
        )
        from typeset import centre_lines

        centre_lines(closing, closing_text.count("\n") + 1)
        closing.move_to(UP * 0.1)
        assert closing.width < 8.4, f"closing card overflows ({closing.width:.2f})"

        url = brand_text("quanticaedu.com", size=38, color=th.ink)
        url.move_to(DOWN * 2.1)
        url_panel = panel(url, th, pad_x=0.34, pad_y=0.17)

        self.clear_caption()
        self.remove(self.wordmark)

        # Silent, like the other video. The words are on screen and the proof has
        # already landed, so a spoken sign-off would only read as an ad.
        self.play(FadeIn(closing, shift=UP * 0.2), run_time=0.85)
        self.play(FadeIn(url_panel, scale=0.9), FadeIn(url, scale=0.9), run_time=0.55)
        self.wait(2.3)


# ---------------------------------------------------------------------------
# layout checks
# ---------------------------------------------------------------------------


class _LayoutBase(Scene):
    """Every zone populated at once, so a single still shows up any collision."""

    stage = "circle"

    def construct(self):
        th = THEME
        self.camera.background_color = th.bg
        fig = Figure(th)

        if self.stage == "circle":
            figure = VGroup(fig.wedges(COARSE))
            extras = VGroup()
        else:
            row = fig.row(COARSE)
            height_brace, base_brace = fig.row_braces(row)
            figure = VGroup(row)
            extras = VGroup(height_brace, base_brace)

        equation = eq_setup(th).move_to(UP * EQUATION_Y)
        caption = caption_block(
            "Half the arcs are the base, so it is *πr*.",
            th,
            size=CAPTION_SIZE,
            max_width=CAPTION_WIDTH,
        ).move_to(CAPTION_CENTER)

        wordmark = brand_text("quanticaedu.com", size=26, color=th.gray)
        wordmark.move_to([-2.55, -7.35, 0])
        milo = MiloActor(MILO_ANCHOR, body_height=MILO_HEIGHT, pose="excited")
        header = eq_header(th).move_to(UP * TITLE_Y)

        self.add(figure, extras, equation, header, caption, wordmark, milo)

        whole = VGroup(figure, extras)
        gaps = [
            ("header -> figure", header.get_bottom()[1] - whole.get_top()[1]),
            ("figure -> equation", whole.get_bottom()[1] - equation.get_top()[1]),
            ("equation -> caption", equation.get_bottom()[1] - caption.get_top()[1]),
            ("caption -> milo", caption.get_bottom()[1] - milo.get_top()[1]),
        ]
        print(f"[layout] row width {ROW_WIDTH:.2f} (frame 9.0, safe 8.0)")
        print(f"[layout] equation width {equation.width:.2f} (limit 8.2)")
        for name, gap in gaps:
            flag = "  <-- COLLISION" if gap < 0 else ""
            print(f"[layout] {name:22s} {gap:+.2f}{flag}")


class LayoutCheckCircle(_LayoutBase):
    stage = "circle"


class LayoutCheckRow(_LayoutBase):
    stage = "row"
