from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from database.database import engine
from models.models import User, Company, Valuation

# Create database session
Session = sessionmaker(bind=engine)

multi_model_bp = Blueprint('multi_model', __name__)

class ValuationModels:
    """Multi-model valuation calculator supporting various startup and business valuation methods"""
    
    @staticmethod
    def berkus_method(data):
        """
        Berkus Method: Pre-revenue qualitative valuation
        Max valuation: $2M across 5 factors
        """
        factors = {
            'sound_idea': data.get('idea_quality', 0.5),  # 0-1 scale
            'prototype_quality': data.get('product_quality', 0.7),
            'quality_management': data.get('team_experience', 0.8),
            'strategic_relationships': data.get('partnerships', 0.6),
            'product_rollout': data.get('market_readiness', 0.5)
        }
        
        max_value_per_factor = 500000  # $500K max per factor
        total_score = sum(factors.values()) / len(factors)
        valuation = total_score * 2000000  # $2M max total
        
        return {
            'valuation': int(valuation),
            'factors': factors,
            'method': 'berkus',
            'confidence': min(95, max(60, total_score * 100))
        }
    
    @staticmethod
    def scorecard_method(data):
        """
        Scorecard Method: Compare against regional startup averages
        """
        # Regional average pre-money valuation
        regional_average = data.get('regional_average', 2000000)
        
        # Scorecard factors with multipliers
        factors = {
            'strength_of_team': data.get('team_multiplier', 1.25),
            'size_of_opportunity': data.get('market_multiplier', 1.0),
            'product_technology': data.get('product_multiplier', 1.1),
            'competitive_environment': data.get('competitive_multiplier', 0.9),
            'marketing_sales': data.get('marketing_multiplier', 1.05),
            'need_for_funding': data.get('funding_multiplier', 0.95),
            'other_factors': data.get('other_multiplier', 1.0)
        }
        
        # Calculate final multiplier
        total_multiplier = 1.0
        for factor_name, multiplier in factors.items():
            total_multiplier *= multiplier
        
        valuation = regional_average * total_multiplier
        
        return {
            'valuation': int(valuation),
            'factors': factors,
            'regional_average': regional_average,
            'total_multiplier': total_multiplier,
            'method': 'scorecard',
            'confidence': min(95, max(65, abs(1.0 - total_multiplier) * 100 + 70))
        }
    
    @staticmethod
    def risk_factor_summation(data):
        """
        Risk Factor Summation: Enhanced scorecard with specific risk adjustments
        Uses 12+ risk categories with -2 to +2 scale
        """
        base_valuation = ValuationModels.scorecard_method(data)['valuation']
        
        # Risk factors with ratings from -2 (very high risk) to +2 (very low risk/opportunity)
        risk_factors = {
            'management_risk': data.get('management_risk', 0),
            'stage_of_business': data.get('stage_risk', -1),
            'legislation_risk': data.get('legislation_risk', 0),
            'manufacturing_risk': data.get('manufacturing_risk', 0),
            'sales_marketing_risk': data.get('sales_risk', 1),
            'funding_capital_risk': data.get('funding_risk', 0),
            'competition_risk': data.get('competition_risk', -1),
            'technology_risk': data.get('technology_risk', 1),
            'litigation_risk': data.get('litigation_risk', 0),
            'international_risk': data.get('international_risk', 0),
            'reputation_risk': data.get('reputation_risk', 0),
            'potential_lucrative_exit': data.get('exit_potential', 1)
        }
        
        # Calculate total risk adjustment
        risk_sum = sum(risk_factors.values())
        risk_adjustment = risk_sum * 0.25  # 25% adjustment per risk unit
        
        adjusted_valuation = base_valuation * (1 + risk_adjustment)
        
        return {
            'valuation': int(max(0, adjusted_valuation)),
            'base_valuation': base_valuation,
            'risk_factors': risk_factors,
            'risk_sum': risk_sum,
            'risk_adjustment': risk_adjustment,
            'method': 'risk_factor_summation',
            'confidence': min(95, max(70, 80 + risk_sum * 2))
        }
    
    @staticmethod
    def venture_capital_method(data):
        """
        Venture Capital Method: ROI-based valuation from exit perspective
        """
        # Project future revenue and exit value
        current_revenue = data.get('revenue', 0)
        growth_rate = data.get('growth_rate', 0.5)  # 50% default
        years_to_exit = data.get('years_to_exit', 5)
        
        # Calculate projected revenue at exit
        if current_revenue > 0:
            projected_revenue = current_revenue * ((1 + growth_rate) ** years_to_exit)
        else:
            projected_revenue = data.get('projected_revenue_exit', 10000000)
        
        # Industry exit multiples
        revenue_multiple = data.get('exit_revenue_multiple', 15)
        projected_exit_value = projected_revenue * revenue_multiple
        
        # VC return requirements
        required_roi = data.get('required_roi', 10)  # 10x return
        investor_ownership = data.get('investor_ownership', 0.25)  # 25% equity
        
        # Calculate pre-money valuation
        post_money_valuation = projected_exit_value / required_roi
        pre_money_valuation = post_money_valuation * (1 - investor_ownership)
        
        return {
            'valuation': int(pre_money_valuation),
            'projected_revenue': projected_revenue,
            'projected_exit_value': projected_exit_value,
            'post_money_valuation': post_money_valuation,
            'required_roi': required_roi,
            'years_to_exit': years_to_exit,
            'method': 'venture_capital',
            'confidence': min(90, max(70, 85 if current_revenue > 0 else 70))
        }
    
    @staticmethod
    def dcf_method(data):
        """
        Discounted Cash Flow: Traditional financial valuation
        """
        revenue = data.get('revenue', 0)
        expenses = data.get('expenses', 0)
        growth_rate = data.get('growth_rate', 0.35)  # 35% default
        discount_rate = data.get('discount_rate', 0.12)  # 12% WACC
        terminal_growth = data.get('terminal_growth', 0.03)  # 3% perpetual growth
        projection_years = data.get('projection_years', 5)
        
        if revenue <= 0:
            return {
                'valuation': 0,
                'method': 'dcf',
                'confidence': 0,
                'note': 'DCF requires positive revenue'
            }
        
        # Calculate initial EBITDA margin
        ebitda = revenue - expenses
        ebitda_margin = ebitda / revenue if revenue > 0 else 0.3
        
        # Project cash flows
        projected_cash_flows = []
        for year in range(1, projection_years + 1):
            projected_revenue = revenue * ((1 + growth_rate) ** year)
            projected_ebitda = projected_revenue * ebitda_margin
            # Discount to present value
            pv_cash_flow = projected_ebitda / ((1 + discount_rate) ** year)
            projected_cash_flows.append(pv_cash_flow)
        
        # Calculate terminal value
        final_year_cf = projected_cash_flows[-1] * (1 + growth_rate)
        terminal_value = final_year_cf * (1 + terminal_growth) / (discount_rate - terminal_growth)
        pv_terminal_value = terminal_value / ((1 + discount_rate) ** projection_years)
        
        # Total enterprise value
        enterprise_value = sum(projected_cash_flows) + pv_terminal_value
        
        return {
            'valuation': int(enterprise_value),
            'projected_cash_flows': [int(cf) for cf in projected_cash_flows],
            'terminal_value': int(terminal_value),
            'pv_terminal_value': int(pv_terminal_value),
            'ebitda_margin': ebitda_margin,
            'discount_rate': discount_rate,
            'method': 'dcf',
            'confidence': min(95, max(80, 90 if revenue > 1000000 else 75))
        }
    
    @staticmethod
    def market_comparables(data):
        """
        Market Comparables: Valuation based on similar companies
        """
        revenue = data.get('revenue', 0)
        expenses = data.get('expenses', 0)
        customers = data.get('customers', 0)
        employees = data.get('employees', 0)
        
        # Industry multiples (can be customized based on sector)
        multiples = {
            'revenue_multiple': data.get('revenue_multiple', 12.5),
            'ebitda_multiple': data.get('ebitda_multiple', 35.0),
            'customer_multiple': data.get('customer_multiple', 4200),
            'employee_multiple': data.get('employee_multiple', 500000)
        }
        
        # Calculate valuations by different methods
        valuations = {}
        
        if revenue > 0:
            valuations['by_revenue'] = revenue * multiples['revenue_multiple']
        
        if revenue > expenses and revenue > 0:
            ebitda = revenue - expenses
            valuations['by_ebitda'] = ebitda * multiples['ebitda_multiple']
        
        if customers > 0:
            valuations['by_customers'] = customers * multiples['customer_multiple']
        
        if employees > 0:
            valuations['by_employees'] = employees * multiples['employee_multiple']
        
        # Take the maximum reasonable valuation
        final_valuation = max(valuations.values()) if valuations else 0
        
        return {
            'valuation': int(final_valuation),
            'valuations_by_metric': {k: int(v) for k, v in valuations.items()},
            'multiples_used': multiples,
            'method': 'market_comparables',
            'confidence': min(90, max(70, 85 if len(valuations) >= 2 else 70))
        }

