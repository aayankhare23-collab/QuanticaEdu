# Rebuilds the QuanticaEdu marketing landing as a WEMBI-style editorial page.
# Scoped under .wmb. Replaces the region from the landing <header> to just before <!-- SIGNUP -->.
# Keeps the course app untouched. CTAs call openLesson() (defined in the app). No interactive demo.
import json, re
ROOT="/Users/aayankhare/Claude/Projects/QuanticaEdu/landing.html"
SCR="/private/tmp/claude-501/-Users-aayankhare-Claude-Projects-QuanticaEdu/020a3e6a-5784-4b7e-b4f9-89d3f3d809c0/scratchpad/wembi"
design_css=open(SCR+"/design.css").read()
milo=open(SCR+"/milo.svg").read()
anim=json.load(open("/Users/aayankhare/Claude/Projects/QuanticaEdu/_anim.json"))
pyth=anim['pyth_anim']; tri=anim['tri_anim']; circ=anim['circ_anim']
html=open(ROOT, encoding="utf-8").read()

# compact Milo face for the chat avatar icon
MILO_IC = '''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<path d="M32 7 C46 7 51 12 51 32 C51 52 46 57 32 57 C18 57 13 52 13 32 C13 12 18 7 32 7Z" fill="#beff8b"/>
<path d="M32 7 C23 7 18 11 15.5 21 C20 14 26 12 32 12 Z" fill="#9dbbc5" opacity=".32"/>
<circle cx="25.5" cy="30" r="4.4" fill="#9dbbc5"/><circle cx="38.5" cy="30" r="4.4" fill="#9dbbc5"/>
<circle cx="25.5" cy="30" r="2.1" fill="#0a0a0a"/><circle cx="38.5" cy="30" r="2.1" fill="#0a0a0a"/>
<circle cx="26.4" cy="29" r=".8" fill="#fff"/><circle cx="39.4" cy="29" r=".8" fill="#fff"/>
<path d="M26 38 Q32 43.5 38 38" fill="none" stroke="#0a0a0a" stroke-width="2.2" stroke-linecap="round"/>
</svg>'''

CHAT = f'''<div class="milo-card">
        <div class="milo-win">
          <div class="top">
            <span class="av">{MILO_IC}</span>
            <div class="who"><div class="nm">Milo</div><div class="st">your Quantica tutor</div></div>
          </div>
          <div class="body" id="miloBody"></div>
          <div class="compose"><span class="fi">Ask me anything about this problem&hellip;</span><span class="snd">&#10148;</span></div>
        </div>
      </div>'''

