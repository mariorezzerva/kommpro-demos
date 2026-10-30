#!/usr/bin/env python3
"""Genera las páginas internas de kommpro.com (verticales y precio).

Uso:  python3 kommpro-src/build.py
Escribe en kommpro/distribuidores/, kommpro/outlet/, kommpro/ferreterias/ y kommpro/precio/.
Los estilos viven en kommpro/assets/kp.css. Editar textos aquí, no en el HTML generado.
"""
import html, json, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / "kommpro"
PRICE = "$99"
DEMO_MAIL = "mailto:hola@kommpro.com?subject=Quiero%20un%20demo%20de%20KommPro"

KPATH = '<path stroke-linecap="round" d="M30 24V76"/><path d="M60 43L70 33Q76 27 71 21Q66 16 60 22L32 50L60 78Q66 84 71 79Q76 73 70 67L60 57"/>'

ICONS = {
 "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "store": '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"/><path d="M2 7h20"/>',
 "card": '<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20"/>',
 "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
 "msg": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
 "box": '<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/><path d="M12 22V12"/><path d="m3.3 7 7.7 4.73a2 2 0 0 0 2 0L20.7 7"/>',
 "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
 "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/>',
 "chart": '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="m19 9-5 5-4-4-3 3"/>',
 "tag": '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5"/>',
 "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
 "lock": '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
 "building": '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
 "home": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
 "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
 "spark": '<path d="M9.94 15.5A2 2 0 0 0 8.5 14.06l-6.14-1.58a.5.5 0 0 1 0-.96L8.5 9.94A2 2 0 0 0 9.94 8.5l1.58-6.14a.5.5 0 0 1 .96 0l1.58 6.14a2 2 0 0 0 1.44 1.44l6.14 1.58a.5.5 0 0 1 0 .96l-6.14 1.58a2 2 0 0 0-1.44 1.44l-1.58 6.14a.5.5 0 0 1-.96 0z"/>',
 "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
 "barcode": '<path d="M3 5v14"/><path d="M8 5v14"/><path d="M12 5v14"/><path d="M17 5v14"/><path d="M21 5v14"/>',
 "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
 "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
 "excel": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="m8 12 4 5"/><path d="m12 12-4 5"/>',
}

def ic(name, cls="i", extra=""):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true"{extra}>{ICONS[name]}</svg>'

def e(s):
    return html.escape(s, quote=False)

NAV = [("distribuidores", "/distribuidores/", "Distribuidores"), ("outlet", "/outlet/", "Outlet"),
       ("ferreterias", "/ferreterias/", "Ferreterías"), ("precio", "/precio/", "Precio"), ("contacto", "#contacto", "Contacto")]

def head(title, desc, canonical):
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0C0F22">
<title>{e(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://kommpro.com{canonical}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="https://kommpro.com/img/kommpro-icon-512.png">
<link rel="icon" href="/img/kommpro-k.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/kp.css?v=2">
</head>
<body>
'''

def header(active):
    links = "".join(f'<a href="{h}"{" class=\"on\" aria-current=\"page\"" if k == active else ""}>{t}</a>' for k, h, t in NAV)
    return f'''<header id="hd">
<div class="w">
<a href="/" class="brandh" aria-label="KommPro, inicio"><svg class="hk" viewBox="0 0 100 100" aria-hidden="true"><rect width="100" height="100" rx="24" fill="#B4C5FF"/><g fill="none" stroke="#0C0F22" stroke-width="9" stroke-linejoin="round">{KPATH}</g></svg><span class="logo" aria-hidden="true"><b>KOMM</b><i>pro</i></span></a>
<nav class="mn" aria-label="Principal">{links}</nav>
<div class="hr"><a href="https://app.kommpro.com" class="login">Iniciar sesión</a><a href="{DEMO_MAIL}" class="btn btn-m">Solicitar demo</a></div>
<button class="burger" id="burger" aria-expanded="false" aria-controls="mmenu" aria-label="Abrir menú"><svg class="i" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
</div>
<div class="mmenu" id="mmenu">{links}<a href="https://app.kommpro.com">Iniciar sesión</a><a href="{DEMO_MAIL}" class="btn btn-m">Solicitar demo</a></div>
</header>
'''

def footer():
    return f'''<footer id="contacto">
<div class="w">
<div class="tp">
<div class="bd"><span class="brand"><svg class="kicon" viewBox="0 0 100 100" aria-hidden="true"><rect width="100" height="100" rx="24" fill="#141A36"/><g fill="none" stroke="#B4C5FF" stroke-width="9" stroke-linejoin="round">{KPATH}</g></svg><span class="logo" aria-hidden="true"><b>KOMM</b><i>pro</i></span></span>
<p>Tienda, inventario y pago en línea en una sola plataforma, para comercios que ya venden en mostrador. Hecho en Costa Rica.</p>
<p><a href="mailto:hola@kommpro.com" style="color:var(--ink);font-weight:600">hola@kommpro.com</a></p></div>
<div class="col"><h4>Producto</h4><a href="/distribuidores/">Distribuidores y mayoristas</a><a href="/outlet/">Outlet y hogar</a><a href="/ferreterias/">Ferreterías</a><a href="/precio/">Precio</a><a href="https://app.kommpro.com">Acceso comercios</a></div>
<div class="col"><h4>KommPro</h4><a href="{DEMO_MAIL}">Solicitar demo</a><a href="mailto:hola@kommpro.com?subject=Soporte%20KommPro">Soporte</a><a href="mailto:hola@kommpro.com">Contacto</a></div>
</div>
<div class="bt"><span>© 2026 KommPro · Costa Rica</span><span>Pagos con tarjeta procesados por Onvo</span></div>
</div>
</footer>
'''

SCRIPT = '''<script>
(function(){
var b=document.getElementById('burger'),m=document.getElementById('mmenu');
if(b)b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)});
if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){document.body.classList.add('io');
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){var el=x.target,i=[].indexOf.call(el.parentNode.children,el);el.style.transitionDelay=Math.min(i,5)*.07+'s';el.classList.add('in');io.unobserve(el)}})},{rootMargin:'0px 0px -6% 0px'});
document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});setTimeout(function(){document.querySelectorAll('.rv').forEach(function(el){el.classList.add('in')})},4500)}
})();
</script>
'''

def kbg(cls):
    return f'<svg class="kbg {cls}" viewBox="0 0 100 100" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="9" stroke-linejoin="round">{KPATH}</g></svg>'

# ---------------------------------------------------------------- piezas comunes

PLAN_FEATS = [
 "Tienda en línea con tu marca, en tu dominio o en tu WordPress",
 "Catálogo ordenado por pasillos, con fotos y nombres claros",
 "Inventario sincronizado con tu sistema de caja o bodega",
 "Cobro con tarjeta por Onvo, directo a tu cuenta IBAN",
 "Asistente de compra que arma el pedido por chat",
 "Panel en app.kommpro.com: pedidos, existencias y clientes",
 "Entrega con tu ruta o retiro en tienda",
 "Instalación y atención personal por chat",
]

def plan_card(label):
    lis = "".join(f'<li>{ic("check")}{e(f)}</li>' for f in PLAN_FEATS)
    return f'''<div class="plan rv">
