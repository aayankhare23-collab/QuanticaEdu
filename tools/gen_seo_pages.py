# Generate static, crawlable SEO pages for a course:
#   - one course HUB page at /<course>            (<course>.html at repo root)
#   - one LESSON page per lesson at /<course>/<slug>.html
# Real teaching intro + problem prompts (KaTeX-rendered), prev/next links, structured data,
# and an "Open in the course" CTA that deep-launches the app.
# Usage: python3 tools/gen_seo_pages.py [course]   (default: prealgebra)
import json, re, html as H, os, sys

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE=sys.argv[1] if len(sys.argv)>1 else "prealgebra"
BASE="https://quanticaedu.com"

# Per-course display metadata. New courses: add an entry (falls back to a generic default).
COURSE_META={
 "prealgebra":{"title":"Prealgebra","level":"Middle school / Prealgebra","og":"og-prealgebra.png",
   "lead":"Work real problems with instant feedback and Sprout, a tutor that helps you find the answer yourself.",
   "blurb":("Learn prealgebra online by solving real problems, not memorizing. Quantica's Prealgebra "
     "course covers 12 chapters and 70 lessons, from arithmetic, exponents, and fractions to ratios, "
     "percents, and geometry, with instant feedback and Sprout, a tutor that helps you find the answer "
     "yourself. Free to start."),
   "note":"", "workload":"P12W", "cross":("algebra1","Algebra I"),
   "faq":[("Is the Prealgebra course free?","Yes, you can start the full Prealgebra course for free, no card required."),
          ("Do I need any prior math knowledge?","No. Prealgebra starts from the rules of arithmetic and builds up, and Sprout is there whenever a problem stops you."),
          ("How is Quantica different from other prealgebra courses?","You learn by solving real problems with instant feedback and layered hints, so the ideas emerge from your own work instead of being memorized."),
          ("How long is the Prealgebra course?","It has 12 chapters and 70 lessons. You move at your own pace, in any order.")]},
 "algebra1":{"title":"Algebra I","level":"High school / Algebra I","og":"og-default.png",
   "lead":"Work real problems with instant feedback and Sprout, a tutor that helps you find the answer yourself.",
   "blurb":("Learn Algebra I online by solving real problems, not memorizing. Quantica's Algebra I course "
     "spans 15 chapters and 79 lessons, from expressions and linear equations to quadratics, functions, "
     "and logarithms, with instant feedback and Sprout, a tutor that helps you find the answer yourself. "
     "Free to start, in early access."),
   "note":"Chapter 1 is live now, with new lessons arriving regularly while Algebra I is in early access.",
   "workload":"P15W", "cross":("prealgebra","Prealgebra"),
   "faq":[("Is the Algebra I course free?","Yes, you can start Algebra I for free while it is in early access, no card required."),
          ("What does Quantica's Algebra I cover?","Expressions, linear equations, exponents and radicals, systems, graphing, inequalities, quadratics, functions, polynomials, exponentials, and logarithms, 15 chapters in all."),
          ("Do I need to finish Prealgebra first?","No, but the two fit together. If arithmetic and fractions feel shaky, Prealgebra builds the ground Algebra I stands on."),
          ("How is Quantica's Algebra I different?","You learn by solving real problems with instant feedback and layered hints, so each idea emerges from your own work instead of being memorized.")]},
}
META=COURSE_META.get(COURSE,{"title":COURSE.replace('-',' ').title(),"level":COURSE,"og":"og-default.png",
   "lead":"Work real problems with instant feedback and Sprout, a tutor that helps you find the answer yourself.",
   "blurb":f"Learn {COURSE} online by solving, with Sprout. Free to start.","note":"","workload":"P12W","cross":None,"faq":[]})
CTITLE=META["title"]; OGIMG=META["og"]; LEVEL=META["level"]

GA='''<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}(function(){try{var h=location.hostname;if(h!=='quanticaedu.com'&&h!=='www.quanticaedu.com')return;if(location.search.indexOf('imfounder=1')>-1&&!localStorage.getItem('qa_internal')){localStorage.setItem('qa_internal','1');alert('Got it. Analytics is now off on this device.');}if(localStorage.getItem('qa_internal')==='1')return;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-98WQ2BFR6N';document.head.appendChild(s);gtag('js',new Date());gtag('config','G-98WQ2BFR6N',{allow_google_signals:false,allow_ad_personalization_signals:false});}catch(e){}})();</script>'''
toc=json.load(open(os.path.join(ROOT,"lessons",COURSE,"toc.json"),encoding="utf-8"))
s=open(ROOT+"/data/lessons.js",encoding="utf-8").read()
DATA=json.loads(s[s.index('{'):s.rindex('}')+1])[COURSE]

