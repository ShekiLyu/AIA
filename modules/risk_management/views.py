from flask import render_template, jsonify
from . import risk_blueprint

# 示例风险数据
sample_risks = {
    'exposure': {
        'stocks': 15000,
        'funds': 7600,
        'total': 22600
    },
    'suggestions': [
        '考虑减少科技股持仓以降低行业集中度风险',
        '建议增加债券基金配置以平衡投资组合'
    ]
}

@risk_blueprint.route('/')
def risk_dashboard():
    return render_template('risk/dashboard.html', 
                         risks=sample_risks)

@risk_blueprint.route('/api/risks')
def get_risks():
    return jsonify(sample_risks)