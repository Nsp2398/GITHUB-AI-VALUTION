from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.comprehensive_valuation import ComprehensiveValuation
from services.report_generator import ReportGenerator
import pandas as pd
import json

comprehensive_valuation_bp = Blueprint('comprehensive_valuation', __name__)

@comprehensive_valuation_bp.route('/api/comprehensive-valuation', methods=['POST'])
@jwt_required()
def perform_comprehensive_valuation():
    """
    Perform comprehensive valuation using all three methods:
    1. DCF Valuation
    2. UCaaS-Specific Metrics 
    3. AI-Powered Valuation
    Then select the best method with justification
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Extract financial data from request
        financial_data = {
            'company_name': data.get('company_name', 'Company'),
            'revenue': float(data.get('revenue', 0)),
            'growth_rate': float(data.get('growth_rate', 0)) / 100 if data.get('growth_rate') else 0.2,
            'ebitda_margin': float(data.get('ebitda_margin', 0)) / 100 if data.get('ebitda_margin') else 0.15,
            'discount_rate': float(data.get('discount_rate', 12)) / 100,
            'terminal_growth_rate': float(data.get('terminal_growth_rate', 3)) / 100,
            'mrr': float(data.get('mrr', 0)),
            'arpu': float(data.get('arpu', 0)),
            'customers': int(data.get('customers', 0)),
            'churn_rate': float(data.get('churn_rate', 0)) / 100 if data.get('churn_rate') else 0.05,
            'cac': float(data.get('cac', 0)),
            'gross_margin': float(data.get('gross_margin', 0)) / 100 if data.get('gross_margin') else 0.7,
            'expansion_revenue': float(data.get('expansion_revenue', 0)),
            'support_costs': float(data.get('support_costs', 10)),
            'market_position': data.get('market_position', 'average'),
            'technology_score': int(data.get('technology_score', 5)),
            'historical_revenue': data.get('historical_revenue', [])
        }
        
        # Initialize comprehensive valuation service
        valuation_service = ComprehensiveValuation()
        
        # Perform comprehensive analysis
        results = valuation_service.perform_comprehensive_valuation(financial_data)
        
        return jsonify({
            'success': True,
            'results': results,
            'message': 'Comprehensive valuation completed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to perform comprehensive valuation'
        }), 500

@comprehensive_valuation_bp.route('/api/upload-financial-data', methods=['POST'])
@jwt_required()
def upload_financial_data():
    """
    Upload and process raw financial data (Excel, CSV, or JSON)
    Automatically extract relevant UCaaS metrics and perform valuation
    """
    try:
        user_id = get_jwt_identity()
        
        # Check if file was uploaded
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return jsonify({
                    'success': False,
                    'error': 'Unsupported file format. Please upload CSV or Excel files.'
                }), 400
                
            # Extract financial metrics from uploaded data
            financial_data = extract_metrics_from_dataframe(df)
            
        elif request.get_json():
            # Handle JSON data input
            financial_data = request.get_json()
        else:
            return jsonify({
                'success': False,
                'error': 'No financial data provided'
            }), 400
        
        # Perform comprehensive valuation
        valuation_service = ComprehensiveValuation()
        results = valuation_service.perform_comprehensive_valuation(financial_data)
        
        return jsonify({
            'success': True,
            'results': results,
            'extracted_data': financial_data,
            'message': 'Financial data processed and valuation completed'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to process financial data'
        }), 500

@comprehensive_valuation_bp.route('/api/generate-comprehensive-report', methods=['POST'])
@jwt_required()
def generate_comprehensive_report():
    """
    Generate a comprehensive valuation report with all three methods
    and the recommended approach with justification
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        valuation_results = data.get('valuation_results')
        report_format = data.get('format', 'all')  # pdf, docx, txt, png, or all
        
        if not valuation_results:
            return jsonify({
                'success': False,
                'error': 'No valuation results provided'
            }), 400
        
        # Prepare comprehensive report data
        company_info = valuation_results.get('company_info', {})
        company_info['name'] = company_info.get('name', 'UCaaS Company')
        
        # Enhanced valuation data with all three methods
        valuation_data = {
            'dcf_valuation': valuation_results['valuation_methods']['dcf']['valuation'],
            'ucaas_valuation': valuation_results['valuation_methods']['ucaas_metrics']['valuation'],
            'ai_valuation': valuation_results['valuation_methods']['ai_powered']['valuation'],
            'recommended_valuation': valuation_results['recommended_valuation']['recommended_valuation'],
            'recommended_method': valuation_results['recommended_valuation']['recommended_method'],
            'confidence_level': valuation_results['recommended_valuation']['confidence_level'],
            'justification': valuation_results['recommended_valuation']['justification'],
            'valuation_range': valuation_results.get('valuation_range', {}),
            'data_quality': valuation_results['company_info']['data_quality']
        }
        
        # Market data (can be enhanced with real market data)
        market_data = {
            'market_size': 50000000000,  # $50B UCaaS market
            'market_growth': 0.15,  # 15% annual growth
            'competitive_position': company_info.get('market_position', 'average')
        }
        
        # Peer comparison data
        peer_comparison = [
            {'name': 'Industry Average', 'revenue_multiple': 8.5, 'growth_rate': 0.25},
            {'name': 'Top Quartile', 'revenue_multiple': 12.0, 'growth_rate': 0.35},
            {'name': 'Bottom Quartile', 'revenue_multiple': 5.0, 'growth_rate': 0.15}
        ]
        
        # Generate report
        report_generator = ReportGenerator()
        
        if report_format == 'all':
            file_paths = report_generator.generate_comprehensive_report_all_formats(
                company_info, valuation_data, market_data, peer_comparison
            )
        else:
            file_paths = report_generator.generate_comprehensive_report_single_format(
                company_info, valuation_data, market_data, peer_comparison, report_format
            )
        
        return jsonify({
            'success': True,
            'file_paths': file_paths,
            'message': f'Comprehensive valuation report generated in {report_format} format(s)'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to generate comprehensive report'
        }), 500

