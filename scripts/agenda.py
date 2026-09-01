#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agenda.py - Que sale, cuando, y que escribimos la ultima vez sobre eso.

Lee data/calendario.json (lo genera build_calendario.py desde los calendarios
oficiales del INDEC y del BCRA) y lo cruza con data/articulos.json para que la
corrida de redaccion no arranque en una pagina en blanco: para cada dato que
esta por salir muestra la nota anterior de esa misma serie, que es la que hay
que actualizar y contra la que hay que comparar.

Es la diferencia entre "a ver que encuentro hoy" y "el jueves a las 16 sale el
IPC de agosto, la ultima que escribimos fue esta, y el dato a superar es este".

Ademas lee data/pedidos.json y lista lo que pidieron los lectores. Son las dos
entradas del paso 0: lo que va a salir (el calendario) y lo que alguien quiere
saber (los pedidos). Un pedido es un CANDIDATO para el Editor, nunca una orden:
ver agente/NEWSROOM.md, seccion 2 ter.

Uso:
  python scripts/agenda.py                # los proximos 14 dias
  python scripts/agenda.py --dias 30
  python scripts/agenda.py --alta         # solo prioridad alta
"""
import argparse
import datetime
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Palabras que no distinguen una serie de otra: no sirven para emparejar.
VACIAS = set("""
de del la el los las y en a al por para con sobre un una unos unas su sus
segundo primer primera tercer cuarto trimestre mes mensual anual año años
argentina argentino nacional cobertura indice índice informe indicador
indicadores sistema valorizacion valorización datos dato total totales
enero febrero marzo abril mayo junio julio agosto septiembre octubre
noviembre diciembre bienes evolucion evolución avance nivel
""".split())

# Emparejar por palabras sueltas no alcanza: el IPC del INDEC y nuestra nota
# titulada "inflación" no comparten ninguna, y en cambio "precios mayoristas"
# engancha cualquier nota que diga "precios". Este mapa dice, para cada serie
# oficial, con que terminos la nombramos nosotros. Se amplia a mano cuando
# aparece una serie nueva; lo que no este aca cae al emparejado por palabras,
# que es mas laxo y por eso exige mas coincidencias.
SERIES = [
    (["precios al consumidor", "ipc"],          ["inflacion", "ipc", "precios"]),
    (["canasta basica", "canasta básica"],      ["canasta", "pobreza", "indigencia"]),
    (["canasta de crianza"],                    ["crianza", "canasta"]),
    (["pobreza"],                               ["pobreza", "indigencia"]),
    (["mercado de trabajo"],                    ["desempleo", "empleo", "trabajo"]),
    (["actividad economica", "emae"],           ["emae", "actividad"]),
    (["produccion industrial manufacturero",
      "producción industrial manufacturero"],   ["industria", "manufacturer", "fabril"]),
    (["actividad de la construccion",
      "actividad de la construcción", "isac"],  ["construccion", "cemento", "corralones"]),
    (["costo de la construccion",
      "costo de la construcción", "icc"],       ["construccion", "corralones"]),
    (["capacidad instalada"],                   ["capacidad instalada", "ociosa"]),
    (["precios mayoristas", "sipm"],            ["mayorista"]),
    (["intercambio comercial", "ica"],          ["comercio exterior", "exportacion",
                                                 "importacion", "superavit comercial",
                                                 "balanza"]),
    (["balanza de pagos", "cuentas internacionales"], ["cuenta corriente", "balanza",
                                                        "deuda externa"]),
    (["deuda externa"],                         ["deuda externa"]),
    (["industrial minero"],                     ["mineria", "litio", "minero"]),
    (["industrial pesquero"],                   ["pesca", "pesquero"]),
    (["servicios publicos", "servicios públicos", "issp"], ["servicios"]),
    (["supermercados", "autoservicios"],        ["supermercado", "shopping", "consumo"]),
    (["turismo"],                               ["turismo", "turista", "pasajeros"]),
    (["expectativas de mercado", "rem"],        ["rem", "expectativas", "proyeccion"]),
    (["monetario mensual"],                     ["monetario", "base monetaria", "pesos"]),
    (["mercado de cambios"],                    ["cambiario", "dolares", "mercado de cambios",
                                                 "reservas"]),
    (["sobre bancos"],                          ["bancos", "credito", "mora", "deposito"]),
    (["estabilidad financiera"],                ["bancos", "financiero", "riesgo"]),
    (["politica monetaria", "política monetaria", "ipom"], ["monetario", "tasa"]),
    (["inversion extranjera", "inversión extranjera"],     ["inversion extranjera", "ied"]),
    (["condiciones crediticias"],               ["credito", "hipotecario"]),
    (["pagos minoristas"],                      ["pagos", "transferencias", "qr"]),
    (["origen provincial"],                     ["provincial", "provincia"]),
    (["accesos a internet"],                    ["internet", "conectividad"]),
    (["farmaceutica", "farmacéutica"],          ["farmac", "medicamento", "prepaga"]),
]


def _rx(termino, cerrado):
    """Regex anclada a comienzo de palabra; cerrada tambien al final si el
    termino es corto. Sin esto 'ica' (por intercambio comercial) matchea dentro
    de 'publica' y el calendario emparejaba la dotacion de personal de la
    administracion publica con una nota de comercio exterior."""
    fin = r"\b" if cerrado or len(termino) <= 4 else ""
    return re.compile(r"\b" + re.escape(termino) + fin)


def terminos_de(publicacion):
    """Los terminos con los que NOSOTROS nombramos esta serie, si la conocemos."""
    t = sin_tildes(publicacion)
    for patrones, nuestros in SERIES:
        if any(_rx(sin_tildes(p), True).search(t) for p in patrones):
            return nuestros
    return None


def sin_tildes(t):
    t = t.lower()
    for a, b in (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n")):
        t = t.replace(a, b)
    return t


def palabras(t):
    return {w for w in re.findall(r"[a-z]{4,}", sin_tildes(t)) if w not in VACIAS}


def cargar(nombre):
    p = os.path.join(ROOT, "data", nombre)
    if not os.path.exists(p):
        return None
    return json.load(io.open(p, encoding="utf-8"))


def pedidos_pendientes():
    """Lo que pidieron los lectores y todavia no tiene respuesta."""
    datos = cargar("pedidos.json")
    if not datos:
        return []
    return [p for p in datos.get("pedidos", [])
            if p.get("estado") in ("recibido", "en_ficha")]


def imprimir_pedidos(pend):
    """La segunda entrada del paso 0. Se imprime siempre, aunque este vacia:
    que aparezca en cero es informacion (nadie pidio nada todavia), y que no
    aparezca haria olvidar que el canal existe."""
    print()
    print("=" * 78)
    print("PEDIDOS DE LECTORES  (%d sin responder)" % len(pend))
    print("=" * 78)
    if not pend:
        print("  No hay pedidos pendientes.")
        print("  Entran por pedidos.html y se registran en data/pedidos.json.")
        return
    for p in sorted(pend, key=lambda x: x.get("recibido", "")):
        en_ficha = p.get("estado") == "en_ficha"
        print("  %s [%s] %s  %s" % (" * " if en_ficha else "   ",
                                    p.get("id", "?"),
                                    p.get("recibido", ""),
                                    p.get("afirmacion", "")[:58]))
        if p.get("de_donde"):
            print("        el lector dice que salio de: %s" % p["de_donde"][:58])
        if en_ficha:
            print("        YA EN FICHA - no volver a empezarlo")
    print()
    print("  Un pedido es un candidato para el Editor, no una orden: se elige")
    print("  con los mismos criterios (riqueza de datos, relevancia, no repetir)")
    print("  y se verifica con el mismo protocolo. Ver NEWSROOM.md, seccion 2 ter.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=14)
    ap.add_argument("--alta", action="store_true", help="solo prioridad alta")
    args = ap.parse_args()

    cal = cargar("calendario.json")
    if not cal:
        print("Falta data/calendario.json. Corre:  python scripts/build_calendario.py",
              file=sys.stderr)
        return 1

    arts = (cargar("articulos.json") or {}).get("articulos", [])
    # Se empareja contra el TITULO y el slug del archivo, no contra la bajada:
    # la bajada menciona de pasada "pobreza" o "pesos" para comparar, y con eso
    # el calendario terminaba diciendo que la nota anterior del IPC era una de
    # hockey. El titulo es de lo que la nota trata.
    idx = []
    for a in arts:
        crudo = " ".join([a.get("titulo", ""), a.get("archivo", "").replace("-", " ")])
        idx.append((palabras(crudo), sin_tildes(crudo), a))
    idx.sort(key=lambda x: x[2].get("fecha", ""), reverse=True)  # la mas nueva primero

    hoy = datetime.date.today()
    hasta = hoy + datetime.timedelta(days=args.dias)

    gen = cal.get("generado", "")[:10]
    if gen and (hoy - datetime.date.fromisoformat(gen)).days > 20:
        print("OJO: el calendario se genero el %s. Convendria rehacerlo.\n" % gen)
    if cal.get("incompleto"):
        print("OJO: calendario incompleto ->", "; ".join(cal["incompleto"]), "\n")

    filas = [p for p in cal["publicaciones"]
             if hoy <= datetime.date.fromisoformat(p["fecha"]) <= hasta
             and (not args.alta or p["prioridad"] == "alta")]

    if not filas:
        print("No hay publicaciones en la ventana pedida.")
        imprimir_pedidos(pedidos_pendientes())
        return 0

    print("AGENDA - %s al %s   (%d publicaciones%s)"
          % (hoy, hasta, len(filas), ", solo alta" if args.alta else ""))
    print("=" * 78)

    dia_actual = None
    for p in filas:
        f = datetime.date.fromisoformat(p["fecha"])
        if p["fecha"] != dia_actual:
            dia_actual = p["fecha"]
            faltan = (f - hoy).days
            cuando = "HOY" if faltan == 0 else ("manana" if faltan == 1 else "en %d dias" % faltan)
            print("\n%s  %s  (%s)" % (p["fecha"], f.strftime("%A"), cuando))
            print("-" * 78)

        marca = {"alta": "***", "media": " * ", "baja": "   "}[p["prioridad"]]
        hora = p["hora"] or "  -  "
        print("  %s %s %-5s %s" % (marca, hora, p["organismo"], p["publicacion"]))

        # La nota anterior de la misma serie: contra esa se compara el dato
        # nuevo. Primero por el mapa SERIES, que es explicito; si la serie no
        # esta mapeada, por palabras, exigiendo 3 coincidencias para no
        # emparejar cualquier cosa que comparta la palabra "precios".
        mejor, como = None, ""
        nuestros = terminos_de(p["publicacion"])
        if nuestros:
            # Anclado a comienzo de palabra: buscar "rem" como subcadena
            # engancha "premios", y "pesos" engancha cualquier cosa. El sufijo
            # libre si conviene: "inflacion" tiene que encontrar "inflacionario".
            rx = [_rx(t, False) for t in nuestros]
            # Gana la que pega mas terminos distintos; entre iguales, la mas
            # nueva (idx ya viene ordenado de nueva a vieja).
            punt = 0
            for _, crudo, a in idx:
                n = sum(1 for r in rx if r.search(crudo))
                if n > punt:
                    mejor, punt = a, n
        if mejor is None:
            pw = palabras(p["publicacion"])
            punt = 0
            for aw, _, a in idx:
                n = len(pw & aw)
                if n > punt:
                    mejor, punt = a, n
            if punt < 3:
                mejor = None
            else:
                como = "  (emparejado por palabras: confirmar)"

        if mejor:
            print("        ultima nuestra: %s (%s)%s"
                  % (mejor["titulo"][:58], mejor["fecha"], como))
            print("        %s" % mejor["archivo"])
        else:
            print("        sin nota previa -> serie nueva")

    print("\n" + "=" * 78)
    print("*** prioridad alta   * media   |  fuentes:", ", ".join(cal["fuentes"]))
    print("La prioridad es preclasificacion editorial, no dato de la fuente.")

    imprimir_pedidos(pedidos_pendientes())
    return 0


if __name__ == "__main__":
    sys.exit(main())
