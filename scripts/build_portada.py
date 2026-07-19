#!/usr/bin/env python3
"""
build_portada.py — Regenera la portada (index.html) del portal Con Interés
a partir de los manifiestos data/articulos.json y data/cola.json.

Lo ejecuta el agente Publicador en cada publicación. Determinista:
mismos manifiestos -> misma portada.

Uso:  python3 scripts/build_portada.py
"""
import json, os, datetime
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# URL base pública del sitio. Cuando se configure un dominio propio,
# cambiar SOLO esta línea (ej. "https://deltadiario.com").
SITE = "https://coninteres.com"

def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)

art = load("articulos.json")
cola = load("cola.json")
portal = art["portal"]
articulos = sorted(art["articulos"], key=lambda a: (a["fecha"], a.get("hora","")), reverse=True)
borradores = cola.get("borradores", [])

# ---- helpers -----------------------------------------------------------
MESES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
DIAS = ["LUN","MAR","MIÉ","JUE","VIE","SÁB","DOM"]
try:
    _md = datetime.date.fromisoformat(portal["actualizado"][:10])
    FECHA_MASTHEAD = f"{DIAS[_md.weekday()]} {_md.day} · {MESES[_md.month-1].upper()} · {_md.year}"
except Exception:
    FECHA_MASTHEAD = ""
def fecha_bonita(f):
    try:
        d = datetime.date.fromisoformat(f)
        return f"{d.day} {MESES[d.month-1]} {d.year}"
    except Exception:
        return f

def actualizado_hace(iso):
    try:
        t = datetime.datetime.fromisoformat(iso)
        return t.strftime("%d/%m %H:%M")
    except Exception:
        return iso

SEC_COLOR = {
    "ECONOMÍA": "#0E7C86", "MERCADOS": "#0A5C63", "MUNDO": "#7A5CC4",
    # compat / fallback
    "PLATA": "#0E7C86", "MÁQUINAS": "#C4701F", "CIENCIA": "#2E8B6F",
    "EL MUNDO EN NÚMEROS": "#7A5CC4", "DEPORTES": "#C0392B", "NEGOCIOS": "#0A5C63",
    "TECNOLOGÍA": "#C4701F",
}

def chip_verif(v):
    if v == "verificada":
        return '<span class="verif ok">&#10003; Verificada</span>'
    if v == "pendiente":
        return '<span class="verif pend">&#9651; En verificación</span>'
    return f'<span class="verif">{escape(v)}</span>'

# ---- lead + grid -------------------------------------------------------
def card_lead(a):
    sc = SEC_COLOR.get(a["seccion"], "#0E7C86")
    num = a.get('numero','')
    # el número ancla se achica según su longitud para no desbordar la caja
    n = len(num)
    fs = 64 if n <= 5 else (50 if n <= 8 else 38)
    return f"""
    <a class="lead" data-sec="{escape(a['seccion'])}" href="{escape(a['archivo'])}">
      <div class="lead-num" style="--sc:{sc}">
        <span class="ln-big" style="font-size:{fs}px">{escape(num)}</span>
        <span class="ln-lab">{escape(a.get('numero_label',''))}</span>
      </div>
      <div class="lead-body">
        <div class="kick" style="color:{sc}">{escape(a['seccion'])} <span>/ {escape(a.get('formato',''))}</span></div>
        <h2>{escape(a['titulo'])}</h2>
        <p>{escape(a['bajada'])}</p>
        <div class="meta">{chip_verif(a.get('verificacion',''))}<span class="dot"></span>{escape(a.get('lectura',''))}<span class="dot"></span>{fecha_bonita(a['fecha'])}</div>
      </div>
    </a>"""

def card(a):
    sc = SEC_COLOR.get(a["seccion"], "#0E7C86")
    return f"""
    <a class="card" data-sec="{escape(a['seccion'])}" href="{escape(a['archivo'])}">
      <div class="kick" style="color:{sc}">{escape(a['seccion'])}</div>
      <h3>{escape(a['titulo'])}</h3>
      <div class="card-num" style="--sc:{sc}"><b>{escape(a.get('numero',''))}</b> {escape(a.get('numero_label',''))}</div>
      <div class="meta">{chip_verif(a.get('verificacion',''))}<span class="dot"></span>{fecha_bonita(a['fecha'])}</div>
    </a>"""

