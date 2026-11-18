# Integral Gym Tech — sitio web

Sitio de **integralgymtech.com** reescrito sin WordPress: HTML semántico generado con plantillas propias, CSS y JavaScript propios (sin jQuery, Elementor ni plugins) y un único script PHP para el formulario. El diseño es el mismo que el sitio original (verificado página por página contra el original en escritorio y móvil).

## Resultados (Lighthouse, móvil)

| Página | Rendimiento original | Rendimiento nuevo | SEO nuevo |
|---|---|---|---|
| Inicio | 51 | 93 | 100 |
| Cardio | 25 | 96 | 100 |
| Nosotros / Hoteles / Reacondicionado | — | 96–97 | 100 |

Peso de la página de Cardio: 7 MB → menos de 1 MB.

## Estructura

```
site/
  templates/        plantillas Jinja2
    base.html       documento base (SEO, cabecera, contacto, pie)
    layouts/        plantilla de "tipo de proyecto"
    partials/       cabecera, pie, contacto, macros (ui, product, blocks)
    pages/          una plantilla por página (la URL es el nombre del archivo)
  css/              CSS propio (orden en css/_order.txt); se minifica y se incrusta en cada página
  js/main.js        interacciones: cabecera fija, menús, panel, animaciones, contadores,
                    pestañas, carruseles, galerías, lightbox, formulario, cursor
  js/flipbook.js    visor de catálogos (se carga solo cuando el catálogo se acerca)
  icons/            iconos SVG (se genera un sprite cacheable)
  fonts/            Plateia, Montserrat y Roboto en WOFF2 (subconjunto latino)
  static/           archivos que se copian tal cual: enviar.php, config-correo.php, .htaccess,
                    robots.txt, favicon, logo, reseñas, video
source/assets/uploads/  imágenes y PDFs originales (el build genera las versiones optimizadas)
source/pages/       HTML del sitio WordPress original (solo como referencia)
tools/build_site.py generador del sitio
tools/seo.py        títulos, descripciones y palabras clave de cada página
```

## Construir

Requisitos: Python 3.10+ con `jinja2` y `pillow` (con soporte AVIF), Node.js (esbuild) y `pdftoppm`/`pdftotext` (poppler-utils).

```bash
npm install
```

```bash
python3 tools/build_site.py
```

El resultado queda en `public/`. Con `--fast` se omite AVIF (útil al desarrollar). Para probar localmente:

```bash
php -S 127.0.0.1:8080 -t public
```

Qué hace el build:

- Renderiza cada página y minifica el HTML.
- Genera variantes **AVIF + WebP** en varios anchos de cada imagen (`srcset`), con `width`/`height` para evitar saltos de diseño. Los fondos de sección se cargan solo cuando se acercan a la pantalla.
- Convierte cada catálogo PDF en páginas WebP para el visor (sin pdf.js); el PDF sigue disponible para descargar.
- Minifica CSS (se incrusta) y JS (archivos con hash, caché de 1 año).
- Crea un sprite SVG con los iconos usados.
- Escribe `sitemap.xml`.

## SEO

Cada página tiene título, descripción y palabras clave propias (`tools/seo.py`), canonical, Open Graph/Twitter, un solo `<h1>`, textos alternativos descriptivos y datos estructurados JSON-LD (LocalBusiness con dirección, horario, teléfono y calificación, WebPage, BreadcrumbList, Service u OfferCatalog). Las URLs son las mismas que en WordPress y `.htaccess` redirige las antiguas.

## Formulario de contacto

`enviar.php` envía cada solicitud a gerencia@integralgymtech.com, gerenciamkt@mediamaster.mx, traffickermkt@mediamaster.mx y programacionmkt@mediamaster.mx, con validación, honeypot, tiempo mínimo de llenado y límite de envíos por IP. Usa `mail()` de Hostinger; si los correos llegan a spam, llena los datos SMTP en `config-correo.php`.

## Publicar en Hostinger

1. Respalda el WordPress actual.
2. Vacía `public_html/`.
3. Sube el ZIP y extráelo directamente en `public_html/` (incluye `.htaccess`).
4. Envía un formulario de prueba y revisa los 4 correos.
5. En Google Search Console envía `https://integralgymtech.com/sitemap.xml`.
