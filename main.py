from flask import Flask, render_template
from modules.position_management import position_blueprint
from modules.risk_management import risk_blueprint
from modules.indicator_management import indicator_blueprint
from modules.strategy_management import strategy_blueprint

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(position_blueprint)
app.register_blueprint(risk_blueprint)
app.register_blueprint(indicator_blueprint)
app.register_blueprint(strategy_blueprint)

@app.route('/')
def index():
    from modules.position_management.views import position_dashboard
    return position_dashboard()

if __name__ == '__main__':
    app.run(debug=True)