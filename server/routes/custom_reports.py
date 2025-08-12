"""
Advanced Custom Reporting Service for ValuAI
Provides flexible report generation with custom templates and data sources
"""

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.database import SessionLocal
from models.models import User, Company, Valuation
from models.enhanced_models import ValuationAnalytics, MarketBenchmarks
from services.analytics_service import AnalyticsService
from datetime import datetime, timedelta
import json
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import Dict, List, Optional
import tempfile
import os

custom_reports_bp = Blueprint('custom_reports', __name__, url_prefix='/api/custom-reports')

class CustomReportBuilder:
    """Advanced report builder with customizable templates and data sources"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.analytics_service = AnalyticsService(db_session)
    
    def generate_executive_summary_report(self, company_id: int, user_id: int, config: Dict) -> Dict:
        """Generate executive summary report with custom sections"""
        try:
            # Get company data
            company = self.db.query(Company).filter(
                Company.id == company_id,
                Company.user_id == user_id
            ).first()
            
            if not company:
                return {"error": "Company not found"}
            
            # Get latest valuation
            latest_valuation = self.db.query(Valuation).filter(
                Valuation.company_id == company_id
            ).order_by(Valuation.valuation_date.desc()).first()
            
            if not latest_valuation:
                return {"error": "No valuations found"}
            
            # Get analytics
            analytics_summary = self.analytics_service.get_company_analytics_summary(company_id)
            
            # Build report sections based on config
            report_data = {
                "report_type": "executive_summary",
                "generated_at": datetime.utcnow().isoformat(),
                "company_info": {
                    "name": company.name,
                    "industry": company.industry,
                    "stage": company.stage,
                    "employees": company.employees,
                    "revenue": company.revenue
                },
                "valuation_summary": {
                    "final_valuation": latest_valuation.final_valuation,
                    "confidence_score": latest_valuation.confidence_score,
                    "method_used": latest_valuation.method_used,
                    "valuation_date": latest_valuation.valuation_date.isoformat()
                },
                "key_metrics": analytics_summary.get('metrics', {}),
                "sections": []
            }
            
            # Add custom sections based on config
            if config.get('include_financial_analysis', True):
                report_data["sections"].append(self._build_financial_analysis_section(company, latest_valuation))
            
            if config.get('include_market_comparison', True):
                report_data["sections"].append(self._build_market_comparison_section(company_id))
            
            if config.get('include_growth_projections', True):
                report_data["sections"].append(self._build_growth_projections_section(company, latest_valuation))
            
            if config.get('include_risk_assessment', True):
                report_data["sections"].append(self._build_risk_assessment_section(company))
            
            return report_data
            
        except Exception as e:
            return {"error": f"Failed to generate report: {str(e)}"}
    
    def _build_financial_analysis_section(self, company, valuation) -> Dict:
        """Build financial analysis section"""
        return {
            "title": "Financial Analysis",
            "type": "financial",
            "data": {
                "revenue_metrics": {
                    "current_revenue": company.revenue,
                    "growth_rate": company.growth_rate,
                    "revenue_per_employee": company.revenue / company.employees if company.employees else 0
                },
                "profitability": {
                    "ebitda": company.ebitda,
                    "profit_margin": company.profit_margin,
                    "ebitda_margin": (company.ebitda / company.revenue * 100) if company.revenue else 0
                },
                "valuation_metrics": {
                    "revenue_multiple": valuation.final_valuation / company.revenue if company.revenue else 0,
                    "ebitda_multiple": valuation.final_valuation / company.ebitda if company.ebitda else 0
                }
            }
        }
    
    def _build_market_comparison_section(self, company_id: int) -> Dict:
        """Build market comparison section"""
        # Get industry benchmarks
        benchmarks = self.db.query(MarketBenchmarks).filter(
            MarketBenchmarks.industry == 'UCaaS'
        ).all()
        
        benchmark_data = {}
        for benchmark in benchmarks:
            benchmark_data[benchmark.metric_name] = {
                "industry_avg": benchmark.avg_value,
                "top_quartile": benchmark.p75_value,
                "top_decile": benchmark.p90_value
            }
        
        return {
            "title": "Market Comparison",
            "type": "market",
            "data": {
                "industry_benchmarks": benchmark_data,
                "market_position": "Analysis based on UCaaS industry standards",
                "competitive_landscape": {
                    "market_size": "$50B+ UCaaS market",
                    "growth_rate": "12% annual growth",
                    "key_trends": ["AI integration", "Security focus", "Remote work adoption"]
                }
            }
        }
    
    def _build_growth_projections_section(self, company, valuation) -> Dict:
        """Build growth projections section"""
        # Calculate 5-year projections
        current_revenue = company.revenue or 0
        growth_rate = (company.growth_rate or 25) / 100
        
        projections = []
        for year in range(1, 6):
            projected_revenue = current_revenue * ((1 + growth_rate) ** year)
            projections.append({
                "year": datetime.now().year + year,
                "revenue": projected_revenue,
                "valuation": projected_revenue * 12.5  # Using industry multiple
            })
        
        return {
            "title": "Growth Projections",
            "type": "projections",
            "data": {
                "assumptions": {
                    "base_revenue": current_revenue,
                    "growth_rate": company.growth_rate,
                    "revenue_multiple": 12.5
                },
                "five_year_projections": projections,
                "scenario_analysis": {
                    "conservative": projections[-1]["valuation"] * 0.8,
                    "base_case": projections[-1]["valuation"],
                    "optimistic": projections[-1]["valuation"] * 1.3
                }
            }
        }
    
    def _build_risk_assessment_section(self, company) -> Dict:
        """Build risk assessment section"""
        # Assess various risk factors
        risks = []
        
        # Market risk
        if company.stage == 'early':
            risks.append({
                "category": "Market Risk",
                "level": "Medium",
                "description": "Early-stage company with market validation needs"
            })
        
        # Financial risk
        if company.revenue and company.revenue < 1000000:
            risks.append({
                "category": "Financial Risk",
                "level": "Medium",
                "description": "Limited revenue base increases financial volatility"
            })
        
        # Competitive risk
        risks.append({
            "category": "Competitive Risk",
            "level": "Medium",
            "description": "UCaaS market has established players and new entrants"
        })
        
        return {
            "title": "Risk Assessment",
            "type": "risk",
            "data": {
                "risk_factors": risks,
                "mitigation_strategies": [
                    "Diversify customer base",
                    "Focus on unique value proposition",
                    "Maintain strong cash position",
                    "Invest in product differentiation"
                ],
                "overall_risk_rating": "Medium"
            }
        }

class ReportVisualizationService:
    """Service for creating charts and visualizations for reports"""
    
    @staticmethod
    def create_valuation_comparison_chart(valuation_data: Dict) -> str:
        """Create valuation comparison chart"""
        plt.figure(figsize=(10, 6))
        
        methods = ['DCF', 'UCaaS', 'AI', 'Comparables']
        values = [
            valuation_data.get('dcf_valuation', 0),
            valuation_data.get('ucaas_valuation', 0),
            valuation_data.get('ai_valuation', 0),
            valuation_data.get('market_comparables_value', 0)
        ]
        
        # Convert to millions
        values = [v / 1000000 for v in values]
        
        colors_list = ['#3498db', '#2ecc71', '#9b59b6', '#e74c3c']
        bars = plt.bar(methods, values, color=colors_list)
        
        plt.title('Valuation by Method ($ Millions)', fontsize=16, fontweight='bold')
        plt.ylabel('Valuation ($M)', fontsize=12)
        plt.xlabel('Valuation Method', fontsize=12)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'${value:.1f}M', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Convert to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_str
    
    @staticmethod
    def create_growth_projection_chart(projections: List[Dict]) -> str:
        """Create growth projection chart"""
        plt.figure(figsize=(12, 8))
        
        years = [p['year'] for p in projections]
        revenues = [p['revenue'] / 1000000 for p in projections]  # Convert to millions
        valuations = [p['valuation'] / 1000000 for p in projections]
        
        plt.subplot(2, 1, 1)
        plt.plot(years, revenues, marker='o', linewidth=3, color='#2ecc71')
        plt.title('Revenue Projections', fontsize=14, fontweight='bold')
        plt.ylabel('Revenue ($M)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 1, 2)
        plt.plot(years, valuations, marker='s', linewidth=3, color='#3498db')
        plt.title('Valuation Projections', fontsize=14, fontweight='bold')
        plt.ylabel('Valuation ($M)', fontsize=12)
        plt.xlabel('Year', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Convert to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_str
    
    @staticmethod
    def create_benchmark_comparison_chart(company_metrics: Dict, benchmarks: Dict) -> str:
        """Create benchmark comparison chart"""
        plt.figure(figsize=(12, 8))
        
        metrics = list(company_metrics.keys())[:5]  # Top 5 metrics
        company_values = []
        benchmark_values = []
        
        for metric in metrics:
            company_values.append(company_metrics[metric].get('value', 0))
            benchmark_values.append(company_metrics[metric].get('benchmark', 0))
        
        x = range(len(metrics))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], company_values, width, label='Company', color='#3498db')
        plt.bar([i + width/2 for i in x], benchmark_values, width, label='Industry Avg', color='#95a5a6')
        
        plt.title('Company vs Industry Benchmarks', fontsize=16, fontweight='bold')
        plt.ylabel('Metric Value', fontsize=12)
        plt.xlabel('Metrics', fontsize=12)
        plt.xticks(x, [m.replace('_', ' ').title() for m in metrics], rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Convert to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_str

@custom_reports_bp.route('/templates', methods=['GET'])
@jwt_required()
def get_report_templates():
    """Get available report templates"""
    templates = [
        {
            "id": "executive_summary",
            "name": "Executive Summary Report",
            "description": "Comprehensive overview with key metrics, valuation analysis, and strategic insights",
            "sections": [
                {"id": "company_overview", "name": "Company Overview", "required": True},
                {"id": "financial_analysis", "name": "Financial Analysis", "required": True},
                {"id": "valuation_summary", "name": "Valuation Summary", "required": True},
                {"id": "market_comparison", "name": "Market Comparison", "optional": True},
                {"id": "growth_projections", "name": "Growth Projections", "optional": True},
                {"id": "risk_assessment", "name": "Risk Assessment", "optional": True}
            ],
            "formats": ["pdf", "docx", "json"],
            "estimated_pages": "8-12 pages"
        },
        {
            "id": "investor_pitch",
            "name": "Investor Pitch Report",
            "description": "Investment-focused report with market opportunity, financial projections, and returns analysis",
            "sections": [
                {"id": "investment_highlights", "name": "Investment Highlights", "required": True},
                {"id": "market_opportunity", "name": "Market Opportunity", "required": True},
                {"id": "financial_projections", "name": "Financial Projections", "required": True},
                {"id": "valuation_analysis", "name": "Valuation Analysis", "required": True},
                {"id": "exit_strategy", "name": "Exit Strategy", "optional": True}
            ],
            "formats": ["pdf", "pptx"],
            "estimated_pages": "15-20 slides"
        },
        {
            "id": "quarterly_review",
            "name": "Quarterly Performance Review",
            "description": "Regular performance tracking with KPIs, benchmarks, and improvement recommendations",
            "sections": [
                {"id": "kpi_dashboard", "name": "KPI Dashboard", "required": True},
                {"id": "performance_vs_benchmarks", "name": "Performance vs Benchmarks", "required": True},
                {"id": "growth_metrics", "name": "Growth Metrics", "required": True},
                {"id": "recommendations", "name": "Strategic Recommendations", "optional": True}
            ],
            "formats": ["pdf", "xlsx", "json"],
            "estimated_pages": "6-8 pages"
        },
        {
            "id": "due_diligence",
            "name": "Due Diligence Report",
            "description": "Comprehensive analysis for M&A, investment, or partnership evaluation",
            "sections": [
                {"id": "business_overview", "name": "Business Overview", "required": True},
                {"id": "financial_analysis", "name": "Financial Analysis", "required": True},
                {"id": "market_analysis", "name": "Market Analysis", "required": True},
                {"id": "operational_review", "name": "Operational Review", "required": True},
                {"id": "risk_factors", "name": "Risk Factors", "required": True},
                {"id": "valuation_opinion", "name": "Valuation Opinion", "required": True}
            ],
            "formats": ["pdf", "docx"],
            "estimated_pages": "25-35 pages"
        }
    ]
    
    return jsonify({
        "templates": templates,
        "custom_options": {
            "charts_available": ["valuation_comparison", "growth_projections", "benchmark_analysis", "financial_trends"],
            "data_sources": ["company_data", "market_benchmarks", "industry_trends", "peer_analysis"],
            "export_formats": ["pdf", "docx", "xlsx", "pptx", "json"]
        }
    })

@custom_reports_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_custom_report():
    """Generate custom report based on template and configuration"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        company_id = data.get('company_id')
        template_id = data.get('template_id')
        config = data.get('config', {})
        output_format = data.get('format', 'pdf')
        
        if not company_id or not template_id:
            return jsonify({'error': 'Company ID and template ID are required'}), 400
        
        db = SessionLocal()
        report_builder = CustomReportBuilder(db)
        
        # Generate report data based on template
        if template_id == 'executive_summary':
            report_data = report_builder.generate_executive_summary_report(company_id, current_user, config)
        else:
            return jsonify({'error': f'Template {template_id} not implemented yet'}), 400
        
        if 'error' in report_data:
            return jsonify(report_data), 400
        
        # Generate visualizations if requested
        if config.get('include_charts', True):
            viz_service = ReportVisualizationService()
            
            # Add valuation comparison chart
            valuation_chart = viz_service.create_valuation_comparison_chart(report_data['valuation_summary'])
            report_data['charts'] = {'valuation_comparison': valuation_chart}
            
            # Add growth projection chart if section exists
            for section in report_data['sections']:
                if section['type'] == 'projections':
                    growth_chart = viz_service.create_growth_projection_chart(section['data']['five_year_projections'])
                    report_data['charts']['growth_projections'] = growth_chart
                    break
        
        # Generate file based on format
        if output_format == 'json':
            return jsonify(report_data)
        elif output_format == 'pdf':
            pdf_file = generate_pdf_report(report_data)
            return send_file(pdf_file, as_attachment=True, 
                           download_name=f"{report_data['company_info']['name']}_report.pdf")
        else:
            return jsonify({'error': f'Format {output_format} not supported yet'}), 400
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate report: {str(e)}'}), 500
    finally:
        db.close()

