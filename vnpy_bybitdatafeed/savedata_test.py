from datetime import datetime
from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.object import HistoryRequest
from vnpy.trader.database import get_database

# 获取数据服务实例
datafeed = get_datafeed()

# 构造历史数据请求
req = HistoryRequest(
    symbol="BTCUSDT",
    exchange=Exchange.BYBIT,
    start=datetime(2024, 1, 1),
    end=datetime(2024, 1, 8),
    interval=Interval.MINUTE
)

# 查询历史K线
data = datafeed.query_bar_history(req)

print(f"\n✅ 成功获取 {len(data)} 条 K线数据")
print("示例数据前3条：")
for bar in data[:3]:
    print(bar)

# 获取数据库实例
database = get_database()

# 手动保存数据并打印调试信息
from vnpy.trader.database import DB_TZ
from vnpy.trader.object import BarData
import traceback

count = 0

for bar in data:
    # 确保 datetime 字段为 tz-aware 的 UTC 时区
    bar.datetime = bar.datetime.astimezone(DB_TZ)

    # 打印调试信息（symbol, datetime, close）
    print(f"正在写入: {bar.symbol} - {bar.datetime} - {bar.close_price}")

    try:
        # 使用 save_bar_data 支持批量，也可以逐条插入测试
        database.save_bar_data([bar])
        count += 1
    except Exception as e:
        print("❌ 写入出错：", e)
        traceback.print_exc()

print(f"\n✅ 实际成功写入 {count} 条记录到数据库中")
