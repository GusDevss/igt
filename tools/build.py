#!/usr/bin/env python3
"""Genera el sitio estático en public/ a partir de source/.

  python3 tools/build.py

- source/pages/*.html  : HTML renderizado del sitio WordPress original
- source/assets/       : recursos descargados (tools/fetch_assets.py)
- source/static/       : archivos propios (formulario PHP, JS, .htaccess, robots...)
"""
import base64
import datetime
import html as htmlmod
import json
import os
import re
import shutil
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
from urlmap import ROOT, ASSETS, URL_RE, local_path, normalize  # noqa: E402
import seo  # noqa: E402

SRC_PAGES = os.path.join(ROOT, "source", "pages")
STATIC = os.path.join(ROOT, "source", "static")
OUT = os.path.join(ROOT, "public")
SITE = seo.SITE
TODAY = datetime.date.today().isoformat()

PAGE_ALIASES = {"/mantenimiento": "/mantenimiento-de-equipo/"}

# ---------------------------------------------------------------- scripts/estilos que se eliminan
DROP_SCRIPT_IDS = re.compile(
    r"^(wp-i18n|wp-hooks|woosw|woosc|woocommerce|wooaa|wc-|underscore|table-head-fixer|swv|sourcebuster|"
    r"pxl-woocommerce|pxl-admin|print-js|perfect-scrollbar|mptt-|jquery-ui-|contact-form-7|wp-emoji)"
)
DROP_SCRIPT_TYPES = ("speculationrules", "application/ld+json")
DROP_LINK_IDS = re.compile(
    r"^(woocommerce-|woosw|woosc|wooaa|mptt-|hint-css|perfect-scrollbar|wp-block-library|dashicons)"
)
DROP_STYLE_IDS = re.compile(r"^(wp-emoji-styles|woocommerce-inline|classic-theme-styles|global-styles|joinchat-button-style|woosw-|woosc-)")


def rewrite_url(raw):
    """Devuelve la URL local para una URL del sitio original (o None si no aplica)."""
    escaped = "\\/" in raw
    u = normalize(raw)
    p = urllib.parse.urlsplit(u)
    host = p.netloc.lower()
    new = None
    if host in ("fonts.googleapis.com", "fonts.gstatic.com", "db.onlinewebfonts.com", "lh3.googleusercontent.com"):
        lp = local_path(u)
        if lp is None:
            return None
        if not os.path.exists(os.path.join(ASSETS, lp)):
            if host == "lh3.googleusercontent.com":
                return "/assets/img/reviews/default.jpg"
            return None
        new = "/assets/" + urllib.parse.quote(lp)
    elif host == "integralgymtech.com":
        path = p.path or "/"
        lp = local_path(u)
        if lp:
            new = "/assets/" + urllib.parse.quote(lp)
            if p.fragment and lp.endswith(".svg"):
                new += "#" + p.fragment
        else:
            for pre, dst in (("/wp-content/uploads/", "uploads/"), ("/wp-content/themes/hadkaur/", "theme/"),
                             ("/wp-content/plugins/", "plugins/"), ("/wp-includes/", "core/")):
                pp = path if path.endswith("/") else path + "/"
                if pp.startswith(pre):
                    new = "/assets/" + dst + pp[len(pre):]
                    if not path.endswith("/"):
                        new = new.rstrip("/")
                    break
            else:
                if path.startswith(("/wp-json", "/xmlrpc", "/feed", "/comments/feed", "/wp-admin")):
                    new = "/"
                else:
                    new = page_link(path)
                    if p.query and not new:
                        new = "/"
                    if p.fragment:
                        new += "#" + p.fragment
    if new is None:
        return None
    return new.replace("/", "\\/") if escaped else new


def page_link(path):
    path = urllib.parse.unquote(path)
    if path in PAGE_ALIASES:
        return PAGE_ALIASES[path]
    if path.rstrip("/") in PAGE_ALIASES:
        return PAGE_ALIASES[path.rstrip("/")]
    m = re.match(r"^/portfolio-category/([^/]+)/?$", path)
    if m:
        return "/" + m.group(1) + "/"
    if path == "" or path == "/":
        return "/"
    if not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
        path += "/"
    return path


