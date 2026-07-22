/* ============================================================
   Con Interés · ficha.js
   Motor de las FICHAS DE INDICADOR (/indicador/*.html):
   historial completo con eventos anotados (enlazados a notas
   propias), selector de rango, estadísticas, descarga CSV y
   notas relacionadas. Lee el indicador de <body data-key="...">.
   ============================================================ */
(function () {
  "use strict";

  var CAT = {
    "dolar-oficial": { label: "Dólar oficial", tipo: "linea", unidad: "$",
      hist: "https://api.argentinadatos.com/v1/cotizaciones/dolares/oficial",
      claves: ["dólar", "bcra", "reservas", "cepo"] },
    "dolar-blue": { label: "Dólar blue", tipo: "linea", unidad: "$",
      hist: "https://api.argentinadatos.com/v1/cotizaciones/dolares/blue",
      claves: ["dólar", "blue", "depósitos", "dolares"] },
    "dolar-mep": { label: "Dólar MEP", tipo: "linea", unidad: "$",
      hist: "https://api.argentinadatos.com/v1/cotizaciones/dolares/bolsa",
      claves: ["dólar", "mep", "mercado", "bonos"] },
    "riesgo-pais": { label: "Riesgo país", tipo: "linea", unidad: "pb",
      hist: "https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais",
      claves: ["riesgo", "deuda", "bonos", "mercados"] },
    "inflacion": { label: "Inflación mensual", tipo: "barras", unidad: "%",
      hist: "https://api.argentinadatos.com/v1/finanzas/indices/inflacion",
      claves: ["inflación", "precios", "ipc", "canasta", "salario", "mayorista"] }
  };
  var MES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
  var KEY = document.body.getAttribute("data-key");
  var S = CAT[KEY];
  if (!S) return;

  function fmtV(n) {
    var num;
    if (KEY === "inflacion") num = String(Math.round(n * 10) / 10).replace(".", ",");
    else num = Number(n).toLocaleString("es-AR", { maximumFractionDigits: 0 });
    if (S.unidad === "$") return "$" + num;
    if (S.unidad === "%") return num + "%";
    return num + " " + S.unidad;
  }
  function fmtF(iso, conAnio) {
    try {
      var p = iso.split("-");
      var lab = p[2] && p[2] !== "01" ? (+p[2] + " " + MES[+p[1] - 1]) : MES[+p[1] - 1];
      return conAnio ? lab + " " + p[0].slice(2) : lab;
    } catch (e) { return iso; }
  }

  var NS = "http://www.w3.org/2000/svg";
  function mk(n, a) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); return e; }
  var tt = document.createElement("div"); tt.className = "f-tt"; document.body.appendChild(tt);
  function showTT(html, x, y) { tt.innerHTML = html; tt.style.opacity = 1; tt.style.left = (x + 14) + "px"; tt.style.top = (y - 12) + "px"; }
  function hideTT() { tt.style.opacity = 0; }

  var SERIE = [], EVENTOS = [];

  function cargar() {
    var pSerie = fetch(S.hist).then(function (r) { return r.json(); }).then(function (raw) {
      var pts = [];
      for (var i = 0; i < raw.length; i++) {
        var d = raw[i];
        var v = (d.venta != null) ? +d.venta : +d.valor;
        if (isFinite(v)) pts.push({ f: d.fecha, v: v });
      }
      pts.sort(function (a, b) { return a.f < b.f ? -1 : 1; });
      SERIE = pts;
    });
    var pEv = fetch("../data/eventos.json").then(function (r) { return r.json(); })
      .then(function (j) { EVENTOS = (j.eventos && j.eventos[KEY]) || []; })
      .catch(function () { EVENTOS = []; });
    var pRel = fetch("../data/articulos.json").then(function (r) { return r.json(); })
      .then(function (j) { renderRelacionadas(j.articulos || []); })
      .catch(function () {});
    return Promise.all([pSerie, pEv, pRel]);
  }

  function filtrar(meses) {
    if (meses === "todo") return SERIE.slice();
    var corte = new Date(); corte.setMonth(corte.getMonth() - meses);
    var lim = corte.toISOString().slice(0, 10);
    return SERIE.filter(function (p) { return p.f >= lim; });
  }

  function stats(serie) {
    var vs = serie.map(function (p) { return p.v; });
    var min = Math.min.apply(null, vs), max = Math.max.apply(null, vs);
    var pMin = serie[vs.indexOf(min)], pMax = serie[vs.indexOf(max)];
    return { min: pMin, max: pMax, primero: serie[0], ultimo: serie[serie.length - 1] };
  }

  function dibujar(meses) {
    var cont = document.getElementById("f-chart");
    cont.innerHTML = "";
    var serie = filtrar(meses);
    if (serie.length < 2) { cont.innerHTML = '<div class="f-estado">No hay datos suficientes.</div>'; return; }
    var completa = serie;
    if (S.tipo === "linea" && serie.length > 300) {
      var paso = Math.ceil(serie.length / 300), m = [];
      for (var i = 0; i < serie.length; i += paso) m.push(serie[i]);
      if (m[m.length - 1].f !== serie[serie.length - 1].f) m.push(serie[serie.length - 1]);
      serie = m;
    }
    var st = stats(completa);
    var W = 860, H = 340, mg = { t: 20, r: 64, b: 30, l: 10 };
    var iw = W - mg.l - mg.r, ih = H - mg.t - mg.b;
    var vMin = st.min.v, vMax = st.max.v;
    if (S.tipo === "barras") vMin = Math.min(0, vMin);
    var span = (vMax - vMin) || 1; vMin -= span * 0.06; vMax += span * 0.08;
    var X = function (i) { return mg.l + (i / (serie.length - 1)) * iw; };
    var Y = function (v) { return mg.t + ih - ((v - vMin) / (vMax - vMin)) * ih; };
    var xDe = function (fecha) {
      // posición aproximada por fecha (para eventos)
      var i0 = 0, dist = Infinity;
      for (var i = 0; i < serie.length; i++) {
        var d = Math.abs(new Date(serie[i].f) - new Date(fecha));
        if (d < dist) { dist = d; i0 = i; }
      }
      return { x: X(i0), v: serie[i0].v, dentro: serie[0].f <= fecha && fecha <= serie[serie.length - 1].f };
    };

    var svg = mk("svg", { viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": S.label + ": mínimo " + fmtV(st.min.v) + ", máximo " + fmtV(st.max.v) + " en el período." });

    for (var g = 0; g <= 4; g++) {
      var gv = vMin + (vMax - vMin) * (g / 4), gy = Y(gv);
      svg.appendChild(mk("line", { x1: mg.l, y1: gy, x2: mg.l + iw, y2: gy, stroke: "#E7E1D7", "stroke-width": 1 }));
      var lab = mk("text", { x: W - mg.r + 8, y: gy + 4, "font-family": "IBM Plex Mono, monospace", "font-size": 11, fill: "#8A847C" });
      lab.textContent = fmtV(gv); svg.appendChild(lab);
    }
    var nx = Math.min(6, serie.length);
    for (var x = 0; x < nx; x++) {
      var ix = Math.round(x * (serie.length - 1) / (nx - 1));
      var xl = mk("text", { x: X(ix), y: H - 8, "text-anchor": x === 0 ? "start" : (x === nx - 1 ? "end" : "middle"), "font-family": "IBM Plex Mono, monospace", "font-size": 11, fill: "#8A847C" });
      xl.textContent = fmtF(serie[ix].f, true); svg.appendChild(xl);
    }

    if (S.tipo === "barras") {
      var bw = Math.max(3, Math.min(30, iw / serie.length - 3));
      var Xb = function (i) { return serie.length === 1 ? mg.l + iw / 2 : mg.l + bw / 2 + (i / (serie.length - 1)) * (iw - bw); };
      serie.forEach(function (p, i) {
        var y0 = Y(Math.max(0, p.v)), h = Math.abs(Y(p.v) - Y(0)) || 2;
        var r = mk("rect", { x: Xb(i) - bw / 2, y: y0, width: bw, height: h, rx: 3, fill: "#0E7C86" });
        svg.appendChild(r);
        r.addEventListener("mousemove", function (e) { r.setAttribute("opacity", .8); showTT("<b>" + fmtF(p.f, true) + "</b> · " + fmtV(p.v), e.clientX, e.clientY); });
        r.addEventListener("mouseleave", function () { r.setAttribute("opacity", 1); hideTT(); });
      });
    } else {
      var path = "";
      serie.forEach(function (p, i) { path += (i ? "L" : "M") + X(i).toFixed(1) + " " + Y(p.v).toFixed(1); });
      svg.appendChild(mk("path", { d: path, fill: "none", stroke: "#0E7C86", "stroke-width": 2, "stroke-linejoin": "round", "stroke-linecap": "round" }));
      svg.appendChild(mk("circle", { cx: X(serie.length - 1), cy: Y(serie[serie.length - 1].v), r: 3.5, fill: "#0E7C86", stroke: "#fff", "stroke-width": 2 }));
      var cross = mk("line", { y1: mg.t, y2: mg.t + ih, stroke: "#B9B3A9", "stroke-width": 1, "stroke-dasharray": "3 3", opacity: 0 });
      var dot = mk("circle", { r: 4, fill: "#0E7C86", stroke: "#fff", "stroke-width": 2, opacity: 0 });
      var captura = mk("rect", { x: mg.l, y: mg.t, width: iw, height: ih, fill: "transparent" });
      svg.appendChild(cross); svg.appendChild(dot); svg.appendChild(captura);
      captura.addEventListener("mousemove", function (e) {
        var box = svg.getBoundingClientRect();
        var fx = (e.clientX - box.left) / box.width * W;
        var i = Math.max(0, Math.min(serie.length - 1, Math.round((fx - mg.l) / iw * (serie.length - 1))));
        var p = serie[i];
        cross.setAttribute("x1", X(i)); cross.setAttribute("x2", X(i)); cross.setAttribute("opacity", 1);
        dot.setAttribute("cx", X(i)); dot.setAttribute("cy", Y(p.v)); dot.setAttribute("opacity", 1);
        showTT("<b>" + fmtF(p.f, true) + "</b> · " + fmtV(p.v), e.clientX, e.clientY);
      });
      captura.addEventListener("mouseleave", function () { cross.setAttribute("opacity", 0); dot.setAttribute("opacity", 0); hideTT(); });
    }

    // eventos anotados (dentro del rango)
    var visibles = [];
    EVENTOS.forEach(function (ev) {
      var pos = xDe(ev.fecha);
      if (!pos.dentro) return;
      visibles.push(ev);
      var n = visibles.length;
      svg.appendChild(mk("line", { x1: pos.x, y1: mg.t, x2: pos.x, y2: mg.t + ih, stroke: "#C4701F", "stroke-width": 1, "stroke-dasharray": "4 4", opacity: .7 }));
      var c = mk("circle", { cx: pos.x, cy: mg.t + 10, r: 9, fill: "#C4701F", cursor: "pointer" });
      var t = mk("text", { x: pos.x, y: mg.t + 14, "text-anchor": "middle", "font-family": "IBM Plex Mono, monospace", "font-size": 11, "font-weight": 600, fill: "#fff", "pointer-events": "none" });
      t.textContent = n;
      svg.appendChild(c); svg.appendChild(t);
      c.addEventListener("mousemove", function (e) { showTT("<b>" + fmtF(ev.fecha, true) + "</b> · " + ev.titulo, e.clientX, e.clientY); });
      c.addEventListener("mouseleave", hideTT);
      c.addEventListener("click", function () { window.location.href = ev.nota; });
    });
    cont.appendChild(svg);

    // lista de eventos bajo el gráfico
    var lev = document.getElementById("f-eventos");
    if (visibles.length) {
      lev.innerHTML = visibles.map(function (ev, i) {
        return '<a class="f-ev" href="' + ev.nota + '"><span class="n">' + (i + 1) + "</span><span>" + fmtF(ev.fecha, true) + " — " + ev.titulo + " →</span></a>";
      }).join("");
      lev.style.display = "";
    } else { lev.style.display = "none"; }

    // stats
    var hoyEl = document.getElementById("f-hoy");
    hoyEl.textContent = fmtV(st.ultimo.v);
    var varEl = document.getElementById("f-variacion");
    if (KEY !== "inflacion" && st.primero.v) {
      var p100 = (st.ultimo.v / st.primero.v - 1) * 100;
      varEl.textContent = (p100 >= 0 ? "+" : "−") + Math.abs(p100).toFixed(1).replace(".", ",") + "% en el período";
      varEl.className = "f-var " + (p100 >= 0 ? "up" : "dn");
    } else { varEl.textContent = ""; }
    document.getElementById("f-min").innerHTML = "<b>" + fmtV(st.min.v) + "</b> mínimo (" + fmtF(st.min.f, true) + ")";
    document.getElementById("f-max").innerHTML = "<b>" + fmtV(st.max.v) + "</b> máximo (" + fmtF(st.max.f, true) + ")";

    // CSV del rango
    document.getElementById("f-csv").onclick = function () {
      var lineas = ["fecha,valor"];
      completa.forEach(function (p) { lineas.push(p.f + "," + p.v); });
      var blob = new Blob([lineas.join("\n")], { type: "text/csv;charset=utf-8" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "coninteres-" + KEY + ".csv";
      a.click();
      URL.revokeObjectURL(a.href);
    };
  }

  function renderRelacionadas(arts) {
    var cont = document.getElementById("f-notas");
    if (!cont) return;
    var rel = arts.filter(function (a) {
      var texto = (a.titulo + " " + (a.bajada || "")).toLowerCase();
      return S.claves.some(function (k) { return texto.indexOf(k) !== -1; });
    }).slice(0, 4);
    if (!rel.length) { cont.parentNode.style.display = "none"; return; }
    cont.innerHTML = rel.map(function (a) {
      return '<a class="f-nota" href="../' + a.archivo + '"><span class="fn-num">' + (a.numero || "") + '</span><span class="fn-tit">' + a.titulo + "</span></a>";
    }).join("");
  }

  // rangos
  document.querySelectorAll(".f-rango").forEach(function (b) {
    b.addEventListener("click", function () {
      document.querySelectorAll(".f-rango").forEach(function (x) { x.classList.remove("activo"); });
      b.classList.add("activo");
      var m = b.getAttribute("data-m");
      dibujar(m === "todo" ? "todo" : +m);
    });
  });

  document.getElementById("f-chart").innerHTML = '<div class="f-estado">Cargando la serie completa…</div>';
  cargar().then(function () {
    var act = document.querySelector(".f-rango.activo");
    var m = act ? act.getAttribute("data-m") : "12";
    dibujar(m === "todo" ? "todo" : +m);
  }).catch(function () {
    document.getElementById("f-chart").innerHTML = '<div class="f-estado">No se pudo cargar la serie. Probá de nuevo en unos minutos.</div>';
  });
})();
