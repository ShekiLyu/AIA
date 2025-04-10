-- SQLite数据库表结构
-- 持仓表
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,  -- 符号
    name TEXT,  -- 名称
    type TEXT NOT NULL,  -- 类型: stock/etf/fund/option/future/cash/us_stock/target
    portfolio TEXT NOT NULL DEFAULT '默认组合',  -- 组合名称
    quantity REAL NOT NULL,  -- 持仓数量
    avg_price REAL NOT NULL,  -- 成本价
    current_price REAL NOT NULL DEFAULT 0.0,  -- 当前价格
    preclose_price REAL NOT NULL DEFAULT 0.0,  -- 昨收
    margin_ratio REAL,  -- 保证金比例(仅期货)
    point_value REAL,  -- 每点价格(期权/期货)
    target_symbol TEXT  -- 跟踪标的(场外基金/期权/期货)
);

-- 示例数据
-- 股票
INSERT INTO positions (symbol, name, type, quantity, avg_price) VALUES 
('AAPL', '苹果公司', 'stock', 100, 150.25),
('MSFT', '微软公司', 'stock', 50, 250.75);

-- ETF基金
INSERT INTO positions (symbol, name, type, quantity, avg_price) VALUES 
('SPY', '标普500ETF', 'etf', 20, 350.60);

-- 场外基金
INSERT INTO positions (symbol, name, type, quantity, avg_price, target_symbol) VALUES 
('000001', '华夏成长混合', 'fund', 5000, 1.25, 'CSI300');

-- 期权
INSERT INTO positions (symbol, name, type, quantity, avg_price, point_value, target_symbol) VALUES 
('AAPL210916C00150000', '苹果看涨期权', 'option', 10, 5.20, 100, 'AAPL');

-- 期货
INSERT INTO positions (symbol, name, type, quantity, avg_price, margin_ratio, point_value, target_symbol) VALUES 
('IF2109', '沪深300指数期货', 'future', 2, 5000.00, 0.15, 300, 'CSI300');

-- 现金
INSERT INTO positions (symbol, name, type, quantity, avg_price) VALUES 
('CNY', '人民币', 'cash', 100000, 1.00);

-- 美股
INSERT INTO positions (symbol, name, type, quantity, avg_price) VALUES 
('TSLA', '特斯拉', 'us_stock', 5, 700.50);

-- 跟踪标的示例
INSERT INTO positions (symbol, name, type, quantity, avg_price, target_symbol) VALUES 
('510300', '华泰柏瑞沪深300ETF', 'etf', 1000, 5.20, 'CSI300');