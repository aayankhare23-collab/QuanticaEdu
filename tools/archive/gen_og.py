# Generate 1200x630 Open Graph share images (wembi palette) with Pillow.
from PIL import Image, ImageDraw, ImageFont
import os

BG=(237,237,235); INK=(10,10,10); LIME=(190,255,139); SLATE=(157,187,197); GRAY=(92,92,88)
W,H=1200,630
FONTS=[
 "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
 "/System/Library/Fonts/Helvetica.ttc",
 "/System/Library/Fonts/HelveticaNeue.ttc",
 "/Library/Fonts/Arial Bold.ttf",
]
def font(sz):
    for p in FONTS:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

def milo(d, cx, cy, r):
    # squircle-ish body via rounded rectangle + face
    d.rounded_rectangle([cx-r,cy-r,cx+r,cy+r], radius=int(r*0.62), fill=LIME)
    er=int(r*0.16)
    for ex in (cx-int(r*0.34), cx+int(r*0.34)):
        d.ellipse([ex-er,cy-int(r*0.1)-er,ex+er,cy-int(r*0.1)+er], fill=SLATE)
        pr=int(er*0.5); d.ellipse([ex-pr,cy-int(r*0.1)-pr,ex+pr,cy-int(r*0.1)+pr], fill=INK)
    # smile
    d.arc([cx-int(r*0.34),cy+int(r*0.02),cx+int(r*0.34),cy+int(r*0.4)], 20,160, fill=INK, width=max(3,int(r*0.07)))

def mark(d, txt, x, y, f, pad=(18,10,18,20)):
    l,t,rr,b=d.textbbox((x,y),txt,font=f)
    d.rounded_rectangle([l-pad[0],t-pad[1],rr+pad[2],b+pad[3]], radius=16, fill=LIME)
    d.text((x,y),txt,font=f,fill=INK)

def card(path, lines, sub, brand):
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    milo(d, W-190, 180, 120)
    y=150
    fH=font(96)
    for seg in lines:  # seg = list of (text, highlight?)
        x=90
        for text,hl in seg:
            if hl: mark(d,text,x,y,fH)
            else: d.text((x,y),text,font=fH,fill=INK)
            x+=d.textlength(text,font=fH)+ (28 if hl else 20)
        y+=118
    d.text((92,y+18),sub,font=font(34),fill=GRAY)
    # brand row
    milo(d, 112, H-70, 26)
    d.text((150,H-92),brand,font=font(40),fill=INK)
    img.save(path)
    print("wrote",path)

SCR=os.path.dirname(os.path.abspath(__file__))
card(SCR+"/og-default.png",
     [[("Understand math.",False)],[("Don't ",False),("memorize",True),(" it.",False)]],
     "Learn math from prealgebra to calculus by solving, with Milo.",
     "quanticaedu")
card(SCR+"/og-prealgebra.png",
     [[("Prealgebra",False)],[("Course",True)]],
     "12 chapters, 70 lessons. Learn by solving, with Milo.",
     "quanticaedu")
