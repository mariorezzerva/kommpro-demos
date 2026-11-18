# Xocios Lab · demo KommPro

Sitio de la perfumería en **xocioslab.kommpro.com** (proyecto de Cloudflare Pages `xocioslab`, carpeta raíz `xocioslab`). La licorera vive aparte en xocios.kommpro.com (carpeta `../xocios`); las dos son de la misma cuenta de Fabio.

- `index.html` → tienda de Xocios Lab: logo de pincel, asesoría de fragancias, Uber Flash, Correos o retiro, y el celular de la tienda (`#panel`) para subir existencia y fotos. Se edita aquí directo.
- `panel/` y `data/` → copias que genera `../xocios/plantilla/separar.py`. No editarlas aquí: editar en `../xocios/` y correr el script.
- `img/lab3/` → fotos del catálogo con el look del Instagram (morado oscuro y dorado). Las genera `plantilla/vitrina.py`: los productos con post propio usan el post de @xocios.lab (Sauvage, 212 Men Heroes, CH Men, Light Blue, Cinderella, Bharara, Odyssey, Valentino Donna, Yara) y el resto monta la foto oficial (`img/lab2/`) en un set morado con piso brillante. Las capturas de IG no se suben al repo.
- `img/lab/` y `img/lab2/` → fotos anteriores (posts viejos y oficiales en blanco), fuente de `vitrina.py`.

Cuando entre una foto nueva, guardarla con nombre nuevo (Cloudflare guarda en caché 4 h).
