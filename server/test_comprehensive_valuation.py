"""
Test script to demonstrate the Comprehensive UCaaS Valuation System

This script tests all three valuation methods:
1. DCF Valuation (Discounted Cash Flow)
2. UCaaS-Specific Metrics  
3. AI-Powered Valuation

And then selects the best method with justification.
"""

import sys
sys.path.append('.')

from services.comprehensive_valuation import ComprehensiveValuation

def test_comprehensive_valuation():
    """Test the comprehensive valuation system with sample UCaaS company data"""
    
    print("🏆 COMPREHENSIVE UCaaS VALUATION SYSTEM TEST")
    print("="*60)
    
    # Sample UCaaS company financial data
    sample_data = {
        'company_name': 'SampleUCaaS Corp',
        'revenue': 12000000,  # $12M annual revenue
        'growth_rate': 0.35,  # 35% growth rate
        'ebitda_margin': 0.20,  # 20% EBITDA margin
        'discount_rate': 0.12,  # 12% discount rate
        'terminal_growth_rate': 0.03,  # 3% terminal growth
        'mrr': 1000000,  # $1M MRR
        'arpu': 200,  # $200 ARPU
        'customers': 5000,  # 5,000 customers
        'churn_rate': 0.04,  # 4% monthly churn
        'cac': 800,  # $800 CAC
        'gross_margin': 0.75,  # 75% gross margin
        'expansion_revenue': 50000,  # $50k monthly expansion
        'support_costs': 15,  # $15 per customer support cost
        'market_position': 'challenger',
        'technology_score': 8,  # 8/10 technology score
        'historical_revenue': [8000000, 9500000, 11200000, 12000000]  # 4 years of revenue
    }
    
    print(f"Company: {sample_data['company_name']}")
    print(f"Annual Revenue: ${sample_data['revenue']:,}")
    print(f"MRR: ${sample_data['mrr']:,}")
    print(f"Growth Rate: {sample_data['growth_rate']*100:.1f}%")
    print(f"Customers: {sample_data['customers']:,}")
    print("-"*60)
    
    # Initialize comprehensive valuation service
    valuation_service = ComprehensiveValuation()
    
    # Perform comprehensive analysis
    print("🔍 PERFORMING COMPREHENSIVE VALUATION ANALYSIS...")
    print()
    
    results = valuation_service.perform_comprehensive_valuation(sample_data)
    
    # Display results
    print("📊 DATA QUALITY ASSESSMENT")
    print("-"*30)
    data_quality = results['company_info']['data_quality']
    print(f"Overall Quality Score: {data_quality['overall_score']*100:.1f}%")
    print(f"Data Completeness: {data_quality['data_completeness_percentage']:.1f}%")
    print()
    
    print("🔍 THREE VALUATION METHODS ANALYZED")
    print("-"*40)
    
    # DCF Valuation
    dcf_result = results['valuation_methods']['dcf']
    print("💼 1. DCF VALUATION (DISCOUNTED CASH FLOW)")
    print(f"   Valuation: ${dcf_result['valuation']:,.0f}")
    print(f"   Confidence: {dcf_result['confidence_score']*100:.1f}%")
    print(f"   Best For: Predictable cash flows and stable growth")
    print()
    
    # UCaaS Metrics
    ucaas_result = results['valuation_methods']['ucaas_metrics']
    print("📊 2. UCaaS-SPECIFIC METRICS")
    print(f"   Valuation: ${ucaas_result['valuation']:,.0f}")
    print(f"   Confidence: {ucaas_result['confidence_score']*100:.1f}%")
    if 'key_metrics' in ucaas_result:
        print(f"   Rule of 40: {ucaas_result['key_metrics'].get('Rule of 40', 0):.1f}")
        print(f"   LTV/CAC: {ucaas_result['key_metrics'].get('LTV/CAC', 0):.2f}")
    print(f"   Best For: Recurring revenue strength and customer metrics")
    print()
    
    # AI-Powered
    ai_result = results['valuation_methods']['ai_powered']
    print("🤖 3. AI-POWERED VALUATION")
    print(f"   Valuation: ${ai_result['valuation']:,.0f}")
    print(f"   Confidence: {ai_result['confidence_score']*100:.1f}%")
    print(f"   Best For: Complex scenarios with qualitative factors")
    print()
    
    print("🎯 FINAL RECOMMENDATION")
    print("-"*25)
    recommendation = results['recommended_valuation']
    print(f"Recommended Valuation: ${recommendation['recommended_valuation']:,.0f}")
    print(f"Selected Method: {recommendation['recommended_method']}")
    print(f"Confidence Level: {recommendation['confidence_level']}")
    print()
    print("💡 Justification:")
    print(f"{recommendation['justification']}")
    print()
    
    # Valuation Range
    if 'valuation_range' in results and results['valuation_range']:
        print("📈 VALUATION RANGE ANALYSIS")
        print("-"*30)
        range_data = results['valuation_range']
        print(f"Low Estimate:  ${range_data.get('low', 0):,.0f}")
        print(f"Average:       ${range_data.get('average', 0):,.0f}")
        print(f"High Estimate: ${range_data.get('high', 0):,.0f}")
        print(f"Recommended:   ${recommendation['recommended_valuation']:,.0f}")
        print()
    
    print("📄 GENERATING COMPREHENSIVE REPORTS...")
    print("-"*40)
    
    # Generate reports in all formats
    from services.report_generator import ReportGenerator
    
    company_info = {
        'name': sample_data['company_name'],
        'arr': sample_data['revenue']
    }
    
    valuation_data = {
        'dcf_valuation': dcf_result['valuation'],
        'ucaas_valuation': ucaas_result['valuation'], 
        'ai_valuation': ai_result['valuation'],
        'recommended_valuation': recommendation['recommended_valuation'],
        'recommended_method': recommendation['recommended_method'],
        'confidence_level': recommendation['confidence_level'],
        'justification': recommendation['justification'],
        'valuation_range': results.get('valuation_range', {}),
        'data_quality': data_quality
    }
    
    market_data = {
        'market_size': 50000000000,  # $50B UCaaS market
        'market_growth': 0.15,
        'competitive_position': sample_data['market_position']
    }
    
    peer_comparison = []
    
    report_generator = ReportGenerator()
    
    try:
        # Generate comprehensive reports
        file_paths = report_generator.generate_comprehensive_report_all_formats(
            company_info, valuation_data, market_data, peer_comparison
        )
        
        print("✅ Reports generated successfully:")
        for format_type, file_path in file_paths.items():
            print(f"   {format_type.upper()}: {file_path}")
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")
    
    print()
    print("🏁 COMPREHENSIVE VALUATION COMPLETED!")
    print("="*60)
    
    return results

if __name__ == "__main__":
    test_comprehensive_valuation()
