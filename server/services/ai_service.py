import openai
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class ValuationAI:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def analyze_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze company metrics and provide AI-powered recommendations."""
        
        prompt = f"""
        Analyze the following UCaaS company metrics and provide valuation insights:
        
        Financial Metrics:
        - Revenue: ${metrics.get('revenue', 0):,.2f}
        - Growth Rate: {metrics.get('growth_rate', 0) * 100:.1f}%
        - EBITDA Margin: {metrics.get('ebitda_margin', 0) * 100:.1f}%
        
        UCaaS Specific Metrics:
        - Monthly Recurring Revenue: ${metrics.get('mrr', 0):,.2f}
        - ARPU: ${metrics.get('arpu', 0):.2f}
        - Churn Rate: {metrics.get('churn_rate', 0) * 100:.1f}%
        - CAC: ${metrics.get('cac', 0):.2f}
        - LTV: ${metrics.get('ltv', 0):.2f}
        
        Please provide:
        1. Valuation multiple recommendations
        2. Key strengths and concerns
        3. Growth opportunities
        4. Risk factors
        5. Comparable company suggestions
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a UCaaS valuation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            analysis = response.choices[0].message.content

            # Extract key insights (simplified)
            return {
                'analysis': analysis,
                'confidence_score': 0.85,  # Placeholder - could be calculated based on metric quality
                'recommendations': analysis.split('\n\n')[1:],  # Skip the first paragraph
            }

        except Exception as e:
            return {
                'error': str(e),
                'analysis': 'Unable to generate AI analysis',
                'confidence_score': 0,
                'recommendations': []
            }

    def suggest_valuation_range(self, 
                              dcf_value: float, 
                              metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest a valuation range based on DCF and company metrics."""
        
        prompt = f"""
        Given the following valuation inputs:
        
        DCF Valuation: ${dcf_value:,.2f}
        
        Company Metrics:
        - Revenue: ${metrics.get('revenue', 0):,.2f}
        - Growth Rate: {metrics.get('growth_rate', 0) * 100:.1f}%
        - EBITDA Margin: {metrics.get('ebitda_margin', 0) * 100:.1f}%
        
        Please suggest:
        1. A reasonable valuation range
        2. Recommended valuation multiples
        3. Confidence level in the valuation
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a UCaaS valuation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            analysis = response.choices[0].message.content

            return {
                'analysis': analysis,
                'confidence_score': 0.8,  # Placeholder
                'valuation_range': {
                    'low': dcf_value * 0.8,  # Simplified range calculation
                    'high': dcf_value * 1.2
                }
            }

        except Exception as e:
            return {
                'error': str(e),
                'analysis': 'Unable to generate valuation range',
                'confidence_score': 0,
                'valuation_range': None
            }
