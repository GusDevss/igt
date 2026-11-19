#!/usr/bin/env python3
"""Genera el sitio de Integral Gym Tech en public/.

    python3 tools/build_site.py            # build completo
    python3 tools/build_site.py --fast     # sin AVIF (más rápido para desarrollo)

Entradas:
  site/templates/   plantillas Jinja2 (layout, parciales y una plantilla por página)
  site/css/         CSS propio (se concatena y minifica)
  site/js/          JS propio (se minifica con esbuild)
  site/icons/       iconos SVG (se genera un sprite solo con los usados en cada página)
  site/fonts/       fuentes WOFF2
  site/static/      archivos que se copian tal cual (enviar.php, .htaccess, robots.txt…)
  source/assets/uploads/  imágenes originales (se generan variantes WebP/AVIF responsivas)
"""
import hashlib
import html as htmlmod
import json
import os
import re
import shutil
import subprocess
import sys
import datetime

from jinja2 import Environment, FileSystemLoader, pass_context
from markupsafe import Markup
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import seo  # noqa: E402

SITE = os.path.join(ROOT, "site")
OUT = os.path.join(ROOT, "public")
UPLOADS = os.path.join(ROOT, "source", "assets", "uploads")
CACHE = os.path.join(ROOT, ".cache", "img")
FAST = "--fast" in sys.argv
TODAY = datetime.date.today().isoformat()
WIDTHS = [360, 480, 768, 1024, 1366, 1920]
ESBUILD = os.environ.get("ESBUILD") or shutil.which("esbuild") or os.path.join(ROOT, "node_modules", ".bin", "esbuild")

# ----------------------------------------------------------------------------- imágenes
_img_meta = {}


def _src_path(src):
    p = os.path.join(UPLOADS, src)
    if not os.path.exists(p):
        raise FileNotFoundError("imagen no encontrada: " + src)
    return p


