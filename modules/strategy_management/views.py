from flask import render_template, jsonify
from . import strategy_blueprint

# 示例策略数据
sample_strategies = {
    'strategies': [
        {
            'name': '价值投资', 
            'positions': ['AAPL', 'MSFT'],
            'next_action': {
                'condition': 'PE_Ratio < 25',
                'action': '买入更多AAPL'
            }
        },
        {
            'name': '趋势跟踪',
            'positions': ['SPY'],
            'next_action': {
                'condition': '价格突破200日均线',
                'action': '增持SPY'
            }
        }
    ]
}

@strategy_blueprint.route('/')
def strategy_dashboard():
    return render_template('strategy/dashboard.html', 
                         strategies=sample_strategies)

@strategy_blueprint.route('/api/strategies')
def get_strategies():
    return jsonify(sample_strategies)