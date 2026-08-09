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
   "lead":"Work real problems with instant feedback and Milo, a tutor that helps you find the answer yourself.",
   "blurb":("Learn prealgebra online by solving real problems, not memorizing. Quantica's Prealgebra "
     "course covers 12 chapters and 70 lessons, from arithmetic, exponents, and fractions to ratios, "
     "percents, and geometry, with instant feedback and Milo, a tutor that helps you find the answer "
     "yourself. Chapter 1 is free."),
   "note":"", "workload":"P12W", "cross":("algebra1","Algebra I"),
   "faq":[("Is the Prealgebra course free?","Chapter 1 of every course is free and no card is required to begin. Everything after that is $14.99 a month."),
          ("Do I need any prior math knowledge?","No. Prealgebra starts from the rules of arithmetic and builds up, and Milo is there whenever a problem stops you."),
          ("How is Quantica different from other prealgebra courses?","You learn by solving real problems with instant feedback and layered hints, so the ideas emerge from your own work instead of being memorized."),
          ("How long is the Prealgebra course?","It has 12 chapters and 70 lessons. You move at your own pace, in any order.")]},
 "algebra1":{"title":"Algebra I","level":"High school / Algebra I","og":"og-default.png",
   "lead":"Work real problems with instant feedback and Milo, a tutor that helps you find the answer yourself.",
   "blurb":("Learn Algebra I online by solving real problems, not memorizing. Quantica's Algebra I course "
     "spans 15 chapters, from expressions and linear equations to quadratics, functions, "
     "and logarithms, with instant feedback and Milo, a tutor that helps you find the answer yourself. "
     "Chapter 1 is free."),
   "note":"New lessons arrive regularly while Algebra I is in early access.",
   "workload":"P15W", "cross":("prealgebra","Prealgebra"),
   "faq":[("Is the Algebra I course free?","Chapter 1 of every course is free and no card is required to begin. Everything after that is $14.99 a month."),
          ("What does Quantica's Algebra I cover?","Expressions, linear equations, exponents and radicals, systems, graphing, inequalities, quadratics, functions, polynomials, exponentials, and logarithms, 15 chapters in all."),
          ("Do I need to finish Prealgebra first?","No, but the two fit together. If arithmetic and fractions feel shaky, Prealgebra builds the ground Algebra I stands on."),
          ("How is Quantica's Algebra I different?","You learn by solving real problems with instant feedback and layered hints, so each idea emerges from your own work instead of being memorized.")]},
}
META=COURSE_META.get(COURSE,{"title":COURSE.replace('-',' ').title(),"level":COURSE,"og":"og-default.png",
   "lead":"Work real problems with instant feedback and Milo, a tutor that helps you find the answer yourself.",
   "blurb":f"Learn {COURSE} online by solving, with Milo. Free to start.","note":"","workload":"P12W","cross":None,"faq":[]})
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

def _block_html(b):
    # Render one lesson block as crawlable HTML. Problems show the prompt plus their hints and full
    # worked solution inside <details> (collapsed for readers, still fully indexable by Google).
    t=b.get('t'); x=b.get('x') or ''
    if t=='p':    return f'<p>{x}</p>'
    if t=='imp':  return f'<aside class="key"><span class="tag">Key idea</span><div>{x}</div></aside>'
    if t=='fact': return f'<aside class="fact"><span class="tag">{H.escape(b.get("label") or "Fun fact")}</span><div>{x}</div></aside>'
    if t=='fig':
        cap=b.get('cap') or ''
        return f'<figure class="fig">{x}{f"<figcaption>{cap}</figcaption>" if cap else ""}</figure>'
    if t=='prob':
        parts=[f'<span class="tag">Problem</span><div class="prob-q">{x}</div>']
        hints=b.get('hints') or []
        if hints:
            hl="".join(f"<li>{h}</li>" for h in hints)
            parts.append(f'<details class="sol"><summary>Show a hint</summary><ul class="hintlist">{hl}</ul></details>')
        sol=b.get('sol') or ''
        if sol:
            parts.append(f'<details class="sol"><summary>Show the full solution</summary><div>{sol}</div></details>')
        return f'<div class="prob">{"".join(parts)}</div>'
    return ''

