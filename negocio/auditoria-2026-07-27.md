# Auditoría semanal — Con Interés
**Fecha del informe:** 2026-07-27 · **Ventana auditada:** notas publicadas del lunes 2026-07-20 al domingo 2026-07-26 (inclusive) · **Notas revisadas:** 49

Metodología: para cada nota se releyó el HTML publicado y se extrajeron la cifra ancla, los superlativos y las URLs de "Fuentes y transparencia". Cada cifra ancla se contrastó contra al menos dos fuentes independientes reales (INDEC, BCRA, organismos oficiales, prensa económica con reportería propia) con **postura de refutación**: se buscó activamente el dato que la contradijera, no solo su confirmación. Se verificó que cada URL citada resolviera y respaldara efectivamente el dato que acompaña (atención especial a URLs con patrón de fecha tipo `nid<DDMMAAAA>`), que todo superlativo ("récord", "primer", "máximo", "el mayor/menor desde…") tuviera su valor previo documentado con fuente, y la coherencia interna copete ↔ gráfico ↔ cuerpo ↔ entrada de manifiesto.

> Nota de proceso: en varias notas se hallaron URLs de La Nación / medios con slugs tipo `nid<fecha>`, marcadas como "sospechosas por diseño" en el protocolo. En **todos los casos verificados esta semana** esas URLs resultaron ser reales (no fabricadas por patrón) — es simplemente el esquema de URLs que usan esos medios. No se detectó ninguna URL inventada por patrón de fecha en este lote.

---

## Scorecard global

| Veredicto | Cantidad |
|---|---|
| CONFIRMADO | 27 |
| IMPRECISO | 20 |
| DISCREPANCIA | 2 |
| NO_VERIFICABLE | 0 |
| **Total** | **49** |

**Hallazgos graves (URGENTE — revisión humana inmediata):** 2
1. `2026-07-20-carne-vacuna-consumo-minimo-record-exportacion` — el superlativo del propio titular/copete ("mínimo en dos décadas") es contradicho por la fuente que la nota misma cita.
2. `2026-07-20-ia-no-reemplaza-oficios` — una cifra que sostiene la tesis central ("71% de complementariedad, no reemplazo") no tiene respaldo documental verificable en ninguna fuente de la OIT ni en cobertura independiente.

Ninguna otra nota presenta cifra ancla o tesis central falsa. El resto de los hallazgos (18 IMPRECISO adicionales + 1 DISCREPANCIA no urgente) son de segundo orden: URLs de respaldo que resuelven pero no corresponden al dato citado (mes/año equivocado, o documento equivocado), matices de redondeo, superlativos correctos pero con un dato de contexto secundario sin fuente, o datos macro de contexto desactualizados a la fecha de publicación.

---

## Detalle por nota

### 2026-07-20 · lote inicial de la semana

**`2026-07-20-mora-familias-record`** — **IMPRECISO**
Cifra ancla (12,1% de mora de crédito a familias, abril 2026, récord desde 2004) confirmada contra el BCRA + Infobae + Puntal. Pero dos URLs del pie de fuentes (Perfil, Ámbito) en realidad corresponden a datos de meses distintos (dic-2025 y feb-2026), no al mes ancla de abril. *Corrección:* reemplazar esos enlaces por cobertura específica de abril 2026.

**`2026-07-20-corralones-construccion-buenos-aires`** — **CONFIRMADO**
ISAC-INDEC +4,1% i.a. de mayo y caída de venta de materiales, verificados contra el PDF oficial y 6 medios independientes. Sin correcciones necesarias (sugerencia menor: sumar fuente textual para "tercer mes consecutivo" del cemento).

**`2026-07-20-ia-no-reemplaza-oficios`** — **IMPRECISO / URGENTE (parcial)**
La cifra ancla (3,3% del empleo mundial en máxima exposición a IA, OIT WP140) y los datos de apoyo (FMI, Banco Mundial, BLS, Min. Economía) están confirmados. **Pero el "71% de complementariedad, no reemplazo" que sostiene la tesis central de la nota no se encontró en ningún documento de la OIT ni en cobertura independiente** — parece una cifra sin fuente real. *Acción:* remover esa cifra o sustituirla por una atribución verificable; marcado para revisión humana porque sostiene el argumento central del artículo.

