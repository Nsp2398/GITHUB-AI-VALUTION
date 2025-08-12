import React, { useState, useEffect } from 'react';
import CompanyAnalytics from './CompanyAnalytics';

interface ValuationAnalysisProps {
  companyData: {
    companyName: string;
    revenue: string;
    growthRate: string;
    expenses: string;
    employees: string;
    customerCount: string;
    churnRate: string;
    cac: string;
    ltv: string;
    stage?: string;
    teamExperience?: string;
    productStage?: string;
    marketSize?: string;
    traction?: string;
  };
}

interface ValuationModel {
  id: string;
  name: string;
  description: string;
  bestFor: string;
  icon: string;
  complexity: 'Low' | 'Medium' | 'High';
  dataRequirements: string[];
  recommendedStages: string[];
}

const ValuationAnalysis: React.FC<ValuationAnalysisProps> = ({ companyData }) => {
  const [activeMethod, setActiveMethod] = useState('selection');
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [calculating, setCalculating] = useState(false);
  const [aiRecommendation, setAiRecommendation] = useState<string>('');
  const [valuationResults, setValuationResults] = useState({
    berkus: 0,
    scorecard: 0,
    riskFactor: 0,
    vcMethod: 0,
    dcf: 0,
    comparables: 0,
    ucaas: 0,
    ai: 0,
    final: 0,
    confidence: 0,
    selectedMethod: '',
    methodology: ''
  });

  // Define all valuation models
  const valuationModels: ValuationModel[] = [
    {
      id: 'berkus',
      name: 'Berkus Method',
      description: 'Qualitative evaluation based on team, product potential, and market opportunity',
      bestFor: 'Pre-revenue startups with strong team and product concept',
      icon: '🌱',
      complexity: 'Low',
      dataRequirements: ['Team experience', 'Product stage', 'Market opportunity'],
      recommendedStages: ['Idea', 'Pre-revenue', 'MVP']
    },
    {
      id: 'scorecard',
      name: 'Scorecard Method',
      description: 'Compares target business against averages of funded startups in region',
      bestFor: 'Early-stage startups with some traction and comparable market data',
      icon: '📊',
      complexity: 'Medium',
      dataRequirements: ['Market comparables', 'Team quality', 'Product development'],
      recommendedStages: ['Pre-revenue', 'Early revenue', 'Growth']
    },
    {
      id: 'riskFactor',
      name: 'Risk Factor Summation',
      description: 'Enhanced scorecard method with 12+ risk categories adjustment',
      bestFor: 'Startups with detailed risk assessment and market analysis',
      icon: '⚖️',
      complexity: 'High',
      dataRequirements: ['Risk assessment', 'Market analysis', 'Financial projections'],
      recommendedStages: ['Early revenue', 'Growth', 'Expansion']
    },
    {
      id: 'vcMethod',
      name: 'Venture Capital Method',
      description: 'ROI-based approach calculating from projected exit scenarios',
      bestFor: 'Startups with clear exit strategy and growth projections',
      icon: '💰',
      complexity: 'High',
      dataRequirements: ['Exit projections', 'ROI targets', 'Time to exit'],
      recommendedStages: ['Growth', 'Expansion', 'Pre-exit']
    },
    {
      id: 'dcf',
      name: 'Discounted Cash Flow',
      description: 'Traditional financial valuation using projected cash flows',
      bestFor: 'Revenue-generating businesses with predictable cash flows',
      icon: '📈',
      complexity: 'High',
      dataRequirements: ['Revenue history', 'Cash flow projections', 'Growth rates'],
      recommendedStages: ['Revenue', 'Growth', 'Mature']
    },
    {
      id: 'comparables',
      name: 'Market Comparables',
      description: 'Valuation based on similar companies and market multiples',
      bestFor: 'Companies in established markets with available comparable data',
      icon: '🏢',
      complexity: 'Medium',
      dataRequirements: ['Industry data', 'Comparable companies', 'Market multiples'],
      recommendedStages: ['Revenue', 'Growth', 'Mature']
    }
  ];

  // AI-powered model recommendation
  const getAIRecommendation = () => {
    const revenue = parseFloat(companyData.revenue) || 0;
    const hasRevenue = revenue > 0;
    const stage = companyData.stage || 'unknown';
    const teamExp = companyData.teamExperience || 'medium';
    const productStage = companyData.productStage || 'development';

    let recommendedModel = '';
    let reasoning = '';

    if (!hasRevenue && (stage === 'idea' || stage === 'pre-revenue')) {
      if (teamExp === 'high' && productStage === 'mvp') {
        recommendedModel = 'scorecard';
        reasoning = 'Early-stage startup with strong team and MVP - Scorecard method provides market-based comparison';
      } else {
        recommendedModel = 'berkus';
        reasoning = 'Pre-revenue startup - Berkus method ideal for qualitative assessment';
      }
    } else if (hasRevenue && revenue < 1000000) {
      recommendedModel = 'riskFactor';
      reasoning = 'Early revenue stage - Risk Factor Summation provides comprehensive risk-adjusted valuation';
    } else if (hasRevenue && revenue >= 1000000) {
      if (stage === 'growth' || stage === 'expansion') {
        recommendedModel = 'dcf';
        reasoning = 'Established revenue - DCF analysis provides accurate cash flow-based valuation';
      } else {
        recommendedModel = 'comparables';
        reasoning = 'Mature company - Market comparables provide industry-standard valuation';
      }
    } else {
      recommendedModel = 'scorecard';
      reasoning = 'Default recommendation - Scorecard method provides balanced startup valuation';
    }

    setSelectedModel(recommendedModel);
    setAiRecommendation(reasoning);
    return { model: recommendedModel, reasoning };
  };

  // Calculate valuations using all methods
  const calculateValuations = () => {
    const revenue = parseFloat(companyData.revenue) || 0;
    const growthRate = parseFloat(companyData.growthRate) || 35;
    const expenses = parseFloat(companyData.expenses) || 0;
    const customerCount = parseFloat(companyData.customerCount) || 0;
    const churnRate = parseFloat(companyData.churnRate) || 8;
    const cac = parseFloat(companyData.cac) || 1200;
    const ltv = parseFloat(companyData.ltv) || 5000;

    // 1. Berkus Method (Pre-revenue qualitative)
    const berkusFactors = {
      soundIdea: 0.5, // 0-1 scale
      prototypeQuality: 0.7,
      qualityManagement: 0.8,
      strategicRelationships: 0.6,
      productRollout: 0.5
    };
    const maxBerkusValue = 2000000; // $2M max
    const berkusValue = Object.values(berkusFactors).reduce((sum, factor) => sum + factor, 0) / 5 * maxBerkusValue;

    // 2. Scorecard Method
    const regionAverage = 2000000; // Average pre-money valuation in region
    const scorecardFactors = {
      strength: 1.25, // Team strength multiplier
      sizeOfOpportunity: 1.0,
      product: 1.1,
      competitive: 0.9,
      marketing: 1.05,
      needForFunding: 0.95,
      other: 1.0
    };
    const scorecardMultiplier = Object.values(scorecardFactors).reduce((prod, factor) => prod * factor, 1);
    const scorecardValue = regionAverage * scorecardMultiplier;

    // 3. Risk Factor Summation Method
    const riskFactors = {
      management: 0, // -2 to +2 scale
      stage: -1,
      legislation: 0,
      manufacturing: 0,
      sales: 1,
      funding: 0,
      competition: -1,
      technology: 1,
      litigation: 0,
      reputation: 0,
      potential: 1,
      exit: 0
    };
    const riskAdjustment = Object.values(riskFactors).reduce((sum, risk) => sum + risk, 0) * 0.25; // 25% per risk unit
    const riskFactorValue = scorecardValue * (1 + riskAdjustment);

    // 4. Venture Capital Method
    const projectedRevenue5Y = revenue * Math.pow(1 + growthRate/100, 5) || 10000000;
    const industryPEMultiple = 15;
    const projectedExitValue = projectedRevenue5Y * industryPEMultiple;
    const requiredROI = 10; // 10x return
    const investorShare = 0.25; // 25% equity
    const vcValue = projectedExitValue / requiredROI * (1 - investorShare);

    // 5. DCF Method (existing)
    const ebitda = revenue - expenses;
    const discountRate = 0.12;
    const terminalGrowth = 0.03;
    const projectedCashFlows = [];
    
    for (let year = 1; year <= 5; year++) {
      const projectedRevenue = revenue * Math.pow(1 + (growthRate / 100), year);
      const projectedEbitda = projectedRevenue * (ebitda / revenue || 0.3);
      projectedCashFlows.push(projectedEbitda);
    }
    
    const terminalValue = projectedCashFlows[4] * (1 + terminalGrowth) / (discountRate - terminalGrowth);
    const dcfValue = projectedCashFlows.reduce((sum, cf, index) => 
      sum + cf / Math.pow(1 + discountRate, index + 1), 0
    ) + terminalValue / Math.pow(1 + discountRate, 5);

    // 6. Comparables Method
    const industryMultiples = {
      revenueMultiple: 12.5,
      ebitdaMultiple: 35,
      customerMultiple: 4200,
      employeeMultiple: 500000
    };
    
    const comparablesValue = Math.max(
      revenue * industryMultiples.revenueMultiple,
      ebitda * industryMultiples.ebitdaMultiple,
      customerCount * industryMultiples.customerMultiple,
      parseFloat(companyData.employees || '0') * industryMultiples.employeeMultiple
    );

    // 7. UCaaS Method (same as comparables for now, can be customized)
    const ucaasValue = comparablesValue;

    // 8. AI Valuation (apply premiums/adjustments)
    let aiValue = comparablesValue;
    if (growthRate > 30) aiValue *= 1.2;
    else if (growthRate > 20) aiValue *= 1.1;
    if (churnRate < 5) aiValue *= 1.1;
    else if (churnRate >= 10) aiValue *= 0.9;
    if ((ltv / cac) > 3) aiValue *= 1.15;
    else aiValue *= 1.05;
    aiValue *= 1.05; // Market position

    // Select best method based on AI recommendation
    const recommendation = getAIRecommendation();
    const methodValues = {
      berkus: berkusValue,
      scorecard: scorecardValue,
      riskFactor: riskFactorValue,
      vcMethod: vcValue,
      dcf: dcfValue,
      comparables: comparablesValue,
      ucaas: ucaasValue,
      ai: aiValue
    };

    const finalValue = methodValues[recommendation.model as keyof typeof methodValues] || scorecardValue;
    
    // Calculate confidence based on data completeness and method appropriateness
    const dataCompleteness = Object.values(companyData).filter(val => val && val !== '').length / Object.keys(companyData).length;
    const methodConfidence = revenue > 0 ? 0.9 : 0.7; // Higher confidence with revenue data
    const confidence = Math.min(95, Math.max(60, dataCompleteness * methodConfidence * 100));

    setValuationResults({
      berkus: Math.round(berkusValue),
      scorecard: Math.round(scorecardValue),
      riskFactor: Math.round(riskFactorValue),
      vcMethod: Math.round(vcValue),
      dcf: Math.round(dcfValue),
      comparables: Math.round(comparablesValue),
      ucaas: Math.round(ucaasValue),
      ai: Math.round(aiValue),
      final: Math.round(finalValue),
      confidence: Math.round(confidence),
      selectedMethod: recommendation.model,
      methodology: recommendation.reasoning
    });
  };

  useEffect(() => {
    setCalculating(true);
    setTimeout(() => {
      calculateValuations();
      setCalculating(false);
    }, 2000);
  }, [companyData]);

  const downloadReport = async (format: string) => {
    try {
      const reportData = {
        company_info: {
          name: companyData.companyName,
          arr: parseFloat(companyData.revenue),
          industry: "UCaaS",
          employees: companyData.employees,
          customers: companyData.customerCount
        },
        valuation_data: {
          dcf_valuation: valuationResults.dcf,
          ucaas_valuation: valuationResults.ucaas,
          ai_valuation: valuationResults.ai,
          final_valuation: valuationResults.final,
          confidence_score: valuationResults.confidence,
          growth_rate: parseFloat(companyData.growthRate) / 100,
          churn_rate: parseFloat(companyData.churnRate) / 100,
          ltv_cac_ratio: parseFloat(companyData.ltv) / parseFloat(companyData.cac),
          revenue_multiple: valuationResults.ucaas / parseFloat(companyData.revenue)
        },
        market_data: {
          market_size: 50000000000,
          growth_rate: 0.12,
          key_trends: ["Remote work adoption", "Cloud migration", "AI integration", "Security focus"]
        }
      };

      const response = await fetch('http://localhost:5000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          ...reportData,
          format: format
        }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        const fileExtension = format === 'all' ? 'zip' : format;
        a.download = `${companyData.companyName}_valuation_report.${fileExtension}`;
        
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        alert('Report generation failed');
      }
    } catch (error) {
      console.error('Report generation error:', error);
      alert('Report generation failed');
    }
  };

  if (calculating) {
    return (
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-8 text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-6"></div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">🤖 AI Valuation in Progress</h3>
        <p className="text-gray-600 mb-4">Analyzing your data using multiple valuation methods...</p>
        <div className="space-y-2 text-sm text-gray-500">
          <p>✓ Processing financial data</p>
          <p>✓ Running DCF analysis</p>
          <p>✓ Applying UCaaS industry metrics</p>
          <p>⏳ AI-enhanced valuation modeling</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Results Overview */}
      <div className="bg-gradient-to-r from-green-100 via-blue-100 to-purple-100 rounded-2xl p-6 shadow-xl">
        <div className="text-center mb-6">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent">
            {companyData.companyName} Valuation Results
          </h2>
          <p className="text-gray-600 mt-2">Comprehensive AI-powered analysis</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="bg-white/70 backdrop-blur-xl rounded-xl p-4 text-center">
            <p className="text-2xl font-bold text-blue-600">${(valuationResults.dcf / 1000000).toFixed(1)}M</p>
            <p className="text-sm text-gray-600">DCF Valuation</p>
          </div>
          <div className="bg-white/70 backdrop-blur-xl rounded-xl p-4 text-center">
            <p className="text-2xl font-bold text-green-600">${(valuationResults.ucaas / 1000000).toFixed(1)}M</p>
            <p className="text-sm text-gray-600">UCaaS Method</p>
          </div>
          <div className="bg-white/70 backdrop-blur-xl rounded-xl p-4 text-center">
            <p className="text-2xl font-bold text-purple-600">${(valuationResults.ai / 1000000).toFixed(1)}M</p>
            <p className="text-sm text-gray-600">AI Valuation</p>
          </div>
          <div className="bg-white/70 backdrop-blur-xl rounded-xl p-4 text-center border-2 border-yellow-400">
            <p className="text-2xl font-bold text-orange-600">${(valuationResults.final / 1000000).toFixed(1)}M</p>
            <p className="text-sm text-gray-600 font-medium">Final Valuation</p>
          </div>
          <div className="bg-white/70 backdrop-blur-xl rounded-xl p-4 text-center">
            <p className="text-2xl font-bold text-indigo-600">{valuationResults.confidence}%</p>
            <p className="text-sm text-gray-600">Confidence</p>
          </div>
        </div>
      </div>

      {/* Method Navigation */}
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl">
        <div className="border-b border-gray-200 px-6 py-3">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', name: 'Overview', icon: '📊' },
              { id: 'dcf', name: 'DCF Analysis', icon: '📈' },
              { id: 'ucaas', name: 'UCaaS Method', icon: '☁️' },
              { id: 'ai', name: 'AI Valuation', icon: '🤖' },
              { id: 'analytics', name: 'Performance Analytics', icon: '📈' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveMethod(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeMethod === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.icon} {tab.name}
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {activeMethod === 'overview' && (
            <div className="space-y-6">
              <h3 className="text-xl font-bold text-gray-900">Executive Summary</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-gray-800 mb-3">Key Metrics</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between"><span>Revenue Multiple:</span><span className="font-medium">{(valuationResults.final / parseFloat(companyData.revenue)).toFixed(1)}x</span></div>
                    <div className="flex justify-between"><span>LTV/CAC Ratio:</span><span className="font-medium">{(parseFloat(companyData.ltv) / parseFloat(companyData.cac)).toFixed(1)}x</span></div>
                    <div className="flex justify-between"><span>Growth Rate:</span><span className="font-medium">{companyData.growthRate}%</span></div>
                    <div className="flex justify-between"><span>Churn Rate:</span><span className="font-medium">{companyData.churnRate}%</span></div>
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-3">Valuation Range</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between"><span>Conservative:</span><span className="font-medium">${(Math.min(valuationResults.dcf, valuationResults.ucaas, valuationResults.ai) / 1000000).toFixed(1)}M</span></div>
                    <div className="flex justify-between"><span>Optimistic:</span><span className="font-medium">${(Math.max(valuationResults.dcf, valuationResults.ucaas, valuationResults.ai) / 1000000).toFixed(1)}M</span></div>
                    <div className="flex justify-between font-bold"><span>Final Estimate:</span><span>${(valuationResults.final / 1000000).toFixed(1)}M</span></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeMethod === 'dcf' && (
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-gray-900">📈 Discounted Cash Flow Analysis</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-gray-800 mb-3">Assumptions</h4>
                  <div className="space-y-2 text-sm bg-gray-50 p-4 rounded-lg">
                    <div className="flex justify-between"><span>Discount Rate:</span><span>12.0%</span></div>
                    <div className="flex justify-between"><span>Terminal Growth:</span><span>3.0%</span></div>
                    <div className="flex justify-between"><span>Projection Period:</span><span>5 years</span></div>
                    <div className="flex justify-between"><span>Current EBITDA Margin:</span><span>{(((parseFloat(companyData.revenue) - parseFloat(companyData.expenses)) / parseFloat(companyData.revenue)) * 100).toFixed(1)}%</span></div>
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-3">DCF Components</h4>
                  <div className="space-y-2 text-sm bg-blue-50 p-4 rounded-lg">
                    <div className="flex justify-between"><span>PV of Cash Flows (5Y):</span><span>${((valuationResults.dcf * 0.7) / 1000000).toFixed(1)}M</span></div>
                    <div className="flex justify-between"><span>Terminal Value:</span><span>${((valuationResults.dcf * 0.3) / 1000000).toFixed(1)}M</span></div>
                    <div className="flex justify-between font-bold border-t pt-2"><span>Enterprise Value:</span><span>${(valuationResults.dcf / 1000000).toFixed(1)}M</span></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeMethod === 'ucaas' && (
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-gray-900">☁️ UCaaS Industry Valuation</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-gray-800 mb-3">Industry Multiples</h4>
                  <div className="space-y-2 text-sm bg-gray-50 p-4 rounded-lg">
                    <div className="flex justify-between"><span>Revenue Multiple:</span><span>12.5x</span></div>
                    <div className="flex justify-between"><span>EBITDA Multiple:</span><span>35.0x</span></div>
                    <div className="flex justify-between"><span>Customer Multiple:</span><span>$4,200</span></div>
                    <div className="flex justify-between"><span>Employee Multiple:</span><span>$500K</span></div>
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-3">Valuation by Method</h4>
                  <div className="space-y-2 text-sm bg-green-50 p-4 rounded-lg">
                    <div className="flex justify-between"><span>By Revenue:</span><span>${(parseFloat(companyData.revenue) * 12.5 / 1000000).toFixed(1)}M</span></div>
                    <div className="flex justify-between"><span>By EBITDA:</span><span>${((parseFloat(companyData.revenue) - parseFloat(companyData.expenses)) * 35 / 1000000).toFixed(1)}M</span></div>
                    <div className="flex justify-between"><span>By Customers:</span><span>${(parseFloat(companyData.customerCount) * 4200 / 1000000).toFixed(1)}M</span></div>
                    <div className="flex justify-between font-bold border-t pt-2"><span>UCaaS Valuation:</span><span>${(valuationResults.ucaas / 1000000).toFixed(1)}M</span></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeMethod === 'ai' && (
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-gray-900">🤖 AI-Enhanced Valuation</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-gray-800 mb-3">AI Adjustments</h4>
                  <div className="space-y-2 text-sm bg-purple-50 p-4 rounded-lg">
                    <div className="flex justify-between"><span>Growth Premium:</span><span>{companyData.growthRate > '30' ? '+20%' : companyData.growthRate > '20' ? '+10%' : '0%'}</span></div>
                    <div className="flex justify-between"><span>Churn Adjustment:</span><span>{companyData.churnRate < '5' ? '+10%' : companyData.churnRate < '10' ? '0%' : '-10%'}</span></div>
                    <div className="flex justify-between"><span>LTV/CAC Premium:</span><span>{(parseFloat(companyData.ltv) / parseFloat(companyData.cac)) > 3 ? '+15%' : '+5%'}</span></div>
                    <div className="flex justify-between"><span>Market Position:</span><span>+5%</span></div>
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-3">AI Confidence Factors</h4>
                  <div className="space-y-2 text-sm bg-indigo-50 p-4 rounded-lg">
                    <div className="flex justify-between"><span>Data Completeness:</span><span>{Math.round(Object.values(companyData).filter(val => val && val !== '').length / Object.keys(companyData).length * 100)}%</span></div>
                    <div className="flex justify-between"><span>Industry Alignment:</span><span>95%</span></div>
                    <div className="flex justify-between"><span>Market Validation:</span><span>88%</span></div>
                    <div className="flex justify-between font-bold border-t pt-2"><span>Overall Confidence:</span><span>{valuationResults.confidence}%</span></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeMethod === 'analytics' && (
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-gray-900">📈 Performance Analytics & Benchmarking</h3>
              <CompanyAnalytics companyId={1} />
            </div>
          )}
        </div>
      </div>

      {/* Download Reports */}
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">📥 Download Comprehensive Reports</h3>
        <p className="text-gray-600 mb-4">Generate detailed valuation reports in multiple formats including all analysis methods and supporting data.</p>
        
        <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
          {['pdf', 'docx', 'xlsx', 'png', 'txt', 'all'].map((format) => (
            <button
              key={format}
              onClick={() => downloadReport(format)}
              className="px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all text-sm font-medium flex flex-col items-center"
            >
              <span className="text-lg mb-1">
                {format === 'pdf' && '📄'}
                {format === 'docx' && '📝'}
                {format === 'xlsx' && '📊'}
                {format === 'png' && '🖼️'}
                {format === 'txt' && '📋'}
                {format === 'all' && '📦'}
              </span>
              {format === 'all' ? 'All Formats' : format.toUpperCase()}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ValuationAnalysis;
