import requests
import json

url = "http://127.0.0.1:5000/api/work-orders/query"
data = {
    "orderIds": ["260403023790001", "260403023790002"]
}

print("=" * 80)
print("批量查询接口测试")
print("=" * 80)

response = requests.post(url, json=data)
result = response.json()

print(f"响应状态码: {response.status_code}")
print(f"响应数据:")
print(json.dumps(result, indent=2, ensure_ascii=False))

print("=" * 80)
print(f"返回的键: {list(result.keys())}")
print(f"orders 字段数量: {len(result.get('orders', []))}")
print("=" * 80)
