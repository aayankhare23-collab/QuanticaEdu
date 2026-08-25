# Quantica figure design system

How lesson figures (`{t:"fig", x:"<svg>", cap}` blocks) should look.

## Read this before the rest of the file (2026-08-25)

**The palette and component sections below are the RETIRED brand.** The site was rebranded and
this document was not, so following it verbatim produces an off-brand figure. On 2026-08-25 the
user said: "Educational figures should be clean manim styled figures and/or animations similar to
on the landing page or in the manim folder. Do NOT use the previous images as references."

That rules out every figure in `tools/lesson-figs/` (chapter 7, and 8.1 to 8.3) and the
`BLUE`/`GOLD` constants in `tools/manim_figs.py` as visual references. The module is still the
right tool for geometry and SVG emission. Only its colours and `pill()` are stale.

**What current is.** Three sources, all live:

- **The app**, `landing.html`, themes per course. Its active `:root` remaps every token to greens
  and `:root[data-course="algebra1"]` remaps to ocean blue: `--ink:#132F49`, `--slate:#42607A`,
  `--navy:#1C5486`, `--blue:#2E7CC0`, `--sky:#4D9EDD`, `--line:rgba(28,84,134,.15)`, page
  background `#E7F2FC`. A figure sits on `.lessonfig`, which is now a **glass** card,
  `rgba(255,255,255,.6)` over a backdrop blur, not the plain white card assumed below.
- **The marketing hero** in `paths/landing.html` is the visual language to match: near-black
  outlines (`#0a0a0a`, stroke-width 2 to 2.5), flat unmodulated fills from its accent set
  (`#7cc7ff` sky, `#beff8b` lime, `#ffc84d` amber, `#c9b8ff` lavender, `#9fe8d8` mint,
  `#ff7a5c` coral), Space Grotesk 700 labels, CSS animation with a `prefers-reduced-motion`
  fallback.
- **`manim/brand.py`** carries the rule the old kit breaks. **Quantica has square corners.**
  `--radius` and `--radius-lg` are 0 on every surface, so `RoundedRectangle`, `Fig.pill()` and any
  `rx` above 0 are off brand. Use `Rectangle`.

**The reference figure is now `tools/lesson-figs/fig_8_4.py`**, the first built in this language.
Preview any figure on the surface it actually ships on with
`http://localhost:8743/tools/lesson-figs/_preview.html?f=fig_8_4&c=algebra1`, which renders the
glass card and the course background. Pass `c=prealgebra` for the green theme.

**Animation is optional.** Animate when the motion teaches. 8.4 ships static on purpose, because
it is a side-by-side comparison and every panel has to be on screen at once; a staggered reveal
left half the argument blank for part of each loop, and it painted each region before its own
boundary, which is backwards from how a region is found.

Everything below still holds except the Palette and Components sections: the two-band structure,
prose in `cap` only, the 560 to 600 viewBox, the 700 weight cap, no all-caps labels, and the whole
manim section.

## Golden rules
1. **The picture does the talking. Prose goes in `cap`, never inside the SVG.** No paragraphs,
   no sentences as `<text>`. A figure has at most short labels (one or two words).
2. **Two clean bands max.** A hero representation on top, one reinforcing representation below,
   separated by a hairline. Generous whitespace. If it feels busy, cut a band.
3. **Self-contained palette (explicit hex, not CSS vars)** so the pedagogical colors never
   theme-shift. Figures render on a glass-white card, so design on a transparent background.
4. `viewBox` width **560–600**; height to fit. `font-family="Space Grotesk, sans-serif"`. That is
   still right, but not for the reason this line used to give. The app shell is no longer Space
   Grotesk throughout; it is Chillax for display and Switzer for body, with Space Grotesk as the
   mono face. Figures keep Space Grotesk because it is the technical face AND because
   `.modal svg text` in landing.html forces the family on every figure label as a presentation
   attribute cannot outrank a CSS rule. Setting anything else in the SVG is silently overridden.
   Inter is legacy, never use it. **Max `font-weight` is 700.** Space Grotesk ships no 800; browsers fake-bold
   the 700 face and the smeared result reads as a generic sans (user-flagged). A CSS safety net in
   landing.html (`.modal svg text`) forces the family, but the weight cap is on you. Captions may
   use KaTeX `\(...\)`.