**`2026-07-20-bono-jubilados-congelado`** — **IMPRECISO**
El congelamiento del bono ANSES desde marzo 2024 y los montos de julio 2026 están confirmados (Chequeado + Ámbito). Pero la cifra "$157.341 / pérdida real 55,5%" se atribuye a Infobae cuando en realidad es una estimación de Chequeado — la nota mezcla cifras de dos fuentes distintas presentándolas como una sola. *Corrección:* atribuir correctamente o presentar ambas estimaciones (Chequeado vs. ODSA) como rango.

**`2026-07-20-deuda-publica-dos-lecturas`** — **CONFIRMADO**
Deuda bruta US$474.192 M (jun-2026) y su comparación con el récord de marzo verificadas en su totalidad, incluida una URL con patrón `nid<fecha>` que resultó real. Sin correcciones.

**`2026-07-20-carne-vacuna-consumo-minimo-record-exportacion`** — **DISCREPANCIA / URGENTE**
La nota afirma que 47,5 kg de consumo de carne vacuna per cápita en 2026 es "el mínimo en unas dos décadas". **La propia fuente citada por la nota (CREEBBA) declara textualmente que el punto más bajo de toda la serie 1990–2025 fue 43,2 kg/hab en el 1er trimestre de 2024** — un valor menor, ocurrido apenas dos años antes. El superlativo del titular es contradicho por su propia fuente: exactamente el patrón de error que motivó la regla de "superlativo con historia" tras el caso del déficit primario. *Acción recomendada:* aplicar caja de "△ Corrección" pública (superlativo impreciso: corregir a "mínimo anual en dos décadas", aclarando que hubo un piso trimestral aún más bajo en 2024 según la misma fuente), o degradar/eliminar el superlativo. Se marca URGENTE para revisión humana inmediata.

**`2026-07-20-pagos-qr-superan-100-millones`** — **CONFIRMADO**
102,5 M pagos QR en mayo (+66,1% i.a.), "primera vez sobre 100 M" verificado contra los informes del BCRA de dic-2025 a may-2026 (diciembre, el mes más estacional, dio 95 M — por debajo de 100 M). Sin correcciones necesarias.

**`2026-07-20-ventas-pyme-cortan-caida`** — **IMPRECISO**
+0,9% i.a. en ventas pyme (CAME, junio), primera suba en 13 meses: confirmado por 6+ medios independientes y el dato de contraste INDEC. La URL #1 de CAME resuelve pero es una página metodológica genérica, no el informe con los datos de junio. *Corrección:* reemplazar por el informe/nota de prensa específico.

**`2026-07-20-salario-real-abril`** — **CONFIRMADO**
Índice de salarios INDEC +3,7% mensual (abril) vs. IPC 2,6%, con desagregado por sector, verificado exacto contra los PDF oficiales del INDEC y RIPTE. Sin hallazgos.

**`2026-07-20-soja-mercado-seis-meses`** — **IMPRECISO**
Precio ancla (US$12,15/bushel, 20-jul) plausible por triangulación de trayectoria; datos de Brasil, aranceles China-EE.UU. y Fed confirmados exactos. Dos imprecisiones: producción mundial "~427 Mt" (el dato real de USDA es 425,8 Mt) y el dato de contexto de petróleo Brent ("~US$71, -38% desde abril") quedó desactualizado — el día de publicación (20-jul) el Brent ya cotizaba ~US$88 y escaló por encima de US$100 días después por ataques hutíes en el Mar Rojo. *Corrección:* actualizar el dato de Brent a la fecha de publicación y ajustar la cifra de producción mundial a ~426 Mt.

