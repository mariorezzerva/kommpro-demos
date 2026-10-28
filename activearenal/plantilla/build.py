#!/usr/bin/env python3
"""
Plantilla vertical: TOUR OPERADORES (motor Rezzerva)
Genera desde data.json:
  dist/index.html                    home completo (Netlify)
  dist/tours/<slug>/index.html       una pagina por tour, con widget Rezzerva
  dist/wp/home.html                  bloque para Elementor (widget HTML), sin header/footer
  dist/wp/tour-<slug>.html           bloque de cada tour para Elementor
Para un operador nuevo: duplicar data.json, cambiar marca, colores, tours y tenant de Rezzerva.
"""
import json, html, os, re, shutil, sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else "data.json"), encoding="utf-8"))
B = D["brand"]
TOURS = D["tours"]
COMBOS = D.get("combos", [])
ALL = TOURS + COMBOS
BY = {t["slug"]: t for t in ALL}
# La plantilla vive en <sitio>/plantilla/ y publica en <sitio>/ (carpeta que sirve Netlify)
OUT = os.path.dirname(ROOT) if os.path.basename(ROOT) == "plantilla" else os.path.join(ROOT, "dist")

def e(s): return html.escape(str(s if s is not None else ""), quote=True)
ASSET = "/"  # raíz de las fotos propias (img/...); en los bloques de WordPress apunta al dominio de la demo
DEMO_URL = "https://activearenal-demo.pages.dev/"
def absimg(u): return (DEMO_URL + u) if u.startswith("img/") else img(u, 1600)
def img(u, w=1400):
    if not u: return ""
    if u.startswith("img/"): return ASSET + u
    if "i0.wp.com" in u: return re.sub(r"\?.*$", "", u) + f"?w={w}&ssl=1"
    m = re.match(r"https?://(.+)$", u)
    return f"https://i0.wp.com/{m.group(1)}?w={w}&ssl=1" if m else u
def money(n): return f"${n:,.0f}" if isinstance(n, (int, float)) else ""
def wa(text=""): return f"https://wa.me/{B['whatsapp']}" + (f"?text={quote(text)}" if text else "")

# ---------------------------------------------------------------- iconos (trazo fino)
I = {
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "flag": '<path d="M5 21V4M5 4h11l-2 3 2 3H5"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 2.6 15.4 0 18M12 3c-2.6 2.6-2.6 15.4 0 18"/>',
 "pin": '<path d="M12 21s-7-5.6-7-11a7 7 0 0114 0c0 5.4-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "cal": '<rect x="3" y="5" width="18" height="16" rx="2.5"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
 "check": '<path d="M20 6L9 17l-5-5"/>',
 "x": '<path d="M18 6L6 18M6 6l12 12"/>',
 "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>',
 "chat": '<path d="M21 11.5a8.4 8.4 0 01-12.6 7.3L3 21l2.2-5.1A8.5 8.5 0 1121 11.5z"/>',
 "send": '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>',
 "drop": '<path d="M12 3s6 6.4 6 11a6 6 0 01-12 0c0-4.6 6-11 6-11z"/>',
 "leaf": '<path d="M5 19c0-8 6-14 15-14 0 9-6 15-14 15"/><path d="M5 19c3-4 6-6 9-7"/>',
 "mountain": '<path d="M3 20l6-10 4 6 2-3 6 7z"/><path d="M8.5 11l1.5 2 1-1.5"/>',
 "moon": '<path d="M20 14.5A8 8 0 019.5 4 8 8 0 1020 14.5z"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
 "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "bus": '<rect x="3" y="5" width="18" height="12" rx="2.5"/><path d="M3 11h18M7 17v2M17 17v2"/><circle cx="7.5" cy="14" r=".6"/><circle cx="16.5" cy="14" r=".6"/>',
 "group": '<circle cx="9" cy="8" r="3.2"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5M15 14.6c3 0 6 1.6 6 4.6"/>',
 "plus": '<path d="M12 5v14M5 12h14"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
}
def ic(name, cls="ic"): return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{I[name]}</svg>'

CAT = {c["id"]: c for c in D["categories"]}

