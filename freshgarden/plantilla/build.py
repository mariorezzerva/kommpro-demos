"""Arma freshgarden/index.html con todas las fotos embebidas.

Uso: python3 build.py  (desde freshgarden/plantilla/)
Toma template.html, logo.png, iso.png y las fotos de img/nav/ (recortes del
catálogo navideño VPC 2026) y escribe ../index.html.
"""
import base64, json, os

def uri(p):
    mime = {'jpg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}[p.rsplit('.', 1)[1]]
    return f"data:{mime};base64," + base64.b64encode(open(p, 'rb').read()).decode()

h = open('template.html').read()
A = {f[:-4]: uri('img/nav/' + f) for f in sorted(os.listdir('img/nav')) if f.endswith('.jpg')}
h = h.replace('{{logo}}', uri('img/logo.png')).replace('{{iso}}', uri('img/iso.png'))
h = h.replace('{{herobox}}', A['herobox'])
h = h.replace('{{ASSETS}}', json.dumps(A))
assert '{{' not in h, 'quedó un marcador sin reemplazar'
open('../index.html', 'w').write(h)
print(len(h) // 1024, 'KB')