**`2026-07-20-inflacion-mayorista-junio`** — **CONFIRMADO**
IPIM +1,1% (junio), menor suba en 4 meses, confirmado por 8+ medios independientes y contraste directo contra junios 2020-2025 (todos muy superiores a 1,1%). Sin hallazgos.

### 2026-07-21

**`2026-07-21-rigi-pampa-4521-millones`** — **CONFIRMADO**
Resolución 1025/2026 del Boletín Oficial (fuente primaria) confirma el monto US$4.521 M y el proyecto n.º 20 del RIGI. Sugerencia menor: aclarar que el total acumulado del RIGI (~US$46.000-57.000 M) es aproximado, no una suma exacta reconciliable entre medios.

**`2026-07-21-record-gas-neuquen-gnl`** — **CONFIRMADO**
115,14 MMm³/d en mayo (récord histórico, supera el pico de jul-2025 de 114,51) confirmado por dos fuentes independientes. Sugerencia menor: sumar un link directo a OLADE para el dato de participación regional.

**`2026-07-21-cheques-rechazados-cadena-pagos`** — **DISCREPANCIA**
La cifra ancla (99.431 cheques rechazados, mayo, BCRA) está confirmada. Pero la URL del BCRA citada como fuente #1 corresponde al informe de **abril**, no de mayo — el link que respalda el dato ancla apunta al informe equivocado. Además, el superlativo "récord histórico" para diciembre 2025 no está sustentado por ninguna fuente citada (solo se compara contra 2025, no contra series largas 2001-02/2018-19/2020); un año antes, otro medio ya había calificado de "récord histórico" a un valor menor. *Corrección (no urgente, la cifra ancla es correcta):* reemplazar la URL por el informe de mayo y degradar "récord histórico" a "el mayor valor de la serie reciente/desde 2025".

**`2026-07-21-credito-privado-rebota-empresas`** — **CONFIRMADO**
+1,7% real del crédito privado en junio, primera suba en 6 meses, y los tres superlativos de apoyo confirmados de forma independiente. Sin hallazgos graves.

**`2026-07-21-compras-courier-se-duplican`** — **IMPRECISO**
US$643 M por courier en 1S2026 (+104,2% i.a.) confirmado contra el PDF oficial ICA-INDEC y 10+ medios. Dos URLs del pie no respaldan directamente el dato (INDEC apunta a sección genérica; ON24 cubre solo 5 de 6 meses). *Corrección:* reemplazar ambos enlaces por las fuentes específicas.

**`2026-07-21-empleo-registrado-abril-anatomia`** — **IMPRECISO**
-28.736 empleos SIPA (abril) confirmado, pero la suma de las categorías del propio gráfico da -28.781 (no -28.736); una fuente independiente da +2.861 para el sector público en vez de +2.816, valor que si se usa cierra la cuenta exacta — sugiere un error de transcripción. Además, la nota presenta "28 mil" y "30 mil" como categorías distintas cuando en realidad son el mismo dato con redondeo distinto. *Corrección:* verificar +2.816 vs +2.861 contra el PDF original del SIPA y reformular la explicación de categorías.

**`2026-07-21-monotributo-como-cambio`** — **CONFIRMADO**
Tope categoría K ($126,6M desde agosto) y toda la serie histórica 2024-2026 confirmadas exacto por dos fuentes independientes. Sin hallazgos.

**`2026-07-21-boom-motos-caen-autos`** — **CONFIRMADO**
+43,5% patentamiento de motos / -10% autos 0km (1S2026) confirmado por fuentes independientes entre sí. Nota curiosa: la fuente primaria tiene una errata en su propio título ("433.000" vs "443.000" en el cuerpo) y Con Interés usó correctamente el dato del cuerpo.

### 2026-07-22

**`2026-07-22-swap-china-repago-renovacion`** — **IMPRECISO**
Swap con China, vencimiento y reservas confirmados por 3+ fuentes. Pero "casi 9 de cada 10 dólares" (90% de repago) sobrestima: el repago real ronda 78%-87% según el BCRA/Ámbito, nunca 90%. *Corrección:* cambiar a "más del 85%" o precisar el rango real.

