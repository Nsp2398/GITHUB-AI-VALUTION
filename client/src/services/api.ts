import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export interface CompanyData {
  name: string;
  industry: string;
  description?: string;
  revenue: number;
  ebitda: number;
  growth_rate: number;
  profit_margin: number;
  mrr: number;
  arpu: number;
  churn_rate: number;
  cac: number;
  ltv: number;
}

export interface ValuationData {
  revenue: number;
  growth_rate: number;
  ebitda_margin: number;
  discount_rate: number;
  terminal_growth_rate: number;
  projection_years?: number;
  mrr?: number;
  arpu?: number;
  churn_rate?: number;
  cac?: number;
  ltv?: number;
}

export interface UCaaSMetricsData {
  arpu: number;
  gross_margin: number;
  churn_rate: number;
  cac: number;
}

const api = {
  // Company endpoints
  createCompany: async (data: CompanyData) => {
    const response = await axios.post(`${API_BASE_URL}/companies`, data);
    return response.data;
  },

  getCompany: async (id: number) => {
    const response = await axios.get(`${API_BASE_URL}/companies/${id}`);
    return response.data;
  },

  // Valuation endpoints
  calculateDCF: async (data: ValuationData) => {
    const response = await axios.post(`${API_BASE_URL}/valuations/dcf`, data);
    return response.data;
  },

  calculateUCaaSMetrics: async (data: UCaaSMetricsData) => {
    const response = await axios.post(`${API_BASE_URL}/metrics/ucaas`, data);
    return response.data;
  },

  createValuation: async (companyId: number, data: any) => {
    const response = await axios.post(`${API_BASE_URL}/valuations/${companyId}`, data);
    return response.data;
  }
};

export default api;
