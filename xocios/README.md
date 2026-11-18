# Xocios · demo KommPro

Dos sitios separados, una sola cuenta de Fabio:

- **xocios.kommpro.com** (esta carpeta) → `index.html` es **Xocio's Lico Market** (licorera). Aviso de 18+, catálogo real (archivo de PedidosYa 2023, 232 productos con foto), asistente, checkout Onvo en modo prueba con Uber Flash coordinado por Xocios o retiro en Heredia o Tibás. `/lab` redirige a xocioslab.kommpro.com (`_redirects`).
- **xocioslab.kommpro.com** (carpeta `../xocioslab`) → **Xocios Lab** (perfumería). Ver `../xocioslab/README.md`.
- `panel/index.html` → **Panel de Fabio** en KommPro: una cuenta con dos negocios. Resumen, pedidos, inventario por sede (Heredia y Tibás ligados, transferencias, importar y descargar CSV del POS), existencias de Lab, links de pago y conexiones. `panel/?n=lico` o `panel/?n=lab`.

Los dos sitios usan `data/catalogo.js` (catálogo) y `data/estado.js` (existencia, pedidos y links). El panel va en los dos dominios (en Lab, copia de este con las rutas cambiadas). En la demo el estado vive en el navegador de cada dominio: lo que se compra en la licorera entra al panel de xocios.kommpro.com y lo de Lab al panel de xocioslab.kommpro.com. "Reiniciar demo" en el panel lo deja como al inicio.

Fuentes en `plantilla/`:
- `fotos.py` corta las fotos de `src-ig/` (capturas de Instagram y originales que pasó Mario) hacia `img/`.
- `separar.py` copia el panel y `data/` a `../xocioslab/` (correr después de `catalogo.py` o de editar el panel).
- `catalogo.py` arma `data/catalogo.js` desde `catalogo-licorera.json` (productos del archivo de PedidosYa con foto, cortadas de `src-pya/`) y el catálogo de Lab.
- `src-ig/` y `src-pya/` no se suben al repo (pesan); las fotos finales están en `img/`.

Precios: los del archivo de PedidosYa 2023, de referencia. Fabio va a mandar un export nuevo del POS.
