"""Datos SEO por página (title, description, keywords, breadcrumb, tipo de schema)."""

BRAND = "Integral Gym Tech"
SITE = "https://integralgymtech.com"
OG_DEFAULT = "/assets/uploads/2026/08/cropped-IGT-logo-back-black.webp"

BASE_KW = [
    "equipo para gimnasio Querétaro", "aparatos de gimnasio", "venta de equipo de gimnasio",
    "equipo de gimnasio profesional", "Integral Gym Tech", "IGT", "BUGE", "distribuidor BUGE México",
    "equipamiento para gimnasio comercial", "cotización de equipo para gimnasio", "equipos de gimnasio Querétaro",
    "venta de equipos para gimnasio", "proveedor de equipos para gimnasio",
]

# slug: (title, description, [keywords], breadcrumb_name, schema_type, og_image(optional))
PAGES = {
    "index": (
        "Equipos de Gimnasio en Querétaro | Venta de Equipo Comercial | Integral Gym Tech",
        "Venta de equipos para gimnasio en Querétaro: máquinas para gimnasio de uso rudo, equipo de fuerza, cardio, Pilates y crossfit. Proveedor de equipos para gimnasio comercial con envío a todo México. Cotiza el precio de tu equipo.",
        ["equipos de gimnasio Querétaro", "venta de equipos para gimnasio", "comprar equipo para gimnasio", "proveedor de equipos para gimnasio", "máquinas para gimnasio", "equipo fitness profesional", "equipo para gimnasio comercial", "precio equipo gimnasio", "cotizar equipo para gimnasio", "equipamiento para gimnasio comercial", "máquina de hacer ejercicio", "Integral Gym Tech Querétaro", "equipos BUGE Fitness México"],
        "Inicio", "WebPage", "/assets/uploads/2023/09/Ellipse-3.png",
    ),
    "nosotros": (
        "Integral Gym Tech Querétaro | Distribuidor de Equipos BUGE Fitness en México",
        "Integral Gym Tech, en Querétaro desde 2008: distribuidor de equipos BUGE Fitness en México y proveedor de equipamiento para gimnasios comerciales, hoteles, condominios y universidades.",
        ["Integral Gym Tech Querétaro", "equipos BUGE Fitness México", "máquinas BUGE para gimnasio", "distribuidor BUGE México"],
        "Nosotros", "AboutPage", None,
    ),
    "mantenimiento-de-equipo": (
        "Mantenimiento de Equipo de Gimnasio en Querétaro | Preventivo y Correctivo | IGT",
        "Servicio de mantenimiento preventivo, correctivo y diagnóstico para equipos de gimnasio en Querétaro. Prolonga la vida útil de caminadoras, elípticas y máquinas de fuerza y evita interrupciones en tu operación.",
        ["mantenimiento de equipo de gimnasio", "reparación de caminadoras", "servicio técnico equipo fitness",
         "mantenimiento preventivo gimnasio", "mantenimiento correctivo aparatos de gimnasio", "refacciones gimnasio Querétaro"],
        "Mantenimiento de equipo", "Service", None,
    ),
    "arrendamiento": (
        "Arrendamiento Financiero de Equipo de Gimnasio | Leasing a Mensualidades Fijas | IGT",
        "Equipa o renueva tu gimnasio sin descapitalizarte con arrendamiento financiero (leasing) de equipo fitness. Mensualidades fijas y pagos flexibles para gimnasios, hoteles y empresas en Querétaro y todo México.",
        ["arrendamiento de equipo de gimnasio", "leasing equipo fitness", "financiamiento para gimnasio",
         "equipo de gimnasio a mensualidades", "crédito para equipar gimnasio"],
        "Arrendamiento", "Service", None,
    ),
    "diseno-de-espacios": (
        "Diseño de Gimnasios y Renderizado 3D de Espacios Fitness | Integral Gym Tech",
        "Diseño de espacios y renderización 3D para gimnasios: distribuye mejor los equipos, aprovecha cada metro cuadrado y visualiza tu proyecto antes de invertir. Gimnasios comerciales, residenciales y corporativos.",
        ["diseño de gimnasios", "render 3D gimnasio", "layout de gimnasio", "proyecto de gimnasio",
         "diseño de gimnasio comercial", "distribución de equipo de gimnasio"],
        "Diseño de espacios", "Service", None,
    ),
    "cardio": (
        "Equipo de Cardio Profesional | Caminadoras, Elípticas y Remos | Integral Gym Tech",
        "Equipo de cardio profesional de uso rudo: caminadoras comerciales, caminadora curva sin motor, elípticas, escaladora profesional, remo de aire y máquina de esquí para gimnasio. Consulta el catálogo.",
        ["caminadora curva sin motor", "remo de aire para gimnasio", "máquina de esquí para gimnasio", "escaladora profesional para gimnasio", "caminadoras profesionales", "elípticas para gimnasio"],
        "Cardio", "CollectionPage", None,
    ),
    "peso-libre": (
        "Equipos de Peso Libre | Bancos Olímpicos, Racks y Smith | Integral Gym Tech",
        "Equipos de peso libre de uso rudo: bancos olímpicos, banco ajustable para pesas, racks, máquina Smith profesional, mancuernas y discos olímpicos. Equipo de fuerza para gimnasio comercial y en casa.",
        ["equipos peso libre", "bancos olímpicos", "banco ajustable para pesas", "banco para press de banca", "máquina Smith profesional", "equipo de fuerza", "mancuernas", "discos olímpicos"],
        "Peso libre", "CollectionPage", None,
    ),
    "peso-integrado": (
        "Equipos de Peso Integrado | Prensa y Máquinas de Fuerza | Integral Gym Tech",
        "Equipos de peso integrado para gimnasio: prensa de pierna, máquinas selectorizadas y equipo de fuerza para armar tu circuito de fuerza. Paquetes de fuerza BUGE con precio a cotización.",
        ["equipos de peso integrado", "prensa", "prensa precio", "prensa de pierna", "circuito de fuerza", "paquete de fuerza", "equipo de fuerza", "máquinas de fuerza", "máquinas selectorizadas"],
        "Peso integrado", "CollectionPage", None,
    ),
    "multifuncionales": (
        "Equipos Multifuncionales para Gimnasio | Multiestaciones | Integral Gym Tech",
        "Equipos multifuncionales y multiestaciones: crossovers, poleas, junglas y multi-smith. Máquinas para gimnasio que aprovechan el espacio en gimnasios, condominios, hoteles y casa.",
        ["equipos multifuncional", "multifuncional de gimnasio", "máquinas para gimnasio", "multiestación", "crossover de poleas", "jungla de gimnasio"],
        "Multifuncionales", "CollectionPage", None,
    ),
    "pilates": (
        "Reformer y Cama de Pilates Profesional en Querétaro | Integral Gym Tech",
        "Venta de equipos de Pilates: reformer y cama de Pilates profesional, cadillac, chair y accesorios. Máquinas de Pilates de maple y roble para estudios y gimnasios en Querétaro. Pide el precio de tu reformer.",
        ["cama de pilates", "máquinas de pilates", "equipos pilates", "venta de equipos pilates", "venta de reformer de pilates", "reformer de pilates profesional", "reformer de pilates precio", "reformer de pilates en Querétaro"],
        "Pilates", "CollectionPage", None,
    ),
    "accesorios": (
        "Accesorios para Gimnasio y Crossfit | Bancos y Trampolines | Integral Gym Tech",
        "Accesorios para gimnasio y equipamiento crossfit: banco de pesas multifuncional, trampolín fitness, kettlebells, bumpers, cuerdas de batalla, wall balls y tapetes de grado comercial.",
        ["equipamiento crossfit", "accesorios para gimnasio", "trampolín fitness para ejercicio", "mini trampolín para cardio", "banco de pesas multifuncional", "kettlebells", "bumpers"],
        "Accesorios", "CollectionPage", None,
    ),
    "reacondicionado": (
        "Equipo de Gimnasio Reacondicionado y Seminuevo | Garantía IGT | Querétaro",
        "Equipo de gimnasio reacondicionado y seminuevo de marcas premium: inspección 360, piezas originales, pintura nueva y garantía IGT. Calidad de primera a una fracción del costo original.",
        ["equipo de gimnasio reacondicionado", "equipo de gimnasio seminuevo", "aparatos de gimnasio usados",
         "caminadoras reacondicionadas", "equipo fitness usado Querétaro", "máquinas de gimnasio seminuevas"],
        "Reacondicionado", "CollectionPage", None,
    ),
    "gimnasio-apertura-remodelacion": (
        "Aparatos para Abrir un Gimnasio | Equipamiento Comercial | Integral Gym Tech",
        "Equipamiento para gimnasios comerciales: paquetes de equipo para abrir o remodelar tu gimnasio con máquinas de uso rudo, diseño de espacios y arrendamiento. Solicita tu cotización de equipo para gimnasio.",
        ["aparatos para abrir un gimnasio", "equipamiento para gimnasio comercial", "paquetes de equipo para gimnasio", "cotización de equipo para gimnasio", "máquinas de gimnasio de uso rudo", "remodelación de gimnasio"],
        "Apertura o remodelación de gimnasio", "Service", None,
    ),
    "gimnasio-casa": (
        "Gimnasio en Casa | Equipo de Gimnasio para el Hogar en Querétaro | IGT",
        "Arma tu gimnasio en casa con equipo profesional: caminadoras, multifuncionales, mancuernas y más. Ahorra tiempo y membresías entrenando en la privacidad de tu hogar. Asesoría y diseño de espacios.",
        ["gimnasio en casa", "equipo de gimnasio para casa", "home gym", "aparatos de ejercicio para casa",
         "multifuncional para casa", "caminadora para casa"],
        "Gimnasio en casa", "Service", None,
    ),
    "condominios-residenciales": (
        "Gimnasio Residencial para Condominios y Casas Club | Integral Gym Tech",
        "Gimnasio residencial para condominios, fraccionamientos y casas club: equipo de gimnasio durable, seguro y de bajo mantenimiento con diseño del espacio y servicio técnico.",
        ["gimnasio residencial", "equipo de gimnasio para condominios", "equipamiento para casas club", "gimnasio para fraccionamiento"],
        "Condominios – residenciales", "Service", None,
    ),
    "clinicas-fisioterapia": (
        "Equipo de Gimnasio para Clínicas y Rehabilitación | Integral Gym Tech",
        "Equipo fitness para clínicas privadas y de rehabilitación: máquinas de ejercicio, bicicletas, poleas y equipo de gimnasio para rehabilitación. Te ayudamos a equipar tu clínica; solicita tu cotización de equipo fitness.",
        ["equipo fitness para clínicas", "equipamiento fitness para clínicas", "equipo de gimnasio para clínicas", "máquinas de ejercicio para clínicas", "equipo fitness para clínica privada", "equipar clínica", "equipar clínica de rehabilitación", "cotización equipo fitness clínica", "equipo de gimnasio para rehabilitación"],
        "Clínicas de fisioterapia", "Service", None,
    ),
    "estudio-pilates": (
        "Equipamiento para Estudios de Pilates | Máquinas de Pilates | Integral Gym Tech",
        "Equipamiento para estudios de Pilates: camas reformer, máquinas de Pilates, cadillac y accesorios. Venta de equipos Pilates y asesoría para abrir tu estudio en Querétaro y todo México.",
        ["equipamiento para estudios de pilates", "máquinas de pilates", "cama de pilates", "equipos pilates", "venta de equipos pilates", "abrir estudio de pilates"],
        "Estudio de pilates", "Service", None,
    ),
    "hoteles": (
        "Gimnasio para Hotel | Equipamiento para Gimnasios de Hoteles | Integral Gym Tech",
        "Equipamiento para gimnasios de hoteles: arma el gimnasio para hotel con caminadoras, elípticas y máquinas de fuerza de grado comercial, diseño del espacio, instalación y mantenimiento.",
        ["gimnasio para hotel", "equipamiento para gimnasios de hoteles", "equipo de gimnasio para hoteles", "amenidades fitness hotel"],
        "Hoteles", "Service", None,
    ),
    "empresas": (
        "Gimnasios Corporativos para Empresas | Bienestar Laboral | Integral Gym Tech",
        "Gimnasios corporativos y programas de bienestar para empresas: equipamos espacios fitness para tus colaboradores con equipo profesional, diseño y mantenimiento en Querétaro y México.",
        ["gimnasio corporativo", "gimnasio para empresas", "bienestar laboral", "wellness corporativo",
         "equipo de gimnasio para oficinas"],
        "Empresas", "Service", None,
    ),
    "universidades": (
        "Gimnasio para Escuelas y Universidades | Integral Gym Tech",
        "Equipo para gimnasios universitarios y gimnasio para escuela: máquinas de uso rudo para tráfico intenso, diseño de espacios y soporte técnico especializado.",
        ["gimnasio para escuela", "equipo para gimnasios universitarios", "gimnasio universitario", "equipamiento deportivo para escuelas"],
        "Universidades", "Service", None,
    ),
    "gubernamentales": (
        "Equipamiento de Gimnasios Gubernamentales y Espacios Públicos | Integral Gym Tech",
        "Equipamiento fitness para dependencias gubernamentales, centros deportivos públicos, corporaciones de seguridad y espacios municipales. Proveedor confiable con facturación y garantía.",
        ["gimnasio gubernamental", "equipo de gimnasio para gobierno", "licitaciones equipo deportivo",
         "gimnasio para corporaciones de seguridad", "centros deportivos municipales"],
        "Gubernamentales", "Service", None,
    ),
    "terminos-y-condiciones": (
        "Términos y Condiciones | Integral Gym Tech",
        "Términos y condiciones de uso del sitio y de venta de equipo para gimnasio de Integral Gym Tech S.A. de C.V., Querétaro, México.",
        ["términos y condiciones", "condiciones de venta equipo de gimnasio"],
        "Términos y condiciones", "WebPage", None,
    ),
    "politica-devoluciones": (
        "Política de Garantías, Devoluciones y Reembolsos | Integral Gym Tech",
        "Política de garantías, devoluciones y reembolsos para equipos de gimnasio de Integral Gym Tech: condiciones, tipos de devolución, proceso y reembolsos.",
        ["política de devoluciones", "garantía equipo de gimnasio", "reembolsos"],
        "Política de devoluciones", "WebPage", None,
    ),
    "404": (
        "Página no encontrada | Integral Gym Tech",
        "La página que buscas no existe. Descubre nuestro equipo para gimnasio profesional y residencial en Querétaro.",
        [],
        "404", "WebPage", None,
    ),
}

BUSINESS = {
    "name": "Integral Gym Tech",
    "legalName": "INTEGRAL GYM TECH S.A. DE C.V.",
    "telephone": "+52 442 127 0018",
    "email": "gerencia@integralgymtech.com",
    "street": "Calle 1, #303, Parque Industrial Jurica",
    "locality": "Santiago de Querétaro",
    "region": "Querétaro",
    "postal": "76120",
    "country": "MX",
    "lat": 20.6597,
    "lng": -100.4319,
    "facebook": "https://www.facebook.com/share/14jmBB9RvvL/",
    "instagram": "https://www.instagram.com/integralgymqro",
    "maps": "https://maps.app.goo.gl/qDbNdcuwhzPoFURi7",
}
