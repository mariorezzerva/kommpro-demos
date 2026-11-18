"""Fotos de catálogo de Xocios Lab con el look de su Instagram (morado oscuro, luz dorada).

- Productos con post propio en IG: se usa el post (recorte 4:5).  Fuente: carpeta ig/ (no se sube al repo).
- El resto: la foto oficial (img/lab2) se recorta con rembg y se monta en un set morado con piso brillante.
Salida: img/lab3/<id>.webp (800x1000). Uso: python3 vitrina.py [carpeta_ig]
"""
import sys, os, numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
W, H = 1080, 1350
OUT = '../img/lab3'
IG = sys.argv[1] if len(sys.argv) > 1 else 'ig'
os.makedirs(OUT, exist_ok=True)

# id -> (archivo IG, caja de recorte relativa x0,y0,x1,y1 o None)
POSTS = {
    'sauvage': ('Df2T2Raigb2_0.jpg', None),
    '212': ('Df2T2Raigb2_1.jpg', None),
    'chmen': ('DfsAp4HiLU2_0.jpg', None),
    'lightblue': ('DfxKOVijpaO_0.jpg', None),
    'bbw-cinderella': ('DajUhOHDQM6_0.jpg', (0, .06, 1, .94)),
}
OLDPOSTS = {'bharara': 'bharara-post', 'odyssey': 'odyssey-post', 'valentino-donna': 'valentino-donna-post', 'yara': 'yara-post'}
SET = ['bleu', 'goodgirl', 'valentino-uomo', 'versace', 'asad', 'lemale', 'bbw-strawberry']
# Solo la botella (la caja blanca no se recorta bien): parte derecha de la foto oficial
BOTTLE = {'versace': (.5, 0, 1, 1)}
# Sin foto oficial limpia: la foto va enmarcada en dorado, como los posts
FRAME = ['kaos', 'orientica', 'acqua']  # Acqua di Giò: vidrio transparente sobre blanco, se enmarca la foto oficial

def fit45(im, box=None):
    w, h = im.size
    if box: im = im.crop((int(box[0]*w), int(box[1]*h), int(box[2]*w), int(box[3]*h))); w, h = im.size
    tw = min(w, int(h*4/5)); th = int(tw*5/4)
    x = (w-tw)//2; y = max(0, (h-th)//2)
    return im.crop((x, y, x+tw, y+th)).resize((800, 1000), Image.LANCZOS)

def backdrop():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.zeros((H, W, 3), np.float32)
    top = np.array([24, 10, 38]); bot = np.array([8, 4, 14])
    t = (y/H)[..., None]; base[:] = top*(1-t)+bot*t
    # halo violeta detrás del producto
    d = np.sqrt(((x-W*.5)/(W*.55))**2+((y-H*.46)/(H*.42))**2)
    glow = np.clip(1-d, 0, 1)**1.6
    base += glow[..., None]*np.array([95, 40, 130])
    # luz dorada cálida arriba a la derecha
    d2 = np.sqrt(((x-W*.86)/(W*.5))**2+((y-H*.08)/(H*.35))**2)
    base += (np.clip(1-d2, 0, 1)**2)[..., None]*np.array([120, 85, 35])
    # piso: franja inferior un poco más clara y lisa
    floor = np.clip((y-H*.74)/(H*.26), 0, 1)
    base = base*(1-floor[..., None]*.35) + floor[..., None]*np.array([30, 16, 40])*.35
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')