LAYOUT = r"""
<style id="wmb-layout">
/* force Space Grotesk across the whole marketing region (app sets h1/p fonts globally) */
.wmb,.wmb h1,.wmb h2,.wmb h3,.wmb h4,.wmb h5,.wmb p,.wmb a,.wmb span,.wmb div,.wmb button,.wmb summary,.wmb small,.wmb li,.wmb ul,.wmb strong,.wmb em,.wmb text{font-family:'Space Grotesk',system-ui,-apple-system,'Segoe UI',sans-serif}
/* ---- hero background (subtle drifting grid + sparse capsule rain) ---- */
.wmb{--hb-lime:#beff8b;--hb-slate:#9dbbc5;--hb-strength:.85}
.wmb-herosec{position:relative;isolation:isolate;overflow:hidden}
.hero-bg{position:absolute;inset:0;z-index:0;overflow:hidden;pointer-events:none;opacity:var(--hb-strength);
  -webkit-mask-image:radial-gradient(120% 108% at 24% 22%,#000 32%,transparent 74%);
          mask-image:radial-gradient(120% 108% at 24% 22%,#000 32%,transparent 74%)}
.hero-bg__grid{position:absolute;inset:-40px;background-image:linear-gradient(to right,rgba(10,10,10,.05) 1px,transparent 1px),linear-gradient(to bottom,rgba(10,10,10,.05) 1px,transparent 1px);background-size:34px 34px;animation:hb-drift 42s linear infinite}
@keyframes hb-drift{from{transform:translate3d(0,0,0)}to{transform:translate3d(-34px,-34px,0)}}
.hero-bg__rain{position:absolute;inset:0}
.hero-bg__rain i{position:absolute;top:-60px;left:var(--x);width:var(--w);height:var(--h);background:var(--c);border-radius:999px;opacity:0;filter:blur(.3px);animation:hb-fall var(--dur) linear var(--d) infinite}
@keyframes hb-fall{0%{transform:translateY(0);opacity:0}12%{opacity:.3}88%{opacity:.3}100%{transform:translateY(120vh);opacity:0}}
@media(prefers-reduced-motion:reduce){.hero-bg__grid{animation:none}.hero-bg__rain i{animation:none;opacity:0}}

/* ---- hero ---- */
.wmb-herosec{padding-block:clamp(28px,5vw,64px) var(--wmb-section-y)}
.wmb-hero-grid{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1.04fr) minmax(0,.96fr);gap:clamp(28px,5vw,64px);align-items:center}
.wmb-hero-copy .wmb-hero{margin:0}
.wmb-hero-copy .wmb-lead{margin-top:clamp(20px,2.4vw,30px)}
.wmb-hero-cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:clamp(26px,3vw,38px)}
.wmb-hero-milo{display:flex;justify-content:center}
.wmb-hero-note{margin-top:18px;font-size:13px}
/* hero Pythagorean proof (large & prominent) */
.wmb-hero-proof{width:100%;max-width:510px;margin:0 auto}
.wmb-hero-proof svg{width:100%;height:auto;display:block}
/* Meet Milo chat showcase row */
.wmb-milo-row{display:grid;grid-template-columns:minmax(0,1.06fr) minmax(0,.94fr);gap:clamp(30px,5vw,72px);align-items:center}
.wmb-milo-chat{display:flex;justify-content:center}
.wmb-milo-copy .wmb-kicker{margin-bottom:14px}
.wmb-milo-copy .wmb-h2{margin:0;max-width:16ch}
.wmb-milo-copy p{margin-top:22px;font-size:var(--wmb-lead)}

/* ---- Milo dark chat (Milo in action) — large & prominent hero element ---- */
.wmb .milo-card{width:100%;max-width:564px}
.wmb .milo-win{width:100%;box-sizing:border-box;background:radial-gradient(120% 130% at 50% 0%,#16273f 0%,#0c1626 60%,#080f19 100%);border:1px solid rgba(190,255,139,.26);border-radius:30px;box-shadow:0 56px 120px -44px rgba(10,10,10,.62),0 0 0 1px rgba(255,255,255,.03),0 0 90px -26px rgba(190,255,139,.45);overflow:hidden}
.wmb .milo-win .top{display:flex;align-items:center;gap:12px;padding:16px 20px;border-bottom:1px solid rgba(255,255,255,.07);background:linear-gradient(120deg,#17293f,#0f2136)}
.wmb .milo-win .av{width:50px;height:50px;flex:none;display:grid;place-items:center;animation:milo-bob 5s ease-in-out infinite}
.wmb .milo-win .av svg{width:100%;height:auto;display:block}
@keyframes milo-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
.wmb .milo-win .av.talk{animation:milo-wig .5s ease-in-out infinite}
@keyframes milo-wig{0%,100%{transform:rotate(0)}30%{transform:rotate(-7deg) translateY(-2px)}70%{transform:rotate(6deg)}}
.wmb .milo-win .who{line-height:1.2}
.wmb .milo-win .nm{font-weight:600;font-size:16px;color:#f4f8ff}
.wmb .milo-win .st{font-size:12px;color:#93e6b4;display:flex;align-items:center;gap:6px;margin-top:2px}
.wmb .milo-win .st::before{content:"";width:7px;height:7px;border-radius:999px;background:#7bd63f;box-shadow:0 0 0 0 rgba(123,214,63,.5);animation:milo-pulse 2s infinite}
@keyframes milo-pulse{0%{box-shadow:0 0 0 0 rgba(123,214,63,.5)}70%{box-shadow:0 0 0 8px rgba(123,214,63,0)}100%{box-shadow:0 0 0 0 rgba(123,214,63,0)}}
.wmb .milo-win .body{position:relative;padding:20px;display:flex;flex-direction:column;justify-content:flex-end;gap:12px;height:452px;box-sizing:border-box;overflow:hidden;-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 38px,#000 100%);mask-image:linear-gradient(to bottom,transparent 0,#000 38px,#000 100%)}
.wmb .milo-win .mb{max-width:86%;flex:0 0 auto;padding:12px 16px;border-radius:18px;font-size:15.5px;line-height:1.5;opacity:0;transform:translateY(18px) scale(.75);transition:opacity .32s ease,transform .55s cubic-bezier(.34,1.56,.64,1)}
.wmb .milo-win .mb.show{opacity:1;transform:none}
.wmb .milo-win .mb.bot{align-self:flex-start;background:linear-gradient(180deg,#2b4468,#1c3049);border:1px solid rgba(124,199,255,.16);color:#eef4fd;border-bottom-left-radius:6px}
.wmb .milo-win .mb.me{align-self:flex-end;background:linear-gradient(135deg,#d5ff9f,#a8f074);color:#0a0a0a;font-weight:600;border-bottom-right-radius:6px;box-shadow:0 8px 20px -10px rgba(190,255,139,.55)}
.wmb .milo-win .mb.pop{box-shadow:0 0 0 1.5px rgba(190,255,139,.55),0 10px 32px -10px rgba(190,255,139,.5)}
.wmb .milo-win .mb.xp{align-self:flex-start;background:linear-gradient(135deg,#ffd36b,#ff9d3c);color:#0a0a0a;font-weight:700;font-size:14px;padding:9px 15px;border-radius:999px;border:1.5px solid rgba(10,10,10,.28);box-shadow:0 8px 22px -8px rgba(255,157,60,.65)}
.wmb .milo-win .mb.xp.show{animation:xpPop .7s .45s ease}
@keyframes xpPop{0%,100%{transform:rotate(0)}25%{transform:rotate(-5deg) scale(1.07)}60%{transform:rotate(4deg)}}
.wmb .milo-win .conf{position:absolute;width:8px;height:8px;border-radius:2px;top:0;left:0;pointer-events:none;animation:confFall 1.6s cubic-bezier(.25,.7,.45,1) forwards}
.wmb .milo-win .conf.rd{border-radius:50%}
@keyframes confFall{0%{opacity:1;transform:translate(var(--x0),var(--y0)) rotate(0) scale(1)}70%{opacity:1}100%{opacity:0;transform:translate(var(--x1),var(--y1)) rotate(var(--r)) scale(.55)}}
.wmb .milo-win .mb b{color:inherit}
.wmb .milo-win .typing{align-self:flex-start;flex:0 0 auto;background:linear-gradient(180deg,#243a54,#1b2e46);border-radius:16px;border-bottom-left-radius:5px;padding:13px 16px;display:none;gap:4px}
.wmb .milo-win .typing.show{display:flex}
.wmb .milo-win .typing i{width:7px;height:7px;border-radius:999px;background:#9fb0c9;animation:milo-dot 1.2s infinite}
.wmb .milo-win .typing i:nth-child(2){animation-delay:.2s}.wmb .milo-win .typing i:nth-child(3){animation-delay:.4s}
@keyframes milo-dot{0%,60%,100%{opacity:.3;transform:translateY(0)}30%{opacity:1;transform:translateY(-4px)}}
.wmb .milo-win .compose{display:flex;gap:9px;align-items:center;padding:13px 15px;border-top:1px solid rgba(255,255,255,.07);background:rgba(255,255,255,.02)}
.wmb .milo-win .compose .fi{flex:1;font-size:13px;color:#9fb0c9;background:#17253d;border-radius:999px;padding:10px 15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wmb .milo-win .compose .snd{width:36px;height:36px;flex:none;border-radius:999px;background:#beff8b;color:#0a0a0a;display:grid;place-items:center;font-size:14px}
@media(prefers-reduced-motion:reduce){.wmb .milo-win .mb{opacity:1;transform:none;transition:none}.wmb .milo-win .av{animation:none}.wmb .milo-win .mb.xp.show{animation:none}.wmb .milo-win .conf{display:none}}

/* ---- value strip ---- */
.wmb-strip{position:relative;z-index:1;display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(20px,3vw,44px);padding-top:clamp(24px,4vw,52px);border-top:1px solid var(--wmb-rule-soft)}
.wmb-strip-item .wmb-kicker{margin-bottom:10px}
.wmb-strip-item h3{font-size:var(--wmb-h3)}
.wmb-strip-item p{margin-top:8px}
/* ---- Meet Milo bold intro ---- */
.mi-sec{position:relative;text-align:center;padding-block:clamp(44px,7vw,110px) clamp(20px,3vw,40px)}
.mi-beam{position:absolute;left:50%;top:clamp(64px,8vw,130px);bottom:0;transform:translateX(-50%);width:min(150px,32vw);background:linear-gradient(180deg,rgba(190,255,139,.42),rgba(190,255,139,0) 85%);border-radius:999px;filter:blur(10px);pointer-events:none}
.mi-face{position:relative;width:clamp(116px,16vw,176px);margin:0 auto;animation:miBob 4.5s ease-in-out infinite}
.mi-face svg{width:100%;height:auto;display:block;filter:drop-shadow(0 20px 34px rgba(10,10,10,.2))}
@keyframes miBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.mi-h{position:relative;font-size:clamp(34px,6.5vw,74px);letter-spacing:-.035em;line-height:1.06;font-weight:700;margin:clamp(24px,3.4vw,40px) 0 0}
@media(prefers-reduced-motion:reduce){.mi-face{animation:none}}

/* ---- meet milo ---- */
.wmb-meet{max-width:20ch}
.wmb-meet .wmb-h2{margin:0}
.wmb-meet p{margin-top:22px;font-size:var(--wmb-lead)}

/* ---- visual proofs (numbered editorial rows) ---- */
.wmb-proof-row{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,6vw,88px);align-items:center;padding-block:clamp(36px,6vw,80px);border-top:1px solid var(--wmb-rule-soft)}
.wmb-proof-row.rev .wmb-proof-fig{order:2}
.wmb-proof-fig{display:flex;justify-content:center}
.wmb-proof-fig svg{width:100%;max-width:440px;height:auto;display:block}
.wmb-num{display:block;font-size:clamp(40px,6vw,84px);font-weight:700;line-height:.9;letter-spacing:-.04em;color:var(--wmb-ink)}
.wmb-proof-txt .wmb-rule{margin:18px 0}
.wmb-proof-txt h2{font-size:var(--wmb-h2)}
.wmb-proof-txt p{margin-top:20px}

/* ---- course path ---- */
.wmb-path .wmb-h2{max-width:16ch;margin:0}
.wmb-pills{display:flex;flex-wrap:wrap;gap:10px;margin-top:clamp(24px,3vw,36px)}
.wmb .wmb-pill--soon{border-style:dashed;border-color:var(--wmb-rule-soft);color:var(--wmb-gray);cursor:default}
.wmb .wmb-pill--soon:hover{transform:none;border-color:var(--wmb-rule-soft)}
.wmb .wmb-pill--soon em{font-style:normal;font-size:10px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;padding:2px 7px;border-radius:999px;background:var(--wmb-rule-soft);color:var(--wmb-ink)}

/* ---- pricing ---- */
.wmb-pricing .wmb-h2{margin:0 0 clamp(28px,3.5vw,44px)}
.wmb-price-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;max-width:860px}
.wmb-price{border:1.5px solid var(--wmb-rule-soft);border-radius:var(--wmb-radius);padding:clamp(24px,3vw,36px);position:relative;background:transparent}
.wmb-price--feat{border-color:var(--wmb-ink)}
.wmb-price .wmb-price-tag{position:absolute;top:-13px;left:24px;background:var(--wmb-lime);color:var(--wmb-ink);font-size:12px;font-weight:600;padding:4px 12px;border-radius:999px}
.wmb-price .wmb-price-name{font-weight:600;font-size:15px;letter-spacing:.02em;text-transform:uppercase;color:var(--wmb-gray)}
.wmb-price .wmb-price-amt{font-size:clamp(38px,5vw,56px);font-weight:700;letter-spacing:-.03em;line-height:1;margin:12px 0 4px}
.wmb-price .wmb-price-amt span{font-size:16px;font-weight:500;color:var(--wmb-gray)}
.wmb-price ul{list-style:none;padding:0;margin:20px 0 26px;display:grid;gap:11px}
.wmb-price li{font-size:15px;display:flex;gap:10px;align-items:flex-start}
.wmb-price li::before{content:"";width:16px;height:16px;flex:none;margin-top:3px;border-radius:999px;background:var(--wmb-lime);box-shadow:inset 0 0 0 1.5px var(--wmb-ink)}
.wmb-price .wmb-btn{width:100%;justify-content:center}
.wmb-price-note{margin-top:22px;font-size:13px}

/* ---- faq ---- */
.wmb-faq .wmb-h2{margin:0 0 clamp(20px,2.5vw,32px)}
.wmb-faq-list{max-width:760px}
.wmb-faq details{border-top:1px solid var(--wmb-rule-soft);padding:20px 0}
.wmb-faq details:last-child{border-bottom:1px solid var(--wmb-rule-soft)}
.wmb-faq summary{list-style:none;cursor:pointer;color:var(--wmb-ink);font-weight:600;font-size:clamp(18px,2vw,22px);letter-spacing:-.02em;display:flex;justify-content:space-between;gap:20px;align-items:center}
.wmb-faq summary::-webkit-details-marker{display:none}
.wmb-faq summary::after{content:"+";font-weight:400;font-size:26px;line-height:1;color:var(--wmb-gray)}
.wmb-faq details[open] summary::after{content:"\2013"}
.wmb-faq details p{margin-top:14px}

/* ---- final cta ---- */
.wmb-final{text-align:left}
.wmb-final .wmb-hero{margin:0 0 clamp(26px,3vw,40px)}

/* ---- footer ---- */
.wmb-foot{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;padding-block:40px;border-top:1px solid var(--wmb-rule)}
.wmb-foot-links{display:flex;gap:20px}
.wmb-foot-links a{color:var(--wmb-ink);text-decoration:none;font-size:14px;font-weight:500}
.wmb-foot-links a:hover{text-decoration:underline}

/* ---- responsive ---- */
@media(max-width:860px){
  .wmb-nav{gap:8px}
  .wmb-herosec{padding-top:8px}
  .wmb-hero-grid{grid-template-columns:1fr;gap:30px}
  .wmb-hero-milo{margin-top:4px}
  .wmb-milo-row{grid-template-columns:1fr;gap:30px}
  .wmb-milo-copy{order:-1}
  .wmb-strip{grid-template-columns:1fr;gap:26px}
  .wmb-proof-row{grid-template-columns:1fr;gap:26px}
  .wmb-proof-row.rev .wmb-proof-fig{order:0}
  .wmb-proof-fig{order:-1}
  .wmb-price-grid{grid-template-columns:1fr}
}
</style>
"""

