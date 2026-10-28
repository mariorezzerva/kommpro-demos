/* Estado compartido de la demo de Xocios: tiendas, celular de Lab y panel de Fabio.
   En la demo vive en el navegador (localStorage), así lo que se vende en la tienda aparece en el panel
   y lo que se ajusta en el panel sale en la tienda. En producción esto es la base de datos de KommPro,
   sincronizada con el POS de cada sede. */
(function(){
  const X = window.XO = {};
  X.get = (k, d) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } };
  X.set = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  X.ZONES_LICO = [
    ["heredia", "Heredia centro, Barva, San Pablo", 2200, "Heredia"],
    ["sdomingo", "Santo Domingo, San Isidro, Santa Bárbara", 2800, "Heredia"],
    ["alajuela", "Belén, Flores, Alajuela centro", 3900, "Heredia"],
    ["tibas", "Tibás, Moravia, Goicoechea", 2200, "Tibás"],
    ["sanjose", "San José centro, Montes de Oca", 2900, "Tibás"],
    ["escazu", "Escazú, Santa Ana, Curridabat", 4300, "Tibás"]
  ];
  const nowISO = () => new Date().toISOString();

  /* Licorera: existencia por sede [Heredia, Tibás, visible en línea] */
  X.licoStock = () => {
    const ov = X.get("xo-lico-stock", {});
    return Object.fromEntries((window.XO_LICO ? XO_LICO.products : []).map(p => {
      const o = ov[p.id]; return [p.id, o ? { h: o[0], t: o[1], on: o[2] !== false } : { h: p.h, t: p.t, on: true }];
    }));
  };
  X.setLicoStock = (id, h, t, on) => { const ov = X.get("xo-lico-stock", {}); ov[id] = [Math.max(0, h), Math.max(0, t), on !== false]; X.set("xo-lico-stock", ov); };
  X.placeLico = (o) => {
    const st = X.licoStock();
    o.lines.forEach(([id, q]) => {
      const s = st[id]; if (!s) return;
      const first = o.sede === "Heredia" ? "h" : "t", other = first === "h" ? "t" : "h";
      const take = Math.min(q, s[first]); s[first] -= take; s[other] = Math.max(0, s[other] - (q - take));
      X.setLicoStock(id, s.h, s.t, s.on);
    });
    const list = X.get("xo-lico-orders", []);
    o.num = "XO-" + (2310 + list.length); o.time = nowISO(); o.status = o.mode === "uber" ? "Buscando repartidor" : "Alistando";
    list.unshift(o); X.set("xo-lico-orders", list);
    return o;
  };

  /* Xocios Lab: existencia única (vitrina de Heredia) */
  X.labStock = () => { const ov = X.get("xo-lab-stock", {}); return Object.fromEntries((window.XO_LAB ? XO_LAB.products : []).concat(X.get("xo-lab-new", [])).map(p => [p.id, ov[p.id] !== undefined ? ov[p.id] : p.stock])); };
  X.setLabStock = (id, n, who) => {
    const ov = X.get("xo-lab-stock", {}); const prev = X.labStock()[id];
    ov[id] = Math.max(0, n); X.set("xo-lab-stock", ov);
    if (who) X.labLog(`${who}: ${X.labName(id)} ${prev} → ${ov[id]}`);
  };
  X.labName = id => { const p = (XO_LAB.products.concat(X.get("xo-lab-new", []))).find(p => p.id === id); return p ? p.name : id; };
  X.labLog = (txt) => { const l = X.get("xo-lab-log", []); l.unshift({ t: nowISO(), txt }); X.set("xo-lab-log", l.slice(0, 60)); };
  X.placeLab = (o) => {
    const st = X.labStock();
    o.lines.forEach(([id, q]) => X.setLabStock(id, (st[id] || 0) - q));
    const list = X.get("xo-lab-orders", []);
    o.num = "XL-" + (518 + list.length); o.time = nowISO(); o.status = o.mode === "retiro" ? "Alistando" : o.mode === "correos" ? "Por empacar" : "Buscando repartidor";
    list.unshift(o); X.set("xo-lab-orders", list);
    X.labLog(`Venta web ${o.num}: ${o.lines.map(([id, q]) => q + "× " + X.labName(id)).join(", ")}`);
    return o;
  };

  /* Links de pago (sirven para lo que se vende por WhatsApp) */
  X.links = biz => X.get("xo-links-" + biz, []);
  X.addLink = (biz, l) => { const L = X.links(biz); l.code = (biz === "lab" ? "LB" : "LX") + Math.random().toString(36).slice(2, 7).toUpperCase(); l.time = nowISO(); l.status = "Pendiente"; L.unshift(l); X.set("xo-links-" + biz, L); return l; };
  X.reset = () => { ["xo-lico-stock", "xo-lico-orders", "xo-lico-cart", "xo-lab-stock", "xo-lab-orders", "xo-lab-cart", "xo-lab-new", "xo-lab-log", "xo-links-lico", "xo-links-lab"].forEach(k => { try { localStorage.removeItem(k); } catch (e) {} }); };
})();
