#!/usr/bin/env python3
"""
inject_widgets.py — Inserta en todas las páginas del sitio que no los tengan:
  - el ticker de indicadores (assets/ticker.js)
  - la instrumentación de métricas (assets/metrics.js)

Idempotente: usa los marcadores CI-WIDGETS y CI-METRICS y no duplica si ya
están. El agente Publicador debe correrlo (o copiar los includes de la
plantilla) para cada nota nueva.

Sobre metrics.js: HOY NO ENVÍA NADA. Mientras `ENDPOINT` sea null dentro de ese
archivo, se corta en la primera línea y no hace ninguna llamada de red. Se
incluye igual para que activar la medición sea editar una línea y no volver a
tocar cien archivos. Ver negocio/activar-medicion.md.

Uso:  python3 scripts/inject_widgets.py
"""
import os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (marcador, plantilla del include, huella para no duplicar)
PIEZAS = [
    ("<!-- CI-WIDGETS -->", '<script defer src="{base}assets/ticker.js?v=5"></script>', "assets/ticker.js"),
    ("<!-- CI-METRICS -->", '<script defer src="{base}assets/metrics.js?v=1"></script>', "assets/metrics.js"),
]

def inject(path, depth):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if "</body>" not in html:
        return 0
    base = "../" * depth
    puestas = 0
    for mark, tpl, huella in PIEZAS:
        if mark in html or huella in html:
            continue
        html = html.replace("</body>", mark + tpl.format(base=base) + "\n</body>", 1)
        puestas += 1
    if puestas:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
    return puestas

def main():
    hechos, saltados, total = [], [], 0
    objetivos = (
        [(p, 1) for p in glob.glob(os.path.join(ROOT, "articulos", "*.html"))]
        + [(p, 1) for p in glob.glob(os.path.join(ROOT, "lecciones", "*.html"))]
        + [(os.path.join(ROOT, "aprender.html"), 0),
           (os.path.join(ROOT, "como-trabajamos.html"), 0),
           (os.path.join(ROOT, "herramientas.html"), 0),
           (os.path.join(ROOT, "pregunta.html"), 0)]
    )
    for path, depth in objetivos:
        if not os.path.exists(path):
            continue
        n = inject(path, depth)
        total += n
        (hechos if n else saltados).append(os.path.basename(path))
    print(f"OK -> {total} includes puestos en {len(hechos)} páginas ({len(saltados)} ya estaban completas)")

if __name__ == "__main__":
    main()
