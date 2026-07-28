import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)

def build_pdf(filename):
    # Printable area: 612 x 792 pt. Margins: 30pt. Width = 552 pt.
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=30, rightMargin=30,
        topMargin=30, bottomMargin=30
    )

    styles = getSampleStyleSheet()
    
    # Palette Elegante Executive Enterprise v5.5
    COLOR_PRIMARY = colors.HexColor('#0f172a')   # Deep Slate / Onyx
    COLOR_ACCENT = colors.HexColor('#6366f1')    # Indigo / Royal Violet
    COLOR_TEAL = colors.HexColor('#0d9488')      # Deep Emerald Teal
    COLOR_EMERALD = colors.HexColor('#10b981')   # Vibrant Emerald Green
    COLOR_GOLD = colors.HexColor('#f59e0b')      # Amber Gold
    COLOR_TEXT = colors.HexColor('#1e293b')      # Slate 800
    COLOR_BG_LIGHT = colors.HexColor('#f8fafc')  # Soft Tint
    COLOR_BORDER = colors.HexColor('#cbd5e1')

    # Typography
    cover_title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.white
    )
    cover_sub_style = ParagraphStyle(
        'CoverSub', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#cbd5e1')
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=COLOR_PRIMARY, spaceAfter=4, spaceBefore=6
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=12.5, textColor=COLOR_ACCENT, spaceAfter=3
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11.2, textColor=COLOR_TEXT, spaceAfter=3.5
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=body_style,
        leftIndent=8, firstLineIndent=-5, spaceAfter=2.5
    )
    table_header_style = ParagraphStyle(
        'TH', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white
    )
    table_cell_style = ParagraphStyle(
        'TC', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.2, leading=9.8, textColor=COLOR_TEXT
    )

    story = []

    # =============================================================
    # PÁGINA 1: PORTADA & BENCHMARKING DE MERCADO INTERNACIONAL
    # =============================================================
    header_data = [[
        Paragraph("<b>DOSSIER MAESTRO COMERCIAL & ARQUITECTURA TECNOLÓGICA v5.5 ENTERPRISE</b><br/>PROPUESTA DE INTEGRACIÓN ENTERPRISE PAGO ÚNICO (LICENCIA PERPETUA)", cover_title_style),
    ], [
        Paragraph("<b>SECRETARÍA CAMILA™ + CHATBOT AI GENERATIVO 24/7 EN CASCADA 70B</b><br/>"
                  "La primera Plataforma Autónoma de Ventas, Calificación BANT, Motor SQL y Atribución ROI Inmobiliaria<br/>"
                  "<i>Diseñada para Inmobiliarias, Corredoras y Loteos de la Región de Los Lagos (Puerto Varas, Frutillar, Puerto Montt)</i>", cover_sub_style)
    ]]

    header_table = Table(header_data, colWidths=[552])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 11),
        ('BOTTOMPADDING', (0,1), (-1,1), 11),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. BENCHMARKING DE MERCADO INTERNACIONAL & VALOR REAL DE LA TECNOLOGÍA", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=4))

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
            Paragraph("<b>Secretaría Camila™ (Nuestra Solución v5.5)</b>", table_cell_style),
            Paragraph("Pago Único / Licencia Perpetua", table_cell_style),
            Paragraph("<b>$590.000 - $1.290.000 CLP (Pago Único)</b><br/>(~$630 - $1.380 USD Pago Único)", table_cell_style),
            Paragraph("<b>Sin cobros mensuales recurrentes, cliente dueño absoluto del software.</b>", table_cell_style)
        ]
    ]

    t_bench = Table(bench_data, colWidths=[120, 110, 150, 172])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. DIAGNÓSTICO DEL MERCADO EN LA REGIÓN DE LOS LAGOS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=4))

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
        ('BACKGROUND', (0,0), (-1,0), COLOR_ACCENT),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_steps)

    story.append(PageBreak()) # PÁGINA 2 COMPLETA

    # =============================================================
    # PÁGINA 2: CÓMO FUNCIONA EL CHATBOT WEB + SECRETARÍA CAMILA (PARTE I)
    # =============================================================
    story.append(Paragraph("3. CÓMO FUNCIONA EL CHATBOT WEB & LA SECRETARÍA CAMILA (PARTE I)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=5))

    p_func1 = ("Secretaría Camila™ opera como una arquitectura de doble motor en tiempo real: el **Chatbot Web 24/7** que reside en el sitio comercial del cliente como antena receptora, y la **Plataforma Autónoma del CEO**, el centro de mando donde se concentran los leads, el CRM y la inteligencia de ventas. A continuación se detallan sus primeras 4 habilidades principales:")
    story.append(Paragraph(p_func1, body_style))

    story.append(Paragraph("<b>SKILL 1: Calificación Conversacional BANT & Scoring en Tiempo Real (0-100 Pts)</b>", h2_style))
    p_s1 = ("A diferencia de los formularios rígidos, Camila interactúa mediante **Lenguaje Natural (NPL)** impulsado por Llama 3.1 70B. "
            "Descubre la capacidad de compra del visitante indagando sutilmente cuatro pilares (Presupuesto, Autoridad de Decisión, Necesidad de Metraje m² y Tiempo de Compra). "
            "Asigna automáticamente un **Lead Score BANT de 0 a 100 puntos**, permitiendo al equipo comercial priorizar de inmediato a los clientes de mayor valor.")
    story.append(Paragraph(p_s1, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>SKILL 2: Inyección Dinámica y Consulta de Catálogo SQL en Tiempo Real</b>", h2_style))
    p_s2 = ("Camila no responde con textos genéricos pregrabados. Está conectada directamente a la **Base de Datos SQL de Propiedades**. "
            "Cuando un usuario pregunta por parcelas en Frutillar o departamentos en Puerto Montt, Camila ejecuta una consulta SQL en vivo e inyecta "
            "las parcelas disponibles en el prompt de la IA, respondiendo con superficies exactas en m², ubicaciones precisas y precios en $ CLP.")
    story.append(Paragraph(p_s2, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>SKILL 3: Captura Inteligente de WhatsApp / Teléfono & Detector de Intención</b>", h2_style))
    p_s3 = ("El motor conversacional detecta patrones numéricos telefónicos chilenos e internacionales (`+569...`) durante el diálogo. "
            "Al identificar la intención de compra del cliente, Camila solicita de forma elegante su WhatsApp para enviarle la ficha técnica del loteo. "
            "El teléfono es validado, etiquetado y registrado en la base de datos de manera instantánea.")
    story.append(Paragraph(p_s3, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>SKILL 4: Disparo Instantáneo de Alertas Duales (&lt;3s) a Telegram Bot / WhatsApp Business</b>", h2_style))
    p_s4 = ("Al momento en que se captura el teléfono o se concreta una solicitud de cita, Camila despacha una **Notificación Dual en menos de 3 segundos** "
            "al celular del corredor o gerente vía Telegram Bot y/o WhatsApp Business. La alerta incluye la ficha completa del prospecto, su puntuación Score, "
            "el requerimiento específico y una etiqueta de horario para llamada de rescate inmediata.")
    story.append(Paragraph(p_s4, body_style))

    story.append(Spacer(1, 6))
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
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_symbiosis)

    story.append(PageBreak()) # PÁGINA 3 COMPLETA

    # =============================================================
    # PÁGINA 3: CÓMO FUNCIONA EL CHATBOT WEB + SECRETARÍA CAMILA (PARTE II - MATRIZ DE SKILLS)
    # =============================================================
    story.append(Paragraph("4. MATRIZ DE SKILLS Y COMPETENCIAS AUTÓNOMAS DE CAMILA (PARTE II)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=5))

    p_func2 = ("Complementando la atención conversacional en la web, la Plataforma Autónoma proporciona al CEO y al equipo comercial 4 habilidades ejecutivas avanzadas para la gestión diaria del negocio inmobiliario:")
    story.append(Paragraph(p_func2, body_style))

    story.append(Paragraph("<b>SKILL 5: Importador Universal Multi-Formato (CSV / XML / JSON)</b>", h2_style))
    p_s5 = ("La plataforma permite a la corredora **subir su cartera histórica de clientes en 1 click**. "
            "El parser universal detecta automáticamente archivos **CSV** (exportados de Excel), **XML** (`<lead><name>...</name></lead>`) y **JSON**, "
            "incorporando miles de contactos a la base de datos SQL de Secretaría Camila sin costo adicional ni límite de volumen.")
    story.append(Paragraph(p_s5, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>SKILL 6: Auto-Entrenamiento y Analítica de Patrones Inmobiliarios en Vivo</b>", h2_style))
    p_s6 = ("Camila analiza continuamente los datos almacenados en SQL para calcular métricas clave: precio promedio de parcelas en catálogo, "
            "porcentaje real de prospectos capturados fuera de horario laboral y sectores de mayor demanda en la Región de Los Lagos. "
            "Genera automáticamente su propio System Prompt actualizado con los datos del catálogo en vivo (`/api/secretaria/ai-training-sync`).")
    story.append(Paragraph(p_s6, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>SKILL 7: Dictado de Voz 🎙️ y Consola Ejecutiva 100% Editable (3 Temas Ultra-Blur)</b>", h2_style))
    p_s7 = ("El dueño o corredor puede interactuar por **dictado de voz directo** con Camila para pedirle resúmenes de inventario y prospectos. "
            "Además, **todos los registros pasados y futuros son 100% editables** (modificar títulos de parcelas, ubicaciones, precios $ CLP, metrajes m², notas y estados comerciales). "
            "Cuenta con un selector de 3 estilos visuales ejecutivos sin emojis (Gris Claro Platinum por defecto, Oscuro Onyx y Esmeralda Corporativo).")
    story.append(Paragraph(p_s7, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>SKILL 8: Medición Fidedigna de Atribución de Ventas e Impresión de Reportes ROI</b>", h2_style))
    p_s8 = ("Cada prospecto capturado recibe un ID de atribución único que rastrea su ciclo de venta completo desde la primera interacción. "
            "El sistema calcula el retorno de inversión real obtenido por las ventas cerradas y permite imprimir un **Reporte Certificado de ROI** para la gerencia.")
    story.append(Paragraph(p_s8, body_style))

    story.append(Spacer(1, 6))
    skills_matrix_data = [
        [Paragraph("Habilidad Autónoma (Skill)", table_header_style), Paragraph("Entorno de Operación", table_header_style), Paragraph("Valor Comercial Inmobiliario", table_header_style)],
        [
            Paragraph("<b>Skill 1: Calificación BANT (0-100)</b>", table_cell_style),
            Paragraph("Chatbot Web 24/7", table_cell_style),
            Paragraph("Filtra automáticamente curiosos de compradores reales con presupuesto.", table_cell_style)
        ],
        [
            Paragraph("<b>Skill 2: Consulta SQL en Vivo</b>", table_cell_style),
            Paragraph("Motor de Base de Datos SQL", table_cell_style),
            Paragraph("Inyecta datos exactos de parcelas (m² y $ CLP) en las respuestas de la IA.", table_cell_style)
        ],
        [
            Paragraph("<b>Skill 3: Captura de WhatsApp</b>", table_cell_style),
            Paragraph("Chatbot Web 24/7", table_cell_style),
            Paragraph("Extrae y valida teléfonos de forma natural durante la conversación.", table_cell_style)
        ],
        [
            Paragraph("<b>Skill 4: Alertas Duales (&lt;3s)</b>", table_cell_style),
            Paragraph("Telegram Bot / WhatsApp Biz", table_cell_style),
            Paragraph("Despacha fichas de prospectos al celular del corredor en tiempo real.", table_cell_style)
        ],
        [
            Paragraph("<b>Skill 5: Importador Universal</b>", table_cell_style),
            Paragraph("Plataforma Autónoma CEO", table_cell_style),
            Paragraph("Sube bases de datos históricas de Excel (CSV/XML/JSON) en 1 click.", table_cell_style)
        ],
        [
            Paragraph("<b>Skill 6: Auto-Entrenamiento SQL</b>", table_cell_style),
            Paragraph("Motor Inteligente Backend", table_cell_style),
            Paragraph("Genera prompts dinámicos y analiza patrones de demanda automáticamente.", table_cell_style)
        ],
        [
            Paragraph("<b>Skill 7: Dictado 🎙️ & Edición Total</b>", table_cell_style),
            Paragraph("Consola Ejecutiva Ultra-Blur", table_cell_style),
            Paragraph("Permite hablarle a Camila y editar cualquier campo de prospectos y parcelas.", table_cell_style)
        ],
        [
            Paragraph("<b>Skill 8: Atribución de Ventas ROI</b>", table_cell_style),
            Paragraph("Plataforma Autónoma CEO", table_cell_style),
            Paragraph("Mide ingresos exactos aportados por Camila e imprime reportes en PDF.", table_cell_style)
        ]
    ]

    t_skills = Table(skills_matrix_data, colWidths=[140, 150, 262])
    t_skills.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_skills)

    story.append(PageBreak()) # PÁGINA 4 COMPLETA

    # =============================================================
    # PÁGINA 4: ARQUITECTURA TÉCNICA SQL, CASCADA 70B & EFICIENCIA n8n
    # =============================================================
    story.append(Paragraph("5. ARQUITECTURA TÉCNICA DE BASE DE DATOS Y CASCADA LLM 70B", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=5))

    story.append(Paragraph("• <b>Motor de Base de Datos Relacional SQL (CamilaDB):</b> Opera por defecto con **SQLite Local ($0 USD - Automático sin costo)** para almacenar hasta 100.000 prospectos y parcelas en Render.com. Permite conmutar opcionalmente a **Turso Cloud SQLite (9 GB gratis en la nube)** para almacenar más de 2.000.000 de registros.", bullet_style))
    story.append(Paragraph("• <b>Estructura de 4 Tablas SQL Dedicadas:</b> Tabla `leads` (pipeline de prospectos BANT), Tabla `properties` (catálogo de parcelas m² y $ CLP), Tabla `interactions` (historial conversacional) y Tabla `sales_roi` (registro fidedigno de comisiones e ingresos).", bullet_style))
    story.append(Paragraph("• <b>Arquitectura de IA Generativa en Cascada 70B:</b> Motor primario **NVIDIA NIM Llama 3.1 70B Instruct** con conmutación automática e instantánea a **OpenRouter Llama 3.1 70B Fallback**. Si un servidor sufre latencia, el segundo responde sin interrupciones.", bullet_style))
    story.append(Paragraph("• <b>Ahorro Ultra-Eficiente en ejecuciones de n8n (Opción 1):</b> Las conversaciones informales no consumen ejecuciones de n8n. El servidor conmuta a n8n 1 sola vez por cliente cuando este entrega su teléfono o agenda una cita (**Ahorro comprobado del 90%+ en ejecuciones**).", bullet_style))
    story.append(Paragraph("• <b>Notificaciones Duales Instantáneas:</b> Alertas a Telegram Bot y/o WhatsApp Business en menos de 3 segundos etiquetadas con horario de rescate.", bullet_style))

    story.append(Spacer(1, 6))

    story.append(Paragraph("6. VENTAJA COMPETITIVA INSUPERABLE CONTRA LA COMPETENCIA", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=5))

    comp_data = [
        [Paragraph("Característica", table_header_style), Paragraph("Chatbot Tradicional / WhatsApp Bot Rígido", table_header_style), Paragraph("Secretaría Camila™ IA 24/7 v5.5", table_header_style)],
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
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_comp)

    story.append(PageBreak()) # PÁGINA 5 COMPLETA

    # =============================================================
    # PÁGINA 5: MODELO COMERCIAL PAGO ÚNICO (LICENCIA PERPETUA LLAVE EN MANO)
    # =============================================================
    story.append(Paragraph("7. MODELO COMERCIAL ENTERPRISE 100% PAGO ÚNICO (LICENCIA PERPETUA)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=5))

    p_mod_intro = ("Nuestra propuesta comercial se basa en un **Modelo de Licencia Perpetua 'Llave en Mano' (100% Pago Único)**, "
                   "sin cobros mensuales ni suscripciones recurrentes cobradas por nuestra empresa. La inmobiliaria es dueña absoluta de su software:")
    story.append(Paragraph(p_mod_intro, body_style))

    modalities_data = [
        [Paragraph("Modalidad Comercial", table_header_style), Paragraph("Estructura de Cobro", table_header_style), Paragraph("Servicios Incluidos & Alcance Corporativo", table_header_style)],
        [
            Paragraph("<b>LICENCIA PERPETUA PRO</b><br/><i>(Para Corredoras de Propiedades)</i>", table_cell_style),
            Paragraph("<b>$590.000 CLP</b><br/>(Pago Único por única vez)", table_cell_style),
            Paragraph("• El cliente es dueño absoluto de su software instalado.<br/>• ChatBot IA 24/7 en sitio web + Alertas a Telegram/WhatsApp Business.<br/>• Plataforma Autónoma 100% Editable con micrófono de voz y CRM.<br/>• Sin suscripciones mensuales recurrentes.", table_cell_style)
        ],
        [
            Paragraph("<b>LICENCIA PERPETUA ENTERPRISE MULTI-PROYECTO</b><br/><i>(Incluye Capacidades Enterprise)</i>", table_cell_style),
            Paragraph("<b>$1.290.000 CLP</b><br/>(Pago Único por única vez)", table_cell_style),
            Paragraph("• **Todo lo del Plan Pro + Servidor Dedicado Autónomo en Render.com**.<br/>• **Base de Datos Turso Cloud SQLite dedicada (9 GB / +2.000.000 registros)**.<br/>• Cobertura multi-proyecto y loteos ilimitados.<br/>• Importador Universal de Cartera (CSV/XML/JSON).<br/>• IA entrenada con data propia de la empresa y catálogo dinámico.<br/>• Integración con CRM (HubSpot, Salesforce, Tokko).", table_cell_style)
        ]
    ]

    t_modalities = Table(modalities_data, colWidths=[150, 140, 262])
    t_modalities.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_modalities)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Detalle del Servicio de Setup Inicial & Puesta en Marcha ($490.000 CLP):</b>", h2_style))
    story.append(Paragraph("• <b>Configuración del Servidor Autónomo:</b> Creación de la instancia en Render.com del cliente, asignación del subdominio corporativo (`camila.sucorredora.cl`) con certificado SSL HTTPS y vinculación de UptimeRobot para keep-alive 24/7.", bullet_style))
    story.append(Paragraph("• <b>Entrenamiento del Prompt y Carga de Cartera:</b> Carga masiva de la cartera de parcelas y proyectos en la base de datos SQL e integración de las reglas de negocio en la IA.", bullet_style))
    story.append(Paragraph("• <b>Verificación de Notificaciones & Prueba Incógnito:</b> Configuración del Telegram Bot / WhatsApp Business y prueba de carga en vivo antes de la entrega final.", bullet_style))

    story.append(PageBreak()) # PÁGINA 6 COMPLETA

    # =============================================================
    # PÁGINA 6: PLANES DE INVERSIÓN CORPORATIVA & CIERRE COMERCIAL
    # =============================================================
    story.append(Paragraph("8. ESTRUCTURA DE INVERSIÓN COMERCIAL ENTERPRISE EN CHILE ($ CLP)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_ACCENT, spaceAfter=5))

    p_pricing_intro = ("Considerando el valor real de mercado internacional ($30.000 USD/año en plataformas como Conversica o Qualified) "
                       "y la potencia de la Inteligencia Artificial Generativa 70B incorporada, la estructura de inversión corporativa 100% Pago Único se establece en:")
    story.append(Paragraph(p_pricing_intro, body_style))

    planes_data = [
        [Paragraph("Paquete Comercial Enterprise", table_header_style), Paragraph("Inversión (Pago Único)", table_header_style), Paragraph("Incluye & Alcance Corporativo", table_header_style)],
        [
            Paragraph("<b>PLAN CORREDORA PRO</b><br/><i>Para corredoras de propiedades de la zona</i>", table_cell_style),
            Paragraph("<b>$590.000 CLP</b><br/>(Pago Único por única vez)<br/><i>(~$630 USD Pago Único)</i>", table_cell_style),
            Paragraph("• ChatBot IA 24/7 en sitio web (1 dominio).<br/>• Alertas a Telegram y/o WhatsApp Business.<br/>• Plataforma Autónoma 100% Editable con micrófono de voz y CRM.<br/>• Atribución de Ventas e impresor de informes ROI.<br/>• Licencia perpetua 'Llave en Mano'.", table_cell_style)
        ],
        [
            Paragraph("<b>PLAN INMOBILIARIA MULTI-PROYECTO ENTERPRISE</b><br/><i>(Incluye Capacidades Enterprise)</i>", table_cell_style),
            Paragraph("<b>$1.290.000 CLP</b><br/>(Pago Único por única vez)<br/><i>(~$1.380 USD Pago Único)</i>", table_cell_style),
            Paragraph("• **Todo lo del Plan Pro + Servidor Dedicado Autónomo en Render.com**.<br/>• **Base de Datos Turso Cloud SQLite dedicada (9 GB / +2.000.000 registros)**.<br/>• Cobertura multi-proyecto y loteos ilimitados.<br/>• Importador Universal de Cartera (CSV/XML/JSON).<br/>• IA Entrenada con data propia de la empresa y catálogo dinámico.<br/>• Integración con CRM (HubSpot, Salesforce, Tokko).", table_cell_style)
        ],
        [
            Paragraph("<b>SETUP INICIAL & PUESTA EN MARCHA</b><br/><i>Pago único por única vez</i>", table_cell_style),
            Paragraph("<b>$490.000 CLP</b><br/>(Pago Único por única vez)", table_cell_style),
            Paragraph("• Configuración de servidor autónomo en Render.com.<br/>• Entrenamiento del prompt con la cartera de propiedades del cliente.<br/>• Prueba de carga y verificación de notificaciones.", table_cell_style)
        ]
    ]

    t_planes = Table(planes_data, colWidths=[150, 130, 272])
    t_planes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_planes)
    story.append(Spacer(1, 8))

    # JUSTIFICACIÓN FINANCIERA DE ALTO IMPACTO
    story.append(Paragraph("<b>Justificación Financiera e Insuperable Retorno de Inversión (ROI):</b>", h2_style))
    story.append(Paragraph("1. <b>Comparativa contra Personal Humano:</b> Contratar ejecutivos humanos para cubrir turnos nocturnos y fines de semana cuesta más de <b>$1.200.000 CLP mensuales</b> por turno (más leyes sociales e imposiciones). Camila cuesta un solo pago, trabaja los 365 días del año, jamás pide licencias y atiende a 100 clientes en paralelo.", bullet_style))
    story.append(Paragraph("2. <b>Retorno de Inversión Inmediato:</b> Con <b>UNA SOLA parcela o departamento vendido al año</b> rescatado un domingo a las 11 PM, la corredora recupera el costo total de la inversión de por vida. Todo lo demás es utilidad neta para la empresa.", bullet_style))

    story.append(Spacer(1, 10))

    # FOOTER CLOSING
    footer_data = [[
        Paragraph("<b>¿Listo para dotar a tu inmobiliaria con la mejor tecnología de IA del mercado mundial?</b><br/>"
                  "Contáctanos hoy para activar tu Licencia Perpetua de Secretaría Camila™ v5.5 Enterprise.", ParagraphStyle('FText5', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, textColor=colors.white, alignment=1))
    ]]
    t_footer = Table(footer_data, colWidths=[552])
    t_footer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_footer)

    doc.build(story)
    print(f"Dossier Maestro v5.5 Enterprise (Pago Único $1.290.000) PDF generado exitosamente en: {filename}")

if __name__ == '__main__':
    out_dir = r"c:\Users\LyCoNs\Desktop\Secretaria Camila+CHATBOTAI"
    pdf_path = os.path.join(out_dir, "DOSSIER_EJECUTIVO_SECRETARIA_CAMILA_V5.5_ENTERPRISE.pdf")
    build_pdf(pdf_path)
