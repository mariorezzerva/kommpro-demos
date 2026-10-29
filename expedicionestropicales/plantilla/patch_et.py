#!/usr/bin/env python3
"""Convierte el build.py de Active Arenal (copiado aqui) en la demo de Expediciones Tropicales.
Se corre una sola vez sobre la copia: python3 patch_et.py"""
import re, sys
p = "build.py"
s = open(p, encoding="utf-8").read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n < 1:
        sys.exit("NO ENCONTRADO: " + old[:90])
    if count == 1 and n > 1:
        s = s.replace(old, new, 1)
    else:
        s = s.replace(old, new)

# ---------- paleta y tipografia (amarillo palmera, negro selva, verde de las olas)
rep("--f:#12491d;--f2:#0e3b17;--leaf:#2a7a3a;--mint:#a0e0a0;--gold:#f2d26b;--onGold:#3a2a06;--paper:#f4f1e8;--paper2:#ebe6d8;--ink:#14241a;--mut:#5a6b5d;--line:rgba(20,36,26,.12);--glass:rgba(255,255,255,.08);--gbrd:rgba(160,224,160,.28);\n--disp:'Fraunces',Georgia,serif;",
    "--f:#16261d;--f2:#0f1a14;--leaf:#00944b;--mint:#f6cf3f;--gold:#f6cf3f;--onGold:#17150a;--paper:#fbf9f2;--paper2:#f2eedf;--ink:#151a16;--mut:#5b645d;--line:rgba(21,26,22,.12);--glass:rgba(255,255,255,.08);--gbrd:rgba(246,207,63,.30);\n--disp:'Montserrat',system-ui,sans-serif;--script:'Sacramento','Brush Script MT',cursive;")
for a, b in [("rgba(160,224,160", "rgba(246,207,63"), ("rgba(9,38,15", "rgba(8,14,10"), ("rgba(18,73,29", "rgba(22,38,29"),
             ("rgba(11,48,19", "rgba(14,24,18"), ("rgba(14,59,23", "rgba(16,28,21"), ("rgba(238,245,238", "rgba(247,245,236"),
             ("rgba(242,210,107", "rgba(246,207,63")]:
    rep(a, b, count=0)
rep("#14241a", "#151a16", 0); rep("#2c3b30", "#2d332e", 0); rep("#7a8a7d", "#7b827c", 0)
rep('content="#12491d"', 'content="#16261d"', 0)
rep("html,body{{margin:0;background:#f4f1e8}}", "html,body{{margin:0;background:#fbf9f2}}")
rep('"html,body{margin:0;background:#f4f1e8}"', '"html,body{margin:0;background:#fbf9f2}"')
rep("family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Mulish:wght@400;600;700;800&family=Poppins:wght@500;600;700",
    "family=Montserrat:wght@600;700;800&family=Sacramento&family=Mulish:wght@400;600;700;800")

