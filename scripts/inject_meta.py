#!/usr/bin/env python3
"""
inject_meta.py — Inyecta (o refresca) los metadatos de marca y redes sociales
en cada nota publicada, tomando los datos de data/articulos.json.

Idempotente: reemplaza el bloque marcado <!-- DELTA-META --> si ya existe.
Se puede correr las veces que haga falta. Lo llama aprobar.py al publicar.

Uso:  python3 scripts/inject_meta.py
"""
import json, os, re
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://hojeda465.github.io/delta-portal"   # mantener igual que build_portada.py

BLOCK_RE = re.compile(r"[ \t]*<!-- DELTA-META:start -->.*?<!-- DELTA-META:end -->\n?", re.S)

def meta_block(a):
    url = f"{SITE}/{a['archivo']}"
    title = escape(a['titulo']) + " — Delta"
    desc = escape(a.get('bajada', ''))
    img = f"{SITE}/assets/og-delta.png"
    return (
        "<!-- DELTA-META:start -->\n"
        '<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">\n'
        f'<link rel="canonical" href="{url}">\n'
        '<meta property="og:type" content="article">\n'
        '<meta property="og:site_name" content="Delta">\n'
        f'<meta property="og:title" content="{title}">\n'
        f'<meta property="og:description" content="{desc}">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:image" content="{img}">\n'
        '<meta property="og:locale" content="es_AR">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{title}">\n'
        f'<meta name="twitter:description" content="{desc}">\n'
        f'<meta name="twitter:image" content="{img}">\n'
        "<!-- DELTA-META:end -->\n"
    )

def main():
    arts = json.load(open(os.path.join(ROOT, "data", "articulos.json"), encoding="utf-8"))["articulos"]
    n = 0
    for a in arts:
        path = os.path.join(ROOT, a["archivo"])
        if not os.path.exists(path):
            print(f"  (falta {a['archivo']}, salteo)"); continue
        html = open(path, encoding="utf-8").read()
        html = BLOCK_RE.sub("", html)            # saca bloque previo si existe
        block = meta_block(a)
        # insertar después del <meta name="viewport" ...>
        m = re.search(r'<meta name="viewport"[^>]*>\n?', html)
        if m:
            html = html[:m.end()] + block + html[m.end():]
        else:                                    # fallback: después de <title>
            html = re.sub(r"(</title>\n?)", r"\1" + block, html, count=1)
        open(path, "w", encoding="utf-8").write(html)
        n += 1
    print(f"OK -> metadatos inyectados en {n} nota(s)")

if __name__ == "__main__":
    main()
