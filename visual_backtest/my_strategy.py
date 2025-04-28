from vnpy_ctastrategy.template import CtaTemplate
from vnpy.trader.object import BarData

class MyVisualStrategy(CtaTemplate):
    author = "你"

    fast_window = 5
    slow_window = 20

    parameters = ["fast_window", "slow_window"]
    variables = []

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.close_prices = []

    def on_bar(self, bar: BarData):
        self.close_prices.append(bar.close_price)
        if len(self.close_prices) > self.slow_window:
            fast_ma = sum(self.close_prices[-self.fast_window:]) / self.fast_window
            slow_ma = sum(self.close_prices[-self.slow_window:]) / self.slow_window

            if fast_ma > slow_ma and self.pos == 0:
                self.buy(bar.close_price, 1)
            elif fast_ma < slow_ma and self.pos > 0:
                self.sell(bar.close_price, 1)

        self.put_event()
