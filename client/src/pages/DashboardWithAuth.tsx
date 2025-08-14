import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { AuthWrapper } from '../components/auth/AuthWrapper';
import { FileUpload } from '../components/ui/FileUpload';
import { useAuth } from '../contexts/AuthContext';
import { 
  CalculatorIcon, 
  ChartBarIcon, 
  CpuChipIcon, 
  RocketLaunchIcon,
  SparklesIcon,
  UserCircleIcon,
  ArrowTopRightOnSquareIcon
} from '@heroicons/react/24/outline';

export const Dashboard: React.FC = () => {
  const { user, logout, login, isLoading } = useAuth();
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);

  const handleFileSelect = (files: File[]) => {
    setUploadedFiles(files);
  };

  const handleFileUpload = async () => {
    if (uploadedFiles.length === 0) {
      alert('Please select files to upload');
      return;
    }

    const formData = new FormData();
    uploadedFiles.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('/api/files/upload-batch', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Successfully uploaded ${result.successful} files`);
        setUploadedFiles([]);
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to upload files');
    }
  };

  const handleGenerateReport = async (format: string = 'all') => {
    setIsGeneratingReport(true);
    
    try {
      // Sample data for demonstration - in real app this would come from valuation analysis
      const sampleData = {
        company_info: {
          name: "Sample UCaaS Company",
          arr: 5000000,
          industry: "UCaaS"
        },
        valuation_data: {
          growth_rate: 0.35,
          gross_margin: 0.78,
          net_revenue_retention: 1.15,
          rule_of_40: 42.5,
          ltv_cac_ratio: 4.2,
          valuation: 75000000,
          revenue_multiple: 15.0,
          ebitda_multiple: 45.0
        },
        market_data: {
          market_size: 50000000000,
          market_growth: 0.25,
          competitive_position: "Strong"
        },
        peer_comparison: [],
        format: format
      };

      const response = await fetch('http://localhost:5000/api/generate-comprehensive-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
          companyName: sampleData.company_info?.name || 'Sample Company',
          industry: sampleData.company_info?.industry || 'Technology',
          revenue: sampleData.company_info?.arr || 5000000,
          growthRate: sampleData.valuation_data?.growth_rate || 0.35,
          ebitdaMargin: sampleData.valuation_data?.gross_margin || 0.25
        })
      });

      if (response.ok) {
        const data = await response.json();
        // Our backend returns { filename, report_url, message }
        // Download the generated report
        const downloadResponse = await fetch(data.report_url, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
        });
        if (downloadResponse.ok) {
          const blob = await downloadResponse.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = data.filename;
          a.click();
          window.URL.revokeObjectURL(url);
          alert('Report generated and downloaded successfully!');
        } else {
          throw new Error('Download failed');
        }
      } else {
        throw new Error('Report generation failed');
      }
    } catch (error) {
      console.error('Report generation error:', error);
      alert('Failed to generate report');
    } finally {
      setIsGeneratingReport(false);
    }
  };

  const handleAuthSuccess = (authData: any) => {
    console.log('=== AUTH SUCCESS HANDLER ===');
    console.log('Auth success data received:', authData);
    console.log('Has token?', !!authData.token);
    console.log('Has user?', !!authData.user);
    console.log('Token value:', authData.token);
    console.log('User value:', authData.user);
    
    if (authData.token && authData.user) {
      console.log('Calling login function with user and token...');
      login(authData.user, authData.token);
      console.log('Login function called successfully');
    } else {
      console.error('Missing token or user data in auth response:', authData);
      console.error('authData keys:', Object.keys(authData));
    }
    console.log('=== END AUTH SUCCESS HANDLER ===');
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
    return <AuthWrapper onAuthSuccess={handleAuthSuccess} />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-xl border-b border-white/20 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="h-10 w-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                  <SparklesIcon className="h-6 w-6 text-white" />
                </div>
                <span className="ml-3 text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  ValuAI
                </span>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <UserCircleIcon className="h-8 w-8 text-gray-400" />
                <div className="hidden md:block">
                  <p className="text-sm font-medium text-gray-900">
                    {user.firstName} {user.lastName}
                  </p>
                  <p className="text-xs text-gray-500">{user.email}</p>
                </div>
              </div>
              <button
                onClick={logout}
                className="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-lg text-gray-700 bg-white/50 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
              >
                <ArrowTopRightOnSquareIcon className="h-4 w-4 mr-2" />
                Sign out
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Comprehensive Valuation Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <h2 className="text-4xl font-bold mb-4">
              🏆 Comprehensive UCaaS Valuation
            </h2>
            <p className="text-xl mb-8 max-w-3xl mx-auto">
              Get your business valued using three industry-standard methods with AI-powered recommendations. 
              Upload financial data or enter manually for instant, professional valuation reports.
            </p>
            
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="text-center">
                <CalculatorIcon className="h-12 w-12 mx-auto mb-3 text-blue-200" />
                <h3 className="font-semibold text-lg mb-2">💼 DCF Analysis</h3>
                <p className="text-blue-100 text-sm">5-year cash flow projections with terminal value</p>
              </div>
              <div className="text-center">
                <ChartBarIcon className="h-12 w-12 mx-auto mb-3 text-green-200" />
                <h3 className="font-semibold text-lg mb-2">📊 UCaaS Metrics</h3>
                <p className="text-blue-100 text-sm">MRR, CAC, LTV, and industry benchmarks</p>
              </div>
              <div className="text-center">
                <CpuChipIcon className="h-12 w-12 mx-auto mb-3 text-purple-200" />
                <h3 className="font-semibold text-lg mb-2">🤖 AI-Powered</h3>
                <p className="text-blue-100 text-sm">Machine learning with qualitative factors</p>
              </div>
            </div>
            
            <Link
              to="/comprehensive-valuation"
              className="inline-flex items-center bg-white text-blue-600 font-semibold py-3 px-8 rounded-lg hover:bg-blue-50 transition-colors text-lg"
            >
              <RocketLaunchIcon className="h-6 w-6 mr-2" />
              Start Comprehensive Valuation
            </Link>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            {/* File Upload Section */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                  Upload Documents
                </h3>
                <p className="text-sm text-gray-600 mb-6">
                  Upload your business documents for valuation analysis. Supported formats include 
                  PDF, Word documents, Excel files, text files, and images.
                </p>
                
                <FileUpload
                  onFileSelect={handleFileSelect}
                  maxFiles={10}
                  className="mb-6"
                />
                
                {uploadedFiles.length > 0 && (
                  <div className="flex justify-end">
                    <button
                      onClick={handleFileUpload}
                      className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md"
                    >
                      Upload Files ({uploadedFiles.length})
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:p-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                  Quick Actions
                </h3>
                
                <div className="space-y-4">
                  <button className="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-8 w-8 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 font-semibold">$</span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <h4 className="text-sm font-medium text-gray-900">DCF Valuation</h4>
                        <p className="text-sm text-gray-600">Calculate discounted cash flow valuation</p>
                      </div>
                    </div>
                  </button>
                  
                  <button className="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-8 w-8 bg-green-100 rounded-full flex items-center justify-center">
                          <span className="text-green-600 font-semibold">📊</span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <h4 className="text-sm font-medium text-gray-900">UCaaS Metrics</h4>
                        <p className="text-sm text-gray-600">Analyze UCaaS-specific KPIs</p>
                      </div>
                    </div>
                  </button>
                  
                  <button className="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-8 w-8 bg-purple-100 rounded-full flex items-center justify-center">
                          <span className="text-purple-600 font-semibold">🤖</span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <h4 className="text-sm font-medium text-gray-900">AI Analysis</h4>
                        <p className="text-sm text-gray-600">Get AI-powered insights</p>
                      </div>
                    </div>
                  </button>
                  
                  <button 
                    onClick={() => handleGenerateReport('all')}
                    disabled={isGeneratingReport}
                    className="w-full text-left p-4 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                  >
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className="h-8 w-8 bg-orange-100 rounded-full flex items-center justify-center">
                          <span className="text-orange-600 font-semibold">📄</span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <h4 className="text-sm font-medium text-gray-900">
                          {isGeneratingReport ? 'Generating...' : 'Generate Report'}
                        </h4>
                        <p className="text-sm text-gray-600">Create valuation report in multiple formats</p>
                      </div>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          {/* Report Generation Section */}
          <div className="mt-8 bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                Download Valuation Reports
              </h3>
              <p className="text-sm text-gray-600 mb-6">
                Generate and download comprehensive valuation reports in your preferred format.
              </p>
              
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <button
                  onClick={() => handleGenerateReport('pdf')}
                  disabled={isGeneratingReport}
                  className="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  <div className="h-12 w-12 bg-red-100 rounded-full flex items-center justify-center mb-2">
                    <span className="text-red-600 font-semibold text-lg">📄</span>
                  </div>
                  <span className="text-sm font-medium text-gray-900">PDF</span>
                  <span className="text-xs text-gray-500">Professional report</span>
                </button>
                
                <button
                  onClick={() => handleGenerateReport('docx')}
                  disabled={isGeneratingReport}
                  className="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  <div className="h-12 w-12 bg-blue-100 rounded-full flex items-center justify-center mb-2">
                    <span className="text-blue-600 font-semibold text-lg">📝</span>
                  </div>
                  <span className="text-sm font-medium text-gray-900">Word</span>
                  <span className="text-xs text-gray-500">Editable document</span>
                </button>
                
                <button
                  onClick={() => handleGenerateReport('txt')}
                  disabled={isGeneratingReport}
                  className="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  <div className="h-12 w-12 bg-gray-100 rounded-full flex items-center justify-center mb-2">
                    <span className="text-gray-600 font-semibold text-lg">📋</span>
                  </div>
                  <span className="text-sm font-medium text-gray-900">Text</span>
                  <span className="text-xs text-gray-500">Plain text</span>
                </button>
                
                <button
                  onClick={() => handleGenerateReport('png')}
                  disabled={isGeneratingReport}
                  className="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  <div className="h-12 w-12 bg-green-100 rounded-full flex items-center justify-center mb-2">
                    <span className="text-green-600 font-semibold text-lg">🖼️</span>
                  </div>
                  <span className="text-sm font-medium text-gray-900">Image</span>
                  <span className="text-xs text-gray-500">Visual charts</span>
                </button>
                
                <button
                  onClick={() => handleGenerateReport('all')}
                  disabled={isGeneratingReport}
                  className="flex flex-col items-center p-4 border-2 border-blue-300 bg-blue-50 rounded-lg hover:bg-blue-100 disabled:opacity-50"
                >
                  <div className="h-12 w-12 bg-blue-100 rounded-full flex items-center justify-center mb-2">
                    <span className="text-blue-600 font-semibold text-lg">📦</span>
                  </div>
                  <span className="text-sm font-medium text-gray-900">All Formats</span>
                  <span className="text-xs text-gray-500">ZIP download</span>
                </button>
              </div>
              
              {isGeneratingReport && (
                <div className="mt-4 flex items-center justify-center">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
                  <span className="ml-2 text-sm text-gray-600">Generating your report...</span>
                </div>
              )}
            </div>
          </div>
          
          {/* Recent Activity */}
          <div className="mt-8 bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                Recent Activity
              </h3>
              <div className="text-sm text-gray-600">
                No recent activity. Start by uploading documents or creating a new valuation.
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
