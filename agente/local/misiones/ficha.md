# Mision 3 - Ficha de investigacion

**Objetivo:** devolver una ficha con datos verificados sobre un tema, para que
la use una persona. **No es una nota.** No lleva bajada, no lleva narrativa y no
cierra con una conclusion: pone el dato al lado de la afirmacion, con la fuente,
y deja la lectura al que la use.

Horacio te pasa un tema, una pregunta o un link (por ejemplo, una entrevista con
proyecciones para contrastar contra la serie).

## Que tiene que tener la ficha

1. **Encabezado** - de que se trata, de donde salio (con link si hay origen),
   fecha de cierre de la ficha, cuantas afirmaciones se chequearon y cuantas
   quedaron confirmadas.
2. **Veredicto por afirmacion** - una tarjeta por afirmacion: que se dijo (citado
   textual y atribuido, nunca reconstruido) y que dice el dato. Cada una con su
   etiqueta.
3. **Los graficos** - SVG propios armados desde el dato crudo. Cada uno: una
   idea, con eje, fuente y unidad. **Si no tenes la serie, no dibujes una linea:**
   tres puntos verificados se muestran como tres puntos, no como una curva, y se
   aclara por que.
4. **"Lo que no cerro"** - la seccion que hace que la ficha sirva. Todo lo que no
   se pudo sostener va escrito aca, no se omite ni se maquilla: fuentes que se
   contradicen, datos que salen de una consultora y no del organismo, cifras que
   parecen la misma pero miden cosas distintas.
5. **Ficha de datos** - la tabla completa: dato, valor, periodo, fuente exacta
   con URL y fecha, y etiqueta. Es lo que se lleva quien use la ficha, y es
   tambien la vista de tabla de los graficos.
6. **Nota de metodo** - que se puede usar y que no, y que falta para cerrarla.

## Las etiquetas

| Etiqueta | Cuando | Se puede usar? |
|---|---|---|
| `CONFIRMADO` | dos fuentes independientes coinciden | Si |
| `ESTIMACION` | proyeccion, dato con rango o una sola fuente de mercado | Si, con el rango y la palabra "estimado" |
| `NO_VERIFICADO` | una sola fuente, o fuentes que se contradicen | **No.** No se afirma nada con esto |
| `CALCULO PROPIO` | aritmetica de Con Interes sobre cifras de la tabla | Si, marcado como tal y rehacible |

Un medio que reproduce un dato oficial **no** es una segunda fuente independiente
del organismo. Dos analisis independientes del mismo dato primario si cuentan,
pero se aclara.

## Reglas que hacen la diferencia

- **Postura de refutacion.** Asumi que el dato esta mal hasta que las fuentes lo
  sostengan. Busca activamente la cifra que lo contradiga.
- **Cuidado con los denominadores.** El error mas comun de las series argentinas
  es comparar dos cifras que se llaman parecido y miden sobre poblaciones
  distintas. Si dos numeros no cierran entre si, ese es el hallazgo, no un
  estorbo: va a "lo que no cerro".
- **Chequea la aritmetica de las fuentes.** Si la fuente dice un porcentaje y las
  dos cifras que publica dan otro, se reporta la diferencia.
- **Citas solo on-the-record y enlazadas.** Nunca reconstruyas una cita ni
  parafrasees como si fuera textual.
- **Neutral.** La ficha no dice si alguien acerto o se equivoco. Pone el dato al
  lado de la afirmacion. La lectura la hace el que la usa.

## Salida

Guardala en `fichas/<AAAA-MM-DD-tema-en-kebab>.html`, con la identidad visual del
sitio (mismos tokens de color y tipografia que `agente/plantilla.html`) y con
`<meta name="robots" content="noindex">`: **las fichas son documentos de trabajo,
no se publican en el sitio.** Si Horacio quiere hacer una nota con eso, sale por
la corrida de redaccion.

Al terminar, decile: donde quedo el archivo, cuantas afirmaciones se confirmaron
y que quedo sin cerrar.
