# manim, for Meta ad animations

Renders branded 1080-wide animations for Facebook and Instagram ads. Separate from
`tools/shorts/`, which is the older hand-rolled pipeline and stays as it is.

## Setup

The venv already exists in the main checkout. A git worktree does not get it, since it is
gitignored, so symlink it in rather than building a second copy:

```bash
ln -sfn /path/to/main/checkout/manim/.venv manim/.venv
```

If it ever needs rebuilding, from the repo root:

```bash
python3 -m venv manim/.venv && manim/.venv/bin/pip install -r manim/requirements.txt
```

No `brew install` step is needed on this machine. pycairo and manimpango both ship arm64
wheels for Python 3.14, and the manimpango wheel bundles its own pango and harfbuzz. If pip
ever tries to build either from source, which shows up as `pkg-config not found` or
`cairo.h not found`, then `brew install cairo pango` is the fix.

## Render

```bash
manim/.venv/bin/python manim/render.py SolveIt --format reel
```

Formats are `reel` (1080x1920, 9:16), `feed` (1080x1350, 4:5) and `square` (1080x1080, 1:1).
Finished files land in `manim/out/`. Add `--no-cache` while iterating, because manim reuses
cached partial movie files and a text change will otherwise render on top of stale geometry.

The three Milo proof videos (`PythagorasWithMilo`, `CircleAreaWithMilo`,
`PythagoreanProofWithMilo`) pin their own 1080x1920 frame at module import, so they render
as reels only and `render.py` refuses other formats for them. The narrated ones keep their
ElevenLabs track through the encode and get an `.srt` sidecar beside the mp4; the silent
proof gets the stamped silent AAC track Meta wants.

## Voice

Narration is ElevenLabs, and every line of the narrated scenes is already synthesised and
cached in `voiceovers/` (cache.json plus the mp3s), which is committed because those takes
are paid-for assets, not render byproducts. A render needs **no API key**: `voice.py`
defaults to the elevenlabs provider and serves everything from cache. A cache-miss error
means a narration string drifted from what was recorded; restore the string rather than
re-recording. Only a genuinely new line needs `ELEVENLABS_API_KEY` exported. Narration
strings are cache keys, byte for byte, including the `{a}` / `{pi}` / `{r}` pronunciation
markers explained in `milo_scene.py`.

## Meta formats

| Name | Pixels | Ratio | Where it runs |
|---|---|---|---|
| `reel` | 1080x1920 | 9:16 | Reels and Stories |
| `feed` | 1080x1350 | 4:5 | Feed, takes more height on mobile than square |
| `square` | 1080x1080 | 1:1 | Feed, Explore, Marketplace |

Build to 10 to 15 seconds. Reels accept up to 90 and Stories up to 60, but delivery favours
short and a cold audience does not stay. `render.py` already encodes what Meta wants, H.264
high profile, yuv420p, a silent AAC track, and `+faststart`.

**Feed video autoplays muted.** Every ad has to read with the sound off, so anything spoken
must also be on screen as type, and the hook has to land in the first two seconds. That is a
constraint on the scene, not a caption you add afterwards.

## Three things that will bite

**Fonts substitute silently.** Chillax, Switzer and Space Grotesk are webfonts. Pango cannot
fetch a webfont, and when a family is missing it does not raise, it picks something else and
the render succeeds. The ad then ships in the wrong typeface with nothing to tell you.
`brand.py` registers the files and asserts the family arrived. See `fonts/README.md` for what
to download.

**No LaTeX on this machine, and MathTex does not degrade.** It raises
`FileNotFoundError: 'latex'`. This is deliberate rather than an oversight. MathTex sets type
in Computer Modern, which looks nothing like Chillax, so a MathTex equation in a Quantica ad
reads as a screenshot from another company. `mathtype.py` builds equations from `Text`
instead and covers everything a prealgebra and algebra ad needs. If one hero equation ever
needs real typesetting, export the app's own KaTeX output as SVG and use `SVGMobject`.

**Set all four frame values, never just two.** `pixel_width` and `pixel_height` alone give a
correctly sized but distorted frame, and every circle comes out an ellipse. `frame_width` and
`frame_height` have to match the same ratio. `scenes/base.py` sets them together so a scene
cannot get it half right.

## Layout

| File | What it is |
|---|---|
| `brand.py` | Colours copied verbatim from the `:root` of `paths/landing.html`, plus font registration that fails loudly |
| `mathtype.py` | LaTeX-free equations as a single `Text`. `math_run()` for expressions, `fraction()`, `power()` |
| `typeset.py` | The Milo scenes' type layer: `AdTheme` (old role names, current palette), per-piece `math_run()`, `caption_block()` with highlighter bands, square `panel()` |
| `voice.py` | `QuanticaVoice`, cache-first ElevenLabs narration. See Voice above |
| `milo_scene.py` | `MiloVoiceoverScene`: vertical format, `say()` beats, pronunciation markers |
| `milo_actor.py` | `MiloActor`: normalised poses, breathing updater, entrances |
| `assets/` | Milo pose PNGs |
| `voiceovers/` | The ElevenLabs narration cache, committed on purpose |
| `scenes/base.py` | `QuanticaScene`. Frame sizing, theme, safe area, captions |
| `scenes/solve_it.py` | Worked example, solving `2x + 3 = 11` step by step |
| `scenes/pythagoras.py` | `PythagorasWithMilo`, the narrated `a² + b² = c²` area proof |
| `scenes/circle_area.py` | `CircleAreaWithMilo`, the narrated `A = πr²` rearrangement proof |
| `scenes/pythagorean_proof.py` | `PythagoreanProofWithMilo`, the older silent cut of the Pythagorean proof |
| `scenes/bayes.py` | `BayesPositive`, a 97% accurate test whose positive result is 3% right. Silent, type-only |
| `render.py` | Render plus the ffmpeg pass that makes the file Meta-safe |
| `fonts/` | Font files: Chillax Semibold and Space Grotesk |
| `out/` | Finished MP4s, gitignored |

## Deployment

`manim/**` is on the `firebase.json` ignore list, so nothing here reaches production. Keep it
that way. Firebase reads the filesystem rather than `.gitignore`, and a gitignored venv was
published to the live CDN for months because of exactly that gap.

## Prior art

The Milo kit and the three proof videos were ported here from `~/manim-projects/milo_manim/`
on 2026-08-20, restyled to Chillax and the current palette with the ElevenLabs narration
preserved through the cache. The old project still exists off-repo but this folder is now
the place to work; the old one encodes the retired navy and orange app tokens and the
`.wmb` set that is now behind `display:none`, so nothing should be copied from it without
rebranding it on the way in.
