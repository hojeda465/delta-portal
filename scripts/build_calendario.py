#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_calendario.py - El calendario de publicaciones oficiales.

Por que existe
--------------
La mitad de la materia prima de un diario de datos tiene fecha de publicacion
conocida con semanas de anticipacion: el IPC sale el 10 de septiembre a las 16,
el informe cambiario del BCRA el 25. Hasta ahora el Rastreador salia a barrer
portales de forma reactiva y llegaba cuando el dato ya habia rebotado en todos
lados. Con este calendario la redaccion sabe hoy que va a escribir en tres
semanas, y puede tener la nota armada entera salvo el numero.

De donde salen los datos - SIEMPRE de la fuente primaria
--------------------------------------------------------
  INDEC  calendario de difusion oficial. La pagina es una SPA; los eventos
         vienen en un JSON embebido en /Calendario/Fecha/0.
  BCRA   https://www.bcra.gob.ar/calendario-de-informes/ (tabla HTML).

No se inventa ni se estima NINGUNA fecha. Si una fuente no publica calendario,
no entra: es preferible un calendario corto y cierto que uno largo y dudoso.

La prioridad y la seccion NO son dato
--------------------------------------
`prioridad` y `seccion` son una preclasificacion editorial hecha con las listas
de palabras de abajo, para que la redaccion no tenga que mirar 120 filas. Van
marcadas como criterio, no como dato. La decision sigue siendo del editor.