def proof_section(num, fig, title_html, body, rev=False):
    rc = " rev" if rev else ""
    return f'''
  <div class="wmb-proof-row{rc}">
    <div class="wmb-proof-fig">{fig}</div>
    <div class="wmb-proof-txt">
      <span class="wmb-num">{num}</span>
      <hr class="wmb-rule">
      <h2>{title_html}</h2>
      <hr class="wmb-rule">
      <p class="wmb-muted">{body}</p>
    </div>
  </div>'''

MARKUP = f'''
<div class="wmb">
<a id="top"></a>

<!-- NAV -->
<nav class="wmb-nav wmb-wrap">
  <a class="wmb-nav-brand" href="#top">QuanticaEdu</a>
  <div class="wmb-nav-links">
    <a class="wmb-pill" href="#how">How it works</a>
    <a class="wmb-pill" href="/prealgebra">Courses</a>
    <a class="wmb-pill" href="/blog">Blog</a>
    <a class="wmb-pill" href="#pricing">Pricing</a>
    <a class="wmb-pill" id="navSignin" href="#" onclick="showAuthModal('in');return false;">Sign in</a>
    <a class="wmb-pill wmb-pill--on" href="/prealgebra"><span class="wmb-dot"></span>Start free</a>
  </div>
</nav>

<!-- HERO -->
<section class="wmb-herosec wmb-section" id="start">
  <div class="hero-bg" aria-hidden="true">
    <div class="hero-bg__grid"></div>
    <div class="hero-bg__rain">
      <i style="--x:9%;--d:0s;--dur:22s;--w:6px;--h:30px;--c:var(--hb-lime)"></i>
      <i style="--x:24%;--d:6s;--dur:19s;--w:6px;--h:22px;--c:var(--hb-slate)"></i>
      <i style="--x:41%;--d:11s;--dur:24s;--w:6px;--h:40px;--c:var(--hb-slate)"></i>
      <i style="--x:63%;--d:3s;--dur:20s;--w:6px;--h:26px;--c:var(--hb-lime)"></i>
      <i style="--x:79%;--d:14s;--dur:23s;--w:6px;--h:34px;--c:var(--hb-slate)"></i>
      <i style="--x:90%;--d:8s;--dur:26s;--w:6px;--h:24px;--c:var(--hb-slate)"></i>
    </div>
  </div>
  <div class="wmb-wrap wmb-hero-grid">
    <div class="wmb-hero-copy">
      <h1 class="wmb-hero">Understand math.<br>Don&#8217;t <span class="wmb-mark-block">memorize</span> it.</h1>
      <p class="wmb-lead">Learn by solving, with Milo. <span class="wmb-dim">A tutor that helps you find the answer yourself.</span></p>
      <div class="wmb-hero-cta">
        <a class="wmb-btn wmb-btn--solid wmb-btn--lg" href="/prealgebra">Start free</a>
        <a class="wmb-btn wmb-btn--lg" href="#how">See how it works</a>
      </div>
      <p class="wmb-hero-note wmb-muted">No card required &middot; Full Prealgebra unit free</p>
    </div>
    <div class="wmb-hero-milo">
      <div class="wmb-hero-proof">{pyth}</div>
    </div>
  </div>
</section>

<!-- MEET MILO (bold intro) -->
<section class="wmb-wrap wmb-section mi-sec">
  <div class="mi-beam" aria-hidden="true"></div>
  <div class="mi-face" aria-hidden="true"><svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
<path d="M32 7 C46 7 51 12 51 32 C51 52 46 57 32 57 C18 57 13 52 13 32 C13 12 18 7 32 7Z" fill="#beff8b"/>
<path d="M32 7 C23 7 18 11 15.5 21 C20 14 26 12 32 12 Z" fill="#9dbbc5" opacity=".32"/>
<circle cx="25.5" cy="30" r="4.4" fill="#9dbbc5"/><circle cx="38.5" cy="30" r="4.4" fill="#9dbbc5"/>
<circle cx="25.5" cy="30" r="2.1" fill="#0a0a0a"/><circle cx="38.5" cy="30" r="2.1" fill="#0a0a0a"/>
<circle cx="26.4" cy="29" r=".8" fill="#fff"/><circle cx="39.4" cy="29" r=".8" fill="#fff"/>
<path d="M26 38 Q32 43.5 38 38" fill="none" stroke="#0a0a0a" stroke-width="2.2" stroke-linecap="round"/>
</svg></div>
  <h2 class="mi-h">Meet <span class="wmb-mark">Milo</span>, your personal tutor.</h2>
</section>

<!-- MEET MILO (chat showcase) -->
<section class="wmb-wrap wmb-section wmb-milo-row">
  <div class="wmb-milo-chat">{CHAT}</div>
  <div class="wmb-milo-copy">
    <span class="wmb-kicker">Milo in action</span>
    <h2 class="wmb-h2">A tutor <span class="wmb-mark">on call</span> for every problem.</h2>
    <p class="wmb-muted">When a problem stops you cold, Milo asks the right question &#8212; not the answer &#8212; and helps you find it yourself.</p>
  </div>
</section>

<!-- VISUAL PROOFS -->
<section class="wmb-wrap" id="how">
{proof_section("01", tri, 'A <span class="wmb-mark-block">problem-first</span><br>philosophy.', "Instead of slogging through a textbook, we take a problem and guide you through it, with Milo at your fingertips.")}
{proof_section("02", circ, 'Building mathematical<br><span class="wmb-mark-block">insight</span>.', "A rigorous curriculum that runs deeper than school math. When you can see why an idea is true, the hard problems start opening up.", rev=True)}
</section>

<!-- COURSE PATH -->
<section class="wmb-wrap wmb-section wmb-path" id="path">
  <h2 class="wmb-h2">From prealgebra to <span class="wmb-mark">calculus</span>. The complete, rigorous mathematics education.</h2>
  <div class="wmb-pills">
    <a class="wmb-pill wmb-pill--on" href="/prealgebra"><span class="wmb-dot"></span>Prealgebra</a>
    <span class="wmb-pill wmb-pill--soon">Algebra I <em>Soon</em></span>
    <span class="wmb-pill wmb-pill--soon">Geometry <em>Soon</em></span>
    <span class="wmb-pill wmb-pill--soon">Number Theory <em>Soon</em></span>
    <span class="wmb-pill wmb-pill--soon">Counting <em>Soon</em></span>
    <span class="wmb-pill wmb-pill--soon">Logic <em>Soon</em></span>
    <span class="wmb-pill wmb-pill--soon">Intermediate <em>Soon</em></span>
    <span class="wmb-pill wmb-pill--soon">Calculus <em>Soon</em></span>
  </div>
  <p style="margin-top:28px;font-size:17px"><a href="/prealgebra" style="border-bottom:2px solid var(--wmb-ink);text-decoration:none;font-weight:600">Browse the full Prealgebra syllabus &mdash; 12 chapters, 64 lessons &rarr;</a></p>
</section>

<!-- PRICING -->
<section class="wmb-wrap wmb-section wmb-pricing" id="pricing">
  <h2 class="wmb-h2"><span class="wmb-mark">Free</span> while we're in early access.</h2>
  <div class="wmb-price-grid" style="grid-template-columns:1fr;max-width:480px">
    <div class="wmb-price wmb-price--feat">
      <div class="wmb-price-tag">Early access</div>
      <div class="wmb-price-name">Everything, free</div>
      <div class="wmb-price-amt">$0</div>
      <ul><li>Full Prealgebra course, every lesson</li><li>Milo, your tutor, on every problem</li><li>Mastery map &amp; spaced review</li><li>No card required</li></ul>
      <a class="wmb-btn wmb-btn--solid" href="/prealgebra">Start free &rarr;</a>
    </div>
  </div>
  <p class="wmb-price-note wmb-muted">No paywall right now. When we do introduce pricing, it will still cost less than a single tutoring session.</p>
</section>

<!-- FAQ -->
<section class="wmb-wrap wmb-section wmb-faq">
  <h2 class="wmb-h2">Good to know</h2>
  <div class="wmb-faq-list">
    <details><summary>What makes Quantica different?</summary><p class="wmb-muted">You learn by solving real problems with instant feedback and layered hints, so concepts emerge from your own work instead of being memorized.</p></details>
    <details><summary>Do I need to be good at math already?</summary><p class="wmb-muted">No. Every course is built from the ground up, and Milo is there whenever a problem stops you.</p></details>
    <details><summary>Is it really free to start?</summary><p class="wmb-muted">Yes. The full Prealgebra unit is free, no card required.</p></details>
    <details><summary>Do I need to buy each course?</summary><p class="wmb-muted">No. Everything on Quantica is free during early access. When pricing launches later, one simple plan will unlock every course.</p></details>
  </div>
</section>

<!-- FINAL CTA -->
<section class="wmb-wrap wmb-section wmb-final">
  <h2 class="wmb-hero">Start <span class="wmb-mark-block">solving</span>.</h2>
  <a class="wmb-btn wmb-btn--solid wmb-btn--lg" href="/prealgebra">Start free &#8594;</a>
</section>

<!-- FOOTER -->
<footer class="wmb-wrap wmb-foot">
  <span class="wmb-nav-brand">QuanticaEdu</span>
  <div class="wmb-foot-links"><a href="/prealgebra">Prealgebra</a><a href="/blog">Blog</a><a href="#pricing">Pricing</a><a href="#how">How it works</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a><a href="mailto:support@quanticaedu.com">Contact</a></div>
  <small class="wmb-muted">&#169; 2026 Quantica &middot; Learn math by solving.</small>
</footer>
</div>
'''

