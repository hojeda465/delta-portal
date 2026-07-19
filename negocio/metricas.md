# Con Interés · Tablero de crecimiento (métricas de tráfico e interés)

> Lo mantiene **Marketing / «Alcance»** con overlay de **Finanzas / «Cuentas»**.
> Nace de la decisión de Horacio (2026-07-19): **la prioridad es crecer en cantidad
> de lectores y demostrar interés, no monetizar.** Este documento define *qué* medimos
> para saber si ese objetivo se está cumpliendo.
>
> - **Creado:** 2026-07-19
> - **Estado:** marco definido · **medición todavía NO instalada** (el sitio no tiene
>   ninguna analítica hoy). Todos los valores arrancan en `s/d` hasta el go-live.

---

## Regla de oro

**Volumen sin interés es vanidad.** Se reporta SIEMPRE la columna de volumen junto a la
de interés/calidad. Cien mil visitas que rebotan no son "muestra contundente de interés";
mil lectores que vuelven y leen hasta el final, sí. Por eso el tablero tiene tres bloques
y ninguno se lee solo.

---

## Bloque A — VOLUMEN (¿cuánta gente llega?)

| # | KPI | Qué mide | Objetivo / dirección | Valor actual |
|---|---|---|---|---|
| A1 | **Visitantes únicos / semana** | usuarios distintos | crecer semana a semana (sano en etapa cero: +15–30% mensual desde base baja) | s/d |
| A2 | **Pageviews / semana** | consumo total | crecer; y que pageviews ÷ únicos > 1 | s/d |
| A3 | **Fuentes de tráfico** (orgánico/SEO · directo · social · referral) | de dónde viene | que el **orgánico** pase de ~0 a canal con tendencia positiva a 90 días | s/d |
| A4 | **Impresiones y clicks en búsqueda** (Search Console) | visibilidad en Google | impresiones ↑, CTR ↑, posición media ↓ (mejor) | s/d |

> El tráfico **orgánico creciente** es la señal más fiable y escalable de interés real:
> no depende de que nosotros empujemos, es la gente que nos busca.

## Bloque B — INTERÉS / CALIDAD (¿les importó?)

| # | KPI | Qué mide | Objetivo indicativo | Valor actual |
|---|---|---|---|---|
| B1 | **Tiempo de lectura por nota** | permanencia real | > 60–90 s, tendencia ↑ | s/d |
| B2 | **Profundidad de scroll** (% que llega al 75–100%) | cuánto del artículo consumen | > 40% llega al final | s/d |
| B3 | **Páginas por sesión** | ¿siguen leyendo otra cosa? | > 1,3 | s/d |
| B4 | **% que entra al Modo Aprendizaje** (click nota → lección) | interés en el producto educativo (métrica-firma) | definir baseline, luego ↑ | s/d |
| B5 | **Tasa de finalización de lecciones** | quién completa una secuencia (= futuro miembro) | baseline, luego ↑ | s/d |
| B6 | **Visitantes recurrentes** (% que vuelve en 30 días) | la métrica reina de "medio de interés" | > 10% recurrentes = señal fuerte | s/d |
| B7 | **Compartidos / backlinks** | señal social y de SEO | tendencia ↑ (proxy: referral + links en Search Console) | s/d |

> B4, B5 y B6 son las que unen "tráfico" con "esto algún día se puede cobrar": tráfico
> que entra a aprender y que vuelve es tráfico monetizable a futuro. Se miden ahora,
> gratis, sin activar ningún cobro.

## Bloque C — EFICIENCIA / COSTO DE CRECER (overlay de Finanzas)

Para que "crecer" no sea "gastar a ciegas". El costo **no escala con ingresos (=0), escala
con la producción**: cada nota cuesta tokens la lea alguien o no. Estas métricas vigilan que
crezcamos en lectores por peso gastado, no en notas publicadas.

| # | KPI | Cómo se calcula | Estado |
|---|---|---|---|
| C1 | **Gasto de tokens / mes vs. tope** | US$ del mes ÷ tope fijado | tope ❌ no definido; gasto [SUPUESTO] |
| C2 | **Costo por artículo publicado** | US$ tokens del mes ÷ piezas publicadas | estimable en banda (~US$1–2 nota, US$2–8 lección) |
| C3 | **US$ por lector nuevo ganado** | US$ tokens del mes ÷ visitantes únicos nuevos | ⭐ la métrica que une costo y crecimiento — requiere analítica |
| C4 | **Costo por suscriptor** (si/cuando haya email) | US$ tokens ÷ altas de email | N/A hoy, definido para el futuro |

> **C3 es la brújula:** si baja mes a mes, crecemos con eficiencia; si sube, estamos
> "comprando" lectores caros produciendo de más.

---

## Cómo se mide (sitio estático GitHub Pages · gratis · sin cookies)

Orden de instalación recomendado por Marketing:

1. **Google Search Console** — primero, gratis, sin fricción. Única fuente de verdad de
   SEO (queries, impresiones, clicks, posición). Cubre A3 (orgánico) y A4. Requiere
   **verificar el dominio** (meta-tag o DNS).
2. **Cloudflare Web Analytics** — gratis, sin cookies, sin banner de consentimiento. Da
   únicos, pageviews, fuentes, países (A1, A2, A3). **Confirmado (2026-07-19): el dominio
   coninteres.com YA está detrás de Cloudflare** (resuelve a IPs 172.67.x / 104.21.x), así
   que se activa desde la misma cuenta de Cloudflare, sin tocar DNS ni usar fallback. (El
   fallback GoatCounter queda descartado salvo que se pierda el acceso a Cloudflare.)
3. **Eventos custom (JS propio, ~15 líneas)** para B1, B2, B4, B5: listeners de scroll
   (25/50/75/100%), tiempo en página, y click a lecciones. Se envían al mismo proveedor
   de analítica como eventos. Scaffold ya preparado en `assets/metrics.js` (pendiente de
   activar con el código de sitio del proveedor).

Todo es privacy-friendly: **sin cookies, sin banners molestos, sin Google Analytics**.
Coherente con "confianza primero".

---

## Cadencia de reporte

- **Semanal**, en cada comité. La primera semana con datos = línea base (baseline),
  aunque varios KPIs arranquen cerca de cero.
- Cada comité: actualizar valores, marcar qué pasó de `s/d` a dato, y leer volumen +
  interés juntos antes de sacar conclusiones.

---

## Sobre el email (aclaración de encuadre)

Las tres gerencias coinciden: **la captura de email NO es monetización, es un canal de
crecimiento y retorno.** Un suscriptor es tráfico recurrente voluntario (la forma más
pura de "muestra contundente de interés") y el único canal propio para traer lectores de
vuelta sin depender del algoritmo de Google o de redes. Bajo la estrategia de "crecer
primero" **se mantiene la idea, reencuadrada como herramienta de tráfico**, pero su
*ejecución se difiere* ~4–6 semanas: primero instalamos la medición y confirmamos que hay
tráfico y retención que valga la pena capturar. No se vende nada a nadie; jamás.
