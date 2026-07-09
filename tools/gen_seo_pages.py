# Generate a static, crawlable SEO page per prealgebra lesson at /prealgebra/<slug>.
# Real teaching content + practice problems (KaTeX-rendered), prev/next links, structured data,
# and an "Open in the course" CTA that deep-launches gotoLesson(key) in the app.
import json, re, html as H, os, sys

# Regenerate the static, crawlable SEO page per lesson under /<course>/<slug>.html.
# Ported from the prior session's scratchpad gen_lessons.py to repo-relative paths.
# Usage: python3 tools/gen_seo_pages.py [course]   (default: prealgebra)
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE=sys.argv[1] if len(sys.argv)>1 else "prealgebra"
BASE="https://quanticaedu.com"
GA='''<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}(function(){try{var h=location.hostname;if(h!=='quanticaedu.com'&&h!=='www.quanticaedu.com')return;if(location.search.indexOf('imfounder=1')>-1&&!localStorage.getItem('qa_internal')){localStorage.setItem('qa_internal','1');alert('Got it. Analytics is now off on this device.');}if(localStorage.getItem('qa_internal')==='1')return;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-98WQ2BFR6N';document.head.appendChild(s);gtag('js',new Date());gtag('config','G-98WQ2BFR6N',{allow_google_signals:false,allow_ad_personalization_signals:false});}catch(e){}})();</script>'''
toc=json.load(open(os.path.join(ROOT,"lessons",COURSE,"toc.json")))
s=open(ROOT+"/data/lessons.js").read()
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
json.dump({k:SLUG[k] for k in ORDER}, open(os.path.join(ROOT,"lessons",COURSE,"slugmap.json"),"w"), indent=1)

def strip_text(x):
    x=re.sub(r'<svg.*?</svg>','',x,flags=re.S)
    x=re.sub(r'\$\$?.*?\$\$?',' ',x)                 # drop math for the plain-text summary
    x=re.sub(r'\\\(|\\\)','',x); x=re.sub(r'<[^>]+>',' ',x)
    x=H.unescape(x); return re.sub(r'\s+',' ',x).strip()

def render_blocks(L):
    out=[]
    if 'html' in L:
        return L['html']
    for b in L.get('blocks',[]):
        t=b.get('t'); x=b.get('x') or ''
        if t=='p':    out.append(f'<p>{x}</p>')
        elif t=='imp':out.append(f'<aside class="key"><span class="tag">Key idea</span><div>{x}</div></aside>')
        elif t=='fact':out.append(f'<aside class="fact"><span class="tag">{H.escape(b.get("label") or "Fun fact")}</span><div>{x}</div></aside>')
        elif t=='prob':
            sol=b.get('sol') or ''
            solblock=f'<details class="sol"><summary>Show solution</summary><div>{sol}</div></details>' if sol else ''
            out.append(f'<div class="prob"><div class="prob-q">{x}</div>{solblock}</div>')
    return "\n".join(out)

def html_intro(html):
    ends=[m.end() for m in re.finditer('</p>', html)]
    if len(ends)>=2: return html[:ends[1]]
    if ends: return html[:ends[0]]
    return html[:700]

def _wc(x):
    return len(re.sub('<[^>]+>',' ',re.sub(r'<svg.*?</svg>','',x,flags=re.S)).split())

def render_intro(L):
    # The lesson's opening only (a real intro, ~90+ words for SEO) — problem PROMPTS shown but no
    # solutions and no full dump. The worked problems, hints, and Milo live in the app.
    if 'html' in L:
        h=html_intro(L['html'])
        if _wc(h)<70:
            ends=[m.end() for m in re.finditer('</p>', L['html'])]
            if len(ends)>=3: h=L['html'][:ends[2]]
        return h
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
            '<p>The rest of this lesson &mdash; the worked problems, layered hints, and Milo right beside you &mdash; happens inside the course. Free to start.</p>'
            f'<a class="pill solid big" href="/?lesson={k}">Start this lesson &mdash; free &rarr;</a></div></aside>')

def review_html(L):
    r=L.get('review') or []
    if not r: return ''
    items=[]
    for i,p in enumerate(r,1):
        x=p.get('x') or ''; sol=p.get('sol') or ''
        sb=f'<details class="sol"><summary>Show solution</summary><div>{sol}</div></details>' if sol else ''
        items.append(f'<div class="prob"><div class="prob-q"><b>Review {i}.</b> {x}</div>{sb}</div>')
    return '<h2 class="sec-h">Review <span class="mark">problems</span></h2>\n'+"\n".join(items)