def extract_metrics_from_dataframe(df: pd.DataFrame) -> dict:
    """
    Extract UCaaS financial metrics from uploaded DataFrame
    Uses intelligent column mapping and data inference
    """
    
    # Standard column mapping
    column_mapping = {
        'revenue': ['revenue', 'total_revenue', 'annual_revenue', 'sales'],
        'mrr': ['mrr', 'monthly_recurring_revenue', 'monthly_revenue'],
        'arpu': ['arpu', 'average_revenue_per_user', 'avg_revenue_per_user'],
        'customers': ['customers', 'customer_count', 'total_customers', 'users'],
        'churn_rate': ['churn', 'churn_rate', 'monthly_churn', 'customer_churn'],
        'cac': ['cac', 'customer_acquisition_cost', 'acquisition_cost'],
        'gross_margin': ['gross_margin', 'margin', 'gross_profit_margin'],
        'growth_rate': ['growth', 'growth_rate', 'revenue_growth', 'monthly_growth'],
        'ebitda_margin': ['ebitda_margin', 'ebitda', 'operating_margin']
    }
    
    financial_data = {}
    
    # Convert column names to lowercase for matching
    df.columns = df.columns.str.lower().str.strip()
    
    # Extract metrics using column mapping
    for metric, possible_columns in column_mapping.items():
        for col in possible_columns:
            if col in df.columns:
                # Take the most recent value or average if multiple rows
                if len(df) == 1:
                    financial_data[metric] = float(df[col].iloc[0]) if pd.notna(df[col].iloc[0]) else 0
                else:
                    # For time series data, take the latest value
                    financial_data[metric] = float(df[col].iloc[-1]) if pd.notna(df[col].iloc[-1]) else 0
                break
    
    # Calculate derived metrics if base metrics are available
    if 'mrr' in financial_data and financial_data['mrr'] > 0:
        financial_data['revenue'] = financial_data.get('revenue', financial_data['mrr'] * 12)
    
    if 'customers' in financial_data and 'mrr' in financial_data and financial_data['customers'] > 0:
        financial_data['arpu'] = financial_data.get('arpu', financial_data['mrr'] / financial_data['customers'])
    
    # Extract historical revenue if multiple rows exist
    if len(df) > 1 and 'revenue' in df.columns:
        financial_data['historical_revenue'] = df['revenue'].dropna().tolist()
    
    # Set defaults for missing critical metrics
    defaults = {
        'growth_rate': 0.2,  # 20% default growth
        'gross_margin': 0.7,  # 70% default gross margin
        'churn_rate': 0.05,  # 5% default monthly churn
        'ebitda_margin': 0.15,  # 15% default EBITDA margin
        'discount_rate': 0.12,  # 12% default discount rate
        'terminal_growth_rate': 0.03,  # 3% default terminal growth
        'support_costs': 10,  # $10 default support cost per customer
        'expansion_revenue': 0,  # $0 default expansion revenue
        'technology_score': 5,  # 5/10 default technology score
        'market_position': 'average'
    }
    
    for key, value in defaults.items():
        if key not in financial_data:
            financial_data[key] = value
    
    return financial_data