@multi_model_bp.route('/api/valuate', methods=['POST'])
@jwt_required()
def multi_model_valuation():
    """
    Multi-model valuation endpoint with PostgreSQL integration
    Accepts method parameter and company data
    Returns valuation results using specified method or AI recommendation
    """
    session = Session()
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        method = data.get('method', 'auto')  # Default to AI recommendation
        
        # Extract company data
        company_data = {
            'revenue': float(data.get('revenue', 0)),
            'expenses': float(data.get('expenses', 0)),
            'growth_rate': float(data.get('growth_rate', 35)) / 100,  # Convert percentage
            'customers': int(data.get('customers', 0)),
            'employees': int(data.get('employees', 0)),
            'stage': data.get('stage', 'unknown'),
            'team_experience': data.get('team_experience', 'medium'),
            'product_stage': data.get('product_stage', 'development'),
            'market_size': data.get('market_size', 'medium'),
            'traction': data.get('traction', 'moderate')
        }
        
        # AI method selection if not specified
        if method == 'auto':
            method = select_best_method(company_data)
        
        # Calculate valuation using specified method
        calculator = ValuationModels()
        
        if method == 'berkus':
            result = calculator.berkus_method(company_data)
        elif method == 'scorecard':
            result = calculator.scorecard_method(company_data)
        elif method == 'risk_factor':
            result = calculator.risk_factor_summation(company_data)
        elif method == 'vc_method':
            result = calculator.venture_capital_method(company_data)
        elif method == 'dcf':
            result = calculator.dcf_method(company_data)
        elif method == 'comparables':
            result = calculator.market_comparables(company_data)
        else:
            # Default to scorecard if unknown method
            result = calculator.scorecard_method(company_data)
            result['method'] = 'scorecard_default'
        
        # Save to database
        company_name = data.get('company_name', 'Unknown Company')
        
        # Check if company exists or create new one
        company = session.query(Company).filter_by(
            user_id=current_user_id, 
            name=company_name
        ).first()
        
        if not company:
            company = Company(
                user_id=current_user_id,
                name=company_name,
                industry=data.get('industry', 'UCaaS'),
                revenue=company_data['revenue'],
                expenses=company_data['expenses'],
                growth_rate=company_data['growth_rate'],
                employees=company_data['employees'],
                stage=company_data['stage'],
                ucaas_metrics={
                    'customer_count': company_data['customers'],
                    'growth_rate': company_data['growth_rate']
                },
                valuation_inputs={
                    'team_experience': company_data['team_experience'],
                    'product_stage': company_data['product_stage'],
                    'market_size': company_data['market_size'],
                    'traction': company_data['traction']
                }
            )
            session.add(company)
            session.flush()  # Get company ID
        
        # Create valuation record
        valuation = Valuation(
            user_id=current_user_id,
            company_id=company.id,
            method_used=method,
            final_valuation=result['valuation'],
            confidence_score=result.get('confidence', 0) / 100.0,
            valuation_results=result,
            dcf_value=result['valuation'] if method == 'dcf' else None,
            ucaas_metrics_value=result['valuation'] if method in ['scorecard', 'berkus'] else None,
            ai_powered_value=result['valuation'] if method == 'auto' else None,
            ai_recommendations={
                'selected_method': method,
                'confidence': result.get('confidence', 0),
                'factors': result.get('factors', {}),
                'reasoning': f"Selected {method} method based on company stage and data quality"
            }
        )
        session.add(valuation)
        session.commit()
        
        # Add metadata
        result['timestamp'] = datetime.now().isoformat()
        result['company_name'] = company_name
        result['selected_method'] = method
        result['valuation_id'] = valuation.valuation_uuid
        result['company_id'] = company.company_uuid
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    finally:
        session.close()