<div class="tp">Plan KommPro</div>
<div class="nm">{e(label)}</div>
<div class="amt"><strong>{PRICE}</strong><span>+ IVA al mes, todo incluido</span></div>
<div class="fee">Sin comisión de KommPro por venta*</div>
<ul>{lis}<li>{ic("truck")}<span>Envíos con Correos de Costa Rica <span class="tg soon">Próximamente</span></span></li></ul>
<a href="{DEMO_MAIL}" class="btn btn-m">Solicitar demo{ic("arrow","i ar")}</a>
</div>'''

FINE = "* Solo pagás el procesamiento de tarjeta de Onvo, a su tarifa estándar, en las ventas pagadas en línea. Precios en dólares, más IVA."

SECURITY = [
 ("La tarjeta nunca toca nuestros servidores", "Los datos de pago se capturan en el formulario seguro de Onvo. KommPro nunca los ve ni los guarda."),
 ("El dinero va directo a tu cuenta", "Cada cobro se hace a nombre de tu empresa y se deposita en tu cuenta IBAN en Costa Rica."),
 ("Cada unidad se vende una sola vez", "Si dos personas compran lo último al mismo tiempo, la existencia se respeta. Sin sobreventas ni llamadas incómodas."),
 ("Pedido confirmado solo cuando el pago entra", "El pedido pasa a despacho cuando Onvo avisa que el pago fue aprobado, y cada aviso se procesa una sola vez."),
]

COMPARE = [
 ("Inventario", "Una sola existencia con tu caja", "Aparte, actualizado a mano"),
 ("Comisión por venta", "Sin comisión de KommPro", "Comisión de la plataforma, más la tarjeta"),
 ("Catálogo", "Lo ordenamos por vos", "Lo cargás vos, producto por producto"),
 ("Pedidos por chat", "Asistente incluido", "App aparte o no existe"),
 ("Dónde cae tu plata", "En tu cuenta en Costa Rica", "Procesadores del extranjero"),
]

def common_bottom(v):
    sec = "".join(f'<div class="nb rv"><b>0{i+1}</b><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i, (t, p) in enumerate(SECURITY))
    rows = '<div class="rw"><div></div><div>KommPro</div><div>Otras plataformas</div></div>' + "".join(
        f'<div class="rw"><div>{e(a)}</div><div>{e(b)}</div><div>{e(c)}</div></div>' for a, b, c in COMPARE)
    faqs = "".join(f'<details class="rv"><summary>{e(q)}<i>+</i></summary><div class="an">{e(a)}</div></details>' for q, a in v["faq"])
    return f'''
<div class="w">
<div class="inst rv">
<div><h2 class="bg">¿Ayuda con la instalación?</h2><p>Lo dejamos todo funcionando por vos, sin costo extra: ordenamos tu catálogo, conectamos tu sistema de caja, instalamos la tienda en tu sitio y abrimos tu cuenta de cobro con Onvo.</p></div>
<div class="ctas"><a href="/precio/" class="btn btn-l">Ver precio</a><a href="{DEMO_MAIL}" class="btn btn-m">Solicitar demo{ic("arrow","i ar")}</a></div>
</div>
</div>

<section class="s" aria-labelledby="t-cmp"><div class="w">
<div class="ctr rv"><p class="eye">La diferencia</p><h2 id="t-cmp" class="bg">KommPro vs. otras plataformas</h2></div>
<div class="cmp rv">{rows}</div>
<p class="cmp-note">Con KommPro pagás una mensualidad fija y el procesamiento de tarjeta de Onvo. No hay comisión de KommPro por cada venta.</p>
</div></section>

<section class="dark star" style="margin-top:110px" aria-labelledby="t-sec"><div class="w">
<div class="ctr rv"><p class="eye">Seguridad y confianza con Onvo</p><h2 id="t-sec" class="bg">Tu plata y la de tus clientes, en buenas manos.</h2></div>
<div class="trio four">{sec}</div>
<div class="onvo rv">Cobros procesados por <b>ONVO</b></div>
</div></section>

<section class="s" aria-labelledby="t-faq"><div class="w">
<div class="ctr rv"><p class="eye">Preguntas frecuentes</p><h2 id="t-faq" class="bg">Lo que nos preguntan antes de empezar</h2></div>
<div class="faq">{faqs}</div>
</div></section>

