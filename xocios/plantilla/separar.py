"""Arma la carpeta ../../xocioslab (sitio propio de Xocios Lab, xocioslab.kommpro.com).

La tienda de Lab se edita en xocioslab/index.html. El panel se edita en xocios/panel/index.html y este script
lo copia con las rutas del otro dominio, junto con data/. Correr después de catalogo.py.
Uso: python3 separar.py
"""
import os, shutil
X = '..'
L = '../../xocioslab'
LICO = 'https://xocios.kommpro.com/'
for d in ['data', 'img', 'panel']:
    os.makedirs(f'{L}/{d}', exist_ok=True)

# La tienda de Lab vive directo en ../../xocioslab/index.html (se edita ahí).

# Panel (misma cuenta de Fabio, abierto en Lab)
s = open(f'{X}/panel/index.html').read()
s = s.replace('const LIMG="../img/", LABIMG="https://xocioslab.kommpro.com/img/", LICO_URL="../index.html", LAB_URL="https://xocioslab.kommpro.com/";',
              f'const LIMG="{LICO}img/", LABIMG="../img/", LICO_URL="{LICO}", LAB_URL="../index.html";')
assert 'LABIMG="../img/"' in s
open(f'{L}/panel/index.html', 'w').write(s)

for f in ['catalogo.js', 'estado.js']:
    shutil.copy(f'{X}/data/{f}', f'{L}/data/{f}')
# Las imágenes de Lab viven solo en xocioslab/img (fotos.py escribe ahí).
print('xocioslab listo')
