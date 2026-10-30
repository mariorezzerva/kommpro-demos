"""Arma freshgarden/index.html con todas las fotos embebidas.

Uso: python3 build.py  (desde freshgarden/plantilla/)
Toma template.html, logo.png, iso.png y las fotos de img/nav/ (recortes del
catálogo navideño VPC 2026, sin fondo) y escribe ../index.html.
"""
import base64, json, os

def uri(p):
    mime = {'jpg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}[p.rsplit('.', 1)[1]]
    return f"data:{mime};base64," + base64.b64encode(open(p, 'rb').read()).decode()

h = open('template.html').read()
A = {f[:-5]: uri('img/nav/' + f) for f in sorted(os.listdir('img/nav')) if f.endswith('.webp')}
h = h.replace('{{logo}}', uri('img/logo.png')).replace('{{iso}}', uri('img/iso.png'))
for k in ('caja2', 'uvaverde', 'peradanjou', 'manzroja'):
    h = h.replace('{{%s}}' % k, A[k])
h = h.replace('{{ASSETS}}', json.dumps(A))
assert '{{' not in h, 'quedó un marcador sin reemplazar'
open('../index.html', 'w').write(h)
print(len(h) // 1024, 'KB')