<section class="cta" aria-labelledby="t-cta"><div class="in rv">{kbg("")}
<h2 id="t-cta" class="bg">{e(v["cta_h"])}</h2>
<p>Te mostramos KommPro con tus propios productos y precios. Sin compromiso.</p>
<div class="ctas"><a href="{DEMO_MAIL}" class="btn btn-m">Solicitar demo{ic("arrow","i ar")}</a><a href="/precio/" class="btn btn-l">Ver precio</a></div>
</div></section>
'''

# ---------------------------------------------------------------- verticales

PH = lambda pid, w=1800: f"https://images.unsplash.com/{pid}?auto=format&fit=crop&w={w}&q=72"

VERT = {
"distribuidores": dict(
 title="Tienda en línea para distribuidoras y mayoristas | KommPro",
 desc="Pedidos de comercios y empresas pagados con tarjeta, con el inventario de tu bodega sincronizado. $99 + IVA al mes, sin comisión de KommPro por venta. Hecho en Costa Rica.",
 photo="photo-1605371924599-2d0365da1ae0", pos="62% center",
 chip="Para distribuidoras y mayoristas · Hecho en Costa Rica",
 h1a="Tu bodega vendiendo en línea,", h1b="con la existencia al día.",
 bullets=["Pedidos de comercios y empresas, pagados al confirmar", "Inventario sincronizado con tu sistema de caja o bodega", "$99 + IVA al mes. Sin comisión de KommPro por venta."],
 shop=dict(name="Tu distribuidora", aisles=["Abarrotes", "Confites", "Bebidas", "Limpieza"], rows=[("box","Arroz 1,8 kg","Caja de 10","₡21.500"),("box","Galletas surtidas","Display de 24","₡14.800"),("box","Refresco 2,5 L","Paca de 6","₡9.900")], pay="Pagar ₡46.200 con tarjeta"),
 fl1=("check","Pedido #10482 pagado","Minisúper San Pedro"), fl2=("repeat","Caja y web: 24 = 24","Una sola existencia"),
 q=("¿Cuántos pedidos se te quedan ", "en WhatsApp?"),
 con_h="Recibí pedidos, cobrá con tarjeta y despachá. Todo en uno.",
 con=["Catálogo por pasillos, con precios por unidad y por caja","Pedidos de comercios y empresas, pagados al confirmar","Datos para factura electrónica en el checkout","El pago entra directo a tu cuenta IBAN","Lo configurás vos, o lo cargamos por vos sin costo extra"],
 pic=("Pedido para la ruta de mañana","Oficinas Central · 18 productos","₡186.400","Pagado"),
 tipos_h="Del minisúper a la oficina, cada cliente como compra.",
 tipos_sub="Comercios que revenden o empresas que compran lo del mes. La misma tienda se adapta a cada uno.",
 tipos=[("store","Para revender","Comercios y pulperías","Minisúpers, sodas y pulperías que surten cada semana. Ven tu precio, arman el pedido y pagan en línea."),
        ("building","Para consumo","Empresas e instituciones","Oficinas, condominios y colegios que compran lo del mes. Piden con cédula jurídica y reciben su factura electrónica.")],
 steps=[("Ordenamos tu catálogo","Tomamos lo que exportás de tu sistema, por desordenado que esté, y lo dejamos con nombres claros, fotos y pasillos."),
        ("La tienda vive en tu web","En tu dominio o en tu WordPress actual. Tu cliente compra sin salir de tu marca, desde la compu o el celular."),
        ("Cobrás directo","Cada pedido llega pagado y el dinero cae en tu cuenta. Sin comisión de KommPro por venta: solo el procesamiento de tarjeta de Onvo.")],
 phone=[("Arroz 1,8 kg","Caja de 10 · ₡21.500","2"),("Aceite 900 ml","Caja de 12 · ₡18.900","1"),("Azúcar 2 kg","Fardo de 10 · ₡16.400","1")], ptot=("₡78.300","Factura a cédula jurídica"),
 why_h=("Hecho para el comercio con bodega.", "No para un marketplace."),
 demos=True,
 cta_h="Este fin de año, con pedidos en tu web.",
 faq=[("¿Funciona con mi sistema de caja o bodega?","Sí. Trabajamos con el export de tu sistema de caja o bodega, o con conexión directa cuando el sistema lo permite. No tenés que cambiar de sistema."),
      ("¿Puedo vender por unidad y por caja?","Sí. Cada producto puede tener su presentación por unidad, caja, paca o fardo, cada una con su precio."),
      ("¿Mis clientes empresa reciben factura electrónica?","El checkout pide nombre de la empresa, cédula jurídica y correo, para que emitas la factura electrónica con tu sistema de siempre."),
      ("¿Cómo recibo el dinero?","Cada pago se hace a nombre de tu empresa con Onvo y se deposita en tu cuenta IBAN en Costa Rica."),
      ("¿Hay mensualidad?","Sí: $99 + IVA al mes, todo incluido. No hay comisión de KommPro por venta; solo pagás el procesamiento de tarjeta de Onvo en las ventas en línea."),
      ("¿Hacen envíos?","Desde el primer día: entrega con tu propia ruta o retiro en bodega. Los envíos con Correos de Costa Rica integrados vienen pronto."),
      ("¿Y si no tengo fotos de los productos?","Las conseguimos o las limpiamos sobre fondo blanco como parte del orden del catálogo.")]),

"outlet": dict(
 title="Tienda en línea para outlets y tiendas de hogar | KommPro",
 desc="Muebles, decoración y electrodomésticos en línea, con la existencia del piso sincronizada y cobro con tarjeta. $99 + IVA al mes, sin comisión de KommPro por venta.",
 photo="photo-1740759546813-6b58d44f5dce", pos="center",
 chip="Para outlets y tiendas de hogar · Hecho en Costa Rica",
 h1a="Lo que entra a tu piso,", h1b="vendiéndose en línea.",
 bullets=["Mercadería que rota cada semana, publicada sin tocar la tienda a mano", "Lo vendido en el piso se baja solo de la web", "$99 + IVA al mes. Sin comisión de KommPro por venta."],
 shop=dict(name="Tu outlet", aisles=["Sala","Comedor","Cocina","Ofertas"], rows=[("home","Sofá de 3 plazas","Última unidad","₡289.000"),("home","Lámpara de mimbre","Quedan 4","₡34.900"),("tag","Juego de vajilla","Oferta de temporada","₡24.500")], pay="Pagar ₡348.400 con tarjeta"),
 fl1=("check","Sofá vendido en el piso","Ya no aparece en la web"), fl2=("truck","Entrega el sábado","Escazú · retiro o envío"),
 q=("¿Cuántas ventas se pierden porque ", "nadie sabe qué llegó?"),
 con_h="Publicá lo que entra, cobrá con tarjeta y entregá. Todo en uno.",
 con=["Productos nuevos publicados en minutos, con foto y precio","Ofertas y temporadas que se activan y se apagan solas","Última unidad: lo que se vende en el piso se baja de la web","El pago entra directo a tu cuenta IBAN","Lo configurás vos, o lo cargamos por vos sin costo extra"],
 pic=("Entró mercadería nueva","32 productos publicados hoy","Sala y comedor","En línea"),
 tipos_h="Del mueble grande al detalle de cocina, cada producto como se vende.",
 tipos_sub="Piezas únicas que se van rápido o artículos de volumen con varias unidades. La tienda maneja los dos.",
 tipos=[("home","Piezas únicas","Muebles y lotes","Sofás, comedores y lotes de una sola unidad. Se venden una vez y desaparecen de la web solos."),
        ("tag","Volumen","Decoración y cocina","Vajillas, lámparas y textiles con varias unidades, variantes de color y ofertas por temporada.")],
 steps=[("Ordenamos tu catálogo","Tomamos tu inventario actual y lo dejamos por ambientes: sala, comedor, cocina, ofertas. Con fotos limpias y nombres claros."),
        ("La tienda vive en tu web","En tu dominio o en tu WordPress actual. Tu cliente ve lo que hay hoy, lo aparta pagando y elige entrega o retiro."),
        ("Cobrás directo","Cada venta llega pagada y el dinero cae en tu cuenta. Sin comisión de KommPro por venta: solo el procesamiento de tarjeta de Onvo.")],
 phone=[("Sofá de 3 plazas","Última unidad · ₡289.000","1"),("Lámpara de mimbre","₡34.900","1"),("Cojines de lino","Juego de 2 · ₡18.500","2")], ptot=("₡360.900","Entrega o retiro en tienda"),
 why_h=("Hecho para la tienda que rota.", "No para el catálogo que nunca cambia."),
 demos=False,
 cta_h="Que lo nuevo se venda antes de llegar al piso.",
 faq=[("¿Funciona con mi sistema de caja?","Sí. Trabajamos con el export de tu sistema de caja, o con conexión directa cuando el sistema lo permite. No tenés que cambiar de sistema."),
      ("¿Qué pasa si vendo en el piso algo que está en la web?","La existencia es una sola: cuando se vende en caja, se baja de la tienda en línea. Si era la última unidad, deja de aparecer."),
      ("¿Puedo poner ofertas por temporada?","Sí. Ofertas con fecha de inicio y fin, precio anterior tachado y una sección de ofertas en la tienda."),
      ("¿Cómo recibo el dinero?","Cada pago se hace a nombre de tu empresa con Onvo y se deposita en tu cuenta IBAN en Costa Rica."),
      ("¿Hay mensualidad?","Sí: $99 + IVA al mes, todo incluido. No hay comisión de KommPro por venta; solo pagás el procesamiento de tarjeta de Onvo en las ventas en línea."),
      ("¿Cómo hago con los muebles grandes?","Cada producto puede llevar su forma de entrega: retiro en tienda, entrega con tu transporte o envío. Los envíos con Correos de Costa Rica integrados vienen pronto.")]),

"ferreterias": dict(
 title="Tienda en línea para ferreterías y depósitos | KommPro",
 desc="Miles de códigos y medidas ordenados por pasillos, con la existencia de tu caja y cobro con tarjeta. $99 + IVA al mes, sin comisión de KommPro por venta.",
 photo="photo-1731694411560-050e5b91e943", pos="center",
 chip="Para ferreterías y depósitos · Hecho en Costa Rica",
 h1a="Toda tu ferretería,", h1b="encontrable en línea.",
 bullets=["Miles de códigos, medidas y presentaciones, ordenados por pasillos", "El cliente encuentra el tornillo exacto, paga y lo retira listo", "$99 + IVA al mes. Sin comisión de KommPro por venta."],
 shop=dict(name="Tu ferretería", aisles=["Tornillería","Eléctrico","Pintura","Fontanería"], rows=[("wrench","Tornillo gypsum 1 1/4\"","Caja de 100","₡2.950"),("wrench","Cable THHN #12","Rollo de 100 m","₡38.500"),("wrench","Pintura látex blanco","Galón","₡14.900")], pay="Pagar ₡56.350 con tarjeta"),
 fl1=("check","Pedido listo para retiro","Mostrador 2 · 10:30 a. m."), fl2=("repeat","Caja y web: 312 = 312","Una sola existencia"),
 q=("¿Cuántas llamadas al día son para preguntar ", "“¿tienen esto?”"),
 con_h="Que te encuentren, que paguen y que retiren. Todo en uno.",
 con=["Búsqueda por nombre, medida o código, como pregunta el cliente","Existencia real por producto, al día con tu caja","Retiro en mostrador con el pedido ya pagado y alistado","El pago entra directo a tu cuenta IBAN","Lo configurás vos, o lo cargamos por vos sin costo extra"],
 pic=("Búsqueda: “tornillo para gypsum”","14 resultados · 3 medidas","Pasillo 4","En existencia"),
 tipos_h="Del maestro de obras al cliente de fin de semana.",
 tipos_sub="Quien compra por volumen para la obra y quien viene por una pieza. La misma tienda atiende a los dos.",
 tipos=[("building","Obra y contratistas","Pedidos de volumen","Maestros de obras y constructoras que piden la lista completa, pagan en línea y retiran o reciben en el proyecto."),
        ("home","Hogar","Cliente de fin de semana","Quien busca la pieza exacta para una reparación. La encuentra por nombre o medida y la retira lista.")],
 steps=[("Ordenamos tu catálogo","Tomamos el export de tu sistema, con sus abreviaturas y códigos, y lo dejamos con nombres claros, medidas y pasillos."),
        ("La tienda vive en tu web","En tu dominio o en tu WordPress actual. El cliente busca como pregunta en el mostrador y ve si hay existencia."),
        ("Cobrás directo","Cada pedido llega pagado y el dinero cae en tu cuenta. Sin comisión de KommPro por venta: solo el procesamiento de tarjeta de Onvo.")],
 phone=[("Tornillo gypsum 1 1/4\"","Caja de 100 · ₡2.950","3"),("Masilla para gypsum","Cubeta · ₡12.400","1"),("Cinta de papel","Rollo 75 m · ₡1.900","2")], ptot=("₡25.050","Retiro en mostrador"),
 why_h=("Hecho para quien conoce cada pasillo.", "No para tiendas genéricas."),
 demos=False,
 cta_h="Que el cliente llegue con el pedido ya pagado.",
 faq=[("¿Funciona con mi sistema de caja?","Sí. Trabajamos con el export de tu sistema de caja, o con conexión directa cuando el sistema lo permite. No tenés que cambiar de sistema."),
      ("Tengo miles de códigos con abreviaturas. ¿Se pueden ordenar?","Sí, es parte del servicio. Pasamos los nombres de tu sistema a nombres claros, con medida y presentación, y los ubicamos por pasillo."),
      ("¿Cómo funciona el retiro en tienda?","El cliente paga en línea, a tu equipo le llega el pedido al panel para alistarlo y el cliente solo pasa a recogerlo."),
      ("¿Cómo recibo el dinero?","Cada pago se hace a nombre de tu empresa con Onvo y se deposita en tu cuenta IBAN en Costa Rica."),
      ("¿Hay mensualidad?","Sí: $99 + IVA al mes, todo incluido. No hay comisión de KommPro por venta; solo pagás el procesamiento de tarjeta de Onvo en las ventas en línea."),
      ("¿Puedo vender a contratistas con factura?","Sí. El checkout pide los datos de la empresa y la cédula jurídica para la factura electrónica.")]),
}

STAR_FEATS = [
 ("store","Se conecta con lo que ya usás","Tu sistema de caja o bodega actual, por export o conexión directa."),
 ("barcode","Por código de barras o interno","Cada producto de la web se enlaza con su código en tu sistema."),
 ("bell","Alertas de existencia baja","Te avisa antes de que se agote lo que más se vende."),
 ("repeat","Caja y web en los dos sentidos","Lo vendido en el mostrador baja en la web, y lo vendido en la web baja en la caja."),
 ("chart","Ventas del día en un panel","Mostrador y web juntos, con lo que más se mueve."),
 ("excel","Tu Excel, adentro","Subís el Excel de productos que ya usás y se llena solo."),
]

def vertical(key):
    v = VERT[key]
    sh = v["shop"]
    aisles = "".join(f'<span{" class=\"on\"" if i == 0 else ""}>{e(a)}</span>' for i, a in enumerate(sh["aisles"]))
    rows = "".join(f'<div class="row"><span class="th">{ic(i_)}</span><span class="n">{e(n)}<small>{e(s)}</small></span><span class="p">{e(p)}</span></div>' for i_, n, s, p in sh["rows"])
    bl = "".join(f"<li>{e(b)}</li>" for b in v["bullets"])
    con = "".join(f'<li>{ic("check")}<span>{e(c)}</span></li>' for c in v["con"])
    tipos = "".join(f'<div class="tipo rv"><span class="ic">{ic(i_)}</span><small>{e(s)}</small><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i_, s, t, p in v["tipos"])
    steps = "".join(f'<div class="step rv"><b>0{i+1}</b><div><h3>{e(t)}</h3><p>{e(p)}</p></div></div>' for i, (t, p) in enumerate(v["steps"]))
    prow = "".join(f'<div class="it"><span class="th">{ic("box")}</span><span class="n">{e(n)}<br><small>{e(s)}</small></span><span class="q2"><i>-</i>{e(q)}<i>+</i></span></div>' for n, s, q in v["phone"])
    feats = "".join(f'<div class="ft rv"><span class="ic">{ic(i_)}</span><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i_, t, p in STAR_FEATS)
    why = [("globe","Tu tienda, en tu dominio","Google encuentra tus productos a tu nombre. Cada venta fortalece tu marca, no la de un marketplace."),
           ("repeat","Una sola existencia","Lo que ves en la web es lo que hay en tu bodega. Nadie paga por algo que ya se vendió."),
           ("card","Sin comisión por venta","Una mensualidad fija. KommPro no se queda con un porcentaje de cada pedido.")]
    whyh = "".join(f'<div class="c rv"><span class="ic">{ic(i_)}</span><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i_, t, p in why)
    f1, f2 = v["fl1"], v["fl2"]
    pic = v["pic"]
    demos = ""
    if v["demos"]:
        demos = f'''
