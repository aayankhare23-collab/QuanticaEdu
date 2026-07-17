# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFilter

src = r'C:\Users\srivi\Downloads\Chat_spot_images\ChatGPT Image Jul 16, 2026, 01_06_20 AM (6).png'
im = Image.open(src).convert('RGB')
out = r'C:\Users\srivi\OneDrive\Desktop\quantica_claude_code\assets\botanical'
os.makedirs(out, exist_ok=True)

# boxes on the 853x1844 roadmap sheet
boxes = {
 'leaf-branch':  (10,135,171,352),
 'pebble-sprout':(680,278,822,390),
 'sprout-soil':  (76,1510,250,1705),
 'sprig':        (375,275,480,318),
}

# per-image flood threshold: greens/browns can use a big thresh (well separated from
# the light background, so shadows get eaten); the light grey rock needs a small one
# so the flood stops at the rock instead of eating it.
flood_thresh = {'pebble-sprout': 22}
# light-pixel cleanup cutoff: greens are dark so an aggressive cutoff clears their soft
# drop-shadow; the rock body is itself light grey, so use a high cutoff that only clears
# the pale trapped shadow and never the rock.
lum_cut = {'pebble-sprout': 236}

def key_and_trim(crop, thresh, lcut):
    orig = crop.convert('RGB')
    w, h = orig.size
    px = orig.load()

    # 1) flood-fill the connected background from every edge -> mark transparent
    marker = orig.copy()
    SENT = (255, 0, 255)
    seeds = ([(x, 0) for x in range(0, w, 8)] + [(x, h-1) for x in range(0, w, 8)] +
             [(0, y) for y in range(0, h, 8)] + [(w-1, y) for y in range(0, h, 8)])
    for s in seeds:
        try:
            ImageDraw.floodfill(marker, s, SENT, thresh=thresh)
        except Exception:
            pass
    mpx = marker.load()

    mask = Image.new('L', (w, h), 255)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            lum = 0.299*r + 0.587*g + 0.114*b
            sat = (max(r, g, b) - min(r, g, b))
            # transparent if flood-reached, OR a leftover light + desaturated
            # pixel (soft drop-shadow / halo). Rock body (lum ~223) and the greens
            # (lum ~120) stay; only pale grey shadow/background is cut.
            if mpx[x, y] == SENT or (lum > lcut and sat < 16):
                mp[x, y] = 0

    # fill interior holes: any transparent region not connected to the border is a
    # hole punched inside the subject (speckles) -> make it opaque again
    fillm = mask.copy()
    ImageDraw.floodfill(fillm, (0, 0), 128, thresh=0)          # mark border-connected transparency
    # (only works if corner is transparent; corners are background, so it is)
    fp = fillm.load(); mp2 = mask.load()
    for y in range(h):
        for x in range(w):
            if mp2[x, y] == 0 and fp[x, y] != 128:
                mp2[x, y] = 255                               # interior hole -> opaque

    mask = mask.filter(ImageFilter.MinFilter(3))              # erode 1px: shave fringe + shadow tendrils
    mask = mask.filter(ImageFilter.GaussianBlur(0.6))         # gentle edge feather
    res = orig.convert('RGBA')
    res.putalpha(mask)
    bbox = mask.getbbox()
    if bbox:
        l, t, r, b = bbox
        pad = 3
        res = res.crop((max(0, l-pad), max(0, t-pad), min(w, r+pad), min(h, b+pad)))
    return res

for name, box in boxes.items():
    key_and_trim(im.crop(box), flood_thresh.get(name, 55), lum_cut.get(name, 231)).save(os.path.join(out, name + '.png'))
print('done:', ', '.join(boxes))
