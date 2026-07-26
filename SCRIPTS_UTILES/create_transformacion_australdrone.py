import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas

LOGO_PATH = r"C:\Users\LyCoNs\.gemini\antigravity\brain\cb459839-1c5d-4150-94dd-57469c060e25\.user_uploaded\media__1784740615873.png"

class RoadmapCanvas(canvas.Canvas):
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
            # Portada de Transformación Estratégica
            self.saveState()
            self.setFillColor(colors.HexColor("#0F172A")) # Navy Profundo
            self.rect(0, 0, 8.5 * inch, 11 * inch, fill=True, stroke=False)
            
            self.setFillColor(colors.HexColor("#0284C7")) # Sky Blue Accent
            self.rect(0, 0, 0.45 * inch, 11 * inch, fill=True, stroke=False)
            
            self.setFillColor(colors.HexColor("#DCCBAE")) # Sand Gold Accent
            self.rect(0.45 * inch, 0, 0.08 * inch, 11 * inch, fill=True, stroke=False)
            self.restoreState()
            return

        self.saveState()
        # Encabezado
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 11 * inch - 36, "PLAN DE TRANSFORMACIÓN ESTRATÉGICA | WWW.AUSTRALDRONE.CL")
        
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Pie de página
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 32, "Documento de Estrategia Interna - AustralDrone.CL")
        
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()


