# 1、constant.py中添加BYBIT枚举
# 2、bybit_gateway.py中account_type = "UNIFIED"
# 3、bybit_gateway再加上两处新代码，移除冗余参数、添加category参数
# 4、新增nvpy_bybitdatafeed数据服务模块
# 写在顶部
from vnpy_chartwizard import ChartWizardApp
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

# from vnpy_ctp import CtpGateway
from vnpy_ctastrategy import CtaStrategyApp
from vnpy_ctabacktester import CtaBacktesterApp
from vnpy_bybit import BybitGateway  # ✅ 新增




def main():
    """Start VeighNa Trader"""
    qapp = create_qapp()

    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    # 写在创建main_engine对象后
    main_engine.add_app(ChartWizardApp)

    # 添加交易网关
    # main_engine.add_gateway(CtpGateway)
    main_engine.add_gateway(BybitGateway)  # ✅ 新增：Bybit 现货/合约接入

    # 添加应用模块
    main_engine.add_app(CtaStrategyApp)
    main_engine.add_app(CtaBacktesterApp)

    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()

    qapp.exec()


if __name__ == "__main__":
    main()
