"""
Pluggable text to speech for the Quantica shorts.

Picks the best provider available, in this order:
  1. ELEVENLABS_API_KEY  -> ElevenLabs. This is what the good narration on educational
                            shorts almost always is. Best quality by a wide margin.
  2. OPENAI_API_KEY      -> OpenAI speech. Very good, much cheaper.
  3. macOS `say`         -> fallback. Robotic. Fine for judging pacing, not for posting.

Nothing here signs up for anything or stores a key. Export the key in your shell and it
gets used; otherwise it degrades to the local voice.

    export ELEVENLABS_API_KEY=...
    python3 voice23.py

Voice IDs are configurable at the top. Provider model names move around, so if a call
fails with "model not found", check the provider's current docs and update MODEL below.
"""
import json, os, subprocess, sys, urllib.request, urllib.error

# ---- provider config ------------------------------------------------------
# Aayan's chosen voice. A voice ID is a public identifier, not a secret, so it lives here.
# The API KEY is a secret and must never be written to a file, only exported in the shell.
EL_VOICE = os.environ.get("EL_VOICE", "kdmDKE6EkgrWrrykO9Qt")
EL_MODEL = os.environ.get("EL_MODEL", "eleven_multilingual_v2")
OA_VOICE = os.environ.get("OA_VOICE", "onyx")
OA_MODEL = os.environ.get("OA_MODEL", "gpt-4o-mini-tts")
MAC_VOICE = os.environ.get("MAC_VOICE", "Samantha")


def provider():
    if os.environ.get("ELEVENLABS_API_KEY"): return "elevenlabs"
    if os.environ.get("OPENAI_API_KEY"):     return "openai"
    return "macos"


def _post(url, payload, headers, out_path):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{url} -> HTTP {e.code}: {e.read()[:300].decode('utf8','replace')}")
    with open(out_path, "wb") as f:
        f.write(data)


def synth(text, wav_path):
    """Render `text` to a 44.1kHz mono wav at wav_path. Returns the provider used."""
    p = provider()
    raw = wav_path + (".mp3" if p != "macos" else ".aiff")

    if p == "elevenlabs":
        _post(f"https://api.elevenlabs.io/v1/text-to-speech/{EL_VOICE}",
              {"text": text, "model_id": EL_MODEL,
               "voice_settings": {"stability": 0.45, "similarity_boost": 0.75,
                                  "style": 0.0, "use_speaker_boost": True}},
              {"xi-api-key": os.environ["ELEVENLABS_API_KEY"],
               "Content-Type": "application/json", "Accept": "audio/mpeg"},
              raw)
    elif p == "openai":
        _post("https://api.openai.com/v1/audio/speech",
              {"model": OA_MODEL, "voice": OA_VOICE, "input": text,
               "response_format": "mp3"},
              {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
               "Content-Type": "application/json"},
              raw)
    else:
        for attempt in range(3):
            try:
                subprocess.run(["say", "-v", MAC_VOICE, "-o", raw, text],
                               check=True, timeout=30)
                break
            except subprocess.TimeoutExpired:
                pass
        else:
            raise RuntimeError("macOS say failed three times")

    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw,
                    "-ar", "44100", "-ac", "1", wav_path], check=True)
    os.remove(raw)
    return p


if __name__ == "__main__":
    p = provider()
    print(f"  provider that would be used: {p}")
    if p == "macos":
        print("  no api key set, so output will be the robotic local voice.")
        print("  set ELEVENLABS_API_KEY or OPENAI_API_KEY to get a natural one.")
    if "--test" in sys.argv:
        out = "/tmp/tts_test.wav"
        used = synth("Twenty five percent off twice is not fifty percent off.", out)
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
        print(f"  synthesised {d}s via {used} -> {out}")
