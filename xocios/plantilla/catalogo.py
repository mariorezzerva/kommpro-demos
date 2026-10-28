"""Arma ../data/catalogo.js: el catálogo de las dos tiendas, que leen la licorera, Xocios Lab y el panel.

Licorera: productos del archivo de PedidosYa 2023 (pedidosya-2023.json) que tienen foto
(catalogo-licorera.json, generado al cortar las fotos). Precios de ese archivo; el export nuevo
del POS de Fabio los reemplaza.
Uso: python3 catalogo.py
"""
import json, re, random, unicodedata, os

random.seed(7)
src = json.load(open('catalogo-licorera.json'))


def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')


SMALL = {'de', 'con', 'y', 'en', 'sin', 'por', 'a'}
KEEP = {'ii': 'II', 'jw': 'JW', 'vs': 'V.S.', 'v.s.': 'V.S.', 'j': 'J', 'b': 'B', 'h2oh': 'H2OH', 'n7': 'Nº 7', 'pro': 'Pro',
        'bbq': 'BBQ', 'act': 'Act'}


def pretty(name):
    n = name.strip()
    n = re.sub(r'\bL\s+(\d+)\s*ML\b', r'\1 ml', n, flags=re.I)
    n = re.sub(r'\bB\s+(\d+)\s*ML\b', r'\1 ml', n, flags=re.I)
    n = n.replace('´', "'").replace('BUCHANAN S', "BUCHANAN'S").replace('Buchanans', "Buchanan's")
    n = re.sub(r'(\d)\s*(ml|ML|Ml)\b', r'\1 ml', n)
    n = re.sub(r'(\d)\s*(g|G|GRS|gr)\b', r'\1 g', n)
    n = re.sub(r'(\d+(?:[.,]\d+)?)\s*(LITROS|LITRO|Litros|Litro|L)\b', lambda m: m.group(1).replace('.', ',') + ' L', n)
    n = re.sub(r'\b1000 ml\b', '1 L', n)
    n = re.sub(r'\b980 ml\b', '980 ml', n)
    words = []
    for w in n.split():
        lw = w.lower()
        if lw in KEEP:
            words.append(KEEP[lw])
        elif re.match(r'^[\d.,]+$', w) or lw in ('ml', 'g', 'l'):
            words.append(w if lw != 'l' else 'L')
        elif lw in SMALL and words:
            words.append(lw)
        else:
            words.append(lw[:1].upper() + lw[1:])
    n = ' '.join(words)
    fixes = {"Buchanan's": "Buchanan's", 'Jose Cuervo': 'José Cuervo', 'Bacardí': 'Bacardí', 'Cañ': 'Cañ', 'Tonica': 'Tónica',
             'Limon': 'Limón', 'Jalapena': 'Jalapeña', 'Jalapenos': 'Jalapeños', 'Mani ': 'Maní ', 'Garapinado': 'Garapiñado',
             'Sandia': 'Sandía', 'Maracuya': 'Maracuyá', 'Piña': 'Piña', 'Azucar': 'Azúcar', 'Añejo': 'Añejo', 'Daniels': "Daniel's",
             'Stela ': 'Stella ', 'Courvoiser': 'Courvoisier', 'Cuba Libre': 'Cuba Libre', 'Four Loco': 'Four Loko', 'Antioqueño': 'Antioqueño',
             'Sminorff': 'Smirnoff', 'Canada Dry Gin': 'Canada Dry Ginger Ale', 'Ligth': 'Light', 'Gengibre': 'Jengibre', 'Toña': 'Toña', '2.5.l': '2,5 L', 'Lima Limón': 'Lima limón',
             'Six Pack': 'six pack', 'Lata': 'lata', 'Botella': 'botella', 'Cerveza ': '', 'Whisky ': '', 'Ron ': 'Ron ', 'Licor Cacique': 'Guaro Cacique', 'J y B': 'J&B', 'Very Especial': 'Very Special', 'Coca Cola': 'Coca-Cola', 'Black And White': 'Black & White', ' Años': ' años', '20cl': '200 ml', '2.5kg': '2,5 kg', 'Hielo Alaska': 'Hielo Alaska'}
    for a, b in fixes.items():
        n = n.replace(a, b)
    n = re.sub(r'(\d)\.(\d)\s?kg', r'\1,\2 kg', n, flags=re.I)
    n = re.sub(r'(\d)kg', r'\1 kg', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n[:1].upper() + n[1:]


def split_pres(n):
    m = re.search(r'(\s(six pack|lata|botella|retornable)?\s*[\d.,]+\s?(ml|g|L|kg)(\s.*)?)$', n, flags=re.I)
    m2 = re.search(r'\s((six pack )?(lata |botella )?[\d.,]+\s?(ml|g|L|kg|cl|G))(\b|$).*$', n, flags=re.I)
    if m2:
        return n[:m2.start()].strip(), n[m2.start():].strip()
    return n, ''


def cat_of(sec, name):
    t = norm(name)
    if sec == 'CERVEZAS':
        return 'listos' if 'sangria' in t else 'cervezas'
    if sec == 'BEBIDAS ALCOHOLICAS':
        return 'listos'
    if sec in ('GASEOSAS', 'AGUA', 'ENERGIZANTES'):
        return 'mezcladores'
    if sec in ('SNACKS', 'SEMILLAS'):
        return 'bocas'
    if 'tequila' in t:
        return 'tequila'
    if 'vodka' in t or 'ginebra' in t:
        return 'vodka-gin'
    if 'whisky' in t or 'cognac' in t:
        return 'whisky'
    if 'ron ' in t or t.startswith('ron') or 'malibu' in t:
        return 'rones'
    return 'guaro'


ALIAS = [
    ('imperial', 'CERVEZA IMPERIAL LATA 350ML'), ('silver6', 'CERVEZA IMPERIAL SILVER SIX PACK'), ('ultra6', 'CERVEZA IMPERIAL ULTRA SIX PACK'),
    ('light6', 'CERVEZA IMPERIAL LIGHT SIX PACK'), ('pilsen6', 'CERVEZA PILSEN SIX PACK LATA 350ML'), ('pilsen', 'CERVEZA PILSEN LATA 350ML'),
    ('silver', 'CERVEZA SILVER LATA 350ML'), ('bavaria', 'Bavaria Gold 350ml'), ('corona', 'Corona Cerveza 355ml'), ('heineken', 'Heineken Botella 330ml'),
    ('modelo', 'Cerveza Modelo 355ml'), ('stella', 'CERVEZA STELLA ARTOIS BOTELLA 330ML'),
    ('centenario4', 'RON CENTENARIO 4 AÑOS ORO'), ('centenario7', 'RON CENTENARIO 7 AÑOS'), ('flor4', 'RON FLOR DE CAÑA 4'),
    ('bacardi', 'RON BACARDÍ CARTA BLANCA'), ('zacapa', 'RON ZACAPA 23'), ('malibu', 'RON MALIBÚ'),
    ('buchanans12', 'WHISKY BUCHANAN´S 12 AÑOS L 1000 ML'), ('buchanans18', 'WHISKY BUCHANAN´S 18'), ('jwblack', 'WHISKY JOHNNIE WALKER BLACK LABEL'),
    ('jwred', 'Whisky Johnnie Walker Red Label'), ('chivas12', 'WHISKY CHIVAS REGAL 12 AÑOS'), ('oldparr12', 'WHISKY OLD PARR 12'),
    ('jack7', 'WHISKY JACK DANIELS N7'), ('jackhoney', 'WHISKY JACK DANIELS HONEY'), ('hennessy', 'COGNAC HENNESSY'),
    ('cuervo', 'TEQUILA JOSE CUERVO GOLD'), ('cuervoplata', 'TEQUILA JOSE CUERVO SILVER'), ('t1800', 'TEQUILA 1800 REPOSADO'), ('t1800a', 'TEQUILA 1800 AÑEJO'),
    ('smirnoff', 'VODKA SMIRNOFF L'), ('absolut', 'VODKA ABSOLUT'), ('tanqueray', 'GINEBRA TANQUERAY'),
    ('cacique', 'LICOR CACIQUE L 1000 ML'), ('cacique365', 'Guaro Cacique 365ml'), ('baileys', 'CREMA BAILEYS'), ('amarula', 'CREMA AMARULA'),
    ('coca15', 'COCA COLA 1.5 LITROS'), ('coca3', 'COCA COLA 3 LITROS'), ('fresca15', 'FRESCA 1.5 LITROS'), ('fresca3', 'FRESCA TORONJA 3 LITROS'), ('ginger15', 'CANADA DRY GIN 1.5 LITROS'),
    ('soda', 'CANADA DRY CLUB SODA'), ('tonica', 'Agua Tonica 354ml'), ('hielo', 'Hielo Alaska'), ('maxenergy', 'MAX ENERGY 350ML'),
    ('pringles', 'PRINGLES ORIGINAL 40G'), ('mani', 'PRO MANI SALADO 80G'), ('quesitos', 'QUESITOS DIANA'), ('papiolas', 'PAPIOLAS SALADAS CLASICAS 180G'),
    ('picaronas', 'PICARONAS QUESO NACHO 150G'), ('semillas', 'PRO SEMILLAS MIXTAS'),
]
alias_of = {}
for a, key in ALIAS:
    hit = [p for p in src if p['name'].upper().startswith(key.upper()) or p['name'].upper() == key.upper()]
    if not hit:
        hit = [p for p in src if key.upper() in p['name'].upper()]
    if not hit:
        print('ALIAS SIN PRODUCTO', a, key)
        continue
    alias_of[hit[0]['name']] = a

P = []
for p in src:
    pn = pretty(p['name'])
    nm, pres = split_pres(pn)
    if not pres:
        pres = 'Unidad'
    if re.match(r'^[\d.,]+\s?L$', pres): pres = 'Botella ' + pres
    elif re.match(r'^[\d.,]+\s?ml$', pres) and cat_of(p['sec'], p['name']) not in ('cervezas','listos','mezcladores'): pres = 'Botella ' + pres
    elif re.match(r'^[\d.,]+\s?g$', pres): pres = 'Bolsa ' + pres
    pres = pres[:1].upper() + pres[1:]
    cat = cat_of(p['sec'], p['name'])
    tot = random.choice([6, 8, 10, 12, 14, 18, 22, 26, 30, 36, 48]) if cat != 'whisky' else random.choice([3, 4, 5, 6, 8, 10, 12])
    h = max(0, round(tot * random.uniform(.4, .65)))
    P.append(dict(id=alias_of.get(p['name'], p['id']), name=nm, pres=pres, price=p['price'], cat=cat, img='p2/' + p['id'] + '.webp',
                  barcode=p['barcode'], h=h, t=max(0, tot - h)))

ids = {p['id'] for p in P}
by = {p['id']: p for p in P}
# Productos nuevos que no están en el Excel 2023 (salen del Instagram reciente)
P.append(dict(id='buchananscoco', name="Buchanan's Coconut", pres='Botella 750 ml', price=22900, cat='whisky', img='p2/buchananscoco.webp',
              barcode='', h=6, t=4, tag='Nuevo'))
by = {p['id']: p for p in P}

# Combos: imagen compuesta con las fotos recortadas (fondo transparente)
# (id, nombre, presentación, precio, [(producto, cantidad)], temporada o None)
COMBOS = [
    ('combo-centenario', 'Combo Ron Centenario + Coca-Cola 1,5 L', 'Ron 1 L + Coca-Cola 1,5 L', 12000, [('centenario4', 1), ('coca15', 1)], None),
    ('combo-mejenga', 'Combo mejenga', '2 six pack Pilsen + hielo', 13900, [('pilsen6', 2), ('hielo', 1)], None),
    ('combo-guaro', 'Guaro con Fresca', 'Cacique 1 L + Fresca 3 L', 10200, [('cacique', 1), ('fresca3', 1)], None),
    ('combo-buchanans', "Buchanan's con soda", "Buchanan's 12 años 1 L + 2 club soda + hielo", 37500, [('buchanans12', 1), ('soda', 2), ('hielo', 1)], None),
    # Halloween
    ('combo-coco-highball', 'Coco Highball', "Buchanan's Coconut + 2 Ginger Ale 1,5 L + hielo", 25900, [('buchananscoco', 1), ('ginger15', 2), ('hielo', 1)], 'halloween'),
    ('combo-pocima', 'Pócima roja', "Cacique Liga'o Sandía + Fresca 3 L + hielo", 11900, [('cacique-ligao-sandia-1-litro', 1), ('fresca3', 1), ('hielo', 1)], 'halloween'),
    ('combo-disfraces', 'Fiesta de disfraces', '3 six pack Imperial Silver + Fireball + 2 hielos', 42900, [('whisky-fireball-l-1000-ml', 1), ('silver6', 3), ('hielo', 2)], 'halloween'),
    # Xocios Black Month
    ('combo-black-label', 'Black Label con soda', 'Johnnie Walker Black 1 L + 2 club soda + hielo', 27900, [('jwblack', 1), ('soda', 2), ('hielo', 1)], 'black'),
    ('combo-noche-negra', 'Noche negra', '6 Modelo Negra + 6 Pilsen 6.0', 12900, [('cerveza-modelo-negra-botella-355ml', 6), ('cerveza-pilsen-6-0-lata-350ml', 6)], 'black'),
    ('combo-duo-black', 'Dúo Black Friday', 'JW Double Black + Ron Zacapa 23', 62900, [('whisky-johnnie-walker-double-black-l-1000-ml', 1), ('zacapa', 1)], 'black'),
    # Navidad
    ('combo-cena-24', 'Cena del 24', 'Centenario 7 años + 2 Coca-Cola 3 L + hielo', 19900, [('centenario7', 1), ('coca3', 2), ('hielo', 1)], 'navidad'),
    ('combo-rompope', 'Rompope y sobremesa', 'Baileys + Amarula, de litro', 29500, [('baileys', 1), ('amarula', 1)], 'navidad'),
    ('combo-brindis-31', 'Brindis del 31', "Buchanan's 18 años + 2 club soda + hielo", 59900, [('buchanans18', 1), ('soda', 2), ('hielo', 1)], 'navidad'),
    # Verano
    ('combo-hielera', 'Hielera playera', '2 six pack Silver + 2 six pack Ultra + 2 hielos', 25900, [('silver6', 2), ('ultra6', 2), ('hielo', 2)], 'verano'),
    ('combo-piscina', 'Tarde de piscina', '6 Adán & Eva + 6 Bamboo Piña Colada + hielo', 15900, [('adan-eva-maracuya-pina-355ml', 3), ('bamboo-pina-colada-350ml', 6), ('adan-eva-coco-limon-355ml', 3), ('hielo', 1)], 'verano'),
    ('combo-malibu', 'Malibú con Fresca', 'Ron Malibú 1 L + Fresca 3 L + hielo', 19900, [('malibu', 1), ('fresca3', 1), ('hielo', 1)], 'verano'),
    # Parejas
    ('combo-peli', 'Noche de peli', 'Amarula + 2 palomitas Act II', 16900, [('amarula', 1), ('palomitas-act-ii-caramelo-161-4g', 1), ('palomitas-act-ii-queso-cheddar-96g', 1)], 'parejas'),
    ('combo-brindis-14', 'Brindis del 14', '4 Sangría Estiu + 2 Pringles', 9500, [('sangria-estiu-botella-330ml', 4), ('pringles', 2)], 'parejas'),
    ('combo-para-dos', 'Para dos, del bueno', 'Tequila 1800 Añejo + Fresca 1,5 L + hielo', 22500, [('t1800a', 1), ('fresca15', 1), ('hielo', 1)], 'parejas'),
]
from PIL import Image


def rel_h(p):
    """Alto relativo aproximado para que una lata no salga del tamaño de una botella de litro."""
    pr = (p['pres'] + ' ' + p['name']).lower()
    if p['id'] == 'hielo': return .5
    if 'six pack' in pr: return .42
    if p['cat'] == 'bocas': return .5 if 'pringles' not in pr else .4
    if re.search(r'\b3 l|2,5 l|2 l', pr): return .9
    if '1,5 l' in pr: return .82
    if p['cat'] in ('cervezas', 'listos', 'mezcladores'): return .6 if 'botella' in pr else .44
    return 1.0


def compose(ids):
    """Productos en fila sobre la misma base, encimados; el primero al centro y adelante."""
    H0 = 620
    ims = []
    for i in ids[:4]:
        im = Image.open('../img/' + by[i]['img']).convert('RGBA')
        h = H0 * rel_h(by[i])
        s = min(h / im.height, (H0 * (.42 if by[i]['cat'] == 'bocas' else .9)) / im.width)
        ims.append(im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS))
    # orden de izquierda a derecha: los de atrás a los lados del principal
    hero, rest = ims[0], ims[1:]
    left = rest[0::2][::-1]
    right = rest[1::2]
    row = left + [hero] + right
    ov = .2
    xs, x = [], 0
    for k, im in enumerate(row):
        if k: x -= round(min(im.width, row[k - 1].width) * ov)
        xs.append(x); x += im.width
    W = x; H = max(im.height for im in row)
    can = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    hi = len(left)
    order = sorted(range(len(row)), key=lambda k: -abs(k - hi))  # de afuera hacia adentro
    for k in order:
        can.alpha_composite(row[k], (xs[k], H - row[k].height))
    return can


