// Cloudflare Pages Function: proxy de solo lectura a la API publica del widget de Rezzerva.
// Sirve /rz/<tenant>/products/<slug> para que el sitio muestre los precios del panel.
export async function onRequestGet({ params }) {
  const path = [].concat(params.path || []).join("/");
  if (!/^[a-z0-9-]+\/products\/[a-z0-9-]+$/.test(path)) {
    return new Response("Not found", { status: 404 });
  }
  const r = await fetch("https://app.rezzerva.com/v1/widget/" + path, {
    cf: { cacheTtl: 300, cacheEverything: true },
  });
  return new Response(r.body, {
    status: r.status,
    headers: {
      "content-type": r.headers.get("content-type") || "application/json",
      "cache-control": "public, max-age=300",
      "access-control-allow-origin": "*",
    },
  });
}
