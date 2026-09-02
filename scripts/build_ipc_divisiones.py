#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_ipc_divisiones.py - Baja del INDEC las doce divisiones del IPC y las deja
en data/ipc-divisiones.json, que es lo que come la calculadora "tu canasta"
de herramientas.html.

Los ponderadores nacionales NO los publica el INDEC en una sola tabla: la
metodologia (Cuadro 7) trae la estructura POR REGION, y aparte la participacion
de cada region en el gasto nacional (GBA 0,447 / Pampeana 0,342 / NOA 0,069 /
Cuyo 0,052 / Patagonia 0,046 / NEA 0,045). El nacional sale de combinarlos.

Ese calculo esta VERIFICADO: reproduce los cinco ponderadores nacionales que se
publicaron cuando se anuncio el cambio de canasta (Alimentos 26,9 / Prendas 9,9
/ Vivienda 9,4 / Transporte 11,0 / Comunicacion 2,8) con diferencias de entre
0,00 y 0,07 puntos. La comprobacion corre sola en cada ejecucion: si algun dia
deja de dar, el script avisa.

Ojo con la vigencia: son los ponderadores de la ENGHo 2004/05. El INDEC preparo
el reemplazo con la ENGHo 2017/18 y la actualizacion quedo suspendida (ver la
nota del 01/09/2026). Cuando se active, hay que rehacer PONDERADORES.

