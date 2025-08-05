import pandas as pd
from typing import Dict, List, Any

class UCaaSMarketData:
    # UCaaS Industry Benchmarks 2025
    INDUSTRY_BENCHMARKS = {
        "public_companies": {
            "RingCentral": {
                "mrr_multiple": 15.2,
                "arr_multiple": 12.8,
                "growth_rate": 0.32,
                "gross_margin": 0.82,
                "net_revenue_retention": 1.15,
                "rule_of_40": 45.2
            },
            "Vonage": {
                "mrr_multiple": 12.5,
                "arr_multiple": 10.2,
                "growth_rate": 0.25,
                "gross_margin": 0.78,
                "net_revenue_retention": 1.12,
                "rule_of_40": 38.5
            },
            "8x8": {
                "mrr_multiple": 11.8,
                "arr_multiple": 9.5,
                "growth_rate": 0.22,
                "gross_margin": 0.75,
                "net_revenue_retention": 1.08,
                "rule_of_40": 35.2
            },
            "Five9": {
                "mrr_multiple": 14.5,
                "arr_multiple": 11.8,
                "growth_rate": 0.28,
                "gross_margin": 0.80,
                "net_revenue_retention": 1.13,
                "rule_of_40": 42.8
            }
        },
        "industry_averages": {
            "revenue_ranges": {
                "<$10M": {
                    "mrr_multiple_range": [8, 12],
                    "growth_rate_range": [0.3, 0.5],
                    "gross_margin_range": [0.65, 0.75],
                    "net_revenue_retention_range": [1.05, 1.15]
                },
                "$10M-$50M": {
                    "mrr_multiple_range": [10, 14],
                    "growth_rate_range": [0.25, 0.4],
                    "gross_margin_range": [0.7, 0.8],
                    "net_revenue_retention_range": [1.08, 1.18]
                },
                "$50M+": {
                    "mrr_multiple_range": [12, 16],
                    "growth_rate_range": [0.2, 0.35],
                    "gross_margin_range": [0.75, 0.85],
                    "net_revenue_retention_range": [1.1, 1.2]
                }
            }
        },
        "metric_benchmarks": {
            "rule_of_40": {
                "excellent": ">45",
                "good": "35-45",
                "average": "25-35",
                "below_average": "<25"
            },
            "ltv_cac_ratio": {
                "excellent": ">4",
                "good": "3-4",
                "average": "2-3",
                "below_average": "<2"
            },
            "cac_payback": {
                "excellent": "<12",
                "good": "12-18",
                "average": "18-24",
                "below_average": ">24"
            },
            "net_revenue_retention": {
                "excellent": ">120%",
                "good": "110-120%",
                "average": "100-110%",
                "below_average": "<100%"
            }
        }
    }

    @staticmethod
    def get_revenue_bracket(arr: float) -> str:
        """Determine the company's revenue bracket based on ARR"""
        if arr < 10_000_000:
            return "<$10M"
        elif arr < 50_000_000:
            return "$10M-$50M"
        else:
            return "$50M+"

    def get_peer_comparison(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Compare company metrics with peers and industry benchmarks"""
        arr = metrics['arr']
        bracket = self.get_revenue_bracket(arr)
        industry_avg = self.INDUSTRY_BENCHMARKS['industry_averages']['revenue_ranges'][bracket]
        
        # Find closest peers based on revenue and growth
        peers_data = self.INDUSTRY_BENCHMARKS['public_companies']
        peer_comparison = []
        
        for peer, peer_data in peers_data.items():
            peer_comparison.append({
                "company": peer,
                "metrics": peer_data,
                "comparison": {
                    "growth_rate_diff": metrics['growth_rate'] - peer_data['growth_rate'],
                    "gross_margin_diff": metrics['gross_margin'] - peer_data['gross_margin'],
                    "net_revenue_retention_diff": metrics['net_revenue_retention'] - peer_data['net_revenue_retention']
                }
            })

        return {
            "peer_comparison": peer_comparison,
            "industry_benchmarks": industry_avg,
            "market_position": {
                "growth_rate": self._get_metric_position(metrics['growth_rate'], 
                                                       industry_avg['growth_rate_range']),
                "gross_margin": self._get_metric_position(metrics['gross_margin'],
                                                        industry_avg['gross_margin_range']),
                "net_revenue_retention": self._get_metric_position(metrics['net_revenue_retention'],
                                                                 industry_avg['net_revenue_retention_range'])
            }
        }

    def get_metric_rating(self, metric_name: str, value: float) -> str:
        """Get the rating for a specific metric based on benchmarks"""
        benchmarks = self.INDUSTRY_BENCHMARKS['metric_benchmarks'][metric_name]
        
        if metric_name == 'rule_of_40':
            if value > 45:
                return 'excellent'
            elif value > 35:
                return 'good'
            elif value > 25:
                return 'average'
            return 'below_average'
            
        elif metric_name == 'ltv_cac_ratio':
            if value > 4:
                return 'excellent'
            elif value > 3:
                return 'good'
            elif value > 2:
                return 'average'
            return 'below_average'
            
        return 'average'

    @staticmethod
    def _get_metric_position(value: float, range_values: List[float]) -> str:
        """Determine if a metric is below, within, or above the industry range"""
        if value < range_values[0]:
            return "below"
        elif value > range_values[1]:
            return "above"
        return "within"

    def get_valuation_guidance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Provide valuation guidance based on metrics and market conditions"""
        bracket = self.get_revenue_bracket(metrics['arr'])
        industry_avg = self.INDUSTRY_BENCHMARKS['industry_averages']['revenue_ranges'][bracket]
        
        # Calculate base multiple range
        base_multiple_low = industry_avg['mrr_multiple_range'][0]
        base_multiple_high = industry_avg['mrr_multiple_range'][1]
        
        # Adjust multiples based on performance
        adjustments = {
            "growth_premium": self._calculate_growth_premium(metrics['growth_rate'], 
                                                          industry_avg['growth_rate_range']),
            "margin_premium": self._calculate_margin_premium(metrics['gross_margin'],
                                                          industry_avg['gross_margin_range']),
            "retention_premium": self._calculate_retention_premium(metrics['net_revenue_retention'],
                                                                industry_avg['net_revenue_retention_range'])
        }
        
        total_premium = sum(adjustments.values())
        
        return {
            "base_multiple_range": {
                "low": base_multiple_low,
                "high": base_multiple_high
            },
            "adjusted_multiple_range": {
                "low": base_multiple_low * (1 + total_premium),
                "high": base_multiple_high * (1 + total_premium)
            },
            "premium_breakdown": adjustments
        }

    @staticmethod
    def _calculate_growth_premium(growth: float, benchmark_range: List[float]) -> float:
        """Calculate valuation premium/discount based on growth rate"""
        avg_growth = sum(benchmark_range) / 2
        return (growth - avg_growth) * 2  # 2x multiplier for growth differential

    @staticmethod
    def _calculate_margin_premium(margin: float, benchmark_range: List[float]) -> float:
        """Calculate valuation premium/discount based on gross margin"""
        avg_margin = sum(benchmark_range) / 2
        return (margin - avg_margin) * 1.5  # 1.5x multiplier for margin differential

    @staticmethod
    def _calculate_retention_premium(retention: float, benchmark_range: List[float]) -> float:
        """Calculate valuation premium/discount based on net revenue retention"""
        avg_retention = sum(benchmark_range) / 2
        return (retention - avg_retention) * 1.8  # 1.8x multiplier for retention differential
