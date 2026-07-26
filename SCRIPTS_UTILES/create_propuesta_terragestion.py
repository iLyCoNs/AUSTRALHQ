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

class ProposalCanvas(canvas.Canvas):
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
            # Portada Comercial Elegante
            self.saveState()
            # Fondo azul noche premium
            self.setFillColor(colors.HexColor("#0F172A")) 
            self.rect(0, 0, 8.5 * inch, 11 * inch, fill=True, stroke=False)
            
            # Franja lateral cobre/naranja tecnológico
            self.setFillColor(colors.HexColor("#EA580C")) 
            self.rect(0, 0, 0.45 * inch, 11 * inch, fill=True, stroke=False)
            
            self.setFillColor(colors.HexColor("#D97706")) 
            self.rect(0.45 * inch, 0, 0.08 * inch, 11 * inch, fill=True, stroke=False)
            self.restoreState()
            return

        self.saveState()
        # Encabezado Comercial
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 11 * inch - 36, "PROPUESTA DE MARKETING - AGENTES IA - TERRAGESTION.CL")
        
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Pie de página
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 32, "AustralDrone.CL | Confidencial - Presentado a Terragestion.cl")
        
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()


def build_pdf(filename="Propuesta_Comercial_Terragestion_AustralDrone.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Paleta de colores ejecutiva
    c_primary = colors.HexColor("#0F172A")    # Dark Slate / Navy
    c_accent = colors.HexColor("#EA580C")     # Cobre / Naranja Tecnología
    c_gold = colors.HexColor("#D97706")       # Warm Gold
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
        textColor=c_accent,
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
        textColor=colors.HexColor("#9A3412")
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
    # PORTADA COMERCIAL CON LOGO Y TÍTULO SOLICITADO
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 0.4 * inch))
    
    # Agregar Logo oficial de Austral Drone si existe el archivo
    if os.path.exists(LOGO_PATH):
        img_logo = Image(LOGO_PATH, width=4.2 * inch, height=2.37 * inch)
        img_logo.hAlign = 'LEFT'
        story.append(img_logo)
        story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("PRESENTACIÓN EJECUTIVA EXCLUSIVA", ParagraphStyle('CoverPre', fontName='Helvetica-Bold', fontSize=11, leading=13, textColor=c_gold, spaceAfter=8)))
    story.append(Paragraph("Propuesta de Marketing - Agentes IA - Terragestion.cl", title_style))
    story.append(Paragraph("Sistema Inteligente de Captación y Aceleración de Ventas Inmobiliarias<br/>Región de Los Lagos, Chile", subtitle_style))
    story.append(Spacer(1, 0.4 * inch))
    
    meta_box = [
        [Paragraph("<b>Cliente Destinatario:</b> Inmobiliaria Terragestion (Terragestion.cl)", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#CBD5E1")))],
        [Paragraph("<b>Empresa Emisora:</b> AustralDrone.CL - Departamento de IA Marketing", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#CBD5E1")))],
        [Paragraph("<b>Modelo de Acuerdo:</b> Programa Piloto Experimental a Resultado (% por Venta)", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#EA580C")))],
        [Paragraph("<b>Objetivo Comercial:</b> Duplicar la velocidad de colocación de parcelas sin costo fijo inicial", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=colors.HexColor("#D97706")))],
    ]
    t_meta = Table(meta_box, colWidths=[6.5 * inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1E293B")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINELEFT', (0,0), (0,-1), 4, c_accent),
    ]))
    story.append(t_meta)
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 1: LA NUEVA ERA COMERCIAL
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. La Nueva Era Comercial en la Región de Los Lagos", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=10))
    
    story.append(Paragraph(
        "Estimado equipo directivo de <b>Terragestion.cl</b>:",
        body_style
    ))

    story.append(Paragraph(
        "El mercado inmobiliario y de parcelaciones en el sur de Chile ha cambiado radicalmente. La demanda por parcelas de agrado y terrenos en la cuenca del Lago Llanquihue y sus alrededores por parte de compradores de la Región Metropolitana, Concepción y el resto del país está en su punto más alto.",
        body_style
    ))
    
    story.append(Paragraph(
        "Sin embargo, el método tradicional de venta (publicar en portales saturados, esperar llamadas o colocar carteles en la carretera) ya no es suficiente. El comprador moderno exige **atención inmediata, experiencias visuales inmersivas y un acompañamiento continuo desde el primer segundo**.",
        body_style
    ))

    # Callout de la propuesta
    callout_data = [[
        Paragraph("<b>NUESTRA PROPUESTA EN SIMPLE:</b> En <b>AustralDrone.CL</b> combinamos nuestra capacidad audiovisual aérea de alta precisión con un <b>Sistema Automatizado de Marketing Inteligente de Última Generación</b>. Nos encargamos de atraer, filtrar y agendar a compradores reales listos para escriturar, para que el equipo comercial de Terragestion.cl se enfoque únicamente en mostrar las parcelas y cerrar los contratos.", callout_style)
    ]]
    t_callout = Table(callout_data, colWidths=[6.8 * inch])
    t_callout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFF7ED")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FFEDD5")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('LINELEFT', (0,0), (0,0), 4, c_accent)
    ]))
    story.append(t_callout)
    story.append(Spacer(1, 10))

    story.append(Paragraph("¿Por qué esta estrategia supera a la publicidad tradicional?", h2_style))
    story.append(Paragraph("<b>1. Captura la emoción del lugar:</b> Utilizamos material aéreo y terrestre de altísima calidad que transmite la verdadera experiencia de vivir en el sur.", bullet_style))
    story.append(Paragraph("<b>2. Respuesta instantánea (Segundo 0):</b> El 80% de las ventas inmobiliarias se pierden por responder tarde. Nuestro sistema atiende las 24 horas del día, los 7 días de la semana.", bullet_style))
    story.append(Paragraph("<b>3. Filtro inteligente de compradores:</b> Descartamos automáticamente a los curiosos y solo enviamos al equipo de Terragestion.cl a clientes con presupuesto verificado.", bullet_style))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CAPÍTULO 2: LA OFERTA EXPERIMENTAL (ALIANZA A RESULTADO)
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Alianza Estratégica: Modelo Piloto a Resultado", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Sabemos que probar un sistema innovador requiere confianza. Por esta razón, en <b>AustralDrone.CL</b> no queremos presentarles una tarifa publicitaria tradicional ni costos fijos elevados.",
        body_style
    ))

    story.append(Paragraph(
        "Les proponemos ingresar a un **Programa Piloto Experimental a Resultado**, donde compartimos el riesgo comercial y basamos nuestro éxito únicamente en el crecimiento real de las ventas de Terragestion.cl.",
        body_style
    ))

    piloto_table_data = [
        [Paragraph("Pilar de la Alianza", table_header_style), Paragraph("¿En qué consiste para Terragestion.cl?", table_header_style), Paragraph("Beneficio para la Inmobiliaria", table_header_style)],
        [
            Paragraph("<b>Riesgo Financiero Cero</b>", table_cell_style),
            Paragraph("AustralDrone.CL despliega toda la tecnología de captación, creativos y automatización sin costo de desarrollo inicial.", table_cell_style),
            Paragraph("Terragestion no arriesga capital en asesorías ni en implementación de software.", table_cell_style)
        ],
        [
            Paragraph("<b>Pago por Éxito Comercial (% por Venta)</b>", table_cell_style),
            Paragraph("Acordamos una <b>comisión razonable por cada parcela vendida</b> directamente a través de nuestro sistema.", table_cell_style),
            Paragraph("Solo pagas cuando el cliente firma la promesa o escrituración de la parcela.", table_cell_style)
        ],
        [
            Paragraph("<b>Cualificación Total</b>", table_cell_style),
            Paragraph("Entregamos prospectos pre-evaluados con día y hora agendada para visitar los loteos.", table_cell_style),
            Paragraph("El equipo de ventas de Terragestion ahorra cientos de horas en llamadas inútiles.", table_cell_style)
        ]
    ]

    t_piloto = Table(piloto_table_data, colWidths=[1.8 * inch, 2.5 * inch, 2.5 * inch])
    t_piloto.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_piloto)
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 3: PROYECCIÓN DE VENTAS Y ACELERACIÓN DE INVENTARIO
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Proyección de Ventas y Aceleración de Inventario", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Nuestra tecnología está diseñada para aumentar drásticamente la tasa de colocación de parcelas. A continuación presentamos una simulación conservadora del impacto comercial en un proyecto inmobiliario de Terragestion.cl:",
        body_style
    ))

    proj_table_data = [
        [Paragraph("Métrica de Impacto", table_header_style), Paragraph("Situación Tradicional Actual", table_header_style), Paragraph("Con Sistema AustralDrone.CL", table_header_style), Paragraph("Crecimiento Estimado", table_header_style)],
        [
            Paragraph("<b>Prospectos Totales / Mes</b>", table_cell_style),
            Paragraph("30 - 50 mensajes desorganizados", table_cell_style),
            Paragraph("<b>150 - 250 leads cualificados</b>", table_cell_style),
            Paragraph("<b>+400% de alcance</b>", table_cell_style)
        ],
        [
            Paragraph("<b>Tiempo de Respuesta al Cliente</b>", table_cell_style),
            Paragraph("4 a 24 horas (Pérdida de interés)", table_cell_style),
            Paragraph("<b>Inmediato (Menos de 60 segundos)</b>", table_cell_style),
            Paragraph("<b>100% Retención</b>", table_cell_style)
        ],
        [
            Paragraph("<b>Visitas Guiadas a Terreno / Mes</b>", table_cell_style),
            Paragraph("5 a 8 visitas (Muchos no llegan)", table_cell_style),
            Paragraph("<b>20 a 35 visitas confirmadas</b>", table_cell_style),
            Paragraph("<b>+300% en terreno</b>", table_cell_style)
        ],
        [
            Paragraph("<b>Venta Mensual de Parcelas</b>", table_cell_style),
            Paragraph("1 a 2 parcelas / mes", table_cell_style),
            Paragraph("<b>4 a 8 parcelas / mes</b>", table_cell_style),
            Paragraph("<b>x3 a x4 en Ventas</b>", table_cell_style)
        ],
        [
            Paragraph("<b>Tiempo para Agotar Loteo (40 u.)</b>", table_cell_style),
            Paragraph("20 a 24 meses", table_cell_style),
            Paragraph("<b>5 a 8 meses</b>", ParagraphStyle('HighlightP', parent=table_cell_style, fontName='Helvetica-Bold', textColor=c_accent)),
            Paragraph("<b>Ahorro de 1 año en costos</b>", table_cell_style)
        ]
    ]

    t_proj = Table(proj_table_data, colWidths=[2.0 * inch, 1.6 * inch, 1.7 * inch, 1.5 * inch])
    t_proj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_proj)
    story.append(Spacer(1, 12))

    story.append(Paragraph("¿Qué significa esta aceleración para la rentabilidad de Terragestion.cl?", h2_style))
    story.append(Paragraph("<b>• Recuperación acelerada de capital:</b> Agotar un loteo en 6 meses en lugar de 2 años permite reinvestir el capital en nuevos terrenos mucho más rápido.", bullet_style))
    story.append(Paragraph("<b>• Reducción de costos fijos operativos:</b> Menos gastos en mantención de salas de venta, personal fijo prolongado y financiamiento bancario.", bullet_style))
    story.append(Paragraph("<b>• Dominio del mercado regional:</b> Posiciona a Terragestion.cl como la inmobiliaria más innovadora y rápida de la X Región.", bullet_style))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CAPÍTULO 4: PLAN DE ESCALAMIENTO GRADUAL A 12 MESES
    # -------------------------------------------------------------------------
    story.append(Paragraph("4. Hoja de Ruta de Crecimiento Mutuo (12 Meses)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("Diseñamos una relación comercial escalonada para construir confianza paso a paso:", body_style))

    roadmap_data = [
        ("FASE 1 (Mes 1): Lanzamiento del Piloto Experimental", [
            "Seleccionamos <b>1 proyecto de parcelaciones específico</b> de Terragestion.cl para la prueba.",
            "Desplegamos la campaña de captación y el sistema inteligente de atención.",
            "Evaluación de los primeros cierres de ventas y calibración del sistema."
        ]),
        ("FASE 2 (Mes 2 - 3): Consolidación y Escalamiento", [
            "Aumentamos el flujo de compradores hacia el proyecto piloto.",
            "Logramos el ritmo constante de 4 a 6 parcelas vendidas por mes.",
            "Presentación de informes de rendimiento y retorno comercial claro."
        ]),
        ("FASE 3 (Mes 4 - 6): Expansión a Nuevos Proyectos", [
            "Incorporamos la totalidad de los loteos y desarrollos activos de Terragestion.cl al sistema.",
            "Lanzamos campañas dirigidas a inversionistas institucionales y compradores de segunda vivienda."
        ]),
        ("FASE 4 (Mes 7 - 12): Exclusividad y Dominio Regional", [
            "Consolidamos a Terragestion.cl como la fuerza inmobiliaria número 1 de la zona.",
            "Garantizamos un canal exclusivo de ventas continuas para futuros lanzamientos de la empresa."
        ])
    ]

    for title, points in roadmap_data:
        story.append(Paragraph(title, h2_style))
        for p in points:
            story.append(Paragraph(f"• {p}", bullet_style))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 5: PRÓXIMOS PASOS Y LLAMADO A LA ACCIÓN
    # -------------------------------------------------------------------------
    story.append(Paragraph("5. Próximos Pasos para Iniciar el Piloto", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Para dar inicio al Programa Piloto Experimental y comenzar a acelerar las ventas de Terragestion.cl este mismo mes, el procedimiento es simple y directo:",
        body_style
    ))

    steps_box = [
        [Paragraph("<b>PASO 1: Reunión Ejecutiva de Alineación (30 Minutos)</b><br/>Revisamos el proyecto elegido para el piloto y definimos la comisión por parcela vendida.", table_cell_style)],
        [Paragraph("<b>PASO 2: Firma de Acuerdo de Confidencialidad y Piloto a Resultado</b><br/>Formalizamos los términos donde Terragestion.cl solo paga al concretar la venta.", table_cell_style)],
        [Paragraph("<b>PASO 3: Levantar Material y Despliegue (En 5 días hábiles)</b><br/>Capturamos las tomas necesarias y activamos la máquina de ventas.", table_cell_style)],
        [Paragraph("<b>PASO 4: Recepción de Primeras Visitas Guiadas</b><br/>El equipo de ventas de Terragestion.cl empieza a recibir citas de compradores calificados.", table_cell_style)]
    ]
    t_steps = Table(steps_box, colWidths=[6.8 * inch])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('LINELEFT', (0,0), (0,-1), 4, c_accent)
    ]))
    story.append(t_steps)
    story.append(Spacer(1, 15))

    # Cuadro de Firma y Contacto
    contact_box = [
        [
            Paragraph("<b>PRESENTADO POR:</b><br/><br/><b>AustralDrone.CL</b><br/>Departamento de IA Marketing<br/>Región de Los Lagos, Chile<br/><i>contacto@australdrone.cl</i>", table_cell_style),
            Paragraph("<b>ACEPTADO POR:</b><br/><br/><b>Inmobiliaria Terragestion.cl</b><br/>Representante Legal / Gerencia Comercial<br/>Fecha: ____ / ____ / 2026<br/>Firma: ________________________", table_cell_style)
        ]
    ]
    t_contact = Table(contact_box, colWidths=[3.4 * inch, 3.4 * inch])
    t_contact.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, c_gold),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(t_contact)

    # Construir PDF
    doc.build(story, canvasmaker=ProposalCanvas)
    print(f"Propuesta comercial con Portada e Imagen generada exitosamente: {filename}")

if __name__ == "__main__":
    build_pdf()
