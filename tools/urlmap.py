"""Mapeo de URLs del sitio WordPress original a rutas locales del sitio estático."""
import hashlib
import html
import os
import re
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "source", "assets")
SITE = "https://integralgymtech.com"

HOSTS = r"(?:www\.)?integralgymtech\.com|fonts\.googleapis\.com|fonts\.gstatic\.com|db\.onlinewebfonts\.com|lh3\.googleusercontent\.com"
URL_RE = re.compile(r"(?:https?:)?(?:\\?/){2}(?:" + HOSTS + r")[^\"'\s<>)]*")

ASSET_EXT = {
    "png", "jpg", "jpeg", "gif", "webp", "svg", "ico", "avif", "bmp",
    "css", "js", "json", "map",
    "woff", "woff2", "ttf", "eot", "otf",
    "pdf", "bcmap", "mp4", "webm", "mp3", "ogg", "wav", "html", "glb", "gltf",
}


def normalize(u):
    """Convierte una URL tal como aparece en el HTML/JSON a una URL absoluta limpia."""
    u = u.replace("\\/", "/")
    for cut in ("&quot;", '\\"', "&#039;", "\\'"):
        if cut in u:
            u = u.split(cut)[0]
    u = html.unescape(u).rstrip("\\,;")
    if u.startswith("//"):
        u = "https:" + u
    u = u.replace("http://", "https://").replace("://www.integralgymtech.com", "://integralgymtech.com")
    return u


def _ext(path):
    base = path.rsplit("/", 1)[-1]
    return base.rsplit(".", 1)[-1].lower() if "." in base else ""


def local_path(url):
    """Ruta relativa dentro de /assets/ para una URL, o None si no es un recurso."""
    p = urllib.parse.urlsplit(url)
    host = p.netloc.lower()
    path = urllib.parse.unquote(p.path)
    if host == "fonts.googleapis.com":
        h = hashlib.md5(url.encode()).hexdigest()[:10]
        return "fonts/google-" + h + ".css"
    if host == "fonts.gstatic.com":
        return "fonts/gstatic" + path
    if host == "db.onlinewebfonts.com":
        return "fonts/web/" + path.rsplit("/", 1)[-1]
    if host == "lh3.googleusercontent.com":
        h = hashlib.md5(url.encode()).hexdigest()[:12]
        return "img/reviews/" + h + ".jpg"
    if host != "integralgymtech.com":
        return None
    if _ext(path) not in ASSET_EXT:
        return None
    for pre, dst in (
        ("/wp-content/uploads/", "uploads/"),
        ("/wp-content/themes/hadkaur/", "theme/"),
        ("/wp-content/plugins/", "plugins/"),
        ("/wp-includes/", "core/"),
    ):
        if path.startswith(pre):
            return dst + path[len(pre):]
    return None


def public_url(url):
    """URL absoluta original -> URL root-relative en el sitio nuevo (o None)."""
    lp = local_path(normalize(url))
    return "/assets/" + urllib.parse.quote(lp) if lp else None
