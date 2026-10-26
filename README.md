# KommPro · demos

Cada carpeta es un sitio estático publicado en Netlify. Cada proyecto de Netlify apunta a su carpeta como base, sin comando de build.

| Carpeta | Sitio | Proyecto Netlify |
|---|---|---|
| sabo | sabo.kommpro.com | saboenlinea |
| lacruz | lacruz.kommpro.com | distribuidoralacruz |
| kommpro | kommpro.com | kommpro |
| activearenal | pendiente (demo Rezzerva · tour operadores) | pendiente de crear |

`activearenal/` se genera con `activearenal/plantilla/build.py` (datos en `data.json`). Para cambiar textos o tours: editar `data_base.json` o `make_data.py`, correr `python3 make_data.py && python3 build.py` dentro de `plantilla/` y hacer commit de todo. `activearenal/wp/` trae los bloques para pegar en Elementor.