**`2026-07-22-emae-actividad-mayo-freno`** — **IMPRECISO**
EMAE -0,5% (mayo) confirmado exacto contra el INDEC. La URL de INDEC citada corresponde al informe de abril, no de mayo (aunque el dato usado en el texto sí es el correcto). *Corrección:* reemplazar el link por el PDF de mayo.

**`2026-07-22-distribucion-ingreso-desigualdad`** — **CONFIRMADO**
33,5% del ingreso para el decil 10 y Gini 0,442 (1T2026) confirmados exacto contra el PDF de INDEC y dos medios independientes; la nota acierta al no llamarlo "récord" (el máximo de la serie, según Chequeado, fue 0,467 en 2024). Sin hallazgos.

**`2026-07-22-riesgo-pais-cerca-400`** — **IMPRECISO**
410 pb (22-jul) y "mínimo desde 2018" confirmados por 8+ medios. Pero dos cifras de un gráfico secundario (costo de financiamiento Banco Mundial 6,3% / BID 7,75%) se atribuyen a una fuente que no las contiene. *Corrección:* re-sourcear o retirar esas dos cifras.

**`2026-07-22-autos-usados-junio-mejor-mes`** — **IMPRECISO**
155.492 usados vendidos en junio confirmado por 3 fuentes independientes. Único problema: la URL de Tiempo Argentino da error 500. *Corrección:* reemplazar el enlace caído.

**`2026-07-22-rem-bcra-dolar-proyeccion`** — **IMPRECISO**
$1.673 proyectado para dic-2026 (REM/BCRA) confirmado. Se detectó una fecha mal atribuida: la nota dice que el récord del dólar minorista ($1.515) fue el 15/07, pero según su propia fuente fue el 07/07 (el 15/07 corresponde al récord del blue). *Corrección:* corregir la fecha.

**`2026-07-22-turismo-receptivo-se-da-vuelta`** — **CONFIRMADO**
+20,4% turistas extranjeros (mayo, INDEC-ETI) y -12,1% turistas argentinos confirmados exacto contra el PDF oficial y 5+ medios. Sin hallazgos.

**`2026-07-22-superavit-semestre-record-exportaciones`** — **CONFIRMADO**
US$13.923 M de superávit comercial (1S2026) confirmado por 4 fuentes independientes; el superlativo acotado ("el mayor... desde 2024") se sostiene con los datos de 2024/2025 verificados. Sin hallazgos graves.

**`2026-07-22-vino-mas-litros-menos-dolares`** — **IMPRECISO**
+14,2% en volumen / +2,6% en valor (1S2026) confirmado exacto contra el INV e Infobae. Tres problemas menores: una URL (Sitio Andino) cubre un mes distinto al citado; el dato de consumo mundial de vino de la OIV mezcla el año 2024 con la etiqueta 2025; y no se pudo verificar la cita atribuida a Magdalena Pesce. *Corrección:* ajustar la URL, corregir el dato de la OIV y verificar o retirar la cita.

### 2026-07-22 (continuación) / 2026-07-23

**`2026-07-22-moodys-sube-calificacion-b3`** — **CONFIRMADO**
Upgrade de Caa1 a B3 (21-jul) y la serie de riesgo país confirmados por 7 medios independientes. Sugerencia menor: falta una URL puntual para el dato de 418 pb del 21-jul.

**`2026-07-22-consumo-supermercados-en-rojo`** — **CONFIRMADO**
-3,7% i.a. en ventas de supermercados (abril, INDEC), cuarto mes en baja, confirmado palabra por palabra contra el PDF oficial. Sin hallazgos.

**`2026-07-22-produccion-leche-record-decada`** — **CONFIRMADO**
11.617 M litros en 2025 (+9,7%), "mayor volumen en una década", confirmado por el comunicado oficial y prensa independiente. Sugerencia menor: falta una cifra concreta de 2015 para completar el respaldo del superlativo "segundo mejor año".

