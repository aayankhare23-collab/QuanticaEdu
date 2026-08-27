"""
Quantica short #11  "A 97% accurate test, and a positive result that is 97% wrong"

  prevalence 1 in 1000, sensitivity = specificity = 97%.
  per 100,000 people:
      100 sick     -> 97 true positives
      99,900 well  -> 3% of them wrong = 2,997 false positives
  positives in total = 97 + 2,997 = 3,094, of which 97 are real.
  97 / 3094 = 3.135...%, so about 3 percent, not 97.

The grid is the argument: 3,094 squares, one for every positive result, and only the
first 97 are lime. The picture is the answer, so it is drawn from the same numbers the
assert block checks rather than from a hand-placed sliver.
"""
import os
from PIL import Image, ImageDraw
from qkit import *
from render import grot, LIME, LIME_I, AMBER, AMBER_I, CORAL, CORAL_I

OUT = os.path.dirname(os.path.abspath(__file__)); FR = os.path.join(OUT, "frames11")

# ---- the arithmetic, computed once and then drawn ---------------------------
POP   = 100_000
SICK  = POP // 1000          # 100
TP    = SICK * 97 // 100     # 97
WELL  = POP - SICK           # 99,900
FP    = WELL * 3 // 100      # 2,997
POS   = TP + FP              # 3,094