CSS='''
:root{--bg:#ededeb;--ink:#0a0a0a;--lime:#beff8b;--slate:#9dbbc5;--gray:#5c5c58;--line:rgba(10,10,10,.12)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:'Space Grotesk',system-ui,sans-serif;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit}img,svg{max-width:100%}
.wrap{max-width:820px;margin:0 auto;padding:0 clamp(20px,4vw,40px)}
h1,h2,h3{font-weight:700;letter-spacing:-.03em;line-height:1.05;margin:0}
.mark{background:var(--lime);border-radius:.16em;padding:.02em .2em}
.milo{width:1em;height:1em;vertical-align:-.18em}
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
.key{background:linear-gradient(180deg,rgba(190,255,139,.5),rgba(190,255,139,.22));border:1px solid rgba(10,10,10,.14);border-radius:16px;padding:20px 22px;margin:24px 0}
.fact{background:rgba(157,187,197,.22);border-left:3px solid var(--slate);border-radius:0 12px 12px 0;padding:16px 20px;margin:24px 0}
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
.gate{margin:6px 0 18px;border:1.5px solid var(--ink);border-radius:24px;background:linear-gradient(180deg,rgba(190,255,139,.42),rgba(190,255,139,.15));padding:clamp(30px,5vw,50px) clamp(22px,4vw,40px);text-align:center}
.gate-in{max-width:44ch;margin:0 auto}
.milo-big{width:58px;height:58px;margin:0 auto 12px;display:block}
.gate h2{font-size:clamp(26px,4.6vw,42px);letter-spacing:-.03em;margin:0 0 14px}
.gate p{font-size:17px;color:#242424;margin:0 0 26px}
.pill.big{padding:15px 30px;font-size:16px}
@media(max-width:560px){.pager{grid-template-columns:1fr}.pager a.next{text-align:left}}
'''
MILO='<svg viewBox="0 0 64 64" class="milo" aria-hidden="true"><path d="M32 7 C46 7 51 12 51 32 C51 52 46 57 32 57 C18 57 13 52 13 32 C13 12 18 7 32 7Z" fill="#beff8b"/><circle cx="25.5" cy="30" r="4.4" fill="#9dbbc5"/><circle cx="38.5" cy="30" r="4.4" fill="#9dbbc5"/><circle cx="25.5" cy="30" r="2.1" fill="#0a0a0a"/><circle cx="38.5" cy="30" r="2.1" fill="#0a0a0a"/><path d="M26 38 Q32 43.5 38 38" fill="none" stroke="#0a0a0a" stroke-width="2.2" stroke-linecap="round"/></svg>'
MILO_BIG=MILO.replace('class="milo"','class="milo-big"')
KATEX='''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>document.addEventListener("DOMContentLoaded",function(){renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"\\\\[",right:"\\\\]",display:true},{left:"\\\\(",right:"\\\\)",display:false},{left:"$",right:"$",display:false}],throwOnError:false});});</script>'''

os.makedirs(ROOT+"/prealgebra", exist_ok=True)
sitemap_urls=[]
for idx,k in enumerate(ORDER):
    L=DATA[k]; title=L['title']; slug=SLUG[k]; chn,cht=CHOF[k]
    url=f"{BASE}/prealgebra/{slug}"
    sitemap_urls.append(url)
    desc=strip_text((L.get('blocks') or [{}])[0].get('x','') if 'blocks' in L else L.get('html',''))[:155] or f"{title} — a prealgebra lesson from Quantica."
    desc=f"{title}: {desc}"[:158]
    prev_k=ORDER[idx-1] if idx>0 else None
    next_k=ORDER[idx+1] if idx<len(ORDER)-1 else None
    def pager_link(kk,dir_,cls):
        if not kk: return '<span></span>'
        return f'<a class="{cls}" href="/prealgebra/{SLUG[kk]}"><span class="dir">{dir_}</span><div class="t">{H.escape(DATA[kk]["title"])}</div></a>'
    ld={"@context":"https://schema.org","@type":"LearningResource","name":title,"url":url,
        "description":desc,"inLanguage":"en","learningResourceType":"lesson",
        "educationalLevel":"Prealgebra","isPartOf":{"@type":"Course","name":"Prealgebra","url":BASE+"/prealgebra"},
        "provider":{"@type":"Organization","name":"Quantica","url":BASE+"/"}}
    crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Quantica","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":"Prealgebra","item":BASE+"/prealgebra"},
        {"@type":"ListItem","position":3,"name":title,"item":url}]}
    body=render_intro(L)
    page=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{GA}
<title>{H.escape(title)} — Prealgebra | Quantica</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Quantica">
<meta property="og:title" content="{H.escape(title)} — Prealgebra">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/og-prealgebra.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}/og-prealgebra.png">
<link rel="icon" href="/favicon.svg">
<script type="application/ld+json">{json.dumps(ld)}</script>
<script type="application/ld+json">{json.dumps(crumb)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
{KATEX}
<style>{CSS}</style></head>
<body>
<header class="wrap nav"><a class="brand" href="/">{MILO}Quantica</a><a class="pill" href="/prealgebra">Prealgebra</a><a class="pill solid" href="/?lesson={k}">Open in the course</a></header>
<div class="wrap">
  <nav class="crumbs"><a href="/">Home</a> › <a href="/prealgebra">Prealgebra</a> › Chapter {chn}: {H.escape(cht)}</nav>
  <div class="head"><p class="ey">Prealgebra · Lesson {k}</p><h1>{H.escape(title)}</h1></div>
  <div class="startbar"><a class="pill solid" href="/?lesson={k}">Solve this lesson — free →</a><a class="pill" href="/prealgebra">All lessons</a></div>
  <article class="content">
  {body}
  {gate_html(k)}
  </article>
  <nav class="pager">{pager_link(prev_k,"← Previous","prev")}{pager_link(next_k,"Next →","next")}</nav>
</div>
<footer class="wrap foot"><a class="brand" href="/">{MILO}Quantica</a><div><a href="/prealgebra">Prealgebra</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div></footer>
</body></html>'''
    open(f"{ROOT}/prealgebra/{slug}.html","w",encoding="utf-8").write(page)

json.dump(sitemap_urls, open(os.path.join(ROOT,"lessons",COURSE,"lesson_urls.json"),"w"))
print(f"generated {len(ORDER)} lesson pages -> <course>/*.html")
print("sample:", ORDER[0], "->", "/"+COURSE+"/"+SLUG[ORDER[0]])
