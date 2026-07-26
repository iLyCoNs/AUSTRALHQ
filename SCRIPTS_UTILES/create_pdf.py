import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Portada: Dibujar fondo elegante
            self.saveState()
            self.setFillColor(colors.HexColor("#0F172A")) # Navy muy oscuro
            self.rect(0, 0, 8.5 * inch, 11 * inch, fill=True, stroke=False)
            
            # Franja decorativa lateral
            self.setFillColor(colors.HexColor("#0D9488")) # Teal vibrante
            self.rect(0, 0, 0.4 * inch, 11 * inch, fill=True, stroke=False)
            
            self.setFillColor(colors.HexColor("#D97706")) # Dorado accent
            self.rect(0.4 * inch, 0, 0.1 * inch, 11 * inch, fill=True, stroke=False)
            self.restoreState()
            return

        self.saveState()
        # Encabezado
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 11 * inch - 36, "MANUAL DE NEGOCIO: AGENCIA IA INMOBILIARIA (PUERTO MONTT & LOS LAGOS)")
        
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Pie de página
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 32, "Confidencial - Basado en agency-agents (msitarzewski)")
        
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()


def build_pdf(filename="Guia_Maestra_Agencia_IA_Puerto_Montt.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Personalización de Estilos
    c_primary = colors.HexColor("#0F172A") # Dark Navy
    c_secondary = colors.HexColor("#0D9488") # Teal Accent
    c_gold = colors.HexColor("#D97706") # Gold
    c_dark = colors.HexColor("#1E293B")
    c_bg_light = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.white,
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=19,
        textColor=colors.HexColor("#94A3B8"),
        spaceAfter=30
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=c_dark,
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=body_style,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#0F766E")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11.5,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark
    )

    dialogue_ia = ParagraphStyle(
        'DialogueIA',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0D9488")
    )

    dialogue_user = ParagraphStyle(
        'DialogueUser',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#334155")
    )

    story = []

    # -------------------------------------------------------------------------
    # PORTADA
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("PLAN DE NEGOCIOS Y MANUAL OPERATIVO COMPLETO", ParagraphStyle('CoverPre', fontName='Helvetica-Bold', fontSize=12, leading=14, textColor=c_gold, spaceAfter=10)))
    story.append(Paragraph("AGENCIA DE MARKETING E INMOBILIARIA IMPULSADA POR IA", title_style))
    story.append(Paragraph("Estrategia de Alto Rendimiento Financiero para Puerto Montt, Puerto Varas y la Región de Los Lagos", subtitle_style))
    story.append(Spacer(1, 1.2 * inch))
    
    meta_box = [
        [Paragraph("<b>Basado en la arquitectura:</b> msitarzewski/agency-agents", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#CBD5E1")))],
        [Paragraph("<b>Enfoque Geográfico:</b> Puerto Montt, Puerto Varas, Frutillar, Llanquihue, Chiloé", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#CBD5E1")))],
        [Paragraph("<b>Modelo de Monetización:</b> Retainers B2B + Comisiones por Venta de Parcelas", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#CBD5E1")))],
        [Paragraph("<b>Objetivo Financiero:</b> > $5.000.000 CLP / mes recurrentes", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#D97706")))],
    ]
    t_meta = Table(meta_box, colWidths=[6.5 * inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1E293B")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINELEFT', (0,0), (0,-1), 4, c_gold),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 1: RESUMEN EJECUTIVO Y DIAGNÓSTICO LOCAL
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Resumen Ejecutivo y Diagnóstico Local", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))
    
    story.append(Paragraph(
        "La Región de Los Lagos (particularmente la cuenca del Lago Llanquihue y el eje Puerto Montt - Puerto Varas) vive una transformación demográfica y económica sin precedentes. El flujo constante de profesionales y familias de ingresos altos provenientes de Santiago, Concepción y otras regiones busca asentarse o invertir en parcelas de agrado (5.000 m²).",
        body_style
    ))
    
    story.append(Paragraph(
        "A pesar de esta demanda masiva, la mayoría de los desarrolladores inmobiliarios y corredores locales operan bajo métodos de comercialización tradicionales y lentos (carteles en la ruta, publicaciones estáticas en portales saturados o atención manual deficiente).",
        body_style
    ))

    # Box de Oportunidad
    callout_data = [[
        Paragraph("<b>LA OPORTUNIDAD CLAVE:</b> Unir la suite de inteligencia artificial de <i>agency-agents</i> con el mercado de parcelaciones y bienes raíces del sur. Esto permite crear una agencia capaz de generar decenas de compradores calificados por semana, cerrando ventas en la mitad del tiempo sin necesidad de comprar terrenos ni arriesgar capital propio.", callout_style)
    ]]
    t_callout = Table(callout_data, colWidths=[6.8 * inch])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BBF7D0")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('LINELEFT', (0,0), (0,0), 4, c_secondary)
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 8))

    story.append(Paragraph("¿Por qué fallan las agencias tradicionales en Puerto Montt?", h2_style))
    story.append(Paragraph("<b>1. Falta de velocidad:</b> Un prospecto que consulta por una parcela en Instagram quiere respuesta en minutos. Si le responden al día siguiente, ya cotizó con 3 loteos más.", bullet_style))
    story.append(Paragraph("<b>2. Campañas genéricas:</b> Usan anuncios aburridos que no transmiten la emoción de vivir en el sur (naturaleza, calidad de vida, seguridad y reserva de agua).", bullet_style))
    story.append(Paragraph("<b>3. Sin filtro de cualificación:</b> Los vendedores pierden horas en llamadas con personas que no tienen el presupuesto ni la capacidad de crédito.", bullet_style))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CAPÍTULO 2: DE DÓNDE SALE EL INVENTARIO (TERRENOS Y CASAS)
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Estrategia de Captación de Inventario", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Una duda común al iniciar es: <i>'¿De dónde saco las casas o parcelas si yo no tengo terrenos?'</i>. La respuesta es clara: <b>Tú no compras la tierra</b>. Te alías con los desarrolladores e inmobiliarias que ya poseen los predios pero carecen de una maquinaria moderna de captación de clientes.",
        body_style
    ))

    story.append(Paragraph("Las 3 Fuentes Principales de Inventario en la X Región:", h2_style))

    inv_table_data = [
        [Paragraph("Fuente de Inventario", table_header_style), Paragraph("Perfil del Propietario", table_header_style), Paragraph("Modelo de Acuerdo Recomendado", table_header_style)],
        [
            Paragraph("<b>Inmobiliarias de Loteos</b>", table_cell_style),
            Paragraph("Desarrolladores con predios de 20 a 100 parcelas (5.000 m²) en Llanquihue, Frutillar, Chiloé.", table_cell_style),
            Paragraph("<b>Retainer Mensual ($1.5M CLP) + Comisión de 2% a 3%</b> por parcela vendida.", table_cell_style)
        ],
        [
            Paragraph("<b>Dueños Directos / Particulares</b>", table_cell_style),
            Paragraph("Agricultores, herederos o inversionistas locales con campos o hijuelas para subdividir o vender.", table_cell_style),
            Paragraph("<b>Corretaje exclusivo con IA:</b> 3% de comisión total de venta sin cobro inicial.", table_cell_style)
        ],
        [
            Paragraph("<b>Corredoras Tradicionales</b>", table_cell_style),
            Paragraph("Corredores locales con gran cartera pero sin habilidades de marketing digital.", table_cell_style),
            Paragraph("<b>Alianza 50/50:</b> Se comparte la comisión de corretaje por cada cliente aportado por tu IA.", table_cell_style)
        ]
    ]

    t_inv = Table(inv_table_data, colWidths=[1.9 * inch, 2.4 * inch, 2.5 * inch])
    t_inv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_inv)
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 3: ARQUITECTURA DE AGENTES IA (msitarzewski/agency-agents)
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Arquitectura del Escuadrón de IA", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Utilizaremos la suite de código abierto <code>msitarzewski/agency-agents</code>. Esta librería provee perfiles altamente especializados con instrucciones operativas rigurosas. Para nuestro modelo inmobiliario, desplegamos un escuadrón compuesto por 5 agentes clave:",
        body_style
    ))

    agents_data = [
        [Paragraph("Agente IA", table_header_style), Paragraph("División Repo", table_header_style), Paragraph("Rol Específico en la Agencia Inmobiliaria", table_header_style)],
        [
            Paragraph("<b>Growth Hacker</b>", table_cell_style),
            Paragraph("Marketing", table_cell_style),
            Paragraph("Diseña la oferta irresistible, define el Buyer Persona y establece el mapa de conversión del embudo.", table_cell_style)
        ],
        [
            Paragraph("<b>Paid Social Strategist</b>", table_cell_style),
            Paragraph("Paid Media", table_cell_style),
            Paragraph("Crea y optimiza las campañas en Meta Ads (IG/FB) hipersegmentadas a Santiago y zonas clave.", table_cell_style)
        ],
        [
            Paragraph("<b>PPC Campaign Strategist</b>", table_cell_style),
            Paragraph("Paid Media", table_cell_style),
            Paragraph("Captura intenciones de compra directa en Google Ads ('comprar parcela puerto varas rol propio').", table_cell_style)
        ],
        [
            Paragraph("<b>Outbound Strategist</b>", table_cell_style),
            Paragraph("Sales", table_cell_style),
            Paragraph("Prospecta inmobiliarias locales para captar inventario y gestiona los diálogos iniciales de WhatsApp.", table_cell_style)
        ],
        [
            Paragraph("<b>Proposal Strategist</b>", table_cell_style),
            Paragraph("Sales", table_cell_style),
            Paragraph("Genera automáticamente la Ficha Técnica y Dossier de Inversión en PDF personalizado para el comprador.", table_cell_style)
        ]
    ]

    t_agents = Table(agents_data, colWidths=[1.8 * inch, 1.3 * inch, 3.7 * inch])
    t_agents.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_agents)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CAPÍTULO 4: EL PASO A PASO DIDÁCTICO DEL EMBUDO AUTOMATIZADO
    # -------------------------------------------------------------------------
    story.append(Paragraph("4. El Paso a Paso Operativo del Embudo", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("A continuación se detalla la secuencia exacta que recorre un prospecto desde que ve el anuncio hasta que compra la parcela:", body_style))

    steps_detail = [
        ("PASO 1: Captura de Atención (Anuncios Hiperlocalizados)", [
            "El agente <b>Paid Social Strategist</b> redacta anuncios emocionales centrados en la calidad de vida y reserva de valor.",
            "Se configuran campañas en Instagram/Facebook segmentadas en comunas de altos ingresos de Santiago (Las Condes, Vitacura, Lo Barnechea, Providencia) y Concepción.",
            "Los anuncios utilizan tomas aéreas con dron mostrando bosques, volcanes y acceso a agua/caminos."
        ]),
        ("PASO 2: Redirección a Formulario / Landing Page Ligera", [
            "El cliente hace clic en el anuncio y es redirigido a una página de captura de carga ultra rápida.",
            "El formulario solicita solo 3 datos clave: Nombre, Teléfono/WhatsApp y Plazo estimado de compra (Ej: <i>'Busco comprar en los próximos 1-3 meses'</i>)."
        ]),
        ("PASO 3: Activación del Bot de WhatsApp en el Segundo 1", [
            "En el instante en que se envía el formulario, la API de WhatsApp (gestionada por el bot configurado según el perfil <b>Outbound Strategist</b>) inicia la conversación.",
            "El bot saluda de forma humana, entrega el catálogo de precios y realiza 2 preguntas filtro."
        ]),
        ("PASO 4: Cualificación Automática y Filtro de Curiosos", [
            "La IA analiza las respuestas: Si el cliente cuenta con presupuesto/crédito y busca comprar pronto, es etiquetado como <b>LEAD CALIENTE</b>.",
            "Si no califica, la IA le envía información general y lo ingresa a una secuencia de correo sutil de largo plazo."
        ]),
        ("PASO 5: Agendamiento Directo de Visita a Terreno", [
            "El agente IA ofrece horarios disponibles en la agenda del vendedor de la inmobiliaria en Puerto Varas o Puerto Montt.",
            "Sincroniza la cita con Google Calendar / Calendly y envía una confirmación con la ubicación exacta en Google Maps."
        ]),
        ("PASO 6: Nutrición Pre-Visita y Envío de Dossier Personalizado", [
            "24 horas antes de la visita, el agente <b>Proposal Strategist</b> genera y envía un PDF con el plano del lote reservado a nombre del cliente.",
            "Envía un recordatorio por WhatsApp: <i>'¡Hola Juan! Te esperamos mañana a las 11:30 hrs en el Proyecto Altos de Llanquihue. El clima estará despejado con vista al volcán.'</i>"
        ])
    ]

    for title, points in steps_detail:
        story.append(Paragraph(title, h2_style))
        for p in points:
            story.append(Paragraph(f"• {p}", bullet_style))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 5: GUIÓN COMPLETO DE CONVERSACIÓN DE LA IA
    # -------------------------------------------------------------------------
    story.append(Paragraph("5. Guión Real de Conversación por WhatsApp (IA)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Para comprender el nivel de sofisticación del bot, a continuación se muestra una transcripción didáctica de una conversación real cualificando a un comprador para un proyecto en Puerto Varas:",
        body_style
    ))

    chat_data = [
        [Paragraph("Emisor", table_header_style), Paragraph("Mensaje de la Conversación", table_header_style)],
        [
            Paragraph("🤖 Bot IA", dialogue_ia),
            Paragraph("¡Hola Felipe! Gracias por consultar por las parcelas en <b>Bosques de Llanquihue</b>. 🌲<br/>Soy Camila, asesora virtual del proyecto. Te acabo de adjuntar el mapa general. Para enviarte la lista de precios exacta: ¿Buscas una parcela para construir tu casa pronto o principalmente como inversión?", dialogue_user)
        ],
        [
            Paragraph("👤 Cliente", ParagraphStyle('UserHead', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#1E293B"))),
            Paragraph("Hola Camila. Busco para construir en unos 6 meses más con mi familia.", dialogue_user)
        ],
        [
            Paragraph("🤖 Bot IA", dialogue_ia),
            Paragraph("¡Excelente proyecto familiar! Las parcelas de la Etapa 1 ya cuentan con <b>Rol Propio individual y factibilidad real de agua y luz</b>, listas para escriturar.<br/>Dado que buscan construir pronto: ¿Tienen preferencia por parcelas con bosque nativo o con vista despejada a los volcanes?", dialogue_user)
        ],
        [
            Paragraph("👤 Cliente", ParagraphStyle('UserHead', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#1E293B"))),
            Paragraph("Prefiero con vista al volcán si es posible. ¿Qué valores tienen?", dialogue_user)
        ],
        [
            Paragraph("🤖 Bot IA", dialogue_ia),
            Paragraph("Las parcelas con vista al volcán Osorno van desde los <b>$34.900.000 CLP</b> (5.000 m²). Puedes reservar la tuya con $500.000.<br/>Para coordinar que nuestro ejecutivo en terreno te muestre los lotes disponibles este fin de semana: ¿Te acomoda mejor el sábado en la mañana o el domingo por la tarde?", dialogue_user)
        ],
        [
            Paragraph("👤 Cliente", ParagraphStyle('UserHead', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor("#1E293B"))),
            Paragraph("El sábado a las 11:30 me acomoda perfecto.", dialogue_user)
        ],
        [
            Paragraph("🤖 Bot IA", dialogue_ia),
            Paragraph("¡Quedó agendado! 🎉 Te acabo de enviar la ubicación exacta en Google Maps y la Ficha Técnica en PDF. Nuestro ejecutivo Pedro te estará esperando en el acceso principal. ¡Que tengas un excelente día!", dialogue_user)
        ]
    ]

    t_chat = Table(chat_data, colWidths=[1.2 * inch, 5.6 * inch])
    t_chat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_chat)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CAPÍTULO 6: PROYECCIÓN FINANCIERA Y CORRIDA DE INGRESOS
    # -------------------------------------------------------------------------
    story.append(Paragraph("6. Modelo Económico y Proyección Financiera", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "El modelo se sostiene sobre dos pilares de ingresos: <b>Fee de Administración (Retainer)</b> cobrado a la inmobiliaria para mantener el sistema publicitario activo, y <b>Comisiones por Cierre</b> de parcelas.",
        body_style
    ))

    fin_data = [
        [Paragraph("Concepto Financiero", table_header_style), Paragraph("Escenario Conservador", table_header_style), Paragraph("Escenario Moderado", table_header_style), Paragraph("Escenario Escalado", table_header_style)],
        [
            Paragraph("<b>Inmobiliarias / Clientes Activos</b>", table_cell_style),
            Paragraph("1 Proyecto (Loteo)", table_cell_style),
            Paragraph("2 Proyectos", table_cell_style),
            Paragraph("4 Proyectos", table_cell_style)
        ],
        [
            Paragraph("<b>Retainers Fijos Mensuales</b>", table_cell_style),
            Paragraph("$1.500.000 CLP", table_cell_style),
            Paragraph("$3.000.000 CLP", table_cell_style),
            Paragraph("$6.000.000 CLP", table_cell_style)
        ],
        [
            Paragraph("<b>Ventas de Parcelas por Mes</b>", table_cell_style),
            Paragraph("2 parcelas / mes", table_cell_style),
            Paragraph("5 parcelas / mes", table_cell_style),
            Paragraph("12 parcelas / mes", table_cell_style)
        ],
        [
            Paragraph("<b>Comisión Promedio (3%)</b>", table_cell_style),
            Paragraph("$2.100.000 CLP", table_cell_style),
            Paragraph("$5.250.000 CLP", table_cell_style),
            Paragraph("$12.600.000 CLP", table_cell_style)
        ],
        [
            Paragraph("<b>INGRESO TOTAL MENSUAL</b>", ParagraphStyle('TotStyle', parent=table_cell_style, fontName='Helvetica-Bold', textColor=c_primary)),
            Paragraph("<b>$3.600.000 CLP</b>", ParagraphStyle('Tot1', parent=table_cell_style, fontName='Helvetica-Bold', textColor=c_secondary)),
            Paragraph("<b>$8.250.000 CLP</b>", ParagraphStyle('Tot2', parent=table_cell_style, fontName='Helvetica-Bold', textColor=c_secondary)),
            Paragraph("<b>$18.600.000 CLP</b>", ParagraphStyle('Tot3', parent=table_cell_style, fontName='Helvetica-Bold', textColor=c_gold))
        ]
    ]

    t_fin = Table(fin_data, colWidths=[2.1 * inch, 1.5 * inch, 1.5 * inch, 1.7 * inch])
    t_fin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, c_bg_light]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#FEF3C7")),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_fin)
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 7: HOJA DE RUTA SEMANAL Y PLAN DE ACCIÓN (90 DÍAS)
    # -------------------------------------------------------------------------
    story.append(Paragraph("7. Hoja de Ruta e Implementación (Primeros 90 Días)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("Para poner en marcha esta agencia y lograr la primera facturación en 30 días, se debe seguir este plan estructurado semana a semana:", body_style))

    roadmap_items = [
        ("SEMANA 1: Configuración de Entorno e Inteligencia", [
            "Clonar el repositorio <code>msitarzewski/agency-agents</code> en tu sistema.",
            "Configurar las herramientas de ejecución (Cursor / Claude Code / Make.com).",
            "Mapear los 15 principales proyectos de parcelaciones en Puerto Varas, Puerto Montt, Frutillar y Chiloé."
        ]),
        ("SEMANA 2: Prospección B2B y Primer Cliente", [
            "Lanzar el agente <b>Outbound Strategist</b> para enviar secuencias de contacto a dueños y gerentes comerciales de inmobiliarias locales.",
            "Agendar 3 a 5 reuniones de presentación en Puerto Montt / Puerto Varas.",
            "Cerrar el primer acuerdo comercial con contrato de Retainer + Comisión."
        ]),
        ("SEMANA 3: Despliegue de Campañas y Bot de WhatsApp", [
            "Utilizar al agente <b>Paid Social Strategist</b> para crear 10 variaciones de anuncios para Instagram/Facebook.",
            "Montar el embudo en Make.com integrando la API de WhatsApp Business con el perfil de cualificación del agente.",
            "Activar las campañas publicitarias con presupuesto de prueba."
        ]),
        ("SEMANA 4: Primeras Visitas y Cierre de Ventas", [
            "El bot empieza a entregar prospectos cualificados y a agendar citas de fin de semana.",
            "El equipo en terreno realiza las muestras de parcelas.",
            "Cobro del primer retainer y primeras promesas de compraventa firmadas."
        ]),
        ("MES 2 Y 3: Escalamiento y Adquisición del Segundo Cliente", [
            "Optimizar los costos por lead con el agente <b>PPC Strategist</b>.",
            "Presentar casos de éxito a un segundo y tercer desarrollador de la zona.",
            "Escalar la facturación sobre los $8.000.000 CLP mensuales."
        ])
    ]

    for title, points in roadmap_items:
        story.append(Paragraph(title, h2_style))
        for p in points:
            story.append(Paragraph(f"• {p}", bullet_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))

    # Conclusión final box
    final_box = [
        [Paragraph("<b>CONCLUSIÓN OPERATIVA:</b> La clave del éxito de este modelo radica en la ejecución disciplinada de los Agentes de IA. Tú no necesitas ser un experto en programación ni tener millones para comprar tierras; tu valor radica en operar el sistema de captación más rápido y eficiente de la Región de Los Lagos.", ParagraphStyle('FinalText', fontName='Helvetica', fontSize=9, leading=13.5, textColor=c_primary))]
    ]
    t_final = Table(final_box, colWidths=[6.8 * inch])
    t_final.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, c_gold),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_final)

    # Construir PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente: {filename}")

if __name__ == "__main__":
    build_pdf()
