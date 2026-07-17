# -*- coding: utf-8 -*-
import os
from PIL import Image
src = r'C:\Users\srivi\Downloads\Chat_spot_images\ChatGPT Image Jul 16, 2026, 01_06_20 AM (5).png'
im = Image.open(src).convert('RGB')
out = r'C:\Users\srivi\OneDrive\Desktop\quantica_claude_code\assets\spot'
os.makedirs(out, exist_ok=True)

# tight boxes on the 1024x1536 sheet (exclude text labels + adjacent poses)
boxes = {
 'hero':     (555,72,915,586),
 'front':    (75,660,298,965),
 'happy':    (60,1016,238,1240),
 'focused':  (238,998,425,1240),
 'thinking': (425,998,590,1240),
 'excited':  (606,998,778,1240),
 'encour':   (792,998,980,1240),
}

def key_and_trim(crop):
    c = crop.convert('RGBA')
    px = c.load()
    w, h = c.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r > 236 and g > 236 and b > 233:   # near-white sheet background
                px[x, y] = (r, g, b, 0)
    bbox = c.split()[3].getbbox()
    if bbox:
        l, t, r, b = bbox
        pad = 6
        c = c.crop((max(0, l-pad), max(0, t-pad), min(w, r+pad), min(h, b+pad)))
    return c

for name, box in boxes.items():
    key_and_trim(im.crop(box)).save(os.path.join(out, 'spot-' + name + '.png'))
print('done:', ', '.join('spot-'+n for n in boxes))