<section class="s" aria-labelledby="t-demos"><div class="w">
<div class="ctr rv"><p class="eye">Demos</p><h2 id="t-demos" class="bg">Así se ve una tienda KommPro.</h2><p class="sub">Dos distribuidoras de Costa Rica ya tienen la suya armada con sus productos reales. Pedinos verlas y te mostramos la que más se parece a tu negocio.</p></div>
<div class="demos">
<div class="demo rv"><div class="im" style="background-image:url('{PH("photo-1670684684445-a4504dca0bbc",1200)}')"><span class="chip">Mayoreo y detalle</span></div><div class="ct"><h3>Distribuidora de confites, abarrotes y fiesta</h3><p>Más de 2.600 productos por pasillos, asistente que arma el pedido de la piñata o lo de la oficina, y panel sincronizado con la caja.</p><div class="pills"><span>Asistente por chat</span><span>Caja sincronizada</span><span>Pago con tarjeta</span></div><a class="lnk" href="mailto:hola@kommpro.com?subject=Quiero%20ver%20la%20demo%20de%20distribuidora%20de%20abarrotes">Pedí ver la demo {ic("arrow")}</a></div></div>
<div class="demo rv"><div class="im" style="background-image:url('{PH("photo-1664382953403-fc1ac77073a0",1200)}')"><span class="chip">Empresas e instituciones</span></div><div class="ct"><h3>Fábrica de productos de limpieza</h3><p>Tienda para empresas con checkout a cédula jurídica, asistente que recomienda por necesidad (cocina, baños, cómputo) y bodega al día.</p><div class="pills"><span>Factura electrónica</span><span>Venta a empresas</span><span>Bodega al día</span></div><a class="lnk" href="mailto:hola@kommpro.com?subject=Quiero%20ver%20la%20demo%20de%20f%C3%A1brica%20de%20limpieza">Pedí ver la demo {ic("arrow")}</a></div></div>
</div>
</div></section>'''
    body = f'''<main>
