# -*- coding: utf-8 -*-
"""
UCaaS Valuation Tool - Enhanced for Web Frontend Integration

Integrated with the existing UCaaS valuation platform to provide
comprehensive business valuation capabilities through web APIs.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import requests
from dataclasses import dataclass, asdict

# Add server directory to path for imports
server_dir = Path(__file__).parent / 'server'
if str(server_dir) not in sys.path:
    sys.path.append(str(server_dir))

# Import existing valuation services
try:
    from services.valuation import DCFCalculator, UCaaSMetrics
    from services.comprehensive_valuation import ComprehensiveValuation
    from services.ai_service import ValuationAI
    SERVICES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Warning: Could not import valuation services: {e}")
    SERVICES_AVAILABLE = False

@dataclass
class CompanyData:
    """Company data structure matching frontend interface"""
    company_name: str
    industry: str = "UCaaS"
    region: str = "North America"
    ownership: str = "private"
    revenue: float = 0
    growth_rate: float = 20  # Percentage format (20 = 20%)
    ebitda_margin: float = 15  # Percentage format (15 = 15%)
    discount_rate: float = 12  # Percentage format (12 = 12%)
    terminal_growth_rate: float = 3  # Percentage format (3 = 3%)
    mrr: float = 0
    arpu: float = 0
    customers: int = 0
    churn_rate: float = 8  # Percentage format (8 = 8%)
    cac: float = 0
    ltv: float = 0
    gross_margin: float = 78  # Percentage format (78 = 78%)
    expansion_revenue: float = 0
    support_costs: float = 10  # Default support costs
    market_position: str = "competitive"
    technology_score: int = 7
    historical_revenue: List[float] = None
    customer_profile: str = ""
    product_description: str = ""
    competitor_names: List[str] = None
    preferred_valuation_method: str = ""
    # Additional frontend fields
    expenses: float = 0
    employees: int = 0
    stage: str = "growth"
    team_experience: str = "experienced"
    product_stage: str = "mature"
    market_size: str = "large"
    traction: str = "strong"

@dataclass
class ValuationResults:
    """Valuation results structure matching frontend expectations"""
    dcf_valuation: float
    ucaas_valuation: float
    ai_valuation: float
    recommended_method: str
    recommended_value: float
    confidence_score: float
    valuation_range: Dict[str, float]
    method_details: Dict[str, Any]
    summary: str
    # Additional result fields for comprehensive analysis
    berkus_valuation: float = 0
    scorecard_valuation: float = 0
    risk_factor_valuation: float = 0
    vc_method_valuation: float = 0
    comparable_valuation: float = 0
    methodology_explanation: str = ""
    risk_factors: List[str] = None
    growth_projections: Dict[str, Any] = None

class UCaaSValuationTool:
    """
    Enhanced UCaaS Valuation Tool that integrates with the existing platform
    """
    
    def __init__(self, api_base_url: str = "http://localhost:5000"):
        self.api_base_url = api_base_url
        self.comprehensive_valuator = ComprehensiveValuation() if SERVICES_AVAILABLE else None
        
    def collect_company_data_interactive(self) -> CompanyData:
        """Interactive data collection with enhanced UCaaS-specific questions"""
        print("🏢 UCaaS Company Valuation Tool")
        print("=" * 50)
        print("Please provide information about your company:")
        
        # Basic company information
        company_name = input("1. Company name: ").strip()
        industry = input("2. Industry (default: UCaaS): ").strip() or "UCaaS"
        region = input("3. Geographic region (default: North America): ").strip() or "North America"
        ownership = input("4. Ownership type (private/public/subsidiary): ").strip() or "private"
        
        # Financial metrics
        print("\n💰 Financial Information:")
        revenue = self._get_float_input("5. Annual revenue ($): ", 0)
        growth_rate = self._get_float_input("6. Annual growth rate (%, e.g., 35 for 35%): ", 20)
        ebitda_margin = self._get_float_input("7. EBITDA margin (%, e.g., 15 for 15%): ", 15)
        expenses = self._get_float_input("8. Annual expenses ($): ", revenue * 0.7 if revenue > 0 else 0)
        employees = self._get_int_input("9. Number of employees: ", 10)
        
        # UCaaS-specific metrics
        print("\n📊 UCaaS Metrics:")
        mrr = self._get_float_input("10. Monthly Recurring Revenue (MRR) ($): ", revenue / 12 if revenue > 0 else 0)
        customers = self._get_int_input("11. Number of customers: ", 100)
        arpu = mrr / customers if customers > 0 and mrr > 0 else self._get_float_input("12. Average Revenue Per User (ARPU) ($): ", 100)
        churn_rate = self._get_float_input("13. Monthly churn rate (%, e.g., 8 for 8%): ", 8)
        cac = self._get_float_input("14. Customer Acquisition Cost (CAC) ($): ", 500)
        ltv = self._get_float_input("15. Customer Lifetime Value (LTV) ($): ", arpu * 24 if arpu > 0 else 2400)
        gross_margin = self._get_float_input("16. Gross margin (%, e.g., 78 for 78%): ", 78)
        
        # Additional information
        print("\n📝 Company Details:")
        customer_profile = input("17. Describe your typical customers: ").strip()
        product_description = input("18. Describe your products/services: ").strip()
        competitor_names = [name.strip() for name in input("19. List main competitors (comma-separated): ").split(",") if name.strip()]
        preferred_method = input("20. Preferred valuation method (DCF/UCaaS/AI/leave blank for recommendation): ").strip()
        
        # Business stage and characteristics  
        print("\n🏢 Business Characteristics:")
        stage = input("21. Business stage (startup/growth/mature): ").strip() or "growth"
        team_experience = input("22. Team experience level (novice/experienced/expert): ").strip() or "experienced"
        product_stage = input("23. Product development stage (mvp/mature/advanced): ").strip() or "mature"
        market_size = input("24. Market size assessment (small/medium/large): ").strip() or "large"
        traction = input("25. Current traction (weak/moderate/strong): ").strip() or "strong"
        
        # Historical revenue data
        print("\n📈 Historical Data (optional):")
        historical_input = input("26. Historical revenue for past 3 years (comma-separated, e.g., 1000000,1200000,1500000): ").strip()
        historical_revenue = []
        if historical_input:
            try:
                historical_revenue = [float(x.strip()) for x in historical_input.split(",")]
            except ValueError:
                print("⚠️ Invalid historical revenue format, skipping...")
        
        return CompanyData(
            company_name=company_name,
            industry=industry,
            region=region,
            ownership=ownership,
            revenue=revenue,
            growth_rate=growth_rate,
            ebitda_margin=ebitda_margin,
            expenses=expenses,
            employees=employees,
            mrr=mrr,
            arpu=arpu,
            customers=customers,
            churn_rate=churn_rate,
            cac=cac,
            ltv=ltv,
            gross_margin=gross_margin,
            customer_profile=customer_profile,
            product_description=product_description,
            competitor_names=competitor_names,
            preferred_valuation_method=preferred_method,
            historical_revenue=historical_revenue,
            stage=stage,
            team_experience=team_experience,
            product_stage=product_stage,
            market_size=market_size,
            traction=traction
        )
    
    def _get_float_input(self, prompt: str, default: float) -> float:
        """Helper method to get float input with validation"""
        try:
            value = input(f"{prompt}(default: {default}): ").strip()
            return float(value) if value else default
        except ValueError:
            print(f"⚠️ Invalid input, using default: {default}")
            return default
    
    def _get_int_input(self, prompt: str, default: int) -> int:
        """Helper method to get integer input with validation"""
        try:
            value = input(f"{prompt}(default: {default}): ").strip()
            return int(value) if value else default
        except ValueError:
            print(f"⚠️ Invalid input, using default: {default}")
            return default
    
    def calculate_all_valuations(self, company_data: CompanyData) -> ValuationResults:
        """
        Calculate all valuation methods including startup methods (Berkus, Scorecard, etc.)
        This matches the frontend's comprehensive valuation approach
        """
        # Try API first
        api_results = self.calculate_valuations_api(company_data)
        if api_results:
            return api_results
        
        # Fallback to local calculations
        print("🔄 API unavailable, calculating comprehensive valuations locally...")
        
        # Calculate all available methods
        dcf_value = self._calculate_dcf_local(company_data)
        ucaas_value = self._calculate_ucaas_local(company_data)
        ai_value = self._calculate_ai_local(company_data)
        berkus_value = self._calculate_berkus_local(company_data)
        scorecard_value = self._calculate_scorecard_local(company_data)
        risk_factor_value = self._calculate_risk_factor_local(company_data)
        vc_method_value = self._calculate_vc_method_local(company_data)
        comparable_value = self._calculate_comparable_local(company_data)
        
        # Determine best method based on company characteristics
        recommended_method, recommended_value, confidence = self._select_best_method(
            company_data, {
                'dcf': dcf_value,
                'ucaas': ucaas_value,
                'ai': ai_value,
                'berkus': berkus_value,
                'scorecard': scorecard_value,
                'risk_factor': risk_factor_value,
                'vc_method': vc_method_value,
                'comparable': comparable_value
            }
        )
        
        all_values = [v for v in [dcf_value, ucaas_value, ai_value, berkus_value, 
                                  scorecard_value, risk_factor_value, vc_method_value, 
                                  comparable_value] if v > 0]
        
        return ValuationResults(
            dcf_valuation=dcf_value,
            ucaas_valuation=ucaas_value,
            ai_valuation=ai_value,
            berkus_valuation=berkus_value,
            scorecard_valuation=scorecard_value,
            risk_factor_valuation=risk_factor_value,
            vc_method_valuation=vc_method_value,
            comparable_valuation=comparable_value,
            recommended_method=recommended_method,
            recommended_value=recommended_value,
            confidence_score=confidence,
            valuation_range={
                'low': min(all_values) if all_values else 0,
                'high': max(all_values) if all_values else 0,
                'average': sum(all_values) / len(all_values) if all_values else 0
            },
            method_details={
                'dcf': {'valuation': dcf_value, 'method': 'Discounted Cash Flow'},
                'ucaas': {'valuation': ucaas_value, 'method': 'UCaaS Metrics'},
                'ai': {'valuation': ai_value, 'method': 'AI-Powered Analysis'},
                'berkus': {'valuation': berkus_value, 'method': 'Berkus Method'},
                'scorecard': {'valuation': scorecard_value, 'method': 'Scorecard Method'},
                'risk_factor': {'valuation': risk_factor_value, 'method': 'Risk Factor Summation'},
                'vc_method': {'valuation': vc_method_value, 'method': 'Venture Capital Method'},
                'comparable': {'valuation': comparable_value, 'method': 'Market Comparables'}
            },
            summary=f"Comprehensive analysis of {company_data.company_name} using 8 valuation methods. "
                   f"Recommended method: {recommended_method} with value ${recommended_value:,.0f} "
                   f"(confidence: {confidence:.0%})",
            methodology_explanation=f"Selected {recommended_method} based on company stage ({company_data.stage}), "
                                  f"revenue level (${company_data.revenue:,.0f}), and available data quality.",
            risk_factors=self._identify_risk_factors(company_data),
            growth_projections=self._calculate_growth_projections(company_data)
        )
    
    def calculate_valuations_local(self, company_data: CompanyData) -> ValuationResults:
        """Calculate valuations using local services (fallback if API unavailable)"""
        if not SERVICES_AVAILABLE:
            print("⚠️ Local valuation services not available, using simplified calculations")
            return self._simplified_valuations(company_data)
        
        try:
            # Prepare financial data for comprehensive valuation (convert percentages to decimals)
            financial_data = {
                'company_name': company_data.company_name,
                'revenue': company_data.revenue,
                'growth_rate': company_data.growth_rate / 100,  # Convert percentage to decimal
                'ebitda_margin': company_data.ebitda_margin / 100,  # Convert percentage to decimal
                'discount_rate': company_data.discount_rate / 100,  # Convert percentage to decimal
                'terminal_growth_rate': company_data.terminal_growth_rate / 100,  # Convert percentage to decimal
                'mrr': company_data.mrr,
                'arpu': company_data.arpu,
                'customers': company_data.customers,
                'churn_rate': company_data.churn_rate / 100,  # Convert percentage to decimal
                'cac': company_data.cac,
                'gross_margin': company_data.gross_margin / 100,  # Convert percentage to decimal
                'expansion_revenue': company_data.expansion_revenue,
                'support_costs': company_data.support_costs,
                'market_position': company_data.market_position,
                'technology_score': company_data.technology_score,
                'historical_revenue': company_data.historical_revenue or []
            }
            
            # Perform comprehensive valuation
            results = self.comprehensive_valuator.perform_comprehensive_valuation(financial_data)
            
            # Extract results and format for return
            dcf_result = results['valuation_methods']['dcf']
            ucaas_result = results['valuation_methods']['ucaas_metrics']
            ai_result = results['valuation_methods']['ai_powered']
            
            return ValuationResults(
                dcf_valuation=dcf_result['valuation'],
                ucaas_valuation=ucaas_result['valuation'],
                ai_valuation=ai_result['valuation'],
                recommended_method=results['recommended_valuation']['method'],
                recommended_value=results['recommended_valuation']['valuation'],
                confidence_score=results['recommended_valuation']['confidence_score'],
                valuation_range=results['valuation_range'],
                method_details={
                    'dcf': dcf_result,
                    'ucaas': ucaas_result,
                    'ai': ai_result
                },
                summary=results['summary']['explanation']
            )
            
        except Exception as e:
            print(f"⚠️ Error in local valuation: {e}")
            return self._simplified_valuations(company_data)
    
    def _calculate_dcf_local(self, company_data: CompanyData) -> float:
        """Calculate DCF valuation locally"""
        revenue = company_data.revenue
        growth_rate = company_data.growth_rate / 100
        ebitda_margin = company_data.ebitda_margin / 100
        discount_rate = company_data.discount_rate / 100
        terminal_growth = company_data.terminal_growth_rate / 100
        
        if revenue <= 0:
            return 0
        
        # Project 5 years of cash flows
        projected_fcf = []
        current_revenue = revenue
        
        for year in range(5):
            current_revenue *= (1 + growth_rate)
            ebitda = current_revenue * ebitda_margin
            fcf = ebitda * 0.8  # Simplified FCF conversion
            projected_fcf.append(fcf)
        
        # Calculate DCF value
        pv_fcf = sum(fcf / ((1 + discount_rate) ** (i + 1)) for i, fcf in enumerate(projected_fcf))
        terminal_value = projected_fcf[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
        pv_terminal = terminal_value / ((1 + discount_rate) ** 5)
        
        return pv_fcf + pv_terminal
    
    def _calculate_ucaas_local(self, company_data: CompanyData) -> float:
        """Calculate UCaaS-specific valuation"""
        if company_data.mrr > 0:
            arr = company_data.mrr * 12
            # UCaaS companies typically trade at 8-15x ARR
            multiple = 10
            if company_data.growth_rate > 50:
                multiple = 15
            elif company_data.growth_rate > 30:
                multiple = 12
            elif company_data.growth_rate < 10:
                multiple = 6
            return arr * multiple
        elif company_data.revenue > 0:
            # Revenue multiple approach
            multiple = 8
            if company_data.growth_rate > 50:
                multiple = 12
            elif company_data.growth_rate > 30:
                multiple = 10
            elif company_data.growth_rate < 10:
                multiple = 4
            return company_data.revenue * multiple
        return 0
    
    def _calculate_ai_local(self, company_data: CompanyData) -> float:
        """Calculate AI-powered valuation with adjustments"""
        dcf = self._calculate_dcf_local(company_data)
        ucaas = self._calculate_ucaas_local(company_data)
        
        if dcf == 0 and ucaas == 0:
            return 0
        
        base_value = (dcf + ucaas) / 2 if dcf > 0 and ucaas > 0 else max(dcf, ucaas)
        
        # Apply AI adjustments based on qualitative factors
        multiplier = 1.0
        
        # Growth rate adjustment
        if company_data.growth_rate > 50:
            multiplier *= 1.3
        elif company_data.growth_rate > 30:
            multiplier *= 1.2
        elif company_data.growth_rate < 10:
            multiplier *= 0.8
        
        # Market position adjustment
        if company_data.market_position == "leader":
            multiplier *= 1.2
        elif company_data.market_position == "competitive":
            multiplier *= 1.0
        else:  # challenger
            multiplier *= 0.9
        
        # Technology score adjustment
        if company_data.technology_score >= 8:
            multiplier *= 1.1
        elif company_data.technology_score <= 5:
            multiplier *= 0.9
        
        return base_value * multiplier
    
    def _calculate_berkus_local(self, company_data: CompanyData) -> float:
        """Calculate Berkus method valuation (max $2.5M)"""
        if company_data.revenue > 1000000:  # Not suitable for revenue-generating companies
            return 0
        
        base_value = 500000  # Base value per element
        total_value = 0
        
        # Sound idea (basic value)
        if company_data.product_description:
            total_value += base_value
        
        # Prototype (reduce technology/implementation risk)
        if company_data.product_stage in ["mvp", "mature", "advanced"]:
            total_value += base_value
        
        # Quality management team
        if company_data.team_experience in ["experienced", "expert"]:
            total_value += base_value
        
        # Strategic relationships (market reach)
        if company_data.market_size in ["medium", "large"]:
            total_value += base_value
        
        # Product rollout or sales
        if company_data.revenue > 0 or company_data.traction in ["moderate", "strong"]:
            total_value += base_value
        
        return min(total_value, 2500000)  # Cap at $2.5M
    
    def _calculate_scorecard_local(self, company_data: CompanyData) -> float:
        """Calculate Scorecard method valuation"""
        # Base pre-money valuation for region (simplified)
        base_valuation = 2000000  # $2M base for developed markets
        
        # Scoring factors (0.5 to 3.0 multiplier each)
        factors = {
            'team': 1.5 if company_data.team_experience == "expert" else 
                   1.2 if company_data.team_experience == "experienced" else 1.0,
            'opportunity': 1.3 if company_data.market_size == "large" else
                          1.1 if company_data.market_size == "medium" else 0.9,
            'product': 1.2 if company_data.product_stage == "advanced" else
                      1.1 if company_data.product_stage == "mature" else 1.0,
            'competition': 1.2 if company_data.market_position == "leader" else
                          1.0 if company_data.market_position == "competitive" else 0.8,
            'sales': 1.3 if company_data.traction == "strong" else
                    1.1 if company_data.traction == "moderate" else 0.8,
            'need_for_investment': 1.1,  # Moderate need
            'other': 1.0
        }
        
        # Calculate weighted average (typical weights)
        weights = {
            'team': 0.30,
            'opportunity': 0.25,
            'product': 0.15,
            'competition': 0.10,
            'sales': 0.10,
            'need_for_investment': 0.05,
            'other': 0.05
        }
        
        weighted_factor = sum(factors[key] * weights[key] for key in factors)
        return base_valuation * weighted_factor
    
    def _calculate_risk_factor_local(self, company_data: CompanyData) -> float:
        """Calculate Risk Factor Summation method"""
        base_scorecard = self._calculate_scorecard_local(company_data)
        
        # Risk adjustments (-2 to +2 each, then convert to multiplier)
        risk_score = 0
        
        # Management risk
        if company_data.team_experience == "expert":
            risk_score += 1
        elif company_data.team_experience == "novice":
            risk_score -= 1
        
        # Stage of business risk
        if company_data.stage == "mature":
            risk_score += 1
        elif company_data.stage == "startup":
            risk_score -= 1
        
        # Legislation/political risk (neutral for UCaaS)
        risk_score += 0
        
        # Manufacturing risk (low for software)
        risk_score += 1
        
        # Sales and marketing risk
        if company_data.traction == "strong":
            risk_score += 1
        elif company_data.traction == "weak":
            risk_score -= 1
        
        # Funding/capital raising risk
        if company_data.revenue > 100000:
            risk_score += 1
        else:
            risk_score -= 1
        
        # Competition risk
        if company_data.market_position == "leader":
            risk_score += 1
        elif len(company_data.competitor_names or []) > 5:
            risk_score -= 1
        
        # Technology risk
        if company_data.technology_score >= 8:
            risk_score += 1
        elif company_data.technology_score <= 4:
            risk_score -= 1
        
        # Litigation risk (assumed low for most UCaaS)
        risk_score += 0
        
        # International risk (depends on region)
        if company_data.region == "North America":
            risk_score += 0
        else:
            risk_score -= 0.5
        
        # Reputation risk
        risk_score += 0  # Neutral assumption
        
        # Convert risk score to multiplier (each point = 5% change)
        multiplier = 1 + (risk_score * 0.05)
        return base_scorecard * max(0.5, min(2.0, multiplier))  # Cap between 50% and 200%
    
    def _calculate_vc_method_local(self, company_data: CompanyData) -> float:
        """Calculate Venture Capital method"""
        if company_data.revenue <= 0:
            return 0
        
        # Project exit value in 5 years
        exit_revenue = company_data.revenue * ((1 + company_data.growth_rate / 100) ** 5)
        
        # UCaaS exit multiples (revenue-based)
        exit_multiple = 8  # Conservative multiple
        if company_data.growth_rate > 40:
            exit_multiple = 12
        elif company_data.growth_rate > 25:
            exit_multiple = 10
        
        exit_value = exit_revenue * exit_multiple
        
        # Required ROI (10x in 5 years is typical for VC)
        required_roi = 10
        
        # Present value
        present_value = exit_value / required_roi
        
        return present_value
    
    def _calculate_comparable_local(self, company_data: CompanyData) -> float:
        """Calculate market comparables valuation"""
        if company_data.revenue <= 0:
            return 0
        
        # UCaaS public company multiples (simplified)
        revenue_multiples = {
            "high_growth": 15,  # >40% growth
            "medium_growth": 10,  # 20-40% growth  
            "steady_growth": 6   # <20% growth
        }
        
        if company_data.growth_rate > 40:
            multiple = revenue_multiples["high_growth"]
        elif company_data.growth_rate > 20:
            multiple = revenue_multiples["medium_growth"]
        else:
            multiple = revenue_multiples["steady_growth"]
        
        # Apply discount for private company
        private_discount = 0.25  # 25% discount
        
        return company_data.revenue * multiple * (1 - private_discount)
    
    def _select_best_method(self, company_data: CompanyData, valuations: Dict[str, float]) -> tuple:
        """Select the best valuation method based on company characteristics"""
        # Filter out zero valuations
        valid_valuations = {k: v for k, v in valuations.items() if v > 0}
        
        if not valid_valuations:
            return "AI-Powered", 0, 0.3
        
        # Method selection logic
        if company_data.revenue > 5000000 and company_data.historical_revenue:
            # Mature company with history - prefer DCF
            method = "DCF Analysis"
            value = valid_valuations.get('dcf', 0)
            confidence = 0.85
        elif company_data.mrr > 50000:
            # Strong recurring revenue - prefer UCaaS metrics
            method = "UCaaS Metrics"
            value = valid_valuations.get('ucaas', 0)
            confidence = 0.8
        elif company_data.revenue > 1000000:
            # Revenue-generating - prefer AI or comparables
            if 'ai' in valid_valuations and 'comparable' in valid_valuations:
                method = "AI-Powered"
                value = valid_valuations['ai']
                confidence = 0.75
            else:
                method = "Market Comparables"
                value = valid_valuations.get('comparable', 0)
                confidence = 0.7
        elif company_data.stage == "startup" and company_data.revenue < 100000:
            # Early stage - prefer startup methods
            if 'scorecard' in valid_valuations:
                method = "Scorecard Method"
                value = valid_valuations['scorecard']
                confidence = 0.65
            elif 'berkus' in valid_valuations:
                method = "Berkus Method"
                value = valid_valuations['berkus']
                confidence = 0.6
            else:
                method = "Risk Factor Summation"
                value = valid_valuations.get('risk_factor', 0)
                confidence = 0.55
        else:
            # Default to highest value with moderate confidence
            method = max(valid_valuations, key=valid_valuations.get)
            value = valid_valuations[method]
            confidence = 0.5
            
            # Convert method key to display name
            method_names = {
                'dcf': 'DCF Analysis',
                'ucaas': 'UCaaS Metrics', 
                'ai': 'AI-Powered',
                'berkus': 'Berkus Method',
                'scorecard': 'Scorecard Method',
                'risk_factor': 'Risk Factor Summation',
                'vc_method': 'Venture Capital Method',
                'comparable': 'Market Comparables'
            }
            method = method_names.get(method, method)
        
        if value <= 0:
            # Fallback if selected method has no value
            value = list(valid_valuations.values())[0]
            confidence *= 0.7
        
        return method, value, confidence
    
    def _identify_risk_factors(self, company_data: CompanyData) -> List[str]:
        """Identify key risk factors for the company"""
        risks = []
        
        if company_data.churn_rate > 10:
            risks.append("High customer churn rate")
        
        if company_data.growth_rate < 10:
            risks.append("Low growth rate")
        
        if company_data.customers < 50:
            risks.append("Small customer base")
        
        if company_data.cac > 0 and company_data.ltv > 0 and company_data.ltv / company_data.cac < 3:
            risks.append("Poor LTV/CAC ratio")
        
        if len(company_data.competitor_names or []) > 5:
            risks.append("Highly competitive market")
        
        if company_data.team_experience == "novice":
            risks.append("Inexperienced management team")
        
        if company_data.market_position == "challenger":
            risks.append("Weak market position")
        
        return risks
    
    def _calculate_growth_projections(self, company_data: CompanyData) -> Dict[str, Any]:
        """Calculate growth projections for the company"""
        current_revenue = company_data.revenue
        growth_rate = company_data.growth_rate / 100
        
        projections = {
            'years': [],
            'revenue': [],
            'customers': [],
            'mrr': []
        }
        
        current_customers = company_data.customers
        current_mrr = company_data.mrr
        
        for year in range(1, 6):
            projections['years'].append(f"Year {year}")
            
            # Revenue projection
            projected_revenue = current_revenue * ((1 + growth_rate) ** year)
            projections['revenue'].append(projected_revenue)
            
            # Customer projection (assuming some churn)
            net_growth_rate = growth_rate - (company_data.churn_rate / 100 * 12)  # Annual churn
            projected_customers = current_customers * ((1 + net_growth_rate) ** year)
            projections['customers'].append(int(projected_customers))
            
            # MRR projection
            projected_mrr = current_mrr * ((1 + growth_rate) ** year)
            projections['mrr'].append(projected_mrr)
        
        return projections
    
    def calculate_valuations_api(self, company_data: CompanyData) -> Optional[ValuationResults]:
        """Calculate valuations using the web API"""
        try:
            # Convert company data to API format (percentages as numbers, not decimals)
            api_data = asdict(company_data)
            
            # Make API request to comprehensive valuation endpoint
            response = requests.post(
                f"{self.api_base_url}/api/comprehensive-valuation",
                json=api_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                
                # Format API results
                return ValuationResults(
                    dcf_valuation=results['valuation_methods']['dcf']['valuation'],
                    ucaas_valuation=results['valuation_methods']['ucaas_metrics']['valuation'],
                    ai_valuation=results['valuation_methods']['ai_powered']['valuation'],
                    recommended_method=results['recommended_valuation']['method'],
                    recommended_value=results['recommended_valuation']['valuation'],
                    confidence_score=results['recommended_valuation']['confidence_score'],
                    valuation_range=results['valuation_range'],
                    method_details={
                        'dcf': results['valuation_methods']['dcf'],
                        'ucaas': results['valuation_methods']['ucaas_metrics'],
                        'ai': results['valuation_methods']['ai_powered']
                    },
                    summary=results['summary']['explanation']
                )
            else:
                print(f"⚠️ API request failed with status {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️ API connection error: {e}")
            return None
        except Exception as e:
            print(f"⚠️ Error calling API: {e}")
            return None
    
    def _simplified_valuations(self, company_data: CompanyData) -> ValuationResults:
        """Simplified valuation calculations as fallback"""
        revenue = company_data.revenue
        growth_rate = company_data.growth_rate
        ebitda_margin = company_data.ebitda_margin
        
        # Simplified DCF calculation
        discount_rate = company_data.discount_rate
        terminal_growth = company_data.terminal_growth_rate
        
        # Project 5 years of cash flows
        projected_fcf = []
        current_revenue = revenue
        
        for year in range(5):
            current_revenue *= (1 + growth_rate)
            ebitda = current_revenue * ebitda_margin
            fcf = ebitda * 0.8  # Simplified FCF conversion
            projected_fcf.append(fcf)
        
        # Calculate DCF value
        pv_fcf = sum(fcf / ((1 + discount_rate) ** (i + 1)) for i, fcf in enumerate(projected_fcf))
        terminal_value = projected_fcf[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
        pv_terminal = terminal_value / ((1 + discount_rate) ** 5)
        dcf_value = pv_fcf + pv_terminal
        
        # Simplified UCaaS multiple valuation
        if company_data.mrr > 0:
            ucaas_value = company_data.mrr * 12 * 10  # 10x ARR multiple
        else:
            ucaas_value = revenue * 8  # 8x revenue multiple
        
        # Simplified AI valuation (average with adjustments)
        base_value = (dcf_value + ucaas_value) / 2
        
        # Growth adjustment
        if growth_rate > 0.3:
            growth_multiplier = 1.2
        elif growth_rate > 0.2:
            growth_multiplier = 1.1
        else:
            growth_multiplier = 1.0
        
        ai_value = base_value * growth_multiplier
        
        # Determine recommended method
        if revenue > 1000000 and company_data.historical_revenue:
            recommended_method = "DCF"
            recommended_value = dcf_value
            confidence = 0.8
        elif company_data.mrr > 0:
            recommended_method = "UCaaS Metrics"
            recommended_value = ucaas_value
            confidence = 0.75
        else:
            recommended_method = "AI-Powered"
            recommended_value = ai_value
            confidence = 0.6
        
        return ValuationResults(
            dcf_valuation=dcf_value,
            ucaas_valuation=ucaas_value,
            ai_valuation=ai_value,
            recommended_method=recommended_method,
            recommended_value=recommended_value,
            confidence_score=confidence,
            valuation_range={
                'low': min(dcf_value, ucaas_value, ai_value),
                'high': max(dcf_value, ucaas_value, ai_value),
                'average': (dcf_value + ucaas_value + ai_value) / 3
            },
            method_details={
                'dcf': {'valuation': dcf_value, 'method': 'Simplified DCF'},
                'ucaas': {'valuation': ucaas_value, 'method': 'Revenue Multiple'},
                'ai': {'valuation': ai_value, 'method': 'Adjusted Average'}
            },
            summary=f"Simplified valuation analysis recommends {recommended_method} "
                   f"with a value of ${recommended_value:,.0f} (confidence: {confidence:.0%})"
        )
    
    def generate_report(self, company_data: CompanyData, results: ValuationResults, 
                       output_format: str = "json") -> str:
        """Generate valuation report in specified format"""
        
        if output_format.lower() == "json":
            return self._generate_json_report(company_data, results)
        elif output_format.lower() == "text":
            return self._generate_text_report(company_data, results)
        elif output_format.lower() == "markdown":
            return self._generate_markdown_report(company_data, results)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def _generate_json_report(self, company_data: CompanyData, results: ValuationResults) -> str:
        """Generate JSON format report"""
        report_data = {
            'company_info': asdict(company_data),
            'valuation_results': asdict(results),
            'generated_at': datetime.now().isoformat(),
            'tool_version': '2.0.0'
        }
        return json.dumps(report_data, indent=2)
    
    def _generate_text_report(self, company_data: CompanyData, results: ValuationResults) -> str:
        """Generate plain text report"""
        report = f"""