def generate_pdf_report(report_data: Dict) -> str:
    """Generate PDF report from report data"""
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_file.close()
    
    # Create PDF document
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#2c3e50')
    )
    story.append(Paragraph(f"{report_data['company_info']['name']} - Executive Summary", title_style))
    story.append(Spacer(1, 20))
    
    # Company Overview
    story.append(Paragraph("Company Overview", styles['Heading2']))
    company_info = report_data['company_info']
    overview_data = [
        ['Company Name', company_info['name']],
        ['Industry', company_info['industry']],
        ['Stage', company_info['stage']],
        ['Employees', str(company_info['employees'])],
        ['Revenue', f"${company_info['revenue']:,.0f}" if company_info['revenue'] else 'N/A']
    ]
    
    overview_table = Table(overview_data, colWidths=[2*inch, 3*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(overview_table)
    story.append(Spacer(1, 20))
    
    # Valuation Summary
    story.append(Paragraph("Valuation Summary", styles['Heading2']))
    valuation_info = report_data['valuation_summary']
    valuation_data = [
        ['Final Valuation', f"${valuation_info['final_valuation']:,.0f}"],
        ['Confidence Score', f"{valuation_info['confidence_score']}%"],
        ['Method Used', valuation_info['method_used']],
        ['Valuation Date', valuation_info['valuation_date'][:10]]
    ]
    
    valuation_table = Table(valuation_data, colWidths=[2*inch, 3*inch])
    valuation_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(valuation_table)
    
    # Add sections
    for section in report_data['sections']:
        story.append(Spacer(1, 20))
        story.append(Paragraph(section['title'], styles['Heading2']))
        
        if section['type'] == 'financial':
            # Add financial analysis content
            story.append(Paragraph("Revenue and Growth Metrics:", styles['Heading3']))
            financial_data = section['data']['revenue_metrics']
            for key, value in financial_data.items():
                story.append(Paragraph(f"• {key.replace('_', ' ').title()}: {value:,.2f}", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    
    return temp_file.name

@custom_reports_bp.route('/history/<int:company_id>', methods=['GET'])
@jwt_required()
def get_report_history(company_id):
    """Get report generation history for a company"""
    try:
        current_user = get_jwt_identity()
        
        # For now, return mock data - in production, store report history in database
        history = [
            {
                "id": 1,
                "template_id": "executive_summary",
                "template_name": "Executive Summary Report",
                "generated_at": "2024-08-07T10:30:00",
                "format": "pdf",
                "size_mb": 2.5,
                "download_url": "/api/custom-reports/download/1"
            },
            {
                "id": 2,
                "template_id": "quarterly_review",
                "template_name": "Quarterly Performance Review",
                "generated_at": "2024-08-05T14:15:00",
                "format": "xlsx",
                "size_mb": 1.2,
                "download_url": "/api/custom-reports/download/2"
            }
        ]
        
        return jsonify({
            "company_id": company_id,
            "reports": history,
            "total_reports": len(history)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get report history: {str(e)}'}), 500
