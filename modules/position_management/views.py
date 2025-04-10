from flask import render_template, jsonify
from datetime import datetime
from . import position_blueprint
from .services import get_real_time_price,get_preclose_price, get_positions_from_db
    
@position_blueprint.route('/')
def position_dashboard():
    positions = get_positions_from_db(force_refresh=True)
    
    # 按portfolio分组
    portfolio_positions = {}
    
    # 获取实时价格并计算盈亏
    for position in positions:
        portfolio = position.get('portfolio', '默认组合')
        if portfolio not in portfolio_positions:
            portfolio_positions[portfolio] = []
        
        position['current_price'] = get_real_time_price(position['symbol'])
        position['pre_close_price'] = get_preclose_price(position['symbol'])
        
        # 计算总盈亏（保留原有逻辑）
        if position['type'] in ['future', 'option']:
            position['profit'] = (position['current_price'] - position['avg_price']) * position['quantity'] * position.get('point_value', 1)
        else:
            position['profit'] = (position['current_price'] - position['avg_price']) * position['quantity']
            
        position['profit_pct'] = (position['current_price'] / position['avg_price'] - 1) * 100
        
        # 计算日盈亏
        position['daily_return'] = (position['current_price'] - position['pre_close_price']) * position['quantity']

        # 计算市值
        if position['type'] in ['future', 'option']:
            # TODO: 期货/期权市值计算需要特殊处理
            position['market_value'] = position['current_price'] * position['quantity']
        else:
            position['market_value'] = position['current_price'] * position['quantity']
        
        portfolio_positions[portfolio].append(position)
      
    return render_template('position/dashboard.html', 
                         positions=portfolio_positions)

    
@position_blueprint.route('/api/realtime_prices')
def get_realtime_prices():
    # 只返回symbol和current_price以减少数据传输量
    prices = []
    positions = get_positions_from_db()
    for position in positions:
        prices.append({
            'symbol': position['symbol'],
            'current_price': get_real_time_price(position['symbol']),
            'pre_close_price': get_preclose_price(position['symbol'])
        })
    
    return jsonify(prices)