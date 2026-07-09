# Build /prealgebra — a standalone, crawlable, SEO-optimized course page (wembi style).
import json, html as H
SCR="/private/tmp/claude-501/-Users-aayankhare-Claude-Projects-QuanticaEdu/020a3e6a-5784-4b7e-b4f9-89d3f3d809c0/scratchpad"
toc=json.load(open(SCR+"/toc.json"))
_SLUG=json.load(open(SCR+"/slugmap.json"))
BASE="https://quanticaedu.com"
GA='''<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}(function(){try{var h=location.hostname;if(h!=='quanticaedu.com'&&h!=='www.quanticaedu.com')return;if(location.search.indexOf('imfounder=1')>-1&&!localStorage.getItem('qa_internal')){localStorage.setItem('qa_internal','1');alert('Got it. Analytics is now off on this device.');}if(localStorage.getItem('qa_internal')==='1')return;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-98WQ2BFR6N';document.head.appendChild(s);gtag('js',new Date());gtag('config','G-98WQ2BFR6N',{allow_google_signals:false,allow_ad_personalization_signals:false});}catch(e){}})();</script>'''
URL=BASE+"/prealgebra"
# count only lessons that actually have a page (openable now), not planned/coming-soon
n_lessons=sum(1 for c in toc for l in c['lessons'] if l['k'] in _SLUG)
DESC=("Learn prealgebra online by solving real problems, not memorizing. Quantica's Prealgebra course covers "
      f"{len(toc)} chapters and {n_lessons} lessons — from arithmetic, exponents, and fractions to ratios, "
      "percents, and geometry — with instant feedback and Milo, a tutor that helps you find the answer yourself. Free to start.")

MILO='''<svg viewBox="0 0 64 64" class="milo" aria-hidden="true"><path d="M32 7 C46 7 51 12 51 32 C51 52 46 57 32 57 C18 57 13 52 13 32 C13 12 18 7 32 7Z" fill="#beff8b"/><circle cx="25.5" cy="30" r="4.4" fill="#9dbbc5"/><circle cx="38.5" cy="30" r="4.4" fill="#9dbbc5"/><circle cx="25.5" cy="30" r="2.1" fill="#0a0a0a"/><circle cx="38.5" cy="30" r="2.1" fill="#0a0a0a"/><path d="M26 38 Q32 43.5 38 38" fill="none" stroke="#0a0a0a" stroke-width="2.2" stroke-linecap="round"/></svg>'''

# --- structured data ---
course_ld={
 "@context":"https://schema.org","@type":"Course","name":"Prealgebra",
 "description":DESC,"url":URL,"courseCode":"prealgebra","educationalLevel":"Middle school / Prealgebra",
 "inLanguage":"en","teaches":[c['t'] for c in toc],
 "provider":{"@type":"Organization","name":"Quantica","url":BASE+"/"},
 "hasCourseInstance":{"@type":"CourseInstance","courseMode":"online","courseWorkload":"P12W"},
 "offers":{"@type":"Offer","price":"0","priceCurrency":"USD","category":"Free trial"},
 "hasPart":[{"@type":"Syllabus","name":f"Chapter {c['n']}: {c['t']}","description":", ".join(l['t'] for l in c['lessons'])} for c in toc]
}
crumb_ld={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {"@type":"ListItem","position":1,"name":"Quantica","item":BASE+"/"},
 {"@type":"ListItem","position":2,"name":"Prealgebra","item":URL}]}
faqs=[
 ("Is the Prealgebra course free?","Yes — you can start the full Prealgebra course for free, no card required."),
 ("Do I need any prior math knowledge?","No. Prealgebra starts from the rules of arithmetic and builds up, and Milo is there whenever a problem stops you."),
 ("How is Quantica different from other prealgebra courses?","You learn by solving real problems with instant feedback and layered hints, so the ideas emerge from your own work instead of being memorized."),
 ("How long is the Prealgebra course?",f"It has {len(toc)} chapters and {n_lessons} lessons. You move at your own pace, in any order."),
]
faq_ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
 {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}

