# Mision 4 - Cambios al sitio

**Objetivo:** hacer una modificacion de fondo en el portal sin romper nada.

Horacio te dice que quiere cambiar. Antes de tocar un archivo, entende como esta
armado el sitio.

## Lo que hay que saber antes de editar

- **`index.html` y `hoy.html` son GENERADOS.** Salen de `scripts/build_portada.py`
  leyendo los manifiestos de `data/`. Editarlos a mano no sirve: el proximo build
  te pisa el cambio. Si hay que cambiar la portada, se cambia el script.
- **Las notas nuevas salen de `agente/plantilla.html`.** Un cambio que tenga que
  aparecer en todas las notas futuras va ahi. Si tiene que aparecer tambien en
  las 90 notas ya publicadas, hace falta un script que las recorra - proponelo,
  no lo improvises nota por nota.
- **Toda pagina nueva lleva los widgets compartidos** antes de `</body>`:
  `<!-- CI-WIDGETS --><script defer src="../assets/ticker.js"></script>`
  o corre `python scripts/inject_widgets.py`, que es idempotente.
- **El sitio es estatico, en GitHub Pages.** No hay servidor ni base de datos.
  Cualquier cosa que necesite guardar algo del lector necesita un servicio
  externo: decilo antes de empezar, no a mitad de camino.
- **Sin registro, sin publicidad, sin pedir emails.** Es decision editorial, no
  una limitacion tecnica. Lo unico que se guarda del lector vive en su navegador
  (la racha de la pregunta del dia, los perfiles de "como te afecta").

## Como trabajar

1. **Primero mostrale el plan.** Que archivos vas a tocar, que hace cada cambio y
   que puede romperse. Espera que confirme.
2. **Un cambio por vez.** Si te pidio tres cosas, hacelas de a una y mostra cada
   una antes de seguir.
3. **Despues de tocar cualquier plantilla o script de build,** corre
   `python scripts/build_portada.py` y revisa que la portada siga bien.
4. **Si tocaste algo con URLs,** corre `python scripts/verificar_enlaces.py`.
5. **Actualiza la documentacion.** Si el cambio altera como se trabaja, se
   escribe en `agente/NEWSROOM.md` o en `CLAUDE.md` en la misma corrida. El
   runbook desactualizado es peor que no tenerlo.

## Cosas que NO se hacen sin preguntar

- Cambiar la identidad visual (tokens de color, tipografias, grilla).
- Tocar el disclaimer legal del pie, el aviso de "no es asesoramiento financiero"
  o cualquier texto de `legal.html` y `privacidad.html`.
- Agregar un servicio de terceros que reciba datos de lectores. Eso obliga a
  revisar `privacidad.html`, que hoy declara que no se mantienen bases de datos
  de lectores.
- Borrar o renombrar notas publicadas: los links viven en Google y en el sitemap.

**No hagas el commit vos.** El script le pregunta al final si sube los cambios.
