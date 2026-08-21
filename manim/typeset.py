"""
The type and caption layer for the Milo ad scenes, ported from milo_manim/quantica.py.

Three things changed in the port, all deliberate, and everything else is the original
machinery kept intact because each piece of it exists to fix something that looked wrong
on screen.

The face is Chillax. The original set everything in Space Grotesk, which was the brand's
display face at the time. Chillax is both display and body on paths/landing.html now, the
page these ads land on. Registration goes through brand.register_fonts, which raises when
the family is missing rather than letting Pango substitute silently. Chillax ships here as
a single Semibold file, so nothing requests BOLD; Pango would resolve the request to the
same face at best and fake-embolden it at worst, and Semibold already carries the weight
the landing page has.

The palette is the current one. milo_manim's WEMBI themes encode the retired .wmb set.
AdTheme below keeps the old role vocabulary the scenes were written against (slate is the
ordinary surface, lime is the surface that matters, ink rules everything) but the values
come from brand.py, which copies the :root of paths/landing.html verbatim. The one
judgment call is slate. The brand has no grey-blue, and its closest mid-tone is SAGE,
which keeps the original figure's value structure: the ordinary surface reads darker than
lime, so alternating wedges stay distinguishable and ink labels stay legible on top of it.
TINT_2 is on the theme as ``surface`` for broad passive panels, but as a fill opposite
lime it is too close in value to alternate against.

Corners are square. The original pill() drew a RoundedRectangle; Quantica's radius is 0
on every surface, so the same treatment is now panel() and draws a Rectangle.
"""

from manim import (
    DOWN,
    ITALIC,
    NORMAL,
    RIGHT,
    MarkupText,
    Rectangle,
    Text,
    VGroup,
)

import brand

_FONT = None


def use_brand_font():
    """Register the brand fonts once and return the family for Text().

    brand.register_fonts raises if Chillax is not visible to Pango after registration,
    which is the loud failure this project prefers over a silently substituted face.
    """
    global _FONT
    if _FONT is None:
        brand.register_fonts(required=("Chillax", "Space Grotesk"))
        _FONT = brand.DISPLAY
    return _FONT


class AdTheme:
    """One coherent set of colours for an ad scene, in the old role vocabulary.

    The figure runs on two surfaces and one rule, exactly as the landing page does.
    Slate is the ordinary surface, lime is the surface that matters, and everything is
    separated by an ink rule. The scenes read these roles, never raw swatches.
    """

    def __init__(self, bg, ink, lime, slate, gray, gray_soft, seam=None, surface=None):
        self.bg = bg
        self.ink = ink  # near-black. All text, all rules.
        self.lime = lime  # the highlighter, and the payoff surface
        self.slate = slate  # the ordinary surface, and the triangles
        self.gray = gray  # AA-safe de-emphasis at any size
        self.gray_soft = gray_soft  # large text only
        self.seam = seam or ink
        self.surface = surface or slate

        # Names the scene reads by intent rather than by swatch.
        self.muted = gray
        self.faint = gray_soft
        self.highlight = lime
        self.tri_fill = slate
        self.tri_stroke = ink


LIGHT = AdTheme(
    bg=brand.PAPER,
    ink=brand.INK,
    lime=brand.LIME,
    slate=brand.SAGE,
    gray=brand.GRAY,
    gray_soft=brand.GRAY_SOFT,
    surface=brand.TINT_2,
)

DARK = AdTheme(
    bg=brand.FOREST,
    ink=brand.PAPER,
    lime=brand.LIME,
    slate=brand.SAGE,
    gray=brand.TINT_2,
    gray_soft=brand.SAGE,
    seam=brand.PAPER,
    surface=brand.FOREST_2,
)


# ---------------------------------------------------------------------------
# type helpers
# ---------------------------------------------------------------------------


def brand_text(s, size=32, color=None, weight=NORMAL, slant=NORMAL, **kw):
    return Text(
        s,
        font=use_brand_font(),
        font_size=size,
        color=color,
        weight=weight,
        slant=slant,
        **kw,
    )


def math_run(parts, size=44, buff=0.13):
    """Lay out a line of maths as coloured pieces.

    ``parts`` is a list of ``(string, colour)``. There is no LaTeX on this machine, so
    variables are set in the display face with an oblique slant, which reads close
    enough to italic maths at video sizes. This returns a VGroup with one submobject
    per piece because the scenes animate pieces individually; mathtype.math_run returns
    a single Text and is the right tool when nothing needs to move on its own.
    """
    group = VGroup()
    operators = []
    for i, (s, color) in enumerate(parts):
        # Anything carrying a letter is a term and gets set oblique. That covers
        # "a²" and "(a + b)²" and "4(½ab)" alike, and leaves + and = upright.
        is_term = any(ch.isalpha() for ch in s)
        group.add(
            brand_text(
                s,
                size=size,
                color=color,
                slant=ITALIC if is_term else NORMAL,
            )
        )
        if not is_term:
            operators.append(i)

    group.arrange(RIGHT, buff=buff, aligned_edge=DOWN)

    # Operators belong on the maths axis, roughly the middle of a lowercase letter.
    # Bottom-aligning them instead leaves + and = sitting visibly low next to a term
    # whose bounding box is stretched upward by its superscript.
    term = group[0]
    axis = term.get_bottom()[1] + 0.32 * term.height
    for i in operators:
        group[i].set_y(axis)
    return group