for cid, name, pres, price, items, season in COMBOS:
    miss = [i for i, _ in items if i not in by]
    assert not miss, (cid, miss)
    img = 'p2/' + cid + '.webp'
    order = [i for i, _ in items if i != 'hielo'] + (['hielo'] if any(i == 'hielo' for i, _ in items) else [])
    compose(order).save('../img/' + img, 'WEBP', quality=86, method=6)
    full = sum(by[i]['price'] * q for i, q in items)
    d = dict(id=cid, name=name, pres=pres, price=price, cat='combos', img=img, barcode='', h=random.randint(6, 14), t=random.randint(5, 12),
             items=items, tag='Combo', was=full)
    if season:
        d['season'] = season
    P.insert(0, d)

CATS = [
    dict(id='combos', name='Combos', note='Armados para compartir y pagar menos'),
    dict(id='cervezas', name='Cervezas', note='Nacionales e importadas, bien frías'),
    dict(id='rones', name='Rones', note='Centenario, Flor de Caña, Zacapa'),
    dict(id='whisky', name='Whisky y coñac', note="Buchanan's, Johnnie Walker, Old Parr"),
    dict(id='tequila', name='Tequila', note='José Cuervo, 1800, Jarana'),
    dict(id='vodka-gin', name='Vodka y ginebra', note='Smirnoff, Absolut, Tanqueray'),
    dict(id='guaro', name='Guaro y cremas', note='Cacique, Baileys, Amarula'),
    dict(id='listos', name='Listos para tomar', note='Bamboo, Adán & Eva, Four Loko, Smirnoff Ice'),
    dict(id='mezcladores', name='Mezcladores y hielo', note='Coca-Cola, Fresca, soda, energizantes y hielo'),
    dict(id='bocas', name='Bocas', note='Papas, maní y algo para picar'),
]
for c in CATS:
    c['count'] = sum(1 for p in P if p['cat'] == c['id'])
    rep = {'combos': 'combo-centenario', 'cervezas': 'imperial', 'rones': 'centenario4', 'whisky': 'buchanans12', 'tequila': 'cuervo',
           'vodka-gin': 'tanqueray', 'guaro': 'cacique', 'listos': next(p['id'] for p in P if p['cat'] == 'listos'), 'mezcladores': 'coca15',
           'bocas': 'pringles'}[c['id']]
    c['img'] = next(p['img'] for p in P if p['id'] == rep)