# ---------------------------------------------------------------- CSS
CSS = r"""
.aax{--f:#12491d;--f2:#0e3b17;--leaf:#2a7a3a;--mint:#a0e0a0;--gold:#f2d26b;--onGold:#3a2a06;--paper:#f4f1e8;--paper2:#ebe6d8;--ink:#14241a;--mut:#5a6b5d;--line:rgba(20,36,26,.12);--glass:rgba(255,255,255,.08);--gbrd:rgba(160,224,160,.28);
--disp:'Fraunces',Georgia,serif;--body:'Mulish',system-ui,-apple-system,'Segoe UI',sans-serif;
font-family:var(--body);color:var(--ink);background:var(--paper);line-height:1.55;-webkit-font-smoothing:antialiased;overflow-x:clip;font-size:16.5px}
.aax *,.aax *::before,.aax *::after{box-sizing:border-box}
.aax img{max-width:100%;display:block}
.aax a{color:inherit;text-decoration:none}
.aax button{font:inherit;color:inherit;white-space:normal;text-transform:none;letter-spacing:normal}
.aax .ic{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;flex:none}
.aax .w{width:100%;max-width:1240px;margin:0 auto;padding-inline:clamp(18px,4vw,40px)}
.aax .eyb{font-size:.74rem;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--leaf)}
.aax .dk .eyb{color:var(--mint)}
.aax h1,.aax h2,.aax h3{font-family:var(--disp);font-weight:600;letter-spacing:-.015em;line-height:1.04;margin:0;font-variation-settings:"opsz" 96}
.aax h2{font-size:clamp(2rem,4.2vw,3.3rem)}
.aax h2 em,.aax h1 em{font-style:italic;font-weight:500;color:var(--leaf)}
.aax .dk h2 em,.aax .dk h1 em{color:var(--mint)}
.aax .lead{color:var(--mut);font-size:1.08rem;max-width:58ch;margin:14px 0 0}
.aax .dk{background:var(--f);color:#eef5ee}
.aax .dk .lead{color:rgba(238,245,238,.72)}
.aax .btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;font-weight:800;font-size:.95rem;padding:14px 24px;border-radius:999px;border:0;cursor:pointer;transition:transform .2s,box-shadow .2s,background .2s;white-space:nowrap}
.aax .btn .ic{width:17px;height:17px;stroke-width:2}
.aax .btn-gold{background:var(--gold);color:var(--onGold);box-shadow:0 10px 26px -8px rgba(242,210,107,.7)}
.aax .btn-gold:hover{transform:translateY(-2px)}
.aax .btn-ghost{background:rgba(255,255,255,.08);color:#fff;border:1px solid rgba(255,255,255,.4);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
.aax .btn-ghost:hover{background:rgba(255,255,255,.16)}
.aax .btn-ink{background:var(--f2);color:#fff}
.aax .btn-ink:hover{background:var(--leaf)}
.aax .btn-line{border:1px solid var(--line);background:#fff;color:var(--ink)}
.aax .rv{opacity:0;transform:translateY(22px);transition:opacity .9s cubic-bezier(.2,.7,.2,1),transform .9s cubic-bezier(.2,.7,.2,1)}
.aax .rv.in{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.aax .rv{opacity:1;transform:none}.aax *{animation:none!important;transition:none!important}}

/* header (solo demo standalone) */
.aax .hdr{position:fixed;inset:0 0 auto;z-index:50;transition:background .35s,box-shadow .35s,padding .35s;padding:16px 0}
.aax .hdr .w{display:flex;align-items:center;gap:22px}
.aax .hdr.sc{background:rgba(18,73,29,.82);backdrop-filter:blur(16px) saturate(1.2);-webkit-backdrop-filter:blur(16px) saturate(1.2);box-shadow:0 1px 0 rgba(160,224,160,.18);padding:8px 0}
.aax .logo{display:inline-flex;align-items:center}
.aax .logo img{height:56px;width:auto;filter:drop-shadow(0 4px 14px rgba(0,0,0,.35));transition:height .35s}
.aax .hdr.sc .logo img{height:46px}
.aax .nav{display:flex;gap:26px;margin-left:auto;color:rgba(255,255,255,.88);font-weight:700;font-size:.93rem}
.aax .nav a:hover{color:var(--mint)}
.aax .hdr .btn{padding:10px 18px;font-size:.88rem}
.aax .burger{display:none;margin-left:auto;background:none;border:0;color:#fff;cursor:pointer;padding:6px}
.aax .burger .ic{width:26px;height:26px}
@media(max-width:860px){.aax .nav{display:none}.aax .hdr .btn{display:none}.aax .burger{display:block}
.aax .nav.open{display:flex;flex-direction:column;position:absolute;top:100%;left:12px;right:12px;background:rgba(18,73,29,.96);backdrop-filter:blur(16px);border:1px solid var(--gbrd);border-radius:18px;padding:18px 22px;gap:14px}}

/* hero */
.aax .hero{position:relative;min-height:min(100svh,920px);display:flex;align-items:center;color:#fff;overflow:hidden;background:var(--f)}
.aax .hero .sl{position:absolute;inset:0;background-size:cover;background-position:center;opacity:0;transform:scale(1.06);transition:opacity 2.4s ease,transform 9s ease-out}
.aax .hero .sl.on{opacity:1;transform:scale(1)}
.aax .hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(9,38,15,.55) 0%,rgba(9,38,15,.12) 32%,rgba(9,38,15,.35) 62%,rgba(9,38,15,.88) 100%),linear-gradient(90deg,rgba(9,38,15,.55),transparent 60%)}
.aax .hero .w{position:relative;z-index:2;padding-top:118px;padding-bottom:84px;display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:48px;align-items:center}
.aax .hbadge{display:inline-flex;align-items:center;gap:10px;padding:8px 14px 8px 10px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.26);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);font-weight:700;font-size:.84rem;margin-bottom:22px}
.aax .stars{display:inline-flex;gap:1px;color:var(--gold)}
.aax .stars .ic{width:14px;height:14px;fill:currentColor;stroke:none}
.aax .hero h1{font-size:clamp(2.9rem,7vw,5.9rem);font-weight:600;max-width:12ch;text-shadow:0 2px 40px rgba(0,0,0,.35)}
.aax .hero h1 em{color:var(--mint)}
.aax .hero .sub{font-size:clamp(1.05rem,1.5vw,1.25rem);color:rgba(255,255,255,.92);max-width:44ch;margin:20px 0 0}
.aax .pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:28px}
.aax .pill{height:32px;display:inline-flex;align-items:center;gap:7px;padding:0 13px;border-radius:999px;font-size:13px;font-weight:700;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.28);color:#fff;cursor:pointer;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);transition:background .2s,border-color .2s}
.aax .pill .ic{width:14px;height:14px}
.aax .pill:hover{background:rgba(160,224,160,.22);border-color:var(--mint)}
/* buscador */
.aax .finder{background:rgba(14,59,23,.42);border:1px solid var(--gbrd);border-radius:24px;padding:22px;backdrop-filter:blur(22px) saturate(1.15);-webkit-backdrop-filter:blur(22px) saturate(1.15);box-shadow:0 30px 70px -20px rgba(0,0,0,.55)}
.aax .finder .fh{display:flex;align-items:center;justify-content:space-between;margin-bottom:4px}
.aax .finder .fh b{font-family:var(--disp);font-weight:600;font-size:1.35rem}
.aax .live{display:inline-flex;align-items:center;gap:6px;font-size:.68rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mint)}
.aax .live i{width:7px;height:7px;border-radius:50%;background:var(--mint);box-shadow:0 0 0 0 rgba(160,224,160,.7);animation:pulse 2s infinite}
@keyframes pulse{70%{box-shadow:0 0 0 8px rgba(160,224,160,0)}100%{box-shadow:0 0 0 0 rgba(160,224,160,0)}}
.aax .finder p{margin:0 0 16px;font-size:.86rem;color:rgba(255,255,255,.7)}
.aax .fld{display:flex;align-items:center;gap:11px;padding:10px 14px;border-radius:14px;background:rgba(255,255,255,.07);border:1px solid rgba(160,224,160,.2);margin-bottom:10px;transition:border-color .2s}
.aax .fld:focus-within{border-color:var(--mint)}
.aax .fld .ic{color:var(--mint)}
.aax .fld label{display:block;font-size:.66rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.6)}
.aax .fld select,.aax .fld input{width:100%;background:transparent;border:0;outline:0;color:#fff;font:700 .96rem var(--body);padding:2px 0;appearance:none;-webkit-appearance:none;color-scheme:dark}
.aax .fld select option{color:#14241a}
.aax .fld>div{flex:1;min-width:0}
.aax .frow{display:grid;grid-template-columns:1.25fr 1fr;gap:10px}
.aax .frow .fld{margin-bottom:0}
.aax .pax{display:flex;align-items:center;justify-content:space-between}
.aax .pax button{width:28px;height:28px;min-width:0;min-height:0;padding:0;margin:0;border-radius:50%;border:1px solid rgba(255,255,255,.35);background:none;color:#fff;cursor:pointer;display:grid;place-items:center;flex:none;box-shadow:none}
.aax .pax button:hover,.aax .pax button:focus{background:rgba(255,255,255,.14);color:#fff;border-color:rgba(255,255,255,.6)}
.aax .pax button .ic{width:14px;height:14px;stroke-width:2.2}
.aax .pax output{min-width:2ch;text-align:center}
.aax .pax output{font-weight:800}
.aax .finder .btn{width:100%;margin-top:14px}
.aax .fnote{display:flex;align-items:center;justify-content:center;gap:7px;margin-top:12px;font-size:.76rem;color:rgba(255,255,255,.7)}
.aax .fnote .ic{width:14px;height:14px;color:var(--mint)}
.aax .dots{position:absolute;z-index:3;left:50%;bottom:18px;transform:translateX(-50%);display:flex;gap:8px}
.aax .dots i{width:26px;height:3px;border-radius:3px;background:rgba(255,255,255,.35);overflow:hidden;position:relative}
.aax .dots i.on::after{content:"";position:absolute;inset:0;background:#fff;animation:fill 7s linear forwards}
@keyframes fill{from{transform:translateX(-100%)}to{transform:none}}
@media(max-width:1000px){.aax .hero .w{grid-template-columns:1fr;gap:30px}.aax .finder{max-width:460px}}

/* cinta */
.aax .tape{background:var(--gold);color:var(--onGold);overflow:hidden;padding:13px 0;font-weight:800;font-size:.92rem;white-space:nowrap}
.aax .tape .tr{display:inline-flex;gap:0;animation:tape 38s linear infinite}
.aax .tape span{display:inline-flex;align-items:center;gap:12px;padding:0 22px}
.aax .tape span::after{content:"";width:6px;height:6px;border-radius:50%;background:var(--onGold);opacity:.45;margin-left:22px}
@keyframes tape{to{transform:translateX(-50%)}}

/* tipos de dia */
.aax .sec{padding:clamp(64px,9vw,120px) 0}
.aax .shd{display:flex;align-items:flex-end;justify-content:space-between;gap:30px;margin-bottom:40px;flex-wrap:wrap}
.aax .moods{display:grid;grid-template-columns:repeat(12,1fr);grid-auto-rows:150px;gap:14px}
.aax .mood{position:relative;border-radius:22px;overflow:hidden;color:#fff;display:flex;align-items:flex-end;padding:20px;cursor:pointer;isolation:isolate;border:0;text-align:left;background:var(--f)}
.aax .mood .bg{position:absolute;inset:0;background-size:cover;background-position:center;z-index:-2;transition:transform 1.1s cubic-bezier(.2,.7,.2,1)}
.aax .mood::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,transparent 30%,rgba(9,38,15,.85))}
.aax .mood:hover .bg{transform:scale(1.07)}
.aax .mood:hover,.aax .mood:focus{background:var(--f);color:#fff}
.aax .mood b{display:block;font-family:var(--disp);font-weight:600;font-size:1.55rem;line-height:1.05}
.aax .mood small{display:block;font-size:.84rem;color:rgba(255,255,255,.82);margin-top:5px;max-width:30ch}
.aax .mood .ct{position:absolute;top:16px;right:16px;font-size:.72rem;font-weight:800;padding:5px 10px;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.3);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.aax .mood .mi{position:absolute;top:16px;left:16px;width:38px;height:38px;border-radius:12px;display:grid;place-items:center;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.28);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.aax .m1{grid-column:span 5;grid-row:span 3}.aax .m2{grid-column:span 4;grid-row:span 2}.aax .m3{grid-column:span 3;grid-row:span 2}
.aax .m4{grid-column:span 3;grid-row:span 1}.aax .m5{grid-column:span 4;grid-row:span 1}
@media(max-width:860px){.aax .moods{grid-template-columns:1fr 1fr;grid-auto-rows:170px}.aax .m1{grid-column:span 2;grid-row:span 2}.aax .m2,.aax .m3,.aax .m4,.aax .m5{grid-column:span 1;grid-row:span 1}.aax .m4,.aax .m5{grid-column:span 1}.aax .mood b{font-size:1.25rem}.aax .mood small{font-size:.78rem}.aax .mood{padding:16px}}
@media(max-width:420px){.aax .moods{grid-auto-rows:150px}.aax .mood b{font-size:1.12rem}.aax .mood small{display:none}.aax .m1 small{display:block}}

/* asistente */
.aax .asst{display:grid;grid-template-columns:1fr minmax(0,520px);gap:clamp(30px,6vw,90px);align-items:center}
.aax .asst .copy p{max-width:44ch}
.aax .asst .hint{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.aax .asst .hint button{height:32px;padding:0 13px;border-radius:999px;font-size:13px;font-weight:700;border:1px solid rgba(160,224,160,.35);background:rgba(160,224,160,.08);color:#eaf4ea;cursor:pointer}
.aax .asst .hint button:hover{background:rgba(160,224,160,.18)}
.aax .chat{border-radius:26px;overflow:hidden;background:rgba(255,255,255,.06);border:1px solid var(--gbrd);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);box-shadow:0 40px 80px -30px rgba(0,0,0,.6);display:flex;flex-direction:column;height:440px}
.aax .chat .top{display:flex;align-items:center;gap:12px;padding:14px 18px;background:rgba(0,0,0,.18);border-bottom:1px solid rgba(160,224,160,.16)}
.aax .chat .av{width:40px;height:40px;border-radius:50%;background:var(--paper);display:grid;place-items:center;overflow:hidden;flex:none}
.aax .chat .av img{width:34px;height:auto}
.aax .chat .top b{display:block;font-size:.96rem}
.aax .chat .top small{display:flex;align-items:center;gap:6px;font-size:.76rem;color:var(--mint)}
.aax .chat .top small i{width:7px;height:7px;border-radius:50%;background:#5ee07a}
.aax .chat .log{flex:1;overflow-y:auto;padding:18px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth;background:radial-gradient(600px 300px at 80% 0%,rgba(160,224,160,.06),transparent)}
.aax .chat .empty{margin:auto;text-align:center;color:rgba(255,255,255,.5);font-size:.88rem;max-width:30ch}
.aax .chat .empty .ic{width:30px;height:30px;margin:0 auto 10px;opacity:.6}
.aax .msg{max-width:84%;padding:10px 14px;border-radius:16px;font-size:.93rem;line-height:1.45;animation:pop .35s cubic-bezier(.2,.8,.2,1)}
@keyframes pop{from{opacity:0;transform:translateY(8px) scale(.98)}}
.aax .msg.me{align-self:flex-end;background:#d9fdd3;color:#14241a;border-bottom-right-radius:5px}
.aax .msg.bot{align-self:flex-start;background:rgba(255,255,255,.92);color:#14241a;border-bottom-left-radius:5px}
.aax .msg .tm{display:block;text-align:right;font-size:.66rem;opacity:.5;margin-top:3px}
.aax .typing{align-self:flex-start;background:rgba(255,255,255,.92);border-radius:16px;padding:12px 14px;display:flex;gap:4px}
.aax .typing i{width:6px;height:6px;border-radius:50%;background:#7a8a7d;animation:tp 1.2s infinite}
.aax .typing i:nth-child(2){animation-delay:.15s}.aax .typing i:nth-child(3){animation-delay:.3s}
@keyframes tp{0%,60%,100%{opacity:.3;transform:none}30%{opacity:1;transform:translateY(-3px)}}
.aax .sug{display:flex;gap:10px;align-items:center;margin-top:8px;padding:8px;border-radius:12px;background:#f4f1e8;color:#14241a;border:1px solid var(--line)}
.aax .sug img{width:58px;height:46px;border-radius:9px;object-fit:cover;flex:none}
.aax .sug b{display:block;font-size:.86rem;line-height:1.2}
.aax .sug small{font-size:.76rem;color:var(--mut)}
.aax .sug a{margin-left:auto;font-size:.76rem;font-weight:800;background:var(--f2);color:#fff;padding:7px 11px;border-radius:999px;white-space:nowrap}
.aax .chat form{display:flex;gap:8px;padding:12px;background:rgba(0,0,0,.18);border-top:1px solid rgba(160,224,160,.16)}
.aax .chat input{flex:1;min-width:0;border-radius:999px;border:1px solid rgba(160,224,160,.25);background:rgba(255,255,255,.95);color:#14241a;padding:12px 16px;font:600 .95rem var(--body);outline:0}
.aax .chat form button{width:46px;height:46px;border-radius:50%;border:0;background:var(--gold);color:var(--onGold);display:grid;place-items:center;cursor:pointer;flex:none}
@media(max-width:900px){.aax .asst{grid-template-columns:1fr}.aax .chat{height:420px}}

/* tours */
.aax .filt{display:flex;flex-wrap:wrap;gap:8px}
.aax .filt button{height:36px;padding:0 15px;border-radius:999px;border:1px solid var(--line);background:#fff;font-weight:700;font-size:.86rem;cursor:pointer;transition:all .2s}
.aax .filt button.on{background:var(--f2);color:#fff;border-color:var(--f2)}
.aax .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.aax .tc{position:relative;display:flex;flex-direction:column;border-radius:22px;overflow:hidden;background:#fff;border:1px solid var(--line);transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s}
.aax .tc:hover{transform:translateY(-6px);box-shadow:0 30px 60px -28px rgba(18,73,29,.45)}
.aax .tc .ph{position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--paper2)}
.aax .tc .ph img{width:100%;height:100%;object-fit:cover;transition:transform 1s cubic-bezier(.2,.7,.2,1)}
.aax .tc:hover .ph img{transform:scale(1.06)}
.aax .tag{position:absolute;top:14px;left:14px;font-size:.7rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase;padding:6px 11px;border-radius:999px;background:var(--mint);color:var(--f2)}
.aax .tc .meta{position:absolute;left:12px;right:12px;bottom:12px;display:flex;gap:6px;flex-wrap:wrap}
.aax .tc .meta span{display:inline-flex;align-items:center;gap:5px;font-size:.74rem;font-weight:700;color:#fff;padding:5px 10px;border-radius:999px;background:rgba(14,59,23,.45);border:1px solid rgba(255,255,255,.25);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
.aax .tc .meta .ic{width:13px;height:13px}
.aax .tc .bd{padding:18px 20px 20px;display:flex;flex-direction:column;gap:8px;flex:1}
.aax .tc h3{font-size:1.42rem;line-height:1.1}
.aax .tc p{margin:0;font-size:.92rem;color:var(--mut)}
.aax .tc .ft{margin-top:auto;padding-top:14px;display:flex;align-items:flex-end;justify-content:space-between;gap:10px;border-top:1px dashed var(--line)}
.aax .pr small{display:block;font-size:.66rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.aax .pr b{font-family:var(--disp);font-size:1.7rem;font-weight:600;line-height:1}
.aax .pr span{font-size:.8rem;color:var(--mut);font-weight:700}
.aax .tc .go{display:inline-flex;align-items:center;gap:6px;font-weight:800;font-size:.86rem;color:var(--f2)}
.aax .tc .go .ic{width:16px;height:16px;transition:transform .25s}
.aax .tc:hover .go .ic{transform:translateX(4px)}
.aax .tc.big{grid-column:span 2;flex-direction:row}
.aax .tc.big .ph{aspect-ratio:auto;flex:1.15}
.aax .tc.big .bd{flex:1;padding:30px}
.aax .tc.big h3{font-size:2rem}
.aax .tc.hide{display:none}
.aax .tc.cta{background:var(--f2);color:#fff;border-color:transparent;background-image:radial-gradient(400px 260px at 100% 0%,rgba(160,224,160,.2),transparent 60%)}
.aax .tc.cta .bd{justify-content:center;padding:30px;gap:12px}
.aax .tc.cta p{color:rgba(255,255,255,.75)}.aax .tc.cta .go{color:var(--mint)}
.aax .tc.cta .mi2{width:48px;height:48px;border-radius:14px;display:grid;place-items:center;background:rgba(255,255,255,.1);border:1px solid rgba(160,224,160,.3);color:var(--gold)}
.aax .tc.cta .mi2 .ic{width:24px;height:24px}
@media(max-width:1000px){.aax .grid{grid-template-columns:1fr 1fr}}
@media(max-width:640px){.aax .grid{grid-template-columns:1fr}.aax .tc.big{grid-column:auto;flex-direction:column}.aax .tc.big .ph{aspect-ratio:4/3}.aax .tc.big .bd{padding:20px}.aax .tc.big h3{font-size:1.5rem}}

/* combos (acordeon) */
.aax .combos{margin-top:72px}
.aax .acc{border-top:1px solid var(--line)}
.aax .acc details{border-bottom:1px solid var(--line)}
.aax .acc summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:14px;padding:20px 4px;font-family:var(--disp);font-size:1.45rem;font-weight:600}
.aax .acc summary::-webkit-details-marker{display:none}
.aax .acc summary small{font-family:var(--body);font-size:.8rem;font-weight:700;color:var(--mut);margin-left:auto}
.aax .acc summary .pl{width:30px;height:30px;border-radius:50%;border:1px solid var(--line);display:grid;place-items:center;transition:transform .3s;flex:none}
.aax .acc details[open] summary .pl{transform:rotate(45deg);background:var(--mint);border-color:var(--mint)}
.aax .acc .rows{padding:0 0 18px;display:grid;gap:8px}
.aax .crow{display:flex;align-items:center;gap:14px;padding:10px 12px;border-radius:14px;background:#fff;border:1px solid var(--line);transition:border-color .2s,transform .2s}
.aax .crow:hover{border-color:var(--leaf);transform:translateX(4px)}
.aax .crow img{width:56px;height:44px;border-radius:9px;object-fit:cover;flex:none}
.aax .crow b{font-size:.96rem;display:block;line-height:1.2}
.aax .crow small{font-size:.78rem;color:var(--mut)}
.aax .crow .pr2{margin-left:auto;text-align:right;font-weight:800;font-size:.95rem;white-space:nowrap}
.aax .crow .pr2 small{display:block;font-weight:700}
@media(max-width:860px){.aax .combos{grid-template-columns:1fr}}

/* combos visibles */
.aax .chead{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:40px;align-items:end;margin-bottom:30px}
.aax .chead .lead{margin:0}
.aax .cgrid{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}
.aax .cgrp{border-radius:24px;background:#fff;border:1px solid var(--line);padding:12px}
.aax .cgh{display:flex;align-items:center;gap:14px;padding:6px 8px 14px}
.aax .cgh img{width:54px;height:54px;border-radius:14px;object-fit:cover}
.aax .cgh b{display:block;font-family:var(--disp);font-size:1.45rem;font-weight:600;line-height:1.1}
.aax .cgh small{font-size:.82rem;color:var(--mut);font-weight:700}
.aax .cgrp .rows{display:grid;gap:6px}
.aax .cgrp .crow{background:var(--paper);border-color:transparent;padding:8px 12px}
.aax .cgrp .crow img{width:46px;height:38px}
.aax .cgrp .crow b{font-size:.92rem}
.aax .cask{display:grid;grid-template-columns:auto 1fr;gap:2px 14px;align-items:center;margin-top:12px;padding:16px 18px;border-radius:16px;background:var(--f2);color:#fff;transition:transform .2s}
.aax .cask:hover{transform:translateY(-2px)}
.aax .cask span{grid-row:span 2;width:40px;height:40px;border-radius:12px;display:grid;place-items:center;background:rgba(255,255,255,.1);color:var(--gold)}
.aax .cask small{color:rgba(255,255,255,.75);font-size:.84rem}
@media(max-width:860px){.aax .chead,.aax .cgrid{grid-template-columns:1fr}}
.aax .cgrp .crow .pr2 b{display:inline}
.aax .cgrp .crow.cmb{display:grid;grid-template-columns:auto 1fr auto auto;gap:16px;align-items:center;padding:14px 16px;background:#fff;border:1px solid var(--line);border-radius:18px}
.aax .cgrp .crow.cmb:hover{border-color:var(--f);transform:translateY(-2px);box-shadow:0 14px 30px -18px rgba(18,73,29,.45)}
.aax .cgrp .rows{gap:10px}
.aax .cimgs{position:relative;width:104px;height:72px;flex:none}
.aax .cgrp .cimgs img{position:absolute;width:64px;height:64px;border-radius:14px;object-fit:cover;border:2px solid #fff;box-shadow:0 6px 14px -6px rgba(0,0,0,.35)}
.aax .cgrp .cimgs img:first-child{left:0;top:0}
.aax .cgrp .cimgs img:last-child{left:40px;top:8px}
.aax .crow.cmb .cn{font-family:var(--disp);font-weight:600;font-size:1.18rem;line-height:1.2;display:block;color:var(--ink)}
.aax .crow.cmb .cn i{font-style:normal;color:var(--leaf);padding:0 2px}
.aax .crow.cmb .ct small{display:block;margin-top:5px;font-size:.8rem;color:var(--mut);font-weight:700}
.aax .crow.cmb .pr2{display:flex;flex-direction:column;align-items:flex-end;line-height:1.1;margin:0}
.aax .crow.cmb .pr2 .fr{font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);font-weight:800}
.aax .crow.cmb .pr2 .pv{font-family:var(--disp);font-size:1.5rem;font-weight:600;display:block;margin:2px 0}
.aax .crow.cmb .pr2 small{font-size:.74rem;color:var(--mut);font-weight:700}
.aax .crow.cmb .cgo{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:var(--f);color:#fff;transition:background .2s}
.aax .crow.cmb:hover .cgo{background:var(--gold);color:var(--onGold)}
@media(max-width:560px){.aax .cgrp .crow.cmb{grid-template-columns:auto 1fr auto;gap:12px;padding:12px}.aax .crow.cmb .cgo{display:none}.aax .cimgs{width:84px;height:60px}.aax .cgrp .cimgs img{width:52px;height:52px}.aax .cgrp .cimgs img:last-child{left:32px;top:8px}.aax .crow.cmb .cn{font-size:1.02rem}.aax .crow.cmb .pr2 .pv{font-size:1.25rem}}

.aax .cgrp .crow b{font-size:1rem}
/* card grande */
.aax .bhl{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:8px}
.aax .bhl li{display:flex;gap:10px;font-size:.93rem;color:#2c3b30}
.aax .bhl .ic{color:var(--leaf);margin-top:2px}
.aax .bch{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}
.aax .bch span{display:inline-flex;align-items:center;gap:6px;font-size:.78rem;font-weight:700;padding:6px 11px;border-radius:999px;background:var(--paper);color:var(--f2)}
.aax .bch .ic{width:14px;height:14px}
/* Tripadvisor */
.aax .hbadge.ta{text-decoration:none}
.aax .hbadge.ta:hover{background:rgba(255,255,255,.18)}
.aax .tai{display:inline-block;width:20px;height:20px;flex:none;border-radius:50%;background:url("data:image/webp;base64,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") center/contain no-repeat}
.aax .tai.lg{width:34px;height:34px}
.aax .bub{display:inline-flex;gap:3px}.aax .bub svg{width:15px;height:15px}
.aax .bub.sm svg{width:14px;height:14px}.aax .bub.lg svg{width:24px;height:24px}
.aax .score .talogo{display:flex;align-items:center;gap:10px;margin-bottom:16px;font-weight:800;font-size:1.25rem;color:#fff;letter-spacing:-.01em}
.aax .score .big{font-size:clamp(2.2rem,3.4vw,2.8rem);line-height:1;margin-bottom:8px}
.aax .score .cnt{margin:10px 0 6px;color:#fff}
.aax .rc .rh{display:flex;align-items:center;gap:11px}
.aax .rc .rh .av{position:relative;width:40px;height:40px;border-radius:50%;overflow:hidden;background:var(--mint);flex:none}
.aax .rc .rh .av i{position:absolute;inset:0;display:grid;place-items:center;font-style:normal;font-weight:800;color:var(--f2)}
.aax .rc .rh .av img{position:relative;width:100%;height:100%;object-fit:cover;background:#fff}
.aax .rc .rh b{display:block;font-size:.93rem}.aax .rc .rh small{color:rgba(238,245,238,.6);font-size:.78rem}
.aax .rc .rh .tai{margin-left:auto;width:24px;height:24px}
.aax .rc .rt{font-family:var(--disp);font-weight:600;font-size:1.15rem;line-height:1.25;color:#fff}
.aax .rc .rx{margin:0;font-size:.93rem;line-height:1.55;color:rgba(238,245,238,.85);display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden}
.aax .rc.open .rx{-webkit-line-clamp:unset;display:block}
.aax .rc .more{align-self:flex-start;background:none;border:0;padding:0;color:var(--mint);font-weight:800;font-size:.84rem;cursor:pointer}
.aax .rc .vr{margin-top:auto;font-size:.76rem;font-weight:700;color:var(--mint)}
/* carrusel de reseñas */
.aax .rwrap{min-width:0}
.aax .rtrack{scrollbar-width:none;-webkit-mask-image:linear-gradient(90deg,#000 82%,transparent);mask-image:linear-gradient(90deg,#000 82%,transparent);transition:-webkit-mask-image .3s}
.aax .rtrack::-webkit-scrollbar{display:none}
.aax .rtrack.end{-webkit-mask-image:none;mask-image:none}
.aax .rnav{display:flex;align-items:center;gap:14px;margin-top:22px}
.aax .rbtn{width:48px;height:48px;border-radius:50%;display:grid;place-items:center;cursor:pointer;color:#fff;background:rgba(255,255,255,.08);border:1px solid var(--gbrd);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);transition:background .2s,opacity .2s,transform .2s}
.aax .rbtn:hover:not(:disabled){background:var(--gold);color:var(--onGold);border-color:var(--gold)}
.aax .rbtn:disabled{opacity:.3;cursor:default}
.aax .rbtn.prev .ic{transform:rotate(180deg)}
.aax .rbtn .ic{width:20px;height:20px;stroke-width:2}
.aax .rdots{display:flex;gap:6px;flex:1}
.aax .rdots i{height:4px;flex:1;max-width:36px;border-radius:4px;background:rgba(255,255,255,.2);transition:background .3s}
.aax .rdots i.on{background:var(--mint)}
.aax .rcount{font-size:.82rem;font-weight:700;color:rgba(238,245,238,.6);white-space:nowrap}
.aax .rbtn.nudge{animation:nudge 1.6s ease-in-out 2}
@keyframes nudge{0%,100%{transform:none}50%{transform:translateX(6px)}}
/* franja Driver Costa Rica (colores de Driver) */
.aax .drv{--dg:#3D590E;--dl:#D0EDA2;--dp:#F0F3E4;background:var(--dl);color:var(--dg);padding:clamp(56px,7vw,88px) 0;position:relative;overflow:hidden}
.aax .drv::before{content:"";position:absolute;right:-120px;top:-140px;width:420px;height:420px;border-radius:50%;background:rgba(255,255,255,.35)}
.aax .dgrid{position:relative;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,5vw,72px);align-items:center}
.aax .dlogo img{height:58px;width:auto;margin-bottom:22px}
.aax .deyb{font-family:Poppins,sans-serif;font-size:.78rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;opacity:.8}
.aax .dh{font-family:Poppins,sans-serif;font-weight:700;font-size:clamp(1.9rem,3.6vw,2.9rem);line-height:1.08;letter-spacing:-.02em;color:var(--dg);margin:10px 0 0;font-variation-settings:normal}
.aax .dh span{display:block;color:#fff;text-shadow:0 1px 0 rgba(61,89,14,.08)}
.aax .dcopy p{font-family:Poppins,sans-serif;font-size:1.02rem;line-height:1.6;max-width:46ch;margin:16px 0 0;color:var(--dg)}
.aax .dbtn{display:inline-flex;align-items:center;gap:10px;margin-top:26px;padding:14px 24px;border-radius:999px;background:var(--dg);color:#fff;font-family:Poppins,sans-serif;font-weight:600;font-size:.95rem;transition:transform .2s}
.aax .dbtn:hover{transform:translateY(-2px)}
.aax .dbtn .ic{width:17px;height:17px;stroke-width:2}
.aax .droutes{display:grid;gap:10px;padding:14px;border-radius:24px;background:rgba(255,255,255,.45);border:1px solid rgba(255,255,255,.7);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
.aax .drow{display:grid;grid-template-columns:1fr auto auto;align-items:center;gap:16px;padding:14px 18px;border-radius:16px;background:var(--dp);transition:transform .2s,background .2s;font-family:Poppins,sans-serif}
.aax .drow:hover{transform:translateX(4px);background:#fff}
.aax .dft small,.aax .dpr small{display:block;font-size:.72rem;font-weight:500;opacity:.75}
.aax .dft b{font-weight:600;font-size:1rem}
.aax .dsw{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;background:var(--dl)}
.aax .dsw .ic{width:16px;height:16px;stroke-width:2}
.aax .dpr{text-align:right}.aax .dpr b{font-weight:700;font-size:1.15rem}
.aax .dnote{display:flex;align-items:center;gap:8px;padding:6px 6px 2px;font-family:Poppins,sans-serif;font-size:.8rem;font-weight:500}
@media(max-width:860px){.aax .dgrid{grid-template-columns:1fr}.aax .drv::before{display:none}}
/* franja foto real */
.aax .band{position:relative;min-height:560px;display:flex;align-items:center;overflow:hidden;color:#fff;background:var(--f)}
.aax .band .bimg{position:absolute;inset:-8% 0;background-size:cover;background-position:center;will-change:transform}
.aax .band::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(9,38,15,.7),rgba(9,38,15,.15) 70%)}
.aax .band .w{position:relative;z-index:2}
.aax .bcard{max-width:480px;padding:34px;border-radius:26px;background:rgba(14,59,23,.38);border:1px solid var(--gbrd);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)}
.aax .bcard .eyb{color:var(--mint)}
.aax .bcard h2 em{color:var(--mint)}
.aax .bcard p{color:rgba(255,255,255,.85);margin:14px 0 0;font-size:1.05rem}
/* resenas */
.aax .revs{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,2fr);gap:clamp(24px,5vw,70px);align-items:start}
.aax .score{border-radius:24px;padding:28px;background:rgba(255,255,255,.06);border:1px solid var(--gbrd);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px)}
.aax .score .big{font-family:var(--disp);font-size:4.4rem;font-weight:600;line-height:1}
.aax .score .stars .ic{width:20px;height:20px}
.aax .score p{color:rgba(238,245,238,.72);margin:12px 0 18px;font-size:.92rem}
.aax .rtrack{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(290px,1fr);gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px;scrollbar-width:thin}
.aax .rc{scroll-snap-align:start;border-radius:22px;padding:24px;background:rgba(255,255,255,.06);border:1px solid rgba(160,224,160,.2);display:flex;flex-direction:column;gap:14px}
.aax .rc q{font-family:var(--disp);font-size:1.18rem;line-height:1.35;font-weight:500;quotes:none;color:#fff}
.aax .rc .who{margin-top:auto;display:flex;align-items:center;gap:11px;font-size:.86rem}
.aax .rc .who i{width:36px;height:36px;border-radius:50%;background:var(--mint);color:var(--f2);display:grid;place-items:center;font-style:normal;font-weight:800}
.aax .rc .who small{display:block;color:rgba(238,245,238,.6)}
@media(max-width:860px){.aax .revs{grid-template-columns:1fr}}

/* footer claro */
.aax .foot{background:var(--paper);border-top:1px solid var(--line);padding:64px 0 28px;color:var(--ink)}
.aax .foot .cols{display:grid;grid-template-columns:1.3fr 1fr 1fr 1.1fr;gap:34px}
.aax .foot h4{font-size:.74rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--leaf);margin:0 0 14px}
.aax .foot ul{list-style:none;margin:0;padding:0;display:grid;gap:9px;font-size:.93rem}
.aax .foot ul a:hover{color:var(--leaf)}
.aax .foot .fl img{height:64px;width:auto}
.aax .foot .fl p{color:var(--mut);font-size:.92rem;max-width:34ch;margin:14px 0 0}
.aax .foot li{display:flex;align-items:center;gap:9px}
.aax .foot .soc{display:flex;gap:10px;margin-top:20px}
.aax .foot .soc a{width:40px;height:40px;border-radius:50%;display:grid;place-items:center;border:1px solid var(--line);color:var(--f);background:rgba(255,255,255,.5);transition:background .2s,color .2s,border-color .2s}
.aax .foot .soc a:hover{background:var(--f);color:var(--mint);border-color:var(--f)}
.aax .foot .soc .ic{width:18px;height:18px}
.aax .foot li .ic{color:var(--leaf)}
.aax .foot{background:var(--mint);border-top:0;color:var(--f2)}
.aax .foot h4,.aax .foot li .ic,.aax .foot .secure .ic{color:var(--f)}
.aax .foot .fl p,.aax .foot .legal{color:rgba(14,59,23,.78)}
.aax .foot .secure{color:var(--f2)}
.aax .foot ul a:hover{color:var(--f);text-decoration:underline;text-underline-offset:3px}
.aax .foot .legal{border-top-color:rgba(18,73,29,.22)}
.aax .legal .rzl{font-weight:800;color:var(--f);text-decoration:underline;text-decoration-color:rgba(18,73,29,.35);text-underline-offset:3px}
.aax .legal .rzl:hover{text-decoration-color:var(--f)}
.aax .foot .soc a{border-color:rgba(18,73,29,.25);background:rgba(255,255,255,.4)}
.aax .pay{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:6px}
.aax .pay svg{height:28px;width:auto;border-radius:5px;box-shadow:0 0 0 1px var(--line)}
.aax .secure{display:flex;align-items:center;gap:8px;font-size:.84rem;font-weight:700;color:var(--ink);margin-bottom:12px}
.aax .secure .ic{color:var(--leaf)}
.aax .legal{margin-top:44px;padding-top:20px;border-top:1px solid var(--line);display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:.8rem;color:var(--mut)}
@media(max-width:860px){.aax .foot .cols{grid-template-columns:1fr 1fr}.aax .foot .fl{grid-column:span 2}}

/* boton flotante */
.aax .fab{position:fixed;right:20px;bottom:20px;z-index:60;display:flex;align-items:center;gap:10px;padding:12px 18px 12px 14px;border-radius:999px;background:var(--f2);color:#fff;font-weight:800;font-size:.9rem;border:1px solid rgba(160,224,160,.4);box-shadow:0 16px 40px -12px rgba(0,0,0,.5);cursor:pointer;transition:transform .25s}
.aax .fab:hover{transform:translateY(-3px)}
.aax .fab .ic{width:22px;height:22px;color:var(--mint)}

/* ===== pagina de tour ===== */
.aax .thero{position:relative;min-height:72svh;display:flex;align-items:flex-end;color:#fff;background:var(--f) center/cover no-repeat}
.aax .thero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(9,38,15,.5),rgba(9,38,15,.05) 35%,rgba(9,38,15,.85))}
.aax .thero .w{position:relative;z-index:2;padding-top:140px;padding-bottom:44px}
.aax .crumb{font-size:.76rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--mint);margin-bottom:16px}
.aax .crumb a:hover{color:#fff}
.aax .thero h1{font-size:clamp(2.6rem,6vw,5rem);max-width:16ch}
.aax .thero .sub{font-size:1.18rem;color:rgba(255,255,255,.9);max-width:52ch;margin:16px 0 0}
.aax .facts{position:relative;z-index:3;margin-top:-1px;background:var(--f);color:#fff}
.aax .facts .row{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid rgba(160,224,160,.18)}
.aax .fact{display:flex;align-items:center;gap:12px;padding:18px 16px;border-right:1px solid rgba(160,224,160,.14)}
.aax .fact:last-child{border-right:0}
.aax .fact .ic{width:22px;height:22px;color:var(--mint)}
.aax .fact small{display:block;font-size:.66rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.6)}
.aax .fact b{font-size:.98rem;line-height:1.25;display:block}
@media(max-width:760px){.aax .facts .row{grid-template-columns:1fr 1fr}.aax .fact:nth-child(2){border-right:0}.aax .fact:nth-child(-n+2){border-bottom:1px solid rgba(160,224,160,.14)}}
.aax .lay{display:grid;grid-template-columns:minmax(0,1fr) 420px;gap:clamp(28px,5vw,64px);align-items:start;padding-top:clamp(48px,7vw,84px);padding-bottom:clamp(48px,7vw,84px)}
.aax .blk{margin-bottom:52px}
.aax .blk h2{font-size:clamp(1.7rem,3vw,2.3rem);margin-bottom:16px}
.aax .blk>p{font-size:1.06rem;color:#2c3b30;max-width:66ch;margin:0 0 14px}
.aax .hl{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:10px}
.aax .hl li{display:flex;gap:11px;align-items:flex-start;padding:14px 16px;border-radius:16px;background:#fff;border:1px solid var(--line);font-weight:600;font-size:.95rem}
.aax .hl .ic{color:var(--leaf);margin-top:2px}
.aax .gal{display:grid;grid-template-columns:2fr 1fr;grid-template-rows:1fr 1fr;gap:10px;height:420px}
.aax .gal div{border-radius:18px;background:var(--paper2) center/cover}
.aax .gal div:first-child{grid-row:span 2}
.aax .tl{list-style:none;padding:0;margin:0;position:relative}
.aax .tl li{position:relative;padding:0 0 22px 46px;font-weight:700}
.aax .tl li::before{content:counter(list-item);position:absolute;left:0;top:-3px;width:30px;height:30px;border-radius:50%;background:var(--f2);color:#fff;display:grid;place-items:center;font-size:.82rem;font-weight:800}
.aax .tl li:not(:last-child)::after{content:"";position:absolute;left:14.5px;top:30px;bottom:2px;width:1px;background:var(--line)}
.aax .inc{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.aax .inc>div{padding:20px;border-radius:18px;background:#fff;border:1px solid var(--line)}
.aax .inc h3{font-family:var(--body);font-size:.78rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;margin-bottom:10px;color:var(--leaf)}
.aax .inc ul{list-style:none;margin:0;padding:0;display:grid;gap:8px;font-size:.95rem}
.aax .inc li{display:flex;gap:9px}
.aax .inc .no .ic{color:#a3574f}
.aax .inc .yes .ic{color:var(--leaf)}
.aax .bring{padding:20px 22px;border-radius:18px;background:var(--paper2);font-size:1rem}
.aax .faq details{border-bottom:1px solid var(--line)}
.aax .faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:14px;padding:18px 2px;font-weight:800}
.aax .faq summary::-webkit-details-marker{display:none}
.aax .faq summary .ic{transition:transform .3s}
.aax .faq details[open] summary .ic{transform:rotate(45deg)}
.aax .faq p{margin:0 0 18px;color:var(--mut)}
.aax .book{position:sticky;top:92px;border-radius:26px;background:#fff;border:1px solid var(--line);box-shadow:0 30px 70px -40px rgba(18,73,29,.55);overflow:hidden}
.aax .book .bh{padding:22px 24px 16px;background:linear-gradient(160deg,var(--f2),var(--f));color:#fff}
.aax .book .bh small{font-size:.68rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--mint)}
.aax .book .bh .amt{font-family:var(--disp);font-size:2.6rem;font-weight:600;line-height:1}
.aax .book .bh .amt span{font-family:var(--body);font-size:.95rem;font-weight:700;color:rgba(255,255,255,.7)}
.aax .book .bh .ch{font-size:.88rem;color:rgba(255,255,255,.78);margin-top:4px}
.aax .book .bw{padding:6px 10px 0;min-height:200px}
.aax .book .bf{padding:14px 22px 20px;display:grid;gap:10px;border-top:1px solid var(--line)}
.aax .book .bf a.wa{display:flex;align-items:center;justify-content:center;gap:8px;font-weight:800;font-size:.9rem;color:var(--f2)}
.aax .book .bf .secure{justify-content:center;margin:0;font-size:.78rem;color:var(--mut)}
.aax .book .pay{justify-content:center}
.aax .book .pay svg{height:22px}
.aax .bw [data-rezzerva]:empty{min-height:420px;border-radius:16px;margin:10px 4px;background:linear-gradient(100deg,#f1efe6 30%,#faf8f2 50%,#f1efe6 70%) 0 0/300% 100%;animation:shim 1.6s linear infinite;position:relative}
.aax .bw [data-rezzerva]:empty::after{content:"Loading live availability";position:absolute;inset:auto 0 50% 0;text-align:center;font-weight:700;font-size:.88rem;color:var(--mut)}
@keyframes shim{to{background-position:-300% 0}}
.aax .rz-fallback{padding:26px 16px;text-align:center;color:var(--mut);font-size:.9rem}
.aax .mbar{display:none}
@media(max-width:1000px){.aax .lay{grid-template-columns:1fr}.aax .book{position:static}
.aax .mbar{display:flex;position:fixed;left:12px;right:12px;bottom:12px;z-index:55;align-items:center;justify-content:space-between;gap:12px;padding:10px 10px 10px 18px;border-radius:999px;background:rgba(18,73,29,.9);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid var(--gbrd);color:#fff;box-shadow:0 20px 40px -15px rgba(0,0,0,.5)}
.aax .mbar b{font-family:var(--disp);font-size:1.4rem}.aax .mbar small{font-size:.78rem;color:rgba(255,255,255,.7)}
.aax.has-mbar .fab{bottom:86px}}
@media(max-width:640px){.aax .hl,.aax .inc{grid-template-columns:1fr}.aax .gal{height:300px}}
.aax .rel{background:var(--paper2)}
"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Mulish:wght@400;600;700;800&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">'

PAY = ('<div class="pay" aria-label="Visa, Mastercard, American Express">'
 '<svg viewBox="0 0 48 30"><rect width="48" height="30" fill="#fff"/><path fill="#1a1f71" d="M20.3 20.5h-3l1.9-11.1h3zm10.6-10.8a7.6 7.6 0 00-2.7-.5c-3 0-5.1 1.5-5.1 3.7 0 1.6 1.5 2.5 2.7 3 1.2.6 1.6.9 1.6 1.4 0 .8-.9 1.1-1.8 1.1a6 6 0 01-2.8-.6l-.4-.2-.4 2.4c.7.3 2 .6 3.3.6 3.2 0 5.2-1.5 5.3-3.8 0-1.3-.8-2.2-2.5-3-1-.5-1.7-.9-1.7-1.4s.6-1 1.7-1c.9 0 1.6.2 2.1.4l.3.1zm7.7-.3h-2.3c-.7 0-1.3.2-1.6.9L30.3 20.5h3.2l.6-1.7h3.9l.4 1.7H41zm-3.8 7.2l1.2-3.1.4-1.1.2 1 .7 3.2zm-17.4-7.2l-3 7.6-.3-1.6a9.1 9.1 0 00-4.3-4.9l2.7 9.9h3.2l4.8-11z"/><path fill="#f7a600" d="M11.7 9.4H6.8v.2c3.8 1 6.3 3.3 7.3 6.1l-1.1-5.3c-.2-.7-.7-1-1.3-1z"/></svg>'
 '<svg viewBox="0 0 48 30"><rect width="48" height="30" fill="#fff"/><circle cx="19.5" cy="15" r="8" fill="#eb001b"/><circle cx="28.5" cy="15" r="8" fill="#f79e1b"/><path fill="#ff5f00" d="M24 8.4a8 8 0 010 13.2 8 8 0 010-13.2z"/></svg>'
 '<svg viewBox="0 0 48 30"><rect width="48" height="30" fill="#1f72cd"/><text x="24" y="19" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="700" font-size="8.5" fill="#fff" letter-spacing=".4">AMEX</text></svg>'
 '</div>')

def stars(n=5): return '<span class="stars">' + ic("star") * n + '</span>'
TA_ICON_URI = "data:image/webp;base64,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"  # ícono oficial de Tripadvisor, embebido para no depender de otra CDN
BUBBLE = '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="7.2" fill="none" stroke="#34E0A1" stroke-width="1.4"/><circle cx="8" cy="8" r="4.6" fill="#34E0A1"/></svg>'
def ta_icon(cls="tai"): return f'<span class="{cls}" role="img" aria-label="Tripadvisor"></span>'
def bubbles(n=5, cls="bub"): return f'<span class="{cls}" role="img" aria-label="{n} of 5 bubbles">' + BUBBLE * n + '</span>'
def ta_badge(text):
    return f'<a class="hbadge ta" href="{e(B["tripadvisor"])}" target="_blank" rel="noopener">{ta_icon()}{bubbles()} {e(text)}</a>'

# ---------------------------------------------------------------- piezas
def header(base):
    return f'''<header class="hdr" id="hdr"><div class="w">
<a class="logo" href="{base}index.html" aria-label="{e(B['name'])}"><img src="{img(B['logo'],300)}" alt="{e(B['name'])}"></a>
<nav class="nav" id="nav"><a href="{base}index.html#tours">Tours</a><a href="{base}index.html#combos">Combos</a><a href="{base}index.html#plan">Plan my day</a><a href="{base}index.html#reviews">Reviews</a><a href="{wa('Hi! I have a question about your tours.')}" target="_blank" rel="noopener">WhatsApp</a></nav>
<a class="btn btn-gold" href="{base}index.html#tours">Book a tour {ic("arrow")}</a>
<button class="burger" aria-label="Menu" onclick="document.getElementById('nav').classList.toggle('open')">{ic("menu")}</button>
</div></header>'''

def sister_band():
    S = D.get("sister")
    if not S: return ""
    rows = "".join(f'''<a class="drow" href="{e(r['url'])}" target="_blank" rel="noopener"><span class="dft"><small>{e(r['from'])}</small><b>{e(r['to'])}</b></span><span class="dsw">{ic("arrow")}</span><span class="dpr"><small>From</small><b>US${r['price']}</b></span></a>''' for r in S["routes"])
    return f'''<section class="drv"><div class="w dgrid">
<div class="dcopy rv"><a href="{e(S['url'])}" target="_blank" rel="noopener" class="dlogo"><img src="{img(S['logo'],400)}" alt="{e(S['name'])}" loading="lazy"></a>
<div class="deyb">{e(S['eyebrow'])}</div><h2 class="dh">{e(S['h1'])}<span>{e(S['h2'])}</span></h2><p>{e(S['text'])}</p>
<a class="dbtn" href="{e(S['all'])}" target="_blank" rel="noopener">See all transfers {ic("arrow")}</a></div>
<div class="droutes rv">{rows}<div class="dnote">{ic("bus")}{e(S['note'])}</div></div>
</div></section>'''

SOC = {
 "Instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".9" fill="currentColor" stroke="none"/>',
 "Facebook": '<path d="M14 21v-7.5h2.6l.4-3H14V8.7c0-.9.3-1.5 1.6-1.5H17V4.5c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.2H8.3v3H11V21"/>',
 "TikTok": '<path d="M14 3v11.5a3.5 3.5 0 11-3.5-3.5M14 3c.4 2.6 2.1 4.2 5 4.5"/>',
 "YouTube": '<rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="M10.5 9.3v5.4l4.6-2.7z"/>',
}
def socials():
    L = B.get("social") or []
    if not L: return ""
    return '<div class="soc">' + "".join(f'<a href="{e(x["url"])}" aria-label="{e(x["name"])}"' + ('' if x["url"] == "#" else ' target="_blank" rel="noopener"') + f'><svg class="ic" viewBox="0 0 24 24" aria-hidden="true">{SOC.get(x["name"], "")}</svg></a>' for x in L) + '</div>'

def footer(base):
    tl = "".join(f'<li><a href="{base}tours/{t["slug"]}/">{e(t["short"])}</a></li>' for t in TOURS)
    return sister_band() + f'''<footer class="foot"><div class="w">
<div class="cols">
<div class="fl"><img src="{img(B['logo'],300)}" alt="{e(B['name'])}"><p>{e(B['footer_blurb'])}</p>{socials()}</div>
<div><h4>Tours</h4><ul>{tl}</ul></div>
<div><h4>Plan</h4><ul><li><a href="{base}index.html#combos">Two-in-one combos</a></li><li><a href="{base}index.html#plan">Help me choose</a></li><li><a href="{base}index.html#reviews">Reviews</a></li><li><a href="{wa('Hi! I would like a custom plan for my days in Arenal.')}" target="_blank" rel="noopener">Private or custom days</a></li></ul></div>
<div><h4>Talk to us</h4><ul>
<li>{ic("chat")}<a href="{wa()}" target="_blank" rel="noopener">WhatsApp {e(B['phone'])}</a></li>
<li>{ic("send")}<a href="mailto:{e(B['email'])}">{e(B['email'])}</a></li>
<li>{ic("pin")}{e(B['location'])}</li></ul>
<div style="margin-top:22px"><div class="secure">{ic("lock")} Secure card payment</div>{PAY}</div></div>
</div>
<div class="legal"><span>&copy; 2026 {e(B['name'])}. {e(B['legal_note'])}</span><span>Online booking by <a class="rzl" href="https://rezzerva.com/" target="_blank" rel="noopener">Rezzerva</a></span></div>
</div></footer>'''

def big_extra(t):
    hl = "".join(f'<li>{ic("check")}<span>{e(x)}</span></li>' for x in (t.get("highlights") or [])[1:5])
    chips = "".join(f'<span>{ic(i)}{e(v)}</span>' for i, v in [("cal", "Departs " + t["departs"]) if t.get("departs") else (None, None), ("pin", "Hotel pickup in La Fortuna"), ("user", t.get("child"))] if i and v)
    return f'<ul class="bhl">{hl}</ul><div class="bch">{chips}</div>'

def tour_card(t, big=False):
    cats = " ".join(t["cats"])
    tag = f'<span class="tag">{e(t["badge"])}</span>' if t.get("badge") else ""
    meta = f'<span>{ic("clock")}{e(t["duration"])}</span>' + (f'<span>{ic("flag")}{e(t["difficulty"])}</span>' if t.get("difficulty") else "")
    return f'''<a class="tc rv{' big' if big else ''}" data-cats="{cats}" href="{{base}}tours/{t['slug']}/">
<div class="ph"><img src="{img(t['card'] or t['hero'],900)}" alt="{e(t['title'])}" loading="lazy">{tag}<div class="meta">{meta}</div></div>
<div class="bd"><h3>{e(t['title'])}</h3><p>{e(t['lead'])}</p>{big_extra(t) if big else ""}
<div class="ft"><div class="pr"><small>From</small><b data-rz="{e(t['product'])}">{money(t['price'])}</b> <span>/ {t.get('unit','adult')}</span></div><span class="go">See dates {ic("arrow")}</span></div></div></a>'''

def rezzerva(t, inline_script=True):
    s = f'<div data-rezzerva data-tenant="{e(B["rezzerva_tenant"])}" data-product="{e(t["product"])}" data-title="{e(t["title"])}" data-lang="en" data-accent="{e(B["accent"])}"></div>'
    if inline_script:
        s += '\n<script src="https://app.rezzerva.com/w/assets/embed.js" async></script>'
    return s

# ---------------------------------------------------------------- HOME
def home_body(base, standalone=True):
    heroes = "".join(f'<div class="sl{" on" if i==0 else ""}" style="background-image:url(\'{img(u,2000)}\')"></div>' for i, u in enumerate(B["hero_images"]))
    dots = "".join(f'<i class="{"on" if i==0 else ""}"></i>' for i in range(len(B["hero_images"])))
    opts = "".join(f'<option value="{t["slug"]}" data-rzopt="{e(t["product"])}" data-short="{e(t["short"])}">{e(t["short"])} · from {money(t["price"])}</option>' for t in TOURS)
    copts = "".join(f'<option value="{t["slug"]}">{e(t["title"])}</option>' for t in COMBOS)
    pills = "".join(f'<button class="pill" data-go="{c["id"]}">{ic(c["icon"])}{e(c["pill"])}</button>' for c in D["categories"])
    tape = "".join(f"<span>{e(x)}</span>" for x in B["tape"]) * 2

    moods = ""
    for i, c in enumerate(D["categories"][:5]):
        n = sum(1 for t in (COMBOS if c["id"] == "combo" else TOURS) if c["id"] in t["cats"])
        moods += f'''<button class="mood m{i+1} rv" data-go="{c['id']}"><span class="bg" style="background-image:url('{img(c['image'],1200)}')"></span><span class="mi">{ic(c['icon'])}</span><span class="ct">{n} {'tour' if n==1 else 'tours'}</span><span><b>{e(c['title'])}</b><small>{e(c['blurb'])}</small></span></button>'''

    filt = '<button class="on" data-f="all">All</button>' + "".join(f'<button data-f="{c["id"]}">{e(c["pill"])}</button>' for c in D["categories"] if c["id"] != "combo")
    cards = "".join(tour_card(t, big=(i == 0)) for i, t in enumerate(TOURS)).replace("{base}", base)
    cards += f'''<a class="tc rv cta" data-cats="all" href="#plan"><div class="bd"><span class="mi2">{ic("chat")}</span><h3>Not sure which one?</h3><p>Tell us who is coming and how much energy you have. We match you with the right day, or build a private one.</p><div class="ft" style="border:0"><span class="go">Plan my day {ic("arrow")}</span></div></div></a>'''

    groups = {}
    for c in COMBOS: groups.setdefault(c["group"], []).append(c)
    acc = ""
    for gi, (g, items) in enumerate(groups.items()):
        gim = img(items[0].get("group_img") or "", 240)
        rows = "".join(f'''<a class="crow cmb" href="{base}tours/{c['slug']}/"><span class="cimgs"><img src="{gim}" alt="" loading="lazy"><img src="{img(c['card'] or c['hero'],240)}" alt="" loading="lazy"></span><span class="ct"><b class="cn">{e(c['first'])} <i>+</i> {e((c.get('pair') or c['title']).lstrip('+ ').strip())}</b><small>Full day · two tours · one hotel pickup</small></span><span class="pr2"><small class="fr">From</small><b data-rz="{e(c['product'])}" class="pv">{money(c['price']) if c.get('price') else ''}</b><small>/ {e(c.get('unit','person'))}</small></span><span class="cgo">{ic("arrow")}</span></a>''' for c in items)
        lo = min([c["price"] for c in items if c.get("price")] or [0])
        gimg = img(items[0].get("group_img") or "", 400)
        cta = f'''<a class="cask" href="{wa('Hi! I would like help choosing a combo tour.')}" target="_blank" rel="noopener"><span>{ic("chat")}</span><b>Not sure which pair?</b><small>Tell us your day and we pick the combo with you on WhatsApp.</small></a>''' if gi == 0 else ""
        acc += f'''<div class="cgrp rv"><div class="cgh"><img src="{gimg}" alt="" loading="lazy"><span><b>{e(g)}</b><small>{e(items[0].get("departs",""))} pickup · {len(items)} pairings{(' · from <span data-rzmin="' + ",".join(e(c["product"]) for c in items) + '">' + money(lo) + '</span>') if lo else ""}</small></span></div><div class="rows">{rows}</div>{cta}</div>'''

    import datetime
    def rdate(ts): return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%B %Y")
    revs = "".join(f'''<figure class="rc rv" style="margin:0"><div class="rh"><span class="av"><i>{e(r['name'][0].upper())}</i><img src="{e(r['avatar'])}" alt="" loading="lazy" width="40" height="40" onerror="this.remove()"></span><span><b>{e(r['name'])}</b><small>{rdate(r['time'])}</small></span>{ta_icon()}</div>{bubbles(5,'bub sm')}<b class="rt">{e(r['title'])}</b><p class="rx">{e(r['text'])}</p><button class="more" type="button" hidden>Read more</button><a class="vr" href="{e(B['tripadvisor'])}" target="_blank" rel="noopener">Verified on Tripadvisor</a></figure>''' for r in sorted(D["reviews"], key=lambda r: -len(r["text"]) if False else 0))
    if B.get("trustindex_id"):
        revs = f"<script defer async src='https://cdn.trustindex.io/loader.js?{e(B['trustindex_id'])}'></script>"
    hints = "".join(f'<button type="button" data-say="{e(h)}">{e(h)}</button>' for h in D["assistant"]["hints"])

    body = f'''
<section class="hero" id="top">{heroes}
<div class="w">
<div>
{ta_badge(B['ta_rating'] + ' · ' + str(B['ta_count']) + ' reviews on Tripadvisor')}
<h1>{B['h1']}</h1>
<p class="sub">{e(B['sub'])}</p>
<div class="pills">{pills}</div>
</div>
<form class="finder" id="finder" autocomplete="off">
<div class="fh"><b>Find your day</b><span class="live"><i></i>Live availability</span></div>
<p>Pick a tour, a date and your group. You will see real spots and pay by card.</p>
<div class="fld">{ic("leaf")}<div><label for="f-tour">Experience</label><select id="f-tour"><optgroup label="Tours">{opts}</optgroup><optgroup label="Two-in-one combos">{copts}</optgroup></select></div></div>
<div class="frow">
<div class="fld">{ic("cal")}<div><label for="f-date">Date</label><input id="f-date" type="date"></div></div>
<div class="fld">{ic("user")}<div><label>Travelers</label><div class="pax"><button type="button" data-p="-1" aria-label="Less"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12h12"/></svg></button><output id="f-pax">2</output><button type="button" data-p="1" aria-label="More"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 6v12M6 12h12"/></svg></button></div></div></div>
</div>
<button class="btn btn-gold" type="submit">Check availability {ic("arrow")}</button>
<div class="fnote">{ic("lock")} Free cancellation up to 24 h · Secure card payment</div>
</form>
</div>
<div class="dots">{dots}</div>
</section>

<div class="tape" aria-hidden="true"><div class="tr">{tape}</div></div>

<section class="sec" id="moods"><div class="w">
<div class="shd rv"><div><div class="eyb">Choose your kind of day</div><h2>Water, wildlife, <em>fire and forest.</em></h2></div><p class="lead">{e(B['moods_lead'])}</p></div>
<div class="moods">{moods}</div>
</div></section>

<section class="sec dk" id="plan" style="background:radial-gradient(900px 520px at 10% 10%,rgba(160,224,160,.10),transparent 60%),radial-gradient(700px 500px at 100% 100%,rgba(242,210,107,.08),transparent 60%),var(--f)"><div class="w asst">
<div class="copy rv"><div class="eyb">Plan my day</div><h2>What are you looking for? <em>Tell me and I'll plan your day.</em></h2>
<p class="lead">{e(D['assistant']['lead'])}</p>
<div class="hint">{hints}</div></div>
<div class="chat rv" id="chat">
<div class="top"><span class="av"><img src="{img(B['logo'],120)}" alt=""></span><span><b>{e(B['name'])}</b><small><i></i>Online · replies in seconds</small></span></div>
<div class="log" id="log" aria-live="polite"><div class="empty" id="empty">{ic("chat")}Write it like you would on WhatsApp. Dates, kids, energy level, anything.</div></div>
<form id="cf"><input id="ci" placeholder="Write here..." aria-label="Your message" autocomplete="off"><button aria-label="Send">{ic("send")}</button></form>
</div>
</div></section>

<section class="sec" id="tours"><div class="w">
<div class="shd rv"><div><div class="eyb">Signature tours</div><h2>Our most-booked <em>days around Arenal.</em></h2></div><div class="filt" id="filt">{filt}</div></div>
<div class="grid" id="grid">{cards}</div>

<div class="combos" id="combos">
<div class="chead rv"><div><div class="eyb">Two-in-one combos</div><h2>Two adventures, <em>one day.</em></h2></div><p class="lead">{e(B['combos_lead'])}</p></div>
<div class="cgrid">{acc}</div>
</div>
</div></section>

<section class="band"><div class="bimg" style="background-image:url('{img(B['band_image'],2000)}');background-position:{B.get('band_pos','center')}"></div><div class="w"><div class="bcard rv"><div class="eyb">From La Fortuna</div><h2>{B['band_title']}</h2><p>{e(B['band_text'])}</p></div></div></section>

<section class="sec dk" id="reviews"><div class="w revs">
<div class="score rv"><div class="talogo">{ta_icon("tai lg")}<span>Tripadvisor</span></div><div class="big">{e(B['ta_rating'])}</div>{bubbles(5,'bub lg')}<p class="cnt">Based on <b>{B['ta_count']} reviews</b></p><p>{e(B['reviews_note'])}</p><a class="btn btn-gold" href="{e(B['tripadvisor'])}" target="_blank" rel="noopener">Read all on Tripadvisor {ic("arrow")}</a></div>
<div class="rwrap"><div class="rtrack" id="rtrack">{revs}</div><div class="rnav"><button class="rbtn prev" type="button" data-d="-1" aria-label="Previous reviews" disabled>{ic("arrow")}</button><div class="rdots" id="rdots"></div><span class="rcount" id="rcount"></span><button class="rbtn" type="button" data-d="1" aria-label="More reviews">{ic("arrow")}</button></div></div>
</div></section>
'''
    return body

# ---------------------------------------------------------------- JS
def js_prices(api):
    """Precios en vivo desde Rezzerva. Lo generado queda de respaldo si Rezzerva no responde."""
    return "var RZ_API=" + json.dumps(api) + ",RZ_TEN=" + json.dumps(B["rezzerva_tenant"]) + ";" + r"""
