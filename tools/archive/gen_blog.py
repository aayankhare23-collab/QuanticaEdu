# Build the Quantica blog: a crawlable /blog index + one article page per post.
# Same wembi theme + SEO rigor as gen_prealgebra.py. Add future posts to POSTS.
import json, html as H, re
ROOT="/Users/aayankhare/Claude/Projects/QuanticaEdu"
BASE="https://quanticaedu.com"
GA='''<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}(function(){try{var h=location.hostname;if(h!=='quanticaedu.com'&&h!=='www.quanticaedu.com')return;if(location.search.indexOf('imfounder=1')>-1&&!localStorage.getItem('qa_internal')){localStorage.setItem('qa_internal','1');alert('Got it. Analytics is now off on this device.');}if(localStorage.getItem('qa_internal')==='1')return;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-98WQ2BFR6N';document.head.appendChild(s);gtag('js',new Date());gtag('config','G-98WQ2BFR6N',{allow_google_signals:false,allow_ad_personalization_signals:false});}catch(e){}})();</script>'''
ORG={"@type":"Organization","name":"Quantica","url":BASE+"/",
     "logo":{"@type":"ImageObject","url":BASE+"/favicon.svg"}}

MILO='''<svg viewBox="0 0 64 64" class="milo" aria-hidden="true"><path d="M32 7 C46 7 51 12 51 32 C51 52 46 57 32 57 C18 57 13 52 13 32 C13 12 18 7 32 7Z" fill="#beff8b"/><circle cx="25.5" cy="30" r="4.4" fill="#9dbbc5"/><circle cx="38.5" cy="30" r="4.4" fill="#9dbbc5"/><circle cx="25.5" cy="30" r="2.1" fill="#0a0a0a"/><circle cx="38.5" cy="30" r="2.1" fill="#0a0a0a"/><path d="M26 38 Q32 43.5 38 38" fill="none" stroke="#0a0a0a" stroke-width="2.2" stroke-linecap="round"/></svg>'''

