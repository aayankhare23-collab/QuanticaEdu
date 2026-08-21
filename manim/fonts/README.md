# Fonts

Pango cannot fetch a webfont, and the site loads all three of these over the network. So
manim needs the actual files here, and `brand.py` registers them at import time.

The failure mode is why this matters. A missing family does not raise. Pango substitutes
another face and the render succeeds, so the ad ships in the wrong typeface with no error
anywhere. `brand.py` asserts each required family is visible after registration rather than
trusting it.

## What is here

| File | Family | Source |
|---|---|---|
| `Chillax-Semibold.otf` | Chillax | Downloaded from Fontshare 2026-08-20. The display and body face of `paths/landing.html`, so the one ads must match. The only weight here on purpose; nothing should request BOLD |
| `SpaceGrotesk.ttf` | Space Grotesk | Copied from `tools/shorts/fonts/`, the only brand font already on this machine |

## What to download

Both are free under the ITF Free Font License, which permits commercial use, and Fontshare
serves desktop files directly.

- **Chillax**, from `fontshare.com/fonts/chillax`. This is the one that actually matters.
  It is both the display and the body face on `paths/landing.html`, which is the page the
  ads land on, so it is what an ad has to match. Save the Semibold as `Chillax-Semibold.otf`.
- **Switzer**, from `fontshare.com/fonts/switzer`. Body type inside the app rather than on
  the marketing page, so ads rarely need it. Save the Medium as `Switzer-Medium.otf`.

The filenames matter. `BRAND_FONTS` in `brand.py` looks for those exact names.

Chillax and Space Grotesk are both here now and the Milo scenes require both, so a missing
file raises at setup. Switzer remains optional; `register_fonts()` only raises for families
listed as required.

Do not reach sideways into `tools/shorts/fonts/`. That directory is not deployed, the
relative path is fragile, and the two pipelines should be able to change independently.
