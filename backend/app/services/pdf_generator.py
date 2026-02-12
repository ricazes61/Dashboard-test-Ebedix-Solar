from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from pathlib import Path
import io
from typing import Optional

from app.services.data_loader import data_loader
from app.services.kpi_calculator import kpi_calculator

class PDFReportGenerator:
    """Generador de reportes ejecutivos en PDF"""
    
    def __init__(self, output_folder: str = "./data/output"):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
    def generate_executive_report(self, date_range: str = "30d") -> str:
        """Genera reporte ejecutivo en PDF"""
        if not data_loader.planta_data:
            raise ValueError("Datos de planta no cargados")
        
        # Nombre del archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Reporte_Ejecutivo_{timestamp}.pdf"
        filepath = self.output_folder / filename
        
        # Crear documento
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        
        # Contenedor para elementos
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=12,
        )
        
        # === PORTADA ===
        planta = data_loader.planta_data.planta
        
        # Título
        story.append(Spacer(1, 1.5*inch))
        story.append(Paragraph("REPORTE EJECUTIVO", title_style))
        story.append(Paragraph(f"<b>{planta.nombre_planta}</b>", subtitle_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Información de planta
        info_text = f"""
        <b>Ubicación:</b> {planta.ciudad}, {planta.provincia_estado}, {planta.pais}<br/>
        <b>Capacidad:</b> {planta.potencia_dc_mwp:.2f} MWp DC / {planta.potencia_ac_mw:.2f} MW AC<br/>
        <b>Fecha del reporte:</b> {datetime.now().strftime("%d/%m/%Y %H:%M")}<br/>
        <b>Período analizado:</b> {self._get_range_label(date_range)}
        """
        story.append(Paragraph(info_text, styles['Normal']))
        story.append(PageBreak())
        
        # === RESUMEN EJECUTIVO ===
        story.append(Paragraph("Resumen Ejecutivo", subtitle_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Calcular KPIs
        kpis = kpi_calculator.calculate_executive_kpis(date_range)
        
        bullets = [
            f"<b>Energía generada:</b> {kpis.energia_real_kwh:,.0f} kWh "
            f"({kpis.desviacion_pct:+.1f}% vs esperado)",
            
            f"<b>Performance Ratio (PR):</b> {kpis.pr_promedio:.2%} "
            f"(objetivo: {planta.target_pr:.2%})",
            
            f"<b>Disponibilidad:</b> {kpis.availability_promedio_pct:.1f}% "
            f"(objetivo: {planta.target_availability:.1f}%)",
            
            f"<b>Ingresos estimados:</b> USD ${kpis.ingresos_estimados_usd:,.2f}",
            
            f"<b>OPEX estimado:</b> USD ${kpis.opex_estimado_usd:,.2f}",
            
            f"<b>Margen bruto:</b> USD ${kpis.margen_bruto_usd:,.2f} "
            f"({kpis.margen_bruto_pct:.1f}%)",
            
            f"<b>CO₂ evitado:</b> {kpis.co2_evitado_kg:,.0f} kg",
            
            f"<b>Backlog de mantenimiento:</b> USD ${kpis.backlog_total_usd:,.2f} "
            f"({kpis.tickets_pendientes} tickets)",
            
            f"<b>Estado del sistema:</b> {kpis.estado_sistema.upper()}",
        ]
        
        for bullet in bullets:
            story.append(Paragraph(f"• {bullet}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Spacer(1, 0.3*inch))
        
        # === ALERTAS Y RIESGOS ===
        if kpis.alertas_principales:
            story.append(Paragraph("Alertas y Riesgos", subtitle_style))
            story.append(Spacer(1, 0.1*inch))
            
            for alerta in kpis.alertas_principales:
                story.append(Paragraph(f"⚠️ {alerta}", styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
            
            story.append(Spacer(1, 0.3*inch))
        
        # === TABLA DE TOP TICKETS ===
        if kpis.top_tickets:
            story.append(PageBreak())
            story.append(Paragraph("Top Tickets por Costo", subtitle_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Preparar datos de la tabla
            table_data = [
                ['ID', 'Descripción', 'Estado', 'Criticidad', 'Costo (USD)']
            ]
            
            for ticket in kpis.top_tickets[:10]:
                table_data.append([
                    ticket.ticket_id,
                    ticket.descripcion[:40] + '...' if len(ticket.descripcion) > 40 else ticket.descripcion,
                    ticket.estado,
                    ticket.criticidad,
                    f"${ticket.costo_estimado_usd:,.2f}"
                ])
            
            # Crear tabla
            table = Table(table_data, colWidths=[0.8*inch, 2.5*inch, 1*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            story.append(table)
        
        # === PIE DE PÁGINA ===
        story.append(Spacer(1, 0.5*inch))
        footer_text = f"""
        <i>Documento generado automáticamente el {datetime.now().strftime("%d/%m/%Y a las %H:%M")}</i><br/>
        <i>Solar PV Analytics - Vreadynow Digital Twin Platform</i>
        """
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        
        return str(filepath)
    
    def _get_range_label(self, date_range: str) -> str:
        """Convierte código de rango a etiqueta legible"""
        labels = {
            "30d": "Últimos 30 días",
            "90d": "Últimos 90 días",
            "YTD": "Año a la fecha",
            "12m": "Últimos 12 meses"
        }
        return labels.get(date_range, "Últimos 30 días")

# Instancia global
pdf_generator = PDFReportGenerator()