# lesson order + chapter lookup from TOC (only lessons that actually have data)
ORDER=[]; CHOF={}
for c in toc:
    for l in c['lessons']:
        if l['k'] in DATA:
            ORDER.append(l['k']); CHOF[l['k']]=(c['n'], c['t'])

def slugify(t):
    t=re.sub(r'&[a-z]+;',' ',t); t=re.sub(r'[^a-zA-Z0-9]+','-',t).strip('-').lower()
    return re.sub(r'-+','-',t)
SLUG={}; used=set()
for k in ORDER:
    base=slugify(DATA[k]['title']) or ('lesson-'+k.replace('.','-'))
    sl=base; i=2
    while sl in used: sl=base+'-'+str(i); i+=1
    used.add(sl); SLUG[k]=sl
json.dump({k:SLUG[k] for k in ORDER}, open(os.path.join(ROOT,"lessons",COURSE,"slugmap.json"),"w",encoding="utf-8"), indent=1)

def strip_text(x):
    x=re.sub(r'<svg.*?</svg>','',x,flags=re.S)
    x=re.sub(r'\$\$?.*?\$\$?',' ',x)                 # drop math for the plain-text summary
    x=re.sub(r'\\\(|\\\)','',x); x=re.sub(r'<[^>]+>',' ',x)
    x=H.unescape(x); return re.sub(r'\s+',' ',x).strip()

def _wc(x):
    return len(re.sub('<[^>]+>',' ',re.sub(r'<svg.*?</svg>','',x,flags=re.S)).split())

def render_intro(L):
    # The lesson's opening only (a real intro, ~90+ words for SEO), problem PROMPTS shown but no
    # solutions and no full dump. The worked problems, hints, and Sprout live in the app.
    out=[]; words=0
    for b in L.get('blocks',[]):
        t=b.get('t'); x=b.get('x') or ''
        if t=='p':    out.append(f'<p>{x}</p>')
        elif t=='imp':out.append(f'<aside class="key"><span class="tag">Key idea</span><div>{x}</div></aside>')
        elif t=='fact':out.append(f'<aside class="fact"><span class="tag">{H.escape(b.get("label") or "Fun fact")}</span><div>{x}</div></aside>')
        elif t=='prob':out.append(f'<div class="prob"><div class="prob-q">{x}</div></div>')
        words+=_wc(x)
        if len(out)>=2 and words>=90: break
        if len(out)>=4: break
    return "\n".join(out)

def gate_html(k):
    return ('<aside class="gate"><div class="gate-in">'+MILO_BIG+
            '<h2>Ready to actually <span class="mark">do it</span>?</h2>'
            '<p>The rest of this lesson, the worked problems, layered hints, and Sprout right beside you, happens inside the course. Free to start.</p>'
            f'<a class="pill solid big" href="/landing.html?course={COURSE}&amp;lesson={k}">Start this lesson, free &rarr;</a></div></aside>')