# ---- grid layout ------------------------------------------------------------
COLS = 56
ROWS = -(-POS // COLS)              # 56
# Sized so the grid AND the two lines under it clear the bottom 500px, which the platform
# paints its own UI over. The first pass ran to y1580 and put the punchline under the caption.
GX, GY, GW = 175, 470, 730
CELL = GW / COLS                    # 13.04
DOT  = 9
GH   = CELL * ROWS                  # 730, so the grid ends at y1200


def grid(d, fill_p, hl, alpha):
    """Draw the positives. fill_p fills them in, hl turns the true 97 lime."""
    if alpha <= 0.003: return
    shown = int(clamp(fill_p) * POS)
    for k in range(shown):
        r, c = divmod(k, COLS)
        x = GX + c*CELL
        y = GY + r*CELL
        real = k < TP
        if real and hl > 0.003:
            col = mix(CORAL, LIME, ease(hl)); ink = mix(CORAL_I, LIME_I, ease(hl))
        elif real:
            col, ink = CORAL, CORAL_I
        else:
            # the false alarms recede once the real ones are called out
            col = mix(CORAL, LINE, ease(hl)*0.72); ink = col
        d.rectangle([x, y, x+DOT, y+DOT], fill=mix(BG, col, alpha),
                    outline=mix(BG, ink, alpha))


def render(t):
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)

    # hook  L0 0.30-3.26, L1 3.68-6.76, L2 7.18-10.84
    if t < 11.6:
        a = 1-ease(seg(t, 11.10, 11.60))
        text(d, (W//2, 700), "A test is", disp(84), INK, alpha=ease(seg(t, 0.35, 0.85))*a)
        text(d, (W//2, 820), "97% accurate.", disp(104), GREEN, alpha=ease(seg(t, 1.15, 1.70))*a)
        text(d, (W//2, 1010), "You test positive.", disp(78), INK, alpha=ease(seg(t, 3.75, 4.25))*a)
        text(d, (W//2, 1110), "Do you have it?", disp(78), INK, alpha=ease(seg(t, 5.05, 5.55))*a)
        # L2 says most people answer 97, so show that guess and then take it away.
        # Without this beat the hook sat motionless from 5.6 to 9.0 and dead_air caught it.
        guess = ease(seg(t, 6.95, 7.45))*(1-ease(seg(t, 8.55, 8.95)))*a
        GUESS = "Most people say 97%"
        text(d, (W//2, 1290), GUESS, ser(56), DIM, alpha=guess)
        if guess > 0.35:
            # struck across the measured width, not a guessed pair of x values
            gw = measure(d, GUESS, ser(56))[0]
            d.line([W//2-gw//2-14, 1290, W//2+gw//2+14, 1290],
                   fill=mix(BG, RED, ease(seg(t, 8.05, 8.50))*a), width=5)
        # the reveal, on L2
        a2 = ease(seg(t, 9.05, 9.60))*a
        text(d, (W//2, 1300), "About 3%.", disp(112), RED, alpha=a2)

    # the setup  L3 11.26-14.64, L4 15.06-17.11
    if 11.5 < t < 21.2:
        a = ease(seg(t, 11.70, 12.15))*(1-ease(seg(t, 20.70, 21.20)))
        text(d, (W//2, 640), "The disease is rare.", ser(62), DIM, alpha=a)
        text(d, (W//2, 780), "1 in 1,000", disp(104), BLUE, alpha=ease(seg(t, 12.80, 13.35))*a)
        text(d, (W//2, 1010), "So take", ser(58), DIM, alpha=ease(seg(t, 15.15, 15.60))*a)
        text(d, (W//2, 1130), f"{POP:,} people", disp(92), INK, alpha=ease(seg(t, 15.75, 16.30))*a)

    # the two sources of a positive  L5 17.53-20.93, L6 21.35-29.51
    if 17.6 < t < 30.4:
        a = 1-ease(seg(t, 29.90, 30.40))
        # sick -> true positives
        a1 = ease(seg(t, 17.95, 18.45))*a
        text(d, (W//2, 620), f"{SICK} have it", grot(54, "Medium"), INK, alpha=a1)
        text(d, (W//2, 730), f"{TP} test positive", disp(80), LIME_I, alpha=ease(seg(t, 19.30, 19.85))*a)
        # well -> false positives
        a2 = ease(seg(t, 21.75, 22.25))*a
        text(d, (W//2, 940), f"{WELL:,} do not", grot(54, "Medium"), INK, alpha=a2)
        text(d, (W//2, 1050), "the test is wrong 3% of the time", ser(50), DIM,
             alpha=ease(seg(t, 23.60, 24.15))*a)
        text(d, (W//2, 1180), f"{FP:,} test positive", disp(80), CORAL_I,
             alpha=ease(seg(t, 26.20, 26.80))*a)
        text(d, (W//2, 1330), "and none of them are sick", ser(50), CORAL_I,
             alpha=ease(seg(t, 27.90, 28.45))*a)

    # the grid of every positive result  L7 29.93-34.64, L8 35.06-39.13
    if 30.2 < t < 40.1:
        a = ease(seg(t, 30.35, 30.80))*(1-ease(seg(t, 39.60, 40.10)))
        text(d, (W//2, 400), f"{POS:,} positive results", disp(76), INK, alpha=a)
        grid(d, seg(t, 30.80, 34.30), seg(t, 35.30, 36.20), a)
        # call out the sliver that is real
        hy = GY + (TP/COLS)*CELL
        ha = ease(seg(t, 35.60, 36.20))*a
        if ha > 0.003:
            d.line([GX-22, GY, GX-22, hy], fill=mix(BG, LIME_I, ha), width=6)
            text(d, (GX-38, (GY+hy)/2), str(TP), disp(52), LIME_I, anchor="rm", alpha=ha)
        text(d, (W//2, GY+GH+68), f"only {TP} are sick", grot(52, "Medium"), LIME_I,
             alpha=ease(seg(t, 36.60, 37.15))*a)
        text(d, (W//2, GY+GH+158), f"{TP} / {POS:,} = 3.1%", disp(72), GREEN,
             alpha=ease(seg(t, 37.70, 38.30))*a)

    # endcard  L9 39.55-44.54
    if t > 40.0:
        text(d, (W//2, 700), "Accuracy is not", ser(58), DIM, alpha=ease(seg(t, 40.30, 40.80)))
        text(d, (W//2, 775), "the whole story.", ser(58), DIM, alpha=ease(seg(t, 40.90, 41.40)))
        text(d, (W//2, 930), "How rare it is", disp(88), INK, alpha=ease(seg(t, 41.90, 42.45)))
        text(d, (W//2, 1040), "matters as much.", disp(88), GREEN, alpha=ease(seg(t, 42.60, 43.15)))
        text(d, (W//2, 1300), "quanticaedu.com", disp(62), GREEN, alpha=ease(seg(t, 44.20, 44.70)))
        text(d, (W//2, 1378), "learn it by solving, free", sans(40), DIM, alpha=ease(seg(t, 44.75, 45.25)))
    brand(img, d); return img


DUR = 46.9

if __name__ == "__main__":
    import sys
    from fractions import Fraction as F
    # the picture and the punchline must come from the same arithmetic
    post = F(1, 1000)*F(97, 100) / (F(1, 1000)*F(97, 100) + F(999, 1000)*F(3, 100))
    assert post == F(97, 3094), post
    assert (SICK, TP, WELL, FP, POS) == (100, 97, 99_900, 2_997, 3_094)
    assert TP + FP == POS and F(TP, POS) == post
    assert round(float(post)*100, 1) == 3.1
    assert ROWS*COLS >= POS and (ROWS-1)*COLS < POS      # grid holds every positive, no spare row
    assert GY + GH + 158 + 40 < 1420                      # grid AND both labels clear the UI band
    assert GX - 38 - 60 > 0                               # the 97 callout stays on canvas
    print(f"  check: {SICK} sick -> {TP} true, {WELL:,} well -> {FP:,} false, "
          f"{TP}/{POS:,} = {float(post)*100:.2f}%")
    if "--check" in sys.argv:
        w, bad = dead_air(render, DUR); print(f"  {DUR}s | worst {w}s | over-2.5s: {bad or 'none'}")
    else:
        render_all(render, DUR, os.path.join(OUT, "quantica-11-bayes.mp4"), FR)