HEAD_SEO = r'''
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}window.track=function(n,p){try{gtag('event',n,p||{});}catch(e){}};(function(){try{var h=location.hostname;if(h!=='quanticaedu.com'&&h!=='www.quanticaedu.com')return;if(location.search.indexOf('imfounder=1')>-1&&!localStorage.getItem('qa_internal')){localStorage.setItem('qa_internal','1');alert('Got it. Analytics is now off on this device.');}if(localStorage.getItem('qa_internal')==='1')return;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=G-98WQ2BFR6N';document.head.appendChild(s);gtag('js',new Date());gtag('config','G-98WQ2BFR6N',{allow_google_signals:false,allow_ad_personalization_signals:false});}catch(e){}})();</script>
<meta name="description" content="Quantica teaches math from prealgebra to calculus by having you solve, not memorize. Instant feedback, layered hints, and Milo, a tutor that helps you find the answer yourself.">
<link rel="canonical" href="https://quanticaedu.com/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Quantica">
<meta property="og:title" content="Quantica | Master Mathematics by Doing Mathematics">
<meta property="og:description" content="Prealgebra to calculus. Learn by solving real problems with instant feedback and Milo, your tutor.">
<meta property="og:url" content="https://quanticaedu.com/">
<meta property="og:image" content="https://quanticaedu.com/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Quantica | Master Mathematics by Doing Mathematics">
<meta name="twitter:description" content="Prealgebra to calculus. Learn by solving, with Milo.">
<meta name="twitter:image" content="https://quanticaedu.com/og-default.png">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"Quantica","url":"https://quanticaedu.com/","logo":"https://quanticaedu.com/og-default.png","sameAs":[],"description":"Quantica teaches math from prealgebra to calculus by having you solve, not memorize."}</script>
'''

