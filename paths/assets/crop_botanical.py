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
 'pebble-sprout':(680,278,822,386),
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

def key_rock(crop):
    # the pebble is a near-white stone on near-white bg, so plain keying bites a notch
    # out of its lit face. Close the low-sat rock silhouette (sealing the notch) without
    # touching the saturated green sprout, then deepen the stone so it reads gray.
    c = crop.convert('RGB'); w,h = c.size; px = c.load()
    marker = c.copy(); SENT=(255,0,255)
    for s in edge_seeds(w,h):
        try: ImageDraw.floodfill(marker, s, SENT, thresh=26)
        except Exception: pass
    mpx = marker.load()
    keep = Image.new('L',(w,h),0); kp=keep.load()
    rock = Image.new('L',(w,h),0); rk=rock.load()
    for y in range(h):
        for x in range(w):
            if mpx[x,y]==SENT: continue
            r,g,b = px[x,y]; sat = max(r,g,b)-min(r,g,b)
            kp[x,y]=255
            if sat<24: rk[x,y]=255
    rock = rock.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.MinFilter(15))  # close notch
    fillm = rock.copy(); ImageDraw.floodfill(fillm,(0,0),128,thresh=0)
    fp=fillm.load(); rk=rock.load()
    for y in range(h):
        for x in range(w):
            if rk[x,y]==0 and fp[x,y]!=128: rk[x,y]=255
    mask = ImageChops.lighter(keep, rock).filter(ImageFilter.GaussianBlur(0.6))
    op = c.load()
    for y in range(h):
        for x in range(w):
            r,g,b = op[x,y]; sat=max(r,g,b)-min(r,g,b); lum=(r+g+b)/3
            if sat<26 and lum>150:
                op[x,y]=(int(r*0.86),int(g*0.86),int(b*0.86))
    res = c.convert('RGBA'); res.putalpha(mask)
    bbox = mask.getbbox()
    if bbox:
        l,t,r,b = bbox; pad=3
        res = res.crop((max(0,l-pad),max(0,t-pad),min(w,r+pad),min(h,b+pad)))
    return res

for name, box in boxes.items():
    crop = im.crop(box)
    res = key_rock(crop) if name=='pebble-sprout' else key_and_trim(crop)
    res.save(os.path.join(out, name + '.png'))
print('done:', ', '.join(boxes))