<section class="vh" aria-labelledby="t-hero">
<div class="ph" style="background-image:url('{PH(v["photo"])}');background-position:{v["pos"]}"></div>
<div class="w">
<div>
<span class="chip rv">{e(v["chip"])}</span>
<h1 id="t-hero" class="bg rv">{e(v["h1a"])} <em>{e(v["h1b"])}</em></h1>
<ul class="bl rv">{bl}</ul>
<div class="ctas rv"><a href="{DEMO_MAIL}" class="btn btn-m">Solicitar demo{ic("arrow","i ar")}</a><a href="#como" class="btn btn-l">Ver cómo funciona</a></div>
</div>
<div class="mock rv" aria-hidden="true">
<div class="glass shop"><div class="top"><b>{e(sh["name"])}</b><span>Tienda en línea</span></div>
<div class="srch">{ic("search")}¿Qué estás buscando?</div>
<div class="aisles">{aisles}</div>
<div class="rows">{rows}</div>
<div class="pay">{ic("lock")}{e(sh["pay"])}</div></div>
<div class="fl fl1 glass"><b>{ic(f1[0])}</b><span><strong>{e(f1[1])}</strong><small>{e(f1[2])}</small></span></div>
<div class="fl fl2 glass"><b>{ic(f2[0])}</b><span><strong>{e(f2[1])}</strong><small>{e(f2[2])}</small></span></div>
</div>
</div>
</section>