EXTRA_CSS = r"""
/* ===== Expediciones Tropicales ===== */
.aax h1,.aax h2,.aax h3{font-weight:800;letter-spacing:-.025em;line-height:1.02}
.aax h2 em,.aax h1 em{font-family:var(--script);font-style:normal;font-weight:400;letter-spacing:0;font-size:1.32em;line-height:.8;color:var(--leaf);display:inline-block;padding:0 .04em}
.aax .dk h2 em,.aax .dk h1 em,.aax .hero h1 em,.aax .bcard h2 em{color:var(--gold)}
.aax .hero h1{max-width:13ch;font-weight:800}
.aax .finder b,.aax .score .big,.aax .book .bh .amt{font-weight:800}
.aax .wav{display:block;width:120px;height:44px;color:var(--gold)}
.aax .wav path{fill:none;stroke:currentColor;stroke-width:5;stroke-linecap:round}
.aax .hero .wav{position:absolute;right:clamp(16px,4vw,48px);top:120px;z-index:2;opacity:.95}
@media(max-width:860px){.aax .hero .wav{display:none}}
.aax .hbadge.ets{gap:12px}
.aax .hbadge.ets b{color:var(--gold);font-weight:800}
.aax .logo img{height:62px;filter:drop-shadow(0 4px 14px rgba(0,0,0,.25))}
.aax .hdr .nav a.ag{color:var(--gold)}
/* footer claro: el logo es negro sobre amarillo */
.aax .foot{background:var(--paper2);color:var(--ink)}
.aax .foot h4,.aax .foot li .ic,.aax .foot .secure .ic{color:var(--leaf)}
.aax .foot .fl p,.aax .foot .legal{color:var(--mut)}
.aax .foot .secure{color:var(--ink)}
.aax .foot .legal{border-top-color:var(--line)}
.aax .foot .soc a{border-color:var(--line);background:#fff;color:var(--ink)}
.aax .foot .soc a:hover{background:var(--ink);color:var(--gold)}
.aax .foot .fl img{height:78px}
.aax .tax{font-size:.78rem;color:var(--mut);margin-top:4px}
/* agencias */
.aax .agency{position:relative;overflow:hidden}
.aax .agency .wav.a1{position:absolute;left:-14px;bottom:40px;width:160px;height:60px;opacity:.9}
.aax .agency .wav.a2{position:absolute;right:-20px;top:46px;width:180px;height:64px;color:var(--leaf);opacity:.8}
.aax .ag{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:clamp(28px,5vw,72px);align-items:center;position:relative;z-index:1}
.aax .ag ul.feat{list-style:none;padding:0;margin:26px 0 30px;display:grid;gap:16px}
.aax .ag ul.feat li{display:grid;grid-template-columns:38px minmax(0,1fr);gap:14px;align-items:start}
.aax .ag ul.feat .fi{width:38px;height:38px;border-radius:12px;display:grid;place-items:center;border:1px solid var(--gbrd);color:var(--gold);background:rgba(246,207,63,.07)}
.aax .ag ul.feat b{display:block;font-size:1rem;color:#fff}
.aax .ag ul.feat small{display:block;color:rgba(247,245,236,.7);font-size:.92rem;line-height:1.45}
.aax .ag .cta{display:flex;flex-wrap:wrap;gap:12px}
.aax .portal{border-radius:24px;background:rgba(255,255,255,.06);border:1px solid var(--gbrd);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);box-shadow:0 40px 90px -40px rgba(0,0,0,.7);overflow:hidden;min-width:0}
.aax .portal .ph1{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px 20px;border-bottom:1px solid rgba(246,207,63,.18)}
.aax .portal .ph1 b{font-size:.98rem}.aax .portal .ph1 small{display:block;color:rgba(247,245,236,.6);font-size:.78rem}
.aax .ex{font-size:.66rem;font-weight:800;letter-spacing:.12em;text-transform:uppercase;padding:5px 9px;border-radius:999px;border:1px dashed rgba(246,207,63,.55);color:var(--gold);white-space:nowrap}
.aax .portal .kp{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:rgba(246,207,63,.14)}
.aax .portal .kp div{background:rgba(16,28,21,.6);padding:14px 18px}
.aax .portal .kp small{display:block;font-size:.68rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:rgba(247,245,236,.55)}
.aax .portal .kp b{font-family:var(--disp);font-size:1.35rem;font-variant-numeric:tabular-nums}
.aax .portal .bar{height:6px;border-radius:9px;background:rgba(255,255,255,.12);margin-top:8px;overflow:hidden}.aax .portal .bar i{display:block;height:100%;width:35%;background:var(--gold);border-radius:9px}
.aax .portal .tw{overflow-x:auto}
.aax .portal table{width:100%;border-collapse:collapse;font-size:.86rem;min-width:520px}
.aax .portal th{text-align:left;font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:rgba(247,245,236,.5);font-weight:800;padding:12px 18px 8px}
.aax .portal td{padding:11px 18px;border-top:1px solid rgba(255,255,255,.07);font-variant-numeric:tabular-nums;vertical-align:middle}
.aax .portal td small{display:block;color:rgba(247,245,236,.55);font-size:.76rem}
.aax .st{display:inline-flex;align-items:center;gap:6px;font-size:.74rem;font-weight:800;padding:4px 10px;border-radius:999px;white-space:nowrap}
.aax .st::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}
.aax .st.ok{color:#8fe3a2;background:rgba(143,227,162,.12)}.aax .st.vo{color:var(--gold);background:rgba(246,207,63,.12)}.aax .st.pe{color:#b8c7ff;background:rgba(184,199,255,.12)}
.aax .portal .pf{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;padding:14px 20px;border-top:1px solid rgba(246,207,63,.18);font-size:.86rem;color:rgba(247,245,236,.75)}
.aax .portal .pf b{color:#fff}
@media(max-width:960px){.aax .ag{grid-template-columns:1fr}}
/* confianza */
.aax .trust{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.3fr);gap:clamp(28px,5vw,70px);align-items:center}
.aax .yrs{font-family:var(--disp);font-weight:800;font-size:clamp(4.5rem,11vw,8.5rem);line-height:.85;letter-spacing:-.05em;color:var(--ink)}
.aax .yrs span{font-family:var(--script);font-weight:400;font-size:.42em;letter-spacing:0;color:var(--leaf);margin-left:.1em}
.aax .facts2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0;border-top:1px solid var(--line)}
.aax .facts2 div{padding:20px 18px 20px 0;border-bottom:1px solid var(--line)}
.aax .facts2 div:nth-child(odd){padding-right:22px;border-right:1px solid var(--line)}
.aax .facts2 div:nth-child(even){padding-left:22px}
.aax .facts2 b{display:block;font-family:var(--disp);font-weight:800;font-size:1.1rem}
.aax .facts2 small{color:var(--mut);font-size:.92rem}
@media(max-width:860px){.aax .trust{grid-template-columns:1fr}}
@media(max-width:480px){.aax .facts2{grid-template-columns:1fr}.aax .facts2 div:nth-child(n){padding:16px 0;border-right:0}}
/* reserva demo (en la pagina de cada tour) */
.aax .bk{padding:16px 18px 6px}
.aax .bk .tabs{display:grid;grid-template-columns:1fr 1fr;padding:4px;border-radius:999px;background:var(--paper2);margin-bottom:14px}
.aax .bk .tabs button{border:0;background:none;padding:9px 10px;border-radius:999px;font-weight:800;font-size:.86rem;cursor:pointer;color:var(--mut)}
.aax .bk .tabs button.on{background:var(--ink);color:var(--gold)}
.aax .bk label{display:block;font-size:.68rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);margin:0 0 6px}
.aax .bk .in2{width:100%;border:1px solid var(--line);border-radius:12px;padding:11px 12px;font:inherit;font-size:.95rem;background:#fff;color:var(--ink)}
.aax .bk .in2:focus{outline:2px solid var(--gold);outline-offset:1px}
.aax .bk .rowp{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--line)}
.aax .bk .rowp span small{display:block;color:var(--mut);font-size:.78rem}
.aax .bk .stp{display:flex;align-items:center;gap:12px}
.aax .bk .stp button{width:32px;height:32px;border-radius:50%;border:1px solid var(--line);background:#fff;cursor:pointer;display:grid;place-items:center}
.aax .bk .stp button:focus-visible{outline:2px solid var(--gold)}
.aax .bk .stp output{min-width:18px;text-align:center;font-weight:800;font-variant-numeric:tabular-nums}
.aax .bk .tot{display:flex;justify-content:space-between;align-items:baseline;padding:14px 0 4px;font-variant-numeric:tabular-nums}
.aax .bk .tot b{font-family:var(--disp);font-size:1.5rem;font-weight:800}
.aax .bk .tot small{color:var(--mut);font-size:.8rem}
.aax .bk .gap{display:grid;gap:12px}
.aax .bk .btn{width:100%;margin-top:10px}
.aax .bk .done{margin-top:12px;padding:14px;border-radius:14px;background:var(--paper2);font-size:.9rem;line-height:1.45}
.aax .bk .done b{display:block;margin-bottom:2px}
.aax .bk .net{display:flex;justify-content:space-between;font-size:.86rem;padding:8px 12px;border-radius:12px;background:rgba(47,138,69,.09);color:var(--leaf);font-weight:700}
.aax .bk .demo{font-size:.74rem;color:var(--mut);text-align:center;margin:10px 0 0}
"""
rep('FONTS = \'<link rel="preconnect"', 'CSS += ' + repr(EXTRA_CSS) + '\nFONTS = \'<link rel="preconnect"')