def render_full(L):
    # The WHOLE lesson as real HTML: teaching prose, key ideas, the figure, and every problem with
    # its worked solution, then the practice set. This is the crawlable, indexable version of the
    # lesson; the app is the interactive, tutored version.
    out=[h for h in (_block_html(b) for b in L.get('blocks',[])) if h]
    rev=L.get('review') or []
    if rev:
        out.append('<h2 class="sec-h">Practice these ideas</h2>')
        for r in rev:
            sol=r.get('sol') or ''
            blk=f'<div class="prob"><span class="tag">Practice</span><div class="prob-q">{r.get("x","")}</div>'
            if sol: blk+=f'<details class="sol"><summary>Show the solution</summary><div>{sol}</div></details>'
            out.append(blk+'</div>')
    return "\n".join(out)

def gate_html(k):
    # Not a content wall (the full lesson is above). A conversion CTA into the interactive app.
    # Chapter-aware like the startbar button: only chapter 1 is genuinely free, so every other
    # lesson page dropped the "Free to start" claim rather than contradict the checkout.
    free = str(k).split('.')[0] == '1'
    tail = ' Free to start.' if free else ''
    return ('<aside class="gate"><div class="gate-in">'+MILO_BIG+
            '<h2>Learn it by <span class="mark">doing it</span></h2>'
            '<p>Reading is a start. In the course you solve each problem yourself, with instant '
            f'feedback, layered hints, and Milo right beside you when you get stuck.{tail}</p>'
            f'<a class="pill solid big" href="/landing?course={COURSE}&amp;lesson={k}">Open this lesson in the course &rarr;</a></div></aside>')