**`2026-07-22-record-petroleo-900-mil-barriles`** — **CONFIRMADO**
903.700 barriles/día (mayo, récord histórico) es el superlativo mejor documentado del lote: ambos valores previos (847.000 de 1998 y 859.500 de oct-2025) están confirmados con fuente. Sin hallazgos.

**`2026-07-22-pbi-crece-inversion-cae`** — **CONFIRMADO**
PBI +2,3% i.a. (1T2026) e inversión -11,6%, con las siete variaciones sectoriales, confirmadas exactas contra Chequeado. Sin hallazgos.

**`2026-07-22-despachos-cemento-tercer-mes-baja`** — **CONFIRMADO**
-1,4% i.a. en despachos de cemento (junio) confirmado exacto por fuente independiente. La URL de la AFCP resuelve pero no muestra el dato sin un clic adicional (cosmético, no bloqueante).

**`2026-07-23-prepagas-cobertura-salud`** — **IMPRECISO**
La tendencia (67,5%→65,4% de cobertura privada, 2S2023-2S2025) está confirmada en su tramo intermedio contra el PDF del INDEC, pero el dato final puntual (742.000/65,4%) es un cálculo del Instituto Argentina Grande (IAG), no un dato directo de INDEC — la nota lo aclara en el cuerpo, pero el manifiesto lo atribuye a "INDEC" sin esa salvedad. Además, el "+417% en dos años" de la cuota en realidad cubre ~30 meses, no 24. *Corrección:* reatribuir el dato en el manifiesto al IAG y precisar el plazo real del +417%.

**`2026-07-23-combustibles-mayo-freno-caida`** — **CONFIRMADO**
-0,2% i.a. en venta de combustibles (mayo), "menor caída de 2026", confirmado por 3 fuentes independientes y contraste contra todos los meses de 2026. Sin hallazgos.

**`2026-07-23-globant-accion-desplome-90`** — **CONFIRMADO**
Caída de ~91% desde el máximo histórico (US$354,44, nov-2021) confirmada exacta contra tres fuentes financieras independientes. El superlativo "valores de 2017" también se confirmó con precisión. Sin hallazgos.

**`2026-07-23-brecha-cambiaria-dolar-blue`** — **CONFIRMADO**
Dólar blue en $1.555 (récord nominal, 22-jul) y evolución de la brecha confirmados por 5 fuentes independientes. Sin hallazgos.

**`2026-07-23-fci-record-money-market`** — **CONFIRMADO**
Patrimonio récord de FCI (~US$67.500 M, junio) confirmado por CAFCI, El Cronista e Infobae/PPI. Sugerencia menor: agregar cita puntual para dos porcentajes intermedios de participación del money market.

**`2026-07-23-produccion-acero-junio`** — **IMPRECISO**
320.100 t (junio, -8,6% mensual/+16,5% i.a.) confirmado por fuentes independientes y World Steel Association. Dos datos de contexto histórico no coinciden con la propia serie oficial de la Cámara Argentina del Acero: "cayó 26%" en 2024 (la serie real da -21,6%) y "~463.600 t" para junio 2022 (la cifra real es 422.900 t). *Corrección:* ajustar ambos valores contra la serie histórica que la propia nota ya usa como fuente.

**`2026-07-23-confianza-consumidor-dos-argentinas`** — **CONFIRMADO**
ICC UTDT 40,67 puntos (julio, -4,8%) y la brecha entre ingresos bajos y altos confirmados exacto por dos fuentes independientes. Sin hallazgos.

**`2026-07-23-metalurgia-capacidad-instalada`** — **IMPRECISO**
40,8% de uso de capacidad instalada (junio, ADIMRA) confirmado por 3 medios independientes. Pero el PDF de INDEC citado como fuente es el informe de Producción Industrial Manufacturero, no el de "Utilización de la capacidad instalada" que contiene las cifras atribuidas (38,7%/58,4%/75,4%); además una fuente rotulada "INDEC" en realidad enlaza a un artículo de Infobae. *Corrección:* reemplazar el PDF por el informe correcto y corregir la atribución.