🏢 UCaaS COMPANY VALUATION REPORT
==================================================

Company: {company_data.company_name}
Industry: {company_data.industry}
Report Date: {datetime.now().strftime('%B %d, %Y')}

EXECUTIVE SUMMARY
-----------------
Recommended Valuation: ${results.recommended_value:,.0f}
Method: {results.recommended_method}
Confidence Level: {results.confidence_score:.0%}

VALUATION METHODS COMPARISON
----------------------------
DCF Valuation:        ${results.dcf_valuation:,.0f}
UCaaS Metrics:        ${results.ucaas_valuation:,.0f}
AI-Powered:           ${results.ai_valuation:,.0f}

VALUATION RANGE
---------------
Low Estimate:         ${results.valuation_range['low']:,.0f}
High Estimate:        ${results.valuation_range['high']:,.0f}
Average:              ${results.valuation_range['average']:,.0f}

KEY FINANCIAL METRICS
---------------------
Annual Revenue:       ${company_data.revenue:,.0f}
Growth Rate:          {company_data.growth_rate:.1%}
EBITDA Margin:        {company_data.ebitda_margin:.1%}
Monthly Churn:        {company_data.churn_rate:.1%}
Customers:            {company_data.customers:,}

ANALYSIS SUMMARY
----------------
{results.summary}