<section class="q" aria-label="El problema"><div class="w"><h2 class="bg rv">{e(v["q"][0])}<span>{e(v["q"][1])}</span></h2>
<div class="con">
<div class="pic rv" style="background-image:url('{PH(v["photo"],1200)}')" aria-hidden="true"><div class="glass"><strong>{e(pic[0])}</strong>{e(pic[1])}<div class="bar"><span>{e(pic[2])}</span><b>{e(pic[3])}</b></div></div></div>
<div class="box rv"><p class="eye">Con KommPro</p><h3 class="bg">{e(v["con_h"])}</h3><ul class="ck">{con}</ul></div>
</div>
</div></section>

<section class="s" aria-labelledby="t-tipos"><div class="w">
<div class="ctr rv"><p class="eye">Para cada tipo de cliente</p><h2 id="t-tipos" class="bg">{e(v["tipos_h"])}</h2><p class="sub">{e(v["tipos_sub"])}</p></div>
<div class="tipos">{tipos}</div>
<p class="more rv"><a class="lnk" href="{DEMO_MAIL}">¿Tu operación es distinta? Hablemos {ic("arrow")}</a></p>
</div></section>

<section class="how" id="como" aria-labelledby="t-how">
<div class="l" aria-hidden="true">
<div class="phone"><div class="scr"><div class="sb"><span>9:12</span><span>5G</span></div><div class="stp"><span class="on">1 Pedido</span><span>2 Entrega</span><span>3 Pago</span></div>{prow}<div class="tot"><span>Total<small>{e(v["ptot"][1])}</small></span><span>{e(v["ptot"][0])}</span></div><div class="go">Pagar con tarjeta</div><div class="pw">Tienda hecha con KommPro · Pago seguro por Onvo</div></div></div>
<div class="pop"><strong>Pedido pagado</strong>Te llega al panel y al correo, con lo que hay que alistar.</div>
<div class="note glass"><small>Sin salir de tu web</small>Pedido, entrega y pago en tres pasos. La plata va a tu cuenta.</div>
</div>
<div class="r"><p class="eye rv">Cómo funciona</p><h2 id="t-how" class="bg rv">Tres pasos y tu tienda empieza a vender.</h2><div class="steps">{steps}</div></div>
</section>

