# Mision 2 - Revisar y publicar de la cola

**Objetivo:** que Horacio pueda leer un borrador y decidir, y que la decision se
ejecute bien.

## Pasos

1. Lee `data/cola.json` y lista los borradores que esperan. Para cada uno mostra:
   titulo, seccion, cifra ancla con su unidad, cuantas fuentes tiene y la fecha
   en que entro a la cola.
   - **Si la cola esta vacia,** decilo y ofrecele correr una corrida de redaccion.
2. Preguntale cual quiere revisar.
3. **Antes de que decida, corre los tres chequeos sobre ese borrador** y mostrale
   el resultado. No alcanza con que la nota ya haya pasado por el editor de
   cierre: se revisa de nuevo antes de publicar.
   - `python scripts/verificar_enlaces.py` - cada URL citada devuelve 200 y
     coincide con el dato que respalda.
   - Cada superlativo ("record", "el mayor desde...") tiene su valor previo
     documentado con fuente.
   - Copete, grafico, cuerpo y entrada de manifiesto cierran entre si: cualquier
     numero que aparezca en dos lugares coincide exactamente.
   - **Si alguno falla, decilo antes de que apruebe.** Ese es el punto de esta
     mision.
4. Mostrale de que se trata la nota: el copete, la cifra ancla y las fuentes. Si
   quiere leerla entera, la ruta local del archivo y la URL publica del borrador.
5. Segun lo que decida:

   **Aprobar:**
   ```
   python scripts/aprobar.py <id>
   ```
   Mueve el archivo de `cola/` a `articulos/`, pasa la entrada de `cola.json` a
   `articulos.json`, marca el tema como `publicada` en `cubiertas.json`, saca el
   `noindex` y regenera la portada.

   **Rechazar:**
   ```
   python scripts/rechazar.py <id> "motivo"
   ```
   Lo borra de la cola y lo deja registrado como descartado en `cubiertas.json`,
   con el motivo, para que no vuelva a salir.

6. Verifica que `index.html` y `hoy.html` se hayan regenerado. Si no, corre
   `python scripts/build_portada.py`.
7. Mostrale que quedo cambiado.

**No hagas el commit vos.** El script le pregunta al final si sube los cambios.

## Ojo

- Publicar es la unica accion de todo el sistema que es visible para el mundo en
  minutos. Si algo no te cierra, decilo aunque Horacio ya haya dicho que si.
- Si aparece un error despues de publicar, la correccion es publica: se corrige
  la nota y la correccion queda visible en la propia pagina, con fecha
  (NEWSROOM.md, marco legal, punto 8).
