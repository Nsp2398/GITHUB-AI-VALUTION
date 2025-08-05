from services.ucaas_valuation import UCaaSMetrics, UCaaSValuation

@app.route('/api/valuations/ucaas', methods=['POST'])
def calculate_ucaas_valuation():
    data = request.json
    
    try:
        # Create UCaaS metrics from request data
        metrics = UCaaSMetrics(
            mrr=data['mrr'],
            arpu=data['arpu'],
            customers=data['customers'],
            churn_rate=data['churn_rate'],
            cac=data['cac'],
            gross_margin=data['gross_margin'],
            growth_rate=data['growth_rate'],
            expansion_revenue=data.get('expansion_revenue', 0),
            support_costs=data.get('support_costs', 0)
        )
        
        # Initialize valuation calculator
        valuator = UCaaSValuation(metrics)
        
        # Perform valuation
        result = valuator.perform_valuation()
        
        # Get AI insights for the valuation
        metrics_for_ai = {
            'arr': result['metrics']['arr'],
            'ltv': result['metrics']['ltv'],
            'growth_rate': metrics.growth_rate,
            'net_revenue_retention': result['metrics']['retention']['net_revenue_retention'],
            'gross_margin': metrics.gross_margin,
            'rule_of_40': result['benchmarks']['rule_of_40'],
            'magic_number': result['benchmarks']['magic_number']
        }
        
        ai_insights = ai_service.analyze_metrics(metrics_for_ai)
        
        # Combine results
        return jsonify({
            'valuation_results': result,
            'ai_insights': ai_insights
        }), 200
        
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
