import React, { useState, useEffect } from 'react';

interface AnalyticsSummary {
  company_id: number;
  company_name: string;
  valuation_date: string;
  final_valuation: number;
  confidence_score: number;
  overall_score: number;
  metrics: {
    [key: string]: {
      value: number;
      benchmark: number;
      percentile: number;
      performance_rating: string;
    };
  };
  strengths: Array<{
    metric: string;
    percentile: number;
    note: string;
  }>;
  improvement_areas: Array<{
    metric: string;
    percentile: number;
    recommendation: string;
  }>;
}

interface CompanyAnalyticsProps {
  companyId: number;
}

export const CompanyAnalytics: React.FC<CompanyAnalyticsProps> = ({ companyId }) => {
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    fetchAnalytics();
  }, [companyId]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('authToken');
      
      const response = await fetch(`http://localhost:5000/api/analytics/company/${companyId}/performance`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setAnalytics(data);
      } else {
        throw new Error('Failed to fetch analytics');
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 75) return 'text-green-600';
    if (score >= 50) return 'text-blue-600';
    if (score >= 25) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getPerformanceIcon = (rating: string) => {
    switch (rating) {
      case 'Excellent': return '🌟';
      case 'Good': return '👍';
      case 'Average': return '⚡';
      case 'Below Average': return '⚠️';
      default: return '📊';
    }
  };

  if (loading) {
    return (
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-8">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white/70 backdrop-blur-xl border border-red-200 rounded-2xl shadow-xl p-8">
        <div className="text-center">
          <div className="text-red-500 text-4xl mb-4">⚠️</div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">Analytics Unavailable</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={fetchAnalytics}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!analytics) {
    return (
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-8">
        <div className="text-center">
          <div className="text-gray-400 text-4xl mb-4">📊</div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">No Analytics Available</h3>
          <p className="text-gray-600">Complete a valuation to see performance analytics.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Overall Performance Score */}
      <div className="bg-gradient-to-r from-blue-100 via-purple-100 to-pink-100 rounded-2xl p-6 shadow-xl">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Performance Analytics</h2>
          <div className="flex items-center justify-center space-x-4">
            <div className="text-center">
              <div className={`text-4xl font-bold ${getScoreColor(analytics.overall_score)}`}>
                {analytics.overall_score}
              </div>
              <div className="text-sm text-gray-600">Overall Score</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600">
                {analytics.confidence_score}%
              </div>
              <div className="text-sm text-gray-600">Confidence</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600">
                ${(analytics.final_valuation / 1000000).toFixed(1)}M
              </div>
              <div className="text-sm text-gray-600">Valuation</div>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics Performance */}
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">📈 Key Metrics vs Industry</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Object.entries(analytics.metrics).map(([metricName, metric]) => (
            <div key={metricName} className="bg-gray-50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-gray-800 capitalize">
                  {getPerformanceIcon(metric.performance_rating)} {metricName.replace('_', ' ')}
                </h4>
                <span className={`px-2 py-1 rounded text-xs font-medium ${getScoreColor(metric.percentile)} bg-gray-100`}>
                  {metric.percentile}th percentile
                </span>
              </div>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span>Your Value:</span>
                  <span className="font-medium">{metric.value.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Industry Avg:</span>
                  <span className="text-gray-600">{metric.benchmark.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Rating:</span>
                  <span className={`font-medium ${getScoreColor(metric.percentile)}`}>
                    {metric.performance_rating}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Strengths */}
      {analytics.strengths.length > 0 && (
        <div className="bg-white/70 backdrop-blur-xl border border-green-200 rounded-2xl shadow-xl p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">🌟 Key Strengths</h3>
          <div className="space-y-3">
            {analytics.strengths.map((strength, index) => (
              <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-green-800 capitalize">
                    {strength.metric.replace('_', ' ')}
                  </h4>
                  <span className="px-2 py-1 bg-green-200 text-green-800 rounded text-xs font-medium">
                    {strength.percentile}th percentile
                  </span>
                </div>
                <p className="text-green-700 text-sm">{strength.note}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Improvement Areas */}
      {analytics.improvement_areas.length > 0 && (
        <div className="bg-white/70 backdrop-blur-xl border border-orange-200 rounded-2xl shadow-xl p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-4">🎯 Areas for Improvement</h3>
          <div className="space-y-3">
            {analytics.improvement_areas.map((area, index) => (
              <div key={index} className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-orange-800 capitalize">
                    {area.metric.replace('_', ' ')}
                  </h4>
                  <span className="px-2 py-1 bg-orange-200 text-orange-800 rounded text-xs font-medium">
                    {area.percentile}th percentile
                  </span>
                </div>
                <p className="text-orange-700 text-sm">{area.recommendation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Market Insights */}
      <div className="bg-white/70 backdrop-blur-xl border border-white/20 rounded-2xl shadow-xl p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">💡 Market Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-blue-50 rounded-lg p-4">
            <div className="text-2xl mb-2">📈</div>
            <h4 className="font-semibold text-blue-800">Growth Trends</h4>
            <p className="text-blue-700 text-sm">UCaaS market growing at 12% annually with increasing demand for remote solutions.</p>
          </div>
          <div className="bg-purple-50 rounded-lg p-4">
            <div className="text-2xl mb-2">🤖</div>
            <h4 className="font-semibold text-purple-800">AI Integration</h4>
            <p className="text-purple-700 text-sm">Companies with AI features see 15-25% valuation premiums.</p>
          </div>
          <div className="bg-green-50 rounded-lg p-4">
            <div className="text-2xl mb-2">🔒</div>
            <h4 className="font-semibold text-green-800">Security Focus</h4>
            <p className="text-green-700 text-sm">Security-first platforms command premium valuations in current market.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompanyAnalytics;
