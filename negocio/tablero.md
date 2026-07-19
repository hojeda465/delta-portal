# Con Interés · Tablero de números (vivo)

> Lo mantiene **Finanzas / «Cuentas»**. Este es el único registro de plata que sobrevive
> entre comités. Cada rubro está marcado como **[DATO]** (medido de verdad) o
> **[SUPUESTO]** (estimación de arranque, sin validar). La regla: no confundir uno con otro.

- **Creado:** 2026-07-19 (primer comité, primera versión del tablero)
- **Última actualización:** 2026-07-19
- **Estado general:** bootstrap puro · ingresos = 0 · costos NO medidos con datos reales todavía

---

## 1. Costos (mensuales)

| Rubro | Monto | Tipo | Nota |
|---|---|---|---|
| Tokens de IA — redacción (notas) | ~US$1–2 por nota | **[SUPUESTO]** | costo marginal del estatuto; sin factura real cruzada |
| Tokens de IA — redacción (lecciones) | ~US$2–8 por lección | **[SUPUESTO]** | ídem |
| Tokens de IA — este comité | s/d | **[SUPUESTO]** | 3 gerencias + síntesis por corrida semanal; no medido |
| Dominio coninteres.com | ~US$10–15 / año (~US$1/mes) | **[SUPUESTO]** | confirmar con el registrador |
| Hosting (GitHub Pages) | US$0 | **[DATO]** | sitio estático, plan gratis |
| Herramientas | US$0 conocidas | **[SUPUESTO]** | revisar si hay suscripciones activas |
| **Total mensual estimado** | **~US$350–800** | **[SUPUESTO]** | banda de arranque del estatuto, NO medida |

## 2. Producción a la fecha (2026-07-19)

| Ítem | Cantidad | Fuente |
|---|---|---|
| Notas publicadas | 10 | **[DATO]** carpeta `articulos/` |
| Lecciones publicadas | 8 | **[DATO]** carpeta `lecciones/` |
| Cadencia observada de notas | ~5–6 notas/día (lote 18–19 jul) | **[DATO]** fechas de archivos |
| Proyección de notas/mes a esa cadencia | ~150–180 | **[SUPUESTO]** (extrapola la cadencia) |

### Costo marginal implícito acumulado (estimado, NO medido)
- Notas: 10 × US$1–2 = **US$10–20**
- Lecciones: 8 × US$2–8 = **US$16–64**
- **Total gastado hasta hoy (estimación): ~US$26–84** — sin dato de factura real.
- ⚠️ A cadencia ~5 notas/día, solo las notas proyectan **~US$150–360/mes** en tokens marginales.

## 3. Ingresos

| Línea | Estado | Monto |
|---|---|---|
| Membresía B2C (Modo Aprendizaje) | no lanzada | US$0 **[DATO]** |
| Afiliados / display | no activo | US$0 **[DATO]** |
| Licenciamiento B2B | no activo | US$0 **[DATO]** |
| **Total ingresos** | — | **US$0** **[DATO]** |

## 4. Unit economics / punto de equilibrio

| Métrica | Valor | Tipo |
|---|---|---|
| Punto de equilibrio | ~100 miembros × US$4/mes = US$400/mes | **[SUPUESTO]** |
| Miembros actuales | 0 | **[DATO]** |
| LTV / CAC | s/d (sin embudo) | **[SUPUESTO]** — no medir publicidad paga hasta tenerlo |
| Runway | s/d — sin caja declarada ni tope de gasto | **[SUPUESTO]** |

## 5. Fiscal

| Ítem | Valor | Tipo |
|---|---|---|
| Régimen | Monotributo | **[SUPUESTO]** |
| Categoría | Cat A (inicial estimada) | **[SUPUESTO]** — confirmar alta/categoría real |

## 6. Kill-switch de costos (PENDIENTE — requiere decisión de Horacio)

| Control | Estado |
|---|---|
| Tope de gasto mensual de tokens (US$/mes) | ❌ **NO DEFINIDO** — riesgo abierto |
| Cascada de modelos (barato p/ tareas simples) | ❌ no definida |
| Frecuencia máxima de corridas de redacción | ❌ no declarada (hoy ~5–6 notas/día) |
| Alerta de gasto / medición real de tokens | ❌ nadie mide con datos reales |

---

## 7. Datos a conseguir (para pasar [SUPUESTO] → [DATO])
1. **Gasto real de tokens** del mes (factura/consumo del proveedor de API). ← prioridad 1
2. Costo real del dominio (registrador, vencimiento).
3. Tope mensual de gasto que fija Horacio.
4. Categoría de monotributo confirmada.
5. Costo de tokens por corrida del comité.