CSS='''
:root{--bg:#F4F9EC;--ink:#1B2E1F;--lime:#C7F09A;--slate:#5FA06B;--gray:#556A58;--line:rgba(22,75,53,.14)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:'Chillax',system-ui,sans-serif;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit}img,svg{max-width:100%}
.wrap{max-width:820px;margin:0 auto;padding:0 clamp(20px,4vw,40px)}
h1,h2,h3{font-family:'Chillax',system-ui,sans-serif;font-weight:700;letter-spacing:-.03em;line-height:1.05;margin:0}
.mark{background:var(--lime);border-radius:0;padding:.02em .2em}
.milo{width:1em;height:1.15em;vertical-align:-.24em;object-fit:contain}
.nav{display:flex;align-items:center;gap:12px;padding:20px 0}
.brand{font-weight:700;font-size:19px;letter-spacing:-.03em;text-decoration:none;margin-right:auto;display:flex;align-items:center;gap:8px}
.brand .milo{width:24px;height:24px}
.pill{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:14px;padding:11px 20px;border-radius:0;border:1.5px solid var(--ink);text-decoration:none;white-space:nowrap;transition:transform .15s}
.pill:hover{transform:translateY(-2px)}.pill.solid{background:var(--lime);border-color:var(--lime)}
.crumbs{font-size:13px;color:var(--gray);padding:8px 0 0}.crumbs a{text-decoration:none}.crumbs a:hover{text-decoration:underline}
.head{padding:22px 0 8px}.head .ey{font-size:14px;font-weight:600;color:var(--gray);margin-bottom:12px}
.head h1{font-size:clamp(30px,5.5vw,52px);letter-spacing:-.035em}
.startbar{display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 8px;padding-bottom:28px;border-bottom:1px solid var(--line)}
.content{padding:12px 0 8px;font-size:17px}
.content p{margin:18px 0}
.content b{font-weight:700}
.key{background:linear-gradient(180deg,rgba(199,240,154,.5),rgba(199,240,154,.22));border:1px solid rgba(10,10,10,.14);border-radius:0;padding:20px 22px;margin:24px 0}
.fact{background:rgba(95,160,107,.22);border-left:3px solid var(--slate);border-radius:0 12px 12px 0;padding:16px 20px;margin:24px 0}
.tag{display:block;font-size:14px;font-weight:700;color:var(--slate);margin-bottom:8px}
.prob{border:1px solid var(--line);border-radius:0;padding:18px 22px;margin:18px 0;background:rgba(255,255,255,.35)}
.prob-q{font-size:16px}
.sol{margin-top:12px}.sol summary{cursor:pointer;font-weight:600;font-size:14px;color:var(--slate);user-select:none}
.sol[open] summary{margin-bottom:10px}.sol>div{font-size:15px;color:#242424}
.hintlist{margin:8px 0 0;padding-left:20px}.hintlist li{margin:6px 0;font-size:15px;color:#242424}
.fig{margin:28px 0;text-align:center}.fig svg{max-width:100%;height:auto}
.fig figcaption{font-size:14px;color:var(--gray);margin-top:10px;text-align:left;line-height:1.6}
.prob .tag{color:var(--slate)}
.sec-h{font-size:clamp(24px,4vw,38px);letter-spacing:-.03em;margin:44px 0 8px}
.katex-display{overflow-x:auto;overflow-y:hidden;padding:4px 0}
.pager{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:48px 0 10px}
.pager a{border:1px solid var(--line);border-radius:0;padding:16px 20px;text-decoration:none;background:rgba(255,255,255,.35)}
.pager a:hover{border-color:var(--ink)}.pager .dir{font-size:13px;color:var(--gray)}
.pager a.next{text-align:right}.pager .t{font-weight:600;margin-top:4px}
.foot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center;border-top:1px solid var(--ink);padding:30px 0;margin-top:30px;font-size:14px}
.foot a{text-decoration:none;margin-left:16px}
.gate{margin:6px 0 18px;border:1.5px solid var(--ink);border-radius:0;background:linear-gradient(180deg,rgba(199,240,154,.42),rgba(199,240,154,.15));padding:clamp(30px,5vw,50px) clamp(22px,4vw,40px);text-align:center}
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
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Chillax',system-ui,sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:0 clamp(20px,4vw,56px)}
h1,h2,h3{font-family:'Chillax',system-ui,sans-serif;margin:0;font-weight:700;letter-spacing:-.03em;line-height:1}
.mark{background:var(--lime);border-radius:0;padding:.02em .2em}
.milo{width:1em;height:1.15em;vertical-align:-.24em;object-fit:contain}
.nav{display:flex;align-items:center;gap:12px;padding:22px 0}
.brand{font-weight:700;font-size:20px;letter-spacing:-.03em;text-decoration:none;margin-right:auto;display:flex;align-items:center;gap:8px}
.brand .milo{width:26px;height:26px}
.pill{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:15px;padding:12px 22px;border-radius:0;border:1.5px solid var(--ink);text-decoration:none;transition:transform .15s}
.pill:hover{transform:translateY(-2px)}
.pill.solid{background:var(--lime);border-color:var(--lime)}
.hero{padding:clamp(30px,6vw,72px) 0 clamp(24px,4vw,48px)}
.kick{font-size:14px;font-weight:600;color:var(--gray);margin:0 0 16px}
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
.ch{border:1px solid var(--line);border-radius:0;padding:24px 26px;background:linear-gradient(180deg,rgba(255,255,255,.5),rgba(255,255,255,.15))}
.ch header{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:14px}
.ch .chn{font-size:13px;font-weight:600;color:var(--gray)}
.ch h3{font-size:22px;letter-spacing:-.02em;flex:1 1 auto}
.ch .chc{font-size:13px;color:var(--gray)}
.ch ul{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.ch li{font-size:15px;color:#242424}
.ch li a{color:inherit;text-decoration:none;border-bottom:1px solid var(--line)}
.ch li a:hover{border-color:var(--ink)}
.ch .lk{display:inline-block;min-width:34px;color:var(--gray);font-variant-numeric:tabular-nums}
.ch li.soon{color:var(--gray)}
.ch li.soon em{font-style:normal;font-size:12px;font-weight:600;padding:1px 8px;margin-left:4px;border-radius:0;background:var(--line);color:var(--ink);vertical-align:1px}
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
MILO='<img src="/paths/assets/spot/spot-happy.png" class="milo" alt="Milo">'
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
    SF=f"/landing?course={COURSE}&amp;start=1"  # valid-HTML start-free deep link
    # structured data
    ld_course={"@context":"https://schema.org","@type":"Course","name":CTITLE,"description":META["blurb"],
      "url":hub_url,"courseCode":COURSE,"educationalLevel":LEVEL,"inLanguage":"en",
      "teaches":[c["t"] for c in toc],
      "provider":{"@type":"Organization","name":"Quantica","url":BASE+"/"},
      "hasCourseInstance":{"@type":"CourseInstance","courseMode":"online","courseWorkload":META["workload"]},
      # Chapter 1 of every course is free and needs no card; everything past it is the paid
      # plan. Advertising price 0 for the whole course is what Google lifts into rich results,
      # so it has to match what the checkout actually charges.
      "offers":[{"@type":"Offer","price":"0","priceCurrency":"USD","name":"Chapter 1, free","category":"Free"},
                {"@type":"Offer","price":"14.99","priceCurrency":"USD","name":"Quantica Pro, monthly"}],
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
<meta name="twitter:description" content="{nchap} chapters, {nlesson} lessons. Learn by solving, with Milo. Free to start.">
<meta name="twitter:image" content="{BASE}/{OGIMG}">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">{json.dumps(ld_course)}</script>
<script type="application/ld+json">{json.dumps(ld_crumb)}</script>
<script type="application/ld+json">{json.dumps(ld_faq)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://api.fontshare.com"><link rel="preconnect" href="https://cdn.fontshare.com" crossorigin><link href="https://api.fontshare.com/v2/css?f%5B%5D=chillax@300,400,500,600,700&display=swap" rel="stylesheet">
<style>{HUB_CSS}</style></head>
<body>
<header class="wrap nav">
  <a class="brand" href="/">{MILO}Quantica</a>
  {crosshtml}
  <a class="pill" href="/">Home</a>
  <a class="pill solid" href="{SF}">Start free</a>
</header>
<main>
<section class="wrap hero">
  <h1><span class="mark">{H.escape(CTITLE)}</span></h1>
  <p class="lead">Learn {H.escape(CTITLE)} by <em>solving</em>, not memorizing. <span class="dim">{H.escape(META["lead"])}</span></p>
  <div class="cta">
    <a class="pill solid" href="{SF}">Start the course, free &rarr;</a>
    <a class="pill" href="#curriculum">See the curriculum</a>
  </div>
  <div class="stats">
    <div class="stat"><b>{nchap}</b><span>chapters</span></div>
    <div class="stat"><b>{nlesson}</b><span>lessons</span></div>
    <div class="stat"><b>Ch 1</b><span>free to start</span></div>
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
    <div class="step"><div class="n">02</div><h3>Guided, never spoiled</h3><p>Layered hints and Milo nudge you toward the answer without handing it over.</p></div>
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
  <a class="brand" href="/">{MILO}Quantica</a>
  <div><a href="/">Home</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div>
</footer>
</body></html>'''
    open(f"{ROOT}/{COURSE}.html","w",encoding="utf-8").write(page)