def rewrite_urls(text):
    def sub(m):
        new = rewrite_url(m.group(0))
        return new if new is not None else m.group(0)
    text = URL_RE.sub(sub, text)
    # enlaces internos relativos (menús): href="/cardio" -> href="/cardio/"
    def rel(m):
        return m.group(1) + page_link(m.group(2)) + m.group(3)
    text = re.sub(r'(href=")(/[a-z0-9\-]+)(")', rel, text)
    return text


# ---------------------------------------------------------------- limpieza de head / scripts
def strip_tags(text):
    def script(m):
        tag = m.group(1)
        idm = re.search(r'\bid=["\']([^"\']+)', tag)
        typ = re.search(r'\btype=["\']([^"\']+)', tag)
        body = m.group(2)
        if idm and DROP_SCRIPT_IDS.match(idm.group(1)):
            return ""
        if typ and typ.group(1) in DROP_SCRIPT_TYPES:
            return ""
        if typ and typ.group(1) == "module" and "wp-emoji" in body:
            return ""
        if "document.body.className.replace( 'woocommerce-no-js'" in body or "c.replace(/woocommerce-no-js/" in body:
            return ""
        return m.group(0)
    text = re.sub(r"<script\b([^>]*)>(.*?)</script>", script, text, flags=re.S)

    def link(m):
        tag = m.group(0)
        idm = re.search(r"\bid=['\"]([^'\"]+)", tag)
        if idm and DROP_LINK_IDS.match(idm.group(1)):
            return ""
        if re.search(r"rel=['\"](profile|dns-prefetch|EditURI|wlwmanifest|shortlink|https://api\.w\.org/|preconnect)['\"]", tag):
            return ""
        if re.search(r"rel=['\"]alternate['\"]", tag):
            return ""
        if re.search(r"rel=['\"](icon|apple-touch-icon)['\"]", tag) or "msapplication-TileImage" in tag:
            return ""
        return tag
    text = re.sub(r"<link\b[^>]*>", link, text)
    text = re.sub(r"<meta\b[^>]*name=['\"](generator|msapplication-TileImage)['\"][^>]*>", "", text)

    def style(m):
        idm = re.search(r"\bid=['\"]([^'\"]+)", m.group(1))
        if idm and DROP_STYLE_IDS.match(idm.group(1)):
            return ""
        return m.group(0)
    text = re.sub(r"<style\b([^>]*)>(.*?)</style>", style, text, flags=re.S)
    # restos de WooCommerce (comparador / wishlist)
    text = re.sub(r'<div class="woosc-popup woosc-search">.*?<div id="woosw_wishlist"[^>]*></div>', "", text, flags=re.S)
    text = re.sub(r"\n?/\*# sourceURL=[^*]*\*/", "", text)
    text = re.sub(r"\n?//# sourceURL=[^\n]*", "", text)
    return text


