from datetime import datetime
import sqlite3
import os
import threading
import time
import random

# 价格缓冲区
global_price_cache = {}
golbal_preclose_price_cache = {}
# 缓存锁
price_cache_lock = threading.Lock()
# 缓存过期时间(秒)
CACHE_EXPIRE_TIME = 5*60  # 5分钟

def init_db():
    db_path = 'positions.db'
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        sql_file = os.path.join(os.path.dirname(__file__), 'positions.sql')
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()

# 持仓数据缓存
cached_positions = None
positions_cache_lock = threading.Lock()

def get_positions_from_db(force_refresh=False):
    global cached_positions
    
    with positions_cache_lock:
        if cached_positions is None or force_refresh:
            conn = sqlite3.connect('positions.db')
            cursor = conn.cursor()
            
            cursor.execute("""SELECT name FROM sqlite_master 
                          WHERE type='table' AND name='positions'""")
            if not cursor.fetchone():
                sql_file = os.path.join(os.path.dirname(__file__), 'positions.sql')
                with open(sql_file, 'r', encoding='utf-8') as f:
                    sql_script = f.read()
                cursor.executescript(sql_script)
                conn.commit()
                
            cursor.execute("""
                SELECT 
                    symbol, name, type, portfolio, quantity, 
                    avg_price, current_price, preclose_price,
                    margin_ratio, point_value, target_symbol 
                FROM positions 
                ORDER BY type
            """)
            positions = cursor.fetchall()
            
            position_list = []
            
            for pos in positions:
                position = {
                    'symbol': pos[0],
                    'name': pos[1],
                    'type': pos[2],
                    'portfolio': pos[3],
                    'quantity': pos[4],
                    'avg_price': pos[5],
                    'current_price': pos[6] if pos[6] != 0 else pos[5],
                    'preclose_price': pos[7] if pos[7]!= 0 else pos[5],
                    'margin_ratio': pos[8] if len(pos) > 7 else None,
                    'point_value': pos[9] if len(pos) > 8 else None,
                    'target_symbol': pos[10] if len(pos) > 9 else None
                }
                position_list.append(position)
            
            conn.close()
            cached_positions = position_list
            
    return cached_positions

def init_price_cache():
    """初始化价格缓存"""
    positions = get_positions_from_db()
    with price_cache_lock:
        for position in positions:
            symbol = position['symbol']
            global_price_cache[symbol] = position['current_price']
            golbal_preclose_price_cache[symbol] = position['preclose_price']
        # 确保cash有默认值
        global_price_cache['cash'] = 1.0
        golbal_preclose_price_cache['cash'] = 1.0

def update_price_db():
    """将缓存中的最新价格更新到数据库并刷新缓存"""
    with price_cache_lock, positions_cache_lock:
        conn = sqlite3.connect('positions.db')
        cursor = conn.cursor()
        
        for symbol, current_price in global_price_cache.items():
            preclose_price = golbal_preclose_price_cache.get(symbol, 0)
            cursor.execute("""
                UPDATE positions 
                SET current_price = ?, preclose_price = ?
                WHERE symbol = ?
            """, (current_price, preclose_price, symbol))
            
            # 更新cached_positions中的价格
            if cached_positions:
                for position in cached_positions:
                    if position['symbol'] == symbol:
                        position['current_price'] = current_price
                        position['preclose_price'] = preclose_price
        
        conn.commit()
        conn.close()

import akshare as ak
def update_stock_price_cache():
    """专门更新A股股票价格缓存"""
    try:
        # 获取A股实时行情数据
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        stock_data = stock_zh_a_spot_df.set_index('代码')['最新价'].to_dict()
        preclose_data = stock_zh_a_spot_df.set_index('代码')['昨收'].to_dict()
        
        with price_cache_lock:
            for symbol in list(global_price_cache.keys()):
                if symbol in stock_data:
                    global_price_cache[symbol] = stock_data[symbol]
                if symbol in preclose_data:
                    golbal_preclose_price_cache[symbol] = preclose_data[symbol]
    except Exception as e:
        print(f"更新A股价格缓存出错: {e}")
        return False
    return True

def update_price_cache():
    """定时更新价格缓存"""
    while True:
        # 检查缓存是否初始化（判断字典是否为空）
        if len(global_price_cache) == 0 or len(golbal_preclose_price_cache) == 0:
            init_price_cache()
        
        rlt = update_stock_price_cache()
        update_price_db()
        if rlt:
            print(f"价格缓存更新完成，当前时间: {datetime.now()}")
        else:
            print(f"价格缓存更新失败，当前时间: {datetime.now()}")
        time.sleep(CACHE_EXPIRE_TIME)

# 启动缓存更新线程
cache_updater = threading.Thread(target=update_price_cache, daemon=True)
cache_updater.start()

def get_real_time_price(symbol):
    """从缓存获取实时价格和前收盘价"""
    with price_cache_lock:
        return global_price_cache.get(symbol, 0)

def get_preclose_price(symbol):
    """从缓存获取实时价格和前收盘价"""
    with price_cache_lock:
        return golbal_preclose_price_cache.get(symbol, 0)