## Palette (RETIRED, kept only to read the existing chapter 7 and 8.1-8.3 figures)
- Blue primary (labels, arrows, braces): `#2f6fe0`  · deep (result text): `#2257c5` · dot: `#3b82f6` · light fill: `#cfe0fa` / pill `#eaf1ff`
- Gold (the kept / highlighted thing): tile `#fcd76a` stroke `#e0a52a` text `#8a5a08` · dot/point `#f0b429`
- Grey (cancelled / inert): fill `#eef1f6` stroke `#dbe1ea` text+strike `#aab4c2`
- Ink/structure: slate `#475569` · mute `#7c8aa0` · connector `#9fb4d6` · hairline `#e4e9f1` · sparkle `#9fc0f5`

## Shared filters (put in `<defs>`)
```
<filter id="softsh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#1f3a66" flood-opacity="0.16"/></filter>
<filter id="tilesh" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#5a708f" flood-opacity="0.22"/></filter>
```

## Components (RETIRED shapes: rounded tiles and pills break the square-corner rule)
- **Band label:** one lowercase word (`before`, `after`), `font-size 13 font-weight 700`, no
  letter-spacing, fill `#2f6fe0`. **Never all-caps and never letter-spaced.** Small all-caps
  eyebrow/kicker/band labels are banned product-wide (memory `no-allcaps-label-boxes`); this line
  used to prescribe them, which contradicted the ban. Algebra I 5.3 and 5.4 are the reference.
- **Cancelled tile:** 56×56 rx13, fill `#eef1f6` stroke `#dbe1ea`, digit 26px 700 `#aab4c2`, plus a
  diagonal strike line `#aab4c2` width 2.5 round-cap.
- **Highlight (gold) tile:** 60×60 rx14, fill `#fcd76a` stroke `#e0a52a` w2, `filter=tilesh`, digit 30px 700 `#8a5a08`.
- **Result card:** white rect rx18 stroke `#dbe6fa`, `filter=softsh`, with two small 2-stroke
  `#9fc0f5` sparkles hugging opposite corners. Fraction in `#2257c5`.
- **Dotted connector:** stroke `#9fb4d6` width 1.6 `stroke-dasharray="2 4"` round-cap.
- **Arrow:** line + chevron path, `#2f6fe0` width 2.5 round cap/join.
- **Dot (array):** r 7.5, column step ~34. Blue `#3b82f6`; the kept group gold `#f0b429`.
- **Bar model:** rounded bar rx9 white stroke `#cbd7ea`; shade `#cfe0fa` (clip to bar); thin unit
  ticks `#e6edf8`; thicker group ticks `#8fb3e8` w2; a `×n` pill (`#eaf1ff`/`#cdddf7`, blue text).
- **Number line:** baseline `#9aa6b6` w2.5 round; ticks `#9aa6b6`; the marked point gold dot
  `#fcd76a`/`#e0a52a` with a gold tick; tiny endpoint labels `#475569`.

## Three reference templates (see lesson 4.4 in chData)
1. **factor-tiles** — cancel shared prime tiles, brace survivors to a result card (4.4 fig 0).
2. **bar-model** — fractions as shaded bars re-sliced to a common denominator (4.4 fig 1).
3. **number-line** — one point wearing several equivalent names via a callout (4.4 fig 2).

## Graphs are rendered with manim

Anything on a set of axes (a plane, a line, a slope triangle, a pair of lines) is **drawn with
manim, not hand-written as SVG**. Hand-placing bezier points for a graph is slow and the results
drift; manim owns the geometry and the output is still a real vector SVG in the house palette.

`tools/manim_figs.py` is the kit. Manim CE only writes raster stills, so the module points
manim's own cairo renderer at a `cairo.SVGSurface`. Every mobject is already a bezier `VMobject`,
so what comes out is true vector SVG, not a traced bitmap.

Two things it does deliberately, both of which will bite anyone who reimplements this:

- **Manim draws geometry only. Labels are emitted as live `<text>`** in Space Grotesk via
  `Fig.label(...)`. Manim's own `Text` bakes glyphs to paths using whatever font the machine has,
  and Space Grotesk is not installed here, so the labels would silently render in a fallback face.
  Live text also stays selectable, stays sharp, and satisfies `check_lesson.py`'s font check
  honestly.
- **Colours are un-swapped.** Manim reverses RGB on purpose (`rgbas[0][2::-1]`) because a cairo
  ARGB32 *image* surface is byte-reversed. An SVG surface is not. Undo the swap or every figure
  ships with its red and blue channels flipped.

Setup, once per machine. Manim needs its own venv; it installs clean on Python 3.14 (manim 0.20.1,
pycairo and manimpango both have cp314 wheels, no LaTeX and no system pango needed because we
never use `MathTex` or manim `Text`):