APP_THEME = r'''
<style id="app-wembi-theme">
/* Re-skin the course app to the landing's palette (cream + lime + dark navy + Space Grotesk).
   Overrides token VALUES + font only — no layout/behaviour changes. Loaded after the app CSS. */
:root{
  --bg:#ededeb; --soft:#e7e7e3; --softer:#e1e1dc;
  --ink:#0a0a0a; --slate:#55554f; --mute:#83837c;
  --line:#dcdcd5;
  --navy:#14243b; --blue:#17293f; --mid:#274264; --sky:#3f74a8;
  --accent:#beff8b; --accent2:#a8f074;
  --green:#1f9d6b; --green2:#3ecf8e;
  --gold:#c79100; --gold2:#f1b51c;
  --purple:#7c3aed; --purple2:#a78bfa;
}
body{font-family:'Space Grotesk',system-ui,-apple-system,'Segoe UI',sans-serif}
/* app titles used the serif 'Fraunces' — switch every one to Space Grotesk to match the landing */
h1,h2,h3,h4,.logo,.tour-pop h4,.auth-card h2,.demo .top .t,.quad .cell b,.cpanel h4,.letter::before,.letter .sig,.course .num,.course h4,.price .amt,.cb-logo,.pagehead h1,.modal h4.sub,.toc .ch,.dchip .ttl,.psethead .pname,.ws-head .ws-title,.ws-nbhead .t,.ws-tuthead .nm,.tocnote .tn-sign,.toast .amt,.rw-ring .lv b,.rw-id .rank,.rw-avatar,.rw-stat .big,.rw-section-h,.shop-item .sw,.shop-item .nm,.dp-card h3,.dg-card h2{font-family:'Space Grotesk',system-ui,sans-serif}
/* primary CTA becomes lime with dark text (was orange gradient + white text) */
.btn-primary{color:#0a0a0a !important;text-shadow:none;border-color:rgba(10,10,10,.12) !important;box-shadow:0 12px 26px -12px rgba(120,190,60,.55) !important}
.btn-primary:hover{box-shadow:0 16px 32px -12px rgba(120,190,60,.7) !important}
/* dark Milo tutor panel — match the landing's dark Milo chat */
.ws-tutor{background:radial-gradient(120% 130% at 50% 0%,#16273f 0%,#0c1626 60%,#080f19 100%) !important;border-color:rgba(190,255,139,.22) !important;color:#dbe6f5}
.ws-tutor .ws-tuthead{background:linear-gradient(120deg,#17293f,#0f2136) !important;border-bottom:1px solid rgba(255,255,255,.08) !important}
.ws-tutor .ws-tuthead .nm{color:#f4f8ff}
.ws-tutor .tut-close{color:#9fb0c9}
.ws-tutor .ws-body{background:transparent !important}
.ws-tutor .tut-bub{color:#e8eef7}
.ws-tutor .tut-bub.bot{background:linear-gradient(180deg,#243a54,#1b2e46) !important}
.ws-tutor .tut-bub.me,.ws-tutor .tut-bub.usr,.ws-tutor .tut-bub.user,.ws-tutor .tut-bub.you{background:#beff8b !important;color:#0a0a0a !important}
.ws-tutor .tut-compose{background:rgba(255,255,255,.03) !important;border-top:1px solid rgba(255,255,255,.08) !important}
.ws-tutor .tut-input{background:#17253d !important;color:#dbe6f5 !important;border-color:rgba(255,255,255,.1) !important}
.ws-tutor .tut-input::placeholder{color:#9fb0c9}
.ws-tutor .snd{background:#beff8b !important;color:#0a0a0a !important}
/* workspace primary "Continue" -> lime (green primary, like the landing) */
.ws-next{background:#beff8b !important;color:#0a0a0a !important;box-shadow:0 12px 26px -12px rgba(120,190,60,.55) !important}
/* accent (lime) was being used as TEXT in a few places (e.g. contents lesson links) where it is
   unreadable/harsh. Recolor those text uses to a deep readable green; buttons keep the lime fill. */
.toc .sec.open,.toc .sec.open::after,.toc a.ex:hover,.hintbtn2,.peek,.factbox .flabel,.tocnote .tn-label,.hud-pill.mp svg,.streakchip svg{color:#2e7d3a !important}
/* app background: beige/cream everywhere (override the themed aurora gradient on the overlay) */
.overlay{background:#ededeb !important}
</style>
'''

