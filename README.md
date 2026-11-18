# Integral Gym Tech — sitio estático

Migración de **integralgymtech.com** de WordPress a HTML/CSS/JS estático con un único script PHP para el formulario de contacto. Visualmente idéntico al sitio original (verificado página por página contra el sitio en vivo en escritorio y móvil).

## Estructura

```
source/pages/    HTML renderizado del sitio WordPress original (fuente)
source/assets/   imágenes, CSS, JS, fuentes y catálogos PDF descargados del sitio original
source/static/   archivos propios: enviar.php, config-correo.php, .htaccess, robots.txt, assets/igt/*
tools/           scripts de construcción (Python 3, sin dependencias)
public/          sitio generado (no se versiona; se crea con el build)
```

## Construir

```bash
python3 tools/build.py
```

Genera `public/` con:

- URLs idénticas a las de WordPress (`/cardio/`, `/nosotros/`, …) para conservar el posicionamiento.
- SEO por página (`tools/seo.py`): title, description, keywords, canonical, Open Graph/Twitter, JSON-LD (LocalBusiness, WebPage, BreadcrumbList, Service/OfferCatalog), un solo `<h1>`, `alt` descriptivos.
- `sitemap.xml`, `robots.txt`, `.htaccess` (HTTPS, redirecciones de URLs viejas de WordPress, compresión y caché).
- Sin WordPress, WooCommerce ni plugins de servidor.

`tools/fetch_assets.py` vuelve a descargar los recursos del sitio original (solo es necesario si se agregan páginas nuevas a `source/pages/`).

## Formulario de contacto

`enviar.php` envía cada solicitud a:

- gerencia@integralgymtech.com
- gerenciamkt@mediamaster.mx
- traffickermkt@mediamaster.mx
- programacionmkt@mediamaster.mx

Incluye validación, honeypot anti-spam, tiempo mínimo de llenado y límite de 5 envíos por IP cada 10 minutos. Usa `mail()` de Hostinger. Si los correos llegan a spam, crea el buzón `no-reply@integralgymtech.com` en Hostinger y llena los datos SMTP en `config-correo.php` (`smtp.hostinger.com`, puerto 465).

Para cambiar destinatarios edita `$DESTINATARIOS` en `source/static/enviar.php`.

## Publicar en Hostinger

1. Haz respaldo del WordPress actual (Hostinger → Respaldos).
2. En el Administrador de archivos, vacía `public_html/` (o muévelo a una carpeta de respaldo).
3. Sube `igt-sitio-estatico.zip` a `public_html/` y extráelo ahí (los archivos deben quedar directamente en `public_html/`, incluido `.htaccess`).
4. Prueba el formulario y revisa que lleguen los correos.
5. En Google Search Console, envía `https://integralgymtech.com/sitemap.xml`.