(function(){
var sel='[data-rz],[data-rzchild],[data-rztiers],[data-rzmin],[data-rzopt]',els=document.querySelectorAll(sel);if(!els.length)return;
var slugs={};els.forEach(function(el){['rz','rzchild','rztiers','rzopt'].forEach(function(k){if(el.dataset[k])slugs[el.dataset[k]]=1});if(el.dataset.rzmin)el.dataset.rzmin.split(',').forEach(function(s){slugs[s]=1})});
function $m(n){var v=n/100;return '$'+(v%1?v.toFixed(2):v.toLocaleString('en-US'))}
function calc(j){var o={};if(j.passenger_types&&j.passenger_types.length){var a=j.passenger_types.filter(function(p){return p.code==='adult'})[0]||j.passenger_types[0],c=j.passenger_types.filter(function(p){return p.code==='child'})[0];o.from=a.price_minor;if(c)o.child=$m(c.price_minor)+' per child, ages '+c.min_age+' to '+c.max_age}
 else if(j.tiers&&j.tiers.length){o.from=Math.min.apply(null,j.tiers.map(function(t){return t.amount_minor}));o.tiers=j.tiers.map(function(t){var n=t.min===t.max?t.min:t.min+'-'+t.max;return n+(n===1?' person ':' people ')+$m(t.amount_minor)}).join(' · ')}
 return o}
function get(s){var k='rz:'+RZ_TEN+':'+s;try{var c=JSON.parse(sessionStorage.getItem(k)||'null');if(c&&Date.now()-c.t<6e5)return Promise.resolve(c.v)}catch(_){}
 return fetch(RZ_API+encodeURIComponent(RZ_TEN)+'/products/'+encodeURIComponent(s)).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(j){var v=calc(j);try{sessionStorage.setItem(k,JSON.stringify({t:Date.now(),v:v}))}catch(_){}return v})}
var P={};Promise.all(Object.keys(slugs).map(function(s){return get(s).then(function(v){P[s]=v},function(){})})).then(function(){
 document.querySelectorAll('[data-rz]').forEach(function(el){var v=P[el.dataset.rz];if(v&&v.from)el.textContent=$m(v.from)});
 document.querySelectorAll('[data-rzchild]').forEach(function(el){var v=P[el.dataset.rzchild];if(v&&v.child)el.textContent=v.child});
 document.querySelectorAll('[data-rztiers]').forEach(function(el){var v=P[el.dataset.rztiers];if(v&&v.tiers)el.textContent=v.tiers});
 document.querySelectorAll('[data-rzmin]').forEach(function(el){var m=el.dataset.rzmin.split(',').map(function(s){return P[s]&&P[s].from}).filter(Boolean);if(m.length)el.textContent=$m(Math.min.apply(null,m))});
 document.querySelectorAll('[data-rzopt]').forEach(function(el){var v=P[el.dataset.rzopt];if(v&&v.from)el.textContent=el.dataset.short+' · from '+$m(v.from)});
 if(window.T)T.forEach(function(t){var v=P[t.s];if(v&&v.from)t.p=v.from/100});
});
})();
"""

def js_common():
    return r"""