SCRIPT = r'''
<script>
(function(){
  var rm = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  var body=document.getElementById('miloBody');
  if(!body) return;
  var av=document.querySelector('.milo-win .av');
  var script=[
    {who:'bot',t:"Hey! I&#8217;m Milo &#128075; What are we cracking today?"},
    {who:'me', t:"3/4 + 1/6 is melting my brain &#129760;"},
    {who:'bot',t:"Fractions only add when the pieces match. What size piece fits quarters <b>and</b> sixths?"},
    {who:'me', t:"hmm&#8230; twelfths?"},
    {who:'bot',t:"Yes!! Twelfths. So what do 3/4 and 1/6 turn into?"},
    {who:'me', t:"9/12 + 2/12 &#8230; 11/12!"},
    {who:'bot',cls:' pop',conf:true,t:"&#128165; Nailed it. You found that yourself, I just asked questions."},
    {who:'xp', t:"+10 XP &#9889;"}
  ];
  var CONF=['#beff8b','#ff7a5c','#ffc84d','#7cc7ff','#ff9ad5','#a97dff'];
  function confetti(){
    if(rm) return;
    var w=body.clientWidth||360, h=body.clientHeight||452;
    for(var k=0;k<16;k++){
      var p=document.createElement('i');
      p.className='conf'+(k%3===0?' rd':'');
      p.style.background=CONF[k%CONF.length];
      var x0=30+Math.random()*(w-90), y0=h-150+Math.random()*40;
      p.style.setProperty('--x0',x0+'px'); p.style.setProperty('--y0',y0+'px');
      p.style.setProperty('--x1',(x0+(Math.random()-.5)*170)+'px');
      p.style.setProperty('--y1',(y0-40-Math.random()*160)+'px');
      p.style.setProperty('--r',(Math.random()*720-360)+'deg');
      p.style.animationDelay=(Math.random()*.18)+'s';
      body.appendChild(p);
      setTimeout(function(el){ return function(){ el.remove(); }; }(p),2100);
    }
  }
  function run(){
    body.innerHTML='';
    var typing=document.createElement('div'); typing.className='typing'; typing.innerHTML='<i></i><i></i><i></i>';
    body.appendChild(typing);
    var i=0;
    function step(){
      if(i>=script.length){ setTimeout(run,4400); return; }
      var m=script[i];
      var show=function(){
        typing.classList.remove('show');
        if(av) av.classList.remove('talk');
        var b=document.createElement('div'); b.className='mb '+m.who+(m.cls||''); b.innerHTML=m.t;
        body.insertBefore(b,typing);
        requestAnimationFrame(function(){ b.classList.add('show'); });
        if(m.conf) setTimeout(confetti,320);
        i++; setTimeout(step, m.who==='me'?620:(m.who==='xp'?1100:820));
      };
      if(m.who==='bot' && !rm){ typing.classList.add('show'); if(av) av.classList.add('talk'); setTimeout(show,700); }
      else if(m.who==='xp'){ setTimeout(show,420); }
      else show();
    }
    step();
  }
  if(rm){ body.innerHTML=script.map(function(m){return '<div class="mb '+m.who+(m.cls||'')+' show">'+m.t+'</div>';}).join(''); }
  else { run(); }
})();
</script>
<script>
/* Deep-launch from the SEO pages: ?start=1 opens the course dashboard; ?lesson=KEY opens that specific lesson. */
window.addEventListener('load',function(){
  var m=location.search.match(/[?&]lesson=([0-9.]+)/);
  var wantStart=location.search.indexOf('start=')>=0;
  if(!m && !wantStart) return;
  var n=0,t=setInterval(function(){
    if(typeof window.openLesson==='function'){
      clearInterval(t);
      try{ window.openLesson(); if(m && typeof window.gotoLesson==='function'){ window.gotoLesson(m[1]); } }catch(e){}
    } else if(++n>120){ clearInterval(t); }
  },40);
});
</script>
'''
STYLE = "<style id=\"wmb-design\">\n" + design_css + "\n</style>\n" + LAYOUT
NEW = STYLE + MARKUP + SCRIPT

