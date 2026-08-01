"""
Quantica short #1  "25% off twice is not 50% off"
Renders 1080x1920 @ 30fps as a PNG sequence, then encodes with ffmpeg.

Every number on screen is exact:
  $80 tag, 16 squares at $5 each
  cut 1  = 4 squares = $20   ->  $60
  cut 2  = 3 squares = $15   ->  $45
  half   = 8 squares = $40, so $45 sits exactly one square above it
  0.75 * 0.75 = 0.5625, so 43.75% off
"""
import os, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from qkit import brand

W, H, FPS = 1080, 1920, 30
OUT = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(OUT, "frames")

# ---- palette, taken from tools/figure_kit.py + the site tokens
BG      = (252, 254, 251)
INK     = (22, 40, 27)
DIM     = (100, 116, 139)
GREEN   = (21, 128, 61)
GREEN_M = (22, 163, 74)
GREEN_S = (220, 252, 231)
BLUE    = (29, 78, 216)
BLUE_M  = (47, 111, 224)
BLUE_S  = (219, 232, 253)
GOLD_I  = (138, 90, 8)
GOLD_M  = (217, 165, 33)
GOLD_S  = (253, 230, 138)
GOLD_L  = (240, 193, 75)
RED     = (180, 54, 42)
LINE    = (219, 225, 234)

F_GROT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts/SpaceGrotesk.ttf")
_gcache = {}
def grot(size, weight="Bold"):
    """Space Grotesk, the landing page's own display face."""
    k = (size, weight)
    if k not in _gcache:
        f = ImageFont.truetype(F_GROT, size)
        try: f.set_variation_by_name(weight)
        except Exception: pass
        _gcache[k] = f
    return _gcache[k]

# ---- colours lifted straight off the landing page, so the video matches the product
LIME    = (190, 255, 139)   # #beff8b, the signature accent
LIME_I  = (21, 128, 61)     # readable ink on lime
AMBER   = (255, 200, 77)    # #ffc84d
AMBER_I = (138, 90, 8)
CORAL   = (255, 122, 92)    # #ff7a5c
CORAL_I = (168, 62, 40)

F_DISP = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
F_SER  = "/System/Library/Fonts/Supplemental/Georgia.ttf"
F_SANS = "/System/Library/Fonts/HelveticaNeue.ttc"
_cache = {}
def font(path, size, index=0):
    k = (path, size, index)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(path, size, index=index)
    return _cache[k]
def disp(s): return font(F_DISP, s)
def ser(s):  return font(F_SER, s)
def sans(s): return font(F_SANS, s)

# ---- easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x):                      # smootherstep
    x = clamp(x); return x*x*x*(x*(x*6-15)+10)
def ease_out(x):
    x = clamp(x); return 1-(1-x)**3
def seg(t, a, b):                 # local 0..1 progress over [a,b]
    return 0.0 if b <= a else clamp((t-a)/(b-a))

def mix(c1, c2, f):
    f = clamp(f); return tuple(int(round(c1[i]+(c2[i]-c1[i])*f)) for i in range(3))

# ---- text helpers
def text(d, xy, s, f, fill, anchor="mm", alpha=1.0, spacing=12):
    if alpha <= 0.003: return
    col = mix(BG, fill, alpha)
    d.multiline_text(xy, s, font=f, fill=col, anchor=anchor, align="center", spacing=spacing)

def measure(d, s, f):
    bb = d.textbbox((0, 0), s, font=f)
    return bb[2]-bb[0], bb[3]-bb[1]

# ---- the bar
BAR_X, BAR_W = 110, 860           # 16 squares
BAR_Y, BAR_H = 980, 190
N = 16
SQ = BAR_W / N
def sq_x(i): return BAR_X + SQ*i   # left edge of square i (0-indexed)

