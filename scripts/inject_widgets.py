#!/usr/bin/env python3
"""
inject_widgets.py — Inserta los widgets compartidos (ticker de indicadores +
newsletter, assets/widgets.js) en todas las páginas del sitio que no los tengan.

Idempotente: usa marcadores CI-WIDGETS y no duplica si ya están.
El agente Publicador debe correrlo (o copiar el include de la plantilla)
para cada nota nueva.

Uso:  python3 scripts/inject_widgets.py
"""
import os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "<!-- CI-WIDGETS -->"

def include_tag(depth):
    base = "../" * depth
    return f'{MARK}<script defer src="{base}assets/widgets.js"></script>\n'

def inject(path, depth):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if MARK in html or "assets/widgets.js" in html:
        return False
    if "</body>" not in html:
        return False
    html = html.replace("</body>", include_tag(depth) + "</body>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return True

def main():
    hechos, saltados = [], []
    objetivos = (
        [(p, 1) for p in glob.glob(os.path.join(ROOT, "articulos", "*.html"))]
        + [(p, 1) for p in glob.glob(os.path.join(ROOT, "lecciones", "*.html"))]
        + [(os.path.join(ROOT, "aprender.html"), 0),
           (os.path.join(ROOT, "como-trabajamos.html"), 0)]
    )
    for path, depth in objetivos:
        if not os.path.exists(path):
            continue
        (hechos if inject(path, depth) else saltados).append(os.path.basename(path))
    print(f"OK -> widgets inyectados en {len(hechos)} páginas ({len(saltados)} ya los tenían)")

if __name__ == "__main__":
    main()