# icono extra
rep(' "menu": \'<path d="M4 7h16M4 12h16M4 17h16"/>\',',
    ' "menu": \'<path d="M4 7h16M4 12h16M4 17h16"/>\',\n "doc": \'<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>\',\n "card": \'<rect x="3" y="6" width="18" height="13" rx="2.5"/><path d="M3 10h18M7 15h3"/>\',\n "brief": \'<rect x="3" y="7" width="18" height="13" rx="2.5"/><path d="M9 7V5h6v2M3 12h18"/>\',\n "tag": \'<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.3"/>\',')

# ---------- olas de la marca
rep("def ta_badge(text):", '''WAVE = '<svg class="wav {c}" viewBox="0 0 120 44" aria-hidden="true"><path d="M4 8c9-8 17-8 26 0s17 8 26 0 17-8 26 0 17 8 26 0"/><path d="M4 22c9-8 17-8 26 0s17 8 26 0 17-8 26 0 17 8 26 0"/><path d="M4 36c9-8 17-8 26 0s17 8 26 0 17-8 26 0 17 8 26 0"/></svg>'
def wave(c=""): return WAVE.replace("{c}", c)
def et_badge():
    return f'<span class="hbadge ets"><b>Since 1993</b> ICT tourism license 293</span>'
def ta_badge(text):''')

# ---------- header
rep('''<nav class="nav" id="nav"><a href="{base}index.html#tours">Tours</a><a href="{base}index.html#combos">Combos</a><a href="{base}index.html#plan">Plan my day</a><a href="{base}index.html#reviews">Reviews</a>''',
    '''<nav class="nav" id="nav"><a href="{base}index.html#tours">One day tours</a><a href="{base}index.html#plan">Plan my day</a><a href="{base}index.html#since">Since 1993</a><a class="ag" href="{base}index.html#agencies">Agencies</a>''')

# ---------- footer
rep('''<div><h4>Plan</h4><ul><li><a href="{base}index.html#combos">Two-in-one combos</a></li><li><a href="{base}index.html#plan">Help me choose</a></li><li><a href="{base}index.html#reviews">Reviews</a></li><li><a href="{wa('Hi! I would like a custom plan for my days in Arenal.')}" target="_blank" rel="noopener">Private or custom days</a></li></ul></div>''',
    '''<div><h4>Plan</h4><ul><li><a href="{base}index.html#plan">Help me choose</a></li><li><a href="{base}index.html#agencies">Travel agencies and DMCs</a></li><li><a href="{base}index.html#since">Since 1993</a></li><li><a href="{wa('Hi! I would like a private or custom tour from San José.')}" target="_blank" rel="noopener">Private or custom days</a></li></ul></div>''')
rep('''<li>{ic("send")}<a href="mailto:{e(B['email'])}">{e(B['email'])}</a></li>''',
    '''<li>{ic("chat")}Office {e(B['office'])}</li><li>{ic("globe")}USA &amp; Canada {e(B['tollfree'])}</li>''')
rep("def footer(base):\n    tl =", "def footer(base):\n    tl =")
rep('return sister_band() + f\'\'\'<footer class="foot">', 'return f\'\'\'<footer class="foot">')

# ---------- card grande
rep('("pin", "Hotel pickup in La Fortuna")', '("pin", "Pickup at your San José hotel")')

# ---------- reserva: tarjeta demo en vez del widget (el tenant aun no existe)
rep('''def rezzerva(t, inline_script=True):''', '''def booking_demo(t):
    p = t.get("price") or 0
    return f\'\'\'<div class="bk" data-price="{p}" data-child="{1 if t.get('child') else 0}" data-name="{e(t['title'])}">
<div class="tabs" role="tablist"><button type="button" class="on" data-tab="trav" role="tab" aria-selected="true">Traveler</button><button type="button" data-tab="agen" role="tab" aria-selected="false">Agency</button></div>
<div class="gap" data-pane="trav">
<div><label for="bk-date">Date</label><input class="in2" id="bk-date" type="date"></div>
<div><div class="rowp"><span><b>Adults</b><small>Ages 11 and up</small></span><span class="stp"><button type="button" data-k="ad" data-d="-1" aria-label="Fewer adults">{ic("x")}</button><output id="bk-ad">2</output><button type="button" data-k="ad" data-d="1" aria-label="More adults">{ic("plus")}</button></span></div>
{('<div class="rowp"><span><b>Children</b><small>Ages 3 to 10, 25% off</small></span><span class="stp"><button type="button" data-k="ch" data-d="-1" aria-label="Fewer children">' + ic("x") + '</button><output id="bk-ch">0</output><button type="button" data-k="ch" data-d="1" aria-label="More children">' + ic("plus") + '</button></span></div>') if t.get('child') else ''}</div>
<div class="tot"><span><small>Total with 13% tax</small></span><b id="bk-tot">$0</b></div>
<button class="btn btn-gold" type="button" id="bk-pay">{ic("card")} Pay by card and confirm</button>
<div class="done" id="bk-done" hidden><b>This is where your checkout opens.</b>Card payment inside this page, instant confirmation by email and the pickup time by WhatsApp. Powered by Rezzerva.</div>
</div>
<div class="gap" data-pane="agen" hidden>
<div><label for="bk-ag">Agency code</label><input class="in2" id="bk-ag" value="AG-0193" autocomplete="off"></div>
<div><label for="bk-cl">Client name and file</label><input class="in2" id="bk-cl" value="Smith family · File 4471" autocomplete="off"></div>
<div class="net"><span>Your net rate (example)</span><span id="bk-net">$0</span></div>
<button class="btn btn-ink" type="button" id="bk-cred">{ic("brief")} Book on credit</button>
<div class="done" id="bk-done2" hidden><b>Booking ET-24817 confirmed.</b>Voucher sent to your agency email, charged to your monthly statement. Nothing to pay today.</div>
</div>
<p class="demo">Demo: no real booking is made.</p>
</div>\'\'\'

def rezzerva(t, inline_script=True):''')
rep('''<div class="bw">{rezzerva(t, inline_script=False)}<noscript><div class="rz-fallback">Enable JavaScript to see live availability, or book by WhatsApp.</div></noscript></div>''',
    '''<div class="bw">{booking_demo(t)}</div>''')