CSS='''
:root{--bg:#F4F9EC;--ink:#1B2E1F;--lime:#C7F09A;--slate:#5FA06B;--gray:#556A58;--line:rgba(22,75,53,.14)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:'Inter',system-ui,sans-serif;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit}img,svg{max-width:100%}
.wrap{max-width:820px;margin:0 auto;padding:0 clamp(20px,4vw,40px)}
h1,h2,h3{font-family:'Fraunces',Georgia,serif;font-weight:700;letter-spacing:-.03em;line-height:1.05;margin:0}
.mark{background:var(--lime);border-radius:.16em;padding:.02em .2em}
.milo{width:1em;height:1.15em;vertical-align:-.24em;object-fit:contain}
.nav{display:flex;align-items:center;gap:12px;padding:20px 0}
.brand{font-weight:700;font-size:19px;letter-spacing:-.03em;text-decoration:none;margin-right:auto;display:flex;align-items:center;gap:8px}
.brand .milo{width:24px;height:24px}
.pill{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:14px;padding:11px 20px;border-radius:999px;border:1.5px solid var(--ink);text-decoration:none;white-space:nowrap;transition:transform .15s}
.pill:hover{transform:translateY(-2px)}.pill.solid{background:var(--lime);border-color:var(--lime)}
.crumbs{font-size:13px;color:var(--gray);padding:8px 0 0}.crumbs a{text-decoration:none}.crumbs a:hover{text-decoration:underline}
.head{padding:22px 0 8px}.head .ey{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--gray);margin-bottom:12px}
.head h1{font-size:clamp(30px,5.5vw,52px);letter-spacing:-.035em}
.startbar{display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px;padding-bottom:28px;border-bottom:1px solid var(--line)}
.content{padding:12px 0 8px;font-size:17px}
.content p{margin:18px 0}
.content b{font-weight:700}
.key{background:linear-gradient(180deg,rgba(199,240,154,.5),rgba(199,240,154,.22));border:1px solid rgba(10,10,10,.14);border-radius:16px;padding:20px 22px;margin:24px 0}
.fact{background:rgba(95,160,107,.22);border-left:3px solid var(--slate);border-radius:0 12px 12px 0;padding:16px 20px;margin:24px 0}
.tag{display:block;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gray);margin-bottom:8px}
.prob{border:1px solid var(--line);border-radius:16px;padding:18px 22px;margin:18px 0;background:rgba(255,255,255,.35)}
.prob-q{font-size:16px}
.sol{margin-top:12px}.sol summary{cursor:pointer;font-weight:600;font-size:14px;color:var(--gray)}
.sol[open] summary{margin-bottom:10px}.sol>div{font-size:15px;color:#242424}
.sec-h{font-size:clamp(24px,4vw,38px);letter-spacing:-.03em;margin:44px 0 8px}
.katex-display{overflow-x:auto;overflow-y:hidden;padding:4px 0}
.pager{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:48px 0 10px}
.pager a{border:1px solid var(--line);border-radius:16px;padding:16px 20px;text-decoration:none;background:rgba(255,255,255,.35)}
.pager a:hover{border-color:var(--ink)}.pager .dir{font-size:12px;color:var(--gray);text-transform:uppercase;letter-spacing:.1em}
.pager a.next{text-align:right}.pager .t{font-weight:600;margin-top:4px}
.foot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center;border-top:1px solid var(--ink);padding:30px 0;margin-top:30px;font-size:14px}
.foot a{text-decoration:none;margin-left:16px}
.gate{margin:6px 0 18px;border:1.5px solid var(--ink);border-radius:24px;background:linear-gradient(180deg,rgba(199,240,154,.42),rgba(199,240,154,.15));padding:clamp(30px,5vw,50px) clamp(22px,4vw,40px);text-align:center}
.gate-in{max-width:44ch;margin:0 auto}
.milo-big{width:58px;height:58px;object-fit:contain;margin:0 auto 12px;display:block}
.gate h2{font-size:clamp(26px,4.6vw,42px);letter-spacing:-.03em;margin:0 0 14px}
.gate p{font-size:17px;color:#242424;margin:0 0 26px}
.pill.big{padding:15px 30px;font-size:16px}
@media(max-width:560px){.pager{grid-template-columns:1fr}.pager a.next{text-align:left}}
'''
HUB_CSS='''
:root{--bg:#F4F9EC;--ink:#1B2E1F;--lime:#C7F09A;--slate:#5FA06B;--gray:#556A58;--line:rgba(22,75,53,.14)}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Inter',system-ui,sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:0 clamp(20px,4vw,56px)}
h1,h2,h3{font-family:'Fraunces',Georgia,serif;margin:0;font-weight:700;letter-spacing:-.03em;line-height:1}
.mark{background:var(--lime);border-radius:.16em;padding:.02em .2em}
.milo{width:1em;height:1.15em;vertical-align:-.24em;object-fit:contain}
.nav{display:flex;align-items:center;gap:12px;padding:22px 0}
.brand{font-weight:700;font-size:20px;letter-spacing:-.03em;text-decoration:none;margin-right:auto;display:flex;align-items:center;gap:8px}
.brand .milo{width:26px;height:26px}
.pill{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:15px;padding:12px 22px;border-radius:999px;border:1.5px solid var(--ink);text-decoration:none;transition:transform .15s}
.pill:hover{transform:translateY(-2px)}
.pill.solid{background:var(--lime);border-color:var(--lime)}
.hero{padding:clamp(30px,6vw,72px) 0 clamp(24px,4vw,48px)}
.kick{font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gray);margin:0 0 16px}
.hero h1{font-size:clamp(48px,9vw,110px);letter-spacing:-.04em}
.hero .lead{font-size:clamp(17px,1.6vw,21px);max-width:60ch;margin:24px 0 0;color:var(--ink)}
.hero .lead .dim{color:var(--gray)}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:32px}
.stats{display:flex;gap:32px;flex-wrap:wrap;margin-top:34px;border-top:1px solid var(--line);padding-top:26px}
.stat b{display:block;font-size:32px;letter-spacing:-.03em}
.stat span{color:var(--gray);font-size:14px}
section{padding:clamp(40px,7vw,90px) 0}
.sec-h{font-size:clamp(30px,5vw,56px);letter-spacing:-.035em;max-width:18ch}
.sec-sub{color:var(--gray);max-width:60ch;margin:18px 0 0;font-size:17px}
.chs{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:40px}
.ch{border:1px solid var(--line);border-radius:20px;padding:24px 26px;background:linear-gradient(180deg,rgba(255,255,255,.5),rgba(255,255,255,.15))}
.ch header{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.ch .chn{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--gray)}
.ch h3{font-size:22px;letter-spacing:-.02em;flex:1 1 auto}
.ch .chc{font-size:13px;color:var(--gray)}
.ch ul{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.ch li{font-size:15px;color:#242424}
.ch li a{color:inherit;text-decoration:none;border-bottom:1px solid var(--line)}
.ch li a:hover{border-color:var(--ink)}
.ch .lk{display:inline-block;min-width:34px;color:var(--gray);font-variant-numeric:tabular-nums}
.ch li.soon{color:var(--gray)}
.ch li.soon em{font-style:normal;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:1px 6px;margin-left:4px;border-radius:999px;background:var(--line);color:var(--ink);vertical-align:1px}
.how{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:40px}
.how .step .n{font-size:40px;font-weight:700;letter-spacing:-.03em}
.how .step h3{font-size:20px;margin:8px 0 6px}
.how .step p{color:var(--gray);font-size:15px;margin:0}
.faq{max-width:760px}
details{border-top:1px solid var(--line);padding:20px 0}
details:last-child{border-bottom:1px solid var(--line)}
summary{list-style:none;cursor:pointer;font-weight:600;font-size:19px;letter-spacing:-.02em;display:flex;justify-content:space-between}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--gray);font-weight:400;font-size:24px}
details[open] summary::after{content:"\\2013"}
details p{color:var(--gray);margin:14px 0 0}
.cta-band{text-align:center;padding:clamp(48px,8vw,110px) 0}
.cta-band h2{font-size:clamp(34px,6vw,72px);letter-spacing:-.04em}
.foot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center;border-top:1px solid var(--ink);padding:34px 0;font-size:14px}
.foot a{text-decoration:none;margin-left:18px}
@media(max-width:760px){.chs,.how{grid-template-columns:1fr}}
'''
MILO='<img src="/paths/assets/spot/spot-happy.png" class="milo" alt="Sprout">'
MILO_BIG=MILO.replace('class="milo"','class="milo-big"')
KATEX='''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>document.addEventListener("DOMContentLoaded",function(){renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"\\\\[",right:"\\\\]",display:true},{left:"\\\\(",right:"\\\\)",display:false},{left:"$",right:"$",display:false}],throwOnError:false});});</script>'''

