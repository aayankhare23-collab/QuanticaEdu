# -*- coding: utf-8 -*-
import os
from PIL import Image, ImageDraw, ImageFilter, ImageChops

src = r'C:\Users\srivi\Downloads\Chat_spot_images\ChatGPT Image Jul 16, 2026, 01_06_20 AM (6).png'
im = Image.open(src).convert('RGB')
out = r'C:\Users\srivi\OneDrive\Desktop\quantica_claude_code\assets\botanical'
os.makedirs(out, exist_ok=True)

# boxes on the 853x1844 roadmap sheet
boxes = {
 'leaf-branch':  (10,135,171,352),
 'sprout-soil':  (76,1510,250,1705),
 'sprig':        (375,275,480,318),
}

def edge_seeds(w, h):
    return ([(x,0) for x in range(0,w,5)] + [(x,h-1) for x in range(0,w,5)] +
            [(0,y) for y in range(0,h,5)] + [(w-1,y) for y in range(0,h,5)])

def key_and_trim(crop, thresh=55, lcut=231):
    # greens/browns: flood bg + drop soft light shadow (they are well separated from white)
    orig = crop.convert('RGB'); w, h = orig.size; px = orig.load()
    marker = orig.copy(); SENT = (255,0,255)
    for s in edge_seeds(w,h):
        try: ImageDraw.floodfill(marker, s, SENT, thresh=thresh)
        except Exception: pass
    mpx = marker.load()
    mask = Image.new('L',(w,h),255); mp = mask.load()
    for y in range(h):
        for x in range(w):
            r,g,b = px[x,y]; lum = 0.299*r+0.587*g+0.114*b; sat = max(r,g,b)-min(r,g,b)
            if mpx[x,y]==SENT or (lum>lcut and sat<16): mp[x,y]=0
    mask = mask.filter(ImageFilter.GaussianBlur(0.6))
    res = orig.convert('RGBA'); res.putalpha(mask)
    bbox = mask.getbbox()
    if bbox:
        l,t,r,b = bbox; pad=3
        res = res.crop((max(0,l-pad),max(0,t-pad),min(w,r+pad),min(h,b+pad)))
    return res

def key_rock(img):
    # rock + green plant from the user's near-white screenshot (pebble-source.png):
    # flood the connected background, split the low-sat stone from the saturated plant,
    # close the stone silhouette to seal the near-white notch, keep the plant as-is.
    from PIL import ImageChops
    c = img.convert('RGB'); w, h = c.size; px = c.load()
    marker = c.copy(); SENT = (255, 0, 255)
    seeds = ([(x, 0) for x in range(0, w, 4)] + [(x, h-1) for x in range(0, w, 4)] +
             [(0, y) for y in range(0, h, 4)] + [(w-1, y) for y in range(0, h, 4)])
    for s in seeds:
        try: ImageDraw.floodfill(marker, s, SENT, thresh=34)
        except Exception: pass
    mpx = marker.load()
    rock = Image.new('L', (w, h), 0); rk = rock.load()
    plant = Image.new('L', (w, h), 0); pl = plant.load()
    for y in range(h):
        for x in range(w):
            if mpx[x, y] == SENT: continue
            r, g, b = px[x, y]; sat = max(r, g, b) - min(r, g, b)
            if sat < 30: rk[x, y] = 255
            else: pl[x, y] = 255
    rock = rock.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))
    fillm = rock.copy()
    for cc in [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]:
        try: ImageDraw.floodfill(fillm, cc, 128, thresh=0)
        except Exception: pass
    fp = fillm.load(); rk = rock.load()
    for y in range(h):
        for x in range(w):
            if rk[x, y] == 0 and fp[x, y] != 128: rk[x, y] = 255
    mask = ImageChops.lighter(rock, plant).filter(ImageFilter.GaussianBlur(0.6))
    res = c.convert('RGBA'); res.putalpha(mask)
    bbox = mask.getbbox()
    if bbox:
        l, t, r, b = bbox; pad = 4
        res = res.crop((max(0, l-pad), max(0, t-pad), min(w, r+pad), min(h, b+pad)))
    return res

for name, box in boxes.items():
    key_and_trim(im.crop(box)).save(os.path.join(out, name + '.png'))
# pebble-sprout comes from the user's rock+plant screenshot, not sheet (6)
_peb = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pebble-source.png')
key_rock(Image.open(_peb)).save(os.path.join(out, 'pebble-sprout.png'))
print('done: ' + ', '.join(list(boxes) + ['pebble-sprout']))
