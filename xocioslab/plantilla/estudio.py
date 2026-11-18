"""Fotos de catálogo de Xocios Lab: producto limpio sobre fondo claro sutil, todas con el mismo encuadre.

Fuentes: fotos oficiales sobre blanco (img/lab2/ y src-of/, esta última no se sube al repo) y,
para Bath & Body Works, la foto de la tienda recortada con rembg.
Salida: img/lab4/<id>.webp (800x1000). Uso: python3 estudio.py
"""
import os, numpy as np
from PIL import Image, ImageFilter, ImageDraw
from scipy.ndimage import label, binary_fill_holes, binary_closing, gaussian_filter
W, H = 1000, 1250
OUT = '../img/lab4'; os.makedirs(OUT, exist_ok=True)
L2 = ['sauvage', 'goodgirl', 'valentino-donna', 'valentino-uomo', 'versace', 'yara', 'bharara', 'odyssey',
      'asad', 'acqua', 'lemale', 'lightblue', 'chmen']
OF = {'bleu': 'bleu_1.png', '212': '212.avif', 'kaos': 'kaos.avif', 'orientica': 'orientica_1.jpg'}
FOTO = {'bbw-strawberry': '../img/lab/bbw-strawberry.webp', 'bbw-cinderella': 'src-of/cinderella.jpg'}

def fondo():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W * .5) / (W * .7)) ** 2 + ((y - H * .42) / (H * .7)) ** 2)
    c0 = np.array([251, 249, 247.]); c1 = np.array([236, 231, 238.])  # marfil al centro, lila muy suave a los bordes
    t = np.clip(d, 0, 1)[..., None] ** 1.4
    return Image.fromarray((c0 * (1 - t) + c1 * t).astype(np.uint8)).convert('RGBA')

def sobre_blanco(im):
    """Recorta el producto de un fondo blanco o gris claro uniforme."""
    if im.mode == 'RGBA' and np.array(im.split()[-1]).min() < 250:
        return im
    rgb = np.array(im.convert('RGB')).astype(int)
    ref = np.median(np.r_[rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]], axis=0)
    claro = (np.abs(rgb - ref).max(axis=2) < 14)
    lab, _ = label(claro); borde = set(np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
    obj = binary_fill_holes(binary_closing(~np.isin(lab, list(borde)), iterations=2))
    a = (gaussian_filter(obj.astype(np.float32), .8) * 255).astype(np.uint8)
    out = im.convert('RGBA'); out.putalpha(Image.fromarray(a)); return out

def con_rembg(im, sess):
    from rembg import remove
    cut = remove(im.convert('RGB'), session=sess, post_process_mask=True)
    a = np.array(cut.split()[-1]); a = np.where(binary_fill_holes(a > 60), np.maximum(a, 255), a).astype(np.uint8); a[a < 20] = 0
    out = im.convert('RGBA'); out.putalpha(Image.fromarray(a)); return out

def montar(cut):
    cut = cut.crop(cut.getbbox())
    s = min(H * .66 / cut.height, W * .72 / cut.width); cut = cut.resize((round(cut.width * s), round(cut.height * s)), Image.LANCZOS)
    bg = fondo(); piso = int(H * .83); x = (W - cut.width) // 2; y = piso - cut.height
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).ellipse((x + cut.width * .06, piso - 10, x + cut.width * .94, piso + 16), fill=95)
    sh = sh.filter(ImageFilter.GaussianBlur(13)); dark = Image.new('RGBA', (W, H), (60, 45, 70, 255)); dark.putalpha(sh); bg.alpha_composite(dark)
    bg.alpha_composite(cut, (x, y))
    return bg.convert('RGB').resize((800, 1000), Image.LANCZOS)

if __name__ == '__main__':
    try: import pillow_avif  # noqa
    except ImportError: pass
    for pid in L2: montar(sobre_blanco(Image.open(f'../img/lab2/{pid}.webp'))).save(f'{OUT}/{pid}.webp', quality=86)
    for pid, f in OF.items(): montar(sobre_blanco(Image.open('src-of/' + f))).save(f'{OUT}/{pid}.webp', quality=86)
    from rembg import new_session
    sess = new_session('isnet-general-use')
    for pid, f in FOTO.items(): montar(con_rembg(Image.open(f), sess)).save(f'{OUT}/{pid}.webp', quality=86)
    print(len(os.listdir(OUT)))
