"""Fotos de las colecciones de Xocios Lab: los posts de @xocios.lab recortados sin el texto del arte.
Fuente: capturas de Instagram en la carpeta que se pase como argumento (no se suben al repo) e img/lab/*-post.webp.
Salida: img/coll/<colección>.webp (5:4). Uso: python3 colecciones.py <carpeta_ig>
"""
import sys, os
from PIL import Image, ImageEnhance
IG = sys.argv[1] if len(sys.argv) > 1 else 'ig'
OUT = '../img/coll'; os.makedirs(OUT, exist_ok=True)
# colección -> (archivo, zona sin texto x0,y0,x1,y1 en fracciones, centro vertical preferido)
C = {
    'noche':   (f'{IG}/Df2T2Raigb2_0.jpg', (0, .262, 1, .83)),
    'dia':     (f'{IG}/DfxKOVijpaO_0.jpg', (0, .37, 1, 1)),
    'el':      (f'{IG}/DfsAp4HiLU2_0.jpg', (0, .19, 1, .75)),
    'cuidado': (f'{IG}/DajUhOHDQM6_0.jpg', (0, .18, 1, .92)),
    'ella':    ('../img/lab/valentino-donna-post.webp', (.12, .30, .88, .74)),
    'arabe':   ('../img/lab/bharara-post.webp', (.14, .175, .86, .62)),
}
for k, (f, (x0, y0, x1, y1)) in C.items():
    im = Image.open(f).convert('RGB'); w, h = im.size
    bx0, by0, bx1, by1 = x0 * w, y0 * h, x1 * w, y1 * h
    bw, bh = bx1 - bx0, by1 - by0
    if bw / bh > 5 / 4:  # demasiado ancho: recortar a los lados
        nw = bh * 5 / 4; cx = (bx0 + bx1) / 2; bx0, bx1 = cx - nw / 2, cx + nw / 2
    else:                # demasiado alto: recortar arriba y abajo
        nh = bw * 4 / 5; cy = (by0 + by1) / 2; by0, by1 = cy - nh / 2, cy + nh / 2
    out = im.crop((round(bx0), round(by0), round(bx1), round(by1))).resize((1200, 960), Image.LANCZOS)
    out = ImageEnhance.Sharpness(out).enhance(1.15)
    out.save(f'{OUT}/{k}.webp', quality=84); print(k, round(bx1 - bx0), 'px de ancho de origen')