def gen_hub():
    hub_url=f"{BASE}/{COURSE}"
    nchap=len(toc); nlesson=sum(len(c['lessons']) for c in toc)
    # curriculum grid
    cards=[]
    for c in toc:
        lis=[]
        for l in c['lessons']:
            k=l['k']; t=H.escape(l['t'])
            if k in SLUG:
                lis.append(f'<li><span class="lk">{k}</span> <a href="/{COURSE}/{SLUG[k]}">{t}</a></li>')
            else:
                lis.append(f'<li class="soon"><span class="lk">{k}</span> {t} <em>soon</em></li>')
        cards.append(f'<article class="ch"><header><span class="chn">Chapter {c["n"]}</span>'
                     f'<h3>{H.escape(c["t"])}</h3><span class="chc">{len(c["lessons"])} lessons</span></header>'
                     f'<ul>{"".join(lis)}</ul></article>')
    grid="\n".join(cards)
    faq_v="".join(f'<details><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q,a in META["faq"])
    note=f'<p class="sec-sub" style="margin-top:12px">{H.escape(META["note"])}</p>' if META.get("note") else ''
    crosshtml=''
    if META.get("cross"):
        cs,ct=META["cross"]; crosshtml=f'<a class="pill" href="/{cs}">{H.escape(ct)}</a>'
    SF=f"/landing.html?course={COURSE}&amp;start=1"  # valid-HTML start-free deep link
    # structured data
    ld_course={"@context":"https://schema.org","@type":"Course","name":CTITLE,"description":META["blurb"],
      "url":hub_url,"courseCode":COURSE,"educationalLevel":LEVEL,"inLanguage":"en",
      "teaches":[c["t"] for c in toc],
      "provider":{"@type":"Organization","name":"Quantica","url":BASE+"/"},
      "hasCourseInstance":{"@type":"CourseInstance","courseMode":"online","courseWorkload":META["workload"]},
      "offers":{"@type":"Offer","price":"0","priceCurrency":"USD","category":"Free trial"},
      "hasPart":[{"@type":"Syllabus","name":f'Chapter {c["n"]}: {c["t"]}',
                  "description":", ".join(l["t"] for l in c["lessons"])} for c in toc]}
    ld_crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Quantica","item":BASE+"/"},
      {"@type":"ListItem","position":2,"name":CTITLE,"item":hub_url}]}
    ld_faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in META["faq"]]}
    desc=H.escape(META["blurb"])
    page=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{GA}