def replace_seo_head(text, slug):
    title, desc, kws, crumb, stype, ogimg = seo.PAGES[slug]
    # quita bloque Yoast + robots + title
    text = re.sub(r"<meta name='robots'[^>]*>\s*", "", text)
    text = re.sub(r"<!-- This site is optimized.*?<!-- / Yoast SEO plugin. -->", "", text, flags=re.S)
    text = re.sub(r"<title>.*?</title>", "", text, count=1, flags=re.S)
    url = SITE + ("/" if slug == "index" else "/" + slug + "/")
    kw = ", ".join(dict.fromkeys(kws + seo.BASE_KW))
    img = SITE + (ogimg or seo.OG_DEFAULT)
    e = htmlmod.escape
    b = seo.BUSINESS
    org_id = SITE + "/#organization"
    graph = [
        {
            "@type": ["Organization", "LocalBusiness", "SportingGoodsStore"],
            "@id": org_id,
            "name": b["name"], "legalName": b["legalName"], "alternateName": ["IGT", "IntegralGYMTech"],
            "url": SITE + "/", "logo": SITE + "/assets/uploads/2023/08/Logo.png", "image": img,
            "description": seo.PAGES["index"][1],
            "telephone": b["telephone"], "email": b["email"], "foundingDate": "2008", "priceRange": "$$",
            "address": {"@type": "PostalAddress", "streetAddress": b["street"], "addressLocality": b["locality"],
                        "addressRegion": b["region"], "postalCode": b["postal"], "addressCountry": b["country"]},
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                           "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                           "opens": "09:00", "closes": "18:00"}],
            "areaServed": [{"@type": "State", "name": "Querétaro"}, {"@type": "Country", "name": "México"}],
            "hasMap": b["maps"], "sameAs": [b["facebook"], b["instagram"]],
            "brand": {"@type": "Brand", "name": "BUGE"},
            "knowsAbout": ["Equipo para gimnasio", "Equipamiento de gimnasios", "Mantenimiento de equipo fitness",
                           "Arrendamiento de equipo de gimnasio", "Diseño de gimnasios", "Pilates"],
        },
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "IntegralGYMTech",
         "inLanguage": "es-MX", "publisher": {"@id": org_id}},
        {"@type": stype if stype in ("WebPage", "AboutPage", "CollectionPage") else "WebPage",
         "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "es-MX",
         "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": org_id},
         "primaryImageOfPage": {"@type": "ImageObject", "url": img}, "dateModified": TODAY,
         "breadcrumb": {"@id": url + "#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement":
            [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"}] +
            ([] if slug == "index" else [{"@type": "ListItem", "position": 2, "name": crumb, "item": url}])},
    ]
    if stype == "Service":
        graph.append({"@type": "Service", "name": crumb, "serviceType": crumb, "description": desc,
                      "provider": {"@id": org_id}, "areaServed": "México", "url": url})
    if stype == "CollectionPage":
        graph.append({"@type": "OfferCatalog", "name": "Catálogo " + crumb + " BUGE", "url": url,
                      "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Product", "name": k.capitalize(),
                                                                             "brand": {"@type": "Brand", "name": "BUGE"}}}
                                          for k in kws[:6]]})
    robots = "noindex, follow" if slug == "404" else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    head = f"""
    <title>{e(title)}</title>
    <meta name="description" content="{e(desc)}">
    <meta name="keywords" content="{e(kw)}">
    <meta name="robots" content="{robots}">
    <meta name="author" content="Integral Gym Tech">
    <meta name="theme-color" content="#000000">
    <meta name="geo.region" content="MX-QUE">
    <meta name="geo.placename" content="Querétaro">
    {'' if slug == '404' else f'<link rel="canonical" href="{url}">'}
    <link rel="alternate" hreflang="es-MX" href="{url}">
    <meta property="og:locale" content="es_MX">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="IntegralGYMTech">
    <meta property="og:title" content="{e(title)}">
    <meta property="og:description" content="{e(desc)}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{img}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{e(title)}">
    <meta name="twitter:description" content="{e(desc)}">
    <meta name="twitter:image" content="{img}">
    <link rel="icon" href="/assets/uploads/2026/08/igt-logo-icon-2.png" sizes="32x32">
    <link rel="icon" href="/assets/uploads/2026/08/igt-logo-icon-2.png" sizes="192x192">
    <link rel="apple-touch-icon" href="/assets/uploads/2026/08/igt-logo-icon-2.png">
    <link rel="preload" href="/assets/theme/assets/fonts/font-custom/Plateia%20Bold.ttf" as="font" type="font/ttf" crossorigin>
    <script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
"""
    text = text.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">' + head, 1)
    text = text.replace('<html lang="es">', '<html lang="es-MX">', 1)
    text = text.replace('content="width=device-width, initial-scale=1, maximum-scale=1"',
                        'content="width=device-width, initial-scale=1"', 1)
    return text, kws