rep('''<div class="bh">{price}{child}</div>''', '''<div class="bh">{price}{child}<div class="ch">Prices in USD plus 13% tax</div></div>''')
rep('''{ta_badge(B['ta_rating'] + ' · ' + str(B['ta_count']) + ' Tripadvisor reviews')}
<h1>{e(t['title'])}</h1>''', '''{et_badge()}
<h1>{e(t['title'])}</h1>''')
rep('''<div class="secure">{ic("lock")} Secure card payment · instant confirmation</div>{PAY}</div>
</aside>''', '''<div class="secure">{ic("lock")} Secure card payment · agencies on credit</div>{PAY}</div>
</aside>''')
rep('''<span>Online booking by <a class="rzl" href="https://rezzerva.com/" target="_blank" rel="noopener">Rezzerva</a></span>''',
    '''<span>Online booking and agency portal by <a class="rzl" href="https://rezzerva.com/" target="_blank" rel="noopener">Rezzerva</a></span>''')

# FAQ
rep('''FAQ_BASE = [
 ("Can I cancel?", "Yes. Cancel up to 24 hours before the tour and you get your money back. Plans change, we get it."),
 ("Where do you pick us up?", "At your hotel or rental in La Fortuna and the Arenal area. After booking we confirm the exact time by WhatsApp."),
 ("How do I pay?", "By card, right here, through a secure checkout. Your spot is confirmed instantly and the receipt arrives by email."),
]''', '''FAQ_BASE = [
 ("Can I cancel?", "Yes. Cancel 48 hours or more before the tour and we refund 90%. Later cancellations and no-shows are not refundable."),
 ("Where do you pick us up?", "At your hotel in San José and the surrounding area. After booking we confirm the exact pickup time by WhatsApp."),
 ("How do I pay?", "By card, right here, through a secure checkout. Your spot is confirmed and the receipt arrives by email."),
 ("I am a travel agency. Can I book for my clients?", "Yes. Agencies get their own access with net rates, bookings on credit, vouchers in their name and a monthly statement."),
]''')
rep('''    if t.get("child"): faq.insert(2, ("Do kids pay less?", f"Yes. {t['child']}."))''',
    '''    if t.get("child"): faq.insert(2, ("Do kids pay less?", f"Yes. {t['child']}. Babies up to 2 pay a seat fee."))
    if t.get("days"): faq.insert(1, ("Which days does it run?", t["days"] + "."))''')
rep('''<div class="eyb">Keep exploring</div><h2>Pairs well <em>with this.</em></h2>''', '''<div class="eyb">Keep exploring</div><h2>Another day <em>from San José.</em></h2>''')