# ---- shared <head> css (wembi base from prealgebra.html + article prose) ----
CSS = r'''
:root{--bg:#ededeb;--ink:#0a0a0a;--lime:#beff8b;--slate:#9dbbc5;--gray:#5c5c58;--line:rgba(10,10,10,.12)}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Space Grotesk',system-ui,sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:0 clamp(20px,4vw,56px)}
h1,h2,h3{margin:0;font-weight:700;letter-spacing:-.03em;line-height:1}
.mark{background:var(--lime);border-radius:.16em;padding:.02em .2em}
.milo{width:1em;height:1em;vertical-align:-.18em}
.nav{display:flex;align-items:center;gap:12px;padding:22px 0}
.brand{font-weight:700;font-size:20px;letter-spacing:-.03em;text-decoration:none;margin-right:auto;display:flex;align-items:center;gap:8px}
.brand .milo{width:26px;height:26px}
.pill{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:15px;padding:12px 22px;border-radius:999px;border:1.5px solid var(--ink);text-decoration:none;transition:transform .15s}
.pill:hover{transform:translateY(-2px)}
.pill.solid{background:var(--lime);border-color:var(--lime)}
section{padding:clamp(40px,7vw,90px) 0}
.kick{font-size:12px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gray);margin:0 0 16px}
.crumbs{font-size:13px;color:var(--gray);padding:26px 0 0;display:flex;gap:8px;flex-wrap:wrap}
.crumbs a{text-decoration:none;border-bottom:1px solid var(--line)}
.crumbs a:hover{border-color:var(--ink)}
.crumbs span{color:var(--gray)}
.foot{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center;border-top:1px solid var(--ink);padding:34px 0;font-size:14px;margin-top:40px}
.foot a{text-decoration:none;margin-left:18px;display:inline-block;padding:11px 0}
.cta-band{text-align:center;padding:clamp(44px,7vw,96px) 0}
.cta-band h2{font-size:clamp(30px,5vw,60px);letter-spacing:-.04em}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:32px}
/* ---- blog index ---- */
.bloghero{padding:clamp(28px,5vw,60px) 0 clamp(18px,3vw,34px)}
.bloghero h1{font-size:clamp(42px,8vw,92px);letter-spacing:-.04em}
.bloghero .lead{font-size:clamp(17px,1.6vw,21px);max-width:56ch;margin:22px 0 0;color:var(--gray)}
.posts{display:grid;gap:20px;margin:8px 0 0}
.postcard{display:block;text-decoration:none;border:1px solid var(--line);border-radius:22px;padding:clamp(24px,3vw,38px);background:linear-gradient(180deg,rgba(255,255,255,.5),rgba(255,255,255,.14));transition:transform .15s,border-color .15s}
.postcard:hover{transform:translateY(-3px);border-color:var(--ink)}
.postcard .meta{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--gray);display:flex;gap:12px;flex-wrap:wrap}
.postcard h2{font-size:clamp(24px,3.4vw,38px);letter-spacing:-.03em;margin:14px 0 0;line-height:1.06}
.postcard p{color:var(--gray);font-size:17px;margin:14px 0 0;max-width:64ch}
.postcard .more{display:inline-block;margin-top:18px;font-weight:600;border-bottom:2px solid var(--lime)}
/* ---- article ---- */
.post{max-width:720px;margin:0 auto}
.post-head{padding:14px 0 clamp(20px,3vw,34px)}
.post-head h1{font-size:clamp(34px,6vw,62px);letter-spacing:-.035em;line-height:1.03;margin:16px 0 0}
.byline{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:26px 0 0;font-size:15px;color:var(--gray)}
.byline .who{font-weight:600;color:var(--ink)}
.byline .dot{width:4px;height:4px;border-radius:50%;background:var(--gray);display:inline-block}
.post-body{font-size:18px;line-height:1.75;color:#1a1a1a}
.post-body p{margin:22px 0}
.post-body .lede{font-size:21px;line-height:1.6;color:var(--ink)}
.post-body h2{font-size:clamp(25px,3.4vw,34px);letter-spacing:-.02em;line-height:1.12;color:var(--ink);margin:52px 0 2px}
.post-body ul{list-style:none;margin:24px 0;padding:0;display:grid;gap:16px}
.post-body li{position:relative;padding-left:26px}
.post-body li::before{content:"";position:absolute;left:0;top:11px;width:11px;height:11px;border-radius:3px;background:var(--lime);border:1px solid rgba(10,10,10,.35)}
.post-body li strong{font-weight:700;color:var(--ink)}
.post-body em{font-style:italic}
.endnote{margin-top:44px;border-top:1px solid var(--line);padding-top:28px;display:flex;gap:16px;align-items:flex-start}
.endnote .m{flex:0 0 auto;width:44px;height:44px}
.endnote p{margin:0;color:var(--gray);font-size:16px}
.endnote a{font-weight:600;border-bottom:2px solid var(--lime);text-decoration:none;color:var(--ink)}
@media(max-width:760px){.post-body{font-size:17px}.post-body .lede{font-size:19px}}
'''

def nav_html():
    return f'''<header class="wrap nav">
  <a class="brand" href="/">{MILO}Quantica</a>
  <a class="pill" href="/blog">Blog</a>
  <a class="pill" href="/prealgebra">Course</a>
  <a class="pill solid" href="/?start=1">Start free</a>
</header>'''

def foot_html():
    return f'''<footer class="wrap foot">
  <a class="brand" href="/">{MILO}Quantica</a>
  <div><a href="/">Home</a><a href="/blog">Blog</a><a href="/prealgebra">Course</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div>
</footer>'''