# ---------------------------------------------------------------- flipbook (catálogos PDF)
def fix_flipbook(text):
    def sub(m):
        try:
            data = json.loads(base64.b64decode(m.group(1)).decode("utf-8"))
        except Exception:  # noqa: BLE001
            return m.group(0)
        s = json.dumps(data, ensure_ascii=False)
        s = rewrite_urls(s.replace("/", "\\/")).replace("\\/", "/")
        return "FB3D_CLIENT_DATA.push('" + base64.b64encode(s.encode("utf-8")).decode() + "'"
    return re.sub(r"FB3D_CLIENT_DATA\.push\('([A-Za-z0-9+/=]+)'", sub, text)


# ---------------------------------------------------------------- formulario
def fix_form(text, slug):
    text = re.sub(r'<form action="[^"]*#wpcf7-f8-o1" method="post" class="wpcf7-form init"',
                  '<form action="/enviar.php" method="post" class="wpcf7-form init igt-form"', text)
    hidden = ('<fieldset class="hidden-fields-container"><input type="hidden" name="pagina" value="' + slug + '" />'
              '<input type="hidden" name="ts" value="" />'
              '<span class="igt-hp" aria-hidden="true"><label for="cf-website-' + '">Website</label>'
              '<input type="text" name="website" id="cf-website" tabindex="-1" autocomplete="off" /></span>\n</fieldset>')
    text = re.sub(r'<fieldset class="hidden-fields-container">.*?</fieldset>', hidden, text, flags=re.S)
    text = text.replace('class="wpcf7 no-js"', 'class="wpcf7 js"')
    return text


