/* ============================================================
   Con Interés · widgets.js
   Widgets compartidos de todo el sitio:
     1. TICKER de indicadores (dólar oficial/blue/MEP, riesgo país,
        inflación mensual) — datos de APIs públicas, se actualiza solo.
     2. NEWSLETTER — captura de email conectada a Buttondown.
   Se incluye con:  <script defer src="assets/widgets.js"></script>
   (o ../assets/widgets.js desde /articulos y /lecciones)
   ============================================================ */
(function () {
  "use strict";

  /* ------------------------------------------------------------
     CONFIGURACIÓN
     Cuando crees la cuenta en https://buttondown.com, poné acá el
     nombre de usuario elegido. Es lo ÚNICO que hay que tocar.
     ------------------------------------------------------------ */
  var BUTTONDOWN_USER = "coninteres"; // ← usuario de Buttondown

  var TICKER_CACHE_KEY = "ci_ticker_v1";
  var TICKER_TTL_MS = 10 * 60 * 1000; // 10 minutos

  /* ---------- estilos (autocontenidos) ---------- */
  var css = ""
    + ".ci-ticker{background:#16130F;border-bottom:1px solid #2E2A25;overflow:hidden}"
    + ".ci-ticker .ci-tk-in{max-width:1080px;margin:0 auto;padding:8px 24px;display:flex;gap:22px;align-items:center;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}"
    + ".ci-ticker .ci-tk-in::-webkit-scrollbar{display:none}"
    + ".ci-tk-item{display:flex;align-items:baseline;gap:7px;font-family:'IBM Plex Mono',ui-monospace,monospace;font-size:12px;white-space:nowrap;flex:0 0 auto}"
    + ".ci-tk-item .k{color:#A39D93;letter-spacing:.04em}"
    + ".ci-tk-item .v{color:#fff;font-weight:600}"
    + ".ci-tk-item .var{font-size:11px;font-weight:600}"
    + ".ci-tk-item .var.up{color:#E8833A}.ci-tk-item .var.dn{color:#4FC0A4}"
    + ".ci-tk-src{margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:10px;color:#6B6560;white-space:nowrap;flex:0 0 auto}"
    + ".ci-news-box{background:#0A5C63;border-radius:16px;padding:30px 30px 26px;margin:36px 0;color:#fff}"
    + ".ci-news-box .nb-kick{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#4FC0A4;font-weight:600;margin-bottom:8px}"
    + ".ci-news-box h3{font-family:'Source Serif 4',Georgia,serif;font-size:26px;font-weight:700;margin:0 0 6px;line-height:1.2;color:#fff}"
    + ".ci-news-box p{font-size:14px;color:#CDE4E1;margin:0 0 18px;max-width:52ch;line-height:1.55}"
    + ".ci-news-form{display:flex;gap:10px;flex-wrap:wrap}"
    + ".ci-news-form input[type=email]{flex:1 1 240px;min-width:0;font-family:'Inter',system-ui,sans-serif;font-size:15px;padding:12px 16px;border-radius:10px;border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.1);color:#fff;outline:none}"
    + ".ci-news-form input[type=email]::placeholder{color:#9DC4C0}"
    + ".ci-news-form input[type=email]:focus{border-color:#4FC0A4;background:rgba(255,255,255,.16)}"
    + ".ci-news-form button{font-family:'Inter',system-ui,sans-serif;font-size:15px;font-weight:600;padding:12px 22px;border-radius:10px;border:none;background:#C4701F;color:#fff;cursor:pointer;transition:.15s}"
    + ".ci-news-form button:hover{background:#E8833A}"
    + ".ci-news-fine{font-family:'IBM Plex Mono',monospace;font-size:11px;color:#9DC4C0;margin-top:12px}"
    + ".ci-news-ok{font-size:15px;color:#fff;background:rgba(79,192,164,.18);border:1px solid #4FC0A4;border-radius:10px;padding:14px 16px;margin-top:4px}"
    + "@media(max-width:600px){.ci-news-box{padding:24px 20px}.ci-news-box h3{font-size:22px}}";

  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  /* ============================================================
     1 · TICKER DE INDICADORES
     Fuentes: dolarapi.com (dólar) · argentinadatos.com (riesgo
     país e inflación). Si una API no responde, el ítem no se
     muestra; si ninguna responde, el ticker entero se oculta.
     ============================================================ */
  function fmtARS(n) {
    try {
      return "$" + Number(n).toLocaleString("es-AR", { maximumFractionDigits: 0 });
    } catch (e) { return "$" + n; }
  }

  function tickerData() {
    // cache para no pegarle a las APIs en cada página vista
    try {
      var c = JSON.parse(sessionStorage.getItem(TICKER_CACHE_KEY) || "null");
      if (c && Date.now() - c.t < TICKER_TTL_MS) return Promise.resolve(c.items);
    } catch (e) { /* sin sessionStorage, seguimos */ }

    var items = [];
    var pDolar = fetch("https://dolarapi.com/v1/dolares")
      .then(function (r) { return r.json(); })
      .then(function (ds) {
        var find = function (casa) {
          for (var i = 0; i < ds.length; i++) if (ds[i].casa === casa) return ds[i];
          return null;
        };
        var of_ = find("oficial"), bl = find("blue"), mep = find("bolsa");
        if (of_) items.push({ k: "Dólar oficial", v: fmtARS(of_.venta) });
        if (bl) items.push({ k: "Blue", v: fmtARS(bl.venta) });
        if (mep) items.push({ k: "MEP", v: fmtARS(mep.venta) });
      }).catch(function () {});

    var pRiesgo = fetch("https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais/ultimo")
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d && d.valor != null) items.push({ k: "Riesgo país", v: Math.round(d.valor) + " pb" });
      }).catch(function () {});

    var pInf = fetch("https://api.argentinadatos.com/v1/finanzas/indices/inflacion")
      .then(function (r) { return r.json(); })
      .then(function (serie) {
        if (serie && serie.length) {
          var u = serie[serie.length - 1];
          var mes = "";
          try {
            var f = u.fecha.split("-");
            var MES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"];
            mes = " (" + MES[parseInt(f[1], 10) - 1] + ")";
          } catch (e) {}
          items.push({ k: "Inflación mensual" + mes, v: String(u.valor).replace(".", ",") + "%" });
        }
      }).catch(function () {});

    return Promise.all([pDolar, pRiesgo, pInf]).then(function () {
      // orden estable: dólares primero, luego riesgo, luego inflación
      try { sessionStorage.setItem(TICKER_CACHE_KEY, JSON.stringify({ t: Date.now(), items: items })); } catch (e) {}
      return items;
    });
  }

  function renderTicker() {
    var mount = document.getElementById("ci-ticker");
    if (!mount) {
      var mast = document.querySelector(".masthead");
      if (!mast) return;
      mount = document.createElement("div");
      mount.id = "ci-ticker";
      mast.parentNode.insertBefore(mount, mast.nextSibling);
    }
    tickerData().then(function (items) {
      if (!items || !items.length) { mount.remove(); return; }
      var h = '<div class="ci-ticker"><div class="ci-tk-in">';
      items.forEach(function (it) {
        h += '<span class="ci-tk-item"><span class="k">' + it.k + '</span><span class="v">' + it.v + "</span></span>";
      });
      h += '<span class="ci-tk-src">dolarapi.com · argentinadatos.com</span></div></div>';
      mount.innerHTML = h;
    });
  }

  /* ============================================================
     2 · NEWSLETTER (Buttondown)
     Se renderiza en cada <div class="ci-news"></div>. Si la página
     no tiene ninguno, se inserta uno solo antes del <footer>.
     ============================================================ */
  function newsletterHTML() {
    return ''
      + '<div class="ci-news-box">'
      + '<div class="nb-kick">% Newsletter · gratis</div>'
      + "<h3>La economía del día, en tu mail</h3>"
      + "<p>Los datos que importan, verificados y explicados sin jerga, directo de la redacción de Con Interés. Un mail por día, se lee en 3 minutos.</p>"
      + '<form class="ci-news-form" action="https://buttondown.com/api/emails/embed-subscribe/' + BUTTONDOWN_USER + '" method="post" target="_blank">'
      + '<input type="email" name="email" required placeholder="tu@email.com" aria-label="Tu email">'
      + "<button type=\"submit\">Suscribirme</button>"
      + "</form>"
      + '<div class="ci-news-fine">Sin spam. Salís cuando quieras, con un clic.</div>'
      + "</div>";
  }

  function renderNewsletter() {
    var mounts = document.querySelectorAll(".ci-news");
    if (!mounts.length) {
      var foot = document.querySelector("footer");
      if (!foot) return;
      var d = document.createElement("div");
      d.className = "ci-news";
      d.style.maxWidth = "720px";
      d.style.margin = "0 auto";
      d.style.padding = "0 22px";
      foot.parentNode.insertBefore(d, foot);
      mounts = [d];
    }
    Array.prototype.forEach.call(mounts, function (m) {
      m.innerHTML = newsletterHTML();
      var form = m.querySelector("form");
      form.addEventListener("submit", function () {
        var box = m.querySelector(".ci-news-box");
        setTimeout(function () {
          form.outerHTML = '<div class="ci-news-ok">¡Listo! Revisá tu casilla para confirmar la suscripción. Gracias por leer Con Interés.</div>';
        }, 300);
      });
    });
  }

  function init() { renderTicker(); renderNewsletter(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
