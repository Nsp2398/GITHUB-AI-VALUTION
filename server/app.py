from flask import Flask, request, jsonify
from flask_cors import CORS
from database.database import engine, get_db, SessionLocal
from models.models import Base, Company, Valuation, User
from services.valuation import DCFCalculator, UCaaSMetrics
from services.ai_service import ValuationAI
from routes.reports import reports_bp
from routes.files import files_bp
from routes.auth import auth_bp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Register blueprints
app.register_blueprint(reports_bp, url_prefix='/api/reports')
app.register_blueprint(files_bp, url_prefix='/api/files')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize services
ai_service = ValuationAI()
ucaas_metrics = UCaaSMetrics()

@app.route('/')
def root():
    return jsonify({
        "message": "ValuAI Backend API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "companies": "/api/companies",
            "dcf_calculation": "/api/valuations/dcf",
            "ucaas_metrics": "/api/valuations/ucaas-metrics",
            "reports": "/api/reports",
            "files": "/api/files"
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Server is running"}), 200

@app.route('/api/companies', methods=['POST'])
def create_company():
    data = request.json
    db = SessionLocal()
    
    try:
        company = Company(
            name=data['name'],
            industry=data['industry'],
            description=data.get('description', ''),
            revenue=data.get('revenue', 0),
            ebitda=data.get('ebitda', 0),
            growth_rate=data.get('growth_rate', 0),
            profit_margin=data.get('profit_margin', 0),
            mrr=data.get('mrr', 0),
            arpu=data.get('arpu', 0),
            churn_rate=data.get('churn_rate', 0),
            cac=data.get('cac', 0),
            ltv=data.get('ltv', 0)
        )
        
        db.add(company)
        db.commit()
        db.refresh(company)
        
        return jsonify({"id": company.id, "message": "Company created successfully"}), 201
    
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    
    finally:
        db.close()

@app.route('/api/companies/<int:company_id>', methods=['GET'])
def get_company(company_id):
    db = SessionLocal()
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            return jsonify({"error": "Company not found"}), 404
            
        return jsonify({
            "id": company.id,
            "name": company.name,
            "industry": company.industry,
            "description": company.description,
            "revenue": company.revenue,
            "ebitda": company.ebitda,
            "growth_rate": company.growth_rate,
            "profit_margin": company.profit_margin,
            "mrr": company.mrr,
            "arpu": company.arpu,
            "churn_rate": company.churn_rate,
            "cac": company.cac,
            "ltv": company.ltv
        }), 200
    
    finally:
        db.close()

@app.route('/api/valuations/dcf', methods=['POST'])
def calculate_dcf():
    data = request.json
    
    try:
        calculator = DCFCalculator(
            revenue=data['revenue'],
            growth_rate=data['growth_rate'],
            ebitda_margin=data['ebitda_margin'],
            discount_rate=data['discount_rate'],
            terminal_growth_rate=data['terminal_growth_rate'],
            projection_years=data.get('projection_years', 5)
        )
        
        result = calculator.perform_dcf_valuation()
        
        # Get AI insights
        metrics = {
            'revenue': data['revenue'],
            'growth_rate': data['growth_rate'],
            'ebitda_margin': data['ebitda_margin'],
            'mrr': data.get('mrr'),
            'arpu': data.get('arpu'),
            'churn_rate': data.get('churn_rate'),
            'cac': data.get('cac'),
            'ltv': data.get('ltv')
        }
        
        ai_insights = ai_service.analyze_metrics(metrics)
        valuation_range = ai_service.suggest_valuation_range(
            result['enterprise_value'],
            metrics
        )
        
        return jsonify({
            "dcf_results": result,
            "ai_insights": ai_insights,
            "valuation_range": valuation_range
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/metrics/ucaas', methods=['POST'])
def calculate_ucaas_metrics():
    data = request.json
    
    try:
        ltv = ucaas_metrics.calculate_ltv(
            arpu=data['arpu'],
            gross_margin=data['gross_margin'],
            churn_rate=data['churn_rate']
        )
        
        payback_period = ucaas_metrics.calculate_payback_period(
            cac=data['cac'],
            arpu=data['arpu'],
            gross_margin=data['gross_margin']
        )
        
        efficiency_score = ucaas_metrics.calculate_efficiency_score(
            ltv=ltv,
            cac=data['cac']
        )
        
        return jsonify({
            "ltv": ltv,
            "payback_period": payback_period,
            "efficiency_score": efficiency_score
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/valuations/<int:company_id>', methods=['POST'])
def create_valuation(company_id):
    data = request.json
    db = SessionLocal()
    
    try:
        valuation = Valuation(
            company_id=company_id,
            dcf_value=data['dcf_value'],
            market_value=data.get('market_value'),
            final_value=data['final_value'],
            discount_rate=data['discount_rate'],
            terminal_growth_rate=data['terminal_growth_rate'],
            projection_years=data.get('projection_years', 5),
            ai_confidence_score=data.get('ai_confidence_score'),
            ai_recommendations=data.get('ai_recommendations')
        )
        
        db.add(valuation)
        db.commit()
        db.refresh(valuation)
        
        return jsonify({
            "id": valuation.id,
            "message": "Valuation created successfully"
        }), 201
        
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
        
    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
