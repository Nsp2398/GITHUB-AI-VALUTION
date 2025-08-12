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
        """💼 1. DCF Valuation (Discounted Cash Flow)"""
        
        try:
            dcf_calculator = DCFCalculator(
                revenue=financial_data.get('revenue', 0),
                growth_rate=financial_data.get('growth_rate', 0.2),
                ebitda_margin=financial_data.get('ebitda_margin', 0.15),
                discount_rate=financial_data.get('discount_rate', 0.12),
                terminal_growth_rate=financial_data.get('terminal_growth_rate', 0.03),
                projection_years=5
            )
            
            dcf_results = dcf_calculator.perform_dcf_valuation()
            
            # Calculate confidence score based on data quality
            confidence_factors = []
            
            # Historical data reliability
            if 'historical_revenue' in financial_data and len(financial_data['historical_revenue']) >= 3:
                confidence_factors.append(0.9)
            else:
                confidence_factors.append(0.6)
            
            # Growth rate reasonableness
            growth_rate = financial_data.get('growth_rate', 0)
            if 0.05 <= growth_rate <= 0.5:  # 5-50% growth range
                confidence_factors.append(0.9)
            elif growth_rate > 0.5:
                confidence_factors.append(0.6)  # High growth less predictable
            else:
                confidence_factors.append(0.4)  # Low/negative growth concerning
            
            # EBITDA margin reasonableness
            ebitda_margin = financial_data.get('ebitda_margin', 0)
            if 0.1 <= ebitda_margin <= 0.4:  # 10-40% EBITDA margin
                confidence_factors.append(0.9)
            else:
                confidence_factors.append(0.6)
            
            confidence_score = np.mean(confidence_factors)
            
            return {
                'method': 'DCF Valuation',
                'valuation': dcf_results['enterprise_value'],
                'confidence_score': confidence_score,
                'details': dcf_results,
                'strengths': [
                    'Based on fundamental cash flow analysis',
                    'Considers time value of money',
                    'Widely accepted in finance industry'
                ],
                'limitations': [
                    'Sensitive to growth rate assumptions',
                    'Requires reliable financial projections',
                    'Terminal value heavily impacts result'
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
    
    def select_best_method(self, dcf_result: Dict, ucaas_result: Dict, ai_result: Dict, data_quality: Dict) -> Dict[str, Any]:
        """🧠 Best Method Selection Logic"""
        
        methods = [
            ('DCF', dcf_result),
            ('UCaaS Metrics', ucaas_result),
            ('AI-Powered', ai_result)
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
        
        # Analyze data quality first
        data_quality = self.analyze_data_quality(financial_data)
        
        # Perform all three valuations
        dcf_result = self.dcf_valuation(financial_data)
        ucaas_result = self.ucaas_metrics_valuation(financial_data)
        ai_result = self.ai_powered_valuation(
            financial_data, 
            dcf_result['valuation'], 
            ucaas_result['valuation']
        )
        
        # Select best method
        best_method = self.select_best_method(dcf_result, ucaas_result, ai_result, data_quality)
        
        # Calculate valuation range across all methods
        valid_valuations = [
            result['valuation'] for result in [dcf_result, ucaas_result, ai_result] 
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
                'name': financial_data.get('company_name', 'Company'),
                'analysis_date': datetime.now().isoformat(),
                'data_quality': data_quality
            },
            'valuation_methods': {
                'dcf': dcf_result,
                'ucaas_metrics': ucaas_result,
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
