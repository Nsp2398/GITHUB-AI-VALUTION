import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardContent } from './ui/Card';

// Simple icon components as alternatives to lucide-react
const AlertTriangle = () => <span className="text-xl">⚠️</span>;
const TrendingUp = () => <span className="text-xl">📈</span>;
const Activity = () => <span className="text-xl">⚡</span>;
const Bell = () => <span className="text-xl">🔔</span>;
const RefreshCw = () => <span className="text-xl">🔄</span>;

interface DashboardData {
  timestamp: string;
  user_id: number;
  summary: {
    total_companies: number;
    total_valuations: number;
    avg_confidence: number;
    portfolio_value: number;
  };
  companies: Array<{
    company_id: number;
    company_name: string;
    latest_valuation: number;
    confidence: number;
    last_updated: string;
  }>;
  recent_activity: Array<{
    id: number;
    company_name: string;
    valuation: number;
    confidence: number;
    date: string;
    method: string;
  }>;
  alerts: Array<{
    type: string;
    title: string;
    message: string;
    action?: string;
    company_id?: number;
  }>;
  recommendations: Array<{
    type: string;
    title: string;
    message: string;
    action: string;
  }>;
}

interface LiveMetrics {
  timestamp: string;
  system_status: string;
  api_calls_per_minute: number;
  active_users: number;
  database_connections: number;
  cache_hit_rate: number;
  average_response_time: number;
  error_rate: number;
}

const RealTimeDashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [liveMetrics, setLiveMetrics] = useState<LiveMetrics | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [lastUpdate, setLastUpdate] = useState<string>('');
  const [notifications, setNotifications] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    // Simulate data fetching
    fetchDashboardData();
    fetchLiveMetrics();
    fetchNotifications();
    setIsConnected(true);

    // Set up periodic updates
    const interval = setInterval(() => {
      fetchLiveMetrics();
      setLastUpdate(new Date().toLocaleTimeString());
    }, 30000); // Every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    // Mock data for demonstration
    const mockData: DashboardData = {
      timestamp: new Date().toISOString(),
      user_id: 1,
      summary: {
        total_companies: 5,
        total_valuations: 12,
        avg_confidence: 85,
        portfolio_value: 45000000
      },
      companies: [
        {
          company_id: 1,
          company_name: "TechCorp Solutions",
          latest_valuation: 15000000,
          confidence: 88,
          last_updated: new Date().toISOString()
        },
        {
          company_id: 2,
          company_name: "CloudComm Inc",
          latest_valuation: 22000000,
          confidence: 92,
          last_updated: new Date().toISOString()
        }
      ],
      recent_activity: [
        {
          id: 1,
          company_name: "TechCorp Solutions",
          valuation: 15000000,
          confidence: 88,
          date: new Date().toISOString(),
          method: "DCF Analysis"
        }
      ],
      alerts: [
        {
          type: "success",
          title: "Market Opportunity",
          message: "UCaaS market showing strong growth trends (+12.3% this quarter)",
          action: "Review market positioning"
        }
      ],
      recommendations: [
        {
          type: "feature",
          title: "Try Analytics Dashboard",
          message: "Get deeper insights with performance analytics and benchmarking",
          action: "View Analytics"
        }
      ]
    };
    
    setDashboardData(mockData);
  };

  const fetchLiveMetrics = async () => {
    // Mock metrics for demonstration
    const mockMetrics: LiveMetrics = {
      timestamp: new Date().toISOString(),
      system_status: "operational",
      api_calls_per_minute: Math.floor(Math.random() * 100) + 50,
      active_users: Math.floor(Math.random() * 30) + 15,
      database_connections: Math.floor(Math.random() * 20) + 10,
      cache_hit_rate: Math.random() * 15 + 85,
      average_response_time: Math.random() * 150 + 150,
      error_rate: Math.random() * 2.5 + 0.1
    };
    
    setLiveMetrics(mockMetrics);
  };

  const fetchNotifications = async () => {
    const mockNotifications = [
      {
        id: 1,
        type: "valuation_complete",
        title: "Valuation Complete",
        message: "Your valuation for TechCorp has been completed",
        timestamp: new Date().toISOString(),
        read: false
      }
    ];
    
    setNotifications(mockNotifications);
  };

  const handleRefresh = () => {
    fetchDashboardData();
    fetchLiveMetrics();
    setLastUpdate(new Date().toLocaleTimeString());
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const getAlertColor = (type: string) => {
    switch (type) {
      case 'warning': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'success': return 'text-green-600 bg-green-50 border-green-200';
      case 'info': return 'text-blue-600 bg-blue-50 border-blue-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Real-Time Dashboard</h1>
            <p className="text-gray-600 mt-1">
              Live insights and analytics for your portfolio
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
              <span className="text-sm text-gray-600">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
            <button
              onClick={handleRefresh}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <RefreshCw />
              <span>Refresh</span>
            </button>
          </div>
        </div>
        {lastUpdate && (
          <p className="text-sm text-gray-500 mt-2">
            Last updated: {lastUpdate}
          </p>
        )}
      </div>

      {/* Navigation Tabs */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'metrics', label: 'System Metrics' },
              { id: 'notifications', label: 'Notifications' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && dashboardData && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Summary Cards */}
          <div className="lg:col-span-2 grid grid-cols-2 gap-4">
            <Card>
              <CardHeader>
                <h3 className="text-lg font-semibold">Portfolio Value</h3>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-blue-600">
                  {formatCurrency(dashboardData.summary.portfolio_value)}
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  Across {dashboardData.summary.total_companies} companies
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <h3 className="text-lg font-semibold">Avg Confidence</h3>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-green-600">
                  {dashboardData.summary.avg_confidence}%
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  From {dashboardData.summary.total_valuations} valuations
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Alerts */}
          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold flex items-center">
                <AlertTriangle />
                <span className="ml-2">Alerts</span>
              </h3>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {dashboardData.alerts.slice(0, 3).map((alert, index) => (
                  <div
                    key={index}
                    className={`p-3 rounded-lg border ${getAlertColor(alert.type)}`}
                  >
                    <h4 className="font-medium text-sm">{alert.title}</h4>
                    <p className="text-xs mt-1">{alert.message}</p>
                    {alert.action && (
                      <button className="text-xs underline mt-1 hover:no-underline">
                        {alert.action}
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <h3 className="text-lg font-semibold flex items-center">
                <Activity />
                <span className="ml-2">Recent Activity</span>
              </h3>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {dashboardData.recent_activity.slice(0, 5).map((activity) => (
                  <div key={activity.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium">{activity.company_name}</h4>
                      <p className="text-sm text-gray-600">
                        {activity.method} • {new Date(activity.date).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="text-right">
                      <div className="font-bold">{formatCurrency(activity.valuation)}</div>
                      <div className="text-sm text-gray-600">{activity.confidence}% confidence</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Recommendations */}
          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold flex items-center">
                <TrendingUp />
                <span className="ml-2">Recommendations</span>
              </h3>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {dashboardData.recommendations.map((rec, index) => (
                  <div key={index} className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <h4 className="font-medium text-sm text-blue-800">{rec.title}</h4>
                    <p className="text-xs text-blue-700 mt-1">{rec.message}</p>
                    <button className="text-xs text-blue-600 underline mt-1 hover:no-underline">
                      {rec.action}
                    </button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* System Metrics Tab */}
      {activeTab === 'metrics' && liveMetrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {liveMetrics.active_users}
                </div>
                <p className="text-sm text-gray-600">Active Users</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {liveMetrics.api_calls_per_minute}
                </div>
                <p className="text-sm text-gray-600">API Calls/Min</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {liveMetrics.cache_hit_rate.toFixed(1)}%
                </div>
                <p className="text-sm text-gray-600">Cache Hit Rate</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {liveMetrics.average_response_time.toFixed(0)}ms
                </div>
                <p className="text-sm text-gray-600">Avg Response</p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Notifications Tab */}
      {activeTab === 'notifications' && (
        <div className="max-w-2xl">
          <Card>
            <CardHeader>
              <h3 className="text-lg font-semibold flex items-center">
                <Bell />
                <span className="ml-2">Notifications</span>
              </h3>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {notifications.map((notification) => (
                  <div
                    key={notification.id}
                    className={`p-4 rounded-lg border ${
                      notification.read ? 'bg-gray-50' : 'bg-blue-50 border-blue-200'
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-medium">{notification.title}</h4>
                        <p className="text-sm text-gray-600 mt-1">{notification.message}</p>
                        <p className="text-xs text-gray-500 mt-2">
                          {new Date(notification.timestamp).toLocaleString()}
                        </p>
                      </div>
                      {!notification.read && (
                        <div className="w-3 h-3 bg-blue-600 rounded-full"></div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default RealTimeDashboard;
