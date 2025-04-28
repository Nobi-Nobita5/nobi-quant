#自定义的，手动编写策略的回测脚本的模块

from datetime import datetime
import pandas as pd
import plotly.graph_objs as go

from vnpy_ctabacktester.engine import BacktestingEngine
from my_strategy import MyVisualStrategy

# 1. 初始化回测引擎并设置参数
engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="btcusdt.BYBIT",
    interval="1m",
    start=datetime(2024, 1, 1),
    end=datetime(2024, 1, 10),
    rate=0.0005,
    slippage=1,
    size=1,
    pricetick=0.1,
    capital=10000,
)

# 2. 添加并运行策略
engine.add_strategy(MyVisualStrategy, {
    "fast_window": 5,
    "slow_window": 20
})
engine.load_data()
engine.run_backtesting()

# 3. 兼容 dict 或 list 的 history_data 提取
raw_history = engine.history_data
if isinstance(raw_history, dict):
    bars = raw_history.get(engine.vt_symbol, [])
else:
    bars = raw_history

if not bars:
    raise RuntimeError("❌ 没有加载到任何 BarData，请先导入历史数据")

# 4. 转为 DataFrame，并重命名列为 open/high/low/close
df_bars = pd.DataFrame([{
    "datetime": bar.datetime,
    "open":      bar.open_price,
    "high":      bar.high_price,
    "low":       bar.low_price,
    "close":     bar.close_price,
    "volume":    bar.volume
} for bar in bars])
df_bars.set_index("datetime", inplace=True)

# 5. 提取所有成交信号
trade_list = engine.get_all_trades()  # 直接使用返回的 trade_list

# 6. 绘图函数
def plot_strategy(df: pd.DataFrame):
    fig = go.Figure()

    # K线
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="K线"
    ))

    # 双均线（MA5 & MA20）
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["close"].rolling(window=5).mean(),
        name="MA5"
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["close"].rolling(window=20).mean(),
        name="MA20"
    ))

    # 买卖点
    for trade in trade_list:
        color = "green" if trade.direction.name == "LONG" else "red"
        symbol = "triangle-up" if color=="green" else "triangle-down"
        label = "买入" if color == "green" else "卖出"
        fig.add_trace(go.Scatter(
            x=[trade.datetime],
            y=[trade.price],
            mode="markers",
            marker=dict(size=10, symbol=symbol, color=color),
            name=label
        ))

    fig.update_layout(
        title=f"{engine.vt_symbol} 回测结果",
        xaxis_rangeslider_visible=False
    )
    fig.show()

# 7. 调用绘图
plot_strategy(df_bars)
