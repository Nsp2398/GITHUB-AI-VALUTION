import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { useAuth } from './contexts/AuthContext';
import { useState } from 'react';
import MultiModelValuation from './components/MultiModelValuation';
import RealTimeDashboard from './components/RealTimeDashboard';

// Authentication Form Component
const AuthForm = ({ onAuthSuccess }: { onAuthSuccess: (authData: any) => void }) => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [usePhone, setUsePhone] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
      if (isSignUp) {
        // Sign Up
        if (formData.password !== formData.confirmPassword) {
          setError('Passwords do not match');
          setIsLoading(false);
          return;
        }

        const response = await fetch('http://localhost:5000/api/auth/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            firstName: formData.firstName,
            lastName: formData.lastName,
            email: usePhone ? formData.phone : formData.email,
            password: formData.password
          }),
        });

        if (response.ok) {
          const authData = await response.json();
          console.log('Signup successful:', authData);
          onAuthSuccess(authData);
        } else {
          const errorData = await response.json();
          setError(errorData.error || 'Registration failed');
        }
      } else {
        // Sign In
        const response = await fetch('http://localhost:5000/api/auth/signin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: usePhone ? formData.phone : formData.email,
            password: formData.password
          }),
        });

        if (response.ok) {
          const authData = await response.json();
          console.log('Login successful:', authData);
          onAuthSuccess(authData);
        } else {
          const errorData = await response.json();
          setError(errorData.error || 'Login failed');
        }
      }
    } catch (error) {
      console.error('Auth error:', error);
      setError('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const fillTestCredentials = () => {
    setFormData({
      ...formData,
      email: 'nsp6575@gmail.com',
      password: 'Newpassword123'
    });
    setUsePhone(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            ValuAI
          </h1>
          <p className="text-gray-600 mt-2">
            {isSignUp ? 'Create your account' : 'Sign in to your account'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {isSignUp && (
            <>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                  <input
                    type="text"
                    value={formData.firstName}
                    onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                  <input
                    type="text"
                    value={formData.lastName}
                    onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    required
                  />
                </div>
              </div>
            </>
          )}

          <div>
            <div className="flex items-center mb-2">
              <label className="block text-sm font-medium text-gray-700">
                {usePhone ? 'Phone Number' : 'Email Address'}
              </label>
              <button
                type="button"
                onClick={() => setUsePhone(!usePhone)}
                className="ml-auto text-sm text-blue-600 hover:text-blue-800"
              >
                Use {usePhone ? 'Email' : 'Phone'} instead
              </button>
            </div>
            {usePhone ? (
              <input
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                placeholder="+1 (555) 123-4567"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                required
              />
            ) : (
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="your@email.com"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                required
              />
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              required
            />
          </div>

          {isSignUp && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
              <input
                type="password"
                value={formData.confirmPassword}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                required
              />
            </div>
          )}

          {error && (
            <div className="p-3 bg-red-100 border border-red-300 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 px-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-purple-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                {isSignUp ? 'Creating Account...' : 'Signing in...'}
              </div>
            ) : (
              isSignUp ? 'Create Account' : 'Sign In'
            )}
          </button>
        </form>

        <div className="mt-6 text-center">
          <button
            onClick={() => setIsSignUp(!isSignUp)}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            {isSignUp ? 'Already have an account? Sign in' : 'Need an account? Sign up'}
          </button>
          
          {!isSignUp && (
            <div className="mt-2">
              <button
                onClick={fillTestCredentials}
                className="text-xs text-gray-500 hover:text-gray-700"
              >
                Fill test credentials (nsp6575@gmail.com)
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// File Upload Component
const FileUploadSection = () => {
  // 🚀 Comprehensive 2025 Industry categorization configuration
  const industryCategories = {
    retail: {
      name: 'Retail',
      subIndustries: {
        gas_station: 'Gas Station',
        grocery_store: 'Grocery Store', 
        liquor_store: 'Liquor Store',
        clothing_store: 'Clothing Store',
        pharmacy: 'Pharmacy',
        convenience_store: 'Convenience Store',
        restaurant: 'Restaurant',
        coffee_shop: 'Coffee Shop',
        luxury_retail: 'Luxury Retail',
        ecommerce_marketplace: 'E-commerce Marketplace'
      }
    },
    technology: {
      name: 'Technology',
      subIndustries: {
        saas_enterprise: 'SaaS/Enterprise Software',
        ai_ml_platform: 'AI/ML Platform',
        cybersecurity: 'Cybersecurity',
        fintech_payments: 'FinTech/Payments',
        ucaas: 'UCaaS/Communications',
        ecommerce: 'E-commerce Platform',
        mobile_apps: 'Mobile Apps',
        healthtech: 'HealthTech'
      }
    },
    healthcare_life_sciences: {
      name: 'Healthcare & Life Sciences',
      subIndustries: {
        digital_health_platform: 'Digital Health Platform',
        biotech_drug_development: 'Biotech/Drug Development',
        medical_devices: 'Medical Devices',
        telemedicine: 'Telemedicine',
        clinic: 'Medical Clinic',
        dental: 'Dental Practice',
        veterinary: 'Veterinary Clinic',
        mental_health: 'Mental Health Services',
        physical_therapy: 'Physical Therapy',
        home_healthcare: 'Home Healthcare'
      }
    },
    financial_services: {
      name: 'Financial Services',
      subIndustries: {
        wealth_management: 'Wealth Management',
        insurance_technology: 'Insurance Technology',
        robo_advisory: 'Robo-Advisory',
        banking_services: 'Banking Services',
        payment_processing: 'Payment Processing',
        lending_platform: 'Lending Platform',
        investment_management: 'Investment Management',
        financial_advisory: 'Financial Advisory'
      }
    },
    real_estate_proptech: {
      name: 'Real Estate & PropTech',
      subIndustries: {
        property_management_saas: 'Property Management SaaS',
        real_estate_marketplace: 'Real Estate Marketplace',
        commercial_real_estate: 'Commercial Real Estate',
        residential_development: 'Residential Development',
        real_estate_investment: 'Real Estate Investment',
        construction_tech: 'Construction Technology'
      }
    },
    energy_utilities: {
      name: 'Energy & Utilities',
      subIndustries: {
        renewable_energy_developer: 'Renewable Energy Developer',
        energy_storage: 'Energy Storage',
        solar_development: 'Solar Development',
        wind_energy: 'Wind Energy',
        energy_efficiency: 'Energy Efficiency',
        grid_technology: 'Grid Technology',
        carbon_management: 'Carbon Management'
      }
    },
    education_training: {
      name: 'Education & Training',
      subIndustries: {
        edtech_platform: 'EdTech Platform',
        corporate_training: 'Corporate Training',
        online_education: 'Online Education',
        skill_development: 'Skill Development',
        certification_programs: 'Certification Programs',
        language_learning: 'Language Learning'
      }
    },
    logistics_transport: {
      name: 'Logistics & Transportation',
      subIndustries: {
        last_mile_delivery: 'Last Mile Delivery',
        freight_technology: 'Freight Technology',
        supply_chain_management: 'Supply Chain Management',
        warehouse_automation: 'Warehouse Automation',
        logistics_platform: 'Logistics Platform',
        transportation_services: 'Transportation Services'
      }
    },
    professional_services: {
      name: 'Professional Services',
      subIndustries: {
        consulting: 'Consulting',
        accounting: 'Accounting',
        legal: 'Legal Services',
        marketing: 'Marketing Agency',
        architecture: 'Architecture',
        engineering: 'Engineering',
        design_services: 'Design Services',
        business_services: 'Business Services'
      }
    },
    manufacturing: {
      name: 'Manufacturing',
      subIndustries: {
        advanced_manufacturing: 'Advanced Manufacturing',
        pharmaceutical_manufacturing: 'Pharmaceutical Manufacturing',
        automotive: 'Automotive',
        food_beverage: 'Food & Beverage',
        electronics: 'Electronics',
        textiles: 'Textiles',
        chemicals: 'Chemicals',
        machinery: 'Machinery',
        packaging: 'Packaging',
        metal_fabrication: 'Metal Fabrication'
      }
    }
  };

  // Get sub-industries for selected industry
  const getSubIndustries = (industry: string) => {
    return industryCategories[industry as keyof typeof industryCategories]?.subIndustries || {};
  };

  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [currentStep, setCurrentStep] = useState(1); // 1: Upload, 2: Data Review, 3: Valuation Methods
  const [manualData, setManualData] = useState({
    companyName: '',
    revenue: '',
    growthRate: '',
    expenses: '',
    industry: 'retail',
    subIndustry: 'gas_station',
    employees: '',
    marketShare: '',
    customerCount: '',
    churnRate: '',
    cac: '',
    ltv: '',
    stage: 'growth',
    teamExperience: 'medium',
    productStage: 'market',
    marketSize: 'medium',
    traction: 'moderate'
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleUpload = async () => {
    setUploading(true);
    const formData = new FormData();
    
    files.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('/api/files/upload-batch', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setUploadComplete(true);
        setCurrentStep(2);
        setFiles([]);
        // Pre-fill some sample data
        setManualData({
          ...manualData,
          companyName: 'Sample UCaaS Corp',
          revenue: '5000000',
          growthRate: '35',
          expenses: '3500000',
          employees: '150',
          customerCount: '1200',
          churnRate: '8',
          cac: '1200',
          ltv: '5000'
        });
      } else {
        alert('Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const proceedToValuation = () => {
    if (!manualData.companyName || !manualData.revenue) {
      alert('Please fill in at least Company Name and Revenue');
      return;
    }
    setCurrentStep(3);
  };

  const supportedFormats = ['PDF', 'Word (.doc, .docx)', 'Excel (.xls, .xlsx)', 'Images (.jpg, .png)', 'Text (.txt, .csv)'];

  if (currentStep === 3) {
    return <MultiModelValuation companyData={manualData} />;
  }

  return (
    <div className="space-y-6">
      {/* Progress Indicator */}
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-gray-900">Valuation Process</h3>
          <span className="text-sm text-gray-600">Step {currentStep} of 3</span>
        </div>
        <div className="flex items-center space-x-4">
          <div className={`flex items-center space-x-2 ${currentStep >= 1 ? 'text-blue-600' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${currentStep >= 1 ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}>1</div>
            <span className="text-sm font-medium">Upload Data</span>
          </div>
          <div className={`w-8 h-1 ${currentStep >= 2 ? 'bg-blue-600' : 'bg-gray-300'} rounded`}></div>
          <div className={`flex items-center space-x-2 ${currentStep >= 2 ? 'text-blue-600' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${currentStep >= 2 ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}>2</div>
            <span className="text-sm font-medium">Review Data</span>
          </div>
          <div className={`w-8 h-1 ${currentStep >= 3 ? 'bg-blue-600' : 'bg-gray-300'} rounded`}></div>
          <div className={`flex items-center space-x-2 ${currentStep >= 3 ? 'text-blue-600' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${currentStep >= 3 ? 'bg-blue-600 text-white' : 'bg-gray-300'}`}>3</div>
            <span className="text-sm font-medium">Valuation</span>
          </div>
        </div>
      </div>

      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6">
        {currentStep === 1 && (
          <>
            <h3 className="text-xl font-bold text-gray-900 mb-4">📁 Step 1: Upload Your Data</h3>
            
            {/* File Upload */}
            <div className="mb-6">
              <h4 className="text-lg font-semibold text-gray-800 mb-3">Upload Financial Documents</h4>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-500 transition-colors">
                <input
                  type="file"
                  multiple
                  onChange={handleFileChange}
                  accept=".pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.txt,.csv"
                  className="hidden"
                  id="fileInput"
                />
                <label htmlFor="fileInput" className="cursor-pointer">
                  <div className="text-gray-600 mb-2">
                    <span className="text-2xl">📄</span>
                  </div>
                  <p className="text-gray-700 font-medium">Click to select files</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Supported: {supportedFormats.join(', ')}
                  </p>
                </label>
              </div>

              {files.length > 0 && (
                <div className="mt-4">
                  <h5 className="font-medium text-gray-700 mb-2">Selected Files:</h5>
                  <div className="space-y-2">
                    {files.map((file, index) => (
                      <div key={index} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                        <span className="text-sm text-gray-700">{file.name}</span>
                        <span className="text-xs text-gray-500">{(file.size / 1024).toFixed(1)} KB</span>
                      </div>
                    ))}
                  </div>
                  <button
                    onClick={handleUpload}
                    disabled={uploading}
                    className="mt-3 px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
                  >
                    {uploading ? 'Uploading...' : `Upload ${files.length} file(s) & Continue`}
                  </button>
                </div>
              )}

              {/* Skip Upload Option */}
              <div className="mt-6 text-center">
                <button
                  onClick={() => setCurrentStep(2)}
                  className="text-blue-600 hover:text-blue-800 text-sm"
                >
                  Skip upload and enter data manually →
                </button>
              </div>
            </div>
          </>
        )}

        {currentStep === 2 && (
          <>
            <h3 className="text-xl font-bold text-gray-900 mb-4">📊 Step 2: Review & Complete Company Data</h3>
            
            {uploadComplete && (
              <div className="mb-4 p-3 bg-green-100 border border-green-300 text-green-700 rounded-lg text-sm">
                ✅ Files uploaded successfully! Please review and complete the extracted data below.
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Company Name *</label>
                <input
                  type="text"
                  value={manualData.companyName}
                  onChange={(e) => setManualData({ ...manualData, companyName: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="Your Company Ltd."
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Industry Type *</label>
                <select
                  value={manualData.industry}
                  onChange={(e) => {
                    const newIndustry = e.target.value;
                    const subIndustries = getSubIndustries(newIndustry);
                    const firstSubIndustry = Object.keys(subIndustries)[0] || '';
                    setManualData({ 
                      ...manualData, 
                      industry: newIndustry,
                      subIndustry: firstSubIndustry
                    });
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                >
                  {Object.entries(industryCategories).map(([key, category]) => (
                    <option key={key} value={key}>{category.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Sub-Industry *</label>
                <select
                  value={manualData.subIndustry}
                  onChange={(e) => setManualData({ ...manualData, subIndustry: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                >
                  {Object.entries(getSubIndustries(manualData.industry)).map(([key, name]) => (
                    <option key={key} value={key}>{name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Annual Revenue ($) *</label>
                <input
                  type="number"
                  value={manualData.revenue}
                  onChange={(e) => setManualData({ ...manualData, revenue: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="5000000"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Growth Rate (%)</label>
                <input
                  type="number"
                  value={manualData.growthRate}
                  onChange={(e) => setManualData({ ...manualData, growthRate: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="35"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Annual Expenses ($)</label>
                <input
                  type="number"
                  value={manualData.expenses}
                  onChange={(e) => setManualData({ ...manualData, expenses: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="3000000"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Number of Employees</label>
                <input
                  type="number"
                  value={manualData.employees}
                  onChange={(e) => setManualData({ ...manualData, employees: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="150"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Customer Count</label>
                <input
                  type="number"
                  value={manualData.customerCount}
                  onChange={(e) => setManualData({ ...manualData, customerCount: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="1200"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Churn Rate (%)</label>
                <input
                  type="number"
                  value={manualData.churnRate}
                  onChange={(e) => setManualData({ ...manualData, churnRate: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="8"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Customer Acquisition Cost ($)</label>
                <input
                  type="number"
                  value={manualData.cac}
                  onChange={(e) => setManualData({ ...manualData, cac: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="1200"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Customer Lifetime Value ($)</label>
                <input
                  type="number"
                  value={manualData.ltv}
                  onChange={(e) => setManualData({ ...manualData, ltv: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="5000"
                />
              </div>
            </div>

            {/* New Valuation Model Fields */}
            <div className="bg-blue-50 p-4 rounded-lg mt-6">
              <h4 className="text-lg font-semibold text-gray-800 mb-3">📊 Additional Valuation Data</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Company Stage</label>
                  <select
                    value={manualData.stage}
                    onChange={(e) => setManualData({ ...manualData, stage: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="idea">Idea Stage</option>
                    <option value="pre-revenue">Pre-Revenue</option>
                    <option value="mvp">MVP</option>
                    <option value="early-revenue">Early Revenue</option>
                    <option value="growth">Growth Stage</option>
                    <option value="expansion">Expansion</option>
                    <option value="mature">Mature</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Team Experience</label>
                  <select
                    value={manualData.teamExperience}
                    onChange={(e) => setManualData({ ...manualData, teamExperience: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="low">Low Experience</option>
                    <option value="medium">Medium Experience</option>
                    <option value="high">High Experience</option>
                    <option value="expert">Expert Level</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Product Stage</label>
                  <select
                    value={manualData.productStage}
                    onChange={(e) => setManualData({ ...manualData, productStage: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="concept">Concept</option>
                    <option value="development">Development</option>
                    <option value="mvp">MVP</option>
                    <option value="beta">Beta</option>
                    <option value="market">Market Ready</option>
                    <option value="mature">Mature Product</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Market Size</label>
                  <select
                    value={manualData.marketSize}
                    onChange={(e) => setManualData({ ...manualData, marketSize: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="small">Small Market</option>
                    <option value="medium">Medium Market</option>
                    <option value="large">Large Market</option>
                    <option value="massive">Massive Market</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Market Traction</label>
                  <select
                    value={manualData.traction}
                    onChange={(e) => setManualData({ ...manualData, traction: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="none">No Traction</option>
                    <option value="minimal">Minimal Traction</option>
                    <option value="moderate">Moderate Traction</option>
                    <option value="strong">Strong Traction</option>
                    <option value="excellent">Excellent Traction</option>
                  </select>
                </div>
              </div>
            </div>
            
            <div className="mt-6 flex justify-between">
              <button
                onClick={() => setCurrentStep(1)}
                className="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                ← Back to Upload
              </button>
              <button
                onClick={proceedToValuation}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Proceed to Valuation →
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

// Report Generation Component
const ReportGeneration = () => {
  const [generating, setGenerating] = useState(false);
  const [reportData] = useState({
    companyName: "Sample UCaaS Company",
    valuation: 75000000,
    revenue: 5000000,
    growthRate: 35,
    confidence: 92
  });

  const generateReport = async (format: string) => {
    setGenerating(true);
    
    try {
      const sampleData = {
        companyName: reportData.companyName,
        industry: "UCaaS",
        revenue: parseFloat(reportData.revenue.toString()) || 5000000,
        growthRate: parseFloat(reportData.growthRate.toString()) / 100 || 0.35,
        ebitdaMargin: 0.25,
        format: format
      };

      const response = await fetch('/api/reports/generate-direct', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify(sampleData),
      });

      if (response.ok) {
        const blob = await response.blob();
        
        // Check if blob is actually a JSON error response
        if (blob.type === 'application/json') {
          const text = await blob.text();
          console.error('Received JSON error:', text);
          alert('Report generation failed: ' + text);
          return;
        }
        
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        const fileExtension = format === 'all' ? 'zip' : format;
        a.download = `${reportData.companyName}_valuation_report.${fileExtension}`;
        
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        alert(`Report downloaded successfully in ${format} format!`);
      } else {
        const errorText = await response.text();
        console.error('Report generation failed:', errorText);
        alert('Report generation failed: ' + errorText);
      }
    } catch (error) {
      console.error('Report generation error:', error);
      alert('Report generation failed');
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6">
      <h3 className="text-xl font-bold text-gray-900 mb-4">📊 Valuation Results</h3>
      
      <div className="bg-gradient-to-r from-green-100 to-blue-100 rounded-lg p-4 mb-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <p className="text-2xl font-bold text-gray-800">${(reportData.valuation / 1000000).toFixed(1)}M</p>
            <p className="text-sm text-gray-600">Company Valuation</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-800">${(reportData.revenue / 1000000).toFixed(1)}M</p>
            <p className="text-sm text-gray-600">Annual Revenue</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-800">{reportData.growthRate}%</p>
            <p className="text-sm text-gray-600">Growth Rate</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-800">{reportData.confidence}%</p>
            <p className="text-sm text-gray-600">Confidence Score</p>
          </div>
        </div>
      </div>

      <h4 className="text-lg font-semibold text-gray-800 mb-3">📥 Download Reports</h4>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {['pdf', 'docx', 'png', 'txt', 'all'].map((format) => (
          <button
            key={format}
            onClick={() => generateReport(format)}
            disabled={generating}
            className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 transition-all text-sm"
          >
            {format === 'all' ? '📦 All' : `📄 ${format.toUpperCase()}`}
          </button>
        ))}
      </div>
      
      {generating && (
        <div className="mt-4 p-3 bg-blue-100 border border-blue-300 text-blue-700 rounded-lg text-sm">
          <div className="flex items-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
            Generating your valuation report...
          </div>
        </div>
      )}
    </div>
  );
};

// Working Dashboard component
const Dashboard = () => {
  const { user, logout, login, isLoading } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');

  const handleAuthSuccess = (authData: any) => {
    console.log('=== AUTH SUCCESS HANDLER ===');
    console.log('Auth success data received:', authData);
    
    if (authData.token && authData.user) {
      console.log('Calling login function...');
      login(authData.user, authData.token);
    } else {
      console.error('Missing token or user data:', authData);
    }
  };

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <AuthForm onAuthSuccess={handleAuthSuccess} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Navigation Header */}
      <div className="bg-white/70 backdrop-blur-xl border-b border-white/20 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                ValuAI
              </h1>
              <div className="ml-10 flex space-x-8">
                <button
                  onClick={() => setActiveTab('dashboard')}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'dashboard' 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Dashboard
                </button>
                <button
                  onClick={() => setActiveTab('realtime')}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'realtime' 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Real-Time
                </button>
                <button
                  onClick={() => setActiveTab('upload')}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'upload' 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Data Input
                </button>
                <button
                  onClick={() => setActiveTab('reports')}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'reports' 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Reports
                </button>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">Welcome, {user.firstName}!</span>
              <button 
                onClick={logout}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' && (
          <div className="space-y-8">
            {/* Welcome Section */}
            <div className="text-center">
              <h2 className="text-4xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent">
                UCaaS Business Valuation Platform
              </h2>
              <p className="text-gray-600 mt-2 text-lg">AI-powered valuation with comprehensive reporting</p>
            </div>

            {/* Feature Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div 
                onClick={() => setActiveTab('upload')}
                className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6 hover:shadow-2xl transition-all duration-300 cursor-pointer group"
              >
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <span className="text-white text-xl">�</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Data Input</h3>
                <p className="text-gray-600">Upload files or enter data manually for valuation analysis</p>
              </div>
              
              <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6 hover:shadow-2xl transition-all duration-300 cursor-pointer group">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-600 to-blue-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <span className="text-white text-xl">🤖</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">AI Analysis</h3>
                <p className="text-gray-600">Advanced AI algorithms for accurate UCaaS valuations</p>
              </div>
              
              <div 
                onClick={() => setActiveTab('reports')}
                className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6 hover:shadow-2xl transition-all duration-300 cursor-pointer group"
              >
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-600 to-pink-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <span className="text-white text-xl">�</span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Reports</h3>
                <p className="text-gray-600">Download comprehensive reports in multiple formats</p>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Account Overview</h3>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="text-center">
                  <p className="text-2xl font-bold text-blue-600">5</p>
                  <p className="text-sm text-gray-600">Valuations Completed</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-green-600">12</p>
                  <p className="text-sm text-gray-600">Files Uploaded</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-purple-600">8</p>
                  <p className="text-sm text-gray-600">Reports Generated</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-orange-600">98%</p>
                  <p className="text-sm text-gray-600">Accuracy Rate</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'upload' && <FileUploadSection />}
        {activeTab === 'realtime' && <RealTimeDashboard />}
        {activeTab === 'reports' && <ReportGeneration />}
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Dashboard />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
