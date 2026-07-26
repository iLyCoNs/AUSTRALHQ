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
            # Portada: Fondo técnico oscuro (Slate / Dark Teal)
            self.saveState()
            self.setFillColor(colors.HexColor("#0284C7")) # Sky blue accent line
            self.rect(0, 0, 0.4 * inch, 11 * inch, fill=True, stroke=False)
            
            self.setFillColor(colors.HexColor("#0F172A")) # Dark navy background
            self.rect(0.4 * inch, 0, 8.1 * inch, 11 * inch, fill=True, stroke=False)
            
            self.setFillColor(colors.HexColor("#38BDF8")) # Cyan accent stripe
            self.rect(0.4 * inch, 0, 0.08 * inch, 11 * inch, fill=True, stroke=False)
            self.restoreState()
            return

        self.saveState()
        # Encabezado
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 11 * inch - 36, "MANUAL TÉCNICO DE ARQUITECTURA: AGENTES IA, N8N Y GEMINI PRO")
        
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Pie de página
        self.line(54, 46, 8.5 * inch - 54, 46)
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#475569"))
        self.drawString(54, 32, "Documento Técnico - agency-agents + n8n + Gemini Pro Integration")
        
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()


def build_pdf(filename="Manual_Tecnico_Agentes_IA_n8n_Gemini.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Colores del tema técnico
    c_primary = colors.HexColor("#0F172A")    # Dark Slate
    c_secondary = colors.HexColor("#0284C7")  # Sky Blue
    c_cyan = colors.HexColor("#06B6D4")       # Cyan
    c_accent = colors.HexColor("#38BDF8")     # Light Cyan Accent
    c_dark = colors.HexColor("#1E293B")
    c_bg_light = colors.HexColor("#F8FAFC")
    c_code_bg = colors.HexColor("#0F172A")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.white,
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#94A3B8"),
        spaceAfter=25
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
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#38BDF8")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=c_dark
    )

    story = []

    # -------------------------------------------------------------------------
    # PORTADA
    # -------------------------------------------------------------------------
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph("MANUAL DE IMPLEMENTACIÓN Y OPERACIÓN TÉCNICA", ParagraphStyle('CoverPre', fontName='Helvetica-Bold', fontSize=11, leading=13, textColor=c_accent, spaceAfter=10)))
    story.append(Paragraph("ARQUITECTURA DE AGENTES IA CON N8N, GEMINI PRO Y AGENCY-AGENTS", title_style))
    story.append(Paragraph("Guía paso a paso de instalación, costos (opción gratuita vs. producción), flujo de trabajo en n8n y operación técnica.", subtitle_style))
    story.append(Spacer(1, 1.2 * inch))
    
    meta_box = [
        [Paragraph("<b>Repositorio de Origen:</b> github.com/msitarzewski/agency-agents", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor("#CBD5E1")))],
        [Paragraph("<b>Stack Tecnológico:</b> n8n + Google Gemini Pro (AI Studio) + Meta WhatsApp Cloud API", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor("#CBD5E1")))],
        [Paragraph("<b>Análisis de Costos:</b> $0 USD/mes (Tier Gratuito) vs. $5-15 USD/mes (Producción)", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor("#CBD5E1")))],
        [Paragraph("<b>Nivel Técnico:</b> Intermedio - Avanzado (Automatización y Prompt Engineering)", ParagraphStyle('CoverMeta', fontName='Helvetica', fontSize=9.5, leading=13, textColor=colors.HexColor("#38BDF8")))],
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
    # CAPÍTULO 1: CÓMO FUNCIONA EXACTAMENTE AGENCY-AGENTS
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Arquitectura Interna de agency-agents", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))
    
    story.append(Paragraph(
        "El repositorio <code>msitarzewski/agency-agents</code> no es un software ejecutable tradicional de Python o Node.js, sino un **marco de trabajo de prompts estructurados en Markdown (.md)** diseñado para dotar a los LLMs (como Gemini Pro) de una personalidad rigurosa, reglas de comportamiento, flujos de trabajo paso a paso y entregables específicos.",
        body_style
    ))
    
    story.append(Paragraph("Anatomía de un Agente en el Repositorio:", h2_style))
    story.append(Paragraph("Cada archivo `.md` de un agente (ej. <code>marketing/growth-hacker.md</code>) está dividido en 4 secciones críticas:", body_style))

    story.append(Paragraph("<b>1. Identity & Persona (Identidad):</b> Define el rol, tono de voz, filosofía de trabajo y principios éticos. Evita respuestas genéricas tipo 'Asistente de IA'.", bullet_style))
    story.append(Paragraph("<b>2. Core Mission (Misión Principal):</b> Establece el objetivo exacto del agente (ej. <i>'Maximizar la tasa de conversión de leads de parcelas en la X Región'</i>).", bullet_style))
    story.append(Paragraph("<b>3. Battle-Tested Workflows (Flujos de Trabajo):</b> Reglas algorítmicas paso a paso que el agente DEBE seguir antes de dar una respuesta final.", bullet_style))
    story.append(Paragraph("<b>4. Technical Deliverables (Entregables):</b> Especifica los formatos exactos de salida (tablas, guiones, JSON, copys publicitarios).", bullet_style))

    story.append(Spacer(1, 8))

    # Diagrama textual de transformación
    story.append(Paragraph("Transformación de Archivo .md a Agente Activo en n8n:", h2_style))
    
    diag_box = [
        [Paragraph("<b>[ Archivo .md en GitHub ]</b><br/><code>marketing/growth-hacker.md</code>", ParagraphStyle('D1', fontName='Helvetica', fontSize=8, textColor=colors.HexColor("#93C5FD"))),
         Paragraph("➔", ParagraphStyle('Arrow', fontName='Helvetica-Bold', fontSize=12, textColor=colors.white)),
         Paragraph("<b>[ Extracción de System Prompt ]</b><br/>Copia del contenido de Identidad y Reglas", ParagraphStyle('D2', fontName='Helvetica', fontSize=8, textColor=colors.HexColor("#93C5FD"))),
         Paragraph("➔", ParagraphStyle('Arrow', fontName='Helvetica-Bold', fontSize=12, textColor=colors.white)),
         Paragraph("<b>[ Nodo AI Agent en n8n ]</b><br/>Motor Gemini Pro + Memoria + Tools", ParagraphStyle('D3', fontName='Helvetica', fontSize=8, textColor=colors.HexColor("#38BDF8")))]
    ]
    t_diag = Table(diag_box, colWidths=[2.2 * inch, 0.3 * inch, 2.2 * inch, 0.3 * inch, 2.0 * inch])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#334155"))
    ]))
    story.append(t_diag)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CAPÍTULO 2: INSTALACIÓN Y CONFIGURACIÓN DEL REPOSITORIO
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Instalación y Configuración Paso a Paso", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>Opción A: Instalación vía Git (Recomendado para inspección local)</b>", h2_style))
    story.append(Paragraph("Abre tu terminal (PowerShell, Bash o VS Code) y ejecuta los siguientes comandos:", body_style))

    code_git = [
        [Paragraph("# 1. Clonar el repositorio oficial de agency-agents<br/>git clone https://github.com/msitarzewski/agency-agents.git<br/><br/># 2. Ingresar al directorio del proyecto<br/>cd agency-agents<br/><br/># 3. Explorar la división de marketing y ventas<br/>ls marketing/<br/>ls sales/", code_style)]
    ]
    t_code1 = Table(code_git, colWidths=[6.8 * inch])
    t_code1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155"))
    ]))
    story.append(t_code1)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Opción B: Uso directo en IDEs (Cursor, VS Code, Claude Code)</b>", h2_style))
    story.append(Paragraph("Si utilizas Cursor o Windsurf, puedes copiar las reglas del agente directamente a la carpeta de configuración de tu proyecto:", body_style))
    story.append(Paragraph("• En Cursor: Copia el archivo `.md` del agente dentro de la carpeta <code>.cursor/rules/</code> con extensión <code>.mdc</code>.", bullet_style))
    story.append(Paragraph("• En Claude Code: Copia los archivos de agentes en <code>~/.claude/agents/</code>.", bullet_style))

    story.append(Spacer(1, 10))
    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 3: DESGLOSE DE COSTOS (OPCIÓN GRATUITA VS PRODUCCIÓN)
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Análisis de Costos: Gratuito vs. Producción", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Una de las mayores ventajas de disponer de <b>n8n</b> y <b>Gemini Pro</b> es que puedes lanzar este sistema con **$0 USD de costo inicial**, evaluarlo con clientes reales y solo escalar a infraestructura de pago cuando comiences a facturar.",
        body_style
    ))

    cost_table_data = [
        [Paragraph("Componente del Stack", table_header_style), Paragraph("Opción 100% Gratuita (MVP)", table_header_style), Paragraph("Opción Producción Mínima", table_header_style)],
        [
            Paragraph("<b>Motor IA (LLM)</b>", table_cell_style),
            Paragraph("<b>Google AI Studio (Gemini 1.5/2.0 Flash/Pro)</b><br/>Free Tier: 15 solicitudes/minuto gratis.", table_cell_style),
            Paragraph("<b>Gemini Pro API (Pay-as-you-go)</b><br/>~$0.001 USD por conversacion (Aprox $2 USD/mes para 2.000 chats).", table_cell_style)
        ],
        [
            Paragraph("<b>Orquestador (n8n)</b>", table_cell_style),
            Paragraph("<b>n8n Self-Hosted Local</b><br/>Ejecutado gratis en tu PC vía Docker o n8n Desktop.", table_cell_style),
            Paragraph("<b>n8n en VPS (Hetzner / DigitalOcean)</b><br/>Servidor VPS básico (2GB RAM): <b>$5 USD / mes</b>.", table_cell_style)
        ],
        [
            Paragraph("<b>API de WhatsApp</b>", table_cell_style),
            Paragraph("<b>Meta WhatsApp Cloud API</b><br/>Primeras 1.000 conversaciones/mes son <b>100% Gratis</b>.", table_cell_style),
            Paragraph("<b>Evolution API (Self-hosted) o Meta Cloud</b><br/>~$0.005 USD por conversación iniciada por negocio.", table_cell_style)
        ],
        [
            Paragraph("<b>Base de Datos / Memoria</b>", table_cell_style),
            Paragraph("<b>PostgreSQL / SQLite local</b><br/>Incluido gratis en el contenedor de n8n.", table_cell_style),
            Paragraph("<b>Redis + PostgreSQL en VPS</b><br/>Incluido dentro del servidor VPS de $5 USD/mes.", table_cell_style)
        ],
        [
            Paragraph("<b>COSTO TOTAL MENSUAL</b>", ParagraphStyle('TotCost', parent=table_cell_style, fontName='Helvetica-Bold', textColor=c_primary)),
            Paragraph("<b>$0 USD / mes</b>", ParagraphStyle('FreeVal', parent=table_cell_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#16A34A"))),
            Paragraph("<b>$5 a $12 USD / mes</b>", ParagraphStyle('PaidVal', parent=table_cell_style, fontName='Helvetica-Bold', textColor=c_secondary))
        ]
    ]

    t_cost = Table(cost_table_data, colWidths=[1.8 * inch, 2.5 * inch, 2.5 * inch])
    t_cost.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, c_bg_light]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#E0F2FE")),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_cost)
    story.append(Spacer(1, 12))

    # -------------------------------------------------------------------------
    # CAPÍTULO 4: INTEGRACIÓN TÉCNICA EN N8N CON GEMINI PRO
    # -------------------------------------------------------------------------
    story.append(Paragraph("4. Construcción del Workflow en n8n con Gemini Pro", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("Para conectar el agente de `agency-agents` en n8n, la arquitectura del workflow consta de 5 nodos interconectados:", body_style))

    story.append(Paragraph("<b>1. Webhook Node (Entrada):</b> Recibe la notificación POST de Meta WhatsApp / Evolution API cuando un cliente envía un mensaje.", bullet_style))
    story.append(Paragraph("<b>2. Switch / Filter Node:</b> Verifica que el mensaje contenga texto válido y extrae el número del remitente (<code>sender_phone</code>).", bullet_style))
    story.append(Paragraph("<b>3. Window Buffer Memory Node:</b> Mantiene la memoria de los últimos 10 a 15 mensajes del cliente para darle contexto a la conversación.", bullet_style))
    story.append(Paragraph("<b>4. AI Agent Node (Google Gemini Chat Model):</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>Credential:</b> API Key de Google AI Studio (Gemini Pro).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;• <b>System Prompt:</b> Se pega el contenido íntegro del agente <code>sales/outbound-strategist.md</code> o <code>growth-hacker.md</code>.", bullet_style))
    story.append(Paragraph("<b>5. HTTP Request Node (Salida):</b> Envía la respuesta generada por Gemini Pro de vuelta al WhatsApp del cliente.", bullet_style))

    story.append(Spacer(1, 8))

    story.append(Paragraph("Ejemplo de Configuración del System Prompt en el nodo AI Agent de n8n:", h2_style))

    code_prompt = [
        [Paragraph(
            "ROLE: Eres Camila, Asesora Inmobiliaria Experta en la Región de Los Lagos (Puerto Varas, Puerto Montt).<br/>"
            "MISSION: Cualificar prospectos interesados en parcelas de 5.000 m2 con Rol Propio.<br/><br/>"
            "REGLAS OBLIGATORIAS:<br/>"
            "1. Mantén un tono cercano, profesional y seguro (español de Chile).<br/>"
            "2. NUNCA respondas más de 3 párrafos por mensaje.<br/>"
            "3. En el primer mensaje, indaga si buscan construir o invertir.<br/>"
            "4. En el segundo mensaje, confirma si requieren financiamiento o presupuesto directo.<br/>"
            "5. Si el cliente está calificado, ofrece agendar visita para el fin de semana.",
            code_style
        )]
    ]
    t_prompt = Table(code_prompt, colWidths=[6.8 * inch])
    t_prompt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155"))
    ]))
    story.append(t_prompt)
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # CAPÍTULO 5: MANUAL DEL OPERADOR (CÓMO INTERACTUAR Y MANEJAR EL AGENTE)
    # -------------------------------------------------------------------------
    story.append(Paragraph("5. Guía del Operador: Control y Operación Diaria", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    story.append(Paragraph(
        "Como operador del sistema, tu función principal es supervisar la ejecución de los agentes, ajustar prompts de comportamiento y gestionar las excepciones cuando un cliente requiere atención humana directa.",
        body_style
    ))

    story.append(Paragraph("Comandos de Invocación y Cambio de Modo:", h2_style))
    story.append(Paragraph("Puedes interactuar con los agentes en tu entorno local (Cursor/n8n/CLI) utilizando comandos de activación directos:", body_style))

    cmd_table_data = [
        [Paragraph("Comando / Contexto", table_header_style), Paragraph("Agente Activado", table_header_style), Paragraph("Acción Ejecutada por la IA", table_header_style)],
        [
            Paragraph("<code>'Activa modo Growth Hacker y audita este proyecto de parcelas'</code>", table_cell_style),
            Paragraph("<b>Growth Hacker</b>", table_cell_style),
            Paragraph("Analiza la propuesta de valor del loteo, detecta puntos débiles y diseña el mapa del embudo.", table_cell_style)
        ],
        [
            Paragraph("<code>'Genera 10 copies de Meta Ads para parcelas en Puerto Varas'</code>", table_cell_style),
            Paragraph("<b>Paid Social Strategist</b>", table_cell_style),
            Paragraph("Escribe ángulos emocionales enfocados en familias de Santiago buscando calidad de vida.", table_cell_style)
        ],
        [
            Paragraph("<code>'Redacta secuencia de contacto B2B para dueños de loteos'</code>", table_cell_style),
            Paragraph("<b>Outbound Strategist</b>", table_cell_style),
            Paragraph("Crea correos y mensajes de LinkedIn para ofrecer el servicio de marketing a inmobiliarias.", table_cell_style)
        ],
        [
            Paragraph("<code>'Genera ficha técnica y dossier de inversión para el Lote 14'</code>", table_cell_style),
            Paragraph("<b>Proposal Strategist</b>", table_cell_style),
            Paragraph("Estructura la información técnica, plano, coordenadas y desglose de pago para el cliente.", table_cell_style)
        ]
    ]

    t_cmd = Table(cmd_table_data, colWidths=[2.2 * inch, 1.4 * inch, 3.2 * inch])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_cmd)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Protocolo de Handover (Traspaso a Vendedor Humano):", h2_style))
    story.append(Paragraph("En n8n, se debe configurar una regla de **Humano en el Bucle (Human-in-the-loop)**:", body_style))
    story.append(Paragraph("<b>1. Detección de Intención Crítica:</b> Si el prospecto escribe palabras clave como <i>'quiero transferir la reserva'</i>, <i>'hablar con un humano'</i> o realiza preguntas legales complejas.", bullet_style))
    story.append(Paragraph("<b>2. Desactivación del Bot:</b> n8n marca la variable <code>bot_active = false</code> en la base de datos para este número de teléfono.", bullet_style))
    story.append(Paragraph("<b>3. Notificación Push:</b> n8n envía una alerta por Telegram o WhatsApp al teléfono del vendedor humano: <i>'🚨 Cliente listo para reserva: +56 9 XXXX XXXX'</i>.", bullet_style))

    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # CAPÍTULO 6: RESOLUCIÓN DE PROBLEMAS Y MEJORES PRÁCTICAS
    # -------------------------------------------------------------------------
    story.append(Paragraph("6. Solución de Problemas y Buenas Prácticas", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_secondary, spaceBefore=2, spaceAfter=10))

    trouble_data = [
        ("Problema: El bot alucina datos de las parcelas (precios o ubicaciones falsas)", [
            "<b>Solución:</b> Incluye la matriz de datos de las parcelas en formato JSON estructurado dentro del nodo de contexto o memoria en n8n.",
            "Añade la instrucción explícita: <i>'Si la información no está en el documento adjunto, responde: No dispongo de esa información exacta, lo verificaré con el equipo técnico.'</i>"
        ]),
        ("Problema: Bloqueo o baneo de número de WhatsApp por spam", [
            "<b>Solución:</b> NUNCA envíes mensajes masivos fríos no solicitados por WhatsApp.",
            "Usa WhatsApp **ÚNICAMENTE para responder a prospectos que hicieron clic voluntariamente en tus anuncios** (Inbound Leads). De esta forma el 100% de las conversaciones son iniciadas por el usuario."
        ]),
        ("Problema: Latencia en las respuestas de Gemini Pro", [
            "<b>Solución:</b> Utiliza el modelo <b>Gemini 1.5 Flash</b> o <b>Gemini 2.0 Flash</b> para conversaciones directas de chat (tiempo de respuesta < 1.5 segundos). Reserva Gemini Pro para tareas analíticas pesadas."
        ])
    ]

    for title, points in trouble_data:
        story.append(Paragraph(title, h2_style))
        for p in points:
            story.append(Paragraph(f"• {p}", bullet_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))

    # Conclusión final técnica
    tech_box = [
        [Paragraph("<b>RESUMEN TÉCNICO:</b> Tienes en tus manos el stack tecnológico más eficiente del mercado actual: n8n como orquestador, Gemini Pro como cerebro analítico y agency-agents como la biblioteca de conocimiento especializado. Comenzar en la versión de $0 USD te permite validar el sistema hoy mismo.", ParagraphStyle('TechText', fontName='Helvetica', fontSize=9, leading=13.5, textColor=c_primary))]
    ]
    t_tech = Table(tech_box, colWidths=[6.8 * inch])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E0F2FE")),
        ('BOX', (0,0), (-1,-1), 1, c_secondary),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_tech)

    # Construir PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF técnico generado exitosamente: {filename}")

if __name__ == "__main__":
    build_pdf()