@multi_model_bp.route('/api/valuate/all-methods', methods=['POST'])
@jwt_required()
def all_methods_valuation():
    """
    Calculate valuation using all available methods with PostgreSQL integration
    Returns comprehensive comparison and saves to database
    """
    session = Session()
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Extract company data
        company_data = {
            'revenue': float(data.get('revenue', 0)),
            'expenses': float(data.get('expenses', 0)),
            'growth_rate': float(data.get('growth_rate', 35)) / 100,
            'customers': int(data.get('customers', 0)),
            'employees': int(data.get('employees', 0)),
            'stage': data.get('stage', 'unknown'),
            'team_experience': data.get('team_experience', 'medium'),
            'product_stage': data.get('product_stage', 'development')
        }
        
        calculator = ValuationModels()
        
        # Calculate using all methods
        results = {
            'berkus': calculator.berkus_method(company_data),
            'scorecard': calculator.scorecard_method(company_data),
            'risk_factor': calculator.risk_factor_summation(company_data),
            'vc_method': calculator.venture_capital_method(company_data),
            'dcf': calculator.dcf_method(company_data),
            'comparables': calculator.market_comparables(company_data)
        }
        
        # AI recommendation
        recommended_method = select_best_method(company_data)
        recommended_valuation = results[recommended_method]['valuation']
        
        # Calculate valuation range
        valuations = [r['valuation'] for r in results.values() if r['valuation'] > 0]
        valuation_range = {
            'min': min(valuations) if valuations else 0,
            'max': max(valuations) if valuations else 0,
            'avg': sum(valuations) / len(valuations) if valuations else 0,
            'median': sorted(valuations)[len(valuations)//2] if valuations else 0
        }
        
        # Save comprehensive analysis to database
        company_name = data.get('company_name', 'Unknown Company')
        
        # Check if company exists or create new one
        company = session.query(Company).filter_by(
            user_id=current_user_id, 
            name=company_name
        ).first()
        
        if not company:
            company = Company(
                user_id=current_user_id,
                name=company_name,
                industry=data.get('industry', 'UCaaS'),
                revenue=company_data['revenue'],
                expenses=company_data['expenses'],
                growth_rate=company_data['growth_rate'],
                employees=company_data['employees'],
                stage=company_data['stage'],
                ucaas_metrics={
                    'customer_count': company_data['customers'],
                    'growth_rate': company_data['growth_rate']
                },
                valuation_inputs={
                    'team_experience': company_data['team_experience'],
                    'product_stage': company_data['product_stage']
                }
            )
            session.add(company)
            session.flush()
        
        # Create comprehensive valuation record
        valuation = Valuation(
            user_id=current_user_id,
            company_id=company.id,
            method_used='comprehensive_analysis',
            final_valuation=recommended_valuation,
            confidence_score=results[recommended_method].get('confidence', 0) / 100.0,
            dcf_value=results['dcf']['valuation'],
            ucaas_metrics_value=results['scorecard']['valuation'],
            ai_powered_value=recommended_valuation,
            market_comparables_value=results['comparables']['valuation'],
            valuation_results={
                'all_methods': results,
                'recommended_method': recommended_method,
                'valuation_range': valuation_range,
                'analysis_type': 'comprehensive'
            },
            ai_recommendations={
                'recommended_method': recommended_method,
                'method_reasoning': f"Selected {recommended_method} based on company characteristics",
                'confidence_distribution': {method: r.get('confidence', 0) for method, r in results.items()},
                'valuation_spread': valuation_range
            }
        )
        session.add(valuation)
        session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'results': results,
                'recommended_method': recommended_method,
                'recommended_valuation': recommended_valuation,
                'valuation_range': valuation_range,
                'timestamp': datetime.now().isoformat(),
                'company_name': company_name,
                'valuation_id': valuation.valuation_uuid,
                'company_id': company.company_uuid
            }
        })
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    finally:
        session.close()

