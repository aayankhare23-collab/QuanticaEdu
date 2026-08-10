"""QuanticaScene, the base class every ad scene should inherit.

It does four things a raw manim Scene does not.

It sets the frame to a real Meta ad shape. Setting pixel_width and pixel_height alone gives
a correctly sized but distorted frame, because manim maps scene units to the frame
separately. frame_width and frame_height have to match the same ratio or every circle comes
out an ellipse. Both are set together here so a scene cannot get it half right.

It registers the brand fonts before any Text is built, and raises if a required family is
missing rather than letting Pango substitute silently.

It exposes a safe area. On Reels and Stories the top and bottom roughly 250px sit under the
profile row, the caption and the CTA button, so type placed there is covered on a real phone
even though it looks fine in the render.

It applies the theme background, defaulting to dark, which reads better in a feed.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from manim import DOWN, UP, Scene, Text, VGroup, config

from brand import DARK, LIGHT, font_or_fallback, register_fonts, BODY, DISPLAY, MONO

# name -> (pixel_width, pixel_height, frame_width, frame_height)
FORMATS = {
    "reel": (1080, 1920, 9.0, 16.0),    # Reels and Stories, 9:16
    "feed": (1080, 1350, 8.0, 10.0),    # Feed vertical, 4:5, best performer of the feed shapes
    "square": (1080, 1080, 8.0, 8.0),   # Feed square, 1:1, safest single asset
}

# Fraction of frame height that is covered by platform chrome, top and bottom, on 9:16.
REEL_CHROME = 250 / 1920


class QuanticaScene(Scene):
    format_name = "reel"
    theme_name = "dark"
    fps = 30

    def __init__(self, *args, **kwargs):
        # render.py sets QUANTICA_FORMAT so one scene can be shot in all three ad shapes
        # without editing it. The class attribute is the default when running manim directly.
        self.format_name = os.environ.get("QUANTICA_FORMAT", self.format_name)
        if self.format_name not in FORMATS:
            raise ValueError(f"Unknown format {self.format_name}. Known: {', '.join(FORMATS)}")
        fmt = FORMATS[self.format_name]
        config.pixel_width, config.pixel_height = fmt[0], fmt[1]
        # Both pairs, always. Setting only the pixel dimensions gives a correctly sized but
        # distorted frame, and every circle comes out an ellipse.
        config.frame_width, config.frame_height = fmt[2], fmt[3]
        config.frame_rate = self.fps
        super().__init__(*args, **kwargs)

    def setup(self):
        self.usable_fonts = register_fonts(required=("Space Grotesk",))
        self.theme = DARK if self.theme_name == "dark" else LIGHT
        self.camera.background_color = self.theme.bg

        # Resolve once, so a scene never has to think about whether Chillax was downloaded.
        self.f_display = font_or_fallback(DISPLAY, self.usable_fonts)
        self.f_body = font_or_fallback(BODY, self.usable_fonts)
        self.f_mono = font_or_fallback(MONO, self.usable_fonts)

    @property
    def safe_top(self):
        """Highest y a caption can sit at without the platform covering it."""
        if self.format_name != "reel":
            return config.frame_height / 2 * 0.88
        return config.frame_height / 2 * (1 - 2 * REEL_CHROME)

    @property
    def safe_bottom(self):
        if self.format_name != "reel":
            return -config.frame_height / 2 * 0.88
        return -config.frame_height / 2 * (1 - 2 * REEL_CHROME)

    def caption(self, text, size=34):
        """A line of supporting type, placed inside the safe area.

        Feed video autoplays muted, so anything spoken has to be on screen as well. This is
        not a nicety, it is the difference between an ad that works and one that plays to
        someone who never hears it.
        """
        t = Text(text, font=self.f_body, font_size=size, color=self.theme.muted)
        t.move_to([0, self.safe_bottom, 0])
        return t

    def title(self, text, size=64):
        t = Text(text, font=self.f_display, font_size=size, color=self.theme.ink)
        t.move_to([0, self.safe_top, 0])
        return t

    def wordmark(self, size=30):
        """The signature. Every ad should end on it."""
        return Text("Quantica", font=self.f_display, font_size=size, color=self.theme.pop)
