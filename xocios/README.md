# Xocios · demo KommPro

Tres páginas, mismo dominio (xocios.kommpro.com):

- `index.html` → **Xocio's Lico Market** (licorera). Aviso de 18+, catálogo real (archivo de PedidosYa 2023, 232 productos con foto), asistente, checkout Onvo en modo prueba con Uber Flash coordinado por Xocios o retiro en Heredia o Tibás.
- `lab/index.html` → **Xocios Lab** (perfumería). Logo de pincel vigente, fotos de @xocios.lab, asesoría de fragancias, Uber Flash, Correos o retiro, y el celular de la tienda (`lab/#panel`) para subir existencia y fotos.
- `panel/index.html` → **Panel de Fabio** en KommPro: una cuenta con dos negocios. Resumen, pedidos, inventario por sede (Heredia y Tibás ligados, transferencias, importar y descargar CSV del POS), existencias de Lab, links de pago y conexiones. `panel/?n=lico` o `panel/?n=lab`.

Las tres comparten `data/catalogo.js` (catálogo) y `data/estado.js` (existencia, pedidos y links). En la demo el estado vive en el navegador: lo que se compra en la tienda entra al panel y lo que se ajusta en el panel sale en la tienda. "Reiniciar demo" en el panel lo deja como al inicio.

Fuentes en `plantilla/`:
- `fotos.py` corta las fotos de `src-ig/` (capturas de Instagram y originales que pasó Mario) hacia `img/`.
- `catalogo.py` arma `data/catalogo.js` desde `catalogo-licorera.json` (productos del archivo de PedidosYa con foto, cortadas de `src-pya/`) y el catálogo de Lab.
- `src-ig/` y `src-pya/` no se suben al repo (pesan); las fotos finales están en `img/`.

Precios: los del archivo de PedidosYa 2023, de referencia. Fabio va a mandar un export nuevo del POS.