# =====================================================================
#  POST CONTENT
#  body blocks: ("lede",html) ("p",html) ("h2",text) ("ul",[html,...])
# =====================================================================
POSTS=[{
 "slug":"watching-your-child-struggle-with-math",
 "title":"Why Watching Your Child Struggle with Math Is Actually a Good Thing",
 "seo_title":"Why Your Child's Math Struggle Is a Good Thing | Quantica",
 "desc":("Why letting your child wrestle with a hard math problem, instead of rescuing them, "
         "builds the persistence and growth mindset that lasts beyond the worksheet."),
 "author":"Aayan Khare",
 "date":"2026-07-04","date_h":"July 4, 2026",
 "read":"6 min read",
 "kw":"productive struggle, growth mindset, math for kids, how children learn math, "
      "Carol Dweck mindset, parenting math, learning by solving, math confidence",
 "excerpt":("There's a concept in math education called productive struggle, and understanding it "
            "might be the most useful thing you can do for your child's long-term success in math."),
 "body":[
  ("lede","In my freshman year of high school, I was introduced to math contests. I stared blankly at the problems in front of me as I wondered how anyone my age was able to solve them. The concept of mathematical competition was so daunting to me that my strategy for the next year was to try a problem for two minutes, deem it impossible, then try my best to internalize the solution. While I got some beginner gains with this strategy, I didn&rsquo;t really learn how to solve the problems I hadn&rsquo;t seen before. The whole point of math contests is to be challenged with unseen, nonfamiliar problems. In fact, looking at solutions and internalizing them is one of the best ways to learn the concept, but not the best way to learn how to think. Over the next year, I plateaued in my ability. I realized that I had been learning the wrong way the entire time. I decided to challenge my attention span, and to really struggle with a problem for at least an hour. While the process was that much more painful, it proved to be that much more rewarding. Within 6 months, my ability nearly doubled."),
  ("p","There&rsquo;s a concept in math education called <em>productive struggle</em>, and understanding it might be the most useful thing you can do for your child&rsquo;s long-term success in the subject."),
  ("h2","What Is Productive Struggle?"),
  ("p","It is important to first note that being completely lost or confused is not the same as productive struggle. In that case, it is a ruthless unproductive struggle. The real productive struggle happens when your child approaches a problem they haven&rsquo;t seen with the skills they have already acquired. It is like solving a puzzle: you may have the tools to solve it, but finding the pathway to the solution is a game of struggle."),
  ("p","It is similar to building a muscle: when you don&rsquo;t perform a &ldquo;progressive overload&rdquo; in the gym and simply perform at the same intensity, you stay at a maintenance phase, where you aren&rsquo;t growing, but you aren&rsquo;t atrophying either."),
  ("p","The opposite, often known as <em>rescue math</em>, is when a parent, teacher, or older sibling jumps in at the first sign of difficulty and shows the child exactly what to do. The child gets the right answer, but they didn&rsquo;t really find it themselves. Their brain didn&rsquo;t have to stretch. It doesn&rsquo;t have to progressive overload. You are effectively stripping them of the most important experience in enriching their mathematical education."),
  ("h2","Why It Matters More Than Getting the Right Answer"),
  ("p","Research has repeatedly shown that the technique a child develops to get to their answers matters far more than whether or not they got the answer right."),
  ("p","When students work through a difficult problem on their own, they build several skills that go far beyond the specific math problem in front of them:"),
  ("ul",[
    "<strong>Persistence.</strong> Learning that effort eventually pays off develops a tolerance for difficulty. You are much less likely to give up when something is hard.",
    "<strong>Flexibility.</strong> Struggling with a problem forces kids to try different approaches. They learn that there&rsquo;s often more than one path to a solution, which is one of the most important mathematical insights they can develop. The solutions I came up with are often different from the &ldquo;median&rdquo; solution I would find online.",
    "<strong>Metacognition.</strong> When a child has to figure something out for themselves, they start paying attention to how they think. This is when I think that learning from a solution is really effective. If you ask yourself &ldquo;How could I have arrived at that solution myself,&rdquo; and reverse engineer the idea into your own cognitive thought process, you will learn extremely fast.",
  ]),
  ("h2","The Role of a &ldquo;Fixed&rdquo; vs. &ldquo;Growth&rdquo; Mindset"),
  ("p","Psychologist Carol Dweck&rsquo;s research on mindset is directly relevant here. Children with a <em>fixed</em> mindset believe their math ability is something they either have or don&rsquo;t, so when something is hard, it feels like confirmation that they&rsquo;re &ldquo;not a math person.&rdquo; They shut down. Unfortunately, this is the case for many children."),
  ("p","Children with a <em>growth</em> mindset believe ability is built through effort. For them, difficulty isn&rsquo;t a signal to stop, it&rsquo;s a sign they&rsquo;re learning something new."),
  ("p","Productive struggle is one of the most powerful ways to build a growth mindset. Every time a child works through something hard and comes out the other side, they add to their self-fulfilling prophecy that effort does in fact pay off. Over time, this fundamentally changes how they relate to challenges. They grow accustomed to challenges, through which a growth mindset is absolutely necessary."),
  ("h2","What You Can Do as a Parent"),
  ("p","None of this means you should leave your child completely on their own when they&rsquo;re frustrated. The goal is to support without rescuing. Here&rsquo;s how:"),
  ("ul",[
    "<strong>Normalize the struggle.</strong> Make them believe that struggling is a natural part of the process, because it is! When they believe that their struggle is normal, and not a result of being bad or unlucky, then they are much more likely to find their efforts productive, and as a result, put in more effort.",
    "<strong>Ask questions instead of giving answers.</strong> Instead of showing them how to solve the problem, ask: What do you already know about this? What have you tried? What would happen if&hellip;? These questions prompt thinking without doing the thinking for them.",
    "<strong>Celebrate effort, not just results.</strong> When you praise your child, focus on what they did, &ldquo;I saw you try three different ways before you got that,&rdquo; rather than how smart they are. This reinforces the idea that process matters.",
    "<strong>Let them sit with it.</strong> It can feel cruel to watch a child be frustrated, but discomfort isn&rsquo;t the same as harm. Give them time. You might be surprised how often they work through it on their own if you don&rsquo;t intervene immediately.",
    "<strong>Know when it&rsquo;s no longer productive.</strong> There&rsquo;s a tipping point where struggle becomes unproductive, when a child is so lost they have no foothold to make progress. At that point, stepping in with a nudge (not the full answer) is the right call. The goal is to get them back to a place where they can struggle productively again.",
  ]),
  ("p","At Quantica, our educational philosophy is exactly this. We emphasize the productivity of struggle and a growth mindset."),
  ("h2","The Long Game"),
  ("p","Math is cumulative. The habits your child builds now, whether they push through difficulty or look for a shortcut, will follow them through their years of schooling and in life. Children who learn to embrace struggle tend to be better prepared for advanced math, standardized tests, and the kind of problem-solving that shows up in virtually every career. As a mathematics undergraduate now, I found that my experience in high school math contests did not just transfer to my college math courses, but to almost every other facet of life, whether it is relationships, music, writing, and education."),
  ("p","More than that, they develop confidence that isn&rsquo;t fragile. It&rsquo;s not the confidence of someone who was always told they were smart. It&rsquo;s the confidence of someone who knows, from experience, that they can figure hard things out."),
  ("p","That&rsquo;s worth a few extra minutes of frustration at the kitchen table."),
 ],
}]