# ---------------------------------------------------------------- SEO dentro del cuerpo
def improve_body(text, slug, kws):
    title = seo.PAGES[slug][3]
    # alt vacíos -> texto descriptivo
    counter = {"n": 0}

    def alt(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        name = ""
        if src:
            name = urllib.parse.unquote(src.group(1).rsplit("/", 1)[-1].rsplit(".", 1)[0])
            name = re.sub(r"[-_]+", " ", re.sub(r"(-\d+x\d+|-scaled|-\d+)$", "", name)).strip()
            name = re.sub(r"\b(igt|img|image|copia|copy|bg\d*|ellipse \d+)\b", "", name, flags=re.I).strip()
        k = kws[counter["n"] % len(kws)] if kws else "equipo para gimnasio"
        counter["n"] += 1
        label = (name.capitalize() + " – " if len(name) > 3 else "") + f"{title} | {k} – Integral Gym Tech"
        return re.sub(r'alt=""', 'alt="' + htmlmod.escape(label) + '"', tag, count=1)
    text = re.sub(r"<img\b[^>]*\balt=\"\"[^>]*>", alt, text)
    text = re.sub(r"<img\b(?![^>]*\balt=)([^>]*)>", lambda m: '<img alt="' + htmlmod.escape(title + " – Integral Gym Tech") + '"' + m.group(1) + ">", text)
    # lazy-loading para imágenes sin atributo loading
    text = re.sub(r"<img\b(?![^>]*\bloading=)", '<img loading="lazy" decoding="async"', text)
    # enlaces externos seguros
    text = re.sub(r'(<a\b[^>]*target="_blank")(?![^>]*rel=)', r'\1 rel="noopener"', text)
    # Encabezado principal -> h1 (las páginas internas usaban h2 y el home tenía varios h1 en contadores)
    text = re.sub(r'<h1\s+class="(pxl--counter-value[^"]*)"([^>]*>[^<]*)</h1>', r'<div class="h1 \1"\2</div>', text)
    if slug != "index" and "<h1" not in text.split("<main", 1)[-1]:
        text = re.sub(r"<h([2-4])\s+class=\"pxl-item--title([^>]*>)(.*?)</h\1>", r'<h1 class="h\1 pxl-item--title\2\3</h1>', text, count=1, flags=re.S)
    # erratas
    text = text.replace("Arredandamiento", "Arrendamiento").replace("Ellos ya confian", "Ellos ya confían")
    text = text.replace(">Page Not Found<", ">Página no encontrada<")
    # textos de WordPress/theme
    text = text.replace('placeholder="Search..."', 'placeholder="Buscar..."')
    return text


# ---------------------------------------------------------------- inyección de recursos propios
def inject(text):
    css = '<link rel="stylesheet" id="igt-css" href="/assets/igt/igt.css" media="all">\n</head>'
    text = text.replace("</head>", css, 1)
    js = '<script src="/assets/igt/igt-form.js" defer></script>\n</body>'
    return text.replace("</body>", js, 1)


def build_page(slug):
    text = open(os.path.join(SRC_PAGES, slug + ".html"), encoding="utf-8").read()
    text = strip_tags(text)
    text = fix_flipbook(text)
    text = rewrite_urls(text)
    text, kws = replace_seo_head(text, slug)
    text = fix_form(text, slug)
    text = improve_body(text, slug, kws)
    text = inject(text)
    text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)
    if slug in ("index", "404"):
        dest = os.path.join(OUT, slug + ".html")
    else:
        dest = os.path.join(OUT, slug, "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(text)
    return dest


# ---------------------------------------------------------------- assets
SKIP_ASSET_DIRS = ("plugins/woocommerce/", "plugins/woo-smart-wishlist/", "plugins/woo-smart-compare/",
                   "plugins/wpc-ajax-add-to-cart/", "plugins/mp-timetable/", "core/js/dist/",
                   "core/js/underscore", "core/js/jquery/ui/", "core/js/wp-emoji", "theme/woocommerce/",
                   "theme/assets/js/admin.js", "core/css/dist/", "core/css/dashicons", "core/fonts/dashicons",
                   "plugins/contact-form-7/includes/js", "plugins/contact-form-7/includes/swv")


def copy_assets():
    dst_root = os.path.join(OUT, "assets")
    for dirpath, _, files in os.walk(ASSETS):
        for fn in files:
            src = os.path.join(dirpath, fn)
            rel = os.path.relpath(src, ASSETS).replace(os.sep, "/")
            if rel.startswith(SKIP_ASSET_DIRS):
                continue
            dst = os.path.join(dst_root, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if fn.endswith((".css", ".js", ".html")) and "pdf.worker" not in fn and "pdf.min" not in fn:
                s = open(src, encoding="utf-8", errors="surrogateescape").read()
                s2 = rewrite_urls(s) if ("integralgymtech.com" in s or "fonts.gstatic.com" in s) else s
                with open(dst, "w", encoding="utf-8", errors="surrogateescape") as f:
                    f.write(s2)
            else:
                shutil.copy2(src, dst)


def copy_static():
    for dirpath, _, files in os.walk(STATIC):
        for fn in files:
            src = os.path.join(dirpath, fn)
            rel = os.path.relpath(src, STATIC)
            dst = os.path.join(OUT, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)


def write_sitemap(slugs):
    prio = {"index": "1.0"}
    urls = []
    for s in slugs:
        if s == "404":
            continue
        loc = SITE + ("/" if s == "index" else f"/{s}/")
        p = prio.get(s, "0.3" if s in ("terminos-y-condiciones", "politica-devoluciones") else "0.8")
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{p}</priority></url>")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w").write(xml)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    copy_assets()
    copy_static()
    slugs = sorted(f[:-5] for f in os.listdir(SRC_PAGES) if f.endswith(".html"))
    for s in slugs:
        if s not in seo.PAGES:
            print("!! sin datos SEO:", s)
            continue
        print("  ->", os.path.relpath(build_page(s), ROOT))
    write_sitemap(slugs)
    # verificación: no deben quedar URLs absolutas al sitio viejo
    for dirpath, _, files in os.walk(OUT):
        for fn in files:
            if fn.endswith(".html") and "assets" not in dirpath:
                s = open(os.path.join(dirpath, fn), encoding="utf-8").read()
                left = set(re.findall(r"https?:(?:\\?/){2}integralgymtech\.com[^\"'\s<>)]*", s))
                left = {x for x in left if not re.match(r"https?:(\\?/){2}integralgymtech\.com(\\?/)?([a-z0-9\-]+(\\?/))?(#[a-z\-]+)?$", x) and "/assets/" not in x}
                if left:
                    print("  !! URLs absolutas restantes en", fn, list(left)[:5])


if __name__ == "__main__":
    main()