<section class="s" aria-labelledby="t-cob"><div class="w">
<div class="ctr rv"><p class="eye">Cobro by KommPro</p><h2 id="t-cob" class="bg">¿Ya tenés tienda en línea? Le ponemos el cobro.</h2></div>
<div class="trio">
<div class="nb rv"><b>01</b><h3>Tu tienda sigue igual</h3><p>Seguís con tu WordPress o tu WooCommerce actual. No hay que migrar nada.</p></div>
<div class="nb rv"><b>02</b><h3>El pago, con KommPro</h3><p>Tu cliente paga con tarjeta en una página de pago segura, procesada por Onvo.</p></div>
<div class="nb rv"><b>03</b><h3>La plata a tu cuenta</h3><p>El dinero llega a tu cuenta IBAN y ves cada cobro en tu panel.</p></div>
</div>
</div></section>

<section class="s" aria-labelledby="t-why"><div class="w">
<div class="ctr rv"><p class="eye">Por qué KommPro</p><h2 id="t-why" class="bg">{e(v["why_h"][0])}<br>{e(v["why_h"][1])}</h2></div>
<div class="why">{whyh}</div>
</div></section>

<section class="s" id="precio" aria-labelledby="t-pr"><div class="w">
<div class="pricew">
<div class="rv"><p class="eye">Precio</p><h2 id="t-pr" class="bg">Un plan, todo incluido.</h2><p class="sub">Tienda, inventario sincronizado, cobro con tarjeta, asistente de compra y atención personal. Todo en una sola mensualidad, igual para cualquier tipo de comercio.</p><p class="fine">{e(FINE)}</p><p style="margin-top:18px"><a class="lnk" href="/precio/">Ver precio y calculadora {ic("arrow")}</a></p></div>
{plan_card("Para " + v["chip"].split(" · ")[0][5:])}
</div>
</div></section>

<section class="dark star" style="margin-top:110px" aria-labelledby="t-star"><div class="w">
<div class="top">
<div class="rv"><p class="eye">Inventario sincronizado</p><h2 id="t-star" class="bg">Caja y web con la misma existencia.</h2><p class="sub">Si se vende en el mostrador, se baja en la web. Si se vende en la web, se baja en la caja. Nadie paga por algo que ya no hay.</p></div>
<div class="sync rv" aria-hidden="true"><div class="g">
<div class="node"><div class="nh"><b>{ic("store")}</b>Caja</div><div class="st">24</div><small>{e(v["shop"]["rows"][0][1])}</small></div>
<div class="wire"><i></i><i></i></div>
<div class="node"><div class="nh"><b>{ic("globe")}</b>Tienda en línea</div><div class="st">24</div><small>{e(v["shop"]["rows"][0][1])}</small></div>
</div><div class="log"><span>16:54:40 venta en caja</span><span>web al día en segundos</span></div></div>
</div>
<div class="feats">{feats}</div>
<div class="foot rv"><strong>Una sola cuenta para varias sucursales.</strong> Si tenés más de un local, cada uno con su existencia, todo vive en el mismo panel y pagás una sola mensualidad.</div>
</div></section>
{demos}
{common_bottom(v)}
</main>
'''
    return head(v["title"], v["desc"], f"/{key}/") + header(key) + body + footer() + SCRIPT + "</body>\n</html>\n"

# ---------------------------------------------------------------- precio

def precio():
    incl = [("store","Tienda en línea","Con tu marca, en tu dominio o en tu WordPress actual."),
            ("box","Catálogo ordenado","Limpieza de nombres, fotos sobre fondo blanco y pasillos."),
            ("repeat","Inventario sincronizado","Una sola existencia para tu caja y tu web."),
            ("card","Cobro con tarjeta","Visa, Mastercard y Amex por Onvo, directo a tu IBAN."),
            ("msg","Asistente de compra","Tu cliente escribe lo que necesita y le arma el pedido."),
            ("chart","Tu panel","Pedidos, existencias, clientes y ventas del día en app.kommpro.com."),
            ("file","Factura electrónica","Datos de la empresa y cédula jurídica en el checkout."),
            ("truck","Entrega o retiro","Tu ruta o retiro en tienda. Correos de Costa Rica, próximamente."),
            ("users","Instalación y atención personal","Lo dejamos funcionando y te atiende una persona por chat.")]
    inclh = "".join(f'<div class="c rv"><span class="ic">{ic(i_)}</span><h3>{e(t)}</h3><p>{e(p)}</p></div>' for i_, t, p in incl)
    vl = [("truck","/distribuidores/","Distribuidores y mayoristas","Pedidos de comercios y empresas"),
          ("home","/outlet/","Outlet y hogar","Mercadería que rota cada semana"),
          ("wrench","/ferreterias/","Ferreterías y depósitos","Miles de códigos, por pasillos")]
    vlh = "".join(f'<a href="{h}"><span class="ic">{ic(i_)}</span><span><strong>{e(t)}</strong><small>{e(s)}</small></span>{ic("arrow","i ar")}</a>' for i_, h, t, s in vl)
    faq = [("¿Hay comisión por cada venta?","No. KommPro no cobra comisión por venta. En las ventas pagadas en línea solo pagás el procesamiento de tarjeta de Onvo, a su tarifa estándar."),
           ("¿La mensualidad cambia según el tipo de comercio?","No. Es el mismo plan de $99 + IVA al mes para distribuidores, outlets y ferreterías, con todo incluido."),
           ("¿Qué pasa si me pagan en efectivo o por transferencia en la tienda?","Esas ventas no pasan por Onvo y no tienen ningún costo. Solo el cobro con tarjeta en línea lleva el procesamiento de Onvo."),
           ("¿Tengo varias sucursales?","Todas viven en la misma cuenta, cada una con su existencia, y pagás una sola mensualidad."),
           ("¿Me facturan?","Sí. La mensualidad se factura electrónicamente a tu empresa."),
           ("¿Qué es la retención del 2 %?","Por ley, los pagos con tarjeta llevan una retención del 2 % a cuenta del impuesto sobre la renta. No es un costo: lo rebajás en tu declaración.")]
    faqh = "".join(f'<details class="rv"><summary>{e(q)}<i>+</i></summary><div class="an">{e(a)}</div></details>' for q, a in faq)
    body = f'''<main>
