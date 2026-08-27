#!/usr/bin/env python
"""Render a scene to a Meta-ready MP4.

    manim/.venv/bin/python manim/render.py SolveIt --format reel

Manim's own encode is fine but not guaranteed to satisfy Meta, so this runs a second ffmpeg
pass that stamps the settings Meta actually wants. H.264 high profile, yuv420p chroma
because Meta rejects yuv444p and some players show green frames, silent AAC because a video
with no audio track is treated inconsistently, and +faststart so the moov atom sits at the
front and the file starts playing before it has finished downloading.
"""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
FORMATS = ("reel", "feed", "square")

# scene name -> module file in scenes/. A "fixed" entry pins its own frame at module
# import (the narrated Milo scenes are laid out for 9:16 only), so asking render.py for
# another format would silently produce a reel anyway; refuse instead.
SCENES = {
    "SolveIt": {"file": "solve_it.py"},
    "PythagorasWithMilo": {"file": "pythagoras.py", "fixed": "reel"},
    "CircleAreaWithMilo": {"file": "circle_area.py", "fixed": "reel"},
    "PythagoreanProofWithMilo": {"file": "pythagorean_proof.py", "fixed": "reel"},
    "BayesPositive": {"file": "bayes.py"},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scene", help=f"one of {', '.join(SCENES)}")
    ap.add_argument("--format", default="reel", choices=FORMATS)
    ap.add_argument("--quality", default="h", choices=list("lmhpk"),
                    help="manim quality flag, h is 1080p and the right default here")
    ap.add_argument("--no-cache", action="store_true",
                    help="manim reuses cached partial movie files, so a text change can "
                         "render on top of stale geometry. Pass this while iterating.")
    args = ap.parse_args()

    if args.scene not in SCENES:
        sys.exit(f"Unknown scene {args.scene}. Known scenes: {', '.join(SCENES)}")

    entry = SCENES[args.scene]
    fixed = entry.get("fixed")
    if fixed and args.format != fixed:
        sys.exit(
            f"{args.scene} pins its frame to {fixed} at module import, so a "
            f"--format {args.format} render would come out {fixed}-shaped anyway. "
            f"Rendering it in another shape means relaying the scene, not reflagging it."
        )

    scene_file = HERE / "scenes" / entry["file"]

    # The format is a class attribute, so it is overridden by writing an env var the scene
    # reads rather than by a CLI flag manim does not have.
    env_line = f"QUANTICA_FORMAT={args.format}"

    cmd = [str(HERE / ".venv" / "bin" / "manim"), "-q", args.quality, str(scene_file), args.scene]
    if args.no_cache:
        cmd.append("--disable_caching")

    print(f"$ {env_line} {' '.join(cmd)}")
    import os
    env = dict(os.environ, QUANTICA_FORMAT=args.format)
    subprocess.run(cmd, cwd=str(HERE), env=env, check=True)

    # manim writes to media/videos/<script>/<height>p<fps>/<Scene>.mp4
    produced = sorted((HERE / "media" / "videos").rglob(f"{args.scene}.mp4"),
                      key=lambda p: p.stat().st_mtime)
    if not produced:
        sys.exit("manim reported success but no mp4 was found under manim/media/videos")
    src = produced[-1]

    out = HERE / "out" / f"{args.scene}_{args.format}.mp4"

    # A narrated scene already carries its ElevenLabs track and that track must survive
    # untouched, so probe rather than assume. Only a genuinely silent render gets the
    # anull track, which exists because Meta treats a video with no audio stream
    # inconsistently.
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(src)],
        capture_output=True, text=True,
    )
    has_audio = "audio" in probe.stdout

    ff = ["ffmpeg", "-y", "-i", str(src)]
    if not has_audio:
        ff += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
               "-shortest"]
    ff += [
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-crf", "18", "-preset", "slow",
        "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "160k",
        str(out),
    ]
    print(f"$ {' '.join(ff)}")
    subprocess.run(ff, check=True, capture_output=True)

    # manim-voiceover writes an .srt of the narration next to the video. Keep it with
    # the finished cut; Meta accepts SRT captions directly.
    srt = src.with_suffix(".srt")
    if srt.exists():
        out_srt = out.with_suffix(".srt")
        out_srt.write_bytes(srt.read_bytes())
        print(f"wrote {out_srt}")

    size_mb = out.stat().st_size / 1e6
    print(f"\nwrote {out}  ({size_mb:.1f} MB, audio: {'kept' if has_audio else 'silent track added'})")
    print("Check it reads with the sound off before you upload it.")


if __name__ == "__main__":
    main()
