/* ============================================================
   Con Interés · leccion-hoy.js
   El puente lección→noticia: al final de cada lección del Modo
   Aprendizaje, muestra "Esto, en la economía real de hoy" con
   las notas actuales donde el concepto está vivo.
   Se incluye en /lecciones con:
     <script defer src="../assets/leccion-hoy.js"></script>
   ============================================================ */
(function () {
  "use strict";

  // lección (por nombre de archivo) -> palabras clave para buscar notas
  var MAPA = {
    "inflacion": ["inflación", "precios", "ipc", "mayorista", "canasta"],
    "inflacion-bolsillo": ["inflación", "precios", "salario", "canasta"],
    "riesgo-pais": ["riesgo", "deuda", "bonos"],
    "presupuesto": ["salario", "canasta", "sueldo", "consumo"],
    "tasa-real": ["plazo fijo", "tasa", "crédito", "depósitos"],
    "pesos-o-dolares": ["dólar", "depósitos", "reservas"],
    "deuda-credito": ["crédito", "mora", "cuotas", "hipotec", "tarjeta"],
    "uva-credito-conviene": ["hipotec", "uva", "crédito"],
    "invertir-primer-paso": ["mercado", "bonos", "acciones", "startups", "inversión", "soja"]
  };

  var archivo = (location.pathname.split("/").pop() || "").replace(".html", "");
  var claves = MAPA[archivo];
  if (!claves) return;

  var css = ""
    + ".lh-band{max-width:900px;margin:40px auto 0;padding:0 22px}"
    + ".lh-head{font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#0A5C63;font-weight:600;display:flex;align-items:center;gap:14px;margin-bottom:14px}"
    + ".lh-head:after{content:'';flex:1;height:1px;background:#DCD6CC}"
    + ".lh-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}"
    + ".lh-card{background:#fff;border:1px solid #EAE4DA;border-radius:12px;padding:16px;text-decoration:none;display:block;transition:.15s}"
    + ".lh-card:hover{border-color:#0E7C86;transform:translateY(-2px)}"
    + ".lh-num{display:block;font-family:'IBM Plex Mono',monospace;font-size:15px;font-weight:600;color:#0A5C63;margin-bottom:6px}"
    + ".lh-tit{font-family:'Source Serif 4',Georgia,serif;font-size:15px;font-weight:600;color:#16130F;line-height:1.3}"
    + ".lh-sub{font-size:12px;color:#8A847C;margin-top:10px;font-family:'IBM Plex Mono',monospace}"
    + "@media(max-width:640px){.lh-grid{grid-template-columns:1fr}}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  fetch("../data/articulos.json").then(function (r) { return r.json(); }).then(function (j) {
    var arts = (j.articulos || []).filter(function (a) {
      var t = (a.titulo + " " + (a.bajada || "") + " " + (a.numero_label || "")).toLowerCase();
      return claves.some(function (k) { return t.indexOf(k) !== -1; });
    }).slice(0, 3);
    if (!arts.length) return;
    var band = document.createElement("div");
    band.className = "lh-band";
    band.innerHTML = '<div class="lh-head">&#9651; Esto, en la economía real de hoy</div>'
      + '<div class="lh-grid">' + arts.map(function (a) {
        return '<a class="lh-card" href="../' + a.archivo + '"><span class="lh-num">' + (a.numero || "") + '</span><span class="lh-tit">' + a.titulo + "</span></a>";
      }).join("") + "</div>"
      + '<p class="lh-sub">Lo que acabás de aprender, aplicado a las noticias de esta semana. Ese es el método Con Interés.</p>';
    var foot = document.querySelector("footer");
    if (foot) foot.parentNode.insertBefore(band, foot);
    else document.body.appendChild(band);
  }).catch(function () {});
})();
