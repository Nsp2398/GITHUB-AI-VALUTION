import numpy as np
from typing import Dict, List

class DCFCalculator:
    def __init__(self, 
                 revenue: float,
                 growth_rate: float,
                 ebitda_margin: float,
                 discount_rate: float,
                 terminal_growth_rate: float,
                 projection_years: int = 5):
        self.revenue = revenue
        self.growth_rate = growth_rate
        self.ebitda_margin = ebitda_margin
        self.discount_rate = discount_rate
        self.terminal_growth_rate = terminal_growth_rate
        self.projection_years = projection_years

    def project_revenue(self) -> List[float]:
        """Project revenue for the forecast period."""
        revenues = []
        current_revenue = self.revenue
        
        for _ in range(self.projection_years):
            current_revenue *= (1 + self.growth_rate)
            revenues.append(current_revenue)
            
        return revenues

    def calculate_fcf(self, revenue: float) -> float:
        """Calculate Free Cash Flow from revenue."""
        ebitda = revenue * self.ebitda_margin
        # Simplified FCF calculation
        # In real world, we'd consider changes in working capital, capex, etc.
        fcf = ebitda * 0.7  # Assuming 30% for taxes and maintenance capex
        return fcf

    def calculate_terminal_value(self, final_fcf: float) -> float:
        """Calculate terminal value using perpetual growth method."""
        return final_fcf * (1 + self.terminal_growth_rate) / (self.discount_rate - self.terminal_growth_rate)

    def calculate_present_value(self, future_value: float, year: int) -> float:
        """Calculate present value of a future cash flow."""
        return future_value / ((1 + self.discount_rate) ** year)

    def perform_dcf_valuation(self) -> Dict[str, float]:
        """Perform full DCF valuation."""
        # Project revenues
        projected_revenues = self.project_revenue()
        
        # Calculate FCF for each year
        fcfs = [self.calculate_fcf(rev) for rev in projected_revenues]
        
        # Calculate terminal value
        terminal_value = self.calculate_terminal_value(fcfs[-1])
        
        # Calculate present value of FCFs
        pv_fcfs = [self.calculate_present_value(fcf, year + 1) 
                   for year, fcf in enumerate(fcfs)]
        
        # Calculate present value of terminal value
        pv_terminal = self.calculate_present_value(terminal_value, self.projection_years)
        
        # Calculate enterprise value
        enterprise_value = sum(pv_fcfs) + pv_terminal
        
        return {
            'enterprise_value': enterprise_value,
            'present_value_fcf': sum(pv_fcfs),
            'present_value_terminal': pv_terminal,
            'projected_fcfs': fcfs,
            'terminal_value': terminal_value
        }

class UCaaSMetrics:
    @staticmethod
    def calculate_ltv(arpu: float, gross_margin: float, churn_rate: float) -> float:
        """Calculate Customer Lifetime Value."""
        return (arpu * gross_margin) / churn_rate

    @staticmethod
    def calculate_payback_period(cac: float, arpu: float, gross_margin: float) -> float:
        """Calculate CAC Payback Period in months."""
        return cac / (arpu * gross_margin)

    @staticmethod
    def calculate_efficiency_score(ltv: float, cac: float) -> float:
        """Calculate LTV/CAC ratio."""
        return ltv / cac if cac > 0 else 0
