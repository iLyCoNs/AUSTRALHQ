import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

os.makedirs('DOCUMENTACION_Y_PDFS', exist_ok=True)
pdf_path = os.path.join('DOCUMENTACION_Y_PDFS', 'COTIZACION_AUSTRALDRONE_RUTA5_100K.pdf')
doc = SimpleDocTemplate(pdf_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)

styles = getSampleStyleSheet()

# Color Palette
primary = colors.HexColor('#0284c7')
secondary = colors.HexColor('#090d16')
accent = colors.HexColor('#10b981')
bg_light = colors.HexColor('#f8fafc')
dark_txt = colors.HexColor('#1e293b')

title_style = ParagraphStyle('TitleStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=primary)
body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=dark_txt)
bold_style = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=13.5, textColor=dark_txt)
header_table_style = ParagraphStyle('HTStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.white)

elements = []

# 1. HEADER BRANDING
header_data = [
    [
        Paragraph('<b>AUSTRALDRONE.CL</b><br/><font size=8.5 color="#64748b">Servicios Aéreos de Alta Precisión & Maquetas 3D</font>', title_style),
        Paragraph('<b>COTIZACIÓN FORMAL</b><br/><font color="#0284c7">N° COT-2026-07-4029</font><br/><font size=8.5 color="#64748b">Fecha: 27 de Julio, 2026</font>', ParagraphStyle('RightHd', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, alignment=2))
    ]
]
t_hd = Table(header_data, colWidths=[340, 200])
t_hd.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
elements.append(t_hd)
elements.append(Spacer(1, 8))
elements.append(HRFlowable(width="100%", thickness=2, color=primary, spaceAfter=14))

# 2. CLIENT & PROVIDER INFO
info_data = [
    [
        Paragraph('<b>DATOS DEL CLIENTE:</b><br/><b>Cliente:</b> Particular<br/><b>Solicitud:</b> Grabación Aérea Drone Ruta 5 Interior<br/><b>Estado:</b> Emitida / Válida por 15 Días', body_style),
        Paragraph('<b>PROVEEDOR DEL SERVICIO:</b><br/><b>Empresa:</b> AustralDrone.CL SpA<br/><b>Sitio Web:</b> www.australdrone.cl<br/><b>Fono / WhatsApp:</b> +56 9 8412 9034', body_style)
    ]
]
t_info = Table(info_data, colWidths=[270, 270])
t_info.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), bg_light),
    ('PADDING', (0,0), (-1,-1), 10),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
    ('VALIGN', (0,0), (-1,-1), 'TOP')
]))
elements.append(t_info)
elements.append(Spacer(1, 14))