def _plain(s):
    """strip tags + decode a few entities -> plain text for JSON-LD/description."""
    s=re.sub(r"<[^>]+>","",s)
    for a,b in [("&rsquo;","’"),("&ldquo;","“"),("&rdquo;","”"),
                ("&hellip;","…"),("&amp;","&"),("&mdash;","—")]:
        s=s.replace(a,b)
    return s

def render_body(blocks):
    out=[]
    for kind,val in blocks:
        if kind in ("p","lede"):
            cls=' class="lede"' if kind=="lede" else ""
            out.append(f"<p{cls}>{val}</p>")
        elif kind=="h2":
            out.append(f"<h2>{val}</h2>")
        elif kind=="ul":
            lis="".join(f"<li>{x}</li>" for x in val)
            out.append(f"<ul>{lis}</ul>")
    return "\n    ".join(out)

def article_body_text(blocks):
    return " ".join(_plain(v if isinstance(v,str) else " ".join(v)) for _,v in blocks)

def head(title,desc,canon,og_title,og_desc,og_img,og_type="website",ld=None,extra=""):
    lds="".join(f'\n<script type="application/ld+json">{json.dumps(x)}</script>' for x in (ld or []))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{GA}
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Quantica">
<meta property="og:title" content="{H.escape(og_title)}">
<meta property="og:description" content="{H.escape(og_desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{H.escape(og_title)}">
<meta name="twitter:description" content="{H.escape(og_desc)}">
<meta name="twitter:image" content="{og_img}">{extra}
<link rel="icon" href="/favicon.svg">{lds}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>'''

# --------------------------- article page ---------------------------
def build_post(P):
    url=f"{BASE}/blog/{P['slug']}"
    img=f"{BASE}/og-blog.png"
    ld_article={
     "@context":"https://schema.org","@type":"BlogPosting","headline":P["title"],
     "description":P["desc"],"url":url,"mainEntityOfPage":{"@type":"WebPage","@id":url},
     "datePublished":P["date"],"dateModified":P["date"],"inLanguage":"en",
     "image":img,"keywords":P["kw"],"wordCount":len(article_body_text(P["body"]).split()),
     "articleSection":"Learning","author":{"@type":"Person","name":P["author"]},
     "publisher":ORG,"isAccessibleForFree":True,
    }
    ld_crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
     {"@type":"ListItem","position":1,"name":"Quantica","item":BASE+"/"},
     {"@type":"ListItem","position":2,"name":"Blog","item":BASE+"/blog"},
     {"@type":"ListItem","position":3,"name":P["title"],"item":url}]}
    extra=(f'\n<meta property="article:published_time" content="{P["date"]}">'
           f'\n<meta property="article:modified_time" content="{P["date"]}">'
           f'\n<meta property="article:author" content="{H.escape(P["author"])}">'
           f'\n<meta property="article:section" content="Learning">'
           f'\n<meta name="author" content="{H.escape(P["author"])}">')
    page=head(P["seo_title"],P["desc"],url,P["title"],P["desc"],img,"article",
              [ld_article,ld_crumb],extra)
    page+=f'''
{nav_html()}
<nav class="wrap crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span>/</span> <a href="/blog">Blog</a> <span>/</span> <span>Productive struggle</span></nav>
<main class="wrap">
<article class="post">
  <header class="post-head">
    <p class="kick">Quantica &middot; Blog</p>
    <h1>{P["title"]}</h1>
    <div class="byline"><span class="who">{H.escape(P["author"])}</span><span class="dot"></span><time datetime="{P["date"]}">{P["date_h"]}</time><span class="dot"></span><span>{P["read"]}</span></div>
  </header>
  <div class="post-body">
    {render_body(P["body"])}
    <div class="endnote">
      <div class="m">{MILO}</div>
      <p>Quantica is a math course built on productive struggle. Every lesson is a real problem to crack, with Milo nudging you toward the answer instead of handing it over. <a href="/?start=1">Start free &rarr;</a></p>
    </div>
  </div>
