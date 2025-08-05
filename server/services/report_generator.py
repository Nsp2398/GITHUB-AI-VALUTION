from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
from typing import Dict, Any, List
import os
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
import base64

class ReportGenerator:
    def __init__(self):
        self.document = Document()
        self.styles = getSampleStyleSheet()
        
    def generate_report_all_formats(self, 
                                  company_info: Dict[str, Any],
                                  valuation_data: Dict[str, Any],
                                  market_data: Dict[str, Any],
                                  peer_comparison: List[Dict[str, Any]],
                                  output_dir: str = "reports") -> Dict[str, str]:
        """Generate reports in all formats and return file paths"""
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        company_name = company_info.get("name", "Company").replace(" ", "_")
        
        # Generate all format reports
        formats = {}
        
        # Word format
        word_path = os.path.join(output_dir, f"{company_name}_valuation_report_{timestamp}.docx")
        self.generate_word_report(company_info, valuation_data, market_data, peer_comparison, word_path)
        formats['docx'] = word_path
        
        # PDF format
        pdf_path = os.path.join(output_dir, f"{company_name}_valuation_report_{timestamp}.pdf")
        self.generate_pdf_report(company_info, valuation_data, market_data, peer_comparison, pdf_path)
        formats['pdf'] = pdf_path
        
        # Text format
        txt_path = os.path.join(output_dir, f"{company_name}_valuation_report_{timestamp}.txt")
        self.generate_text_report(company_info, valuation_data, market_data, peer_comparison, txt_path)
        formats['txt'] = txt_path
        
        # Image format
        img_path = os.path.join(output_dir, f"{company_name}_valuation_report_{timestamp}.png")
        self.generate_image_report(company_info, valuation_data, market_data, peer_comparison, img_path)
        formats['png'] = img_path
        
        return formats

    def generate_word_report(self, 
                           company_info: Dict[str, Any],
                           valuation_data: Dict[str, Any],
                           market_data: Dict[str, Any],
                           peer_comparison: List[Dict[str, Any]],
                           file_path: str) -> str:
        """Generate a detailed valuation report in DOCX format"""
        
        doc = Document()
        
        # Add title
        title = doc.add_heading('UCaaS Company Valuation Report', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add date
        date_paragraph = doc.add_paragraph()
        date_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        date_paragraph.add_run(f'Report Date: {datetime.now().strftime("%B %d, %Y")}')
        
        # Executive Summary
        doc.add_heading('Executive Summary', level=1)
        summary = doc.add_paragraph()
        summary.add_run('Company Overview\n').bold = True
        summary.add_run(f'Company Name: {company_info.get("name", "N/A")}\n')
        summary.add_run(f'Industry: UCaaS (Unified Communications as a Service)\n')
        summary.add_run(f'Annual Recurring Revenue (ARR): ${company_info.get("arr", 0):,.2f}\n')
        
        # Key Metrics
        doc.add_heading('Key Financial Metrics', level=1)
        metrics_table = doc.add_table(rows=1, cols=2)
        metrics_table.style = 'Table Grid'
        
        # Add header row
        header_cells = metrics_table.rows[0].cells
        header_cells[0].text = 'Metric'
        header_cells[1].text = 'Value'
        
        metrics = [
            ('Growth Rate', f'{valuation_data.get("growth_rate", 0)*100:.1f}%'),
            ('Gross Margin', f'{valuation_data.get("gross_margin", 0)*100:.1f}%'),
            ('Net Revenue Retention', f'{valuation_data.get("net_revenue_retention", 0)*100:.1f}%'),
            ('Rule of 40 Score', f'{valuation_data.get("rule_of_40", 0):.1f}'),
            ('LTV/CAC Ratio', f'{valuation_data.get("ltv_cac_ratio", 0):.2f}'),
            ('Company Valuation', f'${valuation_data.get("valuation", 0):,.2f}'),
        ]
        
        for metric, value in metrics:
            row_cells = metrics_table.add_row().cells
            row_cells[0].text = metric
            row_cells[1].text = value
        
        # Market Analysis
        doc.add_heading('Market Analysis', level=1)
        market_para = doc.add_paragraph()
        market_para.add_run(f'Market Size: ${market_data.get("market_size", 0):,.2f}\n')
        market_para.add_run(f'Market Growth Rate: {market_data.get("market_growth", 0)*100:.1f}%\n')
        market_para.add_run(f'Competitive Position: {market_data.get("competitive_position", "N/A")}\n')
        
        # Valuation Summary
        doc.add_heading('Valuation Summary', level=1)
        valuation_para = doc.add_paragraph()
        valuation_para.add_run(f'Total Company Valuation: ${valuation_data.get("valuation", 0):,.2f}\n').bold = True
        valuation_para.add_run(f'Revenue Multiple: {valuation_data.get("revenue_multiple", 0):.2f}x\n')
        valuation_para.add_run(f'EBITDA Multiple: {valuation_data.get("ebitda_multiple", 0):.2f}x\n')
        
        doc.save(file_path)
        return file_path
    
    def generate_pdf_report(self, 
                          company_info: Dict[str, Any],
                          valuation_data: Dict[str, Any],
                          market_data: Dict[str, Any],
                          peer_comparison: List[Dict[str, Any]],
                          file_path: str) -> str:
        """Generate a PDF valuation report"""
        
        doc = SimpleDocTemplate(file_path, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        story = []
        
        # Title
        title = Paragraph("UCaaS Company Valuation Report", title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Date
        date_style = ParagraphStyle('DateStyle', parent=styles['Normal'], alignment=TA_RIGHT)
        date_para = Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y')}", date_style)
        story.append(date_para)
        story.append(Spacer(1, 12))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        story.append(Spacer(1, 6))
        
        summary_text = f"""
        <b>Company Name:</b> {company_info.get("name", "N/A")}<br/>
        <b>Industry:</b> UCaaS (Unified Communications as a Service)<br/>
        <b>Annual Recurring Revenue (ARR):</b> ${company_info.get("arr", 0):,.2f}<br/>
        """
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Key Metrics Table
        story.append(Paragraph("Key Financial Metrics", styles['Heading2']))
        story.append(Spacer(1, 6))
        
        metrics_data = [
            ['Metric', 'Value'],
            ['Growth Rate', f'{valuation_data.get("growth_rate", 0)*100:.1f}%'],
            ['Gross Margin', f'{valuation_data.get("gross_margin", 0)*100:.1f}%'],
            ['Net Revenue Retention', f'{valuation_data.get("net_revenue_retention", 0)*100:.1f}%'],
            ['Rule of 40 Score', f'{valuation_data.get("rule_of_40", 0):.1f}'],
            ['LTV/CAC Ratio', f'{valuation_data.get("ltv_cac_ratio", 0):.2f}'],
            ['Company Valuation', f'${valuation_data.get("valuation", 0):,.2f}'],
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 12))
        
        # Valuation Summary
        story.append(Paragraph("Valuation Summary", styles['Heading2']))
        story.append(Spacer(1, 6))
        
        valuation_text = f"""
        <b>Total Company Valuation:</b> ${valuation_data.get("valuation", 0):,.2f}<br/>
        <b>Revenue Multiple:</b> {valuation_data.get("revenue_multiple", 0):.2f}x<br/>
        <b>EBITDA Multiple:</b> {valuation_data.get("ebitda_multiple", 0):.2f}x<br/>
        """
        story.append(Paragraph(valuation_text, styles['Normal']))
        
        doc.build(story)
        return file_path
    
    def generate_text_report(self, 
                           company_info: Dict[str, Any],
                           valuation_data: Dict[str, Any],
                           market_data: Dict[str, Any],
                           peer_comparison: List[Dict[str, Any]],
                           file_path: str) -> str:
        """Generate a plain text valuation report"""
        
        report_content = f"""
UCaaS COMPANY VALUATION REPORT
{'='*50}

Report Date: {datetime.now().strftime('%B %d, %Y')}

EXECUTIVE SUMMARY
{'-'*20}
Company Name: {company_info.get("name", "N/A")}
Industry: UCaaS (Unified Communications as a Service)
Annual Recurring Revenue (ARR): ${company_info.get("arr", 0):,.2f}

KEY FINANCIAL METRICS
{'-'*25}
Growth Rate: {valuation_data.get("growth_rate", 0)*100:.1f}%
Gross Margin: {valuation_data.get("gross_margin", 0)*100:.1f}%
Net Revenue Retention: {valuation_data.get("net_revenue_retention", 0)*100:.1f}%
Rule of 40 Score: {valuation_data.get("rule_of_40", 0):.1f}
LTV/CAC Ratio: {valuation_data.get("ltv_cac_ratio", 0):.2f}

MARKET ANALYSIS
{'-'*16}
Market Size: ${market_data.get("market_size", 0):,.2f}
Market Growth Rate: {market_data.get("market_growth", 0)*100:.1f}%
Competitive Position: {market_data.get("competitive_position", "N/A")}

VALUATION SUMMARY
{'-'*18}
Total Company Valuation: ${valuation_data.get("valuation", 0):,.2f}
Revenue Multiple: {valuation_data.get("revenue_multiple", 0):.2f}x
EBITDA Multiple: {valuation_data.get("ebitda_multiple", 0):.2f}x

DISCLAIMER
{'-'*10}
This valuation report is based on the information provided and standard UCaaS industry metrics.
The valuation is an estimate and should not be considered as investment advice.
Actual market conditions and company-specific factors may affect the true valuation.

Report Generated by ValuAI - UCaaS Valuation Platform
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return file_path
    
    def generate_image_report(self, 
                            company_info: Dict[str, Any],
                            valuation_data: Dict[str, Any],
                            market_data: Dict[str, Any],
                            peer_comparison: List[Dict[str, Any]],
                            file_path: str) -> str:
        """Generate an image-based valuation report"""
        
        # Create a figure with multiple subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'UCaaS Valuation Report - {company_info.get("name", "Company")}', fontsize=20, fontweight='bold')
        
        # 1. Key Metrics Bar Chart
        metrics = ['Growth Rate', 'Gross Margin', 'NRR', 'Rule of 40']
        values = [
            valuation_data.get("growth_rate", 0) * 100,
            valuation_data.get("gross_margin", 0) * 100,
            valuation_data.get("net_revenue_retention", 0) * 100,
            valuation_data.get("rule_of_40", 0)
        ]
        
        ax1.bar(metrics, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        ax1.set_title('Key Performance Metrics', fontweight='bold')
        ax1.set_ylabel('Percentage / Score')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Add value labels on bars
        for i, v in enumerate(values):
            ax1.text(i, v + max(values)*0.01, f'{v:.1f}%' if i < 3 else f'{v:.1f}', 
                    ha='center', va='bottom', fontweight='bold')
        
        # 2. Valuation Breakdown Pie Chart
        valuation_components = {
            'Revenue Multiple': valuation_data.get("revenue_multiple", 0) * company_info.get("arr", 0),
            'Growth Premium': valuation_data.get("valuation", 0) * 0.3,
            'Market Position': valuation_data.get("valuation", 0) * 0.2,
            'Other Factors': valuation_data.get("valuation", 0) * 0.5
        }
        
        ax2.pie(valuation_components.values(), labels=valuation_components.keys(), autopct='%1.1f%%', startangle=90)
        ax2.set_title('Valuation Components', fontweight='bold')
        
        # 3. Financial Summary Table
        ax3.axis('tight')
        ax3.axis('off')
        
        table_data = [
            ['Metric', 'Value'],
            ['Company Valuation', f'${valuation_data.get("valuation", 0):,.0f}'],
            ['Annual Recurring Revenue', f'${company_info.get("arr", 0):,.0f}'],
            ['Revenue Multiple', f'{valuation_data.get("revenue_multiple", 0):.2f}x'],
            ['LTV/CAC Ratio', f'{valuation_data.get("ltv_cac_ratio", 0):.2f}'],
            ['Market Size', f'${market_data.get("market_size", 0):,.0f}']
        ]
        
        table = ax3.table(cellText=table_data, cellLoc='center', loc='center',
                         colWidths=[0.5, 0.5])
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.5)
        
        # Style the header row
        for i in range(len(table_data[0])):
            table[(0, i)].set_facecolor('#4472C4')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        ax3.set_title('Financial Summary', fontweight='bold')
        
        # 4. Growth Trend (simulated)
        years = list(range(2020, 2026))
        current_arr = company_info.get("arr", 1000000)
        growth_rate = valuation_data.get("growth_rate", 0.3)
        
        projected_arr = [current_arr * (1 + growth_rate) ** (year - 2025) for year in years]
        
        ax4.plot(years, projected_arr, marker='o', linewidth=3, markersize=8, color='#2ca02c')
        ax4.fill_between(years, projected_arr, alpha=0.3, color='#2ca02c')
        ax4.set_title('ARR Growth Projection', fontweight='bold')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Annual Recurring Revenue ($)')
        ax4.grid(True, alpha=0.3)
        
        # Format y-axis to show values in millions
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        
        plt.tight_layout()
        plt.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return file_path