def build_pdf(filename="Plan_Estrategico_Transformacion_AustralDrone.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Paleta de colores AustralDrone
    c_primary = colors.HexColor("#0F172A")    # Dark Navy
    c_blue = colors.HexColor("#0284C7")       # Sky Blue
    c_sand = colors.HexColor("#DCCBAE")       # Sand Gold
    c_dark = colors.HexColor("#1E293B")
    c_bg_light = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.white,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#94A3B8"),
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_primary,
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_blue,
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
        leftIndent=14,
        bulletIndent=4,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#0369A1")
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

    story = []

    # -------------------------------------------------------------------------
    # PORTADA OFICIAL
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 0.4 * inch))
    
    if os.path.exists(LOGO_PATH):
        img_logo = Image(LOGO_PATH, width=4.2 * inch, height=2.37 * inch)
        img_logo.hAlign = 'LEFT'
        story.append(img_logo)
        story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("PLAN DE TRANSFORMACIÓN Y EVOLUCIÓN DE MARCA", ParagraphStyle('CoverPre', fontName='Helvetica-Bold', fontSize=11, leading=13, textColor=c_sand, spaceAfter=8)))
    story.append(Paragraph("UNIFICACIÓN ESTRATÉGICA DE SERVICIOS AUDIOVISUALES E INTELIGENCIA ARTIFICIAL", title_style))
    story.append(Paragraph("Hoja de Ruta para convertir a <b>www.australdrone.cl</b> en el Motor N° 1 de Aceleración Inmobiliaria en la Región de Los Lagos", subtitle_style))
    story.append(Spacer(1, 0.4 * inch))
    
    meta_box = [
        [Paragraph("<b>Sitio Web Oficial:</b> www.australdrone.cl", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#CBD5E1")))],
        [Paragraph("<b>Nueva Categorización:</b> Agencia de Performance & IA Inmobiliaria + Audiovisual 360°", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#CBD5E1")))],
        [Paragraph("<b>Ventaja Competitiva:</b> Monopolio Regional Único (Producción Aérea + Sistema de Conversión IA)", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#38BDF8")))],
        [Paragraph("<b>Proyección Financiera:</b> Escalabilidad a contratos recurrentes + Comisiones a resultado", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#DCCBAE")))],
    ]
    t_meta = Table(meta_box, colWidths=[6.5 * inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1E293B")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINELEFT', (0,0), (0,-1), 4, c_blue),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 1: DIAGNÓSTICO Y EL NUEVO RUMBO DE AUSTRALDRONE.CL
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Diagnóstico y el Nuevo Rumbo de AustralDrone.CL", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Actualmente, <b>www.australdrone.cl</b> está posicionada de manera sobresaliente en el ámbito audiovisual (Grabación con Dron 4K/FPV, Tours Virtuales y Masterplan 360° en Puerto Montt, Puerto Varas y la X Región).",
        body_style
    ))

    story.append(Paragraph(
        "Sin embargo, el mercado inmobiliario actual enfrenta un problema más profundo: **Los desarrolladores de parcelas no necesitan simplemente 'videos bonitos', necesitan VENDER PARCELAS RÁPIDO**.",
        body_style
    ))

    callout_data = [[
        Paragraph("<b>LA GRAN OPORTUNIDAD DE MARCA:</b> Al integrar la suite de Agentes de IA en el núcleo de AustralDrone.CL, el negocio evoluciona de ser un <i>'Proveedor Audiovisual'</i> (servicio commodity por hora o proyecto) a convertirse en un <b>'Motor de Aceleración Inmobiliaria Todo en Uno'</b>. Te conviertes en el socio estratégico imprescindible de las inmobiliarias.", callout_style)
    ]]
    t_callout = Table(callout_data, colWidths=[6.8 * inch])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F9FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BAE6FD")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('LINELEFT', (0,0), (0,0), 4, c_blue)
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 10))

    story.append(Paragraph("La Ventaja Competitiva Imbatible:", h2_style))
    story.append(Paragraph("<b>• Ninguna agencia de marketing tradicional</b> en Puerto Montt/Puerto Varas posee drones FPV, Masterplan 360° interactivos ni contenido aéreo de alta resolución propio.", bullet_style))
    story.append(Paragraph("<b>• Ninguna empresa de drones</b> en la zona cuenta con un sistema de Agentes de IA capaces de responder en WhatsApp en 30 segundos, cualificar clientes e integrar CRM.", bullet_style))
    story.append(Paragraph("<b>• AustralDrone.CL unifica ambos mundos:</b> Es la única empresa en el sur de Chile que ofrece la producción visual que enamora al cliente Y la inteligencia artificial que cierra las ventas.", bullet_style))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CAPÍTULO 2: REDISEÑO ESTRUCTURAL DE LA WEB WWW.AUSTRALDRONE.CL
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Rediseño Estratégico del Sitio Web (www.australdrone.cl)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Para reflejar este nuevo rumbo sin perder el atractivo visual moderno que ya posee la web, se deben aplicar las siguientes modificaciones estructurales en la página:",
        body_style
    ))

    story.append(Paragraph("Nuevos Módulos del Menú de Navegación (Mac Dock):", h2_style))
    story.append(Paragraph("1. <b>INICIO:</b> Posicionamiento renovado.", bullet_style))
    story.append(Paragraph("2. <b>MASTERPLAN 360°:</b> Demostración del mapa aéreo interactivo (Fortaleza actual).", bullet_style))
    story.append(Paragraph("3. <b>SISTEMA IA & PERFORMANCE (NUEVO):</b> Explicación visual de cómo nuestro bot y campañas aceleran las ventas.", bullet_style))
    story.append(Paragraph("4. <b>PACKS Y TARIFAS:</b> Presentación de los 3 niveles de servicio.", bullet_style))
    story.append(Paragraph("5. <b>PORTAFOLIO Y CASOS:</b> Demostraciones reales en la 10ª Región.", bullet_style))

    story.append(Spacer(1, 8))

    story.append(Paragraph("Estructura de los 3 Nuevos Niveles de Oferta en la Web:", h2_style))

    packs_table_data = [
        [Paragraph("Nivel de Servicio", table_header_style), Paragraph("Componentes Incluidos", table_header_style), Paragraph("Modelo Comercial y Cobro", table_header_style)],
        [
            Paragraph("<b>Nivel 1: Audiovisual Pro</b>", table_cell_style),
            Paragraph("• Grabación Dron 4K / FPV<br/>• Fotografía aérea de parcelas<br/>• Edición de video promocional", table_cell_style),
            Paragraph("<b>Pago Único por Proyecto</b><br/>Servicio puntual para corredoras o loteos pequeños.", table_cell_style)
        ],
        [
            Paragraph("<b>Nivel 2: Masterplan 360° Interactivo</b>", table_cell_style),
            Paragraph("• Mapeo 360° aéreo del terreno<br/>• Tour Virtual interactivo por lote<br/>• Integración en la web del cliente", table_cell_style),
            Paragraph("<b>Pago por Proyecto + Mantención</b><br/>Para desarrolladores de parcelaciones mediano tamaño.", table_cell_style)
        ],
        [
            Paragraph("<b>Nivel 3: Pack Aceleración IA 360° (Estrella)</b>", table_cell_style),
            Paragraph("• <b>Todo lo audiovisual y Masterplan 360°</b><br/>• Campañas en Meta/Google Ads<br/>• Bot WhatsApp IA 24/7 en segundo 0<br/>• Cualificación y Agendamiento citas", table_cell_style),
            Paragraph("<b>Retainer Mensual + Comisión a Resultado (% por Parcela Vendida)</b><br/>Para inmobiliarias y loteos grandes (Ej. Terragestion.cl).", table_cell_style)
        ]
    ]

    t_packs = Table(packs_table_data, colWidths=[1.8 * inch, 2.6 * inch, 2.4 * inch])
    t_packs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_packs)
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 3: INTEGRACIÓN DE LOS AGENTES IA EN EL BACK-END DE AUSTRALDRONE
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Operativa Interna: Los Agentes de IA en AustralDrone.CL", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Detrás de pantalla, AustralDrone.CL utilizará la suite de agentes especializados de <code>msitarzewski/agency-agents</code> para operar todo el flujo sin necesidad de contratar un gran equipo humano:",
        body_style
    ))

    workflow_data = [
        [Paragraph("Etapa del Negocio", table_header_style), Paragraph("Agente IA Responsable", table_header_style), Paragraph("Tarea Automatizada Ejecutada", table_header_style)],
        [
            Paragraph("<b>1. Prospección B2B</b>", table_cell_style),
            Paragraph("<code>Outbound Strategist</code>", table_cell_style),
            Paragraph("Busca inmobiliarias y loteos activos en Los Lagos y les envía propuestas comerciales para el Pack IA Nivel 3.", table_cell_style)
        ],
        [
            Paragraph("<b>2. Atracción de Compradores</b>", table_cell_style),
            Paragraph("<code>Paid Social Strategist</code>", table_cell_style),
            Paragraph("Diseña los anuncios de Instagram/Facebook mezclando las tomas aéreas de AustralDrone con copys de alta conversión.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Atención Inmediata</b>", table_cell_style),
            Paragraph("<code>Outbound / Sales Bot</code>", table_cell_style),
            Paragraph("Responde en WhatsApp en menos de 60 segundos, entrega el Masterplan 360° y filtra compradores calificados.", table_cell_style)
        ],
        [
            Paragraph("<b>4. Preparación de Visitas</b>", table_cell_style),
            Paragraph("<code>Proposal Strategist</code>", table_cell_style),
            Paragraph("Genera automáticamente las fichas técnicas en PDF de los lotes reservados y agendra citas en el calendario.", table_cell_style)
        ],
        [
            Paragraph("<b>5. Cierre y Reputación</b>", table_cell_style),
            Paragraph("<code>Customer Success</code>", table_cell_style),
            Paragraph("Realiza seguimiento post-escrituración y recopila reseñas de 5 estrellas en Google para potenciar las ventas del siguiente loteo.", table_cell_style)
        ]
    ]

    t_wf = Table(workflow_data, colWidths=[1.6 * inch, 1.8 * inch, 3.4 * inch])
    t_wf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_wf)
    story.append(Spacer(1, 12))

    # -------------------------------------------------------------------------
    # CAPÍTULO 4: PLAN DE IMPLEMENTACIÓN A 90 DÍAS
    # -------------------------------------------------------------------------
    story.append(Paragraph("4. Plan de Implementación a 90 Días para AustralDrone.CL", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_blue, spaceBefore=2, spaceAfter=10))

    roadmap_steps = [
        ("FASE 1 (Días 1 - 30): Rediseño Web y Armado de la Suite IA", [
            "Actualizar el código de <code>www.australdrone.cl</code> incorporando el nuevo titular, la sección de Sistema IA y los 3 Niveles de Servicio.",
            "Configurar los agentes de IA en n8n conectados con Gemini Pro y la API de WhatsApp.",
            "Diseñar la presentación comercial en PDF para enviar a inmobiliarias locales."
        ]),
        ("FASE 2 (Días 31 - 60): Lanzamiento Comercial y Primeros Pilotos", [
            "Activar al agente <code>Outbound Strategist</code> para prospectar las primeras 20 inmobiliarias de la X Región.",
            "Cerrar la primera alianza comercial bajo el modelo de Piloto a Resultado (ej. Terragestion.cl).",
            "Desplegar las primeras campañas de prueba y evaluar las métricas de captación por WhatsApp."
        ]),
        ("FASE 3 (Días 61 - 90): Consolidación y Escalamiento de Facturación", [
            "Lograr los primeros cierres de parcelas y cobrar las primeras comisiones a resultado.",
            "Publicar el primer Caso de Éxito en la web <code>www.australdrone.cl</code>.",
            "Escalar el modelo para gestionar 3 a 5 loteos simultáneos en la región de Los Lagos."
        ])
    ]

    for title, points in roadmap_steps:
        story.append(Paragraph(title, h2_style))
        for p in points:
            story.append(Paragraph(f"• {p}", bullet_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))

    # Conclusión final
    final_box = [
        [Paragraph("<b>CONCLUSIÓN DEL RUMBO ESTRATÉGICO:</b> AustralDrone.CL tiene todo para dominar el mercado inmobiliario del sur de Chile. La combinación de contenido audiovisual 360° con Inteligencia Artificial automatizada crea una barrera de entrada imposible de superar para la competencia. Es el momento de ejecutar este nuevo rumbo.", ParagraphStyle('FinalT', fontName='Helvetica', fontSize=9, leading=13.5, textColor=c_primary))]
    ]
    t_final = Table(final_box, colWidths=[6.8 * inch])
    t_final.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E0F2FE")),
        ('BOX', (0,0), (-1,-1), 1, c_blue),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_final)

    # Construir PDF
    doc.build(story, canvasmaker=RoadmapCanvas)
    print(f"Plan de transformación estratégico generado exitosamente: {filename}")

if __name__ == "__main__":
    build_pdf()