</article>
</main>

<section class="wrap cta-band">
  <h2>Let them <span class="mark">struggle</span>.</h2>
  <div class="cta" style="justify-content:center"><a class="pill solid" href="/?start=1">Try Quantica &mdash; free &rarr;</a><a class="pill" href="/prealgebra">See the course</a></div>
</section>

{foot_html()}
</body>
</html>'''
    open(f"{ROOT}/blog/{P['slug']}.html","w",encoding="utf-8").write(page)
    print("wrote blog/"+P["slug"]+".html")

# ---------------------------- index page ----------------------------
def build_index():
    url=f"{BASE}/blog"
    img=f"{BASE}/og-blog.png"
    desc=("Essays on how children actually learn math, from productive struggle and growth mindset "
          "to problem-solving. Written for parents and curious learners.")
    ld_blog={"@context":"https://schema.org","@type":"Blog","name":"Quantica Blog","url":url,
     "description":desc,"inLanguage":"en","publisher":ORG,
     "blogPost":[{"@type":"BlogPosting","headline":p["title"],"url":f"{BASE}/blog/{p['slug']}",
                  "datePublished":p["date"],"author":{"@type":"Person","name":p["author"]},
                  "description":p["desc"]} for p in POSTS]}
    ld_crumb={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
     {"@type":"ListItem","position":1,"name":"Quantica","item":BASE+"/"},
     {"@type":"ListItem","position":2,"name":"Blog","item":url}]}
    cards=[]
    for p in POSTS:
        cards.append(f'''<a class="postcard" href="/blog/{p['slug']}">
      <div class="meta"><span>{p['date_h']}</span><span>{p['read']}</span></div>
      <h2>{H.escape(p['title'])}</h2>
      <p>{H.escape(p['excerpt'])}</p>
      <span class="more">Read the essay &rarr;</span>
    </a>''')
    page=head("Blog: How Kids Actually Learn Math | Quantica",desc,url,
              "The Quantica Blog",desc,img,"website",[ld_blog,ld_crumb])
    page+=f'''
{nav_html()}
<main>
<section class="wrap bloghero">
  <p class="kick">Quantica &middot; Blog</p>
  <h1>How kids actually <span class="mark">learn math</span>.</h1>
  <p class="lead">Essays on productive struggle, growth mindset, and problem-solving, for parents and anyone who wants math to finally click.</p>
</section>
<section class="wrap" style="padding-top:0">
  <div class="posts">
    {"".join(cards)}
  </div>
</section>
<section class="wrap cta-band">
  <h2>Learn math by <span class="mark">solving</span>.</h2>
  <div class="cta" style="justify-content:center"><a class="pill solid" href="/?start=1">Start free &rarr;</a><a class="pill" href="/prealgebra">See the course</a></div>
</section>
</main>
{foot_html()}
</body>
</html>'''
    open(f"{ROOT}/blog.html","w",encoding="utf-8").write(page)
    print("wrote blog.html")

for P in POSTS:
    build_post(P)
build_index()
print("done.")
