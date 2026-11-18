# Xocios Lab · demo KommPro

Sitio de la perfumería en **xocioslab.kommpro.com** (proyecto de Cloudflare Pages `xocioslab`, carpeta raíz `xocioslab`). La licorera vive aparte en xocios.kommpro.com (carpeta `../xocios`); las dos son de la misma cuenta de Fabio.

- `index.html` → tienda de Xocios Lab: logo de pincel, asesoría de fragancias, Uber Flash, Correos o retiro, y el celular de la tienda (`#panel`, "Inventario Lab") para subir existencia y fotos. Se edita aquí directo.
- `panel/` y `data/` → copias que genera `../xocios/plantilla/separar.py`. No editarlas aquí: editar en `../xocios/` y correr el script.
- `img/lab4/` → fotos del catálogo: producto limpio sobre fondo claro sutil, todas con el mismo encuadre. Las genera `plantilla/estudio.py` desde las fotos oficiales sobre blanco (`img/lab2/` y `plantilla/src-of/`, que no se sube al repo). Bath & Body Works usa la foto de la tienda recortada.
- `img/coll/` → foto grande de cada colección: posts de @xocios.lab recortados sin el texto del arte (`plantilla/colecciones.py`).
- `img/lab3/` → versión anterior con el look oscuro del Instagram (`plantilla/vitrina.py`), ya no se usa en el catálogo.
- `img/lab/` y `img/lab2/` → fotos anteriores (posts viejos y oficiales en blanco), fuente de `vitrina.py`.

Cuando entre una foto nueva, guardarla con nombre nuevo (Cloudflare guarda en caché 4 h).
