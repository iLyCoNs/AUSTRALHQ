import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36, rightMargin=36,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    COLOR_PRIMARY = colors.HexColor('#6366f1')   # Indigo / Purple accent
    COLOR_SECONDARY = colors.HexColor('#0f172a') # Dark Navy
    COLOR_ACCENT = colors.HexColor('#10b981')    # Emerald
    COLOR_TEXT = colors.HexColor('#1e293b')      # Slate 800
    COLOR_BG_LIGHT = colors.HexColor('#f8fafc')  # Light Gray
    COLOR_BORDER = colors.HexColor('#e2e8f0')

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.white
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#cbd5e1')
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=COLOR_SECONDARY,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=COLOR_PRIMARY,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=COLOR_TEXT,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=COLOR_TEXT
    )

    story = []

    # -------------------------------------------------------------
    # HEADER BANNER (COVER / TOP)
    # -------------------------------------------------------------
    header_data = [[
        Paragraph("PROPUESTA DE INTEGRACIÓN GENERAL<br/><b>SECRETARÍA CAMILA™ + CHATBOT AI</b>", title_style),
    ], [
        Paragraph("Solución de Inteligencia Conversacional 24/7 y Captura de Prospectos Inmobiliarios<br/>Especialmente diseñada para la <b>Región de Los Lagos</b> (Puerto Varas, Puerto Montt, Frutillar, Llanquihue, Osorno y Chiloé)", subtitle_style)
    ]]

    header_table = Table(header_data, colWidths=[540])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,1), (-1,1), 16),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # SECCIÓN 1: EL CONTEXTO INMOBILIARIO EN LOS LAGOS
    # -------------------------------------------------------------
    story.append(Paragraph("1. DIAGNÓSTICO DEL MERCADO INMOBILIARIO EN LA REGIÓN DE LOS LAGOS", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=8))
    
    p1 = ("La Región de Los Lagos se ha consolidado como el polo de inversión inmobiliaria y migración de segunda/primera vivienda "
          "más dinámico de Chile. Compradores provenientes de Santiago, Concepción y Antofagasta buscan parcelas de 5.000m², loteos, "
          "casas en la cuenca del Lago Llanquihue y departamentos urbanos en Puerto Montt y Osorno.")
    story.append(Paragraph(p1, body_style))

    p2 = ("Sin embargo, este perfil de comprador realiza sus búsquedas principalmente <b>fuera de su horario laboral (entre las 20:00 y las 01:00 hrs) y durante fines de semana</b>. "
          "Cuando ingresan a la web de una corredora local y encuentran un formulario estático que promete responder en '24 a 48 horas', "
          "la tasa de abandono supera el <b>70%</b>. El cliente se desplaza inmediatamente a la siguiente inmobiliaria que le entregue atención instantánea.")
    story.append(Paragraph(p2, body_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECCIÓN 2: LA SOLUCIÓN SECRETARÍA CAMILA
    # -------------------------------------------------------------
    story.append(Paragraph("2. LA SOLUCIÓN: SECRETARÍA CAMILA™ INMOBILIARIA 24/7", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=8))

    p3 = ("<b>Secretaría Camila™</b> no es un chat estático de opciones rígidas. Es un agente conversacional avanzado impulsado por "
          "<b>Inteligencia Artificial Generativa 70B</b> que atiende tu sitio web las 24 horas del día, los 365 días del año. "
          "Camila conoce el catálogo de propiedades de tu corredora, comprende las necesidades del cliente y actúa como una "
          "asesora humana experta.")
    story.append(Paragraph(p3, body_style))

    # TABLA DE HABILIDADES
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Matriz de Habilidades y Sincronización en Tiempo Real:</b>", h2_style))

    abilities_data = [
        [Paragraph("Habilidad del Agente", table_header_style), Paragraph("Funcionamiento Técnico", table_header_style), Paragraph("Impacto en Ventas de Los Lagos", table_header_style)],
        [
            Paragraph("<b>IA Generativa Llama 3.1 70B</b>", table_cell_style),
            Paragraph("Respuestas ultra-humanas en máximo 2 párrafos. Entendimiento natural de contexto.", table_cell_style),
            Paragraph("Retiene al comprador conversando fluidamente sin sonar a robot estático.", table_cell_style)
        ],
        [
            Paragraph("<b>Auto-Contexto de Propiedad</b>", table_cell_style),
            Paragraph("Detecta automáticamente la ficha, ubicación y metraje de la parcela o inmueble en vista.", table_cell_style),
            Paragraph("Responde dudas sobre accesibilidad, caminos, agua/luz y superficie en Los Lagos.", table_cell_style)
        ],
        [
            Paragraph("<b>Lead Scoring BANT (0-100)</b>", table_cell_style),
            Paragraph("Califica crédito hipotecario, pago contado, plazo de compra y presupuesto.", table_cell_style),
            Paragraph("Filtra curiosos y entrega solo prospectos con capacidad real de compra.", table_cell_style)
        ],
        [
            Paragraph("<b>Captura de Teléfono Automática</b>", table_cell_style),
            Paragraph("Detecta números de WhatsApp/teléfono y los extrae al instante.", table_cell_style),
            Paragraph("Dispara la alerta inmediata al celular del corredor antes de que el cliente abandone la web.", table_cell_style)
        ],
        [
            Paragraph("<b>Alertas Inmediatas (<3s)</b>", table_cell_style),
            Paragraph("Notificación por Telegram o WhatsApp Business al equipo comercial.", table_cell_style),
            Paragraph("Permite al corredor llamar al cliente mientras su interés en la parcela está 'caliente'.", table_cell_style)
        ],
        [
            Paragraph("<b>Widget de Agenda Interactiva</b>", table_cell_style),
            Paragraph("Despliega calendario automático cuando el cliente desea coordinar una visita.", table_cell_style),
            Paragraph("Transforma visitas web en citas presenciales en terreno o reuniones por Zoom.", table_cell_style)
        ],
        [
            Paragraph("<b>Panel de Atribución ROI Fidedigno</b>", table_cell_style),
            Paragraph("Dashboard para marcar ventas ganadas ($ CLP) y medir rescates nocturnos.", table_cell_style),
            Paragraph("Comprueba con métricas transparentes cuántas comisiones fueron impulsadas por Camila.", table_cell_style)
        ],
        [
            Paragraph("<b>Consola de Voz para el CEO 🎙️</b>", table_cell_style),
            Paragraph("Micrófono de dictado de voz para que el dueño consulte proyecciones y estado.", table_cell_style),
            Paragraph("Revisa el rendimiento comercial de la corredora sin necesidad de planillas complejas.", table_cell_style)
        ]
    ]

    t_abilities = Table(abilities_data, colWidths=[130, 200, 210])
    t_abilities.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_abilities)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # SECCIÓN 3: LA SINCRONIZACIÓN EN TIEMPO REAL
    # -------------------------------------------------------------
    story.append(Paragraph("3. LA ARQUITECTURA DE SINCRONIZACIÓN EN TIEMPO REAL", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=8))

    p4 = ("El sistema opera mediante una <b>sincronización bidireccional inmediata</b>:")
    story.append(Paragraph(p4, body_style))
    
    story.append(Paragraph("• <b>Capa Web (Visitante):</b> El cliente explora parcelas en Puerto Varas o departamentos en Puerto Montt a las 23:00 hrs. Camila dialoga, resuelve dudas del proyecto y califica su capacidad de pago.", bullet_style))
    story.append(Paragraph("• <b>Capa de Notificación Instantánea:</b> El momento en que el prospecto escribe su WhatsApp, la alerta llega en &lt;3 segundos al celular del corredor inmobiliario etiquetada con <code>🌙 FUERA DE HORARIO</code>.", bullet_style))
    story.append(Paragraph("• <b>Capa de Atribución (Plataforma Autónoma):</b> El contacto queda registrado en la Plataforma Autónoma (<code>https://camila.tudominio.cl</code>) con un botón directo a <b>WhatsApp Web</b> para iniciar la gestión comercial inmediatamente.", bullet_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECCIÓN 4: IMPACTO Y ROI EN LA REGIÓN DE LOS LAGOS
    # -------------------------------------------------------------
    story.append(Paragraph("4. PROYECCIÓN DE IMPACTO FINANCIERO Y RETORNO DE INVERSIÓN (ROI)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=8))

    p5 = ("Para una corredora o inmobiliaria promedio en la Región de Los Lagos con un flujo de <b>1.000 visitas mensuales</b>:")
    story.append(Paragraph(p5, body_style))

    roi_data = [
        [Paragraph("Métrica Comercial", table_header_style), Paragraph("Sin Secretaría Camila", table_header_style), Paragraph("Con Secretaría Camila™ 24/7", table_header_style)],
        [Paragraph("Atención fuera de horario (20:00 a 08:00 hrs)", table_cell_style), Paragraph("Sin atención (Formulario estático)", table_cell_style), Paragraph("<b>Atención inmediata en &lt;3 segundos</b>", table_cell_style)],
        [Paragraph("Captura de leads mensuales", table_cell_style), Paragraph("10 - 15 contactos lentos", table_cell_style), Paragraph("<b>35 - 50 prospectos calificados BANT</b>", table_cell_style)],
        [Paragraph("Tasa de fuga de clientes impacientes", table_cell_style), Paragraph("70% de pérdida de tráfico", table_cell_style), Paragraph("<b>Reducida a menos del 15%</b>", table_cell_style)],
        [Paragraph("Cierre mensual estimado de ventas/parcelas", table_cell_style), Paragraph("0 - 1 propiedad", table_cell_style), Paragraph("<b>1 - 3 propiedades / parcelas adicionales</b>", table_cell_style)],
        [Paragraph("Impacto en comisiones ($ CLP estimado)", table_cell_style), Paragraph("Base tradicional", table_cell_style), Paragraph("<b>+$2.500.000 a +$6.000.000 CLP / mes</b>", table_cell_style)]
    ]

    t_roi = Table(roi_data, colWidths=[180, 180, 180])
    t_roi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_roi)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # SECCIÓN 5: ESTRUCTURA DE PLANES EN CLP
    # -------------------------------------------------------------
    story.append(Paragraph("5. PLANES Y MODELO DE INVERSIÓN COMERCIAL ($ CLP)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=8))

    planes_data = [
        [Paragraph("Plan Comercial", table_header_style), Paragraph("Valor Mensual ($ CLP)", table_header_style), Paragraph("Cobertura e Inclusiones", table_header_style)],
        [
            Paragraph("<b>Plan Corredora Pro</b><br/><i>Ideal para corredoras de propiedades locales</i>", table_cell_style),
            Paragraph("<b>$290.000 CLP</b><br/>+ IVA / mes", table_cell_style),
            Paragraph("• ChatBot IA 24/7 en sitio web.<br/>• Alertas a Telegram / WhatsApp de 2 agentes.<br/>• Plataforma Autónoma con micrófono de voz y CRM.<br/>• Atribución de Ventas e impresor de informes ROI.", table_cell_style)
        ],
        [
            Paragraph("<b>Plan Inmobiliaria Multi-Proyecto</b><br/><i>Ideal para inmobiliarias y loteos de parcelas</i>", table_cell_style),
            Paragraph("<b>$590.000 CLP</b><br/>+ IVA / mes", table_cell_style),
            Paragraph("• Todo lo del Plan Pro.<br/>• Cobertura multi-proyecto / loteos ilimitados.<br/>• Integración con CRM (HubSpot, Salesforce, Tokko).<br/>• Capacitación a equipo de ventas + Prompt a medida.", table_cell_style)
        ],
        [
            Paragraph("<b>Setup Inicial & Puesta en Marcha</b><br/><i>Pago único por única vez</i>", table_cell_style),
            Paragraph("<b>$250.000 CLP</b><br/>(Pago Único)", table_cell_style),
            Paragraph("• Configuración de servidor en Render.com.<br/>• Entrenamiento del prompt con catálogo del cliente.<br/>• Prueba de carga y verificación de notificaciones.", table_cell_style)
        ]
    ]

    t_planes = Table(planes_data, colWidths=[150, 130, 260])
    t_planes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT])
    ]))
    story.append(t_planes)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # SECCIÓN 6: PROCESO DE IMPLANTACIÓN (3 PASOS)
    # -------------------------------------------------------------
    story.append(Paragraph("6. PROCESO DE INTEGRACIÓN EN SU SITIO WEB (3 PASOS)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_PRIMARY, spaceAfter=8))

    story.append(Paragraph("<b>1. Configuración de Entorno & Prompt (Día 1):</b> Se ajusta la personalidad de Camila con la cartera de propiedades y el número de atención de la corredora.", bullet_style))
    story.append(Paragraph("<b>2. Instalación de 2 Líneas de HTML (Día 2):</b> Se entregan las 2 líneas de script para pegar antes del <code>&lt;/body&gt;</code> en el sitio web de la corredora (compatible con WordPress, Wix, Webflow o HTML plano).", bullet_style))
    story.append(Paragraph("<b>3. Conexión de Plataforma Autónoma y Subdominio (Día 3):</b> Se deja activa la plataforma del CEO (ej: <code>https://camila.sucorredora.cl</code>) y el probador de notificaciones.", bullet_style))
    story.append(Spacer(1, 16))

    # FOOTER SUMMARY BANNER
    footer_data = [[
        Paragraph("<b>¿Listo para transformar las visitas de tu web en ventas concretadas?</b><br/>"
                  "Contáctanos para activar la versión de prueba de Secretaría Camila™ en tu sitio web.", ParagraphStyle('FText', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.white, alignment=1))
    ]]
    t_footer = Table(footer_data, colWidths=[540])
    t_footer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    story.append(t_footer)

    doc.build(story)
    print(f"PDF generado exitosamente en: {filename}")

if __name__ == '__main__':
    out_dir = r"c:\Users\LyCoNs\Desktop\Secretaria Camila+CHATBOTAI"
    pdf_path = os.path.join(out_dir, "PROPUESTA_INTEGRACION_REGION_LOS_LAGOS.pdf")
    build_pdf(pdf_path)
