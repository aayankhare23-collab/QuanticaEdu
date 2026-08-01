"""Shared render helpers for the Quantica shorts. 1080x1920 @ 30fps."""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30

# palette from tools/figure_kit.py + the site tokens
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
RED     = (180, 54, 42)
LINE    = (219, 225, 234)

F_DISP = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
F_SER  = "/System/Library/Fonts/Supplemental/Georgia.ttf"
F_SANS = "/System/Library/Fonts/HelveticaNeue.ttc"
_c = {}
def font(p, s, i=0):
    k = (p, s, i)
    if k not in _c:
        _c[k] = ImageFont.truetype(p, s, index=i)
    return _c[k]
def disp(s): return font(F_DISP, s)
def ser(s):  return font(F_SER, s)
def sans(s): return font(F_SANS, s)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x):
    x = clamp(x); return x*x*x*(x*(x*6-15)+10)
def ease_out(x):
    x = clamp(x); return 1-(1-x)**3
def seg(t, a, b):
    return 0.0 if b <= a else clamp((t-a)/(b-a))
def mix(c1, c2, f):
    f = clamp(f); return tuple(int(round(c1[i]+(c2[i]-c1[i])*f)) for i in range(3))

def text(d, xy, s, f, fill, anchor="mm", alpha=1.0, spacing=14):
    if alpha <= 0.003: return
    d.multiline_text(xy, s, font=f, fill=mix(BG, fill, alpha),
                     anchor=anchor, align="center", spacing=spacing)

def measure(d, s, f):
    bb = d.textbbox((0, 0), s, font=f)
    return bb[2]-bb[0], bb[3]-bb[1]

def encode(frame_dir, out_mp4, fps=FPS):
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(fps), "-i", os.path.join(frame_dir, "f%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
        "-movflags", "+faststart", out_mp4], check=True)

def render_all(render_fn, dur, out_mp4, frame_dir):
    os.makedirs(frame_dir, exist_ok=True)
    for f in os.listdir(frame_dir):
        os.remove(os.path.join(frame_dir, f))
    n = int(dur*FPS)
    for i in range(n):
        render_fn(i/FPS).save(os.path.join(frame_dir, f"f{i:05d}.png"))
        if i % 200 == 0:
            print(f"  {i}/{n}", flush=True)
    encode(frame_dir, out_mp4)
    print("  wrote", out_mp4)

def dead_air(render_fn, dur, thresh=2.5):
    """Return (worst_static_seconds, [(start, length) over thresh])."""
    import hashlib
    prev = None; run = 0; runs = []
    n = int(dur*FPS)
    for i in range(n):
        h = hashlib.md5(render_fn(i/FPS).resize((216, 384)).tobytes()).hexdigest()
        if h == prev: run += 1
        else:
            if run: runs.append((round((i-run)/FPS, 1), round(run/FPS, 2)))
            run = 0
        prev = h
    if run: runs.append((round((n-run)/FPS, 1), round(run/FPS, 2)))
    worst = max((r[1] for r in runs), default=0)
    return worst, [r for r in runs if r[1] >= thresh]


# ---- persistent brand mark -------------------------------------------------
# Sits top-left from the first frame to the last, so anyone who watches even a
# second of the clip sees where it came from. Kept small and low contrast on
# purpose: a full-size URL in the opening frame reads as an ad, and people swipe
# on ads inside half a second. The endcard still carries the loud call to action.
_SPOT = None
def brand(img, d, alpha=1.0, y=252, x=56):
    global _SPOT
    if alpha <= 0.01: return
    if _SPOT is None:
        # repo-relative, so this runs wherever the checkout lives
        p = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))), "paths/assets/spot/spot-happy.png")
        s = Image.open(p).convert("RGBA")
        h = 66
        _SPOT = s.resize((max(1, int(s.width*h/s.height)), h), Image.LANCZOS)
    sp = _SPOT
    if alpha < 0.999:
        sp = sp.copy()
        a = sp.getchannel("A").point(lambda v: int(v*alpha))
        sp.putalpha(a)
    img.paste(sp, (x, y-sp.height//2), sp)
    d.text((x+sp.width+14, y-11), "Quantica", font=font(F_DISP, 34),
           fill=mix(BG, INK, alpha*0.85), anchor="lm")
    d.text((x+sp.width+14, y+18), "quanticaedu.com", font=font(F_SANS, 25),
           fill=mix(BG, GREEN, alpha*0.9), anchor="lm")