def bar_shadow(img):
    """Soft coloured drop shadow under the bar, the way the landing page cards sit."""
    pad = 70
    box = (BAR_X-pad, BAR_Y-pad//2, BAR_X+BAR_W+pad, BAR_Y+BAR_H+pad)
    lay = Image.new("L", (box[2]-box[0], box[3]-box[1]), 0)
    ImageDraw.Draw(lay).rounded_rectangle(
        [pad, pad//2+16, pad+BAR_W, pad//2+BAR_H+16], 14, fill=110)
    lay = lay.filter(ImageFilter.GaussianBlur(22))
    tint = Image.new("RGB", lay.size, (120, 150, 128))
    img.paste(tint, (box[0], box[1]), lay)


def glow_ring(d, x0, x1, p, col):
    """Expanding fading outline when a block lands. Mirrors keyCardGlow on the site."""
    if p <= 0 or p >= 1: return
    grow = 26*ease_out(p)
    a = (1-p)*0.75
    d.rounded_rectangle([x0-grow, BAR_Y-grow, x1+grow, BAR_Y+BAR_H+grow],
                        int(12+grow), outline=mix(BG, col, a), width=max(2, int(5*(1-p))))


def draw_bar(img, d, filled_blue=0.0, filled_gold=0.0, alpha=1.0,
             grid_p=1.0, half_line=0.0, hl_square=None, t=0.0):
    """filled_blue / filled_gold are counts of squares (fractional while the wipe runs)."""
    if alpha <= 0.003: return
    if alpha > 0.35:
        bar_shadow(img)
        d = ImageDraw.Draw(img)
    outline = mix(BG, INK, alpha)
    d.rounded_rectangle([BAR_X, BAR_Y, BAR_X+BAR_W, BAR_Y+BAR_H], 12,
                        fill=mix(BG, (255, 255, 255), alpha), outline=outline, width=5)
    # cut 1, lime. the landing page's signature accent.
    w = SQ*min(filled_blue, 4)
    if w > 6:
        x1 = BAR_X+BAR_W
        d.rounded_rectangle([x1-w+3, BAR_Y+4, x1-4, BAR_Y+BAR_H-4], 8, fill=mix(BG, LIME, alpha))
    # cut 2, amber, sitting immediately left of it
    w2 = SQ*min(filled_gold, 3)
    if w2 > 6:
        x1 = BAR_X+BAR_W-SQ*4
        d.rounded_rectangle([x1-w2+3, BAR_Y+4, x1-4, BAR_Y+BAR_H-4], 8, fill=mix(BG, AMBER, alpha))
    # the one square above half
    if hl_square is not None:
        i, a2 = hl_square
        if a2 > 0.003:
            d.rounded_rectangle([sq_x(i)+4, BAR_Y+4, sq_x(i+1)-4, BAR_Y+BAR_H-4], 6,
                                fill=mix(BG, CORAL, alpha*a2))
    # grid, drawn left to right so the bar keeps moving while it is explained
    if grid_p > 0.001:
        shown = grid_p*(N-1)
        for i in range(1, N):
            f = clamp(shown-(i-1))
            if f <= 0.01: break
            x = sq_x(i)
            d.line([x, BAR_Y+7, x, BAR_Y+7+(BAR_H-14)*ease_out(f)],
                   fill=mix(BG, LINE, alpha*0.85), width=2)
    d.rounded_rectangle([BAR_X, BAR_Y, BAR_X+BAR_W, BAR_Y+BAR_H], 12, outline=outline, width=5)
    # half marker
    if half_line > 0.003:
        x = sq_x(8)
        top, bot = BAR_Y-34, BAR_Y+BAR_H+34
        yy = top+(bot-top)*ease(half_line)
        col = mix(BG, CORAL_I, half_line)
        y = top
        while y < yy:
            d.line([x, y, x, min(y+14, yy)], fill=col, width=5)
            y += 26
    # each block flashes a ring as it lands
    glow_ring(d, sq_x(12), sq_x(16), seg(t, 14.5, 15.3), LIME_I)
    glow_ring(d, sq_x(9), sq_x(12), seg(t, 18.5, 19.3), AMBER_I)


def render(t):
    """t = seconds. Visual beats are pinned to the narration schedule in lines.py, which was
    written to sound natural and then measured. The pictures move to fit the speech."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ============================================ 1. hook   L0 spans 0.30 - 3.41
    if t < 3.95:
        a = ease(seg(t, 0.0, 0.35)) * (1-ease(seg(t, 3.55, 3.95)))
        hf = disp(112)
        rows = [("", "25% off", 700, 0.0), ("+", "25% off", 850, 0.45), ("=", "50% off", 1000, 0.9)]
        bw = measure(d, "25% off", hf)[0]
        ow = max(measure(d, o, hf)[0] for o, _, _, _ in rows if o)
        gapw = 34
        block = ow+gapw+bw
        body_x = W//2-block//2+ow+gapw
        for op, body, y, t0 in rows:
            aa = (a if t0 == 0 else ease(seg(t, t0, t0+0.35))*a)
            yy = y+(1-ease(seg(t, t0, t0+0.5)))*30
            text(d, (body_x, yy), body, hf, INK, anchor="lm", alpha=aa)
            if op:
                text(d, (body_x-gapw, yy), op, hf, INK, anchor="rm", alpha=aa)
        p = ease_out(seg(t, 1.7, 2.25))
        if p > 0:
            x0, x1 = W//2-block//2-18, body_x+bw+18
            d.line([x0, 1000, x0+(x1-x0)*p, 1000], fill=mix(BG, RED, a), width=11)
        text(d, (W//2, 1190), "the second 25% is smaller\nthan the first", grot(50, "Medium"), RED,
             alpha=ease(seg(t, 2.5, 2.95))*a, spacing=16)

    # ============================================ 2. the sentence   L1 spans 3.83 - 6.76
    if 3.7 < t < 7.15:
        a = ease(seg(t, 3.80, 4.25)) * (1-ease(seg(t, 6.70, 7.10)))
        rise = (1-ease(seg(t, 3.80, 4.50)))*26
        text(d, (W//2, 880+rise), "The coupon comes off\nthe sale price,", disp(92), INK,
             alpha=a, spacing=26)
        text(d, (W//2, 1140), "not the tag.", disp(92), GREEN,
             alpha=ease(seg(t, 5.10, 5.55))*a)

    # ============================================ 3. the bar   L2 - L8
    BAR_END, BAR_FADE = 34.60, 35.15
    if t > 7.0 and t < BAR_FADE+0.2:
        bar_a = ease(seg(t, 7.10, 7.70))*(1-ease(seg(t, BAR_END, BAR_FADE)))

        blue = 4*ease(seg(t, 10.80, 11.90))        # L3 "the sale takes a quarter off"
        gold = 3*ease(seg(t, 14.20, 15.30))        # L4 "the coupon takes a quarter of sixty"
        halfl = seg(t, 21.90, 22.70)               # L6 "one square past half"
        hl = (8, ease(seg(t, 23.00, 23.50))*(1-ease(seg(t, BAR_END, BAR_FADE)))) if t > 22.9 else None

        draw_bar(img, d, blue, gold, bar_a, grid_p=seg(t, 8.80, 10.40),
                 half_line=halfl, hl_square=hl, t=t)

        # the tag, under L2 "an eighty dollar sweater, sixteen squares, five dollars each"
        gone = 1-ease(seg(t, 10.50, 11.00))
        text(d, (W//2, 880), "$80", disp(96), INK, alpha=ease(seg(t, 7.60, 8.10))*gone*bar_a)
        text(d, (W//2, 1268), "16 squares, $5 each", sans(46), DIM,
             alpha=ease(seg(t, 8.40, 8.90))*gone*bar_a)

        # cut 1, under L3
        cuts_gone = 1-ease(seg(t, 22.00, 22.50))
        text(d, ((sq_x(12)+sq_x(16))/2, 900), "-$20", disp(68), LIME_I,
             alpha=ease(seg(t, 11.60, 12.10))*cuts_gone*bar_a)
        text(d, (W//2, 1268), "$60 left", disp(64), INK,
             alpha=ease(seg(t, 12.30, 12.80))*(1-ease(seg(t, 14.00, 14.50)))*bar_a)

        # cut 2, under L4, then the answer under L5
        text(d, ((sq_x(9)+sq_x(12))/2, 900), "-$15", disp(68), AMBER_I,
             alpha=ease(seg(t, 15.00, 15.50))*cuts_gone*bar_a)
        text(d, (W//2, 1268), "a quarter of 60, not of 80", grot(46, "Medium"), AMBER_I,
             alpha=ease(seg(t, 16.30, 16.80))*(1-ease(seg(t, 18.10, 18.55)))*bar_a)
        text(d, (W//2, 1268), "you pay $45", disp(64), GREEN,
             alpha=ease(seg(t, 18.30, 18.80))*cuts_gone*bar_a)
        text(d, (W//2, 1380), "same 25%, smaller chunk", grot(48, "Medium"), RED,
             alpha=ease(seg(t, 19.60, 20.10))*(1-ease(seg(t, 21.50, 21.95)))*bar_a)

        # the half marker, under L6
        half_gone = 1-ease(seg(t, 30.50, 31.00))
        text(d, (sq_x(8), 1268), "half is $40", grot(46, "Medium"), CORAL_I,
             alpha=ease(seg(t, 22.90, 23.40))*half_gone*bar_a)
        text(d, (sq_x(8.4), 900), "$5 above it", disp(52), CORAL_I,
             alpha=ease(seg(t, 23.50, 24.00))*half_gone*bar_a)

    # ============================================ 4. the real number   L7 - L9
    if 24.5 < t < BAR_FADE+0.2:
        fade = 1-ease(seg(t, BAR_END, BAR_FADE))
        # L7 is "you paid seventy five percent, of seventy five percent", so the
        # product lands in two halves, matching where the comma falls in the line.
        mf = disp(74)
        lhs, rhs = "0.75 x 0.75", " = 0.5625"
        lw, rw = measure(d, lhs, mf)[0], measure(d, rhs, mf)[0]
        lx = W//2-(lw+rw)//2
        text(d, (lx+lw//2, 600), lhs, mf, INK, alpha=ease(seg(t, 24.70, 25.20))*fade)
        text(d, (lx+lw+rw//2, 600), rhs, mf, GREEN, alpha=ease(seg(t, 26.60, 27.10))*fade)
        text(d, (W//2, 720), "43.75% off", disp(92), GREEN,
             alpha=ease(seg(t, 28.50, 29.00))*fade)                    # L8
        # the chain, under L9 "keep stacking coupons, and the price never hits zero"
        toks = [("$80", 32.2, INK), ("->", 32.6, DIM), ("$60", 32.8, INK),
                ("->", 33.2, DIM), ("$45", 33.4, GREEN), ("->", 33.8, DIM),
                ("$33.75", 34.0, INK), ("...", 34.4, DIM)]
        fs = sans(44)
        widths = [measure(d, s, fs)[0] for s, _, _ in toks]
        gap = 20
        x = W//2-(sum(widths)+gap*(len(toks)-1))//2
        for (s, t0, col), wd in zip(toks, widths):
            text(d, (x+wd//2, 480), s, fs, col, alpha=ease(seg(t, t0, t0+0.32))*fade)
            x += wd+gap

    # ============================================ 5. endcard
    if t > 35.2:
        text(d, (W//2, 830), "It never hits zero.", disp(88), INK,
             alpha=ease(seg(t, 35.40, 35.90)))
        text(d, (W//2, 960), "You keep three quarters\nof a positive number.", ser(60), DIM,
             alpha=ease(seg(t, 36.30, 36.80)), spacing=18)
        text(d, (W//2, 1180), "quanticaedu.com", disp(66), GREEN,
             alpha=ease(seg(t, 37.30, 37.80)))
        text(d, (W//2, 1265), "prealgebra 9.4, free", sans(42), DIM,
             alpha=ease(seg(t, 37.90, 38.40)))
    brand(img, d)
    return img


DUR = 39.6
def main():
    os.makedirs(FR, exist_ok=True)
    for f in os.listdir(FR):
        os.remove(os.path.join(FR, f))
    n = int(DUR*FPS)
    for i in range(n):
        render(i/FPS).save(os.path.join(FR, f"f{i:05d}.png"))
        if i % 150 == 0:
            print(f"  {i}/{n}", flush=True)
    print(f"  {n}/{n} frames")
    mp4 = os.path.join(OUT, "quantica-01-percent.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(FPS), "-i", os.path.join(FR, "f%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        "-movflags", "+faststart", mp4], check=True)
    print("wrote", mp4)

if __name__ == "__main__":
    main()
