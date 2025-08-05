import React from 'react';
import { InputField } from '../ui/InputField';

interface UCaaSMetricsFormProps {
  metrics: {
    mrr: number;
    arpu: number;
    customers: number;
    churn_rate: number;
    cac: number;
    gross_margin: number;
    growth_rate: number;
    expansion_revenue: number;
    support_costs: number;
  };
  onChange: (name: string, value: number) => void;
}

export const UCaaSMetricsForm: React.FC<UCaaSMetricsFormProps> = ({
  metrics,
  onChange
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    const numValue = parseFloat(value);
    
    // Convert percentage inputs to decimals
    const isPercentage = name === 'churn_rate' || 
                        name === 'gross_margin' || 
                        name === 'growth_rate';
    
    onChange(name, isPercentage ? numValue / 100 : numValue);
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-medium">UCaaS Metrics</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <InputField
          label="Monthly Recurring Revenue ($)"
          name="mrr"
          type="number"
          value={metrics.mrr}
          onChange={handleChange}
          required
        />
        
        <InputField
          label="Average Revenue Per User ($)"
          name="arpu"
          type="number"
          value={metrics.arpu}
          onChange={handleChange}
          required
        />
        
        <InputField
          label="Number of Customers"
          name="customers"
          type="number"
          value={metrics.customers}
          onChange={handleChange}
          required
        />
        
        <InputField
          label="Monthly Churn Rate (%)"
          name="churn_rate"
          type="number"
          value={metrics.churn_rate * 100}
          onChange={handleChange}
          required
        />
        
        <InputField
          label="Customer Acquisition Cost ($)"
          name="cac"
          type="number"
          value={metrics.cac}
          onChange={handleChange}
          required
        />
        
        <InputField
          label="Gross Margin (%)"
          name="gross_margin"
          type="number"
          value={metrics.gross_margin * 100}
          onChange={handleChange}
          required
        />
        
        <InputField
          label="Monthly Growth Rate (%)"
          name="growth_rate"
          type="number"
          value={metrics.growth_rate * 100}
          onChange={handleChange}
          required
        />
        
        <InputField
          label="Monthly Expansion Revenue ($)"
          name="expansion_revenue"
          type="number"
          value={metrics.expansion_revenue}
          onChange={handleChange}
        />
        
        <InputField
          label="Monthly Support Costs per Customer ($)"
          name="support_costs"
          type="number"
          value={metrics.support_costs}
          onChange={handleChange}
        />
      </div>
      
      <div className="bg-blue-50 p-4 rounded-lg">
        <h4 className="text-sm font-medium text-blue-900 mb-2">Key Metrics Info</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• MRR (Monthly Recurring Revenue): Regular monthly revenue from subscriptions</li>
          <li>• ARPU (Average Revenue Per User): Average monthly revenue per customer</li>
          <li>• Churn Rate: Monthly rate at which customers cancel</li>
          <li>• CAC (Customer Acquisition Cost): Cost to acquire one new customer</li>
          <li>• Gross Margin: Revenue minus direct costs, as a percentage</li>
          <li>• Expansion Revenue: Additional revenue from existing customers</li>
        </ul>
      </div>
    </div>
  );
};