# Search-facing titles. The lesson name is what a textbook chapter is called; these are
# what a person actually types into Google. Each one still contains the topic term, so the
# page targets both.
# Hand-written meta descriptions. The auto-extracted fallback below describes the
# LESSON; these describe what a searcher gets, which is what earns the click.
# Add an entry whenever Search Console shows impressions with a poor click rate.
# Keep to about 150 characters, lead with the answer, then the thing the snippet
# cannot give them. Never promise something the page does not actually cover.
SEO_DESC = {
 "prealgebra": {
  # 146 impressions, 0 clicks. The old text was the lesson's opening sentence,
  # "Powers grow as the exponent climbs", which answers nothing and used half the
  # available length. Queries were "0 to the power of 0" and "any number to the
  # zero power", and the page does cover both, including why 0^0 is left undefined.
  "2.3":"Any nonzero number to the zero power is 1. See the two short reasons why, "
        "what makes 0 to the zero power the exception, and practice with full solutions.",
  # The key-idea fallback opened these on a sub-rule or ran too short, so they are
  # written by hand. Each leads with the answer and names the common mistake, which
  # is what the searcher is usually checking.
  "2.2":"Multiply powers with the same base and you add the exponents. All the exponent "
        "laws in one place, with the traps that break them and worked practice.",
  "2.5":"Raising a power to a power multiplies the exponents. The same rule extended to "
        "products and fractions, with the mistakes it is easy to make and full solutions.",
  "4.6":"Add fractions by giving them a common denominator first, never by adding the "
        "denominators. The three steps, why they work, and practice with full solutions.",
  "5.5":"Turn any repeating decimal into a fraction by shifting it and subtracting. Why "
        "decimals repeat at all, how to predict it from the denominator, and practice.",
  "12.4":"Undo a chain of operations in reverse order, and invert each step as you go. "
         "Worked examples of the two rules that make working backwards reliable.",
  "2.1":"A square is a number times itself and a cube is a number times itself twice. "
        "What the names mean, how the picture explains the shortcuts, and practice.",
 },
 "algebra1": {
  # the key-idea fallback ran short on these three
  "5.3":"Add or subtract two equations to make a variable disappear, then solve what is "
        "left. When to scale first, and worked practice with full solutions.",
  "7.6":"Two lines with the same slope are parallel or identical, and slopes multiplying "
        "to -1 mean perpendicular. The three ways a pair of lines can sit, drawn.",
  "8.1":"Every inequality rule follows from one idea, that a is greater than b means "
        "a minus b is positive. Including the one rule that reverses the sign.",
 },
}