Generated by UCaaS Valuation Tool v2.0
"""
        return report
    
    def _generate_markdown_report(self, company_data: CompanyData, results: ValuationResults) -> str:
        """Generate Markdown format report"""
        report = f"""
# 🏢 {company_data.company_name} Valuation Report

**Industry:** {company_data.industry}  
**Report Date:** {datetime.now().strftime('%B %d, %Y')}

## 📊 Executive Summary

- **Recommended Valuation:** ${results.recommended_value:,.0f}
- **Method:** {results.recommended_method}
- **Confidence Level:** {results.confidence_score:.0%}

## 💰 Valuation Methods Comparison

| Method | Valuation |
|--------|-----------|
| DCF Analysis | ${results.dcf_valuation:,.0f} |
| UCaaS Metrics | ${results.ucaas_valuation:,.0f} |
| AI-Powered | ${results.ai_valuation:,.0f} |

## 📈 Valuation Range

- **Low Estimate:** ${results.valuation_range['low']:,.0f}
- **High Estimate:** ${results.valuation_range['high']:,.0f}
- **Average:** ${results.valuation_range['average']:,.0f}

## 🔑 Key Metrics

- **Annual Revenue:** ${company_data.revenue:,.0f}
- **Growth Rate:** {company_data.growth_rate:.1%}
- **EBITDA Margin:** {company_data.ebitda_margin:.1%}
- **Monthly Churn:** {company_data.churn_rate:.1%}
- **Customer Count:** {company_data.customers:,}