def _variant(src, width, fmt):
    """Crea (con caché) una variante redimensionada; devuelve la URL pública."""
    p = _src_path(src)
    base = re.sub(r"\.[a-z0-9]+$", "", src, flags=re.I)
    name = f"{base}-{width}.{fmt}"
    out = os.path.join(OUT, "img", name)
    cache = os.path.join(CACHE, name)
    if not os.path.exists(cache) or os.path.getmtime(cache) < os.path.getmtime(p):
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        im = Image.open(p)
        has_alpha = im.mode in ("RGBA", "LA", "P") and ("transparency" in im.info or im.mode != "P")
        im = im.convert("RGBA" if has_alpha else "RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        if fmt == "webp":
            im.save(cache, "WEBP", quality=80, method=6)
        elif fmt == "avif":
            im.save(cache, "AVIF", quality=55, speed=6)
        else:
            im.save(cache, fmt.upper())
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if not os.path.exists(out):
        shutil.copy2(cache, out)
    return "/img/" + name


def img_size(src):
    if src not in _img_meta:
        with Image.open(_src_path(src)) as im:
            _img_meta[src] = im.size
    return _img_meta[src]


def picture(src, alt, sizes="100vw", cls="", loading="lazy", priority=False, width=None, height=None,
            max_w=None, attrs="", skip_mobile=False):
    """<picture> con AVIF + WebP en varios anchos. `src` es relativo a source/assets/uploads."""
    w0, h0 = img_size(src)
    top = min(max_w or w0, w0)
    widths = sorted({w for w in WIDTHS if w < top} | {top})
    fmts = ["webp"] if FAST else ["avif", "webp"]
    sources = []
    if skip_mobile:  # imagen oculta en móvil: se sirve un GIF de 1px
        sources.append('<source media="(max-width:767px)" srcset="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==">')
    for fmt in fmts:
        srcset = ", ".join(f"{_variant(src, w, fmt)} {w}w" for w in widths)
        sources.append(f'<source type="image/{fmt}" srcset="{srcset}" sizes="{sizes}">')
    fallback = _variant(src, widths[min(len(widths) - 1, 2)], "webp")
    width = width or top
    height = height or round(h0 * top / w0)
    load = 'loading="eager" fetchpriority="high"' if priority else f'loading="{loading}"'
    return Markup(
        f'<picture class="{cls}">' + "".join(sources) +
        f'<img src="{fallback}" alt="{htmlmod.escape(alt)}" width="{width}" height="{height}" {load} decoding="async" {attrs}></picture>'
    )


def img_url(src, width=1366, fmt="webp"):
    w0, _ = img_size(src)
    return _variant(src, min(width, w0), fmt)


def bg(src, big=1920, small=768, lazy=True, q=None):
    """Atributos para un fondo CSS responsivo (AVIF + WebP, grande y móvil).

    Devuelve `class="bg ..." style="--bw:...;--ba:...;--sw:...;--sa:..."`. Con lazy=True el fondo
    solo se descarga cuando la sección se acerca a la pantalla.
    """
    w0, _ = img_size(src)
    big, small = min(big, w0), min(small, w0)
    v = {
        "bw": _variant(src, big, "webp"), "sw": _variant(src, small, "webp"),
        "ba": _variant(src, big, "avif") if not FAST else _variant(src, big, "webp"),
        "sa": _variant(src, small, "avif") if not FAST else _variant(src, small, "webp"),
    }
    style = ";".join(f"--{k}:url({u})" for k, u in v.items())
    cls = "bg" + (" bg--lazy" if lazy else "")
    return Markup(f'data-bgcls="{cls}" style="{style}"')


def bg_preload(src, big=1920, small=768):
    """<link rel=preload> para el fondo principal (LCP), uno por tamaño de pantalla."""
    w0, _ = img_size(src)
    fmt = "webp" if FAST else "avif"
    a = _variant(src, min(small, w0), fmt)
    b = _variant(src, min(big, w0), fmt)
    return Markup(
        f'<link rel="preload" as="image" href="{a}" type="image/{fmt}" media="(max-width:767px)" fetchpriority="high">'
        f'<link rel="preload" as="image" href="{b}" type="image/{fmt}" media="(min-width:768px)" fetchpriority="high">')


# ----------------------------------------------------------------------------- catálogos PDF
_catalog_cache = {}


def catalog(pdf, title):
    """Renderiza las páginas del PDF a WebP (dos tamaños) y devuelve los datos para el visor."""
    if pdf in _catalog_cache:
        return _catalog_cache[pdf]
    src = _src_path(pdf)
    name = os.path.splitext(os.path.basename(pdf))[0].lower()
    cache_dir = os.path.join(CACHE, "catalogos", name)
    out_dir = os.path.join(OUT, "catalogos", name)
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    stamp = os.path.join(cache_dir, ".ok")
    if not os.path.exists(stamp) or os.path.getmtime(stamp) < os.path.getmtime(src):
        for f in os.listdir(cache_dir):
            os.remove(os.path.join(cache_dir, f))
        subprocess.run(["pdftoppm", "-r", "160", "-png", src, os.path.join(cache_dir, "p")], check=True)
        for f in sorted(os.listdir(cache_dir)):
            if not f.endswith(".png"):
                continue
            n = int(re.search(r"(\d+)", f).group(1))
            im = Image.open(os.path.join(cache_dir, f)).convert("RGB")
            for h, q in ((1300, 78), (700, 74)):
                r = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
                r.save(os.path.join(cache_dir, f"{n:02d}-{h}.webp"), "WEBP", quality=q, method=6)
            os.remove(os.path.join(cache_dir, f))
        open(stamp, "w").write("ok")
    files = sorted(f for f in os.listdir(cache_dir) if f.endswith(".webp"))
    for f in files:
        shutil.copy2(os.path.join(cache_dir, f), os.path.join(out_dir, f))
    shutil.copy2(src, os.path.join(out_dir, os.path.basename(pdf)))
    count = len([f for f in files if f.endswith("-700.webp")])
    with Image.open(os.path.join(cache_dir, "01-700.webp")) as im:
        ratio = round(im.width / im.height, 4)
    # texto de cada página para el texto alternativo (SEO)
    txt = subprocess.run(["pdftotext", "-layout", src, "-"], capture_output=True, text=True).stdout.split("\f")
    alts = []
    for i in range(count):
        words = re.sub(r"\s+", " ", txt[i] if i < len(txt) else "").strip()
        words = re.sub(r"BUGE®?\s*\|?\s*(CATALOGO \d{4}|[A-ZÁÉÍÓÚ ]+)?", "", words).strip()
        alts.append(f"{title} – página {i + 1}" + (f": {words[:140]}" if words else ""))
    data = {"base": f"/catalogos/{name}/", "count": count, "ratio": ratio,
            "pdf": f"/catalogos/{name}/{os.path.basename(pdf)}", "alts": alts, "title": title}
    _catalog_cache[pdf] = data
    return data


# ----------------------------------------------------------------------------- iconos
_icons_used = set()


SPRITE_URL = {"url": ""}


_ratio = {}


def icon(name, cls="", label=None):
    """Icono del sprite. Alto = 1em (se controla con font-size); ancho según la proporción del glifo."""
    _icons_used.add(name)
    if name not in _ratio:
        vb = re.search(r'viewBox="([^"]+)"', open(os.path.join(SITE, "icons", name + ".svg")).read()).group(1).split()
        _ratio[name] = round(float(vb[2]) / float(vb[3]), 3)
    aria = f'role="img" aria-label="{htmlmod.escape(label)}"' if label else 'aria-hidden="true"'
    return Markup(f'<svg class="ic {cls}" width="{_ratio[name]}em" height="1em" {aria}><use href="{SPRITE_URL["url"]}#i-{name}"></use></svg>')


def sprite(names):
    parts = []
    for n in sorted(names):
        svg = open(os.path.join(SITE, "icons", n + ".svg")).read()
        vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
        root = re.match(r"<svg[^>]*>", svg.strip()).group(0)
        extra = "".join(f' {a}="{v}"' for a, v in re.findall(r'\b(fill|stroke)="([^"]+)"', root))
        inner = re.sub(r"^<svg[^>]*>|</svg>$", "", svg.strip())
        parts.append(f'<symbol id="i-{n}" viewBox="{vb}"{extra}>{inner}</symbol>')
    return '<svg xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


def build_sprite():
    names = [f[:-4] for f in os.listdir(os.path.join(SITE, "icons")) if f.endswith(".svg")]
    data = sprite(names)
    h = hashlib.md5(data.encode()).hexdigest()[:8]
    rel = f"/assets/icons.{h}.svg"
    open(os.path.join(OUT, rel.lstrip("/")), "w").write(data)
    SPRITE_URL["url"] = rel


def derived():
    """Imágenes fijas usadas desde CSS u Open Graph."""
    d = os.path.join(OUT, "img")
    os.makedirs(d, exist_ok=True)
    # imagen para compartir en redes (1200x630)
    og = Image.new("RGB", (1200, 630), (17, 14, 16))
    hero = Image.open(_src_path("2023/09/bg1-1.png")).convert("RGB")
    hero = hero.resize((1200, round(hero.height * 1200 / hero.width)))
    og.paste(hero.crop((0, 0, 1200, 630)), (0, 0))
    eq = Image.open(_src_path("2026/09/igt-jungla-buge.webp")).convert("RGBA")
    eq.thumbnail((640, 520))
    og.paste(eq, (560, 70), eq)
    logo = Image.open(os.path.join(SITE, "static", "img", "logo-igt.png")).convert("RGBA").resize((356, 160))
    og.paste(logo, (80, 235), logo)
    og.save(os.path.join(d, "og-igt.jpg"), "JPEG", quality=84, optimize=True)


# ----------------------------------------------------------------------------- CSS / JS
def run_esbuild(entry, out, loader=None):
    args = [ESBUILD, entry, "--minify", "--outfile=" + out, "--log-level=warning", "--target=es2018,chrome90,safari14"]
    if entry.endswith(".js"):
        args.append("--bundle")
    if loader:
        args.append(loader)
    subprocess.run(args, check=True)


def build_css(extra=False):
    """CSS del sitio. Con extra=True incluye también shop.css (solo páginas de la tienda)."""
    order = [l.strip() for l in open(os.path.join(SITE, "css", "_order.txt")) if l.strip() and not l.startswith("#")]
    if not extra:
        order = [o for o in order if o != "shop.css"]
    tmp = os.path.join(ROOT, ".cache", "bundle-shop.css" if extra else "bundle.css")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    with open(tmp, "w") as f:
        for name in order:
            f.write(f"/* {name} */\n" + open(os.path.join(SITE, "css", name)).read() + "\n")
    out = tmp.replace(".css", ".min.css")
    run_esbuild(tmp, out)
    return open(out).read()


def build_js():
    res = {}
    for name in ("main.js", "flipbook.js", "shop.js"):
        src = os.path.join(SITE, "js", name)
        if not os.path.exists(src):
            continue
        data = open(src).read()
        h = hashlib.md5(data.encode()).hexdigest()[:8]
        rel = f"/assets/js/{name[:-3]}.{h}.js"
        run_esbuild(src, os.path.join(OUT, rel.lstrip("/")))
        res[name] = rel
    return res


# ----------------------------------------------------------------------------- tienda
SHOP = json.load(open(os.path.join(SITE, "data", "productos.json"), encoding="utf-8"))
CATS = SHOP["categorias"]
PRODUCTS = SHOP["productos"]
for _p in PRODUCTS:
    _p.setdefault("imagenes", [])
    _p.setdefault("musculos", [])
    _p.setdefault("ideal", [])
    _p.setdefault("ficha", {})
    _p.setdefault("venta", "pieza")
    _p.setdefault("destacado", False)
PRODUCTS_BY_SLUG = {p["slug"]: p for p in PRODUCTS}


def _muscles():
    from collections import Counter
    c = Counter(m for p in PRODUCTS for m in p["musculos"] if m != "Sistema cardiovascular")
    return [m for m, n in c.most_common(10)]


def register_shop_seo():
    """Agrega a seo.PAGES la página de catálogo y una entrada por producto."""
    seo.PAGES["productos"] = (
        "Productos | Tienda de Equipo para Gimnasio en Querétaro | Integral Gym Tech",
        f"Catálogo de {len(PRODUCTS)} equipos para gimnasio en existencia: caminadoras, elípticas, máquinas de fuerza, "
        "racks, máquinas Smith, bancos, mancuernas y accesorios. Filtra por categoría y solicita tu cotización en línea.",
        ["tienda de equipo para gimnasio", "comprar equipo de gimnasio", "catálogo de aparatos de gimnasio",
         "equipo de gimnasio en existencia", "máquinas de gimnasio en venta", "precio equipo de gimnasio Querétaro"],
        "Productos", "CollectionPage", None)
    for p in PRODUCTS:
        cat = CATS[p["categoria"]]["nombre"]
        img = ("/img/" + re.sub(r"\.[a-z0-9]+$", "", p["imagenes"][0]) + "-1024.webp") if p["imagenes"] else None
        seo.PAGES["productos/" + p["slug"]] = (
            (f"{p['nombre']} | {cat} para gimnasio | Integral Gym Tech" if len(p['nombre']) + len(cat) < 28
             else f"{p['nombre']} | Integral Gym Tech"),
            (p["resumen"] + f" Equipo de {cat.lower()} de grado comercial en Querétaro con envío a todo México. Cotiza en línea.")[:300],
            [p["nombre"].lower(), f"{p['nombre'].lower()} precio", f"{cat.lower()} para gimnasio",
             f"comprar {p['nombre'].lower()}", f"{p['nombre'].lower()} Querétaro"] + [m.lower() for m in p["musculos"][:3]],
            p["nombre"], "Product", img)


# ----------------------------------------------------------------------------- páginas
NAV = [
    {"label": "IGT", "href": "/nosotros/"},
    {"label": "Servicios", "children": [
        ("Mantenimiento de equipo", "/mantenimiento-de-equipo/", "fal-tools"),
        ("Arrendamiento", "/arrendamiento/", "far-piggy-bank"),
        ("Diseño de espacios", "/diseno-de-espacios/", "far-ruler-triangle"),
    ]},
    {"label": "Productos", "href": "/productos/", "children": [
        ("Todos los productos", "/productos/", "far-layer-group"),
        ("Cardio", "/cardio/", "far-heartbeat"),
        ("Peso libre", "/peso-libre/", "far-dumbbell"),
        ("Peso integrado", "/peso-integrado/", "far-weight-hanging"),
        ("Multifuncionales", "/multifuncionales/", "far-layer-group"),
        ("Pilates", "/pilates/", "fal-child"),
        ("Accesorios", "/accesorios/", "fas-dumbbell"),
        ("Reacondicionado", "/reacondicionado/", "far-recycle"),
    ]},
    {"label": "Tipo de proyecto", "children": [
        ("Apertura o remodelación de gimnasio", "/gimnasio-apertura-remodelacion/", "far-dumbbell"),
        ("Gimnasio en casa", "/gimnasio-casa/", "far-house-return"),
        ("Condominios / Residenciales", "/condominios-residenciales/", "fal-building"),
        ("Clínicas de fisioterapia", "/clinicas-fisioterapia/", "far-hospital-user"),
        ("Estudio de pilates", "/estudio-pilates/", "far-child"),
        ("Hoteles", "/hoteles/", "far-hotel"),
        ("Empresas", "/empresas/", "far-briefcase"),
        ("Universidades", "/universidades/", "far-graduation-cap"),
        ("Gubernamentales", "/gubernamentales/", "far-landmark"),
    ]},
]


def json_ld(slug):
    title, desc, kws, crumb, stype, ogimg = seo.PAGES[slug]
    S = seo.SITE
    url = S + ("/" if slug == "index" else f"/{slug}/")
    b = seo.BUSINESS
    org = S + "/#organization"
    img = S + (ogimg or "/img/og-igt.jpg")
    graph = [
        {"@type": ["Organization", "LocalBusiness", "SportingGoodsStore"], "@id": org,
         "name": b["name"], "legalName": b["legalName"], "alternateName": ["IGT", "IntegralGYMTech"],
         "url": S + "/", "logo": S + "/img/logo-igt.png", "image": S + "/img/og-igt.jpg",
         "description": seo.PAGES["index"][1], "telephone": b["telephone"], "email": b["email"],
         "foundingDate": "2008", "priceRange": "$$",
         "address": {"@type": "PostalAddress", "streetAddress": b["street"], "addressLocality": b["locality"],
                     "addressRegion": b["region"], "postalCode": b["postal"], "addressCountry": b["country"]},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                        "opens": "09:00", "closes": "18:00"}],
         "areaServed": [{"@type": "State", "name": "Querétaro"}, {"@type": "City", "name": "San Luis Potosí"},
                        {"@type": "City", "name": "León, Guanajuato"}, {"@type": "Country", "name": "México"}],
         "hasMap": b["maps"], "sameAs": [b["facebook"], b["instagram"]],
         "brand": {"@type": "Brand", "name": "BUGE Fitness"},
         "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "74", "bestRating": "5"},
         "knowsAbout": ["Equipo para gimnasio", "Equipamiento de gimnasios", "Mantenimiento de equipo fitness",
                        "Arrendamiento de equipo de gimnasio", "Diseño de gimnasios", "Pilates",
                        "Equipamiento para gimnasios comerciales", "Reformer de Pilates profesional"]},
        {"@type": "WebSite", "@id": S + "/#website", "url": S + "/", "name": "IntegralGYMTech",
         "inLanguage": "es-MX", "publisher": {"@id": org}},
        {"@type": stype if stype in ("WebPage", "AboutPage", "CollectionPage") else "WebPage",
         "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "es-MX",
         "isPartOf": {"@id": S + "/#website"}, "about": {"@id": org}, "dateModified": TODAY,
         "primaryImageOfPage": {"@type": "ImageObject", "url": img}, "breadcrumb": {"@id": url + "#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement":
            [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": S + "/"}] +
            ([] if slug == "index" else [{"@type": "ListItem", "position": 2, "name": crumb, "item": url}])},
    ]
    if slug.startswith("productos/"):
        pr = PRODUCTS_BY_SLUG[slug.split("/", 1)[1]]
        cat = CATS[pr["categoria"]]["nombre"]
        graph[-1]["itemListElement"] = [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": S + "/"},
            {"@type": "ListItem", "position": 2, "name": "Productos", "item": S + "/productos/"},
            {"@type": "ListItem", "position": 3, "name": cat, "item": S + "/productos/?categoria=" + pr["categoria"]},
            {"@type": "ListItem", "position": 4, "name": pr["nombre"], "item": url}]
        graph[2]["@type"] = "ItemPage"
        node = {"@type": "Product", "@id": url + "#product", "name": pr["nombre"], "description": " ".join(pr["descripcion"]),
                "category": cat, "url": url, "sku": "IGT-" + pr["slug"].upper()[:24],
                "brand": {"@type": "Brand", "name": "Integral Gym Tech"},
                "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in pr["ficha"].items()]}
        if pr["imagenes"]:
            node["image"] = [S + "/img/" + re.sub(r"\.[a-z0-9]+$", "", i) + "-1024.webp" for i in pr["imagenes"]]
        graph.append(node)
    if slug == "productos":
        graph.append({"@type": "ItemList", "name": "Catálogo de equipo para gimnasio", "numberOfItems": len(PRODUCTS),
                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["nombre"],
                                           "url": S + "/productos/" + p["slug"] + "/"} for i, p in enumerate(PRODUCTS)]})
    if stype == "Service":
        graph.append({"@type": "Service", "name": crumb, "serviceType": crumb, "description": desc,
                      "provider": {"@id": org}, "areaServed": "México", "url": url})
    if stype == "CollectionPage":
        graph.append({"@type": "OfferCatalog", "name": "Catálogo " + crumb + " BUGE", "url": url,
                      "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Product", "name": k[:1].upper() + k[1:],
                                                                             "brand": {"@type": "Brand", "name": "BUGE"}}}
                                          for k in kws[:6]]})
    return Markup(json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/"))


def merge_bg_class(html):
    """Une data-bgcls="bg ..." con el class="..." del mismo elemento."""
    def fix(m):
        tag = m.group(0)
        extra = re.search(r'data-bgcls="([^"]*)"', tag).group(1)
        tag = re.sub(r'\s*data-bgcls="[^"]*"', "", tag)
        if re.search(r'\bclass="', tag):
            return re.sub(r'\bclass="([^"]*)"', lambda c: f'class="{c.group(1)} {extra}"', tag, count=1)
        return tag[:-1] + f' class="{extra}">'
    return re.sub(r"<[a-z][^>]*data-bgcls=\"[^\"]*\"[^>]*>", fix, html)


def minify_html(s):
    # elimina comentarios y espacios entre etiquetas (sin tocar <pre>/<textarea>/<script>)
    s = re.sub(r"<!--(?!\[).*?-->", "", s, flags=re.S)
    s = re.sub(r">\s+<", "> <", s)
    s = re.sub(r"\n\s*", "\n", s)
    return s.strip() + "\n"


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    # estáticos
    shutil.copytree(os.path.join(SITE, "static"), OUT, dirs_exist_ok=True)
    shutil.copytree(os.path.join(SITE, "fonts"), os.path.join(OUT, "assets", "fonts"))
    derived()
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    build_sprite()
    css = build_css()
    css_shop = build_css(extra=True)
    js = build_js()
    env = Environment(loader=FileSystemLoader(os.path.join(SITE, "templates")), autoescape=True,
                      trim_blocks=True, lstrip_blocks=True)
    env.filters["faq_item"] = lambda qa: {"@type": "Question", "name": qa[0],
                                          "acceptedAnswer": {"@type": "Answer", "text": qa[1]}}
    env.globals.update(catalog=catalog, picture=picture, img_url=img_url, img_size=img_size, bg=bg, bg_preload=bg_preload, icon=icon, NAV=NAV,
                       BUSINESS=seo.BUSINESS, SITE_URL=seo.SITE, YEAR=datetime.date.today().year, JS=js,
                       CATS=CATS, PRODUCTS=PRODUCTS, MUSCLES=_muscles(),
                       PRODUCTS_SORTED=sorted(PRODUCTS, key=lambda p: (not p["destacado"], not p["imagenes"])), ITEMLIST="", PRODUCT_LD="")
    register_shop_seo()
    pages = sorted(f[:-5] for f in os.listdir(os.path.join(SITE, "templates", "pages")) if f.endswith(".html"))
    for slug in pages:
        _icons_used.clear()
        title, desc, kws, crumb, stype, ogimg = seo.PAGES[slug]
        url = seo.SITE + ("/" if slug == "index" else f"/{slug}/")
        ctx = dict(slug=slug, path=("/" if slug == "index" else f"/{slug}/"), title=title, description=desc,
                   keywords=", ".join(dict.fromkeys(kws + seo.BASE_KW)), canonical=url, crumb=crumb,
                   og_image=seo.SITE + (ogimg or "/img/og-igt.jpg"), json_ld=json_ld(slug),
                   css=Markup(css_shop if slug == "productos" else css))
        out = env.get_template(f"pages/{slug}.html").render(**ctx)
        out = merge_bg_class(out)
        out = minify_html(out)
        dest = os.path.join(OUT, "404.html" if slug == "404" else ("index.html" if slug == "index" else f"{slug}/index.html"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w").write(out)
        print(f"  {dest[len(ROOT)+1:]:45} {len(out)//1024:4d} KB")
    # páginas de producto
    tpl = env.get_template("layouts/producto.html")
    for p in PRODUCTS:
        _icons_used.clear()
        slug = "productos/" + p["slug"]
        title, desc, kws, crumb, stype, ogimg = seo.PAGES[slug]
        url = f"{seo.SITE}/{slug}/"
        same = [r for r in PRODUCTS if r["categoria"] == p["categoria"] and r is not p]
        same.sort(key=lambda r: (not r["imagenes"], not r["destacado"]))
        related = same[:4]
        if len(related) < 4:
            related += [r for r in PRODUCTS if r is not p and r not in related and r["imagenes"]][:4 - len(related)]
        ctx = dict(slug=slug, path="/productos/", title=title, description=desc,
                   keywords=", ".join(dict.fromkeys(kws + seo.BASE_KW)), canonical=url, crumb=crumb,
                   og_image=seo.SITE + (ogimg or "/img/og-igt.jpg"), json_ld=json_ld(slug), css=Markup(css_shop),
                   p=p, related=related)
        out = minify_html(merge_bg_class(tpl.render(**ctx)))
        dest = os.path.join(OUT, slug, "index.html")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w").write(out)
    print(f"  {len(PRODUCTS)} páginas de producto en public/productos/")
    write_sitemap(pages + ["productos/" + p["slug"] for p in PRODUCTS])


def write_sitemap(pages):
    rows = []
    for s in pages:
        if s == "404":
            continue
        loc = seo.SITE + ("/" if s == "index" else f"/{s}/")
        pr = "1.0" if s == "index" else ("0.3" if s in ("terminos-y-condiciones", "politica-devoluciones") else ("0.7" if s.startswith("productos/") else "0.8"))
        rows.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{pr}</priority></url>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows) + "\n</urlset>\n")


if __name__ == "__main__":
    main()
