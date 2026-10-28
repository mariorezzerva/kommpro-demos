"""Recorta las fotos de producto en alta (capturas de los links del Excel de PedidosYa, src-pya-hd/)
y les quita el fondo blanco. Escribe ../img/p2/<id>.webp con transparencia.
Uso: python3 recorte.py
"""
from PIL import Image, ImageFilter
import numpy as np, json, glob, re, os
from scipy import ndimage

S = 'src-pya-hd/'
O = '../img/p2/'
os.makedirs(O, exist_ok=True)
cat = json.load(open('catalogo-licorera.json'))
pages = json.load(open(S + 'pages.json'))
shots = sorted(glob.glob(S + 'screenshot-*.png'), key=lambda f: int(re.search(r'-(\d+)\.png$', f).group(1)))
shots = [f for f in shots if int(re.search(r'-(\d+)\.png$', f).group(1)) >= 4]
assert len(shots) == len(pages), (len(shots), len(pages))


def cutout(rgb, gris=False):
    a = rgb.astype(float)
    h, w, _ = a.shape
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    ref = np.median(border, axis=0)
    if ref.min() < 200:
        ref = np.array([255., 255, 255])
    dist = np.sqrt(((a - ref) ** 2).sum(2))
    white = a.min(2) > 238
    cand = (dist < 26) | white
    if gris:  # fondo de estudio gris con degradé
        cand |= ((a.max(2) - a.min(2)) < 14) & (a.min(2) > 150)
    lab, n = ndimage.label(cand)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    fg = ~bg
    # quitar manchas sueltas
    lab2, n2 = ndimage.label(fg)
    if n2 > 1:
        sizes = ndimage.sum(fg, lab2, range(1, n2 + 1))
        keep = np.where(sizes >= sizes.max() * 0.02)[0] + 1
        fg = np.isin(lab2, keep)
    fg = ndimage.binary_fill_holes(fg) | (fg)
    # borde suave: alpha según distancia al fondo en el anillo del contorno
    er = ndimage.binary_erosion(fg, iterations=1)
    ring = fg & ~er
    alpha = fg.astype(float)
    soft = np.clip(dist / 60, 0, 1)
    alpha[ring] = np.maximum(soft[ring], 0.35)
    alpha = ndimage.gaussian_filter(alpha, 0.6) * fg + 0 * alpha
    # descontaminar el blanco del borde
    al = alpha[..., None]
    col = np.where(al > 0.05, (a - ref * (1 - al)) / np.maximum(al, 0.05), a)
    col = np.clip(col, 0, 255)
    out = np.dstack([col, alpha * 255]).astype('uint8')
    im = Image.fromarray(out, 'RGBA')
    bb = im.getbbox()
    return im.crop(bb) if bb else im


GRIS = {'fresca-1-5-litros'}
ONLY = set(__import__('sys').argv[1:])
done = 0
for f, spec in zip(shots, pages):
    typ, ids = spec.split(':')
    ids = [int(x) for x in ids.split(',')]
    im = Image.open(f).convert('RGB')
    W = im.width
    cw = W / 4 if typ == 't' else W / 2
    ch = W / 2
    cols = 4 if typ == 't' else 2
    for n, i in enumerate(ids):
        if ONLY and cat[i]['id'] not in ONLY:
            continue
        x0, y0 = (n % cols) * cw, (n // cols) * ch
        cell = np.asarray(im.crop((round(x0) + 2, round(y0) + 2, round(x0 + cw) - 2, round(y0 + ch) - 2)))
        cut = cutout(cell, cat[i]['id'] in GRIS)
        cut.thumbnail((640, 640), Image.LANCZOS)
        cut.save(O + cat[i]['id'] + '.webp', 'WEBP', quality=86, method=6)
        done += 1
print(done, 'fotos')

# Buchanan's Coconut (no está en el Excel 2023): foto de producto de una tienda, capturada aparte
if not ONLY or 'buchananscoco' in ONLY:
    c = cutout(np.asarray(Image.open(S + 'buchanans-coconut.png').convert('RGB')))
    c.thumbnail((640, 640), Image.LANCZOS)
    c.save(O + 'buchananscoco.webp', 'WEBP', quality=86, method=6)