<section class="ph2" aria-labelledby="t-hero">{kbg("")}
<div class="w"><span class="chip rv">Precio</span>
<h1 id="t-hero" class="bg rv">Tienda, inventario y pago en línea. <em>Un solo plan.</em></h1>
<p class="rv">El mismo plan para distribuidores, outlets y ferreterías, con todo incluido. Sin comisión de KommPro por venta.</p></div>
</section>

<section class="pp"><div class="w"><div class="grid">
{plan_card("Para cualquier comercio que ya vende en mostrador")}
<div class="vfor rv"><h3 class="bg">Elegí tu tipo de comercio</h3><p class="m">Mismo precio, misma plataforma. Cada página te muestra cómo se usa en tu negocio.</p><div class="vlist">{vlh}</div><p class="fine">{e(FINE)}</p></div>
</div></div></section>

<section class="s" aria-labelledby="t-incl"><div class="w">
<div class="ctr rv"><p class="eye">Todo incluido</p><h2 id="t-incl" class="bg">Cada plan viene completo.</h2><p class="sub">No hay versión recortada ni extras escondidos. Lo que ves acá lo tenés desde el primer día.</p></div>
<div class="incl">{inclh}</div>
</div></section>

<section class="s" aria-labelledby="t-calc"><div class="w">
<div class="ctr rv"><p class="eye">Calculadora</p><h2 id="t-calc" class="bg">¿Cuánto te queda de cada venta?</h2><p class="sub">Aplica solo a las ventas que tu cliente paga en línea con tarjeta. Si te pagan en efectivo o por transferencia, no hay ningún costo.</p></div>
<div class="calc">
<div class="in rv"><label for="cv">Venta pagada en línea</label><div class="fld">$<input id="cv" type="number" min="0" step="1" value="100" inputmode="decimal"></div>
<div class="two"><div><label for="cr">Onvo %</label><div class="fld"><input id="cr" type="number" min="0" step="0.1" value="3.9">%</div></div><div><label for="cf">Onvo fijo</label><div class="fld">$<input id="cf" type="number" min="0" step="0.05" value="0.35"></div></div></div>
<p class="hint">Precargado con la tarifa estándar de Onvo. Si tu tarifa es otra, cambiala aquí.</p></div>
<div class="out rv" aria-live="polite">
<div class="ln"><span>Paga tu cliente</span><b id="o1">$100.00</b></div>
<div class="ln neg"><span>Procesamiento de tarjeta (Onvo)</span><b id="o2">-$4.25</b></div>
<div class="ln"><span>Comisión de KommPro</span><b>$0.00</b></div>
<div class="ln neg"><span>Retención de renta 2 %**</span><b id="o3">-$2.00</b></div>
<div class="net"><span>Te llega a tu cuenta</span><strong id="o4">$93.75</strong></div>
</div>
</div>
<p class="fine" style="text-align:center">** Por ley, los pagos con tarjeta llevan una retención del 2 % a cuenta del impuesto sobre la renta. No es un costo: lo rebajás en tu declaración.</p>
<div class="medida rv"><div><h3 class="bg">A medida</h3><p>Para proyectos más grandes. Se cotiza por chat y se contrata aparte.</p><div class="pills"><span>Branding</span><span>Sitio nuevo</span><span>Fotografía de producto</span><span>Integraciones especiales</span></div></div><a href="mailto:hola@kommpro.com?subject=Cotizaci%C3%B3n%20a%20medida" class="btn btn-d">Cotizar por chat{ic("arrow","i ar")}</a></div>
</div></section>

<section class="s" aria-labelledby="t-faq"><div class="w">
<div class="ctr rv"><p class="eye">Preguntas</p><h2 id="t-faq" class="bg">Lo que nos preguntan del precio.</h2></div>
<div class="faq">{faqh}</div>
</div></section>

<section class="cta" aria-labelledby="t-cta"><div class="in rv">{kbg("")}
<h2 id="t-cta" class="bg">¿Lo vemos con tus productos?</h2>
<p>En una llamada de 30 minutos te mostramos KommPro con tu catálogo y tus precios.</p>
<div class="ctas"><a href="{DEMO_MAIL}" class="btn btn-m">Solicitar demo{ic("arrow","i ar")}</a></div>
</div></section>
</main>
'''
    calc = '''<script>
(function(){
var v=document.getElementById('cv'),r=document.getElementById('cr'),f=document.getElementById('cf');
function m(x){return (x<0?'-':'')+'$'+Math.abs(x).toFixed(2)}
function go(){var a=+v.value||0,p=a>0?a*(+r.value||0)/100+(+f.value||0):0,t=a*.02;
document.getElementById('o1').textContent=m(a);document.getElementById('o2').textContent=m(-p);document.getElementById('o3').textContent=m(-t);document.getElementById('o4').textContent=m(a-p-t)}
[v,r,f].forEach(function(el){el.addEventListener('input',go)});go();
})();
</script>
'''
    title = "Precio: un solo plan, todo incluido | KommPro"
    desc = "KommPro cuesta $99 + IVA al mes, todo incluido, para distribuidores, outlets y ferreterías. Sin comisión de KommPro por venta."
    return head(title, desc, "/precio/") + header("precio") + body + footer() + SCRIPT + calc + "</body>\n</html>\n"


def main():
    for k in VERT:
        d = ROOT / k
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(vertical(k), encoding="utf-8")
    d = ROOT / "precio"
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(precio(), encoding="utf-8")
    print("ok:", ", ".join(list(VERT) + ["precio"]))

if __name__ == "__main__":
    main()
