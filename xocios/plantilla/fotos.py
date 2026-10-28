"""Prepara las fotos de Xocios a partir de las capturas de Instagram (src-ig/).

Escribe en ../img/ con nombres versionados (Cloudflare guarda imágenes 4 horas).
Uso: python3 fotos.py
"""
from PIL import Image, ImageFilter
import numpy as np
import os

S = 'src-ig/'
O = '../img/'
os.makedirs(O + 'lab', exist_ok=True)


def save(im, name, w=None, q=82):
    if w and im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if name.endswith('.webp'):
        im.save(O + name, 'WEBP', quality=q, method=6)
    else:
        im.convert('RGB').save(O + name, quality=q, optimize=True)
    print(name, im.size, os.path.getsize(O + name) // 1024, 'KB')


def crop(src, box, name, w=None, q=82):
    save(Image.open(S + src).convert('RGB').crop(box), name, w, q)


# Logo Xocio's Lico Market sin el fondo azul (lo nuevo, del rótulo de la tienda)
im = Image.open(S + 'logo-xocios-hd.jpg').convert('RGB')
a = np.asarray(im).astype(float)
bg = np.array([35, 28, 92.0])
d = np.sqrt(((a - bg) ** 2).sum(axis=2))
alpha = np.clip((d - 40) / 70, 0, 1)
# devolver color puro donde hay semitransparencia
rgb = np.clip((a - bg[None, None, :] * (1 - alpha[..., None])) / np.maximum(alpha[..., None], 1e-3), 0, 255)
rgba = np.dstack([rgb, alpha * 255]).astype('uint8')
lg = Image.fromarray(rgba, 'RGBA')
lg = lg.crop(lg.getbbox())
lg.thumbnail((900, 900), Image.LANCZOS)
lg.save(O + 'logo-xocios-lm.webp', 'WEBP', quality=92, method=6)
print('logo-xocios-lm.webp', lg.size)

# Licorera: lo más reciente de @xocios.licorera
crop('lico-rotulo-plaza.png', (40, 330, 819, 1110), 'lico-rotulo-plaza.webp', 760)
crop('lico-refri.png', (0, 0, 819, 1300), 'lico-refri.webp', 700)
crop('lico-casadragones.png', (0, 0, 819, 1340), 'lico-casadragones.webp', 700)
crop('lico-combo.png', (0, 0, 1092, 1092), 'lico-combo.webp', 900)
crop('lico-miedo.png', (0, 0, 980, 1225), 'lico-miedo.webp', 820)
# Buchanan's Coconut del post de Halloween (producto nuevo, no está en el Excel 2023)
crop('lico-miedo.png', (0, 390, 560, 950), 'p/buchanans-coconut.webp', 320)

# Xocios Lab: posts de @xocios.lab
crop('lab-bolsa.png', (0, 300, 819, 1180), 'lab/bolsa.webp', 760)
crop('lab-valentino-donna.png', (240, 330, 840, 1080), 'lab/valentino-donna.webp', 600)
crop('lab-valentino-uomo.png', (248, 445, 848, 1030), 'lab/valentino-uomo.webp', 600)
crop('lab-odyssey.png', (268, 425, 868, 1092), 'lab/odyssey.webp', 600)
crop('lab-yara.png', (238, 165, 838, 880), 'lab/yara.webp', 600)
crop('lab-bharara.png', (246, 215, 846, 830), 'lab/bharara.webp', 600)
crop('lab-goodgirl.png', (505, 230, 1045, 900), 'lab/goodgirl.webp', 640)
crop('lab-versace.png', (430, 230, 1092, 960), 'lab/versace.webp', 660)
crop('lab-regalos.png', (222, 470, 468, 860), 'lab/lightblue.webp')
crop('lab-regalos.png', (466, 470, 642, 860), 'lab/212.webp')
crop('lab-regalos.png', (640, 500, 852, 860), 'lab/chmen.webp')
crop('lab-regalos.png', (836, 450, 1044, 870), 'lab/lemale.webp')
crop('lab-orientica.png', (170, 520, 740, 1300), 'lab/orientica.webp', 600)
crop('lab-bbw-cinderella.png', (150, 170, 810, 1210), 'lab/bbw-cinderella.webp', 600)
crop('lab-bbw-strawberry.png', (140, 380, 730, 1400), 'lab/bbw-strawberry.webp', 600)
crop('lab-goodgirl.png', (0, 0, 1092, 1092), 'lab/goodgirl-post.webp', 900)
crop('lab-versace.png', (0, 0, 1092, 1092), 'lab/versace-post.webp', 900)

# Fotos que ya estaban (cajas de Sauvage, Bleu, Asad, Acqua di Giò y Kaos)
for f in ['p-sauvage', 'p-bleu', 'p-asad', 'p-acqua', 'p-kaos']:
    Image.open('img/' + f + '.webp').save(O + 'lab/' + f[2:] + '.webp', 'WEBP', quality=84)
Image.open('img/lab-hero.jpg').save(O + 'lab/cajas.jpg', quality=84)
Image.open('img/logo-lab.webp').save(O + 'logo-lab.webp', 'WEBP', quality=92)

# Originales en alta que pasó Mario (reemplazan las capturas de esos cinco)
crop('hd-odyssey.png', (330, 460, 900, 1189), 'lab/odyssey.webp', 600)
crop('hd-yara.png', (330, 180, 900, 990), 'lab/yara.webp', 600)
crop('hd-bharara.png', (330, 220, 900, 920), 'lab/bharara.webp', 600)
crop('hd-goodgirl.png', (420, 250, 1160, 1010), 'lab/goodgirl.webp', 680)
crop('hd-versace.png', (470, 240, 1200, 1010), 'lab/versace.webp', 680)
for f in ['odyssey', 'yara', 'bharara', 'goodgirl', 'versace']:
    crop('hd-' + f + '.png', (0, 0) + Image.open(S + 'hd-' + f + '.png').size, 'lab/' + f + '-post.webp', 1000)
# Logo XL de Xocios Lab (del post de Yara), en dorado sobre transparente
im = Image.open(S + 'hd-yara.png').convert('RGB').crop((440, 20, 800, 190))
a = np.asarray(im).astype(float)
lum = a.mean(axis=2)
al = np.clip((lum - 40) / 90, 0, 1)
out = np.dstack([np.full(lum.shape, 214), np.full(lum.shape, 178), np.full(lum.shape, 106), al * 255]).astype('uint8')
lg = Image.fromarray(out, 'RGBA'); lg = lg.crop(lg.getbbox())
lg = lg.resize((lg.width * 2, lg.height * 2), Image.LANCZOS)
lg.save(O + 'logo-xl.webp', 'WEBP', quality=92)
print('logo-xl', lg.size)

# Valentino Donna en alta y el post "Estamos trabajando en algo nuevo" (hero de Lab)
crop('hd-valentino-donna.png', (380, 430, 880, 1120), 'lab/valentino-donna.webp', 560)
crop('hd-valentino-donna.png', (0, 0, 1254, 1254), 'lab/valentino-donna-post.webp', 1000)
crop('hd-algonuevo.png', (0, 0, 720, 900), 'lab/algonuevo.webp', 720, 86)
crop('hd-algonuevo.png', (60, 370, 690, 720), 'lab/vitrina.webp', 720, 88)
# frascos del mismo post para el catálogo
crop('hd-algonuevo.png', (283, 386, 412, 660), 'lab/libre.webp')
crop('hd-algonuevo.png', (196, 474, 316, 670), 'lab/chanel5.webp')
crop('hd-algonuevo.png', (492, 440, 574, 672), 'lab/genifique.webp')
crop('hd-algonuevo.png', (566, 470, 650, 670), 'lab/nightrepair.webp')

# Logo vigente de Xocios Lab: "Xocios" en pincel inclinado + LAB dorado (post "algo nuevo")
im = Image.open(S + 'hd-algonuevo.png').convert('RGB').crop((150, 20, 570, 150))
a = np.asarray(im).astype(float)
lum = a.max(axis=2)
al = np.clip((lum - 95) / 110, 0, 1)
rgb = np.clip(a * 1.08, 0, 255)
lg = Image.fromarray(np.dstack([rgb, al * 255]).astype('uint8'), 'RGBA')
lg = lg.crop(lg.getbbox())
lg = lg.resize((lg.width * 2, lg.height * 2), Image.LANCZOS)
lg.save(O + 'logo-lab-brush.webp', 'WEBP', quality=92)
print('logo-lab-brush', lg.size)
