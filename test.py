import requests
resp = requests.get(
    "https://api.bybit.com/v5/market/time",
    proxies={"https": "socks5h://127.0.0.1:7890"}
)
print(resp.status_code, resp.json())


import requests
response = requests.get("https://api.bybit.com", verify=certifi.where())
print(response.status_code)  # 应返回200