(function(){
var root=document.querySelector('.aax');
document.querySelectorAll('.aax .legal span').forEach(function(sp){if(!sp.querySelector('a')&&/Rezzerva/.test(sp.textContent)){sp.innerHTML=sp.innerHTML.replace('Rezzerva','<a class="rzl" href="https://rezzerva.com/" target="_blank" rel="noopener">Rezzerva</a>')}});
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
document.querySelectorAll('.aax .rv').forEach(function(el){io.observe(el)});
var bi=document.querySelector('.aax .band .bimg');if(bi&&!matchMedia('(prefers-reduced-motion:reduce)').matches){var pf=function(){var r=bi.parentNode.getBoundingClientRect();if(r.bottom>0&&r.top<innerHeight)bi.style.transform='translateY('+((r.top+r.height/2-innerHeight/2)*-.08)+'px)'};addEventListener('scroll',pf,{passive:true});pf()}
document.querySelectorAll('.aax .rc').forEach(function(c){var x=c.querySelector('.rx'),m=c.querySelector('.more');if(x&&m&&x.scrollHeight>x.clientHeight+4){m.hidden=false;m.onclick=function(){c.classList.toggle('open');m.textContent=c.classList.contains('open')?'Show less':'Read more'}}});
(function(){var t=document.getElementById('rtrack');if(!t)return;var cards=t.querySelectorAll('.rc'),dots=document.getElementById('rdots'),cnt=document.getElementById('rcount'),bs=document.querySelectorAll('.aax .rbtn');if(!cards.length){document.querySelector('.aax .rnav').hidden=true;return}
cards.forEach(function(){dots.appendChild(document.createElement('i'))});
function step(){var c=cards[0];return c.getBoundingClientRect().width+parseFloat(getComputedStyle(t).columnGap||16)}
function upd(){var max=t.scrollWidth-t.clientWidth-4,vis=Math.max(1,Math.round(t.clientWidth/step())),first=Math.round(t.scrollLeft/step());
 dots.querySelectorAll('i').forEach(function(d,i){d.classList.toggle('on',i>=first&&i<first+vis)});
 cnt.textContent=Math.min(cards.length,first+vis)+' of '+cards.length;
 bs[0].disabled=t.scrollLeft<4;bs[1].disabled=t.scrollLeft>=max;t.classList.toggle('end',t.scrollLeft>=max);
 if(max<=0)document.querySelector('.aax .rnav').hidden=true}
bs.forEach(function(b){b.onclick=function(){b.classList.remove('nudge');t.scrollBy({left:(+b.dataset.d)*step(),behavior:'smooth'})}});
t.addEventListener('scroll',function(){requestAnimationFrame(upd)},{passive:true});addEventListener('resize',upd);upd();
var ob=new IntersectionObserver(function(es){if(es[0].isIntersecting){bs[1].classList.add('nudge');ob.disconnect()}},{threshold:.5});ob.observe(t)})();
var h=document.getElementById('hdr');if(h){var f=function(){h.classList.toggle('sc',scrollY>40)};f();addEventListener('scroll',f,{passive:true})}
})();
"""

def js_home(base):
    tours = [{"s": t["slug"], "t": t["title"], "p": t.get("price"), "u": t.get("unit", "adult"), "d": t["duration"], "img": img(t["card"] or t["hero"], 240), "c": t["cats"], "k": t.get("keywords", [])} for t in ALL]
    A = D["assistant"]
    return "var BASE=" + json.dumps(base) + ";var T=window.T=" + json.dumps(tours, ensure_ascii=False) + ";var WA=" + json.dumps(wa()) + ";var CAT=" + json.dumps({c["id"]: c["keywords"] for c in D["categories"]}, ensure_ascii=False) + ";" + r"""
