#!/usr/bin/env python3
"""
rechazar.py — Rechaza un borrador de la cola.

Borra la nota de cola/, la saca de cola.json y marca el tema como
descartada en cubiertas.json (para no volver a proponerlo). Regenera la portada.

Uso:  python3 scripts/rechazar.py <id-del-borrador> ["motivo opcional"]
"""
import json, os, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

def load(n):
    with open(os.path.join(DATA, n), encoding="utf-8") as f: return json.load(f)
def save(n, d):
    with open(os.path.join(DATA, n), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def main(draft_id, motivo=""):
    cola = load("cola.json"); cub = load("cubiertas.json")
    if not any(b["id"] == draft_id for b in cola["borradores"]):
        print(f"ERROR: no encontré el borrador '{draft_id}' en la cola."); sys.exit(1)
    f = os.path.join(ROOT, "cola", f"{draft_id}.html")
    if os.path.exists(f): os.remove(f)
    cola["borradores"] = [b for b in cola["borradores"] if b["id"] != draft_id]
    for t in cub["temas"]:
        if t.get("articulo_id") == draft_id:
            t["estado"] = "descartada"
            if motivo: t["motivo_descarte"] = motivo
    save("cola.json", cola); save("cubiertas.json", cub)
    subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "build_portada.py")], check=True)
    print(f"RECHAZADA: {draft_id}" + (f" — {motivo}" if motivo else ""))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Uso: python3 scripts/rechazar.py <id> ["motivo"]'); sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