### 2026-07-23 (continuación) / 2026-07-24

**`2026-07-23-super-peso-tipo-cambio-real`** — **IMPRECISO**
ITCRM en 84,6 puntos (abril, "más apreciado desde 2017") confirmado por 4 fuentes independientes. La URL de la Bolsa de Comercio de Rosario resuelve pero es un informe de 2018, no respalda el dato de 2026. *Corrección:* reemplazar por un informe actualizado de la BCR.

**`2026-07-23-cuenta-corriente-deficit-primer-trimestre`** — **CONFIRMADO**
Déficit de cuenta corriente de US$1.651 M (1T2026) confirmado exacto contra el PDF oficial del INDEC, con aritmética verificada de los cuatro componentes. Sin hallazgos.

**`2026-07-23-cerdo-consumo-record`** — **CONFIRMADO**
19,59 kg per cápita (récord histórico, SAGyP) confirmado por 5 medios independientes, con el valor previo (18,9 kg, 2025) también corroborado. Sin hallazgos.

**`2026-07-23-mundial-tv-boom-electrodomesticos`** — **IMPRECISO**
+27% en ventas de TV (ene-may, NielsenIQ) confirmado, aunque las dos fuentes citadas derivan del mismo informe. La nota no menciona que la propia encuesta oficial del INDEC midió una caída de TV del 1,4% i.a. en el 1er trimestre (antes del repunte previo al Mundial), lo que contextualizaría mejor el "boom". *Corrección:* agregar esa aclaración y reemplazar el link genérico de INDEC.

**`2026-07-23-agro-liquidacion-dolares-semestre`** — **CONFIRMADO**
US$13.378 M liquidados por el agro (1S2026, CIARA-CEC) confirmado por 4 fuentes independientes, con aritmética verificada. Sin hallazgos graves.

**`2026-07-24-record-pasajeros-avion`** — **IMPRECISO**
24,57 M pasajeros (1S2026, ANAC) confirmado por 5 fuentes que derivan del mismo comunicado oficial, sin contradicciones. La frase "desde que existen registros" es una caracterización de la propia ANAC, bien atribuida, pero no está verificada contra series pre-2020. *Corrección:* matizar a "el semestre más alto desde que ANAC compara esta serie (2023-2026)".

**`2026-07-24-deuda-externa-record-321-mil-millones`** — **IMPRECISO**
US$321.783 M (31-mar-2026, INDEC), "mayor stock de la serie", confirmado exacto contra los PDF oficiales; ningún trimestre desde 1994 lo supera. Dos matices: el superlativo omite la acotación "serie iniciada en 1994" (que sí usan medios competidores) y la nota no aclara que el valor de IV-2025 usado es una cifra ya revisada, distinta de la preliminar publicada en marzo. *Corrección:* agregar la acotación de la serie y aclarar la revisión estadística.

---

## Lista priorizada de correcciones

**Prioridad 1 — URGENTE (revisión humana inmediata, posible corrección pública o cola):**
1. `2026-07-20-carne-vacuna-consumo-minimo-record-exportacion` — el superlativo del titular ("mínimo en dos décadas") es contradicho por la propia fuente citada (CREEBBA: 43,2 kg en Q1 2024). Aplicar caja "△ Corrección" o degradar el superlativo a "mínimo anual en dos décadas".
2. `2026-07-20-ia-no-reemplaza-oficios` — la cifra "71% de complementariedad" que sostiene la tesis central no tiene fuente verificable. Retirarla o sustentarla con atribución real.

**Prioridad 2 — discrepancia no urgente (cifra ancla correcta, pero superlativo/fuente mal sustentados):**
3. `2026-07-21-cheques-rechazados-cadena-pagos` — reemplazar la URL del BCRA (apunta al informe de abril, no mayo) y degradar "récord histórico" a una comparación verificable.