SEO_TITLE = {
 "prealgebra": {
  "1.1":"Why Arithmetic Comes Before Algebra",
  "1.2":"How to Add and Subtract Negative Numbers",
  "1.3":"Why a Negative Times a Negative Is Positive",
  "1.4":"Arithmetic Practice Problems with Full Solutions",
  "1.5":"Division Rules and Why You Cannot Divide by Zero",
  "1.6":"The Rules of Arithmetic, Summarized",
  "2.1":"Squares and Cubes, and What They Really Mean",
  "2.2":"The Laws of Exponents and How to Use Them",
  "2.3":"Why Any Number to the Zero Power Equals 1",
  "2.4":"What a Negative Exponent Actually Means",
  "2.5":"How to Raise a Power to Another Power",
  "2.6":"Exponent Rules, Summarized",
  "3.1":"Factors and Multiples, and How They Differ",
  "3.2":"Divisibility Rules for 2, 3, 4, 5, 6, 9 and 10",
  "3.3":"How to Find the Prime Factorization of a Number",
  "3.5":"How to Find the GCD and LCM of Two Numbers",
  "3.6":"How to Count the Factors of a Number",
  "3.7":"Factors, Primes, GCD and LCM, Summarized",
  "4.1":"What a Fraction Actually Means",
  "4.2":"How to Find Equivalent Fractions",
  "4.3":"How to Multiply and Divide Fractions",
  "4.4":"How to Find a Common Denominator and Simplify",
  "4.6":"How to Add and Subtract Fractions",
  "4.7":"Mixed Numbers and Improper Fractions",
  "4.8":"How to Tell Which Fraction Is Bigger",
  "5.1":"Place Value and How Decimals Work",
  "5.2":"How to Add, Subtract, Multiply and Divide Decimals",
  "5.3":"How to Convert Between Fractions and Decimals",
  "5.4":"How to Round Numbers and Estimate Answers",
  "5.5":"How to Turn a Repeating Decimal into a Fraction",
  "6.1":"How to Write an Algebraic Expression",
  "6.2":"How to Solve a Linear Equation, Step by Step",
  "6.3":"How to Solve Equations with Variables on Both Sides",
  "6.4":"How to Turn a Word Problem into an Equation",
  "6.5":"How to Solve Inequalities and When to Flip the Sign",
  "7.1":"What a Ratio Is and How to Use One",
  "7.2":"How to Work with Ratios of Three or More Parts",
  "7.3":"How to Find a Unit Rate",
  "7.4":"How to Set Up and Solve a Proportion",
  "7.5":"How to Convert Units Using Ratios",
  "8.1":"What a Square Root Is",
  "8.2":"How to Estimate a Square Root Without a Calculator",
  "8.3":"How to Simplify a Square Root",
  "8.4":"How to Add, Multiply and Divide Square Roots",
  "9.1":"How to Convert a Percent to a Fraction",
  "9.2":"How to Find a Percent of a Number",
  "9.3":"How to Calculate Percent Increase and Decrease",
  "9.4":"How to Solve Percent Word Problems",
  "10.1":"How to Count by Adding and Subtracting Cases",
  "10.2":"The Multiplication Principle of Counting",
  "10.3":"How to Solve Counting Problems with Casework",
  "10.4":"How to Count Pairs and Handshakes",
  "10.5":"How to Find the Probability of an Event",
  "10.6":"How to Find the Mean, Median and Mode",
  "10.7":"How to Read Tables and Graphs",
  "10.8":"How Statistics Can Mislead You",
  "11.1":"How to Measure and Name Angles",
  "11.2":"Angles Made by Parallel Lines and a Transversal",
  "11.3":"How to Find the Sum of Angles in a Polygon",
  "11.4":"How to Work with Segment Lengths",
  "11.5":"How to Find the Perimeter of a Shape",
  "11.6":"How to Find the Area of Any Common Shape",
  "11.7":"How to Find the Area and Circumference of a Circle",
  "11.8":"How to Use the Pythagorean Theorem",
  "11.9":"30-60-90 and 45-45-90 Triangle Rules",
  "11.10":"The Types of Quadrilaterals and How They Relate",
  "12.1":"How to Solve Math Problems by Finding a Pattern",
  "12.2":"How to Solve Problems with an Organized List",
  "12.3":"How to Solve Math Problems by Drawing a Picture",
  "12.4":"How to Solve Math Problems by Working Backwards",
 },
 "algebra1": {
  "1.1":"Integers, Rationals and Real Numbers Explained",
  "1.2":"Order of Operations, PEMDAS Done Properly",
  "1.3":"When You Can Reorder Terms and When You Cannot",
  "1.4":"What an Algebraic Expression Is",
  "1.5":"Exponent Rules in Algebra",
  "1.6":"How to Evaluate an Algebraic Expression",
  "2.1":"How to Use the Distributive Property",
  "2.2":"How to Evaluate Expressions Quickly",
  "2.3":"How to Factor Out a Common Factor",
  "2.4":"How to Combine Like Terms",
  "2.5":"How to Simplify Fractions with Variables",
  "2.6":"How to Simplify Expressions with Many Variables",
  "3.1":"The Laws of Exponents with Variables",
 },
}

