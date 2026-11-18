#!/usr/bin/env python3
"""Descarga (una sola vez) todos los recursos que usan las páginas fuente.

Uso: python3 tools/fetch_assets.py
Lee source/pages/*.html, encuentra imágenes, CSS, JS, fuentes y PDFs del sitio
original y los guarda en source/assets/ con la ruta que define urlmap.local_path().
Los CSS se procesan recursivamente (url() e @import).
"""
import hashlib
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from urlmap import ROOT, ASSETS, local_path, normalize, URL_RE  # noqa: E402

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)|@import\s+['\"]([^'\"]+)['\"]")

done = {}
failed = []


def fetch(url):
    sp = urllib.parse.urlsplit(url)
    url = urllib.parse.urlunsplit(sp._replace(path=urllib.parse.quote(urllib.parse.unquote(sp.path))))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 403, 410):
                raise
            time.sleep(1 + attempt)
        except Exception:
            time.sleep(1 + attempt)
    raise RuntimeError("no se pudo descargar " + url)


def get(url, referer_css=None):
    url = normalize(url)
    if not url or url in done:
        return done.get(url)
    lp = local_path(url)
    if lp is None:
        done[url] = None
        return None
    dest = os.path.join(ASSETS, lp)
    done[url] = lp
    if not os.path.exists(dest):
        try:
            data = fetch(url)
        except Exception as e:  # noqa: BLE001
            failed.append((url, str(e), referer_css))
            return lp
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(data)
        print("  +", lp, len(data))
    if lp.endswith(".css"):
        with open(dest, "r", encoding="utf-8", errors="replace") as f:
            css = f.read()
        for m in CSS_URL_RE.finditer(css):
            ref = (m.group(1) or m.group(2)).strip()
            if ref.startswith("data:") or ref.startswith("#"):
                continue
            absu = urllib.parse.urljoin(url, ref)
            get(absu, referer_css=url)
    return lp


def main():
    pages_dir = os.path.join(ROOT, "source", "pages")
    urls = set()
    for name in sorted(os.listdir(pages_dir)):
        if not name.endswith(".html"):
            continue
        html = open(os.path.join(pages_dir, name), encoding="utf-8").read()
        for m in URL_RE.finditer(html):
            urls.add(m.group(0))
    extra = os.path.join(ROOT, "tools", "extra_urls.txt")
    if os.path.exists(extra):
        urls.update(u.strip() for u in open(extra) if u.strip() and not u.startswith("#"))
    print(len(urls), "URLs candidatas")
    for u in sorted(urls):
        get(u)
    print("\nFallidas:", len(failed))
    for f in failed:
        print("  -", f)


if __name__ == "__main__":
    main()
