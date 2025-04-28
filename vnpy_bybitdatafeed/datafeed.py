from datetime import datetime
from typing import List
import requests

from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.object import HistoryRequest, BarData
from vnpy.trader.datafeed import BaseDatafeed
from vnpy.trader.utility import ZoneInfo

INTERVAL_MAP = {
    Interval.MINUTE: "1",
    Interval.HOUR: "60",
    Interval.HOUR4: "240",
    Interval.DAILY: "D"
}

class BybitDatafeed(BaseDatafeed):
    """
    Bybit 加密货币历史K线数据服务。
    """
    def __init__(self):
        super().__init__()
        self.session = requests.Session()

    def query_bar_history(self, req: HistoryRequest) -> List[BarData]:
        """
        获取历史K线数据。
        """
        print(f"[BybitDatafeed] 正在请求历史数据：{req.symbol}, {req.interval}, {req.start} - {req.end}")

        symbol = req.symbol
        interval = INTERVAL_MAP.get(req.interval)
        if not interval:
            return []

        start_ts = int(req.start.timestamp() * 1000)
        end_ts = int(req.end.timestamp() * 1000)

        url = "https://api.bybit.com/v5/market/kline"
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": interval,
            "start": start_ts,
            "end": end_ts,
            "limit": 1000
        }

        resp = self.session.get(url, params=params)
        data = resp.json()

        bars = []
        if data.get("retCode") != 0:
            print(f"[BybitDatafeed] API 错误: {data}")
            return bars

        for item in data["result"]["list"]:
            dt = datetime.fromtimestamp(int(item[0]) / 1000).replace(tzinfo=ZoneInfo("UTC"))
            bar = BarData(
                symbol=symbol,
                exchange=Exchange.BYBIT,
                datetime=dt,
                interval=req.interval,
                open_price=float(item[1]),
                high_price=float(item[2]),
                low_price=float(item[3]),
                close_price=float(item[4]),
                volume=float(item[5]),
                open_interest=0,
                gateway_name="BYBIT"
            )
            bars.append(bar)

        return bars