SEOQ = SEO_TITLE.get(COURSE, {})
SEOD = SEO_DESC.get(COURSE, {})

def clean_desc(raw, seo_title, fallback_raw=''):
    """A meta description Google can print. Whole sentences only, and never any math,
    because stripped LaTeX leaves debris like "marks 3 4 of the way out"."""
    x = re.sub(r'<svg.*?</svg>', '', raw or '', flags=re.S)
    x = H.unescape(re.sub(r'<[^>]+>', ' ', x))
    x = re.sub(r'\s+', ' ', x).strip()
    out = ''
    for sent in re.findall(r'[^.!?]+[.!?]', x):
        sent = sent.strip()
        # skip math, and skip fragments left behind when a sentence split inside a number
        if re.search(r'[\\$]', sent) or len(sent.split()) < 4 or not sent[:1].isupper():
            continue
        if len(out) + len(sent) + 1 > 155:
            break
        out = (out + ' ' + sent).strip()
    if len(out) < 60 and fallback_raw:
        return clean_desc(fallback_raw, seo_title)
    if len(out) < 60:
        out = f"{seo_title}. Worked examples with hints and full solutions on Quantica."
    return out

# ---- lesson pages ----
os.makedirs(ROOT+"/"+COURSE, exist_ok=True)
sitemap_urls=[f"{BASE}/{COURSE}"]
for idx,k in enumerate(ORDER):
    L=DATA[k]; title=L['title']; slug=SLUG[k]; chn,cht=CHOF[k]
    url=f"{BASE}/{COURSE}/{slug}"
    sitemap_urls.append(url)
    seo_title=SEOQ.get(k) or title
    imp=next((b.get('x','') for b in (L.get('blocks') or []) if b.get('t')=='imp'), '')
    desc=SEOD.get(k) or clean_desc(imp, seo_title, (L.get('blocks') or [{}])[0].get('x',''))
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
    body=render_full(L)
    page=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{GA}
