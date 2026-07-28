import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)

def build_pdf(filename):
    # Page size: Letter (612 x 792 pt). Margins: 30pt left/right, 30pt top/bottom. Printable width = 552 pt.
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=30, rightMargin=30,
        topMargin=30, bottomMargin=30
    )

    styles = getSampleStyleSheet()
    
    # Palette Elegante Executive
    COLOR_PRIMARY = colors.HexColor('#6366f1')   # Indigo / Royal Purple
    COLOR_SECONDARY = colors.HexColor('#05050f') # Deep Midnight Navy
    COLOR_ACCENT = colors.HexColor('#06b6d4')    # Electric Cyan
    COLOR_EMERALD = colors.HexColor('#10b981')   # Emerald Green
    COLOR_GOLD = colors.HexColor('#f59e0b')      # Amber Gold
    COLOR_TEXT = colors.HexColor('#1e293b')      # Slate 800
    COLOR_BG_LIGHT = colors.HexColor('#f8fafc')  # Background Tint
    COLOR_BORDER = colors.HexColor('#cbd5e1')

    # Typography ajustada para densidad de contenido perfecta
    cover_title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=19, leading=23, textColor=colors.white
    )
    cover_sub_style = ParagraphStyle(
        'CoverSub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor('#cbd5e1')
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12.5, leading=15.5, textColor=COLOR_SECONDARY, spaceAfter=4, spaceBefore=6
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.8, leading=13, textColor=COLOR_PRIMARY, spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.2, leading=11.6, textColor=COLOR_TEXT, spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=body_style,
        leftIndent=10, firstLineIndent=-6, spaceAfter=3
    )
    table_header_style = ParagraphStyle(
        'TH', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.8, leading=10, textColor=colors.white
    )
    table_cell_style = ParagraphStyle(
        'TC', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=10.2, textColor=COLOR_TEXT
    )

    story = []

    # =============================================================
    # PÁGINA 1: PORTADA & BENCHMARKING INTERNACIONAL + DIAGNÓSTICO
    # =============================================================
    header_data = [[
        Paragraph("<b>DOSSIER MAESTRO COMERCIAL & ARQUITECTURA TECNOLÓGICA v4.5</b><br/>PROPUESTA DE INTEGRACIÓN ENTERPRISE INMOBILIARIA", cover_title_style),
    ], [
        Paragraph("<b>SECRETARÍA CAMILA™ + CHATBOT AI GENERATIVO 24/7</b><br/>"
                  "La primera Plataforma Autónoma de Ventas, Calificación BANT y Atribución ROI Inmobiliaria<br/>"
                  "<i>Especialmente diseñada para Inmobiliarias, Corredoras y Loteos de la Región de Los Lagos</i>", cover_sub_style)
    ]]

    header_table = Table(header_data, colWidths=[552])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,1), (-1,1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. BENCHMARKING DE MERCADO INTERNACIONAL & VALOR ENTERPRISE DE LA TECNOLOGÍA", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=5))

    p_bench = ("A nivel mundial en los mercados inmobiliarios más avanzados de Estados Unidos y Latinoamérica, las soluciones de "
               "<b>Agentes de Ventas Autónomos con Inteligencia Artificial (AI Sales SDRs)</b> representan la tecnología de mayor retorno comercial. "
               "Plataformas internacionales como <b>Conversica, Qualified (Piper AI) o Intercom Fin AI</b> registran los siguientes valores de mercado:")
    story.append(Paragraph(p_bench, body_style))

    bench_data = [
        [Paragraph("Plataforma AI Internacional", table_header_style), Paragraph("Modelo de Cobro", table_header_style), Paragraph("Costo Anual / Mensual Estimado", table_header_style), Paragraph("Limitaciones Comerciales", table_header_style)],
        [
            Paragraph("<b>Conversica Real Estate AI</b>", table_cell_style),
            Paragraph("Contrato Enterprise Anual", table_cell_style),
            Paragraph("<b>$30.000+ USD / año</b><br/>(~$2.500 USD / mes)", table_cell_style),
            Paragraph("Diseñado solo para grandes corporativos de EE.UU.", table_cell_style)
        ],
        [
            Paragraph("<b>Qualified (Piper AI)</b>", table_cell_style),
            Paragraph("Licencia por Tráfico / CRM", table_cell_style),
            Paragraph("<b>$40.000 - $68.000 USD / año</b><br/>(~$3.500 - $5.500 USD / mes)", table_cell_style),
            Paragraph("Dependencia de Salesforce y costo elevado por lead.", table_cell_style)
        ],
        [
            Paragraph("<b>Intercom Fin AI</b>", table_cell_style),
            Paragraph("Pago por Resolución + Sede", table_cell_style),
            Paragraph("<b>$0.99 USD / resolución</b><br/>(~$1.200 USD / mes para 1k chats)", table_cell_style),
            Paragraph("Costos impredecibles que aumentan con el tráfico.", table_cell_style)
        ],
        [
            Paragraph("<b>Secretaría Camila™ (Nuestra Solución v4.5)</b>", table_cell_style),
            Paragraph("Suscripción Plana LATAM", table_cell_style),
            Paragraph("<b>$590.000 - $1.290.000 CLP / mes</b><br/>(~$630 - $1.380 USD / mes)", table_cell_style),
            Paragraph("<b>Cero costo por resolución, dictado por voz 🎙️ y Base de Datos SQL.</b>", table_cell_style)
        ]
    ]

    t_bench = Table(bench_data, colWidths=[120, 110, 150, 172])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. DIAGNÓSTICO DEL MERCADO EN LA REGIÓN DE LOS LAGOS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=5))

    p1 = ("En la Región de Los Lagos (Puerto Varas, Puerto Montt, Frutillar, Llanquihue, Osorno y Chiloé), el 68% del tráfico web ocurre "
          "<b>fuera de horario de oficina (20:00 a 01:00 hrs y fines de semana)</b>. Compradores de Santiago o Concepción buscan parcelas de 5.000m² "
          "y proyectos de noche. Si encuentran un formulario estático que responde en 48 hrs, el 70% abandona la web. "
          "<b>Secretaría Camila™ captura ese lead en &lt;3 segundos y lo notifica al celular del corredor.</b>")
    story.append(Paragraph(p1, body_style))

    steps_data = [
        [Paragraph("Paso", table_header_style), Paragraph("Acción del Visitante / IA", table_header_style), Paragraph("Proceso Interno & Resultado", table_header_style)],
        [
            Paragraph("<b>Paso 1</b>", table_cell_style),
            Paragraph("<b>Navegación:</b> El cliente ve una parcela en Frutillar de $55M CLP a las 23:15 hrs.", table_cell_style),
            Paragraph("Camila lee automáticamente la ubicación, precio y superficie de la parcela en vista.", table_cell_style)
        ],
        [
            Paragraph("<b>Paso 2</b>", table_cell_style),
            Paragraph("<b>Saludo Conversacional:</b> Saluda en vivo y resuelve dudas del loteo.", table_cell_style),
            Paragraph("IA Generativa Llama 3.1 70B responde en máximo 2 párrafos cortos sin sonar a robot estático.", table_cell_style)
        ],
        [
            Paragraph("<b>Paso 3</b>", table_cell_style),
            Paragraph("<b>Calificación BANT:</b> Indaga pago al contado vs crédito hipotecario y plazo.", table_cell_style),
            Paragraph("Calcula el Score del Lead en tiempo real (0-100 pts) de forma natural.", table_cell_style)
        ],
        [
            Paragraph("<b>Paso 4</b>", table_cell_style),
            Paragraph("<b>Captura de Teléfono:</b> El cliente escribe su WhatsApp para recibir la ficha.", table_cell_style),
            Paragraph("El motor detecta el patrón telefónico y extrae el contacto instantáneamente.", table_cell_style)
        ],
        [
            Paragraph("<b>Paso 5</b>", table_cell_style),
            Paragraph("<b>Notificación Instantánea (&lt;3s):</b> Alerta a Telegram / WhatsApp Business.", table_cell_style),
            Paragraph("El corredor recibe la ficha completa etiquetada con <code>FUERA DE HORARIO</code> para llamar en el acto.", table_cell_style)
        ]
    ]

    t_steps = Table(steps_data, colWidths=[45, 235, 272])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_steps)

    story.append(PageBreak()) # PÁGINA 2 COMPLETA Y Densa

    # =============================================================
    # PÁGINA 2: BASE DE DATOS SQL, IMPORTADOR MULTI-FORMATO & SIMBIOSIS
    # =============================================================
    story.append(Paragraph("3. MOTOR DE BASE DE DATOS SQL ($0 USD) E IMPORTADOR MULTI-FORMATO", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=5))

    p_db = ("La versión v4.5 incorpora un **Motor de Base de Datos Relacional SQL (CamilaDB)** compatible con **SQLite Local ($0 USD)** y **Turso Cloud SQLite (9 GB gratis en la nube)**, estructurando 4 tablas clave para la gestión inmobiliaria:")
    story.append(Paragraph(p_db, body_style))

    story.append(Paragraph("• <b>Tabla `leads`:</b> Almacena el pipeline completo de prospectos (Nombre, Teléfono, Email, Score BANT, Estado Comercial y Notificaciones).", bullet_style))
    story.append(Paragraph("• <b>Tabla `properties`:</b> Catálogo de parcelas, loteos y departamentos (Ubicación, Superficie m², Precio CLP, Atributos y Disponibilidad).", bullet_style))
    story.append(Paragraph("• <b>Tabla `interactions`:</b> Historial completo de chats y mensajes intercambiados entre el cliente y Camila.", bullet_style))
    story.append(Paragraph("• <b>Tabla `sales_roi`:</b> Registro fidedigno de comisiones e ingresos generados para el cálculo de atribución ROI.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Importador Universal Multi-Formato (CSV, XML, JSON):</b>", h2_style))
    p_imp = ("El sistema permite a la corredora o inmobiliaria **subir su cartera histórica de clientes en 1 click**. "
             "El parser universal detecta automáticamente archivos **CSV** (exportados de Excel), **XML** (`<lead><name>...</name></lead>`) y **JSON**, "
             "incorporando miles de contactos a la base de datos SQL de Secretaría Camila sin costo adicional.")
    story.append(Paragraph(p_imp, body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. LA SIMBIOSIS Y LA CONEXIÓN INMOBILIARIA EN TIEMPO REAL", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=5))

    symbiosis_data = [
        [Paragraph("Componente", table_header_style), Paragraph("Rol en el Negocio Inmobiliario", table_header_style), Paragraph("Interacción Práctica del Equipo", table_header_style)],
        [
            Paragraph("<b>CHATBOT WEB 24/7</b><br/>(La Antena Receptora)", table_cell_style),
            Paragraph("Vive en la esquina de tu sitio web (<code>www.sucorredora.cl</code>). Es la cara visible que saluda, califica y atiende a los visitantes 24/7.", table_cell_style),
            Paragraph("Opera de forma 100% autónoma sin intervención humana, respondiendo dudas de parcelas y proyectos en tiempo real.", table_cell_style)
        ],
        [
            Paragraph("<b>PLATAFORMA AUTÓNOMA</b><br/>(El Cerebro del CEO)", table_cell_style),
            Paragraph("Es el Centro de Mando privado del dueño o gerente comercial (<code>https://camila.sucorredora.cl</code>). Contiene el CRM, proyecciones e inteligencia de ventas.", table_cell_style),
            Paragraph("El corredor habla con Camila por dictado de voz 🎙️, gestiona el pipeline de prospectos y dispara conversaciones por WhatsApp.", table_cell_style)
        ]
    ]

    t_symbiosis = Table(symbiosis_data, colWidths=[130, 205, 217])
    t_symbiosis.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_symbiosis)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Acciones Prácticas que el Dueño/Corredor efectúa en la Plataforma:</b>", h2_style))
    story.append(Paragraph("• <b>Edición Completa 100% de Registros:</b> Todos los prospectos pasados y futuros, así como las parcelas e inmuebles del catálogo, son totalmente editables desde el panel (modificar títulos, precios, metrajes m², notas y estados comerciales).", bullet_style))
    story.append(Paragraph("• <b>Dictado de Voz 🎙️:</b> El CEO presiona el micrófono de voz y consulta directamente a Camila por el resumen de ventas e inventario disponible.", bullet_style))
    story.append(Paragraph("• <b>Disparador Directo a WhatsApp:</b> Click instantáneo en el botón de WhatsApp al lado del prospecto para iniciar llamadas o chats en 1 segundo.", bullet_style))
    story.append(Paragraph("• <b>Selector de Temas Ultra-Blur:</b> 3 estilos visuales ejecutivos (Gris Claro Platinum por defecto, Oscuro Onyx y Esmeralda Corporativo).", bullet_style))

    story.append(PageBreak()) # PÁGINA 3 COMPLETA

    # =============================================================
    # PÁGINA 3: ESCALABILIDAD TECNOLÓGICA & VENTAJA COMPETITIVA
    # =============================================================
    story.append(Paragraph("5. ESCALABILIDAD TECNOLÓGICA Y ARQUITECTURA EN CASCADA 70B", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=5))

    story.append(Paragraph("• <b>Inyección Dinámica de Catálogo SQL a la IA:</b> Cada vez que un usuario pregunta por parcelas en la web, Camila consulta la base de datos SQL en tiempo real y recomienda exactamente los loteos disponibles con sus superficies en m² y precios en $ CLP.", bullet_style))
    story.append(Paragraph("• <b>Arquitectura de IA Generativa en Cascada 70B:</b> Motor primario **NVIDIA NIM Llama 3.1 70B** con conmutación automática a **OpenRouter 70B Fallback**. Si un servidor sufre latencia, el segundo responde sin interrupciones.", bullet_style))
    story.append(Paragraph("• <b>Ahorro Ultra-Eficiente en n8n (Opción 1):</b> Las conversaciones casuales no gastan ejecuciones de n8n. El servidor conmuta a n8n 1 sola vez por cliente cuando este entrega su teléfono o agenda una cita (**Ahorro del 90%+**).", bullet_style))
    story.append(Paragraph("• <b>Notificaciones Duales Instantáneas:</b> Alertas a Telegram Bot y/o WhatsApp Business en menos de 3 segundos.", bullet_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("6. VENTAJA COMPETITIVA INSUPERABLE CONTRA LA COMPETENCIA", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=5))

    comp_data = [
        [Paragraph("Característica", table_header_style), Paragraph("Chatbot Tradicional / WhatsApp Bot Rígido", table_header_style), Paragraph("Secretaría Camila™ IA 24/7 v4.5", table_header_style)],
        [
            Paragraph("<b>Fluidez Conversacional</b>", table_cell_style),
            Paragraph("Menús rígidos molestos (<i>'Marca 1 para parcelas, 2 para casas'</i>). El cliente se frustra.", table_cell_style),
            Paragraph("<b>Conversación humana fluida.</b> Comprende lenguaje natural y responde en 2 párrafos.", table_cell_style)
        ],
        [
            Paragraph("<b>Conocimiento de Propiedades</b>", table_cell_style),
            Paragraph("Solo responde texto estático preprogramado en listas fijas.", table_cell_style),
            Paragraph("<b>Consulta la base de datos SQL</b> y recomienda parcelas disponibles en vivo.", table_cell_style)
        ],
        [
            Paragraph("<b>Disparo de Alertas</b>", table_cell_style),
            Paragraph("Envía correos masivos que terminan en la carpeta de Spam.", table_cell_style),
            Paragraph("<b>Alerta a Telegram / WhatsApp Business en &lt;3s</b> etiquetada con horario de rescate.", table_cell_style)
        ],
        [
            Paragraph("<b>Consola para el CEO</b>", table_cell_style),
            Paragraph("No tiene consola. Solo entrega una planilla Excel a fin de mes.", table_cell_style),
            Paragraph("<b>Plataforma Autónoma 100% Editable con dictado 🎙️</b>, CRM y WhatsApp.", table_cell_style)
        ],
        [
            Paragraph("<b>Atribución de Ventas ROI</b>", table_cell_style),
            Paragraph("Imposible saber qué ventas provinieron del bot.", table_cell_style),
            Paragraph("<b>Medición de Atribución ROI fidedigna</b> con reporte exportable en PDF.", table_cell_style)
        ]
    ]

    t_comp = Table(comp_data, colWidths=[130, 205, 217])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Modalidades de Adquisición Comercial:</b>", h2_style))
    story.append(Paragraph("• <b>Modalidad SaaS Gestionada (Recomendada):</b> $590.000 CLP / mes. Incluye hosting 24/7 en Render, APIs de IA 70B, base de datos SQL y soporte técnico continuo.", bullet_style))
    story.append(Paragraph("• <b>Modalidad Licencia Perpetua ('Llave en Mano'):</b> $1.290.000 CLP Pago Único. Instalación completa en los servidores del cliente para que sea dueño absoluto del software.", bullet_style))

    story.append(PageBreak()) # PÁGINA 4 COMPLETA

    # =============================================================
    # PÁGINA 4: PLANES DE INVERSIÓN & CERRADO COMERCIAL
    # =============================================================
    story.append(Paragraph("7. ESTRUCTURA DE INVERSIÓN COMERCIAL ENTERPRISE EN CHILE ($ CLP)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=5))

    p_pricing_intro = ("Considerando el valor real de mercado internacional ($30.000 USD/año en plataformas como Conversica o Qualified) "
                       "y la potencia de la Inteligencia Artificial Generativa 70B incorporada, la estructura de inversión corporativa se establece en:")
    story.append(Paragraph(p_pricing_intro, body_style))

    planes_data = [
        [Paragraph("Plan Comercial", table_header_style), Paragraph("Inversión Mensual ($ CLP)", table_header_style), Paragraph("Incluye & Alcance Corporativo", table_header_style)],
        [
            Paragraph("<b>PLAN CORREDORA PRO</b><br/><i>Para corredoras de propiedades de la zona</i>", table_cell_style),
            Paragraph("<b>$590.000 CLP</b><br/>+ IVA / mes<br/><i>(~$630 USD/mes)</i>", table_cell_style),
            Paragraph("• ChatBot IA 24/7 en sitio web (1 dominio).<br/>• Alertas a Telegram y/o WhatsApp Business.<br/>• Plataforma Autónoma 100% Editable con micrófono de voz y CRM.<br/>• Atribución de Ventas e impresor de informes ROI.", table_cell_style)
        ],
        [
            Paragraph("<b>PLAN INMOBILIARIA MULTI-PROYECTO</b><br/><i>Para desarrolladores inmobiliarios y loteos</i>", table_cell_style),
            Paragraph("<b>$1.290.000 CLP</b><br/>+ IVA / mes<br/><i>(~$1.380 USD/mes)</i>", table_cell_style),
            Paragraph("• Todo lo del Plan Pro.<br/>• Cobertura multi-proyecto y loteos ilimitados.<br/>• Importador Universal de Cartera (CSV/XML/JSON).<br/>• Integración con CRM (HubSpot, Salesforce, Tokko).<br/>• Capacitación a ejecutivos + Prompt a medida.", table_cell_style)
        ],
        [
            Paragraph("<b>PLAN ENTERPRISE DEDICADO</b><br/><i>Para grandes corporativos o franquicias</i>", table_cell_style),
            Paragraph("<b>$2.490.000 CLP</b><br/>+ IVA / mes<br/><i>(~$2.650 USD/mes)</i>", table_cell_style),
            Paragraph("• Servidor dedicado autónomo en Render.com.<br/>• Base de Datos Turso Cloud SQLite dedicada.<br/>• IA entrenada con data propia de la empresa.<br/>• API exclusiva y soporte prioritario 24/7.", table_cell_style)
        ],
        [
            Paragraph("<b>SETUP INICIAL & PUESTA EN MARCHA</b><br/><i>Pago único por única vez</i>", table_cell_style),
            Paragraph("<b>$490.000 CLP</b><br/>(Pago Único)", table_cell_style),
            Paragraph("• Configuración de servidor autónomo en Render.com.<br/>• Entrenamiento del prompt con la cartera de propiedades del cliente.<br/>• Prueba de carga y verificación de notificaciones.", table_cell_style)
        ]
    ]

    t_planes = Table(planes_data, colWidths=[150, 130, 272])
    t_planes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_planes)
    story.append(Spacer(1, 8))

    # JUSTIFICACIÓN FINANCIERA DE ALTO IMPACTO
    story.append(Paragraph("<b>Justificación Financiera e Insuperable Retorno de Inversión (ROI):</b>", h2_style))
    story.append(Paragraph("1. <b>Comparativa contra Personal Humano:</b> Contratar ejecutivos humanos para cubrir turnos nocturnos y fines de semana cuesta más de <b>$1.200.000 CLP mensuales</b> por turno (más leyes sociales e imposiciones). Camila cuesta la mitad, trabaja los 365 días del año, jamás pide licencias y atiende a 100 clientes en paralelo.", bullet_style))
    story.append(Paragraph("2. <b>Retorno de Inversión Inmediato:</b> Con <b>UNA SOLA parcela o departamento vendido al año</b> rescatado un domingo a las 11 PM, la corredora recupera el costo de <b>2 a 3 años completos del servicio de Camila</b>. Todo lo demás es utilidad neta para la empresa.", bullet_style))

    story.append(Spacer(1, 10))

    # FOOTER CLOSING
    footer_data = [[
        Paragraph("<b>¿Listo para dotar a tu inmobiliaria con la mejor tecnología de IA del mercado mundial?</b><br/>"
                  "Contáctanos hoy para activar la versión de prueba de Secretaría Camila™ v4.5 en tu sitio web.", ParagraphStyle('FText5', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.white, alignment=1))
    ]]
    t_footer = Table(footer_data, colWidths=[552])
    t_footer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_footer)

    doc.build(story)
    print(f"Dossier Maestro PDF totalmente rellenado generado exitosamente en: {filename}")

if __name__ == '__main__':
    out_dir = r"c:\Users\LyCoNs\Desktop\Secretaria Camila+CHATBOTAI"
    pdf_path = os.path.join(out_dir, "DOSSIER_COMERCIAL_SECRETARIA_CAMILA_V4_LOS_LAGOS.pdf")
    build_pdf(pdf_path)
