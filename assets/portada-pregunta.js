/*
 * Con Interes - el bloque de la pregunta del dia en la portada
 * ---------------------------------------------------------------------------
 * Dibuja la version compacta. La logica (respuesta correcta, racha, texto para
 * compartir) sale de assets/pregunta.js, que comparte con pregunta.html: si
 * alguien responde aca y despues abre la pagina completa, ve su respuesta y la
 * racha no se cuenta dos veces.
 *
 * El bloque nace con [hidden] en el HTML y solo se muestra cuando la pregunta
 * cargo bien. Si data/pregunta.json falla, la portada queda como si el bloque
 * no existiera: una seccion vacia seria peor que ninguna.
 */
(function () {
  "use strict";

  var raiz = document.getElementById("pregunta");
  if (!raiz || !window.CIPregunta) return;
  var Q = window.CIPregunta;

  Q.cargar("").then(function (P) {
    if (!P || !P.pregunta || !P.opciones || !P.opciones.length) return;

    document.getElementById("pbQ").textContent = P.pregunta;

    // La fecha va siempre a la vista. data/pregunta.json se renueva en la
    // primera corrida del dia; si un dia no hubo corrida, el bloque mostraria
    // la pregunta de ayer. Que se vea de que dia es, y si no es de hoy que se
    // note: preferimos quedar en evidencia antes que hacerla pasar por nueva.
    var fecha = document.getElementById("pbFecha");
    if (fecha) {
      var hoy = new Date();
      var iso = new Date(hoy.getTime() - hoy.getTimezoneOffset() * 60000)
                  .toISOString().slice(0, 10);
      fecha.textContent = "· " + Q.fechaLarga(P.fecha);
      if (P.fecha !== iso) fecha.className = "pb-fecha vieja";
    }

    var ops = document.getElementById("pbOps");
    P.opciones.forEach(function (texto, i) {
      var b = document.createElement("button");
      b.type = "button";
      b.textContent = texto;
      b.addEventListener("click", function () {
        Q.responder(P, i);
        mostrar(P, i);
      });
      ops.appendChild(b);
    });

    pintarRacha();
    raiz.hidden = false;

    var ya = Q.respondida(P);
    if (ya != null) mostrar(P, ya);
  }).catch(function () {
    /* silencio a proposito: el bloque queda oculto */
  });

  function mostrar(P, eleccion) {
    var acierto = (eleccion === P.correcta);

    [].forEach.call(document.querySelectorAll("#pbOps button"), function (b, j) {
      b.disabled = true;
      if (j === P.correcta) b.className = "ok";
      else if (j === eleccion) b.className = "mal";
    });

    var ver = document.getElementById("pbVer");
    ver.textContent = acierto ? "✓ Correcto." : "✕ No era esa — pero ahora lo sabés.";
    ver.className = "pb-ver " + (acierto ? "ok" : "mal");

    // En la portada va la explicacion recortada; la completa esta a un clic.
    var e = P.explicacion || "";
    var corte = e.length > 260 ? e.slice(0, 260).replace(/\s+\S*$/, "") + "…" : e;
    document.getElementById("pbExpl").textContent = corte;

    var nota = document.getElementById("pbNota");
    if (P.nota) { nota.href = P.nota; nota.hidden = false; }

    document.getElementById("pbRes").classList.add("on");
    pintarRacha();
  }

  function pintarRacha() {
    var s = Q.estado();
    if (!s.racha) return;
    document.getElementById("pbRacha").textContent =
      "Racha: " + Q.plural(s.racha, "día", "días")
      + " · " + (s.aciertos || 0) + "/" + (s.jugadas || 0);
  }
})();