<title>{H.escape(seo_title)} | Quantica</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Quantica">
<meta property="og:title" content="{H.escape(seo_title)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/{OGIMG}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}/{OGIMG}">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">{json.dumps(ld)}</script>
<script type="application/ld+json">{json.dumps(crumb)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://api.fontshare.com"><link rel="preconnect" href="https://cdn.fontshare.com" crossorigin><link href="https://api.fontshare.com/v2/css?f%5B%5D=chillax@300,400,500,600,700&display=swap" rel="stylesheet"><link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
{KATEX}
<style>{CSS}</style></head>
<body>
<header class="wrap nav"><a class="brand" href="/">{MILO}Quantica</a><a class="pill" href="/{COURSE}">{H.escape(CTITLE)}</a><a class="pill solid" href="/landing?course={COURSE}&amp;lesson={k}">Open in the course</a></header>
<div class="wrap">
  <nav class="crumbs"><a href="/">Home</a> › <a href="/{COURSE}">{H.escape(CTITLE)}</a> › Chapter {chn}: {H.escape(cht)}</nav>
  <div class="head"><p class="ey">{H.escape(CTITLE)} · Lesson {k}</p><h1>{H.escape(title)}</h1></div>
  <div class="startbar"><a class="pill solid" href="/landing?course={COURSE}&amp;lesson={k}">{"Solve this lesson, free &rarr;" if chn==1 else "Solve this lesson &rarr;"}</a><a class="pill" href="/{COURSE}">All lessons</a></div>
  <article class="content">
  {body}
  {gate_html(k)}
  </article>
  <nav class="pager">{pager_link(prev_k,"← Previous","prev")}{pager_link(next_k,"Next →","next")}</nav>
</div>
<footer class="wrap foot"><a class="brand" href="/">{MILO}Quantica</a><div><a href="/{COURSE}">{H.escape(CTITLE)}</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div></footer>
</body></html>'''
    open(f"{ROOT}/{COURSE}/{slug}.html","w",encoding="utf-8").write(page)

gen_hub()
json.dump(sitemap_urls, open(os.path.join(ROOT,"lessons",COURSE,"lesson_urls.json"),"w",encoding="utf-8"))
print(f"course={COURSE}: wrote {COURSE}.html (hub) + {len(ORDER)} lesson pages -> {COURSE}/*.html")
if ORDER: print("sample lesson:", ORDER[0], "->", "/"+COURSE+"/"+SLUG[ORDER[0]])
print("sitemap urls:", len(sitemap_urls), "(hub + lessons) written to lessons/%s/lesson_urls.json"%COURSE)
