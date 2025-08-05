import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { InputField } from '../components/ui/InputField';
import { Button } from '../components/ui/Button';
import api, { CompanyData, ValuationData } from '../services/api';

const INITIAL_COMPANY_DATA: CompanyData = {
  name: '',
  industry: '',
  description: '',
  revenue: 0,
  ebitda: 0,
  growth_rate: 0,
  profit_margin: 0,
  mrr: 0,
  arpu: 0,
  churn_rate: 0,
  cac: 0,
  ltv: 0
};

const INITIAL_VALUATION_DATA: ValuationData = {
  revenue: 0,
  growth_rate: 0,
  ebitda_margin: 0,
  discount_rate: 0.1, // Default 10%
  terminal_growth_rate: 0.02, // Default 2%
  projection_years: 5
};

const ValuationWizard: React.FC = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [companyData, setCompanyData] = useState<CompanyData>(INITIAL_COMPANY_DATA);
  const [valuationData, setValuationData] = useState<ValuationData>(INITIAL_VALUATION_DATA);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCompanyDataChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCompanyData(prev => ({
      ...prev,
      [name]: name.includes('rate') || name.includes('margin') ? parseFloat(value) / 100 : parseFloat(value) || value
    }));
  };

  const handleValuationDataChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setValuationData(prev => ({
      ...prev,
      [name]: parseFloat(value) || value
    }));
  };

  const handleNext = () => {
    setStep(prev => prev + 1);
  };

  const handleBack = () => {
    setStep(prev => prev - 1);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Create company first
      const companyResponse = await api.createCompany(companyData);
      
      // Calculate valuation
      const valuationResponse = await api.calculateDCF({
        ...valuationData,
        revenue: companyData.revenue,
        growth_rate: companyData.growth_rate,
        mrr: companyData.mrr,
        arpu: companyData.arpu,
        churn_rate: companyData.churn_rate,
        cac: companyData.cac,
        ltv: companyData.ltv
      });

      // Store valuation results
      await api.createValuation(companyResponse.id, {
        ...valuationResponse.dcf_results,
        ai_confidence_score: valuationResponse.ai_insights.confidence_score,
        ai_recommendations: valuationResponse.ai_insights.analysis
      });

      // Navigate to results
      navigate('/dashboard', { 
        state: { 
          companyId: companyResponse.id,
          valuationResults: valuationResponse 
        }
      });
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An error occurred during valuation');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Business Valuation Wizard</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Step 1: Company Information */}
        {step === 1 && (
          <div>
            <h2 className="text-xl font-semibold mb-4">Company Information</h2>
            <InputField
              label="Company Name"
              name="name"
              value={companyData.name}
              onChange={handleCompanyDataChange}
              required
            />
            <InputField
              label="Industry"
              name="industry"
              value={companyData.industry}
              onChange={handleCompanyDataChange}
              required
            />
            <InputField
              label="Description"
              name="description"
              value={companyData.description || ''}
              onChange={handleCompanyDataChange}
            />
            <Button onClick={handleNext}>Next</Button>
          </div>
        )}

        {/* Step 2: Financial Metrics */}
        {step === 2 && (
          <div>
            <h2 className="text-xl font-semibold mb-4">Financial Metrics</h2>
            <InputField
              label="Annual Revenue ($)"
              name="revenue"
              type="number"
              value={companyData.revenue}
              onChange={handleCompanyDataChange}
              required
            />
            <InputField
              label="EBITDA ($)"
              name="ebitda"
              type="number"
              value={companyData.ebitda}
              onChange={handleCompanyDataChange}
              required
            />
            <InputField
              label="Growth Rate (%)"
              name="growth_rate"
              type="number"
              value={companyData.growth_rate * 100}
              onChange={handleCompanyDataChange}
              required
            />
            <div className="flex gap-4">
              <Button onClick={handleBack} variant="secondary">Back</Button>
              <Button onClick={handleNext}>Next</Button>
            </div>
          </div>
        )}

        {/* Step 3: UCaaS Metrics */}
        {step === 3 && (
          <div>
            <h2 className="text-xl font-semibold mb-4">UCaaS Metrics</h2>
            <InputField
              label="Monthly Recurring Revenue ($)"
              name="mrr"
              type="number"
              value={companyData.mrr}
              onChange={handleCompanyDataChange}
              required
            />
            <InputField
              label="Average Revenue Per User ($)"
              name="arpu"
              type="number"
              value={companyData.arpu}
              onChange={handleCompanyDataChange}
              required
            />
            <InputField
              label="Churn Rate (%)"
              name="churn_rate"
              type="number"
              value={companyData.churn_rate * 100}
              onChange={handleCompanyDataChange}
              required
            />
            <InputField
              label="Customer Acquisition Cost ($)"
              name="cac"
              type="number"
              value={companyData.cac}
              onChange={handleCompanyDataChange}
              required
            />
            <div className="flex gap-4">
              <Button onClick={handleBack} variant="secondary">Back</Button>
              <Button onClick={handleNext}>Next</Button>
            </div>
          </div>
        )}

        {/* Step 4: Valuation Parameters */}
        {step === 4 && (
          <div>
            <h2 className="text-xl font-semibold mb-4">Valuation Parameters</h2>
            <InputField
              label="Discount Rate (%)"
              name="discount_rate"
              type="number"
              value={valuationData.discount_rate * 100}
              onChange={handleValuationDataChange}
              required
            />
            <InputField
              label="Terminal Growth Rate (%)"
              name="terminal_growth_rate"
              type="number"
              value={valuationData.terminal_growth_rate * 100}
              onChange={handleValuationDataChange}
              required
            />
            <InputField
              label="Projection Years"
              name="projection_years"
              type="number"
              value={valuationData.projection_years ?? ''}
              onChange={handleValuationDataChange}
              required
            />
            <div className="flex gap-4">
              <Button onClick={handleBack} variant="secondary">Back</Button>
              <Button type="submit" variant="success" disabled={loading}>
                {loading ? 'Calculating...' : 'Calculate Valuation'}
              </Button>
            </div>
          </div>
        )}
      </form>
    </div>
  );
};

export default ValuationWizard;
