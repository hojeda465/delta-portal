/* ============================================================
   Con Interés · nota.js — mejoras de lectura para las NOTAS:
     1. GLOSARIO VIVO: términos económicos con explicación de
        2 líneas al tocarlos, sin salir de la nota.
     2. AUDIO: botón "Escuchar esta nota" con la voz del propio
        navegador (gratis, sin servidores, sin datos).
   Se incluye en /articulos con:
     <script defer src="../assets/nota.js"></script>
   ============================================================ */
(function () {
  "use strict";

  /* ---------- 1 · GLOSARIO ---------- */
  var GLOSARIO = {
    "dólar blue": "La cotización del mercado informal, fuera del sistema financiero. No es oficial, pero funciona como termómetro de la demanda de dólares de la gente.",
    "dólar mep": "El dólar 'bolsa': se compra legalmente comprando un bono en pesos y vendiéndolo en dólares. La vía más usada por ahorristas.",
    "ccl": "Contado con liquidación: como el MEP, pero los dólares quedan en una cuenta fuera del país. Lo usan sobre todo empresas.",
    "riesgo país": "Mide cuánto más caro le sale a la Argentina endeudarse que a EE.UU. Cada 100 puntos básicos = 1 punto porcentual de sobretasa.",
    "rigi": "Régimen de Incentivo para Grandes Inversiones: beneficios impositivos, aduaneros y cambiarios por 30 años para proyectos de más de US$200 millones.",
    "uva": "Unidad de Valor Adquisitivo: una unidad de cuenta que se ajusta por inflación. Los créditos UVA actualizan la deuda por el índice de precios.",
    "carry trade": "Estrategia financiera: vender dólares, colocar los pesos a tasa de interés y recomprar dólares después, apostando a que el tipo de cambio suba menos que la tasa.",
    "monotributo": "Régimen impositivo simplificado para pequeños contribuyentes: una cuota fija mensual reemplaza a Ganancias, IVA y aportes.",
    "superávit primario": "Cuando al Estado le sobra plata después de pagar todos sus gastos, sin contar los intereses de la deuda.",
    "superávit comercial": "Cuando el país exporta por más dólares de los que importa. Es una de las principales fuentes de divisas.",
    "base monetaria": "La cantidad de pesos emitidos por el Banco Central: billetes en circulación más los depósitos de los bancos en el BCRA.",
    "ipc": "Índice de Precios al Consumidor: la medición oficial del INDEC de cuánto suben los precios que paga una familia. Es 'la inflación' de todos los meses.",
    "ipim": "Índice de Precios Internos al por Mayor: la inflación mayorista, la que pagan los comercios antes de vender al público. Suele anticipar al IPC.",
    "interanual": "Comparación contra el mismo mes del año anterior. Elimina el efecto de la estacionalidad (ej.: julio siempre distinto de diciembre).",
    "embi": "El índice de JP Morgan que mide el riesgo país: la diferencia de rendimiento entre los bonos argentinos y los de EE.UU.",
    "plazo fijo": "Depósito bancario a un plazo pactado (mínimo 30 días) que paga una tasa de interés. El clásico instrumento de ahorro en pesos.",
    "pases": "Préstamos de cortísimo plazo entre el Banco Central y los bancos. Su tasa es una referencia clave del costo del dinero.",
    "brecha cambiaria": "La diferencia porcentual entre el dólar oficial y los paralelos (blue, MEP, CCL). Termómetro de la presión sobre el tipo de cambio.",
    "aportes patronales": "Contribuciones que paga el empleador sobre cada salario para financiar jubilaciones, obras sociales y asignaciones.",
    "letes": "Letras del Tesoro: deuda de corto plazo que emite el Estado para financiarse."
  };

  var css = ""
    + ".gl-t{border-bottom:1px dotted #0E7C86;cursor:help;position:relative}"
    + ".gl-pop{position:absolute;z-index:120;background:#16130F;color:#EDE9E3;font-family:'Inter',system-ui,sans-serif;font-size:13px;line-height:1.55;padding:12px 14px;border-radius:10px;max-width:320px;box-shadow:0 8px 30px rgba(22,19,15,.35)}"
    + ".gl-pop .gl-k{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#4FC0A4;font-weight:600;display:block;margin-bottom:5px}"
    + ".gl-pop .gl-x{position:absolute;top:6px;right:10px;color:#8A847C;cursor:pointer;font-size:14px}"
    + ".ci-audio{display:inline-flex;align-items:center;gap:7px;font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;color:#0A5C63;background:none;border:1px solid #DCD6CC;border-radius:999px;padding:5px 13px;cursor:pointer;transition:.15s}"
    + ".ci-audio:hover{border-color:#0E7C86}"
    + ".ci-audio.on{background:#0E7C86;color:#fff;border-color:#0E7C86}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  function marcarGlosario() {
    var zona = document.querySelectorAll(".prose p, .deep-body p, .cocina p");
    if (!zona.length) return;
    var hechos = {};
    var claves = Object.keys(GLOSARIO).sort(function (a, b) { return b.length - a.length; });
    zona.forEach(function (p) {
      claves.forEach(function (term) {
        if (hechos[term]) return;
        var re = new RegExp("(^|[^\\wáéíóúñ])(" + term.replace(/ /g, "[ \\u00a0]") + ")(?![\\wáéíóúñ])", "i");
        // recorrer solo nodos de texto para no romper el HTML
        var tw = document.createTreeWalker(p, NodeFilter.SHOW_TEXT, null);
        var nodo;
        while ((nodo = tw.nextNode())) {
          if (nodo.parentNode.closest(".gl-t,a,b.hl")) continue;
          var m = nodo.nodeValue.match(re);
          if (!m) continue;
          var idx = m.index + m[1].length;
          var fin = idx + m[2].length;
          var span = document.createElement("span");
          span.className = "gl-t";
          span.setAttribute("data-term", term);
          span.textContent = nodo.nodeValue.slice(idx, fin);
          var resto = nodo.splitText(idx);
          resto.nodeValue = resto.nodeValue.slice(m[2].length);
          nodo.parentNode.insertBefore(span, resto);
          hechos[term] = true;
          break;
        }
      });
    });
    document.addEventListener("click", function (e) {
      var viejo = document.querySelector(".gl-pop");
      if (viejo) viejo.remove();
      var t = e.target.closest(".gl-t");
      if (!t) return;
      var term = t.getAttribute("data-term");
      var pop = document.createElement("div");
      pop.className = "gl-pop";
      pop.innerHTML = '<span class="gl-x">✕</span><span class="gl-k">' + term + "</span>" + GLOSARIO[term.toLowerCase()] ;
      document.body.appendChild(pop);
      var r = t.getBoundingClientRect();
      var x = Math.min(r.left, window.innerWidth - 340);
      pop.style.left = Math.max(10, x) + "px";
      pop.style.top = (r.bottom + window.pageYOffset + 8) + "px";
      pop.style.position = "absolute";
    });
  }

  /* ---------- 2 · AUDIO ---------- */
  function armarAudio() {
    if (!("speechSynthesis" in window)) return;
    var byline = document.querySelector(".byline");
    var art = document.querySelector("article");
    if (!byline || !art) return;
    var btn = document.createElement("button");
    btn.type = "button"; btn.className = "ci-audio";
    btn.innerHTML = "&#9654; Escuchar esta nota";
    byline.appendChild(btn);
    var hablando = false, u = null;

    function texto() {
      var partes = [];
      var t = document.querySelector("h1"); if (t) partes.push(t.textContent);
      var s = document.querySelector(".standfirst"); if (s) partes.push(s.textContent);
      document.querySelectorAll(".prose p").forEach(function (p) { partes.push(p.textContent); });
      return partes.join(". ");
    }
    btn.addEventListener("click", function () {
      if (hablando) {
        speechSynthesis.cancel(); hablando = false;
        btn.classList.remove("on"); btn.innerHTML = "&#9654; Escuchar esta nota";
        return;
      }
      u = new SpeechSynthesisUtterance(texto());
      u.lang = "es-AR";
      var voces = speechSynthesis.getVoices();
      var voz = voces.filter(function (v) { return /es[-_](AR|419|MX|ES|US)/i.test(v.lang); })[0];
      if (voz) u.voice = voz;
      u.rate = 1.02;
      u.onend = function () { hablando = false; btn.classList.remove("on"); btn.innerHTML = "&#9654; Escuchar esta nota"; };
      speechSynthesis.speak(u);
      hablando = true;
      btn.classList.add("on"); btn.innerHTML = "&#9632; Detener";
    });
    window.addEventListener("beforeunload", function () { speechSynthesis.cancel(); });
  }

  function init() { marcarGlosario(); armarAudio(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