Uso:  python scripts/build_ipc_divisiones.py
"""
import datetime
import io
import json
import os
import subprocess
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://apis.datos.gob.ar/series/api/series/"
DESDE = "2016-12"

# id interno -> (nombre INDEC, serie del IPC nacional base dic-2016)
DIVISIONES = [
    ("alimentos",    "Alimentos y bebidas no alcohólicas",                     "146.3_IALIMENNAL_DICI_M_45"),
    ("bebidas",      "Bebidas alcohólicas y tabaco",                           "146.3_IBEBIDANAL_DICI_M_39"),
    ("prendas",      "Prendas de vestir y calzado",                            "146.3_IPRENDANAL_DICI_M_35"),
    ("vivienda",     "Vivienda, agua, electricidad, gas y otros combustibles", "146.3_IVIVIENNAL_DICI_M_52"),
    ("equipamiento", "Equipamiento y mantenimiento del hogar",                 "146.3_IEQUIPANAL_DICI_M_46"),
    ("salud",        "Salud",                                                  "146.3_ISALUDNAL_DICI_M_18"),
    ("transporte",   "Transporte",                                             "146.3_ITRANSPNAL_DICI_M_23"),
    ("comunicacion", "Comunicación",                                           "146.3_ICOMUNINAL_DICI_M_27"),
    ("recreacion",   "Recreación y cultura",                                   "146.3_IRECREANAL_DICI_M_31"),
    ("educacion",    "Educación",                                              "146.3_IEDUCACNAL_DICI_M_22"),
    ("restaurantes", "Restaurantes y hoteles",                                 "146.3_IRESTAUNAL_DICI_M_33"),
    ("varios",       "Bienes y servicios varios",                              "146.3_IBIENESNAL_DICI_M_36"),
]
NIVEL_GENERAL = "145.3_INGNACNAL_DICI_M_15"

# Cuadro 7 de la metodologia: ponderaciones regionales, diciembre de 2016.
REGIONES = ["GBA", "Pampeana", "NEA", "NOA", "Cuyo", "Patagonia"]
PARTICIPACION = {"GBA": .447, "Pampeana": .342, "NEA": .045,
                 "NOA": .069, "Cuyo": .052, "Patagonia": .046}
PONDERADORES_REGIONALES = {
    "alimentos":    [23.44, 28.65, 35.30, 34.67, 28.42, 27.43],
    "bebidas":      [3.27, 3.80, 3.64, 3.13, 3.57, 3.50],
    "prendas":      [8.49, 10.43, 11.60, 12.37, 11.38, 12.82],
    "vivienda":     [10.46, 8.67, 8.11, 7.00, 8.88, 10.06],
    "equipamiento": [6.27, 6.34, 7.78, 6.12, 6.28, 6.55],
    "salud":        [8.80, 8.16, 5.26, 6.33, 7.40, 4.95],
    "transporte":   [11.59, 10.41, 9.63, 8.41, 12.10, 13.42],
    "comunicacion": [2.81, 2.86, 2.82, 2.59, 2.53, 3.19],
    "recreacion":   [7.46, 7.39, 6.23, 5.95, 6.72, 7.77],
    "educacion":    [3.02, 1.61, 1.36, 2.04, 2.24, 2.09],
    "restaurantes": [10.84, 8.10, 4.96, 7.99, 6.85, 5.08],
    "varios":       [3.55, 3.58, 3.30, 3.40, 3.63, 3.14],
}
# Los cinco que el INDEC publico al anunciar el cambio de canasta. Son el
# control de que la combinacion regional -> nacional esta bien hecha.
CONTROL = {"alimentos": 26.9, "prendas": 9.9, "vivienda": 9.4,
           "transporte": 11.0, "comunicacion": 2.8}


def ponderadores_nacionales():
    tot = sum(PARTICIPACION.values())
    crudo = {k: sum(v[i] * PARTICIPACION[REGIONES[i]] for i in range(6)) / tot
             for k, v in PONDERADORES_REGIONALES.items()}
    s = sum(crudo.values())
    nac = {k: v / s * 100 for k, v in crudo.items()}
    malos = [(k, round(nac[k], 2), esp) for k, esp in CONTROL.items()
             if abs(nac[k] - esp) > 0.25]
    if malos:
        print("ERROR: la combinacion regional no reproduce los ponderadores")
        print("       nacionales publicados. Revisar el Cuadro 7 y la")
        print("       participacion por region antes de usar esto:")
        for k, calc, esp in malos:
            print("       %-14s calculado %.2f  publicado %.1f" % (k, calc, esp))
        sys.exit(1)
    return {k: round(v, 2) for k, v in nac.items()}


def bajar(ids):
    url = API + "?" + urllib.parse.urlencode(
        {"ids": ",".join(ids), "format": "json", "limit": 1000, "start_date": DESDE})
    salida = subprocess.run(["curl", "-s", "--max-time", "90", url],
                            capture_output=True, text=True, encoding="utf-8").stdout
    try:
        d = json.loads(salida)
    except ValueError:
        print("ERROR: la API de series no devolvio JSON."); sys.exit(1)
    if "data" not in d:
        print("ERROR de la API:", str(d)[:300]); sys.exit(1)
    cols = [m["field"]["id"] for m in d["meta"][1:]]
    return cols, d["data"]


def main():
    pond = ponderadores_nacionales()
    ids = [s for _, _, s in DIVISIONES] + [NIVEL_GENERAL]
    cols, filas = bajar(ids)
    faltan = [i for i in ids if i not in cols]
    if faltan:
        print("ERROR: la API no devolvio estas series:", faltan); sys.exit(1)

    pos = {c: i for i, c in enumerate(cols)}
    filas = [f for f in filas if all(f[1:][pos[i]] is not None for i in ids)]
    meses = [f[0][:7] for f in filas]

    datos = {
        "descripcion": "Índice de precios al consumidor del INDEC, base diciembre 2016 = 100, "
                       "abierto por las doce divisiones de la canasta, más el nivel general. "
                       "Alimenta la calculadora «tu canasta» de herramientas.html.",
        "fuente": "INDEC, IPC nacional base dic-2016, series abiertas de datos.gob.ar",
        "ponderadores_fuente": "INDEC, Metodología del IPC nacional (Cuadro 7, estructura "
                               "regional de ponderaciones, diciembre de 2016) combinada con la "
                               "participación de cada región en el gasto nacional. Canasta "
                               "ENGHo 2004/05, la vigente.",
        "generado": datetime.date.today().isoformat(),
        "desde": meses[0],
        "hasta": meses[-1],
        "meses": meses,
        "nivel_general": [round(f[1:][pos[NIVEL_GENERAL]], 2) for f in filas],
        "divisiones": [
            {"id": cid, "nombre": nombre, "ponderador": pond[cid],
             "serie": [round(f[1:][pos[sid]], 2) for f in filas]}
            for cid, nombre, sid in DIVISIONES
        ],
    }

    destino = os.path.join(ROOT, "data", "ipc-divisiones.json")
    io.open(destino, "w", encoding="utf-8").write(
        json.dumps(datos, ensure_ascii=False, separators=(",", ":")))
    print("OK -> %s" % destino)
    print("   %d meses (%s a %s), 12 divisiones + nivel general, %.0f KB"
          % (len(meses), meses[0], meses[-1], os.path.getsize(destino) / 1024))
    print("   ponderadores nacionales verificados contra los 5 publicados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