**Prioridad 3 — correcciones de fuente/atribución (no urgentes, no afectan la cifra ancla ni la tesis):**
4. `mora-familias-record` — reemplazar 2 URLs que no corresponden al mes ancla.
5. `bono-jubilados-congelado` — corregir atribución de la cifra $157.341/55,5% (es de Chequeado, no de Infobae).
6. `ventas-pyme-cortan-caida` — reemplazar URL genérica de CAME.
7. `soja-mercado-seis-meses` — actualizar dato de Brent a la fecha de publicación y ajustar producción mundial a ~426 Mt.
8. `compras-courier-se-duplican` — reemplazar 2 URLs (INDEC genérica, ON24 parcial).
9. `empleo-registrado-abril-anatomia` — verificar +2.816 vs +2.861 (sector público) contra el PDF del SIPA; reformular explicación de categorías.
10. `swap-china-repago-renovacion` — corregir "casi 90%" a "más del 85%".
11. `emae-actividad-mayo-freno` — reemplazar URL de INDEC (apunta a abril, no mayo).
12. `riesgo-pais-cerca-400` — re-sourcear o retirar cifras de Banco Mundial/BID no respaldadas.
13. `autos-usados-junio-mejor-mes` — reemplazar URL caída de Tiempo Argentino (error 500).
14. `rem-bcra-dolar-proyeccion` — corregir fecha del récord del dólar minorista (07/07, no 15/07).
15. `vino-mas-litros-menos-dolares` — corregir dato de la OIV (año) y verificar/retirar cita de Magdalena Pesce.
16. `prepagas-cobertura-salud` — reatribuir 742.000/65,4% al IAG en el manifiesto; precisar plazo del +417%.
17. `produccion-acero-junio` — corregir "cayó 26%" (real: -21,6%) y "~463.600 t" (real: 422.900 t) para 2022.
18. `metalurgia-capacidad-instalada` — reemplazar PDF de INDEC citado por el informe correcto de capacidad instalada; corregir atribución.
19. `super-peso-tipo-cambio-real` — reemplazar URL de BCR Rosario (informe de 2018, no de 2026).
20. `mundial-tv-boom-electrodomesticos` — agregar aclaración sobre la caída de TV medida por INDEC en el 1T2026.
21. `record-pasajeros-avion` — matizar "desde que existen registros" (no verificado contra series pre-2020).
22. `deuda-externa-record-321-mil-millones` — agregar acotación "serie iniciada en 1994" y aclarar revisión estadística del dato de IV-2025.

**Sugerencias cosméticas (no requieren acción prioritaria):** corralones-construcción (fuente para "tercer mes" de cemento), rigi-pampa (aclarar aproximación del total RIGI), record-gas-neuquén (link directo a OLADE), moodys (URL puntual para 418 pb), producción-leche (cifra de 2015), despachos-cemento (AFCP requiere un clic extra), fci-record-money-market (fuente para dos porcentajes intermedios), cerdo-consumo (confirmar dato de 2008 con CICCRA).

---

## Cierre

De 49 notas publicadas en la semana, 27 (55%) resultaron CONFIRMADAS sin observaciones de fondo, 20 (41%) IMPRECISAS por detalles de sourcing o matices de contexto que no afectan la cifra ancla ni la tesis, y 2 (4%) con DISCREPANCIA. Ninguna nota resultó NO_VERIFICABLE. De las dos discrepancias, una (`carne-vacuna-consumo-minimo-record-exportacion`) involucra un superlativo de titular contradicho por su propia fuente — el mismo patrón de error que motivó la creación de este runbook — y se marca URGENTE junto con el hallazgo de `ia-no-reemplaza-oficios` (cifra de tesis sin fuente verificable). Ningún caso ameritó recomendar el retiro de una nota de circulación; todas las correcciones propuestas son ediciones puntuales de texto o de fuente.

*Auditoría automatizada — Con Interés. El auditor no edita ni despublica: detecta, informa y recomienda.*
