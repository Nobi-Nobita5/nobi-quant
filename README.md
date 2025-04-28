# VeighNa框架Bybit加密货币交易模块集成说明

## 项目概述
本项目基于VeighNa量化交易框架（原vn.py），新增对Bybit加密货币交易所的全面支持。主要实现以下功能：
- Bybit全品类合约交易接口（期货/现货/期权）
- 实时行情订阅与历史数据下载
- 账户资产与持仓监控
- 低延迟私有Websocket连接

## 功能特性
**核心功能**：

- 支持Bybit统一账户(UNIFIED)交易模式
- 覆盖线性/反向合约、现货、期权交易品种
- 提供Tick/1分钟/K线等多粒度历史数据
- 支持市价单、限价单等常见订单类型

 **增强特性**：
- 优化Websocket断线重连机制
- 增加交易品种分类自动识别
- 支持混合保证金模式仓位查询
- 深度整合vnpy_ctabacktester回测引擎

## 代码改动说明

### 1. 交易所枚举扩展
`vnpy/trader/constant.py`:
```python
class Exchange(Enum):
    # ...原有交易所...
    BYBIT = "BYBIT"  # 新增Bybit交易所枚举
```

<img src="https://raw.githubusercontent.com/Nobi-Nobita5/study-notes/master/img/image-20250428203844749.png?token=ARXTR55SIPU2F5RM3ZJ2IWLIB53US" alt="image-20250428203844749" style="zoom: 33%;" />

### 2. 统一账户模式支持

`vnpy_bybit/bybit_gateway.py`:
```python
def query_account(self) -> None:
    account_type = "UNIFIED"  # 强制使用统一账户模式
    params: dict = {"accountType": account_type}
    # ...
```

### 3. WebSocket连接优化
`vnpy_bybit/bybit_gateway.py`:
```python
# 移除冗余参数，使用kwargs接收
def on_disconnected(self, status_code: int, msg: str, **kwargs) -> None:
    category: str = kwargs.get("category", "")
    # ...

# 添加category参数
def on_error(self, e: Exception, category: str = "") -> None:
    msg: str = f"Public websocket API ({category}) error: {e}"
```

### 4. 新增数据服务模块
`vnpy_bybitdatafeed/datafeed.py`:
```python
class BybitDatafeed(BaseDatafeed):
    def query_bar_history(self, req: HistoryRequest) -> List[BarData]:
        # 实现多时间粒度历史数据下载
```

## 环境配置

### 依赖安装

### API密钥配置
在VeighNa Trader中：
1. 进入"全局配置"
2. 选择"Bybit"网关
3. 填写以下信息：
```
API Key: <Your_API_Key>
Secret Key: <Your_Secret_Key>
Server: REAL/DEMO
```

## 目录结构
```
.
├── vnpy
│   └── trader
│       └── constant.py          # 交易所枚举扩展
├── vnpy_bybit
│   └── bybit_gateway.py         # 核心交易网关
└── vnpy_bybitdatafeed
    └── datafeed.py              # 历史数据服务模块
```

## 注意事项

1. **API权限**：确保API密钥已开通「交易」和「行情」权限
2. **网络要求**：推荐使用香港/新加坡服务器以获得更低延迟
3. **风控限制**：Bybit API默认每秒10次调用限制
4. **模拟交易**：DEMO环境需使用`DEMO`服务器配置

## 故障排查

常见问题解决方案：

- **连接超时**：检查防火墙设置，开放TCP 80/443端口
- **签名错误**：同步本地时间至网络时间服务器
- **仓位不同步**：调用`query_position()`强制刷新

> 更多技术细节请参考[Bybit API文档](https://bybit-exchange.github.io/docs/v5/)

## 其他使用指南

### 行情订阅
```python
from vnpy.trader.object import SubscribeRequest

sub_req = SubscribeRequest(
    symbol="BTCUSDT", 
    exchange=Exchange.BYBIT
)
main_engine.subscribe(sub_req, "BYBIT")
```

### 策略回测
```python
from vnpy_ctabacktester import BacktestingEngine

engine = BacktestingEngine()
engine.set_parameters(
    vt_symbol="BTCUSDT.BYBIT",
    interval=Interval.MINUTE,
    start=datetime(2023, 1, 1),
    end=datetime(2023, 12, 31),
    rate=0.0002,    # Bybit手续费率
    slippage=0.5     # 滑点设置
)
```
