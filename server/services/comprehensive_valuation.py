from typing import Dict, Any, List, Tuple
import numpy as np
from datetime import datetime
import pandas as pd
from .valuation import DCFCalculator
from .ucaas_valuation import UCaaSValuation, UCaaSMetrics
from .ai_service import ValuationAI
import statistics

class ComprehensiveValuation:
    def __init__(self):
        self.ai_service = ValuationAI()
        self.valuation_results = {}
        self.data_quality_score = 0.0
        
        # 🚀 Comprehensive 2025 Industry Benchmarks & Multipliers Database
        self.industry_benchmarks = {
            'retail': {
                'gas_station': {
                    'ev_revenue_multiple': 0.8, 'ev_ebitda_multiple': 4.2, 'profit_margin_benchmark': 0.02,
                    'inventory_turnover': 12, 'risk_factor': 0.15, 'growth_rate_benchmark': 0.03,
                    'key_metrics': ['fuel_margin', 'convenience_sales_ratio', 'location_traffic'],
                    'value_drivers': ['location', 'brand_affiliation', 'environmental_compliance'],
                    'lifecycle_stage_multiplier': {'startup': 0.7, 'growth': 1.0, 'mature': 0.9, 'decline': 0.6}
                },
                'grocery_store': {
                    'ev_revenue_multiple': 0.6, 'ev_ebitda_multiple': 5.8, 'profit_margin_benchmark': 0.01,
                    'inventory_turnover': 24, 'risk_factor': 0.12, 'growth_rate_benchmark': 0.02,
                    'key_metrics': ['same_store_sales', 'private_label_penetration', 'average_ticket'],
                    'value_drivers': ['market_share', 'supply_chain_efficiency', 'digital_integration'],
                    'lifecycle_stage_multiplier': {'startup': 0.6, 'growth': 1.0, 'mature': 0.8, 'decline': 0.5}
                },
                'luxury_retail': {
                    'ev_revenue_multiple': 3.2, 'ev_ebitda_multiple': 12.5, 'profit_margin_benchmark': 0.25,
                    'inventory_turnover': 4, 'risk_factor': 0.35, 'growth_rate_benchmark': 0.08,
                    'key_metrics': ['brand_equity', 'customer_lifetime_value', 'exclusivity_index'],
                    'value_drivers': ['brand_strength', 'exclusivity', 'experiential_retail'],
                    'lifecycle_stage_multiplier': {'startup': 0.8, 'growth': 1.3, 'mature': 1.0, 'decline': 0.4}
                },
                'ecommerce_marketplace': {
                    'ev_revenue_multiple': 4.5, 'ev_ebitda_multiple': 18.2, 'profit_margin_benchmark': 0.12,
                    'inventory_turnover': 'variable', 'risk_factor': 0.32, 'growth_rate_benchmark': 0.25,
                    'key_metrics': ['gmv_growth', 'take_rate', 'customer_acquisition_cost'],
                    'value_drivers': ['network_effects', 'platform_stickiness', 'data_monetization'],
                    'lifecycle_stage_multiplier': {'startup': 1.2, 'growth': 1.5, 'mature': 0.9, 'decline': 0.3}
                }
            },
            'technology': {
                'saas_enterprise': {
                    'ev_revenue_multiple': 12.5, 'ev_ebitda_multiple': 35.0, 'profit_margin_benchmark': 0.22,
                    'risk_factor': 0.28, 'growth_rate_benchmark': 0.35, 'arr_multiple': 8.5,
                    'key_metrics': ['net_revenue_retention', 'logo_retention', 'expansion_revenue'],
                    'value_drivers': ['product_stickiness', 'enterprise_adoption', 'api_ecosystem'],
                    'lifecycle_stage_multiplier': {'startup': 1.4, 'growth': 1.8, 'mature': 1.0, 'decline': 0.4}
                },
                'ai_ml_platform': {
                    'ev_revenue_multiple': 15.8, 'ev_ebitda_multiple': 42.0, 'profit_margin_benchmark': 0.18,
                    'risk_factor': 0.45, 'growth_rate_benchmark': 0.65, 'ip_value_multiple': 2.5,
                    'key_metrics': ['model_accuracy', 'data_volume', 'training_efficiency'],
                    'value_drivers': ['proprietary_algorithms', 'data_moats', 'talent_concentration'],
                    'lifecycle_stage_multiplier': {'startup': 1.8, 'growth': 2.2, 'mature': 1.0, 'decline': 0.2}
                },
                'cybersecurity': {
                    'ev_revenue_multiple': 9.2, 'ev_ebitda_multiple': 28.5, 'profit_margin_benchmark': 0.20,
                    'risk_factor': 0.25, 'growth_rate_benchmark': 0.28, 'threat_detection_premium': 1.3,
                    'key_metrics': ['threat_detection_rate', 'false_positive_rate', 'response_time'],
                    'value_drivers': ['zero_day_protection', 'compliance_coverage', 'threat_intelligence'],
                    'lifecycle_stage_multiplier': {'startup': 1.2, 'growth': 1.6, 'mature': 1.0, 'decline': 0.5}
                },
                'fintech_payments': {
                    'ev_revenue_multiple': 6.8, 'ev_ebitda_multiple': 22.0, 'profit_margin_benchmark': 0.15,
                    'risk_factor': 0.35, 'growth_rate_benchmark': 0.40, 'transaction_volume_multiple': 0.02,
                    'key_metrics': ['transaction_volume', 'take_rate', 'processing_speed'],
                    'value_drivers': ['regulatory_compliance', 'fraud_prevention', 'integration_ease'],
                    'lifecycle_stage_multiplier': {'startup': 1.3, 'growth': 1.7, 'mature': 0.9, 'decline': 0.3}
                }
            },
            'healthcare_life_sciences': {
                'digital_health_platform': {
                    'ev_revenue_multiple': 8.5, 'ev_ebitda_multiple': 25.0, 'profit_margin_benchmark': 0.18,
                    'risk_factor': 0.30, 'growth_rate_benchmark': 0.45, 'patient_engagement_multiple': 1.8,
                    'key_metrics': ['patient_outcomes', 'provider_adoption', 'clinical_validation'],
                    'value_drivers': ['clinical_evidence', 'regulatory_approval', 'care_pathway_integration'],
                    'lifecycle_stage_multiplier': {'startup': 1.5, 'growth': 2.0, 'mature': 1.0, 'decline': 0.4}
                },
                'biotech_drug_development': {
                    'ev_revenue_multiple': 25.0, 'ev_ebitda_multiple': 'n/a', 'profit_margin_benchmark': -0.80,
                    'risk_factor': 0.85, 'growth_rate_benchmark': 'variable', 'pipeline_value_multiple': 15.0,
                    'key_metrics': ['pipeline_stage', 'trial_success_rate', 'regulatory_pathway'],
                    'value_drivers': ['ip_portfolio', 'clinical_data', 'market_exclusivity'],
                    'lifecycle_stage_multiplier': {'preclinical': 0.3, 'phase1': 0.6, 'phase2': 1.2, 'phase3': 2.5, 'approved': 4.0}
                },
                'medical_devices': {
                    'ev_revenue_multiple': 4.2, 'ev_ebitda_multiple': 16.8, 'profit_margin_benchmark': 0.25,
                    'risk_factor': 0.22, 'growth_rate_benchmark': 0.12, 'fda_approval_premium': 1.4,
                    'key_metrics': ['clinical_outcomes', 'adoption_rate', 'reimbursement_coverage'],
                    'value_drivers': ['regulatory_moats', 'clinical_superiority', 'cost_effectiveness'],
                    'lifecycle_stage_multiplier': {'development': 0.6, 'fda_review': 1.0, 'market_entry': 1.4, 'established': 1.0}
                },
                'telemedicine': {
                    'ev_revenue_multiple': 6.2, 'ev_ebitda_multiple': 20.5, 'profit_margin_benchmark': 0.15,
                    'risk_factor': 0.25, 'growth_rate_benchmark': 0.35, 'utilization_multiple': 2.2,
                    'key_metrics': ['consultation_volume', 'provider_network', 'patient_satisfaction'],
                    'value_drivers': ['provider_quality', 'technology_platform', 'insurance_coverage'],
                    'lifecycle_stage_multiplier': {'startup': 1.3, 'growth': 1.6, 'mature': 1.0, 'decline': 0.6}
                }
            },
            'financial_services': {
                'wealth_management': {
                    'ev_revenue_multiple': 3.8, 'ev_ebitda_multiple': 15.2, 'profit_margin_benchmark': 0.25,
                    'risk_factor': 0.18, 'growth_rate_benchmark': 0.08, 'aum_multiple': 0.025,
                    'key_metrics': ['assets_under_management', 'fee_compression', 'client_retention'],
                    'value_drivers': ['client_relationships', 'investment_performance', 'regulatory_compliance'],
                    'lifecycle_stage_multiplier': {'startup': 0.8, 'growth': 1.2, 'mature': 1.0, 'decline': 0.7}
                },
                'insurance_technology': {
                    'ev_revenue_multiple': 5.5, 'ev_ebitda_multiple': 18.0, 'profit_margin_benchmark': 0.12,
                    'risk_factor': 0.28, 'growth_rate_benchmark': 0.22, 'claims_efficiency_multiple': 1.5,
                    'key_metrics': ['loss_ratio', 'customer_acquisition', 'claims_processing_time'],
                    'value_drivers': ['risk_assessment_accuracy', 'customer_experience', 'regulatory_compliance'],
                    'lifecycle_stage_multiplier': {'startup': 1.1, 'growth': 1.4, 'mature': 1.0, 'decline': 0.5}
                },
                'robo_advisory': {
                    'ev_revenue_multiple': 4.2, 'ev_ebitda_multiple': 16.5, 'profit_margin_benchmark': 0.18,
                    'risk_factor': 0.32, 'growth_rate_benchmark': 0.25, 'algorithm_sophistication_premium': 1.3,
                    'key_metrics': ['algorithm_performance', 'fee_structure', 'user_engagement'],
                    'value_drivers': ['algorithmic_sophistication', 'user_experience', 'cost_efficiency'],
                    'lifecycle_stage_multiplier': {'startup': 1.2, 'growth': 1.5, 'mature': 0.9, 'decline': 0.4}
                }
            },
            'real_estate_proptech': {
                'property_management_saas': {
                    'ev_revenue_multiple': 7.2, 'ev_ebitda_multiple': 22.8, 'profit_margin_benchmark': 0.20,
                    'risk_factor': 0.22, 'growth_rate_benchmark': 0.18, 'property_unit_multiple': 150,
                    'key_metrics': ['properties_under_management', 'tenant_retention', 'operational_efficiency'],
                    'value_drivers': ['market_penetration', 'automation_level', 'tenant_experience'],
                    'lifecycle_stage_multiplier': {'startup': 1.0, 'growth': 1.3, 'mature': 1.0, 'decline': 0.6}
                },
                'real_estate_marketplace': {
                    'ev_revenue_multiple': 5.8, 'ev_ebitda_multiple': 19.2, 'profit_margin_benchmark': 0.15,
                    'risk_factor': 0.28, 'growth_rate_benchmark': 0.20, 'transaction_volume_multiple': 0.08,
                    'key_metrics': ['transaction_volume', 'market_share', 'user_engagement'],
                    'value_drivers': ['network_effects', 'data_insights', 'market_coverage'],
                    'lifecycle_stage_multiplier': {'startup': 1.1, 'growth': 1.4, 'mature': 0.9, 'decline': 0.4}
                }
            },
            'energy_utilities': {
                'renewable_energy_developer': {
                    'ev_revenue_multiple': 12.5, 'ev_ebitda_multiple': 18.0, 'profit_margin_benchmark': 0.35,
                    'risk_factor': 0.25, 'growth_rate_benchmark': 0.15, 'carbon_credit_premium': 1.2,
                    'key_metrics': ['capacity_factor', 'ppa_duration', 'development_pipeline'],
                    'value_drivers': ['regulatory_support', 'technology_efficiency', 'grid_connectivity'],
                    'lifecycle_stage_multiplier': {'development': 0.7, 'construction': 1.0, 'operational': 1.2, 'mature': 1.0}
                },
                'energy_storage': {
                    'ev_revenue_multiple': 8.5, 'ev_ebitda_multiple': 14.2, 'profit_margin_benchmark': 0.22,
                    'risk_factor': 0.35, 'growth_rate_benchmark': 0.45, 'grid_services_premium': 1.8,
                    'key_metrics': ['storage_capacity', 'cycle_efficiency', 'grid_services_revenue'],
                    'value_drivers': ['technology_advancement', 'grid_integration', 'cost_competitiveness'],
                    'lifecycle_stage_multiplier': {'pilot': 0.8, 'commercial': 1.2, 'scaled': 1.0, 'commoditized': 0.6}
                }
            },
            'education_training': {
                'edtech_platform': {
                    'ev_revenue_multiple': 6.8, 'ev_ebitda_multiple': 21.5, 'profit_margin_benchmark': 0.18,
                    'risk_factor': 0.30, 'growth_rate_benchmark': 0.28, 'student_engagement_multiple': 1.6,
                    'key_metrics': ['student_outcomes', 'course_completion', 'instructor_quality'],
                    'value_drivers': ['content_quality', 'learning_analytics', 'accreditation'],
                    'lifecycle_stage_multiplier': {'startup': 1.2, 'growth': 1.5, 'mature': 1.0, 'decline': 0.5}
                },
                'corporate_training': {
                    'ev_revenue_multiple': 4.2, 'ev_ebitda_multiple': 16.8, 'profit_margin_benchmark': 0.25,
                    'risk_factor': 0.20, 'growth_rate_benchmark': 0.15, 'enterprise_client_premium': 1.4,
                    'key_metrics': ['enterprise_clients', 'training_effectiveness', 'client_retention'],
                    'value_drivers': ['curriculum_quality', 'measurable_outcomes', 'scalability'],
                    'lifecycle_stage_multiplier': {'startup': 0.9, 'growth': 1.2, 'mature': 1.0, 'decline': 0.7}
                }
            },
            'logistics_transport': {
                'last_mile_delivery': {
                    'ev_revenue_multiple': 2.8, 'ev_ebitda_multiple': 12.5, 'profit_margin_benchmark': 0.08,
                    'risk_factor': 0.32, 'growth_rate_benchmark': 0.25, 'automation_premium': 1.5,
                    'key_metrics': ['delivery_density', 'cost_per_delivery', 'customer_satisfaction'],
                    'value_drivers': ['route_optimization', 'automation_level', 'market_coverage'],
                    'lifecycle_stage_multiplier': {'startup': 0.8, 'growth': 1.2, 'mature': 1.0, 'decline': 0.6}
                },
                'freight_technology': {
                    'ev_revenue_multiple': 4.5, 'ev_ebitda_multiple': 15.8, 'profit_margin_benchmark': 0.12,
                    'risk_factor': 0.28, 'growth_rate_benchmark': 0.20, 'network_efficiency_multiple': 1.3,
                    'key_metrics': ['load_matching_efficiency', 'carrier_network', 'shipper_retention'],
                    'value_drivers': ['network_density', 'technology_platform', 'operational_efficiency'],
                    'lifecycle_stage_multiplier': {'startup': 1.0, 'growth': 1.3, 'mature': 1.0, 'decline': 0.5}
                }
            },
            'manufacturing': {
                'advanced_manufacturing': {
                    'ev_revenue_multiple': 2.8, 'ev_ebitda_multiple': 12.5, 'profit_margin_benchmark': 0.18,
                    'risk_factor': 0.20, 'growth_rate_benchmark': 0.08, 'automation_premium': 1.8,
                    'key_metrics': ['automation_level', 'quality_metrics', 'supply_chain_resilience'],
                    'value_drivers': ['ip_portfolio', 'manufacturing_efficiency', 'customer_relationships'],
                    'lifecycle_stage_multiplier': {'startup': 0.8, 'growth': 1.1, 'mature': 1.0, 'decline': 0.7}
                },
                'pharmaceutical_manufacturing': {
                    'ev_revenue_multiple': 4.5, 'ev_ebitda_multiple': 16.2, 'profit_margin_benchmark': 0.28,
                    'risk_factor': 0.15, 'growth_rate_benchmark': 0.06, 'regulatory_compliance_premium': 1.5,
                    'key_metrics': ['regulatory_compliance', 'capacity_utilization', 'contract_duration'],
                    'value_drivers': ['regulatory_moats', 'quality_systems', 'client_relationships'],
                    'lifecycle_stage_multiplier': {'startup': 0.7, 'growth': 1.0, 'mature': 1.1, 'decline': 0.8}
                }
            }
        }
        
    def get_industry_benchmark(self, industry: str, sub_industry: str) -> Dict[str, float]:
        """Get industry-specific benchmarks for valuation with 2025 market adjustments"""
        try:
            benchmark = self.industry_benchmarks.get(industry, {}).get(sub_industry, {
                'ev_revenue_multiple': 2.0,  # Default
                'ev_ebitda_multiple': 10.0,
                'profit_margin_benchmark': 0.10,
                'risk_factor': 0.20,
                'growth_rate_benchmark': 0.05,
                'key_metrics': ['revenue_growth', 'customer_retention'],
                'value_drivers': ['market_position', 'operational_efficiency'],
                'lifecycle_stage_multiplier': {'startup': 0.8, 'growth': 1.2, 'mature': 1.0, 'decline': 0.6}
            })
            
            # Apply 2025 market adjustments
            market_adjustments = self.get_2025_market_adjustments(industry, sub_industry)
            adjusted_benchmark = benchmark.copy()
            
            # Adjust core multiples based on market conditions
            adjusted_benchmark['ev_revenue_multiple'] *= market_adjustments['revenue_multiple_adjustment']
            adjusted_benchmark['ev_ebitda_multiple'] *= market_adjustments['ebitda_multiple_adjustment']
            adjusted_benchmark['risk_factor'] += market_adjustments['risk_adjustment']
            
            return adjusted_benchmark
        except:
            return {
                'ev_revenue_multiple': 2.0, 'ev_ebitda_multiple': 10.0,
                'profit_margin_benchmark': 0.10, 'risk_factor': 0.20, 'growth_rate_benchmark': 0.05,
                'key_metrics': ['revenue_growth'], 'value_drivers': ['market_position'],
                'lifecycle_stage_multiplier': {'startup': 0.8, 'growth': 1.2, 'mature': 1.0, 'decline': 0.6}
            }
    
    def get_2025_market_adjustments(self, industry: str, sub_industry: str) -> Dict[str, float]:
        """Apply 2025 market condition adjustments to base multiples"""
        
        # Global 2025 market factors
        base_adjustments = {
            'revenue_multiple_adjustment': 0.95,  # Slight compression from 2024 highs
            'ebitda_multiple_adjustment': 0.92,   # EBITDA multiple compression
            'risk_adjustment': 0.02,              # Increased risk premium
            'growth_premium': 1.1,               # Premium for proven growth
            'profitability_premium': 1.2         # Premium for profitability
        }
        
        # Industry-specific 2025 adjustments
        industry_specific = {
            'technology': {
                'ai_ml_platform': {'revenue_multiple_adjustment': 1.25, 'ebitda_multiple_adjustment': 1.35, 'risk_adjustment': 0.05},
                'cybersecurity': {'revenue_multiple_adjustment': 1.15, 'ebitda_multiple_adjustment': 1.20, 'risk_adjustment': -0.02},
                'fintech_payments': {'revenue_multiple_adjustment': 0.85, 'ebitda_multiple_adjustment': 0.90, 'risk_adjustment': 0.08}
            },
            'healthcare_life_sciences': {
                'digital_health_platform': {'revenue_multiple_adjustment': 1.20, 'ebitda_multiple_adjustment': 1.25, 'risk_adjustment': 0.02},
                'biotech_drug_development': {'revenue_multiple_adjustment': 1.45, 'ebitda_multiple_adjustment': 1.50, 'risk_adjustment': 0.10}
            },
            'energy_utilities': {
                'renewable_energy_developer': {'revenue_multiple_adjustment': 1.30, 'ebitda_multiple_adjustment': 1.25, 'risk_adjustment': -0.05},
                'energy_storage': {'revenue_multiple_adjustment': 1.40, 'ebitda_multiple_adjustment': 1.35, 'risk_adjustment': 0.03}
            }
        }
        
        # Get specific adjustments or use base
        specific = industry_specific.get(industry, {}).get(sub_industry, {})
        
        return {
            'revenue_multiple_adjustment': specific.get('revenue_multiple_adjustment', base_adjustments['revenue_multiple_adjustment']),
            'ebitda_multiple_adjustment': specific.get('ebitda_multiple_adjustment', base_adjustments['ebitda_multiple_adjustment']),
            'risk_adjustment': specific.get('risk_adjustment', base_adjustments['risk_adjustment']),
            'growth_premium': base_adjustments['growth_premium'],
            'profitability_premium': base_adjustments['profitability_premium']
        }
    
    def calculate_hybrid_valuation(self, financial_data: Dict[str, Any], industry_benchmarks: Dict[str, Any]) -> Dict[str, Any]:
        """🔄 Advanced Hybrid Valuation Method for Mixed Business Models"""
        
        try:
            revenue = financial_data.get('revenue', 0)
            ebitda = revenue * financial_data.get('ebitda_margin', 0.15)
            
            # Detect business model mix
            business_model_weights = self.detect_business_model_mix(financial_data)
            
            # Calculate component valuations
            component_valuations = {}
            total_weighted_value = 0
            
            for model_type, weight in business_model_weights.items():
                if weight > 0:
                    component_value = self.calculate_component_valuation(
                        financial_data, industry_benchmarks, model_type
                    )
                    component_valuations[model_type] = {
                        'value': component_value,
                        'weight': weight,
                        'weighted_value': component_value * weight
                    }
                    total_weighted_value += component_value * weight
            
            # Apply sector-driven value driver premiums
            value_driver_premium = self.calculate_value_driver_premium(financial_data, industry_benchmarks)
            adjusted_valuation = total_weighted_value * value_driver_premium
            
            # Apply lifecycle stage multiplier
            lifecycle_multiplier = self.get_lifecycle_multiplier(financial_data, industry_benchmarks)
            final_valuation = adjusted_valuation * lifecycle_multiplier
            
            return {
                'method': 'Hybrid Multi-Model Valuation',
                'valuation': final_valuation,
                'confidence_score': self.calculate_hybrid_confidence(financial_data, business_model_weights),
                'component_breakdown': component_valuations,
                'value_driver_premium': value_driver_premium,
                'lifecycle_multiplier': lifecycle_multiplier,
                'business_model_mix': business_model_weights
            }
            
        except Exception as e:
            return {
                'method': 'Hybrid Multi-Model Valuation',
                'valuation': 0,
                'confidence_score': 0,
                'error': str(e)
            }
    
    def detect_business_model_mix(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """Detect and weight different business model components"""
        
        revenue = financial_data.get('revenue', 0)
        recurring_revenue = financial_data.get('mrr', 0) * 12
        transaction_volume = financial_data.get('transaction_volume', 0)
        subscription_revenue = financial_data.get('subscription_revenue', 0)
        marketplace_gmv = financial_data.get('marketplace_gmv', 0)
        
        weights = {}
        
        # SaaS/Subscription component
        if recurring_revenue > 0 or subscription_revenue > 0:
            saas_revenue = max(recurring_revenue, subscription_revenue)
            weights['saas'] = min(saas_revenue / revenue, 1.0) if revenue > 0 else 0
        
        # Transaction/Payment component
        if transaction_volume > 0:
            transaction_revenue = transaction_volume * financial_data.get('take_rate', 0.03)
            weights['transaction'] = min(transaction_revenue / revenue, 1.0) if revenue > 0 else 0
        
        # Marketplace component
        if marketplace_gmv > 0:
            marketplace_revenue = marketplace_gmv * financial_data.get('marketplace_take_rate', 0.08)
            weights['marketplace'] = min(marketplace_revenue / revenue, 1.0) if revenue > 0 else 0
        
        # Traditional service/product component (remainder)
        total_new_economy = sum(weights.values())
        weights['traditional'] = max(1.0 - total_new_economy, 0)
        
        # Normalize weights
        total_weight = sum(weights.values())
        if total_weight > 0:
            weights = {k: v / total_weight for k, v in weights.items()}
        else:
            weights = {'traditional': 1.0}
        
        return weights
    
    def calculate_component_valuation(self, financial_data: Dict[str, Any], 
                                    industry_benchmarks: Dict[str, Any], 
                                    model_type: str) -> float:
        """Calculate valuation for specific business model component"""
        
        revenue = financial_data.get('revenue', 0)
        
        multipliers = {
            'saas': industry_benchmarks.get('ev_revenue_multiple', 8.0),
            'transaction': industry_benchmarks.get('transaction_multiple', 4.5),
            'marketplace': industry_benchmarks.get('marketplace_multiple', 6.0),
            'traditional': industry_benchmarks.get('ev_revenue_multiple', 2.0)
        }
        
        return revenue * multipliers.get(model_type, 2.0)
    
    def calculate_value_driver_premium(self, financial_data: Dict[str, Any], 
                                     industry_benchmarks: Dict[str, Any]) -> float:
        """Calculate premium based on sector-specific value drivers"""
        
        value_drivers = industry_benchmarks.get('value_drivers', [])
        premium = 1.0
        
        # Technology sector value drivers
        if 'proprietary_algorithms' in value_drivers:
            ip_strength = financial_data.get('ip_portfolio_strength', 0.5)  # 0-1 scale
            premium *= (1.0 + ip_strength * 0.4)  # Up to 40% premium
        
        if 'network_effects' in value_drivers:
            network_strength = financial_data.get('network_effect_score', 0.5)  # 0-1 scale
            premium *= (1.0 + network_strength * 0.6)  # Up to 60% premium
        
        # Healthcare sector value drivers
        if 'regulatory_approval' in value_drivers:
            approval_status = financial_data.get('regulatory_approval_score', 0.5)  # 0-1 scale
            premium *= (1.0 + approval_status * 0.8)  # Up to 80% premium
        
        if 'clinical_evidence' in value_drivers:
            clinical_strength = financial_data.get('clinical_evidence_score', 0.5)  # 0-1 scale
            premium *= (1.0 + clinical_strength * 0.5)  # Up to 50% premium
        
        # Financial services value drivers
        if 'regulatory_compliance' in value_drivers:
            compliance_score = financial_data.get('regulatory_compliance_score', 0.5)  # 0-1 scale
            premium *= (1.0 + compliance_score * 0.3)  # Up to 30% premium
        
        # ESG and sustainability premiums (2025 focus)
        esg_score = financial_data.get('esg_score', 0.5)  # 0-1 scale
        premium *= (1.0 + esg_score * 0.2)  # Up to 20% ESG premium
        
        return min(premium, 3.0)  # Cap at 3x premium
    
    def get_lifecycle_multiplier(self, financial_data: Dict[str, Any], 
                               industry_benchmarks: Dict[str, Any]) -> float:
        """Get lifecycle stage multiplier"""
        
        stage = financial_data.get('lifecycle_stage', 'mature')
        multipliers = industry_benchmarks.get('lifecycle_stage_multiplier', {
            'startup': 0.8, 'growth': 1.2, 'mature': 1.0, 'decline': 0.6
        })
        
        return multipliers.get(stage, 1.0)
    
    def calculate_hybrid_confidence(self, financial_data: Dict[str, Any], 
                                  business_model_weights: Dict[str, float]) -> float:
        """Calculate confidence score for hybrid valuation"""
        
        base_confidence = 0.7
        
        # Higher confidence for diversified business models
        model_diversity = len([w for w in business_model_weights.values() if w > 0.1])
        diversity_bonus = min(model_diversity * 0.05, 0.15)
        
        # Data quality bonus
        data_completeness = self.assess_data_completeness(financial_data)
        completeness_bonus = data_completeness * 0.2
        
        return min(base_confidence + diversity_bonus + completeness_bonus, 0.95)
    
    def assess_data_completeness(self, financial_data: Dict[str, Any]) -> float:
        """Assess completeness of financial data"""
        
        critical_fields = [
            'revenue', 'growth_rate', 'ebitda_margin', 'customers',
            'mrr', 'churn_rate', 'cac'
        ]
        
        present_fields = sum(1 for field in critical_fields 
                           if field in financial_data and financial_data[field] is not None)
        
        return present_fields / len(critical_fields)
        
    def analyze_data_quality(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the quality and completeness of uploaded financial data"""
        
        quality_factors = {
            'completeness': 0.0,
            'consistency': 0.0,
            'predictability': 0.0,
            'volatility': 0.0
        }
        
        required_fields = [
            'revenue', 'growth_rate', 'ebitda_margin', 'mrr', 'arpu', 
            'churn_rate', 'cac', 'gross_margin', 'customers'
        ]
        
        # Completeness Score (0-1)
        present_fields = sum(1 for field in required_fields if field in financial_data and financial_data[field] is not None)
        quality_factors['completeness'] = present_fields / len(required_fields)
        
        # Consistency Score (check for logical relationships)
        consistency_score = 1.0
        if 'mrr' in financial_data and 'arpu' in financial_data and 'customers' in financial_data:
            expected_mrr = financial_data['arpu'] * financial_data['customers']
            actual_mrr = financial_data['mrr']
            if expected_mrr > 0:
                consistency_ratio = min(actual_mrr, expected_mrr) / max(actual_mrr, expected_mrr)
                consistency_score = min(consistency_score, consistency_ratio)
        
        quality_factors['consistency'] = consistency_score
        
        # Predictability Score (based on historical data if available)
        if 'historical_revenue' in financial_data and len(financial_data['historical_revenue']) > 2:
            revenues = financial_data['historical_revenue']
            growth_rates = [(revenues[i] - revenues[i-1]) / revenues[i-1] for i in range(1, len(revenues))]
            volatility = np.std(growth_rates) if len(growth_rates) > 1 else 0
            quality_factors['volatility'] = max(0, 1 - volatility * 2)  # Lower volatility = higher quality
            quality_factors['predictability'] = 1 - min(volatility, 0.5) * 2
        else:
            quality_factors['predictability'] = 0.5  # Neutral score for lack of historical data
            quality_factors['volatility'] = 0.5
        
        overall_score = np.mean(list(quality_factors.values()))
        
        return {
            'overall_score': overall_score,
            'factors': quality_factors,
            'missing_fields': [field for field in required_fields if field not in financial_data],
            'data_completeness_percentage': quality_factors['completeness'] * 100
        }
    
    def dcf_valuation(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """💼 1. DCF Valuation (Discounted Cash Flow) with Industry Adjustments"""
        
        try:
            # Get industry benchmarks for risk adjustment
            industry_benchmarks = financial_data.get('industry_benchmarks', {})
            industry_risk_factor = industry_benchmarks.get('risk_factor', 0.20)
            
            # Adjust discount rate based on industry risk
            base_discount_rate = financial_data.get('discount_rate', 0.12)
            industry_adjusted_discount_rate = base_discount_rate + industry_risk_factor
            
            # Use industry benchmark for terminal growth if not provided
            terminal_growth = financial_data.get('terminal_growth_rate', 
                                               industry_benchmarks.get('growth_rate_benchmark', 0.03))
            
            dcf_calculator = DCFCalculator(
                revenue=financial_data.get('revenue', 0),
                growth_rate=financial_data.get('growth_rate', 0.2),
                ebitda_margin=financial_data.get('ebitda_margin', 0.15),
                discount_rate=industry_adjusted_discount_rate,
                terminal_growth_rate=terminal_growth,
                projection_years=5
            )
            
            dcf_results = dcf_calculator.perform_dcf_valuation()
            
            # Apply industry multiple adjustment to base DCF result
            industry_multiple = industry_benchmarks.get('ev_revenue_multiple', 1.0)
            revenue = financial_data.get('revenue', 0)
            industry_adjusted_value = revenue * industry_multiple
            
            # Blend DCF result with industry multiple (70% DCF, 30% industry multiple)
            blended_valuation = (dcf_results['enterprise_value'] * 0.7) + (industry_adjusted_value * 0.3)
            
            # Calculate confidence score based on data quality and industry context
            confidence_factors = []
            
            # Historical data reliability
            if 'historical_revenue' in financial_data and len(financial_data['historical_revenue']) >= 3:
                confidence_factors.append(0.9)
            else:
                confidence_factors.append(0.6)
            
            # Growth rate vs industry benchmark
            growth_rate = financial_data.get('growth_rate', 0)
            benchmark_growth = industry_benchmarks.get('growth_rate_benchmark', 0.05)
            growth_ratio = growth_rate / benchmark_growth if benchmark_growth > 0 else 1
            if 0.5 <= growth_ratio <= 2.0:  # Within reasonable range of industry
                confidence_factors.append(0.9)
            else:
                confidence_factors.append(0.6)
            
            # EBITDA margin vs industry benchmark
            ebitda_margin = financial_data.get('ebitda_margin', 0)
            benchmark_margin = industry_benchmarks.get('profit_margin_benchmark', 0.10)
            margin_ratio = ebitda_margin / benchmark_margin if benchmark_margin > 0 else 1
            if 0.5 <= margin_ratio <= 2.0:  # Within reasonable range of industry
                confidence_factors.append(0.9)
            else:
                confidence_factors.append(0.6)
            
            confidence_score = np.mean(confidence_factors)
            
            return {
                'method': 'DCF Valuation (Industry-Adjusted)',
                'valuation': blended_valuation,
                'confidence_score': confidence_score,
                'details': {
                    **dcf_results,
                    'industry_adjusted_discount_rate': industry_adjusted_discount_rate,
                    'industry_multiple': industry_multiple,
                    'industry_adjusted_value': industry_adjusted_value,
                    'blending_ratio': '70% DCF, 30% Industry Multiple'
                },
                'strengths': [
                    'Based on fundamental cash flow analysis',
                    'Adjusted for industry-specific risk factors',
                    'Considers industry valuation multiples',
                    'Widely accepted in finance industry'
                ],
                'limitations': [
                    'Sensitive to growth rate assumptions',
                    'Requires reliable financial projections',
                    'Terminal value heavily impacts result',
                    'Industry benchmarks may not reflect unique factors'
                ],
                'applicability_score': confidence_score * 0.8 + (1 if confidence_score > 0.7 else 0.5) * 0.2
            }
            
        except Exception as e:
            return {
                'method': 'DCF Valuation',
                'valuation': 0,
                'confidence_score': 0,
                'error': str(e),
                'applicability_score': 0
            }
    
    def ucaas_metrics_valuation(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """📊 2. UCaaS-Specific Metrics Valuation"""
        
        try:
            metrics = UCaaSMetrics(
                mrr=financial_data.get('mrr', 0),
                arpu=financial_data.get('arpu', 0),
                customers=financial_data.get('customers', 0),
                churn_rate=financial_data.get('churn_rate', 0.05),
                cac=financial_data.get('cac', 0),
                gross_margin=financial_data.get('gross_margin', 0.7),
                growth_rate=financial_data.get('growth_rate', 0.2),
                expansion_revenue=financial_data.get('expansion_revenue', 0),
                support_costs=financial_data.get('support_costs', 10)
            )
            
            valuation_service = UCaaSValuation(metrics)
            ucaas_results = valuation_service.perform_valuation()
            
            # Use mid-point of ARR-based valuation
            valuation = ucaas_results['valuation_ranges']['arr_based']['mid']
            
            # Calculate confidence based on UCaaS-specific factors
            confidence_factors = []
            
            # MRR quality
            if metrics.mrr > 100000:  # >$100k MRR
                confidence_factors.append(0.9)
            elif metrics.mrr > 10000:  # >$10k MRR
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.5)
            
            # Churn rate health
            if metrics.churn_rate < 0.05:  # <5% monthly churn
                confidence_factors.append(0.9)
            elif metrics.churn_rate < 0.1:  # <10% monthly churn
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.4)
            
            # LTV/CAC ratio
            ltv_cac = ucaas_results['metrics']['efficiency']['ltv_cac_ratio']
            if ltv_cac > 3:
                confidence_factors.append(0.9)
            elif ltv_cac > 2:
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.5)
            
            # Rule of 40
            rule_of_40 = ucaas_results['benchmarks']['rule_of_40']
            if rule_of_40 > 40:
                confidence_factors.append(0.9)
            elif rule_of_40 > 20:
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.5)
            
            confidence_score = np.mean(confidence_factors)
            
            return {
                'method': 'UCaaS Metrics Valuation',
                'valuation': valuation,
                'confidence_score': confidence_score,
                'details': ucaas_results,
                'key_metrics': {
                    'ARR': ucaas_results['metrics']['arr'],
                    'MRR': metrics.mrr,
                    'LTV/CAC': ltv_cac,
                    'Rule of 40': rule_of_40,
                    'NRR': ucaas_results['metrics']['retention']['net_revenue_retention']
                },
                'strengths': [
                    'Industry-specific metrics and benchmarks',
                    'Considers recurring revenue strength',
                    'Accounts for customer retention and expansion'
                ],
                'limitations': [
                    'May overestimate based on aggressive assumptions',
                    'Less applicable for early-stage companies',
                    'Market conditions not fully considered'
                ],
                'applicability_score': confidence_score * 0.9 + (1 if metrics.mrr > 50000 else 0.6) * 0.1
            }
            
        except Exception as e:
            return {
                'method': 'UCaaS Metrics Valuation',
                'valuation': 0,
                'confidence_score': 0,
                'error': str(e),
                'applicability_score': 0
            }
    
    def ai_powered_valuation(self, financial_data: Dict[str, Any], dcf_value: float, ucaas_value: float) -> Dict[str, Any]:
        """🤖 3. AI-Powered Valuation"""
        
        try:
            # Prepare comprehensive metrics for AI analysis
            ai_metrics = {
                **financial_data,
                'dcf_valuation': dcf_value,
                'ucaas_valuation': ucaas_value
            }
            
            # Get AI analysis
            ai_analysis = self.ai_service.analyze_metrics(ai_metrics)
            ai_range = self.ai_service.suggest_valuation_range(dcf_value, financial_data)
            
            # Calculate AI-suggested valuation (blend of DCF and UCaaS with AI adjustments)
            if dcf_value > 0 and ucaas_value > 0:
                base_valuation = (dcf_value + ucaas_value) / 2
            elif dcf_value > 0:
                base_valuation = dcf_value
            elif ucaas_value > 0:
                base_valuation = ucaas_value
            else:
                base_valuation = financial_data.get('revenue', 0) * 5  # Fallback multiple
            
            # AI adjustments based on qualitative factors
            ai_adjustment_factor = 1.0
            
            # Growth narrative adjustment
            growth_rate = financial_data.get('growth_rate', 0)
            if growth_rate > 0.3:  # High growth
                ai_adjustment_factor *= 1.15
            elif growth_rate < 0.1:  # Low growth
                ai_adjustment_factor *= 0.9
            
            # Market position adjustment
            market_position = financial_data.get('market_position', 'average')
            if market_position == 'leader':
                ai_adjustment_factor *= 1.1
            elif market_position == 'challenger':
                ai_adjustment_factor *= 1.05
            elif market_position == 'niche':
                ai_adjustment_factor *= 0.95
            
            # Technology differentiation
            tech_score = financial_data.get('technology_score', 5)  # 1-10 scale
            if tech_score >= 8:
                ai_adjustment_factor *= 1.1
            elif tech_score <= 3:
                ai_adjustment_factor *= 0.9
            
            ai_valuation = base_valuation * ai_adjustment_factor
            
            # Confidence score based on data richness and AI model confidence
            confidence_factors = []
            
            # Data richness
            data_points = len([v for v in financial_data.values() if v is not None and v != 0])
            if data_points >= 10:
                confidence_factors.append(0.9)
            elif data_points >= 7:
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.5)
            
            # Consistency with other methods
            if dcf_value > 0 and ucaas_value > 0:
                variance = abs(dcf_value - ucaas_value) / max(dcf_value, ucaas_value)
                if variance < 0.2:  # <20% variance
                    confidence_factors.append(0.9)
                elif variance < 0.5:  # <50% variance
                    confidence_factors.append(0.7)
                else:
                    confidence_factors.append(0.5)
            else:
                confidence_factors.append(0.6)
            
            # AI model confidence
            ai_confidence = ai_analysis.get('confidence_score', 0.5)
            confidence_factors.append(ai_confidence)
            
            confidence_score = np.mean(confidence_factors)
            
            return {
                'method': 'AI-Powered Valuation',
                'valuation': ai_valuation,
                'confidence_score': confidence_score,
                'details': {
                    'base_valuation': base_valuation,
                    'adjustment_factor': ai_adjustment_factor,
                    'ai_analysis': ai_analysis,
                    'ai_range': ai_range
                },
                'strengths': [
                    'Considers non-numeric qualitative factors',
                    'Learns from industry patterns and trends',
                    'Adapts to market conditions and sentiment'
                ],
                'limitations': [
                    'Requires comprehensive data for accuracy',
                    'May be influenced by model training bias',
                    'Less transparent than traditional methods'
                ],
                'applicability_score': confidence_score * 0.85 + (1 if data_points >= 8 else 0.6) * 0.15
            }
            
        except Exception as e:
            return {
                'method': 'AI-Powered Valuation',
                'valuation': 0,
                'confidence_score': 0,
                'error': str(e),
                'applicability_score': 0
            }
    
    def select_best_method(self, dcf_result: Dict, ucaas_result: Dict, ai_result: Dict, hybrid_result: Dict, data_quality: Dict) -> Dict[str, Any]:
        """🧠 Best Method Selection Logic - Now supports 4 valuation methods"""
        
        methods = [
            ('DCF', dcf_result),
            ('UCaaS Metrics', ucaas_result),
            ('AI-Powered', ai_result),
            ('Hybrid Multi-Model', hybrid_result)
        ]
        
        # Calculate composite scores for each method
        method_scores = []
        
        for method_name, result in methods:
            if result['valuation'] <= 0:
                continue
                
            # Scoring factors
            confidence = result.get('confidence_score', 0)
            applicability = result.get('applicability_score', 0)
            data_quality_factor = data_quality['overall_score']
            
            # Method-specific adjustments
            if method_name == 'DCF':
                # DCF is better with more historical data and stable growth
                if data_quality['factors']['predictability'] > 0.7:
                    applicability *= 1.2
                if data_quality['factors']['completeness'] > 0.8:
                    confidence *= 1.1
                    
            elif method_name == 'UCaaS Metrics':
                # UCaaS metrics are better for established SaaS companies
                if 'mrr' in result.get('details', {}).get('metrics', {}):
                    mrr = result['details']['metrics'].get('arr', 0) / 12
                    if mrr > 50000:  # Established company
                        applicability *= 1.3
                        
            elif method_name == 'AI-Powered':
                # AI is better with richer data
                if data_quality['factors']['completeness'] > 0.8:
                    applicability *= 1.2
                if len(result.get('details', {})) > 5:  # Rich qualitative data
                    confidence *= 1.1
                    
            elif method_name == 'Hybrid Multi-Model':
                # Hybrid excels with mixed business models and complex revenue streams
                if data_quality['factors']['completeness'] > 0.7:
                    applicability *= 1.4  # Strong bonus for hybrid with good data
                if data_quality['factors']['predictability'] > 0.6:
                    confidence *= 1.2
                # Additional bonus if company shows complexity indicators
                details = result.get('details', {})
                if 'mixed_model_detected' in details and details['mixed_model_detected']:
                    applicability *= 1.3
                if 'value_driver_premiums' in details and details['value_driver_premiums']:
                    confidence *= 1.15
            
            composite_score = (
                confidence * 0.4 + 
                applicability * 0.4 + 
                data_quality_factor * 0.2
            )
            
            method_scores.append((method_name, result, composite_score))
        
        # Sort by composite score
        method_scores.sort(key=lambda x: x[2], reverse=True)
        
        if not method_scores:
            return {
                'recommended_method': 'None',
                'recommended_valuation': 0,
                'justification': 'Insufficient data quality for reliable valuation',
                'confidence_level': 'Low'
            }
        
        best_method_name, best_result, best_score = method_scores[0]
        
        # Generate justification
        justification = self._generate_justification(
            best_method_name, best_result, method_scores, data_quality
        )
        
        # Determine confidence level
        if best_score > 0.8:
            confidence_level = 'High'
        elif best_score > 0.6:
            confidence_level = 'Medium'
        else:
            confidence_level = 'Low'
        
        return {
            'recommended_method': best_method_name,
            'recommended_valuation': best_result['valuation'],
            'justification': justification,
            'confidence_level': confidence_level,
            'composite_score': best_score,
            'all_method_scores': [(name, score) for name, _, score in method_scores]
        }
    
    def _generate_justification(self, best_method: str, best_result: Dict, all_methods: List, data_quality: Dict) -> str:
        """Generate natural language justification for method selection"""
        
        valuation = best_result['valuation']
        confidence = best_result['confidence_score']
        
        base_justification = f"Based on the quality and predictability of your financial data, the {best_method} provides the most robust valuation estimate of ${valuation:,.0f}."
        
        # Method-specific justifications
        if best_method == 'DCF':
            if data_quality['factors']['predictability'] > 0.7:
                base_justification += " The company has consistent cash flows, stable growth patterns, and low volatility, making future projections reliable."
            else:
                base_justification += " Despite some data limitations, the fundamental cash flow approach provides the most conservative and defensible valuation."
                
        elif best_method == 'UCaaS Metrics':
            if 'key_metrics' in best_result:
                metrics = best_result['key_metrics']
                if metrics.get('Rule of 40', 0) > 40:
                    base_justification += f" The company shows strong UCaaS fundamentals with a Rule of 40 score of {metrics['Rule of 40']:.1f} and healthy recurring revenue metrics."
                else:
                    base_justification += " The UCaaS-specific approach captures the recurring revenue strength and customer retention dynamics most accurately."
                    
        elif best_method == 'AI-Powered':
            base_justification += " The AI model successfully integrated multiple qualitative and quantitative factors, market conditions, and industry patterns to provide the most comprehensive valuation."
        
        # Add comparison with other methods
        if len(all_methods) > 1:
            other_methods = [m for m in all_methods if m[0] != best_method]
            if other_methods:
                second_best = other_methods[0]
                variance = abs(best_result['valuation'] - second_best[1]['valuation']) / best_result['valuation']
                
                if variance < 0.15:
                    base_justification += f" The {second_best[0]} method yielded a similar result, increasing confidence in the valuation range."
                else:
                    base_justification += f" Other methods showed significant variance, but {best_method} had the highest confidence score due to data quality factors."
        
        return base_justification
    
    def perform_comprehensive_valuation(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🏆 Main method to perform all three valuations and select the best one
        """
        
        # Get industry-specific benchmarks
        industry = financial_data.get('industry', 'retail')
        sub_industry = financial_data.get('sub_industry', 'gas_station')
        industry_benchmarks = self.get_industry_benchmark(industry, sub_industry)
        
        # Add industry benchmarks to financial data for calculations
        enhanced_financial_data = financial_data.copy()
        enhanced_financial_data.update({
            'industry_benchmarks': industry_benchmarks,
            'industry_context': {
                'industry': industry,
                'sub_industry': sub_industry,
                'industry_name': industry.replace('_', ' ').title(),
                'sub_industry_name': sub_industry.replace('_', ' ').title()
            }
        })
        
        # Analyze data quality first
        data_quality = self.analyze_data_quality(enhanced_financial_data)
        
        # Perform all three valuations with industry context + hybrid method
        dcf_result = self.dcf_valuation(enhanced_financial_data)
        ucaas_result = self.ucaas_metrics_valuation(enhanced_financial_data)
        hybrid_result = self.calculate_hybrid_valuation(enhanced_financial_data, industry_benchmarks)
        ai_result = self.ai_powered_valuation(
            enhanced_financial_data, 
            dcf_result['valuation'], 
            ucaas_result['valuation'],
            hybrid_result['valuation']
        )
        
        # Select best method from 4 options
        best_method = self.select_best_method(dcf_result, ucaas_result, ai_result, hybrid_result, data_quality)
        
        # Calculate valuation range across all methods
        valid_valuations = [
            result['valuation'] for result in [dcf_result, ucaas_result, hybrid_result, ai_result] 
            if result['valuation'] > 0
        ]
        
        valuation_range = {}
        if valid_valuations:
            valuation_range = {
                'low': min(valid_valuations),
                'high': max(valid_valuations),
                'average': statistics.mean(valid_valuations),
                'median': statistics.median(valid_valuations)
            }
        
        return {
            'company_info': {
                'name': enhanced_financial_data.get('company_name', 'Company'),
                'industry': industry_benchmarks,
                'industry_context': enhanced_financial_data['industry_context'],
                'analysis_date': datetime.now().isoformat(),
                'data_quality': data_quality
            },
            'valuation_methods': {
                'dcf': dcf_result,
                'ucaas_metrics': ucaas_result,
                'hybrid_multi_model': hybrid_result,
                'ai_powered': ai_result
            },
            'recommended_valuation': best_method,
            'valuation_range': valuation_range,
            'summary': {
                'final_valuation': best_method['recommended_valuation'],
                'method_used': best_method['recommended_method'],
                'confidence_level': best_method['confidence_level'],
                'justification': best_method['justification']
            }
        }