def select_best_method(company_data):
    """
    AI-powered method selection based on company characteristics
    """
    revenue = company_data.get('revenue', 0)
    stage = company_data.get('stage', 'unknown')
    team_exp = company_data.get('team_experience', 'medium')
    product_stage = company_data.get('product_stage', 'development')
    
    # Decision logic
    if revenue == 0 and stage in ['idea', 'pre-revenue']:
        if team_exp == 'high' and product_stage == 'mvp':
            return 'scorecard'
        else:
            return 'berkus'
    elif 0 < revenue < 1000000:
        return 'risk_factor'
    elif revenue >= 1000000:
        if stage in ['growth', 'expansion']:
            return 'dcf'
        else:
            return 'comparables'
    else:
        return 'scorecard'  # Default

@multi_model_bp.route('/api/methods', methods=['GET'])
def get_available_methods():
    """
    Return information about all available valuation methods
    """
    methods = {
        'berkus': {
            'name': 'Berkus Method',
            'description': 'Pre-revenue qualitative valuation based on team, product, and market factors',
            'best_for': 'Pre-revenue startups with strong team and product concept',
            'complexity': 'Low',
            'data_requirements': ['Team experience', 'Product stage', 'Market opportunity'],
            'recommended_stages': ['Idea', 'Pre-revenue', 'MVP'],
            'max_valuation': 2000000
        },
        'scorecard': {
            'name': 'Scorecard Method',
            'description': 'Compares target business against averages of funded startups in region',
            'best_for': 'Early-stage startups with some traction and comparable market data',
            'complexity': 'Medium',
            'data_requirements': ['Market comparables', 'Team quality', 'Product development'],
            'recommended_stages': ['Pre-revenue', 'Early revenue', 'Growth']
        },
        'risk_factor': {
            'name': 'Risk Factor Summation',
            'description': 'Enhanced scorecard method with 12+ risk categories adjustment',
            'best_for': 'Startups with detailed risk assessment and market analysis',
            'complexity': 'High',
            'data_requirements': ['Risk assessment', 'Market analysis', 'Financial projections'],
            'recommended_stages': ['Early revenue', 'Growth', 'Expansion']
        },
        'vc_method': {
            'name': 'Venture Capital Method',
            'description': 'ROI-based approach calculating from projected exit scenarios',
            'best_for': 'Startups with clear exit strategy and growth projections',
            'complexity': 'High',
            'data_requirements': ['Exit projections', 'ROI targets', 'Time to exit'],
            'recommended_stages': ['Growth', 'Expansion', 'Pre-exit']
        },
        'dcf': {
            'name': 'Discounted Cash Flow',
            'description': 'Traditional financial valuation using projected cash flows',
            'best_for': 'Revenue-generating businesses with predictable cash flows',
            'complexity': 'High',
            'data_requirements': ['Revenue history', 'Cash flow projections', 'Growth rates'],
            'recommended_stages': ['Revenue', 'Growth', 'Mature']
        },
        'comparables': {
            'name': 'Market Comparables',
            'description': 'Valuation based on similar companies and market multiples',
            'best_for': 'Companies in established markets with available comparable data',
            'complexity': 'Medium',
            'data_requirements': ['Industry data', 'Comparable companies', 'Market multiples'],
            'recommended_stages': ['Revenue', 'Growth', 'Mature']
        }
    }
    
    return jsonify({
        'success': True,
        'methods': methods
    })