# ---------- HOME
rep('''{ta_badge(B['ta_rating'] + ' · ' + str(B['ta_count']) + ' reviews on Tripadvisor')}
<h1>{B['h1']}</h1>''', '''{et_badge()}
<h1>{B['h1']}</h1>''')
rep('''<p>Pick a tour, a date and your group. You will see real spots and pay by card.</p>''', '''<p>Pick a tour, a date and your group. See the price, pay by card, done.</p>''')
rep('''<optgroup label="Tours">{opts}</optgroup><optgroup label="Two-in-one combos">{copts}</optgroup>''', '''<optgroup label="One day tours">{opts}</optgroup>''')
rep('''<div class="fnote">{ic("lock")} Free cancellation up to 24 h · Secure card payment</div>''', '''<div class="fnote">{ic("lock")} Hotel pickup in San José · Secure card payment</div>''')
rep('''<div class="dots">{dots}</div>
</section>''', '''<div class="dots">{dots}</div>{wave()}
</section>''')
rep('''<div class="eyb">Choose your kind of day</div><h2>Water, wildlife, <em>fire and forest.</em></h2>''', '''<div class="eyb">Choose your kind of day</div><h2>Craters, coffee, <em>rivers and sea.</em></h2>''')
rep('''<div class="eyb">Signature tours</div><h2>Our most-booked <em>days around Arenal.</em></h2>''', '''<div class="eyb">One day tours</div><h2>Out at sunrise, <em>back for dinner.</em></h2>''')
# combos -> agencias
s = re.sub(r'\n<div class="combos" id="combos">.*?\n</div>\n</div></section>', '\n<p class="tax">Prices per adult in USD, plus 13% tax. Hotel pickup in San José included.</p>\n</div></section>\n{agency_html}', s, count=1, flags=re.S)
rep('''<div class="eyb">From La Fortuna</div>''', '''<div class="eyb">From San José</div>''')
# reseñas -> confianza (sin reseñas reales todavia)
s = re.sub(r'\n<section class="sec dk" id="reviews">.*?</div></section>\n', '\n{trust_html}\n', s, count=1, flags=re.S)
rep('''    body = f\'\'\'
<section class="hero" id="top">''', '''    agency_html = agency_section()
    trust_html = trust_section()
    body = f\'\'\'
<section class="hero" id="top">''')
rep('''# ---------------------------------------------------------------- HOME''', '''# ---------------------------------------------------------------- AGENCIAS
AG_ROWS = [
 ("Nov 4", "Irazú, Orosi & Lankester", "Smith family", "File 4471", 4, "ok", "Confirmed"),
 ("Nov 5", "Poás, Doka, Grecia & Sarchí", "Grupo Morales", "File 4475", 12, "vo", "Voucher sent"),
 ("Nov 6", "Tortuga Island cruise", "J. Dupont", "File 4480", 2, "pe", "Pickup 6:15 a.m."),
 ("Nov 8", "La Paz Waterfall Gardens", "Chen + 3", "File 4483", 4, "ok", "Confirmed"),
]
def agency_section():
    rows = "".join(f\'<tr><td>{d}</td><td>{e(t)}</td><td>{e(c)}<small>{e(f)}</small></td><td>{n}</td><td><span class="st {k}">{e(st)}</span></td></tr>\' for d, t, c, f, n, k, st in AG_ROWS)
    feats = [("tag", "Your net rate, already applied", "Each agency sees its own contract rates. No price lists by email, no math."),
             ("brief", "Book on credit", "Confirm now, pay with your monthly statement. Your credit line and balance always in view."),
             ("doc", "Vouchers and pickup times, automatic", "The voucher goes out in your agency's name the moment you book. Pickup time follows by WhatsApp."),
             ("user", "Every booking under your client's file", "Search by passenger or file number. Your team sees the same bookings from any computer.")]
    fl = "".join(f\'<li><span class="fi">{ic(i)}</span><span><b>{e(a)}</b><small>{e(b)}</small></span></li>\' for i, a, b in feats)
    return f\'\'\'<section class="sec dk agency" id="agencies">{wave("a1")}{wave("a2")}<div class="w ag">
<div class="rv"><div class="eyb">For travel agencies and DMCs</div><h2>Your clients, our day tours. <em>One account.</em></h2>
<p class="lead">Since 1993 most incoming agencies in Costa Rica have trusted us with their FIT clients and their groups. Now your team books online, at your rate, on credit.</p>
<ul class="feat">{fl}</ul>
<div class="cta"><a class="btn btn-gold" href="{wa('Hola, somos una agencia y queremos acceso al portal de Expediciones Tropicales.')}" target="_blank" rel="noopener">Request agency access {ic("arrow")}</a><a class="btn btn-ghost" href="#agencies">{ic("lock")} Agency login</a></div></div>
<div class="portal rv" aria-label="Agency portal example">
<div class="ph1"><span><b>Agency portal</b><small>Andes &amp; Pacific Travel · AG-0193</small></span><span class="ex">Example data</span></div>
<div class="kp"><div><small>Credit used</small><b>$3,480</b><div class="bar"><i></i></div></div><div><small>Credit line</small><b>$10,000</b></div><div><small>November</small><b>22 pax</b></div></div>
<div class="tw"><table><thead><tr><th>Date</th><th>Tour</th><th>Client</th><th>Pax</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="pf"><span>October statement <b>$5,212 net</b></span><span>Due Nov 15 · <b>Download PDF</b></span></div>
</div>
</div></section>\'\'\'

def trust_section():
    facts = [("ICT license 293", "Authorized tour operator since 1993."), ("CST sustainability", "Certified for Sustainable Tourism."),
             ("Tour consolidator", "We run the daily departures that incoming agencies sell."), ("Costa Rica, Panama, Nicaragua", "Tours, transfers, hotels and packages.")]
    fh = "".join(f\'<div><b>{e(a)}</b><small>{e(b)}</small></div>\' for a, b in facts)
    return f\'\'\'<section class="sec" id="since"><div class="w trust">
<div class="rv"><div class="eyb">Since 1993</div><div class="yrs">30+<span>years</span></div><p class="lead">Three decades taking travelers out of San José in the morning and bringing them back with stories. Same office on Calle 3, same care.</p></div>
<div class="facts2 rv">{fh}</div>
</div></section>\'\'\'

# ---------------------------------------------------------------- HOME''')

# ---------- asistente: textos de La Fortuna
rep("'Contame un poco más: ¿agua, animales, volcán o algo de noche? ¿Van con niños? Si preferís, seguimos por", "'Contame un poco más: ¿volcanes, café, cataratas o playa? ¿Van con niños? Si preferís, seguimos por")
rep("'Tell me a little more. Water, wildlife, volcano or something after dark? Traveling with kids? You can also", "'Tell me a little more. Volcanoes, coffee, waterfalls or the beach? Traveling with kids? You can also")
rep("if(kids&&(t.c.indexOf('wildlife')>-1))", "if(kids&&(t.c.indexOf('forest')>-1))")
rep("if(easy&&t.c.indexOf('wildlife')>-1)", "if(easy&&(t.c.indexOf('culture')>-1||t.c.indexOf('forest')>-1))")
rep('''<br><small>Tap "See dates" to check real availability and book in a minute.</small>''', '''<br><small>Tap "See dates" to pick your day and book in a minute.</small>''')

# ---------- JS de la tarjeta de reserva demo
rep('''def js_home(base):''', '''def js_book():
    return r"""
(function(){var bk=document.querySelector('.aax .bk');if(!bk)return;var P=+bk.dataset.price,hasC=bk.dataset.child==='1',q={ad:2,ch:0};
function $(n){return '$'+n.toLocaleString('en-US',{minimumFractionDigits:0,maximumFractionDigits:2})}
var dt=document.getElementById('bk-date'),d=new Date(),u=new URLSearchParams(location.search);d.setDate(d.getDate()+2);dt.min=new Date().toISOString().slice(0,10);dt.value=u.get('date')||d.toISOString().slice(0,10);
if(u.get('pax'))q.ad=Math.max(1,Math.min(30,+u.get('pax')||2));
function upd(){document.getElementById('bk-ad').textContent=q.ad;var c=document.getElementById('bk-ch');if(c)c.textContent=q.ch;var sub=P*q.ad+(hasC?P*.75*q.ch:0);document.getElementById('bk-tot').textContent=$(Math.round(sub*1.13*100)/100);document.getElementById('bk-net').textContent=$(Math.round(P*.8*(q.ad+q.ch)*100)/100)+' + tax'}
bk.querySelectorAll('.stp button').forEach(function(b){b.onclick=function(){var k=b.dataset.k;q[k]=Math.max(k==='ad'?1:0,Math.min(30,q[k]+(+b.dataset.d)));upd()}});
bk.querySelectorAll('.tabs button').forEach(function(b){b.onclick=function(){bk.querySelectorAll('.tabs button').forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-selected',on)});bk.querySelectorAll('[data-pane]').forEach(function(p){p.hidden=p.dataset.pane!==b.dataset.tab})}});
document.getElementById('bk-pay').onclick=function(){document.getElementById('bk-done').hidden=false};
document.getElementById('bk-cred').onclick=function(){document.getElementById('bk-done2').hidden=false};
upd()})();
"""

def js_home(base):''')

