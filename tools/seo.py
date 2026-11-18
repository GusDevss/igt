"""Datos SEO por página (title, description, keywords, breadcrumb, tipo de schema)."""

BRAND = "Integral Gym Tech"
SITE = "https://integralgymtech.com"
OG_DEFAULT = "/assets/uploads/2026/08/cropped-IGT-logo-back-black.webp"

BASE_KW = [
    "equipo para gimnasio Querétaro", "aparatos de gimnasio", "venta de equipo de gimnasio",
    "equipo de gimnasio profesional", "Integral Gym Tech", "IGT", "BUGE", "distribuidor BUGE México",
]

# slug: (title, description, [keywords], breadcrumb_name, schema_type, og_image(optional))
PAGES = {
    "index": (
        "Equipo para Gimnasio en Querétaro | Venta de Aparatos de Gimnasio Profesional | Integral Gym Tech",
        "Proveedores líderes de equipo para gimnasio profesional y residencial en Querétaro. Distribuidores exclusivos BUGE: cardio, peso libre, peso integrado, multifuncionales, pilates y accesorios. Arrendamiento, diseño de espacios y mantenimiento. ¡Cotiza hoy!",
        ["equipamiento de gimnasios", "tienda de aparatos de gimnasio Querétaro", "equipo fitness comercial",
         "gimnasio en casa", "caminadoras profesionales", "bicicletas de spinning", "mancuernas y discos",
         "racks y jaulas de potencia", "equipo de pilates reformer", "proveedor de equipo fitness México"],
        "Inicio", "WebPage", "/assets/uploads/2023/09/Ellipse-3.png",
    ),
    "nosotros": (
        "Nosotros | Proveedor Líder de Equipo Fitness desde 2008 en Querétaro | Integral Gym Tech",
        "Conoce a Integral Gym Tech: fundada en Querétaro en 2008, proveedor líder en la industria fitness mexicana y distribuidor exclusivo de la marca BUGE. Equipamos gimnasios, hoteles, empresas, universidades y desarrollos residenciales.",
        ["quiénes somos Integral Gym Tech", "empresa de equipo de gimnasio en Querétaro", "proveedor fitness México",
         "equipamiento integral de gimnasios", "distribuidor exclusivo BUGE"],
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
        "Equipo de Cardio Profesional | Caminadoras, Elípticas y Bicicletas BUGE | IGT Querétaro",
        "Equipo de cardio profesional de uso rudo: caminadoras comerciales, elípticas, bicicletas de spinning, escaladoras y remos BUGE. Durabilidad, seguridad y respaldo real para gimnasios, hoteles y empresas. Consulta el catálogo.",
        ["equipo de cardio", "caminadoras profesionales", "caminadora comercial", "elípticas para gimnasio",
         "bicicletas de spinning", "bicicleta recumbente", "remo para gimnasio", "escaladora", "catálogo cardio BUGE"],
        "Cardio", "CollectionPage", None,
    ),
    "peso-libre": (
        "Peso Libre para Gimnasio | Mancuernas, Discos, Barras y Racks | Integral Gym Tech",
        "Equipo de peso libre para gimnasio profesional y en casa: mancuernas, discos olímpicos, barras, bancos, racks y jaulas de potencia BUGE. Calidad comercial con envíos a todo México. Descarga el catálogo.",
        ["peso libre", "mancuernas", "discos olímpicos", "barras olímpicas", "bancos para gimnasio",
         "rack de sentadillas", "jaula de potencia", "catálogo peso libre BUGE"],
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
        "Equipo de Pilates Profesional | Reformer, Cadillac y Chair | Integral Gym Tech",
        "Equipo de pilates profesional BUGE: reformer, cadillac, chair, barrel y accesorios para estudios de pilates, clínicas y gimnasios. Calidad, precisión y durabilidad. Consulta el catálogo de pilates.",
        ["equipo de pilates", "reformer de pilates", "cama de pilates", "cadillac pilates", "silla de pilates",
         "equipo para estudio de pilates", "catálogo pilates BUGE"],
        "Pilates", "CollectionPage", None,
    ),
    "accesorios": (
        "Accesorios para Gimnasio | Kettlebells, Ligas, Tapetes y Funcional | IGT Querétaro",
        "Accesorios para gimnasio y entrenamiento funcional: kettlebells, balones medicinales, ligas, cuerdas, tapetes, pisos y más. Durabilidad de uso rudo, versatilidad y seguridad. Descarga el catálogo de accesorios.",
        ["accesorios para gimnasio", "kettlebells", "balones medicinales", "ligas de resistencia",
         "piso para gimnasio", "entrenamiento funcional", "catálogo de accesorios"],
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
        "Apertura o Remodelación de Gimnasio | Equipamiento Llave en Mano | Integral Gym Tech",
        "¿Vas a abrir o remodelar tu gimnasio? Te asesoramos en el diseño, equipamiento y financiamiento de gimnasios comerciales en Querétaro y todo México con equipo profesional BUGE.",
        ["abrir un gimnasio", "remodelación de gimnasio", "equipar gimnasio comercial", "cuánto cuesta abrir un gimnasio",
         "proyecto llave en mano gimnasio", "equipamiento de gimnasio comercial"],
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
        "Gimnasios para Condominios y Desarrollos Residenciales | Integral Gym Tech",
        "Equipamiento de gimnasios para condominios, fraccionamientos y desarrollos residenciales: equipo durable, seguro y de bajo mantenimiento, con diseño de espacios y servicio técnico.",
        ["gimnasio para condominio", "gimnasio residencial", "amenidades fitness", "equipo de gimnasio para fraccionamiento",
         "gimnasio para desarrollos inmobiliarios"],
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
        "Equipa tu Estudio de Pilates | Reformers y Equipo Profesional | Integral Gym Tech",
        "Todo para tu estudio de pilates: reformers, cadillac, chairs, barrels y accesorios profesionales. Asesoría para abrir o equipar tu estudio de pilates en Querétaro y México.",
        ["estudio de pilates", "abrir estudio de pilates", "reformer profesional", "equipo de pilates para estudio",
         "máquinas de pilates"],
        "Estudio de pilates", "Service", None,
    ),
    "hoteles": (
        "Gimnasios para Hoteles | Equipamiento Fitness Hotelero | Integral Gym Tech",
        "Equipamiento de gimnasios para hoteles: equipo de cardio y fuerza de grado comercial, diseño del espacio y mantenimiento para ofrecer una experiencia fitness de primer nivel a tus huéspedes.",
        ["gimnasio para hotel", "equipamiento hotelero fitness", "equipo de gimnasio para hoteles",
         "amenidades de hotel gimnasio"],
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
        "Gimnasios para Universidades y Escuelas | Equipamiento Deportivo | Integral Gym Tech",
        "Equipamiento de gimnasios para universidades, escuelas y centros deportivos: equipo resistente para uso intensivo, diseño de espacios y servicio técnico especializado.",
        ["gimnasio universitario", "equipo de gimnasio para escuelas", "equipamiento deportivo universidades",
         "gimnasio para instituciones educativas"],
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
