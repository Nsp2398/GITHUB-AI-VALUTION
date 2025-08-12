from flask import Blueprint, jsonify, request, send_file, abort
from services.market_data import UCaaSMarketData
from services.report_generator import ReportGenerator
import os
from datetime import datetime
import zipfile
import tempfile

reports_bp = Blueprint('reports', __name__)
market_data = UCaaSMarketData()

@reports_bp.route('/generate', methods=['POST'])
def generate_report():
    try:
        data = request.json
        
        # Validate required data
        required_fields = ['company_info', 'valuation_data', 'market_data']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required data'}), 400
        
        # Get requested format
        report_format = data.get('format', 'all').lower()
        
        # Create reports directory if it doesn't exist
        reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate report
        report_gen = ReportGenerator()
        peer_comparison = data.get('peer_comparison', [])
        
        if report_format == 'all':
            # Generate all formats and return as zip
            file_paths = report_gen.generate_report_all_formats(
                company_info=data['company_info'],
                valuation_data=data['valuation_data'],
                market_data=data['market_data'],
                peer_comparison=peer_comparison,
                output_dir=reports_dir
            )
            
            # Create zip file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            company_name = data['company_info'].get('name', 'Company').replace(' ', '_')
            zip_filename = f'{company_name}_valuation_reports_{timestamp}.zip'
            zip_path = os.path.join(reports_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for format_type, file_path in file_paths.items():
                    if os.path.exists(file_path):
                        zipf.write(file_path, os.path.basename(file_path))
            
            return send_file(
                zip_path,
                mimetype='application/zip',
                as_attachment=True,
                download_name=zip_filename
            )
        
        else:
            # Generate single format
            file_paths = report_gen.generate_report_all_formats(
                company_info=data['company_info'],
                valuation_data=data['valuation_data'],
                market_data=data['market_data'],
                peer_comparison=peer_comparison,
                output_dir=reports_dir
            )
            
            if report_format not in file_paths:
                return jsonify({'error': f'Unsupported format: {report_format}'}), 400
            
            file_path = file_paths[report_format]
            
            # Determine mimetype
            mimetypes = {
                'pdf': 'application/pdf',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'txt': 'text/plain',
                'png': 'image/png'
            }
            
            if not os.path.exists(file_path):
                return jsonify({'error': 'Report generation failed'}), 500
            
            return send_file(
                file_path,
                mimetype=mimetypes.get(report_format, 'application/octet-stream'),
                as_attachment=True,
                download_name=os.path.basename(file_path)
            )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/formats', methods=['GET'])
def get_supported_formats():
    """Get list of supported report formats"""
    return jsonify({
        'formats': [
            {'key': 'pdf', 'name': 'PDF Document', 'description': 'Professional PDF report'},
            {'key': 'docx', 'name': 'Word Document', 'description': 'Editable Word document'},
            {'key': 'txt', 'name': 'Text File', 'description': 'Plain text report'},
            {'key': 'png', 'name': 'Image Report', 'description': 'Visual chart-based report'},
            {'key': 'all', 'name': 'All Formats', 'description': 'Download all formats in a ZIP file'}
        ]
    })