# ---------- build: dominio de la demo, sin embed.js, sin bloques de WordPress de Driver
rep('DEMO_URL = "https://activearenal-demo.pages.dev/"', 'DEMO_URL = "https://expedicionestropicales.rezzerva.com/"')
rep('''        rz = '<script src="https://app.rezzerva.com/w/assets/embed.js" async></script>'
        open(os.path.join(d, "index.html"), "w").write(
            page(f'{t["title"]} · {B["name"]}', t["lead"], tb + schema_tour(t) + rz, "../../", "", cls=" has-mbar", og=absimg(t["hero"])))''',
    '''        rz = ""
        open(os.path.join(d, "index.html"), "w").write(
            page(f'{t["title"]} · {B["name"]}', t["lead"], tb + schema_tour(t), "../../", js_book(), cls=" has-mbar", og=absimg(t["hero"])))''')
rep('''    wb = home_body("/", False).replace('href="/tours/', 'href="/').replace(fab, "") + sister_band() + fab''',
    '''    wb = home_body("/", False).replace('href="/tours/', 'href="/').replace(fab, "") + fab''')
rep('''"provider": {"@type": "TravelAgency", "name": B["name"], "telephone": B["phone"], "url": B["url"]}}''',
    '''"provider": {"@type": "TravelAgency", "name": B["name"], "telephone": B["office"], "url": B["url"]}}''')
rep("<!-- Active Arenal · bloque KommPro/Rezzerva", "<!-- Expediciones Tropicales · bloque Rezzerva", 0)
rep("<!-- Active Arenal · pagina completa", "<!-- Expediciones Tropicales · pagina completa", 0)

open(p, "w", encoding="utf-8").write(s)
print("patched")

# ================= animaciones tipo Nacarcosta: reel vertical, titular palabra a palabra, contador
s = open(p, encoding="utf-8").read()
REEL_CSS = r"""
/* reel */
.aax .reel .rl{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.aax .rcard{position:relative;aspect-ratio:9/16;max-width:100%;border-radius:22px;overflow:hidden;background:var(--f);color:#fff;isolation:isolate}
.aax .rcard .ri{position:absolute;inset:0;background-size:cover;background-position:center;opacity:0;transform:scale(1.12);transition:opacity 1.1s ease}
.aax .rcard .ri.on{opacity:1;animation:kb 6.5s linear forwards}
@keyframes kb{from{transform:scale(1.14) translate(1.5%,1%)}to{transform:scale(1) translate(0,0)}}
.aax .rcard::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,14,10,.55),transparent 28%,transparent 55%,rgba(8,14,10,.85));z-index:1}
.aax .rcard .pb{position:absolute;left:12px;right:12px;top:12px;display:flex;gap:4px;z-index:2}
.aax .rcard .pb i{flex:1;height:3px;border-radius:3px;background:rgba(255,255,255,.3);overflow:hidden}
.aax .rcard .pb i b{display:block;height:100%;width:0;background:#fff}
.aax .rcard .pb i.done b{width:100%}
.aax .rcard .pb i.now b{animation:pbar 3.2s linear forwards}
@keyframes pbar{to{width:100%}}
.aax .rcard .rh2{position:absolute;left:12px;right:12px;top:24px;display:flex;align-items:center;gap:8px;z-index:2;font-size:.78rem;font-weight:700}
.aax .rcard .rh2 img{width:28px;height:28px;border-radius:50%;background:var(--gold)}
.aax .rcard .rc2{position:absolute;left:16px;right:16px;bottom:16px;z-index:2}
.aax .rcard .rc2 b{display:block;font-family:var(--script);font-weight:400;font-size:2rem;line-height:1;color:var(--gold)}
.aax .rcard .rc2 span{font-size:.86rem;color:rgba(255,255,255,.88)}
.aax .rcard:hover .rc2 span{text-decoration:underline;text-underline-offset:3px}
@media(max-width:960px){.aax .reel .rl{grid-template-columns:none;grid-auto-flow:column;grid-auto-columns:62%;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:6px}.aax .rcard{scroll-snap-align:start}}
@media(max-width:480px){.aax .reel .rl{grid-auto-columns:78%}}
/* titular palabra a palabra */
.aax .hero h1 .wd{display:inline-block;opacity:0;transform:translateY(.45em);filter:blur(6px);animation:wd .9s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes wd{to{opacity:1;transform:none;filter:none}}
.aax .rv.in .stg>*{animation:wd .8s cubic-bezier(.2,.7,.2,1) both}
.aax .stg>*:nth-child(2){animation-delay:.08s!important}.aax .stg>*:nth-child(3){animation-delay:.16s!important}.aax .stg>*:nth-child(4){animation-delay:.24s!important}.aax .stg>*:nth-child(5){animation-delay:.32s!important}
@media (prefers-reduced-motion:reduce){.aax .hero h1 .wd{opacity:1;transform:none;filter:none}.aax .rcard .ri.on{animation:none;transform:none}}
"""
s = s.replace("FONTS = '<link rel=\"preconnect\"", "CSS += " + repr(REEL_CSS) + "\nFONTS = '<link rel=\"preconnect\"", 1)

