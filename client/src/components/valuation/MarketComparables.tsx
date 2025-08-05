import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface MarketComparablesProps {
  peerData: {
    company: string;
    metrics: {
      mrr_multiple: number;
      growth_rate: number;
      gross_margin: number;
      net_revenue_retention: number;
    };
  }[];
  companyMetrics: {
    growth_rate: number;
    gross_margin: number;
    net_revenue_retention: number;
  };
  isLoading?: boolean;
}

export const MarketComparables: React.FC<MarketComparablesProps> = ({
  peerData,
  companyMetrics,
  isLoading = false,
}) => {
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Market Comparables Analysis',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function (tickValue: string | number) {
            if (typeof tickValue === 'number') {
              return tickValue.toFixed(2);
            }
            return tickValue;
          },
        },
      },
    },
  };

  const metrics = ['Growth Rate', 'Gross Margin', 'Net Revenue Retention'];
  
  const data = {
    labels: peerData.map((peer) => peer.company),
    datasets: [
      {
        label: 'Your Company',
        data: peerData.map(() => companyMetrics.growth_rate),
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Peer Companies',
        data: peerData.map((peer) => peer.metrics.growth_rate),
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
        borderColor: 'rgba(53, 162, 235, 1)',
        borderWidth: 1,
      },
    ],
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6">Market Comparables Analysis</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {metrics.map((metric) => (
          <div key={metric} className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold text-lg mb-2">{metric}</h3>
            <Bar options={options} data={data} height={300} />
          </div>
        ))}
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full table-auto">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2">Company</th>
              <th className="px-4 py-2">Growth Rate</th>
              <th className="px-4 py-2">Gross Margin</th>
              <th className="px-4 py-2">Net Revenue Retention</th>
              <th className="px-4 py-2">MRR Multiple</th>
            </tr>
          </thead>
          <tbody>
            {peerData.map((peer) => (
              <tr key={peer.company} className="border-b">
                <td className="px-4 py-2">{peer.company}</td>
                <td className="px-4 py-2">{(peer.metrics.growth_rate * 100).toFixed(1)}%</td>
                <td className="px-4 py-2">{(peer.metrics.gross_margin * 100).toFixed(1)}%</td>
                <td className="px-4 py-2">
                  {(peer.metrics.net_revenue_retention * 100).toFixed(1)}%
                </td>
                <td className="px-4 py-2">{peer.metrics.mrr_multiple.toFixed(1)}x</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
