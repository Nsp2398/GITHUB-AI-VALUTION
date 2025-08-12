import React, { useState, useCallback } from 'react';
import { ChartBarIcon, CpuChipIcon, CalculatorIcon, DocumentArrowDownIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import { FileUpload } from '../components/ui/FileUpload';
import { Button } from '../components/ui/Button';
import { InputField } from '../components/ui/InputField';

interface ComprehensiveValuationData {
  company_name: string;
  revenue: number;
  growth_rate: number;
  ebitda_margin: number;
  discount_rate: number;
  terminal_growth_rate: number;
  mrr: number;
  arpu: number;
  customers: number;
  churn_rate: number;
  cac: number;
  gross_margin: number;
  expansion_revenue: number;
  support_costs: number;
  market_position: string;
  technology_score: number;
  historical_revenue: number[];
}

interface ValuationResults {
  company_info: any;
  valuation_methods: {
    dcf: any;
    ucaas_metrics: any;
    ai_powered: any;
  };
  recommended_valuation: any;
  valuation_range: any;
  summary: any;
}

export const ComprehensiveValuationWizard: React.FC = () => {
  const [step, setStep] = useState(1);
  const [valuationData, setValuationData] = useState<ComprehensiveValuationData>({
    company_name: '',
    revenue: 0,
    growth_rate: 20,
    ebitda_margin: 15,
    discount_rate: 12,
    terminal_growth_rate: 3,
    mrr: 0,
    arpu: 0,
    customers: 0,
    churn_rate: 5,
    cac: 0,
    gross_margin: 70,
    expansion_revenue: 0,
    support_costs: 10,
    market_position: 'average',
    technology_score: 5,
    historical_revenue: []
  });
  const [results, setResults] = useState<ValuationResults | null>(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (field: keyof ComprehensiveValuationData, value: any) => {
    setValuationData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleFileUpload = useCallback(async (files: File[]) => {
    if (files.length === 0) return;

    const formData = new FormData();
    formData.append('file', files[0]);

    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('/api/upload-financial-data', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        setResults(data.results);
        setStep(4); // Jump to results
        // alert('Failed to upload and process file'); // This alert seems misplaced, consider removing or moving it to the error block
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Error uploading file');
    } finally {
      setLoading(false);
    }
  }, []);

  const performComprehensiveValuation = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('/api/comprehensive-valuation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(valuationData)
      });

      if (response.ok) {
        const data = await response.json();
        setResults(data.results);
        setStep(4);
      } else {
        alert('Failed to perform valuation');
      }
    } catch (error) {
      console.error('Valuation error:', error);
      alert('Error performing valuation');
    } finally {
      setLoading(false);
    }
  };

  const generateComprehensiveReport = async (format: string) => {
    if (!results) return;

    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch('/api/generate-comprehensive-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          valuation_results: results,
          format: format
        })
      });

      if (response.ok) {
        const data = await response.json();
        if (format === 'all') {
          // Download all formats as ZIP
          const zipResponse = await fetch(`/api/reports/download-zip`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          if (zipResponse.ok) {
            const blob = await zipResponse.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'comprehensive_valuation_report.zip';
            a.click();
          }
        } else {
          // Download single format
          const filePath = data.file_paths[format];
          const downloadResponse = await fetch(`/api/reports/download/${filePath.split('/').pop()}`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          if (downloadResponse.ok) {
            const blob = await downloadResponse.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filePath.split('/').pop();
            a.click();
          }
        }
      } else {
        alert('Failed to generate report');
      }
    } catch (error) {
      console.error('Report generation error:', error);
      alert('Error generating report');
    } finally {
      setLoading(false);
    }
  };

  const renderStep1 = () => (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          🏆 Comprehensive UCaaS Valuation
        </h2>
        <p className="text-lg text-gray-600 mb-8">
          Get your business valued using three industry-standard methods with AI-powered recommendations
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Option 1: Upload Financial Data */}
        <div className="bg-white p-6 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 transition-colors">
          <h3 className="text-xl font-semibold mb-4 flex items-center">
            📊 Upload Financial Data
          </h3>
          <p className="text-gray-600 mb-4">
            Upload your raw financial data (Excel, CSV) and let ValuAI automatically process and evaluate your business.
          </p>
          <FileUpload
            onFileSelect={handleFileUpload}
            acceptedTypes={[".csv", ".xlsx", ".xls"]}
            maxFiles={1}
            className="h-40"
          />
          <div className="mt-4 text-sm text-gray-500">
            <p>✅ Automatic metric extraction</p>
            <p>✅ All three valuation methods</p>
            <p>✅ Instant results</p>
          </div>
        </div>

        {/* Option 2: Manual Entry */}
        <div className="bg-white p-6 border-2 border-solid border-gray-300 rounded-lg">
          <h3 className="text-xl font-semibold mb-4 flex items-center">
            ✏️ Manual Data Entry
          </h3>
          <p className="text-gray-600 mb-4">
            Enter your financial metrics manually for precise control over the valuation inputs.
          </p>
          <Button
            onClick={() => setStep(2)}
            className="w-full mb-4"
          >
            Start Manual Entry
          </Button>
          <div className="text-sm text-gray-500">
            <p>✅ Complete control over inputs</p>
            <p>✅ Step-by-step guidance</p>
            <p>✅ Detailed explanations</p>
          </div>
        </div>
      </div>

      {/* Three Methods Overview */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-8 rounded-lg">
        <h3 className="text-2xl font-bold text-center mb-6">
          🔍 Three Industry-Standard Valuation Methods
        </h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <CalculatorIcon className="h-12 w-12 mx-auto mb-3 text-blue-600" />
            <h4 className="font-semibold text-lg mb-2">💼 DCF Valuation</h4>
            <p className="text-sm text-gray-600">
              Projects future cash flows over 5 years with terminal value analysis
            </p>
          </div>
          <div className="text-center">
            <ChartBarIcon className="h-12 w-12 mx-auto mb-3 text-green-600" />
            <h4 className="font-semibold text-lg mb-2">📊 UCaaS Metrics</h4>
            <p className="text-sm text-gray-600">
              Uses MRR, CAC, LTV, and industry benchmarks for SaaS-specific valuation
            </p>
          </div>
          <div className="text-center">
            <CpuChipIcon className="h-12 w-12 mx-auto mb-3 text-purple-600" />
            <h4 className="font-semibold text-lg mb-2">🤖 AI-Powered</h4>
            <p className="text-sm text-gray-600">
              Machine learning analysis with qualitative factors and market sentiment
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Company & Basic Information
        </h2>
        <p className="text-gray-600">Enter your company's basic details</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <InputField
          label="Company Name"
          name="company_name"
          type="text"
          value={valuationData.company_name}
          onChange={(e) => handleInputChange('company_name', e.target.value)}
          placeholder="Enter company name"
        />

        <InputField
          label="Annual Revenue ($)"
          name="revenue"
          type="number"
          value={valuationData.revenue}
          onChange={(e) => handleInputChange('revenue', Number(e.target.value))}
          placeholder="1000000"
        />

        <InputField
          label="Monthly Recurring Revenue ($)"
          name="mrr"
          type="number"
          value={valuationData.mrr}
          onChange={(e) => handleInputChange('mrr', Number(e.target.value))}
          placeholder="100000"
        />

        <InputField
          label="Number of Customers"
          name="customers"
          type="number"
          value={valuationData.customers}
          onChange={(e) => handleInputChange('customers', Number(e.target.value))}
          placeholder="1000"
        />

        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Market Position
          </label>
          <select
            value={valuationData.market_position}
            onChange={(e) => handleInputChange('market_position', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="leader">Market Leader</option>
            <option value="challenger">Challenger</option>
            <option value="average">Average Player</option>
            <option value="niche">Niche Player</option>
          </select>
        </div>
      </div>

      <div className="flex justify-between">
        <Button variant="secondary" onClick={() => setStep(1)}>
          Back
        </Button>
        <Button onClick={() => setStep(3)}>
          Next: Financial Metrics
        </Button>
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Financial & UCaaS Metrics
        </h2>
        <InputField
          label="Growth Rate (%)"
          name="growth_rate"
          type="number"
          value={valuationData.growth_rate}
          onChange={(e) => handleInputChange('growth_rate', Number(e.target.value))}
          placeholder="20"
        />

        <InputField
          label="EBITDA Margin (%)"
          name="ebitda_margin"
          type="number"
          value={valuationData.ebitda_margin}
          onChange={(e) => handleInputChange('ebitda_margin', Number(e.target.value))}
          placeholder="15"
        />

        <InputField
          label="Gross Margin (%)"
          name="gross_margin"
          type="number"
          value={valuationData.gross_margin}
          onChange={(e) => handleInputChange('gross_margin', Number(e.target.value))}
          placeholder="70"
        />

        <InputField
          label="Monthly Churn Rate (%)"
          name="churn_rate"
          type="number"
          value={valuationData.churn_rate}
          onChange={(e) => handleInputChange('churn_rate', Number(e.target.value))}
          placeholder="5"
        />

        <InputField
          label="Customer Acquisition Cost ($)"
          name="cac"
          type="number"
          value={valuationData.cac}
          onChange={(e) => handleInputChange('cac', Number(e.target.value))}
          placeholder="500"
        />

        <InputField
          label="Average Revenue Per User ($)"
          name="arpu"
          type="number"
          value={valuationData.arpu}
          onChange={(e) => handleInputChange('arpu', Number(e.target.value))}
          placeholder="100"
        />

        <InputField
          label="Discount Rate (%)"
          name="discount_rate"
          type="number"
          value={valuationData.discount_rate}
          onChange={(e) => handleInputChange('discount_rate', Number(e.target.value))}
          placeholder="12"
        />

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Technology Score (1-10)
          </label>
          <input
            type="range"
            min="1"
            max="10"
            value={valuationData.technology_score}
            onChange={(e) => handleInputChange('technology_score', Number(e.target.value))}
            className="w-full"
          />
          <div className="text-center text-sm text-gray-600 mt-1">
            {valuationData.technology_score}/10
          </div>
        </div>
      </div>

      <div className="flex justify-between">
        <Button variant="secondary" onClick={() => setStep(2)}>
          Back
        </Button>
        <Button onClick={performComprehensiveValuation} disabled={loading}>
          {loading ? 'Calculating...' : 'Calculate Valuation'}
        </Button>
      </div>
    </div>
  );

  const renderResults = () => {
    if (!results) return null;

    const { valuation_methods, valuation_range, summary } = results;

    return (
      <div className="space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            🏆 Valuation Results
          </h2>
          <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg">
            <div className="text-4xl font-bold text-green-600 mb-2">
              ${summary.final_valuation?.toLocaleString() || 'N/A'}
            </div>
            <div className="text-lg text-gray-700 mb-2">
              Recommended using: <span className="font-semibold">{summary.method_used}</span>
            </div>
            <div className="text-sm text-gray-600">
              Confidence Level: <span className="font-medium">{summary.confidence_level}</span>
            </div>
          </div>
        </div>

        {/* Three Methods Comparison */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className={`p-6 rounded-lg border-2 ${summary.method_used === 'DCF Valuation' ? 'border-green-500 bg-green-50' : 'border-gray-200 bg-white'}`}>
            <div className="text-center">
              <CalculatorIcon className="h-8 w-8 mx-auto mb-2 text-blue-600" />
              <h3 className="font-semibold text-lg mb-2">💼 DCF Valuation</h3>
              <div className="text-2xl font-bold text-blue-600 mb-2">
                ${valuation_methods.dcf.valuation?.toLocaleString() || 'N/A'}
              </div>
              <div className="text-sm text-gray-600">
                Confidence: {(valuation_methods.dcf.confidence_score * 100).toFixed(0)}%
              </div>
              {summary.method_used === 'DCF Valuation' && (
                <CheckCircleIcon className="h-6 w-6 mx-auto mt-2 text-green-600" />
              )}
            </div>
          </div>

          <div className={`p-6 rounded-lg border-2 ${summary.method_used === 'UCaaS Metrics' ? 'border-green-500 bg-green-50' : 'border-gray-200 bg-white'}`}>
            <div className="text-center">
              <ChartBarIcon className="h-8 w-8 mx-auto mb-2 text-green-600" />
              <h3 className="font-semibold text-lg mb-2">📊 UCaaS Metrics</h3>
              <div className="text-2xl font-bold text-green-600 mb-2">
                ${valuation_methods.ucaas_metrics.valuation?.toLocaleString() || 'N/A'}
              </div>
              <div className="text-sm text-gray-600">
                Confidence: {(valuation_methods.ucaas_metrics.confidence_score * 100).toFixed(0)}%
              </div>
              {summary.method_used === 'UCaaS Metrics' && (
                <CheckCircleIcon className="h-6 w-6 mx-auto mt-2 text-green-600" />
              )}
            </div>
          </div>

          <div className={`p-6 rounded-lg border-2 ${summary.method_used === 'AI-Powered' ? 'border-green-500 bg-green-50' : 'border-gray-200 bg-white'}`}>
            <div className="text-center">
              <CpuChipIcon className="h-8 w-8 mx-auto mb-2 text-purple-600" />
              <h3 className="font-semibold text-lg mb-2">🤖 AI-Powered</h3>
              <div className="text-2xl font-bold text-purple-600 mb-2">
                ${valuation_methods.ai_powered.valuation?.toLocaleString() || 'N/A'}
              </div>
              <div className="text-sm text-gray-600">
                Confidence: {(valuation_methods.ai_powered.confidence_score * 100).toFixed(0)}%
              </div>
              {summary.method_used === 'AI-Powered' && (
                <CheckCircleIcon className="h-6 w-6 mx-auto mt-2 text-green-600" />
              )}
            </div>
          </div>
        </div>

        {/* Justification */}
        <div className="bg-blue-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold mb-3">💡 Why This Valuation Method?</h3>
          <p className="text-gray-700">{summary.justification}</p>
        </div>

        {/* Valuation Range */}
        {valuation_range && (
          <div className="bg-gray-50 p-6 rounded-lg">
            <h3 className="text-lg font-semibold mb-3">📊 Valuation Range Analysis</h3>
            <div className="grid grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-sm text-gray-600">Low</div>
                <div className="text-lg font-bold">${valuation_range.low?.toLocaleString()}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Average</div>
                <div className="text-lg font-bold">${valuation_range.average?.toLocaleString()}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">High</div>
                <div className="text-lg font-bold">${valuation_range.high?.toLocaleString()}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Recommended</div>
                <div className="text-lg font-bold text-green-600">${summary.final_valuation?.toLocaleString()}</div>
              </div>
            </div>
          </div>
        )}

        {/* Report Download Options */}
        <div className="bg-white p-6 border rounded-lg">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <DocumentArrowDownIcon className="h-6 w-6 mr-2" />
            Download Comprehensive Report
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <Button
              onClick={() => generateComprehensiveReport('pdf')}
              disabled={loading}
              variant="secondary"
              className="text-red-600 border-red-300 hover:bg-red-50"
            >
              📄 PDF
            </Button>
            <Button
              onClick={() => generateComprehensiveReport('docx')}
              disabled={loading}
              variant="secondary"
              className="text-blue-600 border-blue-300 hover:bg-blue-50"
            >
              📝 Word
            </Button>
            <Button
              onClick={() => generateComprehensiveReport('txt')}
              disabled={loading}
              variant="secondary"
              className="text-gray-600 border-gray-300 hover:bg-gray-50"
            >
              📄 Text
            </Button>
            <Button
              onClick={() => generateComprehensiveReport('png')}
              disabled={loading}
              variant="secondary"
              className="text-purple-600 border-purple-300 hover:bg-purple-50"
            >
              🖼️ Image
            </Button>
            <Button
              onClick={() => generateComprehensiveReport('all')}
              disabled={loading}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white"
            >
              📦 All Formats
            </Button>
          </div>
        </div>

        <div className="text-center">
          <Button
            onClick={() => {
              setStep(1);
              setResults(null);
              setValuationData({
                company_name: '',
                revenue: 0,
                growth_rate: 20,
                ebitda_margin: 15,
                discount_rate: 12,
                terminal_growth_rate: 3,
                mrr: 0,
                arpu: 0,
                customers: 0,
                churn_rate: 5,
                cac: 0,
                gross_margin: 70,
                expansion_revenue: 0,
                support_costs: 10,
                market_position: 'average',
                technology_score: 5,
                historical_revenue: []
              });
            }}
            variant="secondary"
          >
            Start New Valuation
          </Button>
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      {step === 1 && renderStep1()}
      {step === 2 && renderStep2()}
      {step === 3 && renderStep3()}
      {step === 4 && renderResults()}
    </div>
  );
};
