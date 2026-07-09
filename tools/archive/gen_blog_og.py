# Generate the 1200x630 Open Graph card for the blog (wembi palette), Pillow.
from PIL import Image, ImageDraw, ImageFont
import os
BG=(237,237,235); INK=(10,10,10); LIME=(190,255,139); SLATE=(157,187,197); GRAY=(92,92,88)
W,H=1200,630
FONTS=["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
       "/System/Library/Fonts/Helvetica.ttc","/System/Library/Fonts/HelveticaNeue.ttc",
       "/Library/Fonts/Arial Bold.ttf"]
def font(sz):
    for p in FONTS:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()
def milo(d,cx,cy,r):
    d.rounded_rectangle([cx-r,cy-r,cx+r,cy+r],radius=int(r*0.62),fill=LIME)
    er=int(r*0.16)
    for ex in (cx-int(r*0.34),cx+int(r*0.34)):
        d.ellipse([ex-er,cy-int(r*0.1)-er,ex+er,cy-int(r*0.1)+er],fill=SLATE)
        pr=int(er*0.5); d.ellipse([ex-pr,cy-int(r*0.1)-pr,ex+pr,cy-int(r*0.1)+pr],fill=INK)
    d.arc([cx-int(r*0.34),cy+int(r*0.02),cx+int(r*0.34),cy+int(r*0.4)],20,160,fill=INK,width=max(3,int(r*0.07)))
def mark(d,txt,x,y,f,pad=(18,10,18,20)):
    l,t,rr,b=d.textbbox((x,y),txt,font=f)
    d.rounded_rectangle([l-pad[0],t-pad[1],rr+pad[2],b+pad[3]],radius=16,fill=LIME)
    d.text((x,y),txt,font=f,fill=INK)
img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
# eyebrow
d.text((92,86),"QUANTICA  ·  BLOG",font=font(30),fill=GRAY)
milo(d,W-190,180,120)
fH=font(92); y=150
# line 1
d.text((90,y),"Let them",font=fH,fill=INK); y+=118
# line 2 (marked)
mark(d,"struggle",90,y,fH); x=90+d.textlength("struggle",font=fH)+40
d.text((x,y),".",font=fH,fill=INK); y+=140
d.text((92,y),"The case for productive struggle in math.",font=font(34),fill=GRAY)
milo(d,112,H-70,26); d.text((150,H-92),"quanticaedu",font=font(40),fill=INK)
out=os.path.dirname(os.path.abspath(__file__))+"/og-blog.png"
img.save(out); print("wrote",out)
