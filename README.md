# KommPro · demos

Cada carpeta es un sitio estático. Desde el 26 oct se publican en **Cloudflare Pages** (Netlify quedó sin créditos y no publica cambios nuevos). Cada proyecto de Pages se enlaza a este repo, rama `main`, con su carpeta como root directory y sin comando de build. Cada push a `main` se publica solo.

| Carpeta | Sitio | Proyecto (Cloudflare Pages) |
|---|---|---|
| sabo | sabo.kommpro.com | saboenlinea |
| lacruz | lacruz.kommpro.com | distribuidoralacruz |
| kommpro | kommpro.com | kommpro |
| activearenal | activearenal-demo.pages.dev (demo Rezzerva · tour operadores) | activearenal-demo |

`activearenal/` se genera con `activearenal/plantilla/build.py` (datos en `data.json`). Para cambiar textos o tours: editar `data_base.json` o `make_data.py`, correr `python3 make_data.py && python3 build.py` dentro de `plantilla/` y hacer commit de todo. `activearenal/wp/` trae los bloques para pegar en Elementor.

Precios en vivo: al cargar, el sitio lee los precios de Rezzerva por `/rz/<tenant>/products/<slug>`, que atiende la Pages Function `activearenal/functions/rz/[[path]].js` (solo esa ruta, cache de 5 min). La genera `build.py`. Si Rezzerva no responde, quedan los precios de `data.json`. Los bloques de WordPress consultan Rezzerva directo y necesitan CORS habilitado en las rutas GET de `/v1/widget/` para actualizarse.

Demos de clientes de Rezzerva: en `<cliente>.rezzerva.com`. Demos de KommPro: en `<cliente>.kommpro.com`.
