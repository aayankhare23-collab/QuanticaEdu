"""Setting mathematics without LaTeX.

There is no TeX distribution on this machine, so MathTex does not degrade gracefully, it
raises FileNotFoundError looking for `latex`. Installing one is possible (BasicTeX plus
about a dozen tlmgr packages, roughly 700MB) but it is the wrong trade for ads. MathTex sets
type in Computer Modern, a serif face that looks nothing like Chillax, so a MathTex equation
dropped into a Quantica ad reads as a screenshot from a different company. Matching the
brand from the TeX side means mathastext plus a locally installed Chillax, which is a lot of
work to arrive back where Text() already is.

So everything here builds equations out of Text pieces. What this handles cleanly covers
every ad a prealgebra and algebra product would want to run. Linear equations and each step
of solving them, powers via unicode superscripts, negatives and the real multiplication and
division glyphs, fractions as a VGroup with a drawn rule, and anything on axes.

Where it genuinely stops is radicals with a proper vinculum, integrals, summation with
limits above and below, matrices, and deeply nested fractions. None of those belong in a
ten second feed ad. If one specific hero equation needs real typesetting, export the app's
own KaTeX output as SVG and bring it in with SVGMobject, which matches the product exactly
and still needs no TeX install.
"""

from manim import DOWN, ITALIC, LEFT, RIGHT, UP, Line, Text, VGroup

SUPERSCRIPT = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
    "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "n": "ⁿ", "+": "⁺", "-": "⁻",
}

MINUS = "−"      # true minus, not a hyphen
TIMES = "×"
DIVIDE = "÷"
NEQ = "≠"
LEQ = "≤"
GEQ = "≥"

# Anything that is a bare operator or a number stays upright. Anything containing a letter
# is a variable and gets an oblique slant, which is how mathematics is conventionally set
# and what makes an expression read as mathematics rather than as a sentence.
_UPRIGHT = set("0123456789+=<>()[]{}.,/ ") | {MINUS, TIMES, DIVIDE, NEQ, LEQ, GEQ}


def _is_variable(piece):
    return any(ch.isalpha() for ch in piece)


def power(base, exponent):
    """Render a power using unicode superscripts. power('a', 2) gives a-squared."""
    sup = "".join(SUPERSCRIPT.get(ch, ch) for ch in str(exponent))
    return f"{base}{sup}"


def math_run(pieces, font, size=64, color="#16281B"):
    """Lay out an equation from (text, colour) pairs and return a single Text.

    One Text, not a VGroup of them. An earlier version built each term separately and
    arranged them left to right, which meant every baseline had to be reconciled by hand,
    and it got it wrong. Operators sat below the digits because arrange() centres on the
    bounding box and a superscript or a tall digit moves that box. Pango already solves
    this, along with kerning and the spacing either side of an equals sign, so the fix is
    to hand it the whole string and colour ranges within it rather than to reimplement
    typesetting.

    Variables are slanted and operators and numbers stay upright, which is the convention
    that makes a line read as mathematics rather than as a sentence.

    `pieces` is a list of either "x" or ("x", "#BEFF8B").
    """
    text = ""
    t2c = {}
    t2s = {}
    for piece in pieces:
        s, col = piece if isinstance(piece, (tuple, list)) else (piece, None)
        start = len(text)
        text += s
        end = len(text)
        if not s.strip():
            continue
        # Index ranges rather than substring keys. A substring key colours every occurrence,
        # and "2" appears twice in "2x + 3 = 11 - 2".
        key = f"[{start}:{end}]"
        if col:
            t2c[key] = col
        if _is_variable(s) and s.strip() not in _UPRIGHT:
            t2s[key] = ITALIC

    return Text(text, font=font, font_size=size, color=color, t2c=t2c, t2s=t2s)


def fraction(numerator, denominator, font, size=64, color="#16281B", rule_color=None):
    """A fraction as numerator, a drawn rule, denominator.

    Ten lines, and you control the bar weight so it matches the brand rule rather than
    whatever a TeX vinculum happens to be.
    """
    num = Text(str(numerator), font=font, font_size=size, color=color)
    den = Text(str(denominator), font=font, font_size=size, color=color)
    width = max(num.width, den.width) * 1.25
    bar = Line(LEFT * width / 2, RIGHT * width / 2,
               color=rule_color or color, stroke_width=size / 14)
    return VGroup(num, bar, den).arrange(DOWN, buff=size / 420)
