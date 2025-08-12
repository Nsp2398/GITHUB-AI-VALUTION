import React, { useState, useEffect } from 'react';

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

const MultiModelValuation: React.FC<ValuationAnalysisProps> = ({ companyData }) => {
  const [activeView, setActiveView] = useState('selection');
  const [selectedModel, setSelectedModel] = useState<string>('');
  const [aiRecommendation, setAiRecommendation] = useState<string>('');
  const [showAllMethods, setShowAllMethods] = useState(false);
  const [valuationResults, setValuationResults] = useState({
    berkus: 0,
    scorecard: 0,
    riskFactor: 0,
    vcMethod: 0,
    dcf: 0,
    comparables: 0,
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

    // 5. DCF Method
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

    // Select best method based on AI recommendation
    const recommendation = getAIRecommendation();
    const methodValues = {
      berkus: berkusValue,
      scorecard: scorecardValue,
      riskFactor: riskFactorValue,
      vcMethod: vcValue,
      dcf: dcfValue,
      comparables: comparablesValue
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
      final: Math.round(finalValue),
      confidence: Math.round(confidence),
      selectedMethod: recommendation.model,
      methodology: recommendation.reasoning
    });
  };

  useEffect(() => {
    // Get AI recommendation immediately
    getAIRecommendation();
  }, []);

  const handleCalculateValuation = () => {
    setActiveView('calculating');
    
    // Call backend API for all methods
    const requestData = {
      company_name: companyData.companyName,
      revenue: companyData.revenue,
      expenses: companyData.expenses,
      growth_rate: companyData.growthRate,
      customers: companyData.customerCount,
      employees: companyData.employees,
      stage: companyData.stage,
      team_experience: companyData.teamExperience,
      product_stage: companyData.productStage,
      market_size: companyData.marketSize,
      traction: companyData.traction
    };

    fetch('http://localhost:5000/api/valuate/all-methods', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('authToken')}`
      },
      body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const results = data.data.results;
        setValuationResults({
          berkus: results.berkus.valuation,
          scorecard: results.scorecard.valuation,
          riskFactor: results.risk_factor.valuation,
          vcMethod: results.vc_method.valuation,
          dcf: results.dcf.valuation,
          comparables: results.comparables.valuation,
          final: data.data.recommended_valuation,
          confidence: results[data.data.recommended_method].confidence,
          selectedMethod: data.data.recommended_method,
          methodology: `AI selected ${data.data.recommended_method} as the most appropriate method based on company stage and data availability.`
        });
        setSelectedModel(data.data.recommended_method);
        setActiveView('results');
      } else {
        console.error('API Error:', data.error);
        // Fallback to local calculation
        setTimeout(() => {
          calculateValuations();
          setActiveView('results');
        }, 2000);
      }
    })
    .catch(error => {
      console.error('Network Error:', error);
      // Fallback to local calculation
      setTimeout(() => {
        calculateValuations();
        setActiveView('results');
      }, 2000);
    });
  };

  const downloadReport = async (format: string) => {
    try {
      console.log('Starting download for format:', format);
      
      const reportData = {
        company_info: {
          name: companyData.companyName,
          arr: parseFloat(companyData.revenue) || 0,
          industry: "Multi-sector",
          employees: parseInt(companyData.employees) || 0,
          customers: parseInt(companyData.customerCount) || 0
        },
        valuation_data: {
          selected_method: valuationResults.selectedMethod,
          methodology: valuationResults.methodology,
          berkus_valuation: valuationResults.berkus,
          scorecard_valuation: valuationResults.scorecard,
          risk_factor_valuation: valuationResults.riskFactor,
          vc_method_valuation: valuationResults.vcMethod,
          dcf_valuation: valuationResults.dcf,
          comparables_valuation: valuationResults.comparables,
          final_valuation: valuationResults.final,
          confidence_score: valuationResults.confidence,
          growth_rate: parseFloat(companyData.growthRate) / 100 || 0
        },
        market_data: {
          market_size: 50000000000,
          growth_rate: 0.12,
          key_trends: ["Digital transformation", "Remote work", "AI adoption", "ESG focus"]
        }
      };

      console.log('Sending request to:', `http://localhost:5000/api/reports/generate`);
      console.log('Report data:', reportData);

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

      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);

      if (response.ok) {
        const blob = await response.blob();
        console.log('Blob received, size:', blob.size);
        
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        const fileExtension = format === 'all' ? 'zip' : format;
        a.download = `${companyData.companyName}_${valuationResults.selectedMethod}_valuation_report.${fileExtension}`;
        
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        alert(`Report downloaded successfully in ${format} format!`);
      } else {
        const errorText = await response.text();
        console.error('Download failed:', response.status, errorText);
        alert(`Report generation failed: ${errorText}`);
      }
    } catch (error) {
      console.error('Report generation error:', error);
      const errorMessage = error instanceof Error ? error.message : String(error);
      alert(`Report generation failed: ${errorMessage}`);
    }
  };

  // Model Selection View
  if (activeView === 'selection') {
    return (
      <div className="space-y-6">
        {/* AI Recommendation */}
        <div className="bg-gradient-to-r from-blue-100 via-purple-100 to-green-100 rounded-2xl p-6 shadow-xl">
          <div className="text-center mb-6">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent">
              🤖 AI Valuation Method Selector
            </h2>
            <p className="text-gray-600 mt-2">Choose the most appropriate valuation method for {companyData.companyName}</p>
          </div>

          {aiRecommendation && (
            <div className="bg-white/70 backdrop-blur-xl rounded-xl p-4 mb-6">
              <h3 className="text-lg font-bold text-green-700 mb-2">🎯 AI Recommendation</h3>
              <p className="text-gray-700 mb-3">{aiRecommendation}</p>
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{valuationModels.find(m => m.id === selectedModel)?.icon}</span>
                <span className="font-semibold text-blue-700">
                  Recommended: {valuationModels.find(m => m.id === selectedModel)?.name}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Method Selection Grid */}
        <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6">
          <div className="flex justify-between items-center mb-6">
            <h3 className="text-xl font-bold text-gray-900">Choose Valuation Method</h3>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setShowAllMethods(!showAllMethods)}
                className="text-sm bg-gray-200 hover:bg-gray-300 px-3 py-1 rounded-lg transition-colors"
              >
                {showAllMethods ? 'Hide Details' : 'Show All Details'}
              </button>
              <button
                onClick={handleCalculateValuation}
                disabled={!selectedModel}
                className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 transition-all"
              >
                Calculate Valuation
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {valuationModels.map((model) => (
              <div
                key={model.id}
                onClick={() => setSelectedModel(model.id)}
                className={`cursor-pointer border-2 rounded-xl p-4 transition-all ${
                  selectedModel === model.id
                    ? 'border-blue-500 bg-blue-50 shadow-lg'
                    : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
                }`}
              >
                <div className="flex items-center space-x-3 mb-3">
                  <span className="text-2xl">{model.icon}</span>
                  <div>
                    <h4 className="font-bold text-gray-900">{model.name}</h4>
                    <span className={`text-xs px-2 py-1 rounded-full ${
                      model.complexity === 'Low' ? 'bg-green-100 text-green-700' :
                      model.complexity === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {model.complexity} Complexity
                    </span>
                  </div>
                </div>
                
                <p className="text-sm text-gray-600 mb-3">{model.description}</p>
                
                {showAllMethods && (
                  <div className="text-xs text-gray-500 space-y-2">
                    <div>
                      <strong>Best for:</strong> {model.bestFor}
                    </div>
                    <div>
                      <strong>Data needed:</strong> {model.dataRequirements.join(', ')}
                    </div>
                    <div>
                      <strong>Stages:</strong> {model.recommendedStages.join(', ')}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // Calculating View
  if (activeView === 'calculating') {
    return (
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-8 text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-6"></div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          🤖 Running {valuationModels.find(m => m.id === selectedModel)?.name} Analysis
        </h3>
        <p className="text-gray-600 mb-4">Calculating valuation using multiple methods...</p>
        <div className="space-y-2 text-sm text-gray-500">
          <p>✓ Processing company data</p>
          <p>✓ Analyzing market conditions</p>
          <p>✓ Applying {valuationModels.find(m => m.id === selectedModel)?.name} methodology</p>
          <p>⏳ Generating comprehensive results</p>
        </div>
      </div>
    );
  }

  // Results View
  return (
    <div className="space-y-6">
      {/* Results Header */}
      <div className="bg-gradient-to-r from-green-100 via-blue-100 to-purple-100 rounded-2xl p-6 shadow-xl">
        <div className="text-center mb-6">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent">
            {companyData.companyName} Valuation Results
          </h2>
          <p className="text-gray-600 mt-2">
            Primary Method: {valuationModels.find(m => m.id === selectedModel)?.name}
          </p>
          <p className="text-sm text-gray-500 mt-1">{valuationResults.methodology}</p>
        </div>
        
        {/* Primary Result */}
        <div className="bg-white/70 backdrop-blur-xl rounded-xl p-6 text-center border-2 border-yellow-400 mb-4">
          <p className="text-4xl font-bold text-orange-600 mb-2">
            ${(valuationResults.final / 1000000).toFixed(1)}M
          </p>
          <p className="text-lg font-medium text-gray-700">Final Valuation</p>
          <p className="text-sm text-gray-500">
            Confidence: {valuationResults.confidence}% | Method: {valuationModels.find(m => m.id === selectedModel)?.name}
          </p>
        </div>

        {/* All Methods Comparison */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {Object.entries(valuationResults).filter(([key]) => 
            ['berkus', 'scorecard', 'riskFactor', 'vcMethod', 'dcf', 'comparables'].includes(key)
          ).map(([method, value]) => {
            const model = valuationModels.find(m => m.id === method);
            const isSelected = method === selectedModel;
            return (
              <div
                key={method}
                className={`bg-white/70 backdrop-blur-xl rounded-xl p-3 text-center ${
                  isSelected ? 'ring-2 ring-blue-500' : ''
                }`}
              >
                <p className="text-xl font-bold text-gray-800">
                  ${(Number(value) / 1000000).toFixed(1)}M
                </p>
                <p className="text-xs text-gray-600">{model?.name || method}</p>
                {isSelected && <p className="text-xs text-blue-600 font-medium">Selected</p>}
              </div>
            );
          })}
        </div>
      </div>

      {/* Methodology Details */}
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          {valuationModels.find(m => m.id === selectedModel)?.icon} {valuationModels.find(m => m.id === selectedModel)?.name} Methodology
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-gray-800 mb-3">Method Overview</h4>
            <div className="space-y-2 text-sm bg-gray-50 p-4 rounded-lg">
              <p><strong>Description:</strong> {valuationModels.find(m => m.id === selectedModel)?.description}</p>
              <p><strong>Best Used For:</strong> {valuationModels.find(m => m.id === selectedModel)?.bestFor}</p>
              <p><strong>Complexity:</strong> {valuationModels.find(m => m.id === selectedModel)?.complexity}</p>
            </div>
          </div>
          
          <div>
            <h4 className="font-semibold text-gray-800 mb-3">Key Assumptions</h4>
            <div className="space-y-2 text-sm bg-blue-50 p-4 rounded-lg">
              {selectedModel === 'berkus' && (
                <>
                  <div className="flex justify-between"><span>Sound Idea Quality:</span><span>50%</span></div>
                  <div className="flex justify-between"><span>Prototype Quality:</span><span>70%</span></div>
                  <div className="flex justify-between"><span>Management Quality:</span><span>80%</span></div>
                  <div className="flex justify-between"><span>Strategic Relationships:</span><span>60%</span></div>
                </>
              )}
              {selectedModel === 'scorecard' && (
                <>
                  <div className="flex justify-between"><span>Regional Average:</span><span>$2.0M</span></div>
                  <div className="flex justify-between"><span>Team Strength:</span><span>125%</span></div>
                  <div className="flex justify-between"><span>Product Quality:</span><span>110%</span></div>
                  <div className="flex justify-between"><span>Market Competitive:</span><span>90%</span></div>
                </>
              )}
              {selectedModel === 'dcf' && (
                <>
                  <div className="flex justify-between"><span>Discount Rate:</span><span>12.0%</span></div>
                  <div className="flex justify-between"><span>Terminal Growth:</span><span>3.0%</span></div>
                  <div className="flex justify-between"><span>Projection Period:</span><span>5 years</span></div>
                  <div className="flex justify-between"><span>Revenue Growth:</span><span>{companyData.growthRate}%</span></div>
                </>
              )}
              {selectedModel === 'vcMethod' && (
                <>
                  <div className="flex justify-between"><span>Required ROI:</span><span>10x</span></div>
                  <div className="flex justify-between"><span>PE Multiple:</span><span>15x</span></div>
                  <div className="flex justify-between"><span>Investor Share:</span><span>25%</span></div>
                  <div className="flex justify-between"><span>Time to Exit:</span><span>5 years</span></div>
                </>
              )}
            </div>
          </div>
        </div>

        <div className="mt-6 flex justify-between">
          <button
            onClick={() => setActiveView('selection')}
            className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
          >
            ← Change Method
          </button>
          <button
            onClick={() => downloadReport('pdf')}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Download Report →
          </button>
        </div>
      </div>

      {/* Download Reports */}
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">📥 Download Comprehensive Reports</h3>
        <p className="text-gray-600 mb-4">
          Generate detailed valuation reports including methodology, assumptions, and comparative analysis.
        </p>
        
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {['pdf', 'docx', 'png', 'txt', 'all'].map((format) => (
            <button
              key={format}
              onClick={() => downloadReport(format)}
              className="px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all text-sm font-medium flex flex-col items-center"
            >
              <span className="text-lg mb-1">
                {format === 'pdf' && '📄'}
                {format === 'docx' && '📝'}
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

export default MultiModelValuation;