REEL_FN = '''REELS = [
 ("Irazú", "Above the clouds before 8 a.m.", ["img/ig-irazu.webp", "img/ig-lankester.webp", "img/ig-japanese-garden.webp"], "irazu-orosi-lankester"),
 ("Doka & Sarchí", "The golden bean and the oxcart painters", ["img/ig-doka.webp", "img/ig-sarchi-artisan.webp", "img/ig-sarchi-sign.webp"], "poas-doka-grecia-sarchi"),
 ("San Luis", "Zip lines over a cloud forest canyon", ["img/ig-zipline.webp", "img/ig-group.webp", "img/ig-trail.webp"], "san-luis-zip-lines"),
 ("Tortuga Island", "Ceviche, live music, white sand", ["img/ig-tortuga.webp", "img/ig-monkey.webp"], "tortuga-island-cruise"),
]
def reel_section(base):
    cards = ""
    for i, (t, c, ims, slug) in enumerate(REELS):
        ri = "".join(f\'<span class="ri{" on" if j==0 else ""}" style="background-image:url(\\\'{img(u,700)}\\\')"></span>\' for j, u in enumerate(ims))
        pb = "".join(\'<i><b></b></i>\' for _ in ims)
        cards += f\'<a class="rcard rv" href="{base}tours/{slug}/" style="transition-delay:{i*90}ms"><span class="pb">{pb}</span><span class="rh2"><img src="{img(B["logo"],80)}" alt="">expedicionestropicales</span>{ri}<span class="rc2"><b>{e(t)}</b><span>{e(c)}</span></span></a>\'
    return f\'\'\'<section class="sec reel" id="reel"><div class="w">
<div class="shd rv"><div><div class="eyb">This week on the road</div><h2>Straight from <em>our reels.</em></h2></div><p class="lead">What our guides see every morning out of San José. Tap a story to see that day.</p></div>
<div class="rl">{cards}</div></div></section>\'\'\'

# ---------------------------------------------------------------- AGENCIAS'''
s = s.replace("# ---------------------------------------------------------------- AGENCIAS", REEL_FN, 1)
s = s.replace('<section class="sec dk plan" id="plan">', '{reel_html}\n<section class="sec dk plan" id="plan">', 1)
s = s.replace("    agency_html = agency_section()", "    agency_html = agency_section()\n    reel_html = reel_section(base)", 1)
# contador en 30+
s = s.replace('<div class="yrs">30+<span>years</span></div>', '<div class="yrs"><span class="cnt2" data-to="33">33</span>+<span>years</span></div>', 1)
s = s.replace('.aax .yrs span{', '.aax .yrs .cnt2{font:inherit;color:inherit;margin:0;letter-spacing:inherit}\\n.aax .yrs span:not(.cnt2){', 1)
s = s.replace('<ul class="feat">{fl}</ul>', '<ul class="feat stg">{fl}</ul>', 1)
REEL_JS = r'''
/* reel: cada historia avanza sola, desfasadas */
(function(){var rm=matchMedia('(prefers-reduced-motion:reduce)').matches;document.querySelectorAll('.aax .rcard').forEach(function(c,ci){var im=c.querySelectorAll('.ri'),bars=c.querySelectorAll('.pb i'),k=0;
function show(n){im.forEach(function(x,i){x.classList.toggle('on',i===n)});bars.forEach(function(b,i){b.classList.toggle('done',i<n);b.classList.remove('now');if(i===n){void b.offsetWidth;b.classList.add('now')}})}
show(0);if(rm||im.length<2)return;setTimeout(function(){setInterval(function(){k=(k+1)%im.length;show(k)},3200)},ci*700)})})();
/* titular palabra a palabra */
(function(){var h=document.querySelector('.aax .hero h1');if(!h)return;var i=0;function wrap(n){Array.from(n.childNodes).forEach(function(c){if(c.nodeType===3){var f=document.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(function(w){if(!w)return;if(/^\s+$/.test(w)){f.appendChild(document.createTextNode(w));return}var s=document.createElement('span');s.className='wd';s.style.animationDelay=(0.15+i++*0.09)+'s';s.textContent=w;f.appendChild(s)});c.replaceWith(f)}else if(c.nodeType===1){if(c.tagName==='EM'){c.classList.add('wd');c.style.animationDelay=(0.15+i++*0.09)+'s'}else wrap(c)}})}wrap(h)})();
/* contador */
(function(){var c=document.querySelector('.aax .cnt2');if(!c)return;var to=+c.dataset.to;new IntersectionObserver(function(es,o){if(!es[0].isIntersecting)return;o.disconnect();var t0=performance.now();(function f(t){var p=Math.min(1,(t-t0)/1400);c.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(f)})(t0)},{threshold:.4}).observe(c)})();
'''
s = s.replace("/* hero carrusel */", REEL_JS + "\n/* hero carrusel */", 1)
open(p, "w", encoding="utf-8").write(s)
print("reel ok")

# ================= catalogo oficial (manual de ventas 2024-2025): logos, verde de marca, paquetes, tarifa neta por tour
s = open(p, encoding="utf-8").read()
def r2(a, b):
    global s
    if a not in s: sys.exit("NO ENCONTRADO 2: " + a[:80])
    s = s.replace(a, b, 1)
r2('''<div class="fl"><img src="{img(B['logo'],300)}"''', '''<div class="fl"><img src="{img(B.get('logo_foot') or B['logo'],300)}"''')
r2('''<span class="av"><img src="{img(B['logo'],120)}" alt=""></span>''', '''<span class="av"><img src="{img(B.get('mark') or B['logo'],120)}" alt=""></span>''')
r2('''<img src="{img(B["logo"],80)}" alt="">expedicionestropicales''', '''<img src="{img(B.get("mark") or B["logo"],80)}" alt="">expedicionestropicales''')
r2('<div class="bk" data-price="{p}" ', '<div class="bk" data-price="{p}" data-comm="{t.get(\'comm\', 20)}" ')
r2('<p class="demo">Demo: no real booking is made.</p>', '{(\'<p class="demo">Operates with a minimum of \' + str(t["min"]) + \' guests.</p>\') if t.get("min") else ""}<p class="demo">Demo: no real booking is made.</p>')
r2("document.getElementById('bk-net').textContent=$(Math.round(P*.8*(q.ad+q.ch)*100)/100)+' + tax'",
   "var cm=(+bk.dataset.comm||20)/100;document.getElementById('bk-net').textContent=$(Math.round(P*(1-cm)*(q.ad+(hasC?.75*q.ch:q.ch))*100)/100)+' + tax'")
