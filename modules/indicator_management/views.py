from flask import render_template, jsonify
from . import indicator_blueprint

# 示例指标数据
sample_indicators = {
    'market': {
        'PE_Ratio': 25.3,
        'PB_Ratio': 3.2,
        'Dividend_Yield': 1.8
    },
    'triggers': [
        {'name': 'PE_Ratio', 'value': 25.3, 'threshold': 30, 'direction': 'above'},
        {'name': 'Dividend_Yield', 'value': 1.8, 'threshold': 2.0, 'direction': 'below'}
    ]
}

@indicator_blueprint.route('/')
def indicator_dashboard():
    return render_template('indicator/dashboard.html', 
                         indicators=sample_indicators)

@indicator_blueprint.route('/api/indicators')
def get_indicators():
    return jsonify(sample_indicators)