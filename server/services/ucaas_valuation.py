from typing import Dict, Any
import numpy as np
from dataclasses import dataclass

@dataclass
class UCaaSMetrics:
    mrr: float  # Monthly Recurring Revenue
    arpu: float  # Average Revenue Per User
    customers: int  # Number of customers
    churn_rate: float  # Monthly churn rate
    cac: float  # Customer Acquisition Cost
    gross_margin: float  # Gross margin percentage
    growth_rate: float  # Monthly growth rate
    expansion_revenue: float  # Monthly expansion revenue
    support_costs: float  # Monthly support costs per customer

class UCaaSValuation:
    def __init__(self, metrics: UCaaSMetrics):
        self.metrics = metrics

    def calculate_arr(self) -> float:
        """Calculate Annual Recurring Revenue"""
        return self.metrics.mrr * 12

    def calculate_ltv(self) -> float:
        """
        Calculate Customer Lifetime Value
        LTV = (ARPU * Gross Margin) / Churn Rate
        """
        return (self.metrics.arpu * self.metrics.gross_margin) / self.metrics.churn_rate

    def calculate_payback_period(self) -> float:
        """
        Calculate CAC Payback Period in months
        Payback Period = CAC / (ARPU * Gross Margin)
        """
        return self.metrics.cac / (self.metrics.arpu * self.metrics.gross_margin)

    def calculate_efficiency_metrics(self) -> Dict[str, float]:
        """Calculate key efficiency metrics"""
        ltv = self.calculate_ltv()
        return {
            "ltv_cac_ratio": ltv / self.metrics.cac,
            "cac_payback_months": self.calculate_payback_period(),
            "margin_adjusted_growth": self.metrics.growth_rate * self.metrics.gross_margin
        }

    def calculate_retention_metrics(self) -> Dict[str, float]:
        """Calculate retention-related metrics"""
        return {
            "logo_retention": 1 - self.metrics.churn_rate,
            "net_revenue_retention": (
                1 - self.metrics.churn_rate + 
                (self.metrics.expansion_revenue / self.metrics.mrr)
            ),
            "customer_lifetime": 1 / self.metrics.churn_rate
        }

    def calculate_revenue_quality(self) -> Dict[str, float]:
        """Calculate revenue quality metrics"""
        return {
            "arpu_efficiency": self.metrics.arpu / self.metrics.support_costs,
            "gross_margin": self.metrics.gross_margin,
            "recurring_revenue_ratio": self.metrics.mrr * 12 / (self.metrics.mrr * 12 + self.metrics.expansion_revenue * 12)
        }

    def calculate_growth_metrics(self) -> Dict[str, float]:
        """Calculate growth-related metrics"""
        return {
            "monthly_growth_rate": self.metrics.growth_rate,
            "annual_growth_rate": (1 + self.metrics.growth_rate) ** 12 - 1,
            "expansion_revenue_ratio": self.metrics.expansion_revenue / self.metrics.mrr
        }

    def calculate_valuation_multiples(self) -> Dict[str, float]:
        """
        Calculate recommended valuation multiples based on metrics
        Returns different multiple ranges based on company performance
        """
        efficiency_metrics = self.calculate_efficiency_metrics()
        retention_metrics = self.calculate_retention_metrics()
        revenue_quality = self.calculate_revenue_quality()
        
        # Base multiple ranges for UCaaS companies
        arr = self.calculate_arr()
        base_multiple = 5.0  # Starting point
        
        # Adjust multiple based on key metrics
        adjustments = 0.0
        
        # Growth rate impact (0-3x adjustment)
        if self.metrics.growth_rate > 0.1:  # >10% monthly growth
            adjustments += 3.0
        elif self.metrics.growth_rate > 0.05:  # >5% monthly growth
            adjustments += 1.5
            
        # Net Revenue Retention impact (0-2x adjustment)
        if retention_metrics["net_revenue_retention"] > 1.1:  # >110% NRR
            adjustments += 2.0
        elif retention_metrics["net_revenue_retention"] > 1.0:  # >100% NRR
            adjustments += 1.0
            
        # Gross Margin impact (0-2x adjustment)
        if revenue_quality["gross_margin"] > 0.8:  # >80% margin
            adjustments += 2.0
        elif revenue_quality["gross_margin"] > 0.7:  # >70% margin
            adjustments += 1.0
            
        # Scale impact (0-3x adjustment)
        if arr > 100_000_000:  # >$100M ARR
            adjustments += 3.0
        elif arr > 10_000_000:  # >$10M ARR
            adjustments += 1.5
            
        # Efficiency impact (0-2x adjustment)
        if efficiency_metrics["ltv_cac_ratio"] > 3:
            adjustments += 2.0
        elif efficiency_metrics["ltv_cac_ratio"] > 2:
            adjustments += 1.0
            
        final_multiple = base_multiple + adjustments
        
        return {
            "arr_multiple_low": final_multiple - 2,
            "arr_multiple_mid": final_multiple,
            "arr_multiple_high": final_multiple + 2,
            "mrr_multiple_low": final_multiple * 12 - 24,
            "mrr_multiple_mid": final_multiple * 12,
            "mrr_multiple_high": final_multiple * 12 + 24
        }

    def perform_valuation(self) -> Dict[str, Any]:
        """
        Perform comprehensive UCaaS valuation analysis
        Returns all metrics and valuation ranges
        """
        arr = self.calculate_arr()
        multiples = self.calculate_valuation_multiples()
        
        return {
            "metrics": {
                "arr": arr,
                "ltv": self.calculate_ltv(),
                "efficiency": self.calculate_efficiency_metrics(),
                "retention": self.calculate_retention_metrics(),
                "revenue_quality": self.calculate_revenue_quality(),
                "growth": self.calculate_growth_metrics()
            },
            "valuation_ranges": {
                "arr_based": {
                    "low": arr * multiples["arr_multiple_low"],
                    "mid": arr * multiples["arr_multiple_mid"],
                    "high": arr * multiples["arr_multiple_high"]
                },
                "mrr_based": {
                    "low": self.metrics.mrr * multiples["mrr_multiple_low"],
                    "mid": self.metrics.mrr * multiples["mrr_multiple_mid"],
                    "high": self.metrics.mrr * multiples["mrr_multiple_high"]
                }
            },
            "multiples": multiples,
            "benchmarks": {
                "rule_of_40": self.metrics.growth_rate * 100 + (self.metrics.gross_margin * 100),
                "magic_number": (self.metrics.mrr * 12) / (self.metrics.cac * self.metrics.customers),
                "burn_multiple": self.metrics.cac / (self.metrics.mrr * self.metrics.gross_margin)
            }
        }
