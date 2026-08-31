# Fichas de investigacion

Documentos de trabajo, **no se publican en el sitio**.

Una ficha es lo que devuelve la mision de investigacion del agente local: un tema investigado en
fuentes primarias, con cada numero etiquetado (`CONFIRMADO`, `ESTIMACION`,
`NO_VERIFICADO`, `CALCULO PROPIO`), sus fuentes con URL y fecha, los graficos
armados desde el dato crudo, y una seccion con lo que no se pudo verificar.

Sirven para dos cosas:

1. **Material para una nota.** Si la ficha da para nota, sale por la corrida de redaccion,
   que la escribe con el metodo de 6 capas y la deja en la cola.
2. **Insumo para terceros.** Un economista, un profesor o un periodista puede
   usar la ficha para su propia columna, informe o clase. Si la usa afuera, la
   atribucion pedida es una linea: "datos verificados por Con Interes".

## Por que no se versionan

Los `.html` de esta carpeta estan en `.gitignore`. Son borradores de trabajo:
pueden citar a terceros, pueden tener datos todavia sin cerrar y pueden hablar
de personas por su nombre. Nada de eso deberia quedar accesible en un sitio
publico solo por estar en el repo. Si una ficha tiene que ser publica, se
convierte en nota y sale por la cola de revision, con la aprobacion de siempre.