def wrap(s, max_chars=36):
    """Greedy word wrap. Captions are short, so this is enough."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) > max_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# captions
# ---------------------------------------------------------------------------


def _escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _atoms(text):
    """Split ``*marked*`` text into unbreakable atoms of tagged characters.

    Two rules, both of which exist because of something that looked wrong on screen.

    Working per character rather than per word matters at a span boundary. In
    "side *c*, so", the comma is not marked and is not a word of its own, so a
    word-level split would push it onto the far side of a space and leave the band
    reading "c ,".

    Breaking only on *unmarked* whitespace is what keeps a marked span whole. A
    marked span is a unit, and an equation is the case that matters: wrapping inside
    "*a² + b² = c²*" strands "= c²" alone on the next line and cuts the highlighter
    band in half. A span that will not fit alongside its neighbours moves to the next
    line entire.
    """
    tagged = []
    for i, segment in enumerate(text.split("*")):
        marked = i % 2 == 1
        tagged.extend((ch, marked) for ch in segment)

    atoms, current = [], []
    for ch, marked in tagged:
        if ch.isspace() and not marked:
            if current:
                atoms.append(current)
                current = []
        else:
            current.append((ch, marked))
    if current:
        atoms.append(current)
    return atoms


def _atom_markup(atom, theme):
    """One atom as Pango markup, banding each run of marked characters."""
    out, run, run_marked = [], [], atom[0][1]
    for ch, marked in atom:
        if marked != run_marked:
            out.append(_span("".join(run), run_marked, theme))
            run, run_marked = [], marked
        run.append(ch)
    out.append(_span("".join(run), run_marked, theme))
    return "".join(out)


def _span(chunk, marked, theme):
    chunk = _escape(chunk)
    if not marked:
        return chunk
    return f'<span background="{theme.highlight}">{chunk}</span>'


def panel(mob, theme, color=None, pad_x=0.17, pad_y=0.10):
    """A solid square-cornered panel sized to a mobject.

    The original called this pill and rounded it. Quantica's radius is 0 on every
    surface, so the panel is a plain Rectangle now. Returned separately rather than
    grouped, so the caller controls when it appears and so it does not disturb
    submobject indices in an equation.
    """
    box = Rectangle(
        width=mob.width + 2 * pad_x,
        height=mob.height + 2 * pad_y,
        fill_color=color or theme.lime,
        fill_opacity=1,
        stroke_width=0,
    )
    box.move_to(mob)
    box.set_z_index(mob.z_index - 1)
    return box


def centre_lines(block, n_lines):
    """Centre each visual line of a text mobject on the block's own axis.

    Pango left-aligns, and manim's ``MarkupText`` hardcodes ``pango_width`` without
    ever passing an ``alignment`` through, so anything that wraps comes out ragged
    with the short line stuck to the left edge. Manim's ``Text`` behaves the same.

    Glyphs come back in reading order at a uniform line pitch, so binning by pitch
    and re-centring each bin horizontally is enough. Only x moves, which leaves
    Pango's vertical layout and baselines exactly as it laid them out. Rebuilding
    each line as its own mobject and stacking them would not, because a line with no
    descender would sit at a different height from one that has a comma in it.
    """
    if n_lines < 2:
        return block

    top, bottom = block.get_top()[1], block.get_bottom()[1]
    pitch = (top - bottom) / n_lines
    rows = [[] for _ in range(n_lines)]
    for glyph in block.submobjects:
        index = int((top - glyph.get_center()[1]) / pitch)
        rows[min(max(index, 0), n_lines - 1)].append(glyph)

    assert all(rows), f"line binning lost a row: {[len(r) for r in rows]}"

    axis = block.get_center()[0]
    for row in rows:
        group = VGroup(*row)
        group.shift(RIGHT * (axis - group.get_center()[0]))
    return block


def _caption_markup(atoms, theme, size, char_limit):
    """Wrap atoms to lines and build the caption."""
    lines, current, used = [], [], 0
    for atom in atoms:
        cost = len(atom) + (1 if current else 0)
        if current and used + cost > char_limit:
            lines.append(current)
            current, used, cost = [], 0, len(atom)
        current.append(atom)
        used += cost
    if current:
        lines.append(current)

    # No widows. A last line holding one short atom reads as a mistake, and it is
    # worst in exactly the case this is written for: "...of radius" / "r." leaves a
    # single italic letter stranded under a full line. Pull a word down to join it.
    if len(lines) > 1 and len(lines[-1]) == 1 and len(lines[-2]) > 1:
        if len(lines[-1][0]) <= 3:
            lines[-1].insert(0, lines[-2].pop())

    rendered = [
        " ".join(_atom_markup(atom, theme) for atom in line) for line in lines
    ]
    # Chillax Semibold is the only weight registered and it already carries the
    # landing page's heft, so no <b> here. The band is what separates a marked
    # phrase from the rest, not weight.
    block = MarkupText(
        "\n".join(rendered),
        font=use_brand_font(),
        font_size=size,
        color=theme.ink,
        line_spacing=0.7,
    )
    return centre_lines(block, len(rendered))


def caption_block(text, theme, size=33, max_width=6.0):
    """A caption in the ink colour, with ``*marked*`` spans on a highlighter band.

    Pango draws the band itself, which is why this goes through MarkupText rather
    than measuring word boxes. Laying the words out by hand would mean re-deriving
    baselines and kerning, and font ligatures ("fi") make character index into glyph
    index unreliable.

    The character limit is only a first guess. The result is measured and the wrap
    tightened until it actually fits, so a caption can never run under Milo.
    """
    atoms = _atoms(text)

    block = None
    for char_limit in range(30, 11, -2):
        block = _caption_markup(atoms, theme, size, char_limit)
        if block.width <= max_width:
            return block

    # Overflowing silently would put the caption under Milo, so fail instead. The
    # usual cause is one marked span too long to sit on a line by itself, since a
    # span is never broken.
    raise ValueError(
        f"caption will not fit {max_width} units even at the tightest wrap "
        f"(got {block.width:.2f}): {text!r}. Shorten it, or split one long "
        f"*marked* span into two."
    )
