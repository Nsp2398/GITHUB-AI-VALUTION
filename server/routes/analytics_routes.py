"""
Enhanced Analytics API Routes for ValuAI
Provides advanced analytics, benchmarking, and insights
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.database import SessionLocal
from services.analytics_service import AnalyticsService, BenchmarkingService, ActivityTracker
from models.models import User, Company, Valuation
from models.enhanced_models import ValuationAnalytics, MarketBenchmarks

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@analytics_bp.route('/company/<int:company_id>/summary', methods=['GET'])
@jwt_required()
def get_company_analytics_summary(company_id):
    """Get comprehensive analytics summary for a company"""
    try:
        db = SessionLocal()
        current_user = get_jwt_identity()
        
        # Verify user owns the company
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.user_id == current_user
        ).first()
        
        if not company:
            return jsonify({'error': 'Company not found or access denied'}), 404
        
        analytics_service = AnalyticsService(db)
        summary = analytics_service.get_company_analytics_summary(company_id)
        
        # Add company basic info
        summary['company_name'] = company.name
        summary['industry'] = company.industry
        summary['stage'] = company.stage
        
        return jsonify(summary)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get analytics: {str(e)}'}), 500
    finally:
        db.close()

@analytics_bp.route('/benchmarks/<industry>', methods=['GET'])
@jwt_required()
def get_industry_benchmarks(industry):
    """Get all benchmarks for a specific industry"""
    try:
        db = SessionLocal()
        
        benchmarks = db.query(MarketBenchmarks).filter(
            MarketBenchmarks.industry == industry
        ).all()
        
        result = {}
        for benchmark in benchmarks:
            result[benchmark.metric_name] = {
                'average': benchmark.avg_value,
                'median': benchmark.median_value,
                'percentiles': {
                    '25th': benchmark.p25_value,
                    '75th': benchmark.p75_value,
                    '90th': benchmark.p90_value
                },
                'sample_size': benchmark.sample_size,
                'last_updated': benchmark.last_updated.isoformat()
            }
        
        return jsonify({
            'industry': industry,
            'benchmarks': result,
            'total_metrics': len(result)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to get benchmarks: {str(e)}'}), 500
    finally:
        db.close()

@analytics_bp.route('/company/<int:company_id>/performance', methods=['GET'])
@jwt_required()
def get_company_performance_analysis(company_id):
    """Get detailed performance analysis comparing company to industry benchmarks"""
    try:
        db = SessionLocal()
        current_user = get_jwt_identity()
        
        # Verify access
        company = db.query(Company).filter(
            Company.id == company_id,
            Company.user_id == current_user
        ).first()
        
        if not company:
            return jsonify({'error': 'Company not found or access denied'}), 404
        
        # Get latest valuation analytics
        latest_valuation = db.query(Valuation).filter(
            Valuation.company_id == company_id
        ).order_by(Valuation.valuation_date.desc()).first()
        
        if not latest_valuation:
            return jsonify({'error': 'No valuations found for this company'}), 404
        
        analytics = db.query(ValuationAnalytics).filter(
            ValuationAnalytics.valuation_id == latest_valuation.id
        ).all()
        
        # Get industry benchmarks
        benchmarks = db.query(MarketBenchmarks).filter(
            MarketBenchmarks.industry == company.industry or 'UCaaS'
        ).all()
        
        benchmark_dict = {b.metric_name: b for b in benchmarks}
        
        performance_analysis = {
            'company_id': company_id,
            'company_name': company.name,
            'analysis_date': latest_valuation.valuation_date.isoformat(),
            'overall_score': 0,
            'metrics': [],
            'strengths': [],
            'improvement_areas': []
        }
        
        total_percentile = 0
        metric_count = 0
        
        for analytic in analytics:
            metric_info = {
                'metric_name': analytic.metric_name,
                'company_value': analytic.metric_value,
                'industry_benchmark': analytic.industry_benchmark,
                'percentile_rank': analytic.percentile_rank,
                'performance_rating': get_performance_rating(analytic.percentile_rank)
            }
            
            # Add benchmark details if available
            if analytic.metric_name in benchmark_dict:
                benchmark = benchmark_dict[analytic.metric_name]
                metric_info['industry_stats'] = {
                    'average': benchmark.avg_value,
                    'median': benchmark.median_value,
                    'top_quartile': benchmark.p75_value,
                    'top_decile': benchmark.p90_value
                }
            
            performance_analysis['metrics'].append(metric_info)
            
            # Track strengths and areas for improvement
            if analytic.percentile_rank >= 75:
                performance_analysis['strengths'].append({
                    'metric': analytic.metric_name,
                    'percentile': analytic.percentile_rank,
                    'note': f"Top quartile performance in {analytic.metric_name.replace('_', ' ')}"
                })
            elif analytic.percentile_rank <= 25:
                performance_analysis['improvement_areas'].append({
                    'metric': analytic.metric_name,
                    'percentile': analytic.percentile_rank,
                    'recommendation': get_improvement_recommendation(analytic.metric_name, analytic.percentile_rank)
                })
            
            total_percentile += analytic.percentile_rank
            metric_count += 1
        
        # Calculate overall score
        if metric_count > 0:
            performance_analysis['overall_score'] = round(total_percentile / metric_count, 1)
        
        return jsonify(performance_analysis)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get performance analysis: {str(e)}'}), 500
    finally:
        db.close()

@analytics_bp.route('/user/activity', methods=['GET'])
@jwt_required()
def get_user_activity():
    """Get user activity summary"""
    try:
        db = SessionLocal()
        current_user = get_jwt_identity()
        days = request.args.get('days', 30, type=int)
        
        activity_tracker = ActivityTracker(db)
        summary = activity_tracker.get_user_activity_summary(current_user, days)
        
        return jsonify(summary)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get activity: {str(e)}'}), 500
    finally:
        db.close()

@analytics_bp.route('/market-insights', methods=['GET'])
@jwt_required()
def get_market_insights():
    """Get market insights and trends"""
    try:
        db = SessionLocal()
        
        # Get recent valuations for trend analysis
        recent_valuations = db.query(Valuation).join(Company).filter(
            Valuation.valuation_date >= db.func.date('now', '-90 days')
        ).all()
        
        # Calculate market trends
        insights = {
            'market_activity': {
                'total_valuations_90d': len(recent_valuations),
                'avg_valuation': sum(v.final_valuation for v in recent_valuations) / len(recent_valuations) if recent_valuations else 0,
                'avg_confidence': sum(v.confidence_score for v in recent_valuations) / len(recent_valuations) if recent_valuations else 0
            },
            'industry_trends': {
                'ucaas_growth': 'Strong demand in remote work solutions',
                'ai_integration': 'Increasing valuation premiums for AI-powered platforms',
                'security_focus': 'Enhanced valuations for security-first solutions'
            },
            'valuation_factors': {
                'growth_premium': 'Companies with >30% growth seeing 20% premium',
                'retention_impact': 'Low churn (<5%) adds 10-15% to valuations',
                'market_position': 'Market leaders command 25-40% premium'
            }
        }
        
        return jsonify(insights)
        
    except Exception as e:
        return jsonify({'error': f'Failed to get market insights: {str(e)}'}), 500
    finally:
        db.close()

@analytics_bp.route('/setup-benchmarks', methods=['POST'])
@jwt_required()
def setup_industry_benchmarks():
    """Initialize industry benchmarks (admin function)"""
    try:
        db = SessionLocal()
        
        benchmarking_service = BenchmarkingService(db)
        success = benchmarking_service.populate_ucaas_benchmarks()
        
        if success:
            return jsonify({'message': 'Industry benchmarks populated successfully'})
        else:
            return jsonify({'error': 'Failed to populate benchmarks'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Failed to setup benchmarks: {str(e)}'}), 500
    finally:
        db.close()

def get_performance_rating(percentile: float) -> str:
    """Convert percentile to performance rating"""
    if percentile >= 75:
        return "Excellent"
    elif percentile >= 50:
        return "Good"
    elif percentile >= 25:
        return "Average"
    else:
        return "Below Average"

def get_improvement_recommendation(metric_name: str, percentile: float) -> str:
    """Get improvement recommendations based on metric and performance"""
    recommendations = {
        'ltv_cac_ratio': 'Focus on increasing customer lifetime value through upselling and reducing churn, or optimize acquisition costs',
        'growth_rate': 'Implement growth strategies: expand market reach, improve product features, or increase marketing investment',
        'churn_rate': 'Improve customer retention through better onboarding, customer success programs, and product stickiness',
        'revenue_per_employee': 'Optimize operational efficiency through automation, better processes, or strategic hiring'
    }
    
    return recommendations.get(metric_name, 'Review industry best practices and consider strategic improvements')