Uso:  python scripts/build_calendario.py [--dias 120]
"""
import argparse
import datetime
import html
import io
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(ROOT, "data", "calendario.json")

INDEC_VISTA = "https://www.indec.gob.ar/Calendario/Fecha/0"
INDEC_HUMANO = "https://www.indec.gob.ar/indec/web/Institucional-Indec-Calendario"
BCRA_CAL = "https://www.bcra.gob.ar/calendario-de-informes/"

UA = "Mozilla/5.0 (compatible; ConInteres/1.0; +https://coninteres.com)"

MESES_AR = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
            "jul": 7, "ago": 8, "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12}

# --- preclasificacion editorial (criterio, no dato) -------------------------
# ALTA: series que tocan el bolsillo o que mueven la conversacion del dia.
ALTA = [
    "precios al consumidor", "canasta b", "canasta de crianza", "pobreza",
    "mercado de trabajo", "salarios", "actividad econ", "emae",
    "intercambio comercial", "balanza de pagos", "deuda externa",
    "produccion industrial manufacturero", "producción industrial manufacturero",
    "construcci", "capacidad instalada", "precios mayoristas",
    "expectativas de mercado", "rem", "monetario mensual", "mercado de cambios",
    "politica monetaria", "política monetaria", "estabilidad financiera",
    "informe sobre bancos", "cuentas nacionales", "distribuci",
]
MEDIA = [
    "servicios p", "minero", "pesquero", "turismo", "supermercados",
    "internet", "tecnolog", "energ", "farmac", "boletin estad",
    "boletín estad", "pagos minoristas", "inversion extranjera",
    "inversión extranjera", "condiciones crediticias", "inclusi",
]

SECCION = [
    ("tu-plata", ["precios al consumidor", "canasta", "pobreza", "salarios",
                  "mercado de trabajo", "crianza", "supermercados", "inclusi",
                  "protecci", "pagos minoristas", "condiciones crediticias"]),
    ("los-mercados", ["expectativas de mercado", "monetario", "bancos",
                      "estabilidad financiera", "mercado de cambios",
                      "deuda externa", "boletin estad", "boletín estad",
                      "inversion extranjera", "inversión extranjera",
                      "politica monetaria", "política monetaria"]),
    ("tu-provincia", ["provincial", "origen provincial", "jurisdicci"]),
    ("el-mundo", ["intercambio comercial", "balanza de pagos", "internacional"]),
]


def bajar(url):
    pedido = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(pedido, timeout=90) as r:
        return r.read().decode("utf-8", "replace")


def limpiar(t):
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def prioridad_de(titulo):
    t = titulo.lower()
    if any(k in t for k in ALTA):
        return "alta"
    if any(k in t for k in MEDIA):
        return "media"
    return "baja"


def seccion_de(titulo):
    t = titulo.lower()
    for sec, claves in SECCION:
        if any(k in t for k in claves):
            return sec
    return "el-pais"


# --------------------------------------------------------------------- INDEC
def indec(desde, hasta):
    """El calendario del INDEC viaja como un JSON dentro de un <script>."""
    s = bajar(INDEC_VISTA)
    m = re.search(r"<script[^>]*>(.*?)</script>", s, re.S)
    if not m:
        raise RuntimeError("INDEC: no encontre el script con los eventos")
    js = m.group(1)
    i = js.find('[{"id":')
    if i < 0:
        raise RuntimeError("INDEC: no encontre el array de eventos")

    # Recorre hasta cerrar el corchete respetando comillas y escapes: hay
    # titulos con corchetes adentro.
    prof, fin, en_str, escapando = 0, None, False, False
    for k in range(i, len(js)):
        c = js[k]
        if escapando:
            escapando = False
            continue
        if c == "\\":
            escapando = True
            continue
        if c == '"':
            en_str = not en_str
            continue
        if en_str:
            continue
        if c == "[":
            prof += 1
        elif c == "]":
            prof -= 1
            if prof == 0:
                fin = k + 1
                break
    eventos = json.loads(js[i:fin])

    salida = []
    for e in eventos:
        fp = (e.get("fechaPublicacion") or "")[:10]
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", fp):
            continue
        f = datetime.date.fromisoformat(fp)
        if not (desde <= f <= hasta):
            continue
        titulo = (e.get("titulo_espaniol") or "").strip()
        if not titulo:
            continue
        hora = str(e.get("hora") or "").zfill(4)
        salida.append({
            "fecha": fp,
            "hora": (hora[:2] + ":" + hora[2:]) if len(hora) == 4 else None,
            "organismo": "INDEC",
            "publicacion": titulo,
            "prioridad": prioridad_de(titulo),
            "seccion_sugerida": seccion_de(titulo),
            "calendario": INDEC_HUMANO,
        })
    return salida


# ---------------------------------------------------------------------- BCRA
def bcra(desde, hasta):
    s = bajar(BCRA_CAL)
    t = re.search(r"<table.*?</table>", s, re.S)
    if not t:
        raise RuntimeError("BCRA: no encontre la tabla del calendario")
    salida = []
    for fila in re.findall(r"<tr[^>]*>(.*?)</tr>", t.group(0), re.S):
        celdas = [limpiar(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", fila, re.S)]
        if len(celdas) < 2 or not celdas[0] or not celdas[1]:
            continue
        m = re.match(r"^(\d{1,2})\s+([a-zA-Zéáí]{3,4})\.?\s+(\d{4})$", celdas[1].strip())
        if not m:
            continue  # la fila de encabezado cae aca
        dia, mes_txt, anio = int(m.group(1)), m.group(2)[:3].lower(), int(m.group(3))
        mes = MESES_AR.get(mes_txt)
        if not mes:
            continue
        try:
            f = datetime.date(anio, mes, dia)
        except ValueError:
            continue
        if not (desde <= f <= hasta):
            continue
        titulo = celdas[0]
        salida.append({
            "fecha": f.isoformat(),
            "hora": None,          # el BCRA no publica hora
            "organismo": "BCRA",
            "publicacion": titulo,
            "prioridad": prioridad_de(titulo),
            "seccion_sugerida": seccion_de(titulo),
            "calendario": BCRA_CAL,
        })
    return salida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=120,
                    help="ventana hacia adelante (default 120)")
    args = ap.parse_args()

    hoy = datetime.date.today()
    hasta = hoy + datetime.timedelta(days=args.dias)

    filas, errores = [], []
    for nombre, fn in (("INDEC", indec), ("BCRA", bcra)):
        try:
            n = fn(hoy, hasta)
            filas += n
            print("  %-6s %3d publicaciones" % (nombre, len(n)))
        except Exception as e:
            # Si una fuente falla, el calendario sale igual con la otra y lo
            # dice. Es preferible incompleto y avisado que completo e inventado.
            errores.append("%s: %s" % (nombre, e))
            print("  %-6s FALLO -> %s" % (nombre, e), file=sys.stderr)

    if not filas:
        print("Ninguna fuente respondio. No se toca data/calendario.json.", file=sys.stderr)
        return 1

    filas.sort(key=lambda x: (x["fecha"], x["organismo"], x["publicacion"]))

    doc = {
        "descripcion": ("Calendario de publicaciones oficiales. Lo genera "
                        "scripts/build_calendario.py desde los calendarios de "
                        "difusion del INDEC y del BCRA. Ninguna fecha se estima: "
                        "si una fuente no publica calendario, no entra. "
                        "'prioridad' y 'seccion_sugerida' son preclasificacion "
                        "editorial, no dato de la fuente."),
        "generado": datetime.datetime.now().replace(microsecond=0).isoformat(),
        "desde": hoy.isoformat(),
        "hasta": hasta.isoformat(),
        "fuentes": {"INDEC": INDEC_HUMANO, "BCRA": BCRA_CAL},
        "incompleto": errores or None,
        "total": len(filas),
        "publicaciones": filas,
    }
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with io.open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("OK -> data/calendario.json  %d publicaciones  %s a %s"
          % (len(filas), hoy, hasta))
    if errores:
        print("     OJO: calendario INCOMPLETO ->", "; ".join(errores))
    return 0


if __name__ == "__main__":
    sys.exit(main())