def chapters_html():
    out=[]
    for c in toc:
        items=[]; avail=0
        for l in c['lessons']:
            k=l['k']; ti=H.escape(l['t'])
            if k in _SLUG:
                avail+=1
                items.append(f'<li><span class="lk">{k}</span> <a href="/prealgebra/{_SLUG[k]}">{ti}</a></li>')
            else:
                items.append(f'<li class="soon"><span class="lk">{k}</span> {ti} <em>Soon</em></li>')
        chc = (f"{avail} lesson" if avail==1 else f"{avail} lessons") if avail else "Coming soon"
        out.append(f'''<article class="ch">
      <header><span class="chn">Chapter {c['n']}</span><h3>{H.escape(c['t'])}</h3><span class="chc">{chc}</span></header>
      <ul>{"".join(items)}</ul>
    </article>''')
    return "\n    ".join(out)

def faq_html():
    return "\n    ".join(f'<details><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q,a in faqs)

page=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{GA}
<title>Prealgebra Course — Learn Prealgebra by Solving | Quantica</title>
<meta name="description" content="{H.escape(DESC)}">
<link rel="canonical" href="{URL}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Quantica">
<meta property="og:title" content="Prealgebra Course — Learn Prealgebra by Solving">
<meta property="og:description" content="{H.escape(DESC)}">
<meta property="og:url" content="{URL}">
<meta property="og:image" content="{BASE}/og-prealgebra.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Prealgebra Course — Learn Prealgebra by Solving | Quantica">
<meta name="twitter:description" content="{len(toc)} chapters, {n_lessons} lessons. Learn by solving, with Milo. Free to start.">
<meta name="twitter:image" content="{BASE}/og-prealgebra.png">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">{json.dumps(course_ld)}</script>
<script type="application/ld+json">{json.dumps(crumb_ld)}</script>
<script type="application/ld+json">{json.dumps(faq_ld)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#ededeb;--ink:#0a0a0a;--lime:#beff8b;--slate:#9dbbc5;--gray:#5c5c58;--line:rgba(10,10,10,.12)}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Space Grotesk',system-ui,sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}}
a{{color:inherit}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 clamp(20px,4vw,56px)}}
h1,h2,h3{{margin:0;font-weight:700;letter-spacing:-.03em;line-height:1}}
.mark{{background:var(--lime);border-radius:.16em;padding:.02em .2em}}
.milo{{width:1em;height:1em;vertical-align:-.18em}}
.nav{{display:flex;align-items:center;gap:12px;padding:22px 0}}
.brand{{font-weight:700;font-size:20px;letter-spacing:-.03em;text-decoration:none;margin-right:auto;display:flex;align-items:center;gap:8px}}
.brand .milo{{width:26px;height:26px}}
.pill{{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:15px;padding:12px 22px;border-radius:999px;border:1.5px solid var(--ink);text-decoration:none;transition:transform .15s}}
.pill:hover{{transform:translateY(-2px)}}
.pill.solid{{background:var(--lime);border-color:var(--lime)}}
.hero{{padding:clamp(30px,6vw,72px) 0 clamp(24px,4vw,48px)}}
.kick{{font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gray);margin:0 0 16px}}
.hero h1{{font-size:clamp(48px,9vw,110px);letter-spacing:-.04em}}
.hero .lead{{font-size:clamp(17px,1.6vw,21px);max-width:60ch;margin:24px 0 0;color:var(--ink)}}
.hero .lead .dim{{color:var(--gray)}}
.cta{{display:flex;gap:12px;flex-wrap:wrap;margin-top:32px}}
.stats{{display:flex;gap:32px;flex-wrap:wrap;margin-top:34px;border-top:1px solid var(--line);padding-top:26px}}
.stat b{{display:block;font-size:32px;letter-spacing:-.03em}}
.stat span{{color:var(--gray);font-size:14px}}
section{{padding:clamp(40px,7vw,90px) 0}}
.sec-h{{font-size:clamp(30px,5vw,56px);letter-spacing:-.035em;max-width:18ch}}
.sec-sub{{color:var(--gray);max-width:60ch;margin:18px 0 0;font-size:17px}}
.chs{{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:40px}}
.ch{{border:1px solid var(--line);border-radius:20px;padding:24px 26px;background:linear-gradient(180deg,rgba(255,255,255,.5),rgba(255,255,255,.15))}}
.ch header{{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:14px}}
.ch .chn{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--gray)}}
.ch h3{{font-size:22px;letter-spacing:-.02em;flex:1 1 auto}}
.ch .chc{{font-size:13px;color:var(--gray)}}
.ch ul{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}
.ch li{{font-size:15px;color:#242424}}
.ch li a{{color:inherit;text-decoration:none;border-bottom:1px solid var(--line)}}
.ch li a:hover{{border-color:var(--ink)}}
.ch .lk{{display:inline-block;min-width:34px;color:var(--gray);font-variant-numeric:tabular-nums}}
.ch li.soon{{color:var(--gray)}}
.ch li.soon em{{font-style:normal;font-size:10px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;padding:1px 6px;margin-left:4px;border-radius:999px;background:var(--line);color:var(--ink);vertical-align:1px}}
.how{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:40px}}
.how .step .n{{font-size:40px;font-weight:700;letter-spacing:-.03em}}
.how .step h3{{font-size:20px;margin:8px 0 6px}}
.how .step p{{color:var(--gray);font-size:15px;margin:0}}
.faq{{max-width:760px}}
details{{border-top:1px solid var(--line);padding:20px 0}}
details:last-child{{border-bottom:1px solid var(--line)}}
summary{{list-style:none;cursor:pointer;font-weight:600;font-size:19px;letter-spacing:-.02em;display:flex;justify-content:space-between}}
summary::-webkit-details-marker{{display:none}}
summary::after{{content:"+";color:var(--gray);font-weight:400;font-size:24px}}
details[open] summary::after{{content:"\\2013"}}
details p{{color:var(--gray);margin:14px 0 0}}
.cta-band{{text-align:center;padding:clamp(48px,8vw,110px) 0}}
.cta-band h2{{font-size:clamp(34px,6vw,72px);letter-spacing:-.04em}}
.foot{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center;border-top:1px solid var(--ink);padding:34px 0;font-size:14px}}
.foot a{{text-decoration:none;margin-left:18px}}
@media(max-width:760px){{.chs,.how{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<header class="wrap nav">
  <a class="brand" href="/">{MILO}Quantica</a>
  <a class="pill" href="/blog">Blog</a>
  <a class="pill" href="/">Home</a>
  <a class="pill solid" href="/?start=1">Start free</a>
</header>

<main>
<section class="wrap hero">
  <p class="kick">Quantica · Course</p>
  <h1><span class="mark">Prealgebra</span></h1>
  <p class="lead">Learn prealgebra by <em>solving</em>, not memorizing. <span class="dim">Work real problems with instant feedback and Milo, a tutor that helps you find the answer yourself.</span></p>
  <div class="cta">
    <a class="pill solid" href="/?start=1">Start the course — free →</a>
    <a class="pill" href="#curriculum">See the curriculum</a>
  </div>
  <div class="stats">
    <div class="stat"><b>{len(toc)}</b><span>chapters</span></div>
    <div class="stat"><b>{n_lessons}</b><span>lessons</span></div>
    <div class="stat"><b>$0</b><span>to start</span></div>
  </div>
</section>

<section class="wrap" id="curriculum">
  <h2 class="sec-h">What you'll <span class="mark">learn</span></h2>
  <p class="sec-sub">The full Prealgebra path, from the rules of arithmetic to a problem-solving toolkit. Every lesson is a problem to crack, not a worksheet to grind.</p>
  <div class="chs">
    {chapters_html()}
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
  <div style="margin-top:30px">
    {faq_html()}
  </div>
</section>

<section class="wrap cta-band">
  <h2>Start <span class="mark">solving</span>.</h2>
  <div class="cta" style="justify-content:center;margin-top:30px"><a class="pill solid" href="/?start=1">Start Prealgebra — free →</a></div>
</section>
</main>

<footer class="wrap foot">
  <a class="brand" href="/">{MILO}Quantica</a>
  <div><a href="/">Home</a><a href="/blog">Blog</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div>
</footer>
</body>
</html>'''

open("/Users/aayankhare/Claude/Projects/QuanticaEdu/prealgebra.html","w",encoding="utf-8").write(page)
print("wrote prealgebra.html:", len(page), "chars |", len(toc), "chapters,", n_lessons, "lessons")
