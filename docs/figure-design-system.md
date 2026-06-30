# Quantica figure design system

How lesson figures (`{t:"fig", x:"<svg>", cap}` blocks) should look. Established when the
4.4 figures were rebuilt; lesson 4.4 is the reference for all three core templates.

## Golden rules
1. **The picture does the talking. Prose goes in `cap`, never inside the SVG.** No paragraphs,
   no sentences as `<text>`. A figure has at most short labels (one or two words).
2. **Two clean bands max.** A hero representation on top, one reinforcing representation below,
   separated by a hairline. Generous whitespace. If it feels busy, cut a band.
3. **Self-contained palette (explicit hex, not CSS vars)** so the pedagogical colors never
   theme-shift. Figures render on a glass-white card, so design on a transparent background.
4. `viewBox` width **560–600**; height to fit. `font-family="Inter"`. Captions may use KaTeX
   `\(...\)`.

## Palette
- Blue primary (labels, arrows, braces): `#2f6fe0`  · deep (result text): `#2257c5` · dot: `#3b82f6` · light fill: `#cfe0fa` / pill `#eaf1ff`
- Gold (the kept / highlighted thing): tile `#fcd76a` stroke `#e0a52a` text `#8a5a08` · dot/point `#f0b429`
- Grey (cancelled / inert): fill `#eef1f6` stroke `#dbe1ea` text+strike `#aab4c2`
- Ink/structure: slate `#475569` · mute `#7c8aa0` · connector `#9fb4d6` · hairline `#e4e9f1` · sparkle `#9fc0f5`

## Shared filters (put in `<defs>`)
```
<filter id="softsh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#1f3a66" flood-opacity="0.16"/></filter>
<filter id="tilesh" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="3.5" flood-color="#5a708f" flood-opacity="0.22"/></filter>
```

## Components
- **Section label:** `font-size 12.5 font-weight 700 letter-spacing 1.4` uppercase, fill `#2f6fe0`.
- **Cancelled tile:** 56×56 rx13, fill `#eef1f6` stroke `#dbe1ea`, digit 26px 700 `#aab4c2`, plus a
  diagonal strike line `#aab4c2` width 2.5 round-cap.
- **Highlight (gold) tile:** 60×60 rx14, fill `#fcd76a` stroke `#e0a52a` w2, `filter=tilesh`, digit 30px 800 `#8a5a08`.
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

## Where the data lives
Each figure is in **two** places that must stay in sync: the inline `chData` in `landing.html`
(what renders) and `lessons/prealgebra/chapter-N.json` (source). See the memory note on inline
lesson data. Edit by brace-matching `var chData=`, JSON.parse, mutate, re-serialize.

## Rollout status (messiest-first)
- Done (11): 4.4 ×3 · 7.3 ×2 (speed triangle, avg speed) · 7.5 area · 9.4 cascade · 6.4 tape ·
  6.2 unwrap · 4.3 strip · 7.4 map scale.
- Remaining: ~97 figures. Next in the ranked-by-cramming list: 6.1 (4x+x=5x), 6.2#0 (balance
  scale), 7.2 (match shared part), 8.3 (largest factor), 6.3 (take same x off both pans), 5.5, 3.2…
