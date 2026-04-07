import requests
import json

print("=" * 80)
print("测试查询工单编号和新工单编号接口")
print("=" * 80)

base_url = "http://127.0.0.1:5000"

print("\n--- 测试：获取有新工单编号的工单列表 ---")
try:
    response = requests.get(f"{base_url}/api/work-orders/new-orderids")
    print(f"响应状态码: {response.status_code}")
    result = response.json()
    print(f"响应数据:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result.get("success"):
        print("✅ 查询成功")
        data = result.get("data", [])
        print(f"查询到 {len(data)} 个工单")
        for i, order in enumerate(data, 1):
            print(f"  {i}. 工单编号: {order.get('orderid')}, 新工单编号: {order.get('neworderid')}")
    else:
        print("❌ 查询失败")
except Exception as e:
    print(f"❌ 请求失败: {e}")

print("\n" + "=" * 80)
print("测试完成！")
print("=" * 80)