# 3. LOCATION & GPS MAP ACCESS
elements.append(Paragraph('📍 <b>UBICACIÓN TÁCTICA Y RUTEO DE ACCESO (COORDENADAS GPS)</b>', ParagraphStyle('SecTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, textColor=primary)))
elements.append(Spacer(1, 4))

loc_text = '''
<b>Coordenadas GPS Objetivo:</b> <font color="#0284c7"><b>-41.373013, -72.999397</b></font><br/>
<b>Sector:</b> Ruta 5 Sur - Interior (Eje Puerto Varas - Alerce Norte / La Vara, Región de Los Lagos).<br/>
<b>Mejores Indicaciones de Ruteo y Acceso:</b><br/>
• <b>Ruta de Llegada Principal:</b> Conducir por Ruta 5 Sur en dirección Sur hacia el km 1010.<br/>
• <b>Desvío Caletera Interior:</b> Tomar la salida lateral hacia la caletera Este en dirección al cruce La Vara / Alerce Norte.<br/>
• <b>Ingreso al Predio:</b> Avanzar 800 metros por el camino vecinal interior asfaltado/estabilizado.<br/>
• <b>Punto Cero (Despegue Seguro):</b> Zona despejada plana habilitada libre de tendido eléctrico de alta tensión, con visibilidad directa de 360° para operaciones bajo normativa DGAC.
'''
elements.append(Paragraph(loc_text, body_style))
elements.append(Spacer(1, 14))

# 4. SERVICES TABLE
elements.append(Paragraph('🚁 <b>DETALLE DE SERVICIOS Y EQUIPAMIENTO TÉCNICO</b>', ParagraphStyle('SecTitle2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, textColor=primary)))
elements.append(Spacer(1, 6))

table_data = [
    [Paragraph('<b>DESCRIPCIÓN DEL SERVICIO</b>', header_table_style), Paragraph('<b>CANT.</b>', header_table_style), Paragraph('<b>VALOR NETO</b>', header_table_style)]
]

items = [
    ('<b>Operación de Vuelo Aéreo 4K UHD en Ruta 5 Interior</b><br/><font size=8.5 color="#475569">• Vuelo de grabación con Drone DJI Mavic 3 Cine / Hasselblad CMOS 4/3.<br/>• Captura de Tomas Aéreas 4K @ 60fps & 15+ Fotografías HDR 20 MP.<br/>• Piloto Certificado DGAC con protocolo de seguridad operacional.</font>', '1 Servicio', '$75.000 CLP'),
    ('<b>Post-Procesamiento, Corrección de Color & Entrega Cloud</b><br/><font size=8.5 color="#475569">• Edición de video en D-Log con corrección de color cinemática.<br/>• Respaldo digital en servidor privado cloud para descarga inmediata en 24 hrs.</font>', '1 Pack', '$25.000 CLP')
]

for item, cant, val in items:
    table_data.append([Paragraph(item, body_style), Paragraph(cant, body_style), Paragraph(val, bold_style)])

t_services = Table(table_data, colWidths=[350, 80, 110])
t_services.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), primary),
    ('PADDING', (0,0), (-1,-1), 8),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
]))
elements.append(t_services)
elements.append(Spacer(1, 10))

# 5. TOTALS
totals_data = [
    [Paragraph('<b>SUBTOTAL NETO:</b>', ParagraphStyle('R1', parent=body_style, alignment=2)), Paragraph('<b>$100.000 CLP</b>', ParagraphStyle('R2', parent=bold_style, alignment=2))],
    [Paragraph('<b>IVA (EXENTO / MONTO ACORDADO):</b>', ParagraphStyle('R3', parent=body_style, alignment=2)), Paragraph('<b>$0 CLP</b>', ParagraphStyle('R4', parent=bold_style, alignment=2))],
    [Paragraph('<font size=11 color="#10b981"><b>TOTAL A PAGAR:</b></font>', ParagraphStyle('R5', parent=body_style, alignment=2)), Paragraph('<font size=11 color="#10b981"><b>$100.000 CLP</b></font>', ParagraphStyle('R6', parent=bold_style, alignment=2))]
]
t_totals = Table(totals_data, colWidths=[380, 160])
t_totals.setStyle(TableStyle([
    ('PADDING', (0,0), (-1,-1), 4),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
]))
elements.append(t_totals)
elements.append(Spacer(1, 16))

# 6. PROMOTIONAL BANNER FOR WWW.AUSTRALDRONE.CL
promo_data = [
    [
        Paragraph('''
<font color="#66fcf1" size=10.5><b>🌟 ¿DESARROLLAS LOTEOS, PARCELACIONES O PROYECTOS EN EL SUR?</b></font><br/>
<font color="#ffffff" size=8.5>
Conoce nuestras maquetas 3D interactivas y <b>MasterPlans 360°</b> con ortomosaicos aéreos georreferenciados. Aumenta la velocidad de venta de tus terrenos con maquetas inmersivas recorribles desde cualquier smartphone o PC.<br/>
👉 <b>Visítanos hoy en <font color="#66fcf1"><u>www.australdrone.cl</u></font> y solicita una demostración en vivo.</b>
</font>
        ''', ParagraphStyle('PromoStyle', parent=styles['Normal'], leading=12.5))
    ]
]
t_promo = Table(promo_data, colWidths=[540])
t_promo.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#090d16')),
    ('PADDING', (0,0), (-1,-1), 12),
    ('BOX', (0,0), (-1,-1), 2, colors.HexColor('#0284c7')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
]))
elements.append(t_promo)
elements.append(Spacer(1, 12))

# 7. TERMS & SIGNATURE
terms_text = '''
<b>Condiciones Comerciales:</b> Validez de cotización: 15 días corridos. Forma de pago: 50% al confirmar vuelo y 50% a la entrega del material final. Vuelo sujeto a condiciones meteorológicas favorables según norma DGAC.<br/>
<b>AustralDrone.CL — Innovación Aérea & Fotogrametría 3D en la Patagonia</b>
'''
elements.append(Paragraph(terms_text, ParagraphStyle('Terms', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#64748b'), alignment=1)))

doc.build(elements)
print('✅ PDF Generado exitosamente en: ' + pdf_path)