@multi_model_bp.route('/api/valuations/history', methods=['GET'])
@jwt_required()
def get_valuation_history():
    """
    Get user's valuation history with PostgreSQL support
    """
    session = Session()
    try:
        current_user_id = get_jwt_identity()
        
        # Get user's valuations with company info
        valuations = session.query(Valuation, Company).join(
            Company, Valuation.company_id == Company.id
        ).filter(Valuation.user_id == current_user_id).order_by(
            Valuation.valuation_date.desc()
        ).limit(50).all()
        
        history = []
        for valuation, company in valuations:
            history.append({
                'valuation_id': valuation.valuation_uuid,
                'company_id': company.company_uuid,
                'company_name': company.name,
                'industry': company.industry,
                'method_used': valuation.method_used,
                'valuation': valuation.final_valuation,
                'confidence_score': valuation.confidence_score,
                'valuation_date': valuation.valuation_date.isoformat(),
                'revenue': company.revenue,
                'stage': company.stage,
                'key_metrics': {
                    'dcf_value': valuation.dcf_value,
                    'ucaas_metrics_value': valuation.ucaas_metrics_value,
                    'ai_powered_value': valuation.ai_powered_value,
                    'market_comparables_value': valuation.market_comparables_value
                }
            })
        
        return jsonify({
            'success': True,
            'data': {
                'history': history,
                'total_valuations': len(history)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    finally:
        session.close()

@multi_model_bp.route('/api/analytics/dashboard', methods=['GET'])
@jwt_required()
def get_analytics_dashboard():
    """
    Get analytics dashboard data for user
    """
    session = Session()
    try:
        current_user_id = get_jwt_identity()
        
        # Get user's companies and valuations
        companies = session.query(Company).filter_by(user_id=current_user_id).all()
        valuations = session.query(Valuation).filter_by(user_id=current_user_id).all()
        
        # Calculate analytics
        total_companies = len(companies)
        total_valuations = len(valuations)
        
        # Average valuation by method
        method_stats = {}
        for valuation in valuations:
            method = valuation.method_used
            if method not in method_stats:
                method_stats[method] = {'count': 0, 'total_value': 0, 'avg_confidence': 0}
            method_stats[method]['count'] += 1
            method_stats[method]['total_value'] += valuation.final_valuation or 0
            method_stats[method]['avg_confidence'] += valuation.confidence_score or 0
        
        # Calculate averages
        for method in method_stats:
            count = method_stats[method]['count']
            method_stats[method]['avg_valuation'] = method_stats[method]['total_value'] / count
            method_stats[method]['avg_confidence'] = method_stats[method]['avg_confidence'] / count
        
        # Portfolio valuation
        portfolio_value = sum(v.final_valuation or 0 for v in valuations if v.final_valuation)
        
        # Industry distribution
        industry_dist = {}
        for company in companies:
            industry = company.industry or 'Unknown'
            industry_dist[industry] = industry_dist.get(industry, 0) + 1
        
        return jsonify({
            'success': True,
            'data': {
                'overview': {
                    'total_companies': total_companies,
                    'total_valuations': total_valuations,
                    'portfolio_value': portfolio_value,
                    'avg_valuation': portfolio_value / total_valuations if total_valuations > 0 else 0
                },
                'method_statistics': method_stats,
                'industry_distribution': industry_dist,
                'recent_activity': len([v for v in valuations if (datetime.now() - v.valuation_date).days <= 30])
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    finally:
        session.close()
