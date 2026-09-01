/*
 * Con Interes - La pregunta del dia: logica compartida
 * ---------------------------------------------------------------------------
 * La pregunta vive en dos lugares: la pagina completa (pregunta.html) y el
 * bloque de la portada. Este archivo es la UNICA fuente de verdad de lo que no
 * puede divergir entre los dos: cual es la respuesta correcta, como se cuenta
 * la racha y que texto se comparte. Cada pagina dibuja lo suyo.
 *
 * La racha vive solo en el navegador del lector (localStorage). No se envia a
 * ningun lado y no identifica a nadie. Si el navegador la bloquea, todo sigue
 * funcionando: se pierde la racha, no la pregunta.
 */
(function (global) {
  "use strict";

  var K = "ci_pregunta";
  var MES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"];

  function estado() {
    try { return JSON.parse(localStorage.getItem(K) || "{}"); } catch (e) { return {}; }
  }
  function guardar(s) {
    try { localStorage.setItem(K, JSON.stringify(s)); } catch (e) {}
  }
  function diaAnterior(iso) {
    var d = new Date(iso + "T12:00:00");
    d.setDate(d.getDate() - 1);
    return d.toISOString().slice(0, 10);
  }

  /* Carga la pregunta del dia. `base` es el prefijo hasta la raiz del sitio
     ("" en la portada, "../" si algun dia se usa desde articulos/). */
  function cargar(base) {
    return fetch((base || "") + "data/pregunta.json").then(function (r) {
      if (!r.ok) throw new Error("pregunta " + r.status);
      return r.json();
    });
  }

  /* Ya respondio la de hoy? Devuelve la eleccion o null. */
  function respondida(P) {
    var s = estado();
    return (s.ultimaFecha === P.fecha && s.ultimaEleccion != null) ? s.ultimaEleccion : null;
  }

  /* Registra la respuesta. Idempotente por dia: si ya jugo hoy, no vuelve a
     contar (asi responder en la portada y despues abrir la pagina completa no
     infla la racha ni las estadisticas). */
  function responder(P, eleccion) {
    var s = estado();
    var acierto = (eleccion === P.correcta);
    if (s.ultimaFecha !== P.fecha) {
      if (s.rachaFecha === diaAnterior(P.fecha)) s.racha = (s.racha || 0) + 1;
      else s.racha = 1;
      s.rachaFecha = P.fecha;
      s.ultimaFecha = P.fecha;
      s.ultimaEleccion = eleccion;
      s.jugadas = (s.jugadas || 0) + 1;
      s.aciertos = (s.aciertos || 0) + (acierto ? 1 : 0);
      guardar(s);
    }
    return { acierto: acierto, racha: s.racha || 1, jugadas: s.jugadas || 1, aciertos: s.aciertos || 0 };
  }

  function fechaLarga(iso) {
    var f = iso.split("-");
    return (+f[2]) + " de " + MES[+f[1] - 1] + " de " + f[0];
  }

  function plural(n, sing, plu) { return n + " " + (n === 1 ? sing : plu); }

  function textoCompartir(acierto, racha) {
    return (acierto ? "🟩" : "🟥")
      + " La Pregunta del Día de Con Interés · racha: " + plural(racha, "día", "días")
      + " · Jugala vos: https://coninteres.com/pregunta.html";
  }

  global.CIPregunta = {
    cargar: cargar,
    estado: estado,
    respondida: respondida,
    responder: responder,
    fechaLarga: fechaLarga,
    plural: plural,
    textoCompartir: textoCompartir
  };
})(window);