# locate & replace the old landing region: from landing <header> to just before <!-- SIGNUP -->
start_anchor = '<header>\n  <div class="wrap">\n    <nav>\n      <a class="logo" href="#top">'
i0 = html.index(start_anchor); i1 = html.index('<!-- SIGNUP -->')
# strip any old footer between the region and app (defensive)
html = re.sub(r'\n<footer>\n  <div class="wrap">\n    <a class="logo" href="#top">.*?</footer>\n', '\n', html, flags=re.S)
i0 = html.index(start_anchor); i1 = html.index('<!-- SIGNUP -->')
before, after = html[:i0], html[i1:]
out = before + NEW.strip() + "\n\n" + after

# CRITICAL: excise the retired interactive-demo JS. Its DOM (#chips/#hintbtn/#opts/...) lived in the
# marketing region we just removed, but its driver JS sits after <!-- SIGNUP --> (kept verbatim). On load
# it does getElementById('hintbtn').addEventListener(...) on now-missing nodes, throws, and halts the app
# script BEFORE it defines TOC/LESSONS — which silently breaks the entire course app. Remove the block
# (from the PROBLEMS data through its init IIFE) so the app script reaches TOC/LESSONS.
out, n_demo = re.subn(
    r'  // --- interactive problems: one from each course ---\n.*?\n\n  // --- Prealgebra course modal',
    '  // --- Prealgebra course modal', out, count=1, flags=re.S)
assert n_demo == 1, "demo-JS block not found/removed (n=%d) — course app would break" % n_demo

# remove the "early stages / team grants free access in 3-12 hours" banner (kills credibility; paywall is off)
out, n_banner = re.subn(r'<div class="site-banner">.*?</div>\n\n', '', out, count=1, flags=re.S)
# and the pricing tour tooltip that repeats the same "team grants you free access shortly" claim
out = out.replace(
    'A single subscription unlocks every course. Create an account and our team grants you free access shortly.',
    'A single subscription unlocks every course on Quantica. Start free, no card required.')
print("banner removed:", n_banner)

# inject SEO head tags (description, canonical, Open Graph, Twitter card, Organization JSON-LD)
assert out.count('</head>') >= 1
out = out.replace('</head>', HEAD_SEO + APP_THEME + '</head>', 1)

open(ROOT,"w",encoding="utf-8").write(out)
print("replaced landing region: removed", i1-i0, "chars, inserted", len(NEW), "chars; demo-JS removed:", n_demo, "; new size", len(out))
