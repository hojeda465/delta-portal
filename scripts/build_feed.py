#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_feed.py - Genera feed.xml (RSS 2.0) desde data/articulos.json.

Por que existe: un diario de datos sin feed deja afuera a los agregadores y,
sobre todo, obliga a escribir un bot para publicar en redes. Con un feed, la
distribucion se automatiza enchufandolo a un programador de posteos (Buffer,
Make, Zapier): no se paga la API de X, las credenciales no tocan este repo ni
la maquina del editor, y queda un paso de revision humana antes de que salga
—que es exactamente lo que la seccion 9 del NEWSROOM queria proteger—.

Cada item lleva la TARJETA de la nota como enclosure y como media:content, que
son los dos formatos que leen esas herramientas. Asi el posteo sale con la
imagen de la cifra ancla y no con una placa generica.

Uso:  python scripts/build_feed.py [--items 30]
"""
import argparse
import datetime
import io
import json
import os
import sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://coninteres.com"          # mantener igual que build_portada.py
TZ = "-0300"                             # Argentina, sin horario de verano
DIAS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def rfc822(fecha, hora):
    """RFC-822, que es lo que exige RSS 2.0. Si la nota no trae hora, 09:00."""
    try:
        y, m, d = (int(x) for x in fecha.split("-"))
        hh, mm = (int(x) for x in (hora or "09:00").split(":")[:2])
        dt = datetime.datetime(y, m, d, hh, mm)
    except (ValueError, AttributeError):
        dt = datetime.datetime.now()
    return "%s, %02d %s %d %02d:%02d:00 %s" % (
        DIAS[dt.weekday()], dt.day, MESES[dt.month - 1], dt.year,
        dt.hour, dt.minute, TZ)


def item(a):
    url = "%s/%s" % (SITE, a["archivo"])
    partes = [
        "    <item>",
        "      <title>%s</title>" % escape(a.get("titulo", "")),
        "      <link>%s</link>" % escape(url),
        '      <guid isPermaLink="true">%s</guid>' % escape(url),
        "      <pubDate>%s</pubDate>" % rfc822(a.get("fecha", ""), a.get("hora", "")),
        "      <dc:creator>Redacción Con Interés</dc:creator>",
        "      <category>%s</category>" % escape(a.get("seccion", "")),
        "      <description>%s</description>" % escape(a.get("bajada", "")),
    ]
    # La cifra ancla, para que la herramienta de posteo pueda usarla en el texto.
    if (a.get("numero") or "").strip():
        partes.append("      <ci:numero>%s</ci:numero>" % escape(a["numero"]))
        if a.get("numero_label"):
            partes.append("      <ci:numeroEtiqueta>%s</ci:numeroEtiqueta>"
                          % escape(a["numero_label"]))
    tarjeta = os.path.join(ROOT, "assets", "tarjetas", a["id"] + ".png")
    if os.path.exists(tarjeta):
        u = "%s/assets/tarjetas/%s.png" % (SITE, a["id"])
        tam = os.path.getsize(tarjeta)
        partes.append('      <enclosure url="%s" length="%d" type="image/png"/>'
                      % (escape(u), tam))
        partes.append('      <media:content url="%s" medium="image" type="image/png"/>'
                      % escape(u))
    partes.append("    </item>")
    return "\n".join(partes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", type=int, default=30, help="cuantas notas incluir")
    args = ap.parse_args()

    datos = json.load(io.open(os.path.join(ROOT, "data", "articulos.json"),
                              encoding="utf-8"))
    arts = datos["articulos"][:args.items]
    if not arts:
        print("No hay notas publicadas."); return 1

    ahora = datetime.datetime.now()
    construido = "%s, %02d %s %d %02d:%02d:00 %s" % (
        DIAS[ahora.weekday()], ahora.day, MESES[ahora.month - 1], ahora.year,
        ahora.hour, ahora.minute, TZ)

    xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:media="http://search.yahoo.com/mrss/"
     xmlns:ci="https://coninteres.com/ns/">
  <channel>
    <title>Con Interés</title>
    <link>{site}/</link>
    <atom:link href="{site}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>La economía argentina, con interés: cada dato con su fuente, su contexto y su verificación a la vista.</description>
    <language>es-AR</language>
    <copyright>Con Interés</copyright>
    <lastBuildDate>{construido}</lastBuildDate>
    <ttl>60</ttl>
    <image>
      <url>{site}/assets/og-delta.png</url>
      <title>Con Interés</title>
      <link>{site}/</link>
    </image>
{items}
  </channel>
</rss>
""".format(site=SITE, construido=construido,
           items="\n".join(item(a) for a in arts))

    destino = os.path.join(ROOT, "feed.xml")
    io.open(destino, "w", encoding="utf-8").write(xml)

    con_tarjeta = sum(1 for a in arts
                      if os.path.exists(os.path.join(ROOT, "assets", "tarjetas",
                                                     a["id"] + ".png")))
    print("OK -> %s  (%d notas, %d con tarjeta)" % (destino, len(arts), con_tarjeta))
    if con_tarjeta < len(arts):
        print("  [aviso] %d sin tarjeta: corre scripts/build_tarjetas.py"
              % (len(arts) - con_tarjeta))
    return 0


if __name__ == "__main__":
    sys.exit(main())
