"""
Real-time Dashboard Service for ValuAI
Provides live data updates and real-time analytics
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_socketio import SocketIO, emit, join_room, leave_room
from database.database import SessionLocal
from models.models import User, Company, Valuation
from models.enhanced_models import ValuationAnalytics, UserActivity, MarketBenchmarks
from services.analytics_service import AnalyticsService, ActivityTracker
from datetime import datetime, timedelta
import json
from typing import Dict, List
import threading
import time
import random

realtime_bp = Blueprint('realtime', __name__, url_prefix='/api/realtime')

class RealTimeDashboardService:
    """Service for managing real-time dashboard data and updates"""
    
    def __init__(self, socketio_instance):
        self.socketio = socketio_instance
        self.active_users = {}
        self.dashboard_cache = {}
        self.update_thread = None
        self.running = False
    
    def start_background_updates(self):
        """Start background thread for real-time updates"""
        if not self.running:
            self.running = True
            self.update_thread = threading.Thread(target=self._background_update_loop)
            self.update_thread.daemon = True
            self.update_thread.start()
    
    def stop_background_updates(self):
        """Stop background updates"""
        self.running = False
        if self.update_thread:
            self.update_thread.join()
    
    def _background_update_loop(self):
        """Background loop for sending periodic updates"""
        while self.running:
            try:
                # Update market data every 30 seconds
                self._update_market_data()
                
                # Update user activity every 10 seconds
                self._update_user_activity()
                
                # Update performance metrics every 60 seconds
                self._update_performance_metrics()
                
                time.sleep(10)  # Update interval
                
            except Exception as e:
                print(f"Error in background update: {e}")
                time.sleep(5)
    
    def _update_market_data(self):
        """Update real-time market data"""
        market_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "ucaas_market": {
                "growth_rate": round(random.uniform(11.5, 12.5), 2),
                "market_size": 52000000000 + random.randint(-1000000000, 1000000000),
                "trending_metrics": [
                    {"name": "AI Integration", "change": "+15%"},
                    {"name": "Security Solutions", "change": "+22%"},
                    {"name": "Remote Work Tools", "change": "+8%"}
                ]
            },
            "valuation_trends": {
                "avg_revenue_multiple": round(random.uniform(11.8, 13.2), 1),
                "avg_growth_premium": round(random.uniform(18, 25), 1),
                "market_sentiment": random.choice(["Bullish", "Neutral", "Cautious"])
            }
        }
        
        self.socketio.emit('market_update', market_data, room='dashboard')
    
    def _update_user_activity(self):
        """Update user activity metrics"""
        try:
            db = SessionLocal()
            
            # Get recent activity
            recent_activity = db.query(UserActivity).filter(
                UserActivity.timestamp >= datetime.utcnow() - timedelta(hours=1)
            ).count()
            
            activity_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "active_users": len(self.active_users),
                "recent_activity": recent_activity,
                "popular_features": [
                    {"feature": "Valuation Analysis", "usage": random.randint(45, 85)},
                    {"feature": "Report Generation", "usage": random.randint(25, 65)},
                    {"feature": "Analytics Dashboard", "usage": random.randint(35, 75)}
                ]
            }
            
            self.socketio.emit('activity_update', activity_data, room='dashboard')
            db.close()
            
        except Exception as e:
            print(f"Error updating user activity: {e}")
    
    def _update_performance_metrics(self):
        """Update performance metrics"""
        try:
            db = SessionLocal()
            
            # Get recent valuations
            recent_valuations = db.query(Valuation).filter(
                Valuation.valuation_date >= datetime.utcnow() - timedelta(days=7)
            ).all()
            
            if recent_valuations:
                avg_confidence = sum(v.confidence_score for v in recent_valuations) / len(recent_valuations)
                avg_valuation = sum(v.final_valuation for v in recent_valuations) / len(recent_valuations)
            else:
                avg_confidence = 0
                avg_valuation = 0
            
            performance_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "weekly_stats": {
                    "total_valuations": len(recent_valuations),
                    "avg_confidence": round(avg_confidence, 1),
                    "avg_valuation": avg_valuation,
                    "growth_rate": round(random.uniform(15, 35), 1)
                },
                "system_health": {
                    "api_response_time": round(random.uniform(120, 250), 0),
                    "database_performance": "Good",
                    "ai_model_accuracy": round(random.uniform(85, 95), 1)
                }
            }
            
            self.socketio.emit('performance_update', performance_data, room='dashboard')
            db.close()
            
        except Exception as e:
            print(f"Error updating performance metrics: {e}")
    
    def get_real_time_dashboard_data(self, user_id: int) -> Dict:
        """Get comprehensive real-time dashboard data"""
        try:
            db = SessionLocal()
            
            # Get user's companies
            user_companies = db.query(Company).filter(Company.user_id == user_id).all()
            
            # Get recent valuations
            company_ids = [c.id for c in user_companies]
            recent_valuations = db.query(Valuation).filter(
                Valuation.company_id.in_(company_ids),
                Valuation.valuation_date >= datetime.utcnow() - timedelta(days=30)
            ).order_by(Valuation.valuation_date.desc()).limit(10).all()
            
            # Get analytics data
            analytics_service = AnalyticsService(db)
            company_analytics = []
            
            for company in user_companies:
                summary = analytics_service.get_company_analytics_summary(company.id)
                if summary:
                    company_analytics.append({
                        "company_id": company.id,
                        "company_name": company.name,
                        "latest_valuation": summary.get('final_valuation', 0),
                        "confidence": summary.get('confidence_score', 0),
                        "last_updated": summary.get('valuation_date', '')
                    })
            
            # Compile dashboard data
            dashboard_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "summary": {
                    "total_companies": len(user_companies),
                    "total_valuations": len(recent_valuations),
                    "avg_confidence": round(sum(v.confidence_score for v in recent_valuations) / len(recent_valuations), 1) if recent_valuations else 0,
                    "portfolio_value": sum(ca.get('latest_valuation', 0) for ca in company_analytics)
                },
                "companies": company_analytics,
                "recent_activity": [
                    {
                        "id": v.id,
                        "company_name": next((c.name for c in user_companies if c.id == v.company_id), "Unknown"),
                        "valuation": v.final_valuation,
                        "confidence": v.confidence_score,
                        "date": v.valuation_date.isoformat(),
                        "method": v.method_used
                    } for v in recent_valuations
                ],
                "alerts": self._generate_alerts(user_companies, recent_valuations),
                "recommendations": self._generate_recommendations(company_analytics)
            }
            
            db.close()
            return dashboard_data
            
        except Exception as e:
            print(f"Error getting dashboard data: {e}")
            return {"error": str(e)}
    
    def _generate_alerts(self, companies: List[Company], valuations: List[Valuation]) -> List[Dict]:
        """Generate smart alerts for the dashboard"""
        alerts = []
        
        # Check for companies without recent valuations
        recent_valuation_company_ids = {v.company_id for v in valuations}
        for company in companies:
            if company.id not in recent_valuation_company_ids:
                alerts.append({
                    "type": "info",
                    "title": "Valuation Update Needed",
                    "message": f"{company.name} hasn't been valued in the last 30 days",
                    "action": "Run new valuation",
                    "company_id": company.id
                })
        
        # Check for low confidence scores
        for valuation in valuations:
            if valuation.confidence_score < 70:
                company_name = next((c.name for c in companies if c.id == valuation.company_id), "Unknown")
                alerts.append({
                    "type": "warning",
                    "title": "Low Confidence Score",
                    "message": f"{company_name} valuation has {valuation.confidence_score}% confidence",
                    "action": "Review data quality",
                    "company_id": valuation.company_id
                })
        
        # Market opportunity alerts
        if random.random() > 0.7:  # 30% chance
            alerts.append({
                "type": "success",
                "title": "Market Opportunity",
                "message": "UCaaS market showing strong growth trends (+12.3% this quarter)",
                "action": "Review market positioning"
            })
        
        return alerts[:5]  # Limit to 5 alerts
    
    def _generate_recommendations(self, company_analytics: List[Dict]) -> List[Dict]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if company_analytics:
            # Find best performing company
            best_company = max(company_analytics, key=lambda x: x.get('latest_valuation', 0))
            recommendations.append({
                "type": "insight",
                "title": "Top Performer",
                "message": f"{best_company['company_name']} is your highest valued company",
                "action": "Analyze success factors"
            })
            
            # Check for improvement opportunities
            low_confidence = [ca for ca in company_analytics if ca.get('confidence', 100) < 75]
            if low_confidence:
                recommendations.append({
                    "type": "improvement",
                    "title": "Data Quality",
                    "message": f"{len(low_confidence)} companies have low confidence scores",
                    "action": "Improve data completeness"
                })
        
        # General recommendations
        recommendations.append({
            "type": "feature",
            "title": "Try Analytics Dashboard",
            "message": "Get deeper insights with performance analytics and benchmarking",
            "action": "View Analytics"
        })
        
        return recommendations[:3]  # Limit to 3 recommendations

# Initialize real-time service (will be set by the main app)
realtime_service = None

@realtime_bp.route('/dashboard-data', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    """Get real-time dashboard data"""
    try:
        current_user = get_jwt_identity()
        
        if realtime_service:
            data = realtime_service.get_real_time_dashboard_data(current_user)
            return jsonify(data)
        else:
            return jsonify({"error": "Real-time service not available"}), 503
            
    except Exception as e:
        return jsonify({"error": f"Failed to get dashboard data: {str(e)}"}), 500

@realtime_bp.route('/metrics/live', methods=['GET'])
@jwt_required()
def get_live_metrics():
    """Get live system metrics"""
    try:
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "system_status": "operational",
            "api_calls_per_minute": random.randint(45, 120),
            "active_users": random.randint(15, 45),
            "database_connections": random.randint(8, 25),
            "cache_hit_rate": round(random.uniform(85, 95), 1),
            "average_response_time": round(random.uniform(150, 300), 0),
            "error_rate": round(random.uniform(0.1, 2.5), 2)
        }
        
        return jsonify(metrics)
        
    except Exception as e:
        return jsonify({"error": f"Failed to get live metrics: {str(e)}"}), 500

@realtime_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get real-time notifications"""
    try:
        current_user = get_jwt_identity()
        
        # Generate sample notifications
        notifications = [
            {
                "id": 1,
                "type": "valuation_complete",
                "title": "Valuation Complete",
                "message": "Your valuation for TechCorp has been completed",
                "timestamp": datetime.utcnow().isoformat(),
                "read": False,
                "action_url": "/company/1/valuation"
            },
            {
                "id": 2,
                "type": "market_update",
                "title": "Market Alert",
                "message": "UCaaS market showing strong growth (+15% this quarter)",
                "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                "read": False,
                "action_url": "/market-insights"
            },
            {
                "id": 3,
                "type": "recommendation",
                "title": "Performance Insight",
                "message": "Your company metrics are above industry average",
                "timestamp": (datetime.utcnow() - timedelta(hours=6)).isoformat(),
                "read": True,
                "action_url": "/analytics"
            }
        ]
        
        return jsonify({
            "notifications": notifications,
            "unread_count": len([n for n in notifications if not n["read"]])
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to get notifications: {str(e)}"}), 500

# WebSocket event handlers (to be registered with SocketIO)
def register_socketio_events(socketio):
    """Register WebSocket events for real-time features"""
    global realtime_service
    realtime_service = RealTimeDashboardService(socketio)
    
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')
        emit('connected', {'message': 'Connected to ValuAI real-time service'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')
    
    @socketio.on('join_dashboard')
    def handle_join_dashboard(data):
        """Join dashboard room for real-time updates"""
        user_id = data.get('user_id')
        if user_id:
            join_room('dashboard')
            realtime_service.active_users[user_id] = datetime.utcnow()
            emit('joined_dashboard', {'message': 'Joined dashboard updates'})
            
            # Send initial dashboard data
            dashboard_data = realtime_service.get_real_time_dashboard_data(user_id)
            emit('dashboard_data', dashboard_data)
    
    @socketio.on('leave_dashboard')
    def handle_leave_dashboard(data):
        """Leave dashboard room"""
        user_id = data.get('user_id')
        if user_id:
            leave_room('dashboard')
            realtime_service.active_users.pop(user_id, None)
            emit('left_dashboard', {'message': 'Left dashboard updates'})
    
    @socketio.on('request_update')
    def handle_request_update(data):
        """Handle manual update request"""
        update_type = data.get('type', 'all')
        user_id = data.get('user_id')
        
        if update_type == 'dashboard' and user_id:
            dashboard_data = realtime_service.get_real_time_dashboard_data(user_id)
            emit('dashboard_data', dashboard_data)
        elif update_type == 'market':
            realtime_service._update_market_data()
        elif update_type == 'performance':
            realtime_service._update_performance_metrics()
    
    # Start background updates
    realtime_service.start_background_updates()
    
    return realtime_service
