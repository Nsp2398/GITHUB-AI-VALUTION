import React, { useState } from 'react';
import { AuthWrapper } from '../components/auth/AuthWrapper';
import { FileUpload } from '../components/ui/FileUpload';
import { useAuth } from '../contexts/AuthContext';

export const Dashboard: React.FC = () => {
  const { user, logout, login } = useAuth();
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [reportData, setReportData] = useState<any>(null);
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
      const response = await fetch('http://localhost:5000/api/files/upload-batch', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
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

      const response = await fetch('http://localhost:5000/api/reports/generate-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify(sampleData)
      });

      if (response.ok) {
        // Get filename from response headers or create one
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'valuation_report';
        if (contentDisposition) {
          const match = contentDisposition.match(/filename="(.+)"/);
          if (match) filename = match[1];
        }
        
        // Download the file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        window.URL.revokeObjectURL(url);
        
        alert('Report generated and downloaded successfully!');
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
    console.log('Auth success data:', authData);
    if (authData.token && authData.user) {
      login(authData.user, authData.token);
    } else {
      console.error('Missing token or user data in auth response:', authData);
    }
  };

  if (!user) {
    return <AuthWrapper onAuthSuccess={handleAuthSuccess} />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">ValuAI Dashboard</h1>
              <p className="text-gray-600">Welcome, {user.firstName} {user.lastName}</p>
            </div>
            <button
              onClick={logout}
              className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-md"
            >
              Sign Out
            </button>
          </div>
        </div>
      </header>

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
