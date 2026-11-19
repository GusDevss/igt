"""Datos SEO por página (title, description, keywords, breadcrumb, tipo de schema)."""

BRAND = "Integral Gym Tech"
SITE = "https://integralgymtech.com"
OG_DEFAULT = "/assets/uploads/2026/08/cropped-IGT-logo-back-black.webp"

BASE_KW = [
    "equipo para gimnasio Querétaro", "aparatos de gimnasio", "venta de equipo de gimnasio",
    "equipo de gimnasio profesional", "Integral Gym Tech", "IGT", "BUGE", "distribuidor BUGE México",
    "equipamiento para gimnasio comercial", "cotización de equipo para gimnasio",
]

# slug: (title, description, [keywords], breadcrumb_name, schema_type, og_image(optional))
PAGES = {
    "index": (
        "Equipamiento para Gimnasios Comerciales en Querétaro | Integral Gym Tech",
        "Equipo para gimnasio profesional y residencial en Querétaro: máquinas de uso rudo, cardio, fuerza, Pilates Reformer y accesorios. Distribuidores de equipos BUGE Fitness en México. Pide tu cotización de equipo para gimnasio.",
        ["equipamiento para gimnasio comercial", "máquinas de gimnasio de uso rudo", "cotización de equipo para gimnasio", "paquetes de equipo para gimnasio", "Integral Gym Tech Querétaro", "equipos BUGE Fitness México", "máquinas BUGE para gimnasio", "equipamiento para gimnasios en San Luis Potosí", "equipo para gimnasio en León Guanajuato", "tienda de aparatos de gimnasio Querétaro", "proveedor de equipo fitness México"],
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
        "Peso Libre para Gimnasio | Bancos, Racks y Máquina Smith | Integral Gym Tech",
        "Equipo de peso libre de uso rudo: banco ajustable para pesas, banco para press de banca, racks, máquina Smith profesional, mancuernas y discos olímpicos. Descarga el catálogo.",
        ["banco ajustable para pesas", "banco para press de banca", "máquina Smith profesional", "rack de sentadillas", "mancuernas", "discos olímpicos"],
        "Peso libre", "CollectionPage", None,
    ),
    "peso-integrado": (
        "Máquinas de Peso Integrado para Gimnasio | Equipo de Fuerza BUGE | IGT Querétaro",
        "Máquinas de peso integrado (selectorizadas) para gimnasio comercial: prensa, extensión y curl de pierna, jalón, press de pecho y más. Equipo de fuerza BUGE resistente y seguro. Consulta el catálogo.",
        ["peso integrado", "máquinas de fuerza", "máquinas selectorizadas", "prensa de pierna",
         "máquina de jalón", "equipo de musculación", "catálogo peso integrado BUGE"],
        "Peso integrado", "CollectionPage", None,
    ),
    "multifuncionales": (
        "Multifuncionales y Multiestaciones para Gimnasio | Equipo BUGE | Integral Gym Tech",
        "Multifuncionales y multiestaciones de gimnasio: poleas, crossover y estaciones de entrenamiento completo para gimnasios, condominios, hoteles y gimnasio en casa. Aprovecha el espacio con equipo BUGE.",
        ["multifuncional de gimnasio", "multiestación", "crossover de poleas", "estación de entrenamiento",
         "aparato multifuncional para casa", "catálogo multiestaciones BUGE"],
        "Multifuncionales", "CollectionPage", None,
    ),
    "pilates": (
        "Reformer de Pilates Profesional en Querétaro | Integral Gym Tech",
        "Venta de reformer de Pilates profesional en Querétaro: reformers de maple y roble, cadillac y accesorios para estudios y gimnasios. Pide el precio de tu reformer de Pilates y equipa tu estudio.",
        ["venta de reformer de pilates", "reformer de pilates profesional", "reformer de pilates precio", "reformer de pilates en Querétaro", "equipamiento para estudios de pilates"],
        "Pilates", "CollectionPage", None,
    ),
    "accesorios": (
        "Accesorios para Gimnasio | Bancos y Trampolines Fitness | Integral Gym Tech",
        "Accesorios para gimnasio: banco de pesas multifuncional, trampolín fitness para ejercicio, mini trampolín para cardio, kettlebells, bumpers, cuerdas y tapetes. Catálogo de accesorios de grado comercial.",
        ["trampolín fitness para ejercicio", "mini trampolín para cardio", "banco de pesas multifuncional", "kettlebells", "accesorios para gimnasio"],
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
        "Equipo de Gimnasio para Condominios y Casas Club | Integral Gym Tech",
        "Equipo de gimnasio para condominios, fraccionamientos y casas club: máquinas durables, seguras y de bajo mantenimiento con diseño del espacio y servicio técnico.",
        ["equipo de gimnasio para condominios", "equipamiento para casas club", "gimnasio para fraccionamiento", "gimnasio residencial"],
        "Condominios – residenciales", "Service", None,
    ),
    "clinicas-fisioterapia": (
        "Equipo para Clínicas de Fisioterapia y Rehabilitación | Integral Gym Tech",
        "Equipo para clínicas de fisioterapia y rehabilitación: bicicletas recumbentes, caminadoras, poleas, pilates y accesorios terapéuticos seguros y de alta calidad en Querétaro.",
        ["equipo para fisioterapia", "equipo de rehabilitación", "aparatos para clínica de fisioterapia",
         "bicicleta recumbente rehabilitación", "pilates terapéutico"],
        "Clínicas de fisioterapia", "Service", None,
    ),
    "estudio-pilates": (
        "Equipamiento para Estudios de Pilates | Reformers | Integral Gym Tech",
        "Equipamiento para estudios de Pilates: reformers profesionales, cadillac y accesorios. Asesoría para abrir o crecer tu estudio de Pilates en Querétaro y todo México.",
        ["equipamiento para estudios de pilates", "reformer de pilates profesional", "abrir estudio de pilates", "venta de reformer de pilates"],
        "Estudio de pilates", "Service", None,
    ),
    "hoteles": (
        "Equipamiento para Gimnasios de Hoteles | Integral Gym Tech",
        "Equipamiento para gimnasios de hoteles: caminadoras, elípticas y máquinas de fuerza de grado comercial, con diseño del espacio, instalación y mantenimiento en Querétaro y todo México.",
        ["equipamiento para gimnasios de hoteles", "equipo de gimnasio para hoteles", "gimnasio para hotel", "amenidades fitness hotel"],
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
        "Equipo para Gimnasios Universitarios | Integral Gym Tech",
        "Equipo para gimnasios universitarios y escuelas: máquinas de uso rudo para tráfico intenso, diseño de espacios y soporte técnico especializado.",
        ["equipo para gimnasios universitarios", "gimnasio universitario", "equipamiento deportivo para universidades"],
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
