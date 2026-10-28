"""Arma las dos tiendas de Xocios con las imágenes embebidas.

licorera.html -> ../index.html      (xocios.kommpro.com)
lab.html      -> ../lab/index.html  (xocios.kommpro.com/lab/)

Uso: python3 build.py  (dentro de xocios/plantilla/)
"""
import base64, json, os, re

def uri(f):
    ext = f.rsplit('.', 1)[1]
    mime = {'webp': 'image/webp', 'jpg': 'image/jpeg', 'png': 'image/png'}[ext]
    return f"data:{mime};base64," + base64.b64encode(open('img/' + f, 'rb').read()).decode()

def build(src, out, slots, assets):
    h = open(src).read()
    for k, f in slots.items():
        h = h.replace('{{%s}}' % k, uri(f))
    h = h.replace('{{ASSETS}}', json.dumps({k: uri(f) for k, f in assets.items()}))
    left = re.findall(r'\{\{\w+\}\}', h)
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    open(out, 'w').write(h)
    print(out, len(h) // 1024, 'KB', 'faltan: ' + ', '.join(left) if left else '')

build('licorera.html', '../index.html',
      {'logo': 'logo-xocios.webp', 'fachada': 'tienda-fachada.jpg', 'combo': 'combo-centenario.webp', 'interior': 'tienda-interior.jpg'},
      {'logo': 'logo-xocios.webp', 'combo': 'combo-centenario.webp'})

lab_photos = {f[2:-5]: f for f in os.listdir('img') if f.startswith('p-')}
if os.path.exists('lab.html'):
    build('lab.html', '../lab/index.html',
          {'logo': 'logo-lab.webp', 'hero': 'lab-hero.jpg', 'circle': 'lab-circle.webp', 'kaos': 'p-kaos.webp'},
          {'logo': 'logo-lab.webp', **lab_photos})