lead_html = card_lead(articulos[0]) if articulos else '<p class="empty">Todavía no hay notas publicadas.</p>'
grid_html = "\n".join(card(a) for a in articulos[1:]) or '<p class="empty small">La redacción publicará más notas en las próximas horas.</p>'

# cola panel
if borradores:
    filas = "\n".join(
        f"""<li><span class="q-sec">{escape(b.get('seccion',''))}</span>
        <span class="q-tit">{escape(b['titulo'])}</span>
        <span class="q-badge">En revisión</span></li>""" for b in borradores)
    cola_html = f"""
    <section class="cola">
      <div class="cola-head"><span class="pulse"></span> Cola de revisión · {len(borradores)} borrador(es) esperando tu OK</div>
      <ul class="q-list">{filas}</ul>
      <p class="cola-foot">Los agentes ya investigaron y verificaron estas notas. Se publican recién cuando las aprobás.</p>
    </section>"""
else:
    cola_html = ""

secciones_nav = '<button class="sec-chip active" data-filter="all" style="--sc:#16130F">Todas</button>' + "".join(
    f'<button class="sec-chip" data-filter="{escape(s)}" style="--sc:{SEC_COLOR.get(s,"#0E7C86")}">{escape(s)}</button>' for s in art.get("secciones", []))

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(portal['nombre'])} — {escape(portal['tagline'])}</title>
<meta name="description" content="{escape(portal['descripcion'])}">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="canonical" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{escape(portal['nombre'])}">
<meta property="og:title" content="{escape(portal['nombre'])} — {escape(portal['tagline'])}">
<meta property="og:description" content="{escape(portal['descripcion'])}">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/assets/og-delta.png">
<meta property="og:locale" content="es_AR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{escape(portal['nombre'])} — {escape(portal['tagline'])}">
<meta name="twitter:description" content="{escape(portal['descripcion'])}">
<meta name="twitter:image" content="{SITE}/assets/og-delta.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{{
    --paper:#FAF8F4;--ink:#16130F;--ink-soft:#3C3833;--teal:#0E7C86;--teal-deep:#0A5C63;
    --amber:#C4701F;--red:#C0392B;--green:#2E8B6F;--muted:#6B6560;--faint:#8A847C;
    --grid:#E7E1D7;--rule:#DCD6CC;--card:#FFFFFF;--card-edge:#EAE4DA;
    --serif:"Source Serif 4",Georgia,serif;--sans:"Inter",system-ui,sans-serif;--mono:"IBM Plex Mono",monospace;
  }}
  *{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
  body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.6;-webkit-font-smoothing:antialiased}}
  .wrap{{max-width:1080px;margin:0 auto;padding:0 24px}}
  a{{text-decoration:none;color:inherit}}

  .masthead{{border-bottom:2px solid var(--ink)}}
  .masthead .wrap{{display:flex;align-items:center;justify-content:space-between;padding:16px 24px}}
  .brand{{font-family:var(--serif);font-weight:700;font-size:34px;letter-spacing:-.01em;display:flex;align-items:center;gap:10px}}
  .brand .tri{{color:var(--teal);font-size:28px;transform:translateY(-2px)}}
  .brand .tag{{font-family:var(--mono);font-size:11px;color:var(--muted);letter-spacing:.14em;text-transform:uppercase;border-left:1px solid var(--rule);padding-left:10px;font-weight:500}}
  .mh-right{{text-align:right;font-family:var(--mono);font-size:11px;color:var(--muted);line-height:1.6}}
  .mh-right b{{color:var(--ink)}}

  .concept{{background:var(--ink);color:var(--paper)}}
  .concept .wrap{{display:flex;align-items:center;gap:18px;padding:11px 24px;flex-wrap:wrap;font-size:13px}}
  .concept .k{{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#4FC0A4;font-weight:600}}
  .concept .item{{color:#CFC9BF}} .concept .item b{{color:#fff;font-weight:600}}
  .concept .sep{{color:#3E3A34}}

  .secnav{{border-bottom:1px solid var(--rule)}}
  .secnav .wrap{{display:flex;gap:8px;padding:12px 24px;flex-wrap:wrap}}
  .sec-chip{{font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:var(--sc);background:var(--paper);border:1px solid var(--card-edge);padding:6px 13px;border-radius:999px;font-weight:600;cursor:pointer;transition:.15s}}
  .sec-chip:hover{{border-color:var(--sc)}}
  .sec-chip.active{{background:var(--sc);color:#fff;border-color:var(--sc)}}
  .lead.is-hidden,.card.is-hidden{{display:none}}

  main{{padding:30px 0 20px}}
  .learn-link{{margin-left:auto;font-family:var(--mono);font-size:12px;color:var(--teal-deep);text-decoration:none;display:flex;align-items:center;gap:7px;white-space:nowrap;font-weight:600}}
  .learn-link b{{background:var(--amber);color:#fff;font-size:9px;letter-spacing:.06em;text-transform:uppercase;padding:2px 6px;border-radius:999px;font-weight:600}}
  .learn-link:hover{{color:var(--teal)}}
  @media(max-width:560px){{.learn-link{{margin-left:0;width:100%;padding-top:6px}}}}
  .empty{{color:var(--muted);font-family:var(--mono);font-size:14px;padding:40px 0}} .empty.small{{padding:14px}}

  .lead{{display:grid;grid-template-columns:300px 1fr;gap:30px;border-bottom:1px solid var(--rule);padding-bottom:30px;margin-bottom:30px;align-items:center}}
  .lead-num{{background:var(--ink);border-radius:16px;padding:32px 26px;display:flex;flex-direction:column;justify-content:center;min-height:210px}}
  .lead-num .ln-big{{font-family:var(--mono);font-weight:600;font-size:64px;line-height:1;letter-spacing:-.03em;color:#fff}}
  .lead-num .ln-lab{{font-size:13px;color:#B9B3A9;margin-top:12px;line-height:1.45}}
  .lead-num{{border-top:4px solid var(--sc)}}
  .lead-body .kick,.card .kick{{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;margin-bottom:12px}}
  .lead-body .kick span{{color:var(--faint)}}
  .lead-body h2{{font-family:var(--serif);font-weight:700;font-size:34px;line-height:1.14;letter-spacing:-.01em;margin:0 0 14px}}
  .lead-body p{{font-size:17px;color:var(--ink-soft);margin:0 0 16px;max-width:60ch}}
  .lead:hover h2{{color:var(--teal-deep)}}

  .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}}
  .card{{background:var(--card);border:1px solid var(--card-edge);border-radius:14px;padding:20px;display:flex;flex-direction:column;transition:.15s}}
  .card:hover{{transform:translateY(-2px);border-color:var(--teal)}}
  .card h3{{font-family:var(--serif);font-weight:600;font-size:20px;line-height:1.25;margin:0 0 14px;flex:1}}
  .card-num{{font-family:var(--mono);font-size:12px;color:var(--muted);border-left:3px solid var(--sc);padding-left:10px;margin-bottom:14px}}
  .card-num b{{color:var(--ink);font-size:15px}}

  .meta{{display:flex;align-items:center;gap:10px;font-family:var(--mono);font-size:11px;color:var(--muted);flex-wrap:wrap}}
  .meta .dot{{width:3px;height:3px;border-radius:50%;background:var(--faint)}}
  .verif{{font-weight:600}} .verif.ok{{color:var(--green)}} .verif.pend{{color:var(--amber)}}

  .cola{{background:#F3EFE7;border:1px solid var(--card-edge);border-left:3px solid var(--amber);border-radius:12px;padding:20px 22px;margin:34px 0 10px}}
  .cola-head{{font-family:var(--mono);font-size:13px;font-weight:600;color:var(--ink);display:flex;align-items:center;gap:9px;margin-bottom:14px}}
  .pulse{{width:9px;height:9px;border-radius:50%;background:var(--amber);box-shadow:0 0 0 0 rgba(196,112,31,.5);animation:p 2s infinite}}
  @keyframes p{{70%{{box-shadow:0 0 0 8px rgba(196,112,31,0)}}100%{{box-shadow:0 0 0 0 rgba(196,112,31,0)}}}}
  .q-list{{list-style:none;margin:0;padding:0}}
  .q-list li{{display:flex;align-items:center;gap:12px;padding:11px 0;border-top:1px dashed var(--rule);font-size:15px}}
  .q-sec{{font-family:var(--mono);font-size:10px;letter-spacing:.08em;color:var(--amber);font-weight:600;flex:0 0 auto}}
  .q-tit{{flex:1;color:var(--ink-soft)}}
  .q-badge{{font-family:var(--mono);font-size:10px;background:var(--amber);color:#fff;padding:3px 9px;border-radius:999px;font-weight:600}}
  .cola-foot{{font-size:12px;color:var(--muted);margin:12px 0 0}}

  footer{{border-top:2px solid var(--ink);margin-top:44px;padding:26px 0 60px}}
  footer .wrap{{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}}
  .f-brand{{font-family:var(--serif);font-weight:700;font-size:20px}} .f-brand .tri{{color:var(--teal)}}
  .f-desc{{font-size:13px;color:var(--muted);max-width:480px;margin-top:6px;line-height:1.55}}
  .f-meta{{font-family:var(--mono);font-size:11px;color:var(--faint);text-align:right;line-height:1.8}}

  @media(max-width:820px){{
    .grid{{grid-template-columns:1fr 1fr}} .lead{{grid-template-columns:1fr}} .lead-num{{min-height:150px}}
    .lead-body h2{{font-size:27px}} .brand{{font-size:28px}}
  }}
  @media(max-width:560px){{ .grid{{grid-template-columns:1fr}} .concept .wrap{{gap:8px 14px}} }}
</style>
</head>
<body>

<header class="masthead">
  <div class="wrap">
    <div class="brand"><span class="tri">%</span>{escape(portal['nombre'])}<span class="tag">{escape(portal['tagline'])}</span></div>
    <div class="mh-right">
      <div>{FECHA_MASTHEAD}</div>
    </div>
  </div>
</header>

<nav class="secnav"><div class="wrap">{secciones_nav}<a class="learn-link" href="aprender.html">% Modo Aprendizaje <b>beta</b> →</a></div></nav>

<main class="wrap">
  {lead_html}
  <div class="grid">
    {grid_html}
  </div>
  {cola_html}
</main>

<footer>
  <div class="wrap">
    <div>
      <div class="f-brand"><span class="tri">%</span> {escape(portal['nombre'])}</div>
      <div class="f-desc">{escape(portal['descripcion'])}</div>
      <div style="margin-top:10px"><a href="como-trabajamos.html" style="font-family:var(--mono);font-size:12px;color:var(--teal-deep);text-decoration:none;border-bottom:1px solid var(--grid)">% Cómo trabajamos — método, IA y ética →</a></div>
    </div>
  </div>
</footer>

<script>
(function(){{
  var chips=document.querySelectorAll('.sec-chip');
  var lead=document.querySelector('.lead');
  var cards=document.querySelectorAll('.card');
  function match(el,f){{ return f==='all' || (el && el.getAttribute('data-sec')===f); }}
  chips.forEach(function(c){{
    c.addEventListener('click',function(){{
      chips.forEach(function(x){{x.classList.remove('active');}});
      c.classList.add('active');
      var f=c.getAttribute('data-filter');
      if(lead){{ lead.classList.toggle('is-hidden', !match(lead,f)); }}
      cards.forEach(function(cd){{ cd.classList.toggle('is-hidden', !match(cd,f)); }});
    }});
  }});
}})();
</script>

</body>
</html>"""

out = os.path.join(ROOT, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)

# ---- sitemap.xml (para SEO) --------------------------------------------
urls = [f"  <url><loc>{SITE}/</loc><changefreq>hourly</changefreq><priority>1.0</priority></url>"]
for a in articulos:
    urls.append(
        f"  <url><loc>{SITE}/{escape(a['archivo'])}</loc>"
        f"<lastmod>{a['fecha']}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>")
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' \
          + "\n".join(urls) + "\n</urlset>\n"
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"OK -> {out}  ({len(articulos)} notas, {len(borradores)} en cola)  + sitemap.xml")