## 📝 Analysis Summary

{results.summary}

---
*Generated by UCaaS Valuation Tool v2.0*
"""
        return report
    
    def save_report(self, report_content: str, company_name: str, 
                   output_format: str = "text") -> Path:
        """Save report to file"""
        # Create reports directory
        reports_dir = Path.cwd() / "valuation_reports"
        reports_dir.mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_company_name = safe_company_name.replace(' ', '_')
        
        file_extension = {
            'json': '.json',
            'text': '.txt',
            'markdown': '.md'
        }.get(output_format.lower(), '.txt')
        
        filename = f"{safe_company_name}_valuation_{timestamp}{file_extension}"
        file_path = reports_dir / filename
        
        # Save file
        file_path.write_text(report_content, encoding='utf-8')
        
        return file_path

def main():
    """Main execution function"""
    print("🚀 UCaaS Valuation Tool v2.0")
    print("Enhanced for web platform integration")
    print("=" * 50)
    
    # Initialize the valuation tool
    tool = UCaaSValuationTool()
    
    # Collect company data
    print("\n📋 Data Collection")
    company_data = tool.collect_company_data_interactive()
    
    print(f"\n🔄 Calculating comprehensive valuations for {company_data.company_name}...")
    
    # Calculate all valuation methods
    results = tool.calculate_all_valuations(company_data)
    
    # Display results
    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE VALUATION RESULTS")
    print("=" * 70)
    print(f"Company: {company_data.company_name}")
    print(f"Stage: {company_data.stage.title()}")
    print(f"Revenue: ${company_data.revenue:,.0f}")
    print(f"Growth Rate: {company_data.growth_rate:.1f}%")
    print()
    print(f"💰 RECOMMENDED VALUATION: ${results.recommended_value:,.0f}")
    print(f"📊 Method: {results.recommended_method}")
    print(f"🎯 Confidence: {results.confidence_score:.0%}")
    print()
    print("📈 All Valuation Methods:")
    print(f"  DCF Analysis:          ${results.dcf_valuation:,.0f}")
    print(f"  UCaaS Metrics:         ${results.ucaas_valuation:,.0f}")
    print(f"  AI-Powered:            ${results.ai_valuation:,.0f}")
    print(f"  Berkus Method:         ${results.berkus_valuation:,.0f}")
    print(f"  Scorecard Method:      ${results.scorecard_valuation:,.0f}")
    print(f"  Risk Factor Sum:       ${results.risk_factor_valuation:,.0f}")
    print(f"  VC Method:             ${results.vc_method_valuation:,.0f}")
    print(f"  Market Comparables:    ${results.comparable_valuation:,.0f}")
    print()
    print("📊 Valuation Range:")
    print(f"  Low Estimate:          ${results.valuation_range['low']:,.0f}")
    print(f"  High Estimate:         ${results.valuation_range['high']:,.0f}")
    print(f"  Average:               ${results.valuation_range['average']:,.0f}")
    print()
    if results.risk_factors:
        print("⚠️ Key Risk Factors:")
        for risk in results.risk_factors:
            print(f"  • {risk}")
        print()
    print("📝 Analysis Summary:")
    print(f"  {results.summary}")
    if results.methodology_explanation:
        print(f"  {results.methodology_explanation}")
    
    # Generate and save reports
    print("\n📄 Generating Reports...")
    
    # Save in multiple formats
    for format_type in ['text', 'json', 'markdown']:
        try:
            report_content = tool.generate_report(company_data, results, format_type)
            file_path = tool.save_report(report_content, company_data.company_name, format_type)
            print(f"✅ {format_type.upper()} report saved: {file_path}")
        except Exception as e:
            print(f"⚠️ Failed to generate {format_type} report: {e}")
    
    print(f"\n🎯 Valuation Complete!")
    print(f"Reports saved in: {Path.cwd() / 'valuation_reports'}")

if __name__ == "__main__":
    main()