(function(){
/* hero carrusel */
var sl=document.querySelectorAll('.hero .sl'),dt=document.querySelectorAll('.dots i'),k=0;
if(sl.length>1)setInterval(function(){sl[k].classList.remove('on');dt[k].classList.remove('on');k=(k+1)%sl.length;sl[k].classList.add('on');void dt[k].offsetWidth;dt[k].classList.add('on')},7000);
/* buscador -> pagina del tour con ?date&pax (embed.js de Rezzerva los lee solo) */
var fd=document.getElementById('f-date'),fp=document.getElementById('f-pax'),pax=2;
var d=new Date();d.setDate(d.getDate()+1);fd.min=new Date().toISOString().slice(0,10);fd.value=d.toISOString().slice(0,10);
document.querySelectorAll('.pax button').forEach(function(b){b.onclick=function(){pax=Math.max(1,Math.min(20,pax+(+b.dataset.p)));fp.textContent=pax}});
document.getElementById('finder').onsubmit=function(ev){ev.preventDefault();var s=document.getElementById('f-tour').value;location.href=BASE+'tours/'+s+'/?date='+fd.value+'&pax='+pax+'#book'};
/* filtros */
var fb=document.querySelectorAll('#filt button'),cards=document.querySelectorAll('#grid .tc');
function filt(c){fb.forEach(function(b){b.classList.toggle('on',b.dataset.f===c)});cards.forEach(function(x){var ok=c==='all'||x.dataset.cats==='all'||x.dataset.cats.split(' ').indexOf(c)>-1;x.classList.toggle('hide',!ok);x.classList.toggle('big',ok&&c==='all'&&x===cards[0]);if(ok)x.classList.add('in')})}
fb.forEach(function(b){b.onclick=function(){filt(b.dataset.f)}});
document.querySelectorAll('[data-go]').forEach(function(b){b.onclick=function(){var c=b.dataset.go;if(c==='combo'){document.getElementById('combos').scrollIntoView({behavior:'smooth'});return}filt(c);document.getElementById('tours').scrollIntoView({behavior:'smooth'})}});
/* asistente */
var log=document.getElementById('log'),ci=document.getElementById('ci'),hist=[];
function tm(){var n=new Date();return n.getHours()+':'+('0'+n.getMinutes()).slice(-2)}
function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function add(cls,html){var e=document.getElementById('empty');if(e)e.remove();var m=document.createElement('div');m.className='msg '+cls;m.innerHTML=html+'<span class="tm">'+tm()+'</span>';log.appendChild(m);log.scrollTop=log.scrollHeight;return m}
function norm(s){return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
function sug(t){return '<div class="sug"><img src="'+t.img+'" alt=""><span><b>'+esc(t.t)+'</b><small>'+esc(t.d)+(t.p?' · from $'+t.p+(t.u==='group'?' / group':''):'')+'</small></span><a href="'+BASE+'tours/'+t.s+'/#book">See dates</a></div>'}
function think(q){
 var n=norm(q),score={};
 T.forEach(function(t){var s=0;t.k.forEach(function(w){if(n.indexOf(norm(w))>-1)s+=3});t.c.forEach(function(c){(CAT[c]||[]).forEach(function(w){if(n.indexOf(norm(w))>-1)s+=1})});if(s)score[t.s]=s});
 var kids=/(kid|child|nin|famil|hij|baby|bebe)/.test(n),easy=/(easy|calm|relax|tranq|suave|abuel|grandm|older|slow)/.test(n),adr=/(adrenal|extreme|wild ride|intens|aventur|rapids|thrill)/.test(n);
 var combo=/(combo|two|both|full day|dia completo|dos|2 tours|all day)/.test(n);
 T.forEach(function(t){if(kids&&(t.c.indexOf('wildlife')>-1))score[t.s]=(score[t.s]||0)+2;if(easy&&t.c.indexOf('wildlife')>-1)score[t.s]=(score[t.s]||0)+2;if(adr&&/raft/.test(t.s))score[t.s]=(score[t.s]||0)+3;if(combo&&t.c.indexOf('combo')>-1)score[t.s]=(score[t.s]||0)+2;if(!combo&&t.c.indexOf('combo')>-1&&score[t.s])score[t.s]-=1});
 var top=Object.keys(score).sort(function(a,b){return score[b]-score[a]}).slice(0,3).map(function(s){return T.filter(function(t){return t.s===s})[0]});
 var es=/[áéíóúñ¿¡]|\b(quiero|para|con|ninos|familia|cascada|perezoso|volcan|noche|hola|gracias)\b/.test(q.toLowerCase());
 if(!top.length){return es?'Contame un poco más: ¿agua, animales, volcán o algo de noche? ¿Van con niños? Si preferís, seguimos por <a href="'+WA+'?text='+encodeURIComponent(q)+'" target="_blank" rel="noopener"><b>WhatsApp</b></a>.':'Tell me a little more. Water, wildlife, volcano or something after dark? Traveling with kids? You can also <a href="'+WA+'?text='+encodeURIComponent(q)+'" target="_blank" rel="noopener"><b>continue on WhatsApp</b></a> with our team.'}
 var intro=es?(kids?'Con niños, estas son las que más disfrutan:':'Para lo que me contás, yo iría con esto:'):(kids?'With kids along, these are the ones families love most:':(easy?'For an easy, unhurried day, I would go with:':(adr?'If you want your heart racing, start here:':'Here is what I would book for you:')));
 var tail=es?'<br><small>Tocá "See dates" para ver espacios reales y reservar.</small>':'<br><small>Tap "See dates" to check real availability and book in a minute.</small>';
 return intro+top.map(sug).join('')+tail}
function send(q){q=q.trim();if(!q)return;add('me',esc(q));hist.push(q);ci.value='';var ty=document.createElement('div');ty.className='typing';ty.innerHTML='<i></i><i></i><i></i>';log.appendChild(ty);log.scrollTop=log.scrollHeight;setTimeout(function(){ty.remove();add('bot',think(q))},650+Math.random()*500)}
document.getElementById('cf').onsubmit=function(e){e.preventDefault();send(ci.value)};
document.querySelectorAll('[data-say]').forEach(function(b){b.onclick=function(){send(b.dataset.say)}});
var fab=document.getElementById('fab');if(fab)fab.onclick=function(){document.getElementById('plan').scrollIntoView({behavior:'smooth'});setTimeout(function(){ci.focus({preventScroll:true})},700)};
})();
"""

# ---------------------------------------------------------------- TOUR
FAQ_BASE = [
 ("Can I cancel?", "Yes. Cancel up to 24 hours before the tour and you get your money back. Plans change, we get it."),
 ("Where do you pick us up?", "At your hotel or rental in La Fortuna and the Arenal area. After booking we confirm the exact time by WhatsApp."),
 ("How do I pay?", "By card, right here, through a secure checkout. Your spot is confirmed instantly and the receipt arrives by email."),
]

def tour_body(t, base):
    hero = img(t["hero"], 2000)
    facts = [("clock", "Duration", t["duration"]), ("flag", "Difficulty", t.get("difficulty") or "Easy"), (("cal", "Departs", t["departs"]) if t.get("departs") else ("globe", "Guide", t.get("guide") or "English / Spanish")), ("pin", "Pickup", t.get("pickup") or "La Fortuna / Arenal")]
    fx = "".join(f'<div class="fact">{ic(a)}<span><small>{b}</small><b>{e(c)}</b></span></div>' for a, b, c in facts)
    ov = "".join(f"<p>{e(p)}</p>" for p in (t.get("overview") or [t["lead"]]))
    hl = "".join(f'<li>{ic("check")}<span>{e(x)}</span></li>' for x in (t.get("highlights") or []))
    gal = (t.get("gallery") or [])[:3]
    while len(gal) < 3 and gal: gal.append(gal[-1])
    galh = "".join(f'<div style="background-image:url(\'{img(u,1200)}\')"></div>' for u in gal)
    steps = "".join(f"<li>{e(s)}</li>" for s in (t.get("steps") or []))
    inc = "".join(f'<li>{ic("check")}{e(x)}</li>' for x in (t.get("included") or []))
    noi = "".join(f'<li>{ic("x")}{e(x)}</li>' for x in (t.get("not_included") or []))
    faq = list(FAQ_BASE)
    if t.get("child"): faq.insert(2, ("Do kids pay less?", f"Yes. {t['child']}."))
    faqh = "".join(f'<details><summary>{e(q)}{ic("plus")}</summary><p>{e(a)}</p></details>' for q, a in faq)
    rel = [x for x in TOURS if x["slug"] != t["slug"] and set(x["cats"]) & set(t["cats"])] or [x for x in TOURS if x["slug"] != t["slug"]]
    rel = (rel + [x for x in TOURS if x not in rel and x["slug"] != t["slug"]])[:3]
    relh = "".join(tour_card(x) for x in rel).replace("{base}", base)
    crumb_cat = "Combos" if "combo" in t["cats"] else "Tours"
    price = f'<small>From</small><div class="amt"><span data-rz="{e(t["product"])}" style="font:inherit;color:inherit">{money(t["price"])}</span> <span>/ {t.get("unit","adult")}</span></div>' if t.get("price") else '<small>Book online</small><div class="amt" style="font-size:2rem">Live prices</div>'
    child = f'<div class="ch" data-rzchild="{e(t["product"])}">{e(t["child"])}</div>' if t.get("child") else ""
    if t.get("price_note"): child += f'<div class="ch" data-rztiers="{e(t["product"])}">{e(t["price_note"])}</div>'
    sec = lambda title, inner: f'<div class="blk rv"><h2>{title}</h2>{inner}</div>' if inner else ""

    return f'''
<section class="thero" style="background-image:url('{hero}');background-position:{t.get('hero_pos','center')}"><div class="w">
<div class="crumb"><a href="{base}index.html">Home</a> &nbsp;/&nbsp; <a href="{base}index.html#{'combos' if crumb_cat=='Combos' else 'tours'}">{crumb_cat}</a></div>
{ta_badge(B['ta_rating'] + ' · ' + str(B['ta_count']) + ' Tripadvisor reviews')}
<h1>{e(t['title'])}</h1>
<p class="sub">{e(t['lead'])}</p>
</div></section>
<section class="facts"><div class="w"><div class="row">{fx}</div></div></section>
<div class="w lay">
<div>
{sec("The day, <em>in short</em>", ov)}
{sec("Highlights", f'<ul class="hl">{hl}</ul>' if hl else "")}
{sec("Gallery", f'<div class="gal">{galh}</div>' if galh else "")}
{sec("Your day, <em>step by step</em>", f'<ol class="tl">{steps}</ol>' if steps else "")}
{sec("What's included", f'<div class="inc"><div class="yes"><h3>Included</h3><ul>{inc}</ul></div><div class="no"><h3>Not included</h3><ul>{noi}</ul></div></div>' if inc else "")}
{sec("What to bring", f'<div class="bring">{e(t["bring"])}</div>' if t.get("bring") else "")}
{sec("Good to know", f'<div class="faq">{faqh}</div>')}
</div>
<aside class="book" id="book">
<div class="bh">{price}{child}</div>
<div class="bw">{rezzerva(t, inline_script=False)}<noscript><div class="rz-fallback">Enable JavaScript to see live availability, or book by WhatsApp.</div></noscript></div>
<div class="bf"><a class="wa" href="{wa('Hi! I have a question about ' + t['title'] + '.')}" target="_blank" rel="noopener">{ic("chat")} Prefer to ask first? WhatsApp us</a><div class="secure">{ic("lock")} Secure card payment · instant confirmation</div>{PAY}</div>
</aside>
</div>
<section class="sec rel"><div class="w"><div class="shd rv"><div><div class="eyb">Keep exploring</div><h2>Pairs well <em>with this.</em></h2></div></div><div class="grid">{relh}</div></div></section>
<div class="mbar"><span><small>From</small> <b data-rz="{e(t["product"])}">{money(t.get("price")) or ""}</b> <small>/ {t.get("unit","adult")}</small></span><a class="btn btn-gold" href="#book">Check dates {ic("arrow")}</a></div>
'''

def schema_tour(t):
    o = {"@context": "https://schema.org", "@type": "TouristTrip", "name": t["title"], "description": t["lead"], "image": absimg(t["hero"]),
         "touristType": "Adventure", "provider": {"@type": "TravelAgency", "name": B["name"], "telephone": B["phone"], "url": B["url"]}}
    if t.get("price"): o["offers"] = {"@type": "Offer", "price": t["price"], "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": f'{B["url"]}/tours/{t["slug"]}/'}
    return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + "</script>"

# ---------------------------------------------------------------- ensamblado
def page(title, desc, body, base, js, cls="", og=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#12491d">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{og}">
<link rel="icon" href="{img(B['logo'],64)}">{FONTS}<style>html,body{{margin:0;background:#f4f1e8}}{CSS}</style></head>
<body><div class="aax{cls}">{header(base)}{body}{footer(base)}</div>
<script>{js_common()}{js}{js_prices("/rz/")}</script></body></html>'''

def wp_block(body, js, extra_head="", cls=""):
    # Para el widget HTML de Elementor: sin header/footer (los pone el tema), mismo CSS con alcance .aax
    return f'''<!-- Active Arenal · bloque KommPro/Rezzerva · pegar en un widget HTML de Elementor (ancho completo, sin padding) -->
{FONTS}<style>{CSS}
.aax .hero .w,.aax .thero .w{{padding-top:110px}}</style>
{extra_head}<div class="aax{cls}">{body}</div>
<script>{js_common()}{js}{js_prices("https://app.rezzerva.com/v1/widget/")}</script>'''

import hashlib
def _ver():
    # cambia solo cuando cambian el CSS o el JS comun: los navegadores bajan la version nueva
    return hashlib.sha1((CSS + js_common() + js_prices("x")).encode()).hexdigest()[:8]

def wpfix(h):
    # rutas del sitio estatico -> paginas reales de WordPress (/tour-xxx/, /#combos)
    return (h.replace('href="/index.html#', 'href="/#').replace('href="/index.html"', 'href="/"')
             .replace('href="/tours/', 'href="/').replace('activearenal.com/tours/', 'activearenal.com/'))

def wp_full(body, home=False, cls=""):
    # Pagina completa para WordPress (plantilla Elementor Canvas): header, cuerpo, franja de Driver y footer propios.
    # CSS y JS comunes viven en /assets/ del proyecto de Pages (un solo lugar, cache del navegador).
    a = DEMO_URL + "assets/"
    js = f'<script src="{a}aa.js?v={_ver()}" defer></script>' + (f'<script src="{a}aa-home.js?v={_ver()}" defer></script>' if home else "")
    return wpfix(f'''<!-- Active Arenal · pagina completa · bloque HTML con plantilla Elementor Canvas · generado por plantilla/build.py -->
{FONTS}<link rel="stylesheet" href="{a}aa.css?v={_ver()}">
<div class="aax{cls}">{header("/")}{body}{footer("/")}</div>
{js}''')

RZ_FUNCTION = """// Cloudflare Pages Function: proxy de solo lectura a la API publica del widget de Rezzerva.
// Sirve /rz/<tenant>/products/<slug> para que el sitio muestre los precios del panel.
export async function onRequestGet({ params }) {
  const path = [].concat(params.path || []).join("/");
  if (!/^[a-z0-9-]+\\/products\\/[a-z0-9-]+$/.test(path)) {
    return new Response("Not found", { status: 404 });
  }
  const r = await fetch("https://app.rezzerva.com/v1/widget/" + path, {
    cf: { cacheTtl: 300, cacheEverything: true },
  });
  return new Response(r.body, {
    status: r.status,
    headers: {
      "content-type": r.headers.get("content-type") || "application/json",
      "cache-control": "public, max-age=300",
      "access-control-allow-origin": "*",
    },
  });
}
"""

def build():
    # solo borra lo que genera (index.html, tours/, wp/); nunca la plantilla ni otros archivos
    for x in ("tours", "wp"):
        if os.path.isdir(os.path.join(OUT, x)): shutil.rmtree(os.path.join(OUT, x))
    os.makedirs(os.path.join(OUT, "wp"), exist_ok=True)
    fab = f'<button class="fab" id="fab">{ic("chat")} Plan my day</button>'
    # home
    hb = home_body("", True) + fab
    open(os.path.join(OUT, "index.html"), "w").write(page(B["seo_title"], B["seo_desc"], hb, "", js_home(""), og=absimg(B["hero_images"][0])))
    # wp home: las rutas apuntan a las paginas reales de WordPress (/tour-xxx/)
    global ASSET
    ASSET = DEMO_URL
    wb = home_body("/", False).replace('href="/tours/', 'href="/').replace(fab, "") + sister_band() + fab
    wjs = js_home("/").replace("BASE+'tours/'+s+'/", "BASE+s+'/").replace("BASE+'tours/'+t.s+'/", "BASE+t.s+'/")
    open(os.path.join(OUT, "wp", "home.html"), "w").write(wp_block(wb, wjs))
    os.makedirs(os.path.join(OUT, "wp", "full"), exist_ok=True)
    ad = os.path.join(OUT, "assets"); os.makedirs(ad, exist_ok=True)
    open(os.path.join(ad, "aa.css"), "w").write("html,body{margin:0;background:#f4f1e8}" + CSS)
    open(os.path.join(ad, "aa.js"), "w").write(js_common() + js_prices(DEMO_URL + "rz/"))
    open(os.path.join(ad, "aa-home.js"), "w").write(wjs)
    open(os.path.join(OUT, "wp", "full", "home.html"), "w").write(wp_full(home_body("/", False).replace(fab, "") + fab, home=True))
    ASSET = "/"
    # tours
    for t in ALL:
        d = os.path.join(OUT, "tours", t["slug"]); os.makedirs(d)
        tb = tour_body(t, "../../")
        tb += f'<a class="fab" href="{wa("Hi! I have a question about " + t["title"] + ".")}" target="_blank" rel="noopener">{ic("chat")} WhatsApp</a>'
        rz = '<script src="https://app.rezzerva.com/w/assets/embed.js" async></script>'
        open(os.path.join(d, "index.html"), "w").write(
            page(f'{t["title"]} · {B["name"]}', t["lead"], tb + schema_tour(t) + rz, "../../", "", cls=" has-mbar", og=absimg(t["hero"])))
        ASSET = DEMO_URL
        wtb = tour_body(t, "/").replace('href="/tours/', 'href="/')
        open(os.path.join(OUT, "wp", f"{t['slug']}.html"), "w").write(wp_block(wtb + schema_tour(t) + rz, "", cls=" has-mbar"))
        wfab = f'<a class="fab" href="{wa("Hi! I have a question about " + t["title"] + ".")}" target="_blank" rel="noopener">{ic("chat")} WhatsApp</a>'
        open(os.path.join(OUT, "wp", "full", f"{t['slug']}.html"), "w").write(wp_full(wtb + wfab + schema_tour(t) + rz, cls=" has-mbar"))
        ASSET = "/"
    # Precios en vivo: /rz/<tenant>/products/<slug> lo atiende una Pages Function de Cloudflare
    # que consulta la API publica del widget de Rezzerva (solo esa ruta, con cache de 5 min).
    fdir = os.path.join(OUT, "functions", "rz"); os.makedirs(fdir, exist_ok=True)
    with open(os.path.join(fdir, "[[path]].js"), "w") as f:
        f.write(RZ_FUNCTION)
    # CORS solo para los bloques de WordPress y los assets (los lee el admin de activearenal.com al publicar)
    open(os.path.join(OUT, "_headers"), "w").write("/wp/*\n  Access-Control-Allow-Origin: *\n/assets/*\n  Access-Control-Allow-Origin: *\n")
    rd = os.path.join(OUT, "_redirects")
    if os.path.exists(rd): os.remove(rd)
    print("ok:", len(ALL), "tours ->", OUT)

if __name__ == "__main__":
    build()
