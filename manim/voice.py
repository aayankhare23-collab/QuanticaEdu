"""
Speech for Milo, ported from ~/manim-projects/milo_manim/voice.py.

The audio itself is already synthesised. Every narration line in the ad scenes has an
ElevenLabs take cached in ``manim/voiceovers/`` (cache.json plus the mp3s), and the cache
is consulted before anything is sent to an API, so a normal render needs no key at all.
That cache is the preserved voiceover. Do not delete it; regenerating costs API credits
and produces different takes.

The provider therefore defaults to ElevenLabs unconditionally. If a line changes, the
cache misses and this raises with instructions rather than quietly re-recording the ad
in a different voice. Export the key only when a line is genuinely new:

    export ELEVENLABS_API_KEY=sk_...

``QUANTICA_VOICE`` can still pin another provider (``openai``, ``macos``) for pacing
experiments, but those takes land in the same cache keyed by provider, so they can
never overwrite the ElevenLabs audio.

The voice id is a public identifier, not a secret, so it lives here and can be
overridden with EL_VOICE. The cache key is (text, service, provider, voice), and the
values below must stay exactly as they were in milo_manim or every lookup misses.
"""

import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService, initialize_speech_service

ROOT = Path(__file__).parent

EL_VOICE = os.environ.get("EL_VOICE", "kdmDKE6EkgrWrrykO9Qt")

# Turbo rather than multilingual, because SSML <phoneme> tags are the only exact way
# to make the engine say the letter "a", and multilingual v2 does not accept them.
# Only Flash v2, Turbo v2 and English v1 do. See the pronunciation notes in
# milo_scene.py. This applies to the whole video on purpose. Using Turbo for the one
# line that needs a phoneme tag and multilingual for the rest would put a single line
# in a noticeably different voice.
EL_MODEL = os.environ.get("EL_MODEL", "eleven_turbo_v2")
OA_VOICE = os.environ.get("OA_VOICE", "onyx")
OA_MODEL = os.environ.get("OA_MODEL", "gpt-4o-mini-tts")
MAC_VOICE = os.environ.get("MAC_VOICE", "Samantha")


def active_provider():
    """ElevenLabs, unless QUANTICA_VOICE pins something else.

    The milo_manim original chose a provider from whichever key was exported, which
    meant a keyless shell silently fell through to the macOS voice and a cache miss
    re-recorded a line in the wrong voice. Here the cached ElevenLabs takes are the
    product, so ElevenLabs is the default whether or not a key is present. A full
    cache hit never needs one.
    """
    return os.environ.get("QUANTICA_VOICE") or "elevenlabs"


_KEY_FOR = {"elevenlabs": "ELEVENLABS_API_KEY", "openai": "OPENAI_API_KEY"}


def _post(url, payload, headers, out_path):
    request = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:300].decode("utf8", "replace")
        raise RuntimeError(f"{url} -> HTTP {exc.code}: {detail}")
    Path(out_path).write_bytes(data)


class QuanticaVoice(SpeechService):
    """Milo's narration, cached by manim-voiceover so re-renders cost nothing."""

    def __init__(self, provider=None, **kwargs):
        # The cache lives in a committed directory rather than under media/, which is
        # gitignored. These takes are paid-for assets, not render byproducts.
        kwargs.setdefault("cache_dir", str(ROOT / "voiceovers"))
        initialize_speech_service(self, kwargs)
        self.provider = provider or active_provider()

    def generate_from_text(self, text, cache_dir=None, path=None, **kwargs):
        cache_dir = Path(cache_dir or self.cache_dir)
        spoken = remove_bookmarks(text)

        # Provider and voice go into the cache key, so switching either one
        # regenerates rather than silently reusing the old take.
        input_data = {
            "input_text": spoken,
            "service": "quantica",
            "provider": self.provider,
            "voice": self._voice_id(),
        }

        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached

        basename = path or (self.get_audio_basename(input_data) + ".mp3")

        needed = _KEY_FOR.get(self.provider)
        if needed and not os.environ.get(needed):
            raise RuntimeError(
                f"Cache miss for {self.provider!r} on {spoken[:48]!r} and {needed} is "
                f"not set. The line changed since it was last synthesised, so it has "
                f"to be regenerated. Export {needed} and render again."
            )

        self._synthesise(spoken, cache_dir / basename)

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": str(basename),
        }

    def _voice_id(self):
        return {
            "elevenlabs": EL_MODEL + "/" + EL_VOICE,
            "openai": OA_MODEL + "/" + OA_VOICE,
            "macos": MAC_VOICE,
        }[self.provider]

    def _synthesise(self, text, out_path):
        raw = str(out_path) + (".aiff" if self.provider == "macos" else ".src")

        if self.provider != "elevenlabs":
            # Nothing else here understands SSML, and a fallback voice reading
            # "phoneme alphabet cmu arpabet" out loud is worse than a wrong vowel.
            text = re.sub(r"<phoneme[^>]*>(.*?)</phoneme>", r"\1", text)

        if self.provider == "elevenlabs":
            _post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{EL_VOICE}",
                {
                    "text": text,
                    "model_id": EL_MODEL,
                    "voice_settings": {
                        "stability": 0.45,
                        "similarity_boost": 0.75,
                        "style": 0.0,
                        "use_speaker_boost": True,
                    },
                },
                {
                    "xi-api-key": os.environ["ELEVENLABS_API_KEY"],
                    "Content-Type": "application/json",
                    "Accept": "audio/mpeg",
                },
                raw,
            )
        elif self.provider == "openai":
            _post(
                "https://api.openai.com/v1/audio/speech",
                {
                    "model": OA_MODEL,
                    "voice": OA_VOICE,
                    "input": text,
                    "response_format": "mp3",
                },
                {
                    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
                    "Content-Type": "application/json",
                },
                raw,
            )
        else:
            subprocess.run(
                ["say", "-v", MAC_VOICE, "-r", "172", "-o", raw, text],
                check=True,
                timeout=90,
            )

        # Normalise everything to a plain 44.1k mp3 so manim's audio mux and the
        # duration probe both behave the same whichever provider ran.
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", raw,
             "-ar", "44100", "-ac", "1", "-b:a", "160k", str(out_path)],
            check=True,
        )
        os.remove(raw)


if __name__ == "__main__":
    print(f"provider that would be used: {active_provider()}")