```bash
python3 -m venv .venv-manim && .venv-manim/bin/pip install manim
```

Writing and applying one:

```bash
.venv-manim/bin/python tools/lesson-figs/fig_7_3.py            # renders fig_7_3.svg beside it
open http://localhost:8743/tools/lesson-figs/_preview.html?f=fig_7_3,fig_7_6   # eyeball it
python3 tools/lesson-figs/apply_fig.py 7.3 --course algebra1 --write
python3 tools/build_lessons.py
```

`apply_fig.py` finds the lesson's single fig block, swaps `x`, keeps `cap` unless you pass one,
preserves the file's own indent and unicode-escaping style, and warns if the figure prints two or
more numbers at or above 12 that a problem in the same lesson also prints (which would pre-solve
it). **A figure must still be eyeballed in the preview.** Blind generation is unreliable and the
checker cannot see a label sitting on top of an axis.

### Animation

Figures animate. Three primitives, all of which keep manim as the thing that decides
the geometry and every keyframe:

- **`Fig.motion(mobjects, keys, about=...)`** for anything that is a similarity
  transform (travel, growth, rotation). The geometry is emitted ONCE and carried by
  an SVG `<animateTransform>` whose `values` are the positions manim computed. The
  browser interpolates between them at its own refresh rate.
- **`Fig.draw(mobjects, span=...)`** for a stroke that appears progressively. Uses
  `pathLength="1"` so one dash pattern and one `stroke-dashoffset` animation reveal
  any path regardless of its real length.
- **`Fig.frames(builder, n=...)`** is the fallback flipbook, one manim-rendered frame
  per `<g>` with a CSS keyframe showing one at a time. Use it only when the motion is
  NOT a similarity transform and cannot be drawn on.

**Why the flipbook is the fallback and not the default.** Measured on 7.3: about
2.4KB per frame, so 34 frames is 84KB at ~4.5 fps and 30 fps for 7 seconds would be
half a megabyte for one figure. That reads as a slideshow. The same animation via
`motion` is **10KB and smooth at the browser's refresh rate**, an eight-fold size cut
and a large quality gain at once.

Three traps, all of which shipped silently before being caught:

- A negative `animation-delay` of `-i/n` runs a flipbook BACKWARDS. Frame `i` only
  lands in slot `i` at `-(n-i)/n`.
- SVG `scale()` is about the origin, so a growing object flies off unless the content
  is counter-translated and the scale happens in a frame centred on its anchor. That
  is what `about=` does.
- **Text inside a scaled group scales with it.** On 7.3 the leg labels went from 17px
  to 37px on the way across. Labels ride their own translate-only track via
  `label_keys`.

The preview tab does not paint continuously, so an animation's clock reads 0 and
looks frozen. Drive it by hand to check: `svg.setCurrentTime(4.0)` for SMIL, or
`document.getAnimations().forEach(a => {a.pause(); a.currentTime = 4000})` for CSS.

Chapter 7's six figures are built and rendered in `tools/lesson-figs/` (`fig_7_1` the plane and
its quadrants, `fig_7_2` a line as the points satisfying its equation, `fig_7_3` two slope
triangles on one line, `fig_7_4` one point plus one slope pinning a line, `fig_7_5` the two
intercepts, `fig_7_6` the three solution counts of a system side by side, which is the picture
5.1 promised the reader). `fig_7_2` is a spare; 7.2 shipped with a hand-authored figure that also
shows the substitution check, so re-point the script before applying that one.

## Where the data lives
Each figure is in **two** places that must stay in sync: the inline `chData` in `landing.html`
(what renders) and `lessons/prealgebra/chapter-N.json` (source). See the memory note on inline
lesson data. Edit by brace-matching `var chData=`, JSON.parse, mutate, re-serialize.

## Rollout status (messiest-first)
- Done (17): 4.4 ×3 · 7.3 ×2 · 7.5 area · 9.4 cascade · 6.4 tape · 6.2 unwrap+balance ·
  4.3 strip · 7.4 map scale · 6.1 tiles · 6.3 balance · 7.2 ratio-link · 8.3 sqrt routes · 5.5 decimals.
- Remaining: ~91 figures. Next in the ranked-by-cramming list: 3.2 (powers of ten = nines+1),
  5.3 (climb to a power of ten), 4.6 (recut over twelfths), 3.6 (divisors of 72), 6.5 (compound
  inequality gates), 10.3 (counting pairs a²+b<13)…
