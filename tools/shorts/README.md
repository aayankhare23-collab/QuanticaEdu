# Shorts factory

Renders vertical 1080x1920 math videos as PNG frame sequences, encodes them with ffmpeg, and
lays a narration track on top. Ten videos were built this way on 2026-07-30. No camera, no
hand on screen, no editor.

`half-plus-quarter.html` is an earlier, unrelated HTML experiment. Everything else is the
Python pipeline.

## Files

| file | what it is |
|------|------------|
| `qkit.py` | shared kit: palette, fonts, easing, `text()`, `render_all()`, `dead_air()`, `brand()` |
| `lines.py` | the spoken script for every video, one list per video, keyed `v1`..`v10` |
| `tts.py` | pluggable speech. ElevenLabs if `ELEVENLABS_API_KEY` is set, OpenAI if `OPENAI_API_KEY`, else macOS `say` |
| `mux.py` | lays the narration onto a rendered mp4 and writes a timecoded voiceover script |
| `render.py` … `render10.py` | one file per video, each a pure `render(t) -> PIL.Image` |
| `fonts/SpaceGrotesk.ttf` | the display face, SIL OFL, from Google Fonts |

## The one rule that matters

**Write the words first, measure them, then move the pictures to fit.** Never trim a spoken
line so it fits a visual you already timed. That was the original mistake: commas were stripped
from "One, two, four, eight, sixteen" purely to save time, and TTS reads a comma as a breath, so
removing them is a direct instruction to gabble. Every video was retimed to fix it.

The measured narration schedule lives in `measured/durations.json` (regenerated on demand). Each
`renderN.py` carries the schedule in comments, e.g. `# L3 10.71-13.68`, so the visual beats can
be read against the speech.

## Making a video

```bash
export ELEVENLABS_API_KEY=sk_...          # optional; falls back to a robotic local voice
cd tools/shorts

python3 renderN.py --check                # timing + math asserts, renders nothing
python3 renderN.py                        # writes quantica-NN-name.mp4 (silent)
python3 mux.py vN                         # adds narration -> ...-voiced.mp4
```

`--check` runs `dead_air()`, which hashes every frame and reports the longest stretch where
nothing moves. **Keep it under 2.5s.** People swipe on static frames, and the check is the only
thing that catches it reliably.

Each `renderN.py` also asserts its own arithmetic at import, so a wrong number fails loudly
before a single frame is drawn.

## Rules learned the hard way

- **Screenshot before you trust a measurement.** `getComputedStyle().marginLeft` returned `0px`
  in the automation browser regardless of the real layout, and a whole diagnosis was built on
  that before a screenshot showed the truth in one look.
- **Check text fits.** Use the `fit()` helper (see `render2.py`) or `measure()`. Several strings
  overflowed 1080px on the first pass.
- **Compute layout, do not nudge it.** The pizza row was centred by solving for the group widths
  and gaps, then verified by scanning the rendered pixels for ink columns.
- **`∝` renders as tofu** in every font here despite `getmask()` claiming otherwise. Use words.
- **Safe zones**: keep anything that matters out of the top 200px and bottom 500px. Platforms
  paint their own UI there.
- **Brand mark**: `brand()` puts Milo plus quanticaedu.com top-left in every frame. A full-size
  URL in the opening frame reads as an ad and costs retention; this does the job quietly.
- The spoken call to action was **removed** on request. The domain stays on screen throughout
  and on the endcard.

## The ten built

1 percent off twice · 2 pizza · 3 circle regions · 4 average speed · 5 `0.999... = 1` ·
6 PEMDAS · 7 `(2x)³` · 8 no square ends in 7 · 9 down 20 up 20 · 10 pay cut vs raise

Every number in every video was verified in exact `Fraction` or `sympy` arithmetic first.
`render3.py` goes further and flood-fills its own rendered figure to count the regions, so the
picture proves its own number rather than trusting the formula.
