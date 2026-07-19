/*
 * Con Interés — instrumentación de métricas de crecimiento (privacy-first)
 * ------------------------------------------------------------------------
 * Mide INTERÉS sin cookies, sin datos personales, sin banners:
 *   - profundidad de scroll (25/50/75/100%)
 *   - tiempo de lectura (buckets)
 *   - click al Modo Aprendizaje (nota -> lección)
 *   - salida (para tiempo efectivo)
 *
 * ESTADO: scaffold LISTO PARA ACTIVAR. No envía nada hasta que se defina el
 * proveedor. Rellenar ENDPOINT/SITE con GoatCounter o Cloudflare/Plausible una
 * vez que Horacio autorice el alta de la cuenta. Mientras ENDPOINT sea null,
 * el script no hace ninguna llamada de red (no rompe nada al incluirlo).
 *
 * Inclusión sugerida (una línea, al final del <body> de notas y lecciones):
 *   <script defer src="/assets/metrics.js"></script>
 */
(function () {
  "use strict";

  // === CONFIG (completar al activar) ===
  var ENDPOINT = null;          // p.ej. "https://coninteres.goatcounter.com/count"
  var PROVIDER = null;          // "goatcounter" | "plausible" | "cloudflare"
  // ======================================

  if (!ENDPOINT) return;        // sin proveedor definido: no medimos, no molestamos.

  var path = location.pathname;
  var start = Date.now();
  var sent = {};                // evita duplicar eventos

  function send(event, extra) {
    if (sent[event]) return;
    sent[event] = true;
    try {
      var payload = { p: path, e: event, t: Date.now() - start };
      if (extra) for (var k in extra) payload[k] = extra[k];
      // beacon: no bloquea la navegación, sobrevive a la salida de página
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, JSON.stringify(payload));
      } else {
        fetch(ENDPOINT, { method: "POST", keepalive: true, body: JSON.stringify(payload) });
      }
    } catch (_) { /* nunca romper la página del lector */ }
  }

  // --- Profundidad de scroll (B2) ---
  var marks = [25, 50, 75, 100];
  function onScroll() {
    var h = document.documentElement;
    var scrolled = (h.scrollTop || document.body.scrollTop);
    var height = (h.scrollHeight - h.clientHeight) || 1;
    var pct = Math.min(100, Math.round((scrolled / height) * 100));
    for (var i = 0; i < marks.length; i++) {
      if (pct >= marks[i]) send("scroll_" + marks[i]);
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  // --- Tiempo de lectura por buckets (B1) ---
  [30, 60, 120, 300].forEach(function (s) {
    setTimeout(function () { send("dwell_" + s + "s"); }, s * 1000);
  });

  // --- Click al Modo Aprendizaje (B4) ---
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a");
    if (!a) return;
    var href = a.getAttribute("href") || "";
    if (/aprender\.html|\/lecciones\//.test(href)) {
      send("to_modo_aprendizaje", { dest: href });
    }
  }, true);

  // --- Salida: tiempo efectivo final (B1) ---
  window.addEventListener("pagehide", function () { send("exit"); });
})();
