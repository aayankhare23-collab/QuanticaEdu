"""Quantica brand tokens for manim, and the font registration that makes them real.

Every colour here is copied verbatim from the :root block of paths/landing.html, which is
the page the ads land on and therefore the canonical palette. If that block changes, change
this file. Do not read tokens from landing.html instead. That file carries three other
:root blocks, including a retired navy and orange set and a .wmb set that is now behind
display:none, and picking the wrong one produces an ad in a palette the company stopped
using.

The font handling is the part that bites. Chillax, Switzer and Space Grotesk are webfonts,
loaded over the network by the site. Pango, which manim uses to set type, cannot fetch a
webfont, and when a family is missing it does not raise. It silently substitutes another
face and the render succeeds. The ad then ships in the wrong typeface with no error anywhere,
which is worse than a crash because nothing tells you. So register the files explicitly and
assert the family actually arrived.
"""

from pathlib import Path

import manimpango

FONT_DIR = Path(__file__).parent / "fonts"

# The families the brand actually uses. Chillax is both display and body on the landing
# page, so it is the one that matters most for ads. Space Grotesk is the mono face and is
# already on this machine, copied from tools/shorts/fonts. Switzer is body type inside the
# app rather than on the marketing page, so ads rarely need it.
BRAND_FONTS = {
    "Chillax": "Chillax-Semibold.otf",
    "Switzer": "Switzer-Medium.otf",
    "Space Grotesk": "SpaceGrotesk.ttf",
}


class MissingFont(RuntimeError):
    pass


def register_fonts(required=("Space Grotesk",)):
    """Register every brand font file present, then assert the required families exist.

    Returns the set of families that are usable. Anything in `required` that is missing
    raises, because a silent substitution is the failure mode this whole function exists
    to prevent. Families not in `required` are reported and allowed to be absent, so the
    scaffold works before someone has downloaded Chillax.
    """
    for family, filename in BRAND_FONTS.items():
        path = FONT_DIR / filename
        if path.exists():
            manimpango.register_font(str(path))

    available = set(manimpango.list_fonts())
    usable = {f for f in BRAND_FONTS if f in available}

    missing = [f for f in required if f not in available]
    if missing:
        raise MissingFont(
            f"Pango cannot see {', '.join(missing)}, so Text() would quietly render in a "
            f"substitute face and the ad would ship in the wrong typeface. Put the file in "
            f"{FONT_DIR} and name it as BRAND_FONTS expects. See manim/fonts/README.md."
        )
    return usable


class Theme:
    """One theme, named by role rather than by colour.

    Say theme.pop, not theme.lime. The scene should not care which green it is, and the
    palette has been regenerated once already.
    """

    def __init__(self, **kw):
        self.__dict__.update(kw)


# Copied verbatim from the :root block of paths/landing.html.
PAPER = "#FCFEFB"
PAPER_2 = "#EAF6E4"
CARD = "#FFFFFF"
BOX = "#EEF7E8"
AMBER = "#FBF2E2"
INK = "#16281B"
FOREST = "#14532D"
FOREST_2 = "#0F3D22"
ACCENT = "#15803D"
MOSS = "#1A9E4B"
GRASS = "#22C55E"
SAGE = "#5FA06B"
LIME = "#BEFF8B"
LIME_DEEP = "#96E85C"
TINT = "#E6F5E2"
TINT_2 = "#D2ECCB"
GRAY = "#52685A"
GRAY_SOFT = "#7C8C7E"
LINE = "#E1EEDB"
LINE_2 = "#EDF6E9"
HONEY = "#F59E0B"

LIGHT = Theme(
    name="light",
    bg=PAPER,
    ink=INK,
    primary=FOREST,
    pop=LIME,
    muted=GRAY,
    faint=GRAY_SOFT,
    rule=LINE,
    surface=TINT,
    good=GRASS,
    warn=HONEY,
)

# Dark is the better default for a feed. A deep forest field cuts through a scrolling
# timeline, and it is the brand's own --forest rather than a generic black.
DARK = Theme(
    name="dark",
    bg=FOREST,
    ink=PAPER,
    primary=LIME,
    pop=LIME,
    muted=TINT_2,
    faint=SAGE,
    rule=FOREST_2,
    surface=FOREST_2,
    good=LIME,
    warn=HONEY,
)

# Quantica has square corners. --radius and --radius-lg are both 0 on every surface, so a
# rounded rectangle is off brand. manim's RoundedRectangle exists and would quietly break
# this, so reach for Rectangle.
CORNER_RADIUS = 0

DISPLAY = "Chillax"
BODY = "Chillax"
MONO = "Space Grotesk"


def font_or_fallback(preferred, usable):
    """Use the brand face when it is registered, otherwise a face that definitely exists.

    Returning a real family name rather than None keeps Text() from falling into Pango's
    own default, which varies by machine.
    """
    return preferred if preferred in usable else "Space Grotesk"
