"""
The shared shape of a narrated Quantica ad: vertical format, Milo in the corner,
burned-in captions, and narration that every animation is sized against. Ported from
milo_manim/milo_scene.py; the type layer underneath moved to Chillax and the current
palette, see typeset.py.

A video imports ``MiloVoiceoverScene`` and the layout constants, then only has to
write its own figure and its own beats.

    from milo_scene import MiloVoiceoverScene, apply_vertical_format, EQUATION_Y
    from typeset import LIGHT

    apply_vertical_format(LIGHT)

    class MyAd(MiloVoiceoverScene):
        theme = LIGHT
        def construct(self):
            self.open_with_milo()
            with self.say("Some line.", caption="Some *line*.") as t:
                self.play(..., run_time=t.duration * 0.8)

These scenes pin their own 1080x1920 frame at import, so they render as reels only.
The QUANTICA_FORMAT machinery in scenes/base.py does not apply to them.
"""

import numpy as np
from manim import config
from manim_voiceover import VoiceoverScene

from milo_actor import MiloActor
from typeset import brand_text, caption_block
from voice import QuanticaVoice

# ---------------------------------------------------------------------------
# format and layout
#
# Text sits centred above and below the figure at full frame width, rather than
# being pushed to one side. Milo drops into the corner underneath the caption.
# ---------------------------------------------------------------------------

FRAME_W, FRAME_H = 9, 16

DIAGRAM_CENTER = np.array([0.0, 2.35, 0.0])
TITLE_Y = 6.15
EQUATION_Y = -1.6
CAPTION_CENTER = np.array([0.0, -3.1, 0.0])
CAPTION_SIZE = 38
CAPTION_WIDTH = 8.0

MILO_ANCHOR = np.array([2.85, -7.5, 0.0])
MILO_HEIGHT = 2.1
WORDMARK_AT = np.array([-2.55, -7.3, 0.0])


def apply_vertical_format(theme):
    """1080x1920 at 30fps, set at module level so it beats the -q CLI flag."""
    config.pixel_width = 1080
    config.pixel_height = 1920
    config.frame_width = FRAME_W
    config.frame_height = FRAME_H
    config.frame_rate = 30
    config.background_color = theme.bg


# ---------------------------------------------------------------------------
# pronunciation
#
# "a" is the one letter that is also an English word, so a bare "a" gets read as the
# article, "uh", instead of the letter name. An SSML phoneme tag is the exact fix,
# and it is why voice.py renders on eleven_turbo_v2: multilingual v2 refuses phoneme
# tags outright, and only Flash v2, Turbo v2 and English v1 accept them.
#
# Respelling was tried first and does not hold up. A capital "A" reads as the letter
# in front of "and", "plus" or "b", then reverts to the article in front of
# "squared", because "a squared" is grammatical English. The tag is context-free.
#
# Which "a" is which cannot be decided automatically. "Start with a right triangle"
# wants the article and "sides are a and b" wants the letter, in the same video. So
# the letter is written {a} in every narration line, and a plain "a" is always the
# article. b, c and r need no help, since none of them is an English word.
#
# "pi" has no ambiguity to resolve, unlike "a", but confirmed by ear it still needs
# help: on its own it is not a common English word, and the engine does not reliably
# land on the diphthong ("pie") rather than a short vowel. Respelling settles it, so
# it does not need the SSML machinery the letter does. Every "pi" in narration is
# written {pi}, and the .srt sidecar still shows "pi", since that is the correct
# spelling for a reader.
#
# "r" is confirmed by ear to need the same exact fix as "a": bare "r" was landing
# harsh, close to spelling out the letter as if barked rather than said. Unlike "a"
# there is no article to collide with, so no context-dependence, but the fix is the
# same phoneme tag rather than a respelling, since a respelling is a guess about how
# the model reads English orthography and the tag is not. AA1 R is the same ARPABET
# ending as "car" or "far", which is how the letter name "r" actually sounds.
#
# The expansions below are part of the voiceover cache key. Changing one invalidates
# every cached take of every line that uses it, so do not touch them without an
# ELEVENLABS_API_KEY exported and a reason to re-record.
# ---------------------------------------------------------------------------

PRONOUNCE = {
    "{a}": '<phoneme alphabet="cmu-arpabet" ph="EY1">a</phoneme>',
    "{pi}": "pie",
    "{r}": '<phoneme alphabet="cmu-arpabet" ph="AA1 R">r</phoneme>',
}


def for_speech(line):
    """The narration line as the TTS engine should receive it."""
    for marker, sound in PRONOUNCE.items():
        line = line.replace(marker, sound)
    return line


def as_written(line):
    """The same line as a human should read it, for the .srt sidecar."""
    for marker in PRONOUNCE:
        line = line.replace(marker, marker[1:-1])
    return line


_SPOKEN_LINE = object()  # sentinel: caption defaults to whatever Milo says


class MiloVoiceoverScene(VoiceoverScene):
    """A narrated Quantica ad with Milo presenting from the corner."""

    theme = None  # set by the subclass

    def setup(self):
        super().setup()
        self.camera.background_color = self.theme.bg
        self.set_speech_service(QuanticaVoice())
        self._caption = None

    # -- opening -----------------------------------------------------------

    def open_with_milo(self, pose="neutral"):
        """Put the wordmark down and walk Milo on. Returns the wordmark."""
        self.milo = MiloActor(MILO_ANCHOR, body_height=MILO_HEIGHT, pose=pose)
        self.wordmark = brand_text("quanticaedu.com", size=26, color=self.theme.gray)
        self.wordmark.move_to(WORDMARK_AT)
        self.add(self.wordmark)
        self.milo.enter(self, run_time=0.6)
        return self.wordmark

    # -- narration ---------------------------------------------------------

    def say(self, line, caption=_SPOKEN_LINE):
        """Speak a line, show it as a caption, and keep Milo animated while it runs.

        These ads get watched with the sound off, so every spoken line also goes on
        screen, dark and large. ``caption`` overrides the wording where speech and
        text should differ, "a squared" against "a²". Anything wrapped in asterisks
        is set on a highlighter band, and a marked span is never broken across lines,
        which is what keeps an equation whole. Pass ``None`` for a beat with no
        caption.

        Returns the tracker so the caller can size its animations to the audio
        instead of guessing run times.
        """
        scene = self

        class _Beat:
            def __enter__(self):
                # The engine gets the phoneme tag, the subtitle sidecar gets "a".
                self._cm = scene.voiceover(
                    text=for_speech(line), subcaption=as_written(line)
                )
                tracker = self._cm.__enter__()
                shown = line if caption is _SPOKEN_LINE else caption
                if shown is None:
                    scene.clear_caption()
                else:
                    scene.set_caption(shown)
                scene.milo.speaking = True
                return tracker

            def __exit__(self, *exc):
                scene.milo.speaking = False
                return self._cm.__exit__(*exc)

        return _Beat()

    def set_caption(self, text):
        new = caption_block(
            text, self.theme, size=CAPTION_SIZE, max_width=CAPTION_WIDTH
        )
        new.move_to(CAPTION_CENTER)
        if self._caption is not None:
            self.remove(self._caption)
        self.add(new)
        self._caption = new

    def clear_caption(self):
        if self._caption is not None:
            self.remove(self._caption)
            self._caption = None
