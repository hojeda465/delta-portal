# ▽ Delta — Portal de datos con redacción de agentes de IA

Diario digital argentino donde **una redacción de agentes de IA** rastrea las
noticias más destacadas, hace foco en los datos y el contexto, **verifica** cada
cifra y publica notas con profundidad — cada hora, con aprobación humana antes de
salir al aire.

- **Concepto e identidad:** ver el documento de concepto (marca, método, secciones).
- **Cómo trabajan los agentes:** [`agente/NEWSROOM.md`](agente/NEWSROOM.md) — el runbook operativo de los 6 agentes.
- **Nota de referencia:** [`articulos/2026-07-18-inflacion-argentina.html`](articulos/2026-07-18-inflacion-argentina.html)

## Cómo funciona

```
cada hora:  Rastreador → Editor → Investigador → Verificador → Redactor → Publicador
            → deja un BORRADOR en la cola de revisión (no publica solo)
vos:        aprobás con un mensaje → la nota se publica en la portada
```

La portada (`index.html`) **se genera sola** desde los manifiestos de `data/`.
Nunca se edita a mano.

```bash
python3 scripts/build_portada.py   # regenera index.html
```

## Estructura

```
index.html              portada (generada)
articulos/              notas publicadas
cola/                   borradores esperando aprobación
assets/                 estilos y componentes de gráficos
data/                   manifiestos JSON (fuente de verdad)
agente/                 NEWSROOM.md + plantilla de nota
scripts/                build_portada.py
```

## Puesta en marcha (una sola vez)

1. **Crear el repo en GitHub** y subir esta carpeta.
2. **Activar GitHub Pages** (Settings → Pages → rama `main`, carpeta raíz).
   El portal queda en `https://<usuario>.github.io/<repo>/`.
3. **Programar la tarea horaria** que corre la redacción (pega el prompt de la
   sección 7 de `NEWSROOM.md`). Deja borradores en la cola.
4. **Revisar y aprobar**: cuando llega el aviso, abrís el borrador y le decís a
   Delta "aprobá la nota `<id>`".

## Estado

Prototipo editorial. Modo **cola de revisión** (aprobación humana antes de
publicar). Frecuencia: cada 1 hora (nativa de Cowork). Próximo paso opcional:
infraestructura propia para bajar a cada 30 min.

---
*Delta — La noticia, medida.*