<title>{H.escape(CTITLE)} Course, Learn {H.escape(CTITLE)} by Solving | Quantica</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{hub_url}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website"><meta property="og:site_name" content="Quantica">
<meta property="og:title" content="{H.escape(CTITLE)} Course, Learn {H.escape(CTITLE)} by Solving">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{hub_url}"><meta property="og:image" content="{BASE}/{OGIMG}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{H.escape(CTITLE)} Course | Quantica">
<meta name="twitter:description" content="{nchap} chapters, {nlesson} lessons. Learn by solving, with Sprout. Free to start.">
<meta name="twitter:image" content="{BASE}/{OGIMG}">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">{json.dumps(ld_course)}</script>
<script type="application/ld+json">{json.dumps(ld_crumb)}</script>
<script type="application/ld+json">{json.dumps(ld_faq)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{HUB_CSS}</style></head>
<body>
<header class="wrap nav">
  <a class="brand" href="/paths/landing.html">{MILO}Quantica</a>
  {crosshtml}
  <a class="pill" href="/paths/landing.html">Home</a>
  <a class="pill solid" href="{SF}">Start free</a>
</header>
<main>
<section class="wrap hero">
  <p class="kick">Quantica · Course</p>
  <h1><span class="mark">{H.escape(CTITLE)}</span></h1>
  <p class="lead">Learn {H.escape(CTITLE)} by <em>solving</em>, not memorizing. <span class="dim">{H.escape(META["lead"])}</span></p>
  <div class="cta">
    <a class="pill solid" href="{SF}">Start the course, free &rarr;</a>
    <a class="pill" href="#curriculum">See the curriculum</a>
  </div>
  <div class="stats">
    <div class="stat"><b>{nchap}</b><span>chapters</span></div>
    <div class="stat"><b>{nlesson}</b><span>lessons</span></div>
    <div class="stat"><b>$0</b><span>to start</span></div>
  </div>
</section>
<section class="wrap" id="curriculum">
  <h2 class="sec-h">What you'll <span class="mark">learn</span></h2>
  <p class="sec-sub">The full {H.escape(CTITLE)} path. Every lesson is a problem to crack, not a worksheet to grind.</p>
  {note}
  <div class="chs">
  {grid}
  </div>
</section>
<section class="wrap">
  <h2 class="sec-h">How it <span class="mark">works</span></h2>
  <div class="how">
    <div class="step"><div class="n">01</div><h3>Solve, don't memorize</h3><p>Each lesson is a real problem. The idea emerges as you work toward it.</p></div>
    <div class="step"><div class="n">02</div><h3>Guided, never spoiled</h3><p>Layered hints and Sprout nudge you toward the answer without handing it over.</p></div>
    <div class="step"><div class="n">03</div><h3>It sticks</h3><p>Because you discovered it yourself, the next hard problem feels winnable.</p></div>
  </div>
</section>
<section class="wrap faq">
  <h2 class="sec-h">Good to know</h2>
  <div style="margin-top:30px">{faq_v}</div>
</section>
<section class="wrap cta-band">
  <h2>Start <span class="mark">solving</span>.</h2>
  <div class="cta" style="justify-content:center;margin-top:30px"><a class="pill solid" href="{SF}">Start {H.escape(CTITLE)}, free &rarr;</a></div>
</section>
</main>
<footer class="wrap foot">
  <a class="brand" href="/paths/landing.html">{MILO}Quantica</a>
  <div><a href="/paths/landing.html">Home</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div>
</footer>
</body></html>'''
    open(f"{ROOT}/{COURSE}.html","w",encoding="utf-8").write(page)

# ---- lesson pages ----
os.makedirs(ROOT+"/"+COURSE, exist_ok=True)
sitemap_urls=[f"{BASE}/{COURSE}"]
for idx,k in enumerate(ORDER):
    L=DATA[k]; title=L['title']; slug=SLUG[k]; chn,cht=CHOF[k]
    url=f"{BASE}/{COURSE}/{slug}"
    sitemap_urls.append(url)
    desc=strip_text((L.get('blocks') or [{}])[0].get('x',''))[:155] or f"{title}, a {CTITLE} lesson from Quantica."
    desc=f"{title}: {desc}"[:158]
    prev_k=ORDER[idx-1] if idx>0 else None
    next_k=ORDER[idx+1] if idx<len(ORDER)-1 else None
    def pager_link(kk,dir_,cls):
        if not kk: return '<span></span>'
        return f'<a class="{cls}" href="/{COURSE}/{SLUG[kk]}"><span class="dir">{dir_}</span><div class="t">{H.escape(DATA[kk]["title"])}</div></a>'
    ld={"@context":"https://schema.org","@type":"LearningResource","name":title,"url":url,
        "description":desc,"inLanguage":"en","learningResourceType":"lesson",
        "educationalLevel":CTITLE,"isPartOf":{"@type":"Course","name":CTITLE,"url":BASE+"/"+COURSE},
        "provider":{"@type":"Organization","name":"Quantica","url":BASE+"/"}}
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Quantica","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":CTITLE,"item":BASE+"/"+COURSE},
        {"@type":"ListItem","position":3,"name":title,"item":url}]}
    body=render_intro(L)
    page=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{GA}
<title>{H.escape(title)}, {H.escape(CTITLE)} | Quantica</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Quantica">
<meta property="og:title" content="{H.escape(title)}, {H.escape(CTITLE)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/{OGIMG}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}/{OGIMG}">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">{json.dumps(ld)}</script>
<script type="application/ld+json">{json.dumps(crumb)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
{KATEX}
<style>{CSS}</style></head>
<body>
<header class="wrap nav"><a class="brand" href="/paths/landing.html">{MILO}Quantica</a><a class="pill" href="/{COURSE}">{H.escape(CTITLE)}</a><a class="pill solid" href="/landing.html?course={COURSE}&amp;lesson={k}">Open in the course</a></header>
<div class="wrap">
  <nav class="crumbs"><a href="/paths/landing.html">Home</a> › <a href="/{COURSE}">{H.escape(CTITLE)}</a> › Chapter {chn}: {H.escape(cht)}</nav>
  <div class="head"><p class="ey">{H.escape(CTITLE)} · Lesson {k}</p><h1>{H.escape(title)}</h1></div>
  <div class="startbar"><a class="pill solid" href="/landing.html?course={COURSE}&amp;lesson={k}">Solve this lesson, free &rarr;</a><a class="pill" href="/{COURSE}">All lessons</a></div>
  <article class="content">
  {body}
  {gate_html(k)}
  </article>
  <nav class="pager">{pager_link(prev_k,"← Previous","prev")}{pager_link(next_k,"Next →","next")}</nav>
</div>
<footer class="wrap foot"><a class="brand" href="/paths/landing.html">{MILO}Quantica</a><div><a href="/{COURSE}">{H.escape(CTITLE)}</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div></footer>
</body></html>'''
    open(f"{ROOT}/{COURSE}/{slug}.html","w",encoding="utf-8").write(page)

gen_hub()
json.dump(sitemap_urls, open(os.path.join(ROOT,"lessons",COURSE,"lesson_urls.json"),"w",encoding="utf-8"))
print(f"course={COURSE}: wrote {COURSE}.html (hub) + {len(ORDER)} lesson pages -> {COURSE}/*.html")
if ORDER: print("sample lesson:", ORDER[0], "->", "/"+COURSE+"/"+SLUG[ORDER[0]])
print("sitemap urls:", len(sitemap_urls), "(hub + lessons) written to lessons/%s/lesson_urls.json"%COURSE)
