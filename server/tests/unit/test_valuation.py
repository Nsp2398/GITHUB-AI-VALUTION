import pytest
from services.valuation import DCFCalculator
from services.ucaas_valuation import UCaaSMetrics
from decimal import Decimal

@pytest.fixture
def dcf_calculator():
    return DCFCalculator()

@pytest.fixture
def sample_financials():
    return {
        "revenue": 1000000,
        "growth_rate": 0.15,
        "ebitda_margin": 0.25,
        "tax_rate": 0.21,
        "discount_rate": 0.12,
        "terminal_growth_rate": 0.03,
        "projection_years": 5
    }

def test_dcf_calculation(dcf_calculator, sample_financials):
    result = dcf_calculator.calculate_dcf(
        revenue=sample_financials["revenue"],
        growth_rate=sample_financials["growth_rate"],
        ebitda_margin=sample_financials["ebitda_margin"],
        tax_rate=sample_financials["tax_rate"],
        discount_rate=sample_financials["discount_rate"],
        terminal_growth_rate=sample_financials["terminal_growth_rate"],
        projection_years=sample_financials["projection_years"]
    )
    
    assert isinstance(result, dict)
    assert "enterprise_value" in result
    assert result["enterprise_value"] > 0
    assert len(result["projected_cash_flows"]) == sample_financials["projection_years"]

@pytest.fixture
def ucaas_metrics():
    return UCaaSMetrics()

@pytest.fixture
def sample_ucaas_data():
    return {
        "mrr": 100000,
        "customers": 1000,
        "churn_rate": 0.05,
        "cac": 1000,
        "expansion_revenue": 10000,
        "contraction_revenue": 5000
    }

def test_ucaas_metrics_calculation(ucaas_metrics, sample_ucaas_data):
    result = ucaas_metrics.calculate_metrics(
        mrr=sample_ucaas_data["mrr"],
        customers=sample_ucaas_data["customers"],
        churn_rate=sample_ucaas_data["churn_rate"],
        cac=sample_ucaas_data["cac"],
        expansion_revenue=sample_ucaas_data["expansion_revenue"],
        contraction_revenue=sample_ucaas_data["contraction_revenue"]
    )
    
    assert isinstance(result, dict)
    assert "arr" in result
    assert "arpu" in result
    assert "ltv" in result
    assert "net_revenue_retention" in result
    
    # Test ARR calculation
    assert result["arr"] == sample_ucaas_data["mrr"] * 12
    
    # Test ARPU calculation
    assert result["arpu"] == sample_ucaas_data["mrr"] / sample_ucaas_data["customers"]
    
    # Test Net Revenue Retention
    expected_nrr = (sample_ucaas_data["mrr"] + 
                    sample_ucaas_data["expansion_revenue"] - 
                    sample_ucaas_data["contraction_revenue"]) / sample_ucaas_data["mrr"]
    assert abs(result["net_revenue_retention"] - expected_nrr) < 0.01  # Allow for small floating-point differences
