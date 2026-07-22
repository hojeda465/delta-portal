/* ============================================================
   Con Interés · test-nivel.js
   "¿Cuánto entendés de economía?" — 5 preguntas, sin registro.
   El resultado (con humor) vive solo en el navegador del lector
   y sugiere por dónde arrancar el Modo Aprendizaje.
   Se incluye en aprender.html con:
     <script defer src="assets/test-nivel.js"></script>
   y se monta solo después del hero.
   ============================================================ */
(function () {
  "use strict";
  var K = "ci_nivel";
  var QS = [
    { q: "Si la inflación de un mes fue 2%, eso significa que…",
      ops: ["Todos los precios subieron exactamente 2%", "En promedio, los precios subieron 2% (algunos más, otros menos)", "El dólar subió 2%"], ok: 1 },
    { q: "Te aumentan el sueldo 10%, pero la inflación acumulada fue 15%. Tu poder de compra…",
      ops: ["Subió: cobrás más pesos", "Quedó igual", "Bajó: comprás menos que antes"], ok: 2 },
    { q: "El 'riesgo país' mide…",
      ops: ["Cuánto más caro le sale al Estado argentino endeudarse que a EE.UU.", "El nivel de inseguridad del país", "Cuántas empresas quebraron en el año"], ok: 0 },
    { q: "Un plazo fijo te paga 3% mensual y la inflación fue 2%. Tu ganancia real fue…",
      ops: ["5%", "Alrededor de 1%", "Perdiste plata"], ok: 1 },
    { q: "¿Cuál de estos dólares suele ser el más caro?",
      ops: ["El oficial", "El blue", "Son todos iguales"], ok: 1 }
  ];
  var NIVELES = [
    { max: 1, titulo: "Recién llegás — y este diario se hizo exactamente para vos.",
      detalle: "Nada de vergüenza: nadie nace sabiendo qué es el IPC. Arrancá por la ruta 'La economía desde cero' y en dos semanas leés el diario de otra manera.",
      emoji: "🌱" },
    { max: 3, titulo: "Nivel: sobreviviente de la inflación.",
      detalle: "La economía la vivís todos los días — ahora te falta ponerle nombre a lo que ya intuís. La ruta de 'Tu plata' es tu próximo paso natural.",
      emoji: "🛡️" },
    { max: 5, titulo: "Casi economista de asado — te falta el título nomás.",
      detalle: "Tenés la base firme. Andá directo a las lecciones de inversión y crédito, y usá las fichas de indicadores para afilar el ojo.",
      emoji: "🎓" }
  ];

  var css = ""
    + ".tn{margin:6px 0 34px}"
    + ".tn-card{background:linear-gradient(120deg,#16130F,#0A5C63);border-radius:16px;color:#fff;padding:26px 28px}"
    + ".tn-kick{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#E8833A;font-weight:600;margin-bottom:8px}"
    + ".tn-card h2{font-family:'Source Serif 4',Georgia,serif;font-size:clamp(20px,2.6vw,26px);font-weight:700;margin:0 0 6px;color:#fff;letter-spacing:-.015em}"
    + ".tn-card .sub{font-size:13px;color:#CDE4E1;margin:0 0 16px}"
    + ".tn-prog{font-family:'IBM Plex Mono',monospace;font-size:11px;color:#9DC4C0;margin-bottom:10px}"
    + ".tn-q{font-family:'Source Serif 4',Georgia,serif;font-size:18px;font-weight:600;margin:0 0 14px;color:#fff}"
    + ".tn-ops{display:flex;flex-direction:column;gap:10px}"
    + ".tn-op{text-align:left;font-family:'Inter',system-ui,sans-serif;font-size:14px;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.22);color:#EDE9E3;border-radius:10px;padding:12px 15px;cursor:pointer;transition:.15s;line-height:1.45}"
    + ".tn-op:hover{border-color:#4FC0A4;background:rgba(255,255,255,.14)}"
    + ".tn-res .emoji{font-size:40px;line-height:1}"
    + ".tn-res h3{font-family:'Source Serif 4',Georgia,serif;font-size:clamp(19px,2.4vw,24px);font-weight:700;color:#F3D9A8;margin:10px 0 8px;letter-spacing:-.01em}"
    + ".tn-res p{font-size:14px;color:#CDE4E1;margin:0 0 16px;line-height:1.6}"
    + ".tn-res .pts{font-family:'IBM Plex Mono',monospace;font-size:12px;color:#9DC4C0;margin-bottom:6px}"
    + ".tn-acciones{display:flex;gap:10px;flex-wrap:wrap}"
    + ".tn-acciones a,.tn-acciones button{font-family:'Inter',system-ui,sans-serif;font-size:13px;font-weight:600;border-radius:10px;padding:10px 16px;cursor:pointer;text-decoration:none;border:none;transition:.15s}"
    + ".tn-a1{background:#fff;color:#16130F}.tn-a1:hover{background:#F3D9A8}"
    + ".tn-a2{background:#2E8B6F;color:#fff}.tn-a2:hover{background:#1E6B4F}"
    + ".tn-a3{background:none;border:1px solid rgba(255,255,255,.3) !important;color:#CDE4E1}"
    + ".tn-empezar{font-family:'Inter',system-ui,sans-serif;font-size:14px;font-weight:600;background:#C4701F;color:#fff;border:none;border-radius:10px;padding:12px 22px;cursor:pointer;transition:.15s}"
    + ".tn-empezar:hover{background:#E8833A}";
  var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);

  function est() { try { return JSON.parse(localStorage.getItem(K) || "null"); } catch (e) { return null; } }
  function guardar(s) { try { localStorage.setItem(K, JSON.stringify(s)); } catch (e) {} }
  function nivelDe(p) { for (var i = 0; i < NIVELES.length; i++) if (p <= NIVELES[i].max) return NIVELES[i]; return NIVELES[2]; }

  var cont = document.createElement("div");
  cont.className = "tn";
  cont.innerHTML = '<div class="tn-card" id="tnCard"></div>';
  // montar después del hero (primer .wrap del contenido) o antes del footer
  var hero = document.querySelector(".hero");
  if (hero && hero.parentNode) hero.parentNode.insertBefore(cont, hero.nextSibling);
  else { var f = document.querySelector("footer"); (f ? f.parentNode : document.body).insertBefore(cont, f); }

  var card = document.getElementById("tnCard");
  var idx = 0, puntos = 0;

  function inicio() {
    var s = est();
    if (s && s.nivel != null) { resultado(s.puntos, true); return; }
    card.innerHTML = '<div class="tn-kick">Test · 1 minuto · sin registro</div>'
      + "<h2>¿Cuánto entendés de economía?</h2>"
      + '<p class="sub">Cinco preguntas para saber tu punto de partida. El resultado queda solo en tu navegador — como todo acá, no te pedimos nada.</p>'
      + '<button class="tn-empezar" type="button">Empezar el test →</button>';
    card.querySelector(".tn-empezar").addEventListener("click", function () { idx = 0; puntos = 0; pregunta(); });
  }

  function pregunta() {
    var q = QS[idx];
    card.innerHTML = '<div class="tn-kick">Test de nivel</div>'
      + '<div class="tn-prog">Pregunta ' + (idx + 1) + " de " + QS.length + "</div>"
      + '<p class="tn-q">' + q.q + "</p>"
      + '<div class="tn-ops"></div>';
    var ops = card.querySelector(".tn-ops");
    q.ops.forEach(function (o, i) {
      var b = document.createElement("button");
      b.className = "tn-op"; b.type = "button"; b.textContent = o;
      b.addEventListener("click", function () {
        if (i === q.ok) puntos++;
        idx++;
        if (idx < QS.length) pregunta();
        else { guardar({ puntos: puntos, nivel: nivelDe(puntos).titulo, fecha: new Date().toISOString().slice(0, 10) }); resultado(puntos, false); }
      });
      ops.appendChild(b);
    });
  }

  function resultado(p, previo) {
    var n = nivelDe(p);
    card.innerHTML = '<div class="tn-kick">' + (previo ? "Tu nivel (según tu último test)" : "Resultado") + "</div>"
      + '<div class="tn-res">'
      + '<div class="emoji">' + n.emoji + "</div>"
      + '<div class="pts">' + p + " de " + QS.length + " correctas</div>"
      + "<h3>" + n.titulo + "</h3>"
      + "<p>" + n.detalle + "</p>"
      + '<div class="tn-acciones">'
      + '<a class="tn-a1" href="#tracks">Ver las rutas →</a>'
      + '<button class="tn-a2" type="button" id="tnWsp">Compartir por WhatsApp</button>'
      + '<button class="tn-a3" type="button" id="tnRe">Rehacer el test</button>'
      + "</div></div>";
    var texto = n.emoji + " Mi nivel de economía según Con Interés: “" + n.titulo + "” (" + p + "/" + QS.length + "). Medí el tuyo — 1 minuto, gratis: https://coninteres.com/aprender.html";
    document.getElementById("tnWsp").addEventListener("click", function () { window.open("https://wa.me/?text=" + encodeURIComponent(texto), "_blank"); });
    document.getElementById("tnRe").addEventListener("click", function () { try { localStorage.removeItem(K); } catch (e) {} idx = 0; puntos = 0; pregunta(); });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", inicio);
  else inicio();
})();