LAB = [
    # id, nombre, marca, ml, para, familias, precio, existencia, historia, foto
    ('sauvage', 'Sauvage Parfum', 'Dior', '100 ml', 'm', ['fresco', 'intenso'], 98000, 6, 'Bergamota de Calabria y maderas suaves. Fresco de día, profundo de noche.', 'lab/sauvage.webp'),
    ('bleu', 'Bleu de Chanel Parfum', 'Chanel', '100 ml', 'm', ['fresco', 'intenso'], 115000, 4, 'Cítricos, cedro y sándalo. Elegante sin hacer ruido.', 'lab/bleu.webp'),
    ('goodgirl', 'Good Girl Eau de Parfum', 'Carolina Herrera', '80 ml', 'f', ['dulce', 'intenso'], 92000, 6, 'Tuberosa, cacao y haba tonka. El tacón que nunca pasa de moda.', 'lab/goodgirl.webp'),
    ('valentino-donna', 'Born in Roma Donna', 'Valentino', '100 ml', 'f', ['dulce'], 98000, 5, 'Jazmín y vainilla bourbon. Dulce, moderno y muy de ella.', 'lab/valentino-donna.webp'),
    ('valentino-uomo', 'Uomo Born in Roma Intense', 'Valentino', '100 ml', 'm', ['dulce', 'intenso'], 89000, 5, 'Vainilla y lavanda. Seductor, para salir de noche.', 'lab/valentino-uomo.webp'),
    ('versace', 'Man Eau Fraîche', 'Versace', '100 ml', 'm', ['fresco'], 52000, 9, 'Limón, cedro y notas acuáticas. Limpio para el calor.', 'lab/versace.webp'),
    ('yara', 'Yara Candy', 'Lattafa', '100 ml', 'f', ['dulce', 'arabe'], 25900, 12, 'Frutal y avainillado. Una golosina elegante.', 'lab/yara.webp'),
    ('bharara', 'Bharara King', 'Bharara', '100 ml', 'm', ['fresco', 'intenso', 'arabe'], 49900, 8, 'Cítricos y almizcle. Poder, elegancia y presencia.', 'lab/bharara.webp'),
    ('odyssey', 'Odyssey Mandarin Sky', 'Armaf', '100 ml', 'm', ['fresco', 'dulce', 'arabe'], 29900, 11, 'Mandarina caramelizada y ámbar. Alegre y llamativo.', 'lab/odyssey.webp'),
    ('orientica', 'Amber Rouge', 'Orientica', '80 ml', 'u', ['intenso', 'arabe', 'dulce'], 36900, 6, 'Azafrán y ámbar. Unisex, para dejar estela a donde vayás.', 'lab/orientica.webp'),
    ('asad', 'Asad Eau de Parfum', 'Lattafa', '100 ml', 'm', ['intenso', 'arabe'], 24900, 14, 'Pimienta negra, tabaco y vainilla. Mucha presencia por poca plata.', 'lab/asad.webp'),
    ('acqua', 'Acqua di Giò Eau de Parfum', 'Giorgio Armani', '75 ml', 'm', ['fresco'], 72000, 7, 'Notas marinas y bergamota. El de la playa y la oficina.', 'lab/acqua.webp'),
    ('lemale', 'Le Male', 'Jean Paul Gaultier', '125 ml', 'm', ['dulce', 'intenso'], 78000, 4, 'Lavanda, menta y vainilla. Un clásico que se reconoce de lejos.', 'lab/lemale.webp'),
    ('lightblue', 'Light Blue Pour Homme', 'Dolce & Gabbana', '125 ml', 'm', ['fresco'], 54000, 8, 'Pomelo, enebro y almizcle. Mediterráneo y fresco.', 'lab/lightblue.webp'),
    ('212', '212 Men', 'Carolina Herrera', '100 ml', 'm', ['fresco'], 56000, 6, 'Cítrico y especiado. Urbano y limpio.', 'lab/212.webp'),
    ('chmen', 'CH Men', 'Carolina Herrera', '100 ml', 'm', ['intenso'], 62000, 5, 'Cuero y maderas. Elegancia de noche.', 'lab/chmen.webp'),
    ('kaos', 'Kaos', 'Tous', '90 ml', 'f', ['dulce', 'fresco'], 45000, 7, 'Frutal y floral. Divertido, para el día a día.', 'lab/kaos.webp'),
    ('bbw-cinderella', 'Cinderella: crema y bruma', 'Bath & Body Works', '226 g + 236 ml', 'f', ['dulce', 'cuidado'], 32000, 5, 'Body cream y fine fragrance mist de la colección Disney Princess.', 'lab/bbw-cinderella.webp'),
    ('bbw-strawberry', 'Strawberry Pound Cake: bruma y loción', 'Bath & Body Works', '236 ml + 236 ml', 'f', ['dulce', 'cuidado'], 29000, 6, 'Para oler a pastelito de fresa todo el día.', 'lab/bbw-strawberry.webp'),
]
LABP = [dict(id=r[0], name=r[1], brand=r[2], ml=r[3], g=r[4], fam=r[5], price=r[6], stock=r[7], story=r[8], img=r[9]) for r in LAB]

os.makedirs('../data', exist_ok=True)
with open('../data/catalogo.js', 'w') as f:
    f.write('/* Catálogo de demo de Xocios. Licorera: archivo PedidosYa 2023 (precios de referencia). Lab: posts de @xocios.lab. */\n')
    f.write('window.XO_LICO=' + json.dumps({'cats': CATS, 'products': P}, ensure_ascii=False, separators=(',', ':')) + ';\n')
    f.write('window.XO_LAB=' + json.dumps({'products': LABP}, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(len(P), 'productos licorera,', len(LABP), 'Lab;', os.path.getsize('../data/catalogo.js') // 1024, 'KB')
for c in CATS:
    print(c['id'], c['count'])