r2('<div class="net"><span>Your net rate (example)</span>', '<div class="net"><span>Your net rate, {t.get(\'comm\', 20)}% commission off</span>')
r2('("tag", "Your net rate, already applied", "Each agency sees its own contract rates. No price lists by email, no math."),',
   '("tag", "Your net rate, already applied", "Commission from 10% to 23% depending on the tour, already off every price. No rate sheets by email, no math."),')
PKG = r'''
def packages_section():
    P = D.get("packages") or []
    if not P: return ""
    rows = "".join(f'<a class="pk rv" href="{wa("Hi! I would like information about the package " + x["code"] + " " + x["name"] + ".")}" target="_blank" rel="noopener"><span class="pc">{e(x["code"])}</span><span class="pn"><b>{e(x["name"])}</b><small>{e(x["route"])}</small></span><span class="pd">{x["days"]} days<br><small>{x["nights"]} nights</small></span><span class="pp"><small>From</small><b>{money(x["from"])}</b><small>per person</small></span></a>' for x in P)
    return f"""<section class="sec pks" id="packages"><div class="w">
<div class="shd rv"><div><div class="eyb">Vacation packages</div><h2>Ten ways to see the country, <em>tour by tour.</em></h2></div><p class="lead">From five days to two weeks, built around our day tours. From price per person in double occupancy, economy or tourist hotels, plus 13% tax. Ask us to tailor any of them.</p></div>
<div class="pkl">{rows}</div></div></section>"""

# ---------------------------------------------------------------- AGENCIAS'''
s = s.replace("# ---------------------------------------------------------------- AGENCIAS", PKG, 1)
r2("    agency_html = agency_section()\n", "    agency_html = packages_section() + agency_section()\n")
r2('<a href="{base}index.html#plan">Plan my day</a>', '<a href="{base}index.html#packages">Packages</a><a href="{base}index.html#plan">Plan my day</a>')
PCSS = r"""
.aax .logo img{height:46px}
.aax .hdr.sc .logo img{height:40px}
.aax .chat .av img{object-fit:contain;background:#fff;padding:3px}
.aax .pkl{display:grid;border-top:1px solid var(--line)}
.aax .pk{display:grid;grid-template-columns:70px minmax(0,1fr) 90px 120px;gap:18px;align-items:center;padding:18px 6px;border-bottom:1px solid var(--line);transition:background .2s}
.aax .pk:hover{background:var(--paper2)}
.aax .pk .pc{font-family:var(--disp);font-weight:800;font-size:.82rem;letter-spacing:.06em;color:var(--leaf)}
.aax .pk .pn b{display:block;font-family:var(--disp);font-weight:700;font-size:1.08rem}
.aax .pk .pn small{color:var(--mut);font-size:.9rem}
.aax .pk .pd{font-weight:700;font-size:.95rem;line-height:1.2}.aax .pk .pd small{color:var(--mut);font-weight:600}
.aax .pk .pp{text-align:right;font-variant-numeric:tabular-nums}.aax .pk .pp small{display:block;font-size:.72rem;color:var(--mut)}
.aax .pk .pp b{font-family:var(--disp);font-size:1.35rem;font-weight:800}
@media(max-width:700px){.aax .pk{grid-template-columns:56px minmax(0,1fr) auto;row-gap:6px}.aax .pk .pd{grid-column:2;grid-row:2;font-size:.85rem}.aax .pk .pd br{display:none}.aax .pk .pp{grid-row:1/span 2;grid-column:3}}
"""
s = s.replace("FONTS = '<link rel=\"preconnect\"", "CSS += " + repr(PCSS) + "\nFONTS = '<link rel=\"preconnect\"", 1)
open(p, "w", encoding="utf-8").write(s)
print("catalogo ok")

# ================= la pagina publica es solo para el turista: sin pestaña de agencia en la reserva
s = open(p, encoding="utf-8").read()
import re as _re
s, n1 = _re.subn(r'<div class="tabs" role="tablist">.*?</div>\n', '', s, count=1, flags=_re.S)
s, n2 = _re.subn(r'<div class="gap" data-pane="agen" hidden>.*?\n</div>\n', '', s, count=1, flags=_re.S)
s = s.replace("bk.querySelectorAll('.tabs button').forEach(function(b){b.onclick=function(){bk.querySelectorAll('.tabs button').forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-selected',on)});bk.querySelectorAll('[data-pane]').forEach(function(p){p.hidden=p.dataset.pane!==b.dataset.tab})}});", "")
s = s.replace("document.getElementById('bk-cred').onclick=function(){document.getElementById('bk-done2').hidden=false};", "")
s = s.replace("var cm=(+bk.dataset.comm||20)/100;document.getElementById('bk-net').textContent=$(Math.round(P*(1-cm)*(q.ad+(hasC?.75*q.ch:q.ch))*100)/100)+' + tax'", "")
s = s.replace('("I am a travel agency. Can I book for my clients?", "Yes. Agencies get their own access with net rates, bookings on credit, vouchers in their name and a monthly statement."),',
              '("I am a travel agency. Can I book for my clients?", "Yes, through the agency portal: your net rate, bookings on credit, vouchers in your name and a monthly statement. Ask us for access."),')
s = s.replace('<div class="secure">{ic("lock")} Secure card payment · agencies on credit</div>', '<div class="secure">{ic("lock")} Secure card payment · instant confirmation</div>')
assert n1 == 1 and n2 == 1, (n1, n2)
open(p, "w", encoding="utf-8").write(s)
print("solo turista ok")