def compose(pid, sess):
    from rembg import remove
    oficial = os.path.exists(f'../img/lab2/{pid}.webp')
    src = Image.open(f'../img/lab2/{pid}.webp' if oficial else f'../img/lab/{pid}.webp').convert('RGB')
    if pid in BOTTLE:
        b = BOTTLE[pid]; w, h = src.size; src = src.crop((int(b[0]*w), int(b[1]*h), int(b[2]*w), int(b[3]*h)))
    cut = remove(src, session=sess, post_process_mask=True)
    a = np.array(cut.split()[-1]); a[a < 18] = 0
    # el vidrio transparente deja huecos: se rellenan para que la botella quede entera
    from scipy.ndimage import binary_fill_holes, binary_closing
    from scipy.ndimage import label, gaussian_filter
    px = np.array(src); white = px.min(axis=2) > 236 if oficial else np.ones(px.shape[:2], bool)
    lab_, _ = label(white); edge = set(np.unique(np.r_[lab_[0], lab_[-1], lab_[:, 0], lab_[:, -1]])) - {0}
    fondo = np.isin(lab_, list(edge))
    solid = binary_fill_holes(binary_closing((a > 40) | ~fondo, iterations=3))
    soft = (gaussian_filter(solid.astype(np.float32), 1.0)*255).astype(np.uint8)
    if oficial: a = np.maximum(a, soft); a[soft < 10] = 0
    cut = src.convert('RGBA')
    cut.putalpha(Image.fromarray(a)); cut = cut.crop(cut.getbbox())
    # un toque más de contraste y cálido
    rgb = ImageEnhance.Contrast(cut.convert('RGB')).enhance(1.06); rgb.putalpha(cut.split()[-1]); cut = rgb
    bg = backdrop()
    maxh, maxw = int(H*.56), int(W*.78)
    s = min(maxh/cut.height, maxw/cut.width); cut = cut.resize((int(cut.width*s), int(cut.height*s)), Image.LANCZOS)
    floor_y = int(H*.80); x = (W-cut.width)//2; y = floor_y-cut.height
    # reflejo en el piso
    ref = cut.transpose(Image.FLIP_TOP_BOTTOM)
    fade = np.linspace(.32, 0, ref.height)[:, None]*np.ones((1, ref.width))
    ra = (np.array(ref.split()[-1]).astype(np.float32)*fade).astype(np.uint8); ref.putalpha(Image.fromarray(ra))
    ref = ref.filter(ImageFilter.GaussianBlur(2)); bg.alpha_composite(ref, (x, floor_y+4))
    # sombra de contacto
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).ellipse((x+cut.width*.08, floor_y-14, x+cut.width*.92, floor_y+18), fill=170)
    sh = sh.filter(ImageFilter.GaussianBlur(14)); dark = Image.new('RGBA', (W, H), (0, 0, 0, 255)); dark.putalpha(sh); bg.alpha_composite(dark)
    # línea dorada del borde del piso
    gl = Image.new('L', (W, H), 0); ImageDraw.Draw(gl).ellipse((W*.12, floor_y-22, W*.88, floor_y+30), outline=120, width=3)
    gl = gl.filter(ImageFilter.GaussianBlur(1.2)); gold = Image.new('RGBA', (W, H), (214, 178, 106, 255)); gold.putalpha(gl)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, floor_y+2, W, H), fill=255); gold.putalpha(Image.fromarray(np.minimum(np.array(gl), np.array(m))))
    bg.alpha_composite(gold)
    bg.alpha_composite(cut, (x, y))
    # viñeta
    yy, xx = np.mgrid[0:H, 0:W]; v = np.sqrt(((xx-W/2)/(W*.75))**2+((yy-H/2)/(H*.75))**2)
    arr = np.array(bg.convert('RGB')).astype(np.float32)*np.clip(1.15-v*.55, .55, 1)[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((800, 1000), Image.LANCZOS)

def framed(pid):
    src = Image.open(f'../img/lab2/{pid}.webp' if os.path.exists(f'../img/lab2/{pid}.webp') else f'../img/lab/{pid}.webp').convert('RGB')
    bg = backdrop()
    fw, fh = int(W*.62), int(H*.56)
    s = max(fw/src.width, fh/src.height); ph = src.resize((int(src.width*s)+1, int(src.height*s)+1), Image.LANCZOS)
    ph = ph.crop(((ph.width-fw)//2, (ph.height-fh)//2, (ph.width-fw)//2+fw, (ph.height-fh)//2+fh))
    m = Image.new('L', (fw, fh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fw-1, fh-1), 34, fill=255)
    x, y = (W-fw)//2, int(H*.18)
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle((x+10, y+30, x+fw-10, y+fh+30), 34, fill=200)
    dark = Image.new('RGBA', (W, H), (0, 0, 0, 255)); dark.putalpha(sh.filter(ImageFilter.GaussianBlur(30))); bg.alpha_composite(dark)
    pr = ph.convert('RGBA'); pr.putalpha(m); bg.alpha_composite(pr, (x, y))
    ImageDraw.Draw(bg).rounded_rectangle((x, y, x+fw-1, y+fh-1), 34, outline=(214, 178, 106, 200), width=3)
    yy, xx = np.mgrid[0:H, 0:W]; v = np.sqrt(((xx-W/2)/(W*.75))**2+((yy-H/2)/(H*.75))**2)
    arr = np.array(bg.convert('RGB')).astype(np.float32)*np.clip(1.15-v*.55, .55, 1)[..., None]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).resize((800, 1000), Image.LANCZOS)

if __name__ == '__main__':
    for pid in FRAME: framed(pid).save(f'{OUT}/{pid}.webp', quality=84)
    for pid, (f, box) in POSTS.items():
        p = os.path.join(IG, f)
        if os.path.exists(p): fit45(Image.open(p).convert('RGB'), box).save(f'{OUT}/{pid}.webp', quality=84)
    for pid, f in OLDPOSTS.items():
        fit45(Image.open(f'../img/lab/{f}.webp').convert('RGB')).save(f'{OUT}/{pid}.webp', quality=84)
    from rembg import new_session
    sess = new_session('isnet-general-use')
    for pid in SET:
        compose(pid, sess).save(f'{OUT}/{pid}.webp', quality=84); print(pid)
