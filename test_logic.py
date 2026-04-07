import requests
import json

print("=" * 80)
print("测试禁用时返回空数组的逻辑")
print("=" * 80)

base_url = "http://127.0.0.1:5000"

print("\n当前配置:")
try:
    response = requests.get(f"{base_url}/api/config/system")
    result = response.json()
    if result.get("success"):
        print(f"enable_work_order = {result.get('data', {}).get('enable_work_order')}")
    else:
        print("获取配置失败")
except Exception as e:
    print(f"❌ 获取配置失败: {e}")

print("\n测试查询:")
try:
    response = requests.get(f"{base_url}/api/work-orders/new-orderids")
    result = response.json()
    print(f"响应: {json.dumps(result, ensure_ascii=False)}")
    
    data = result.get("data", [])
    print(f"\n返回数据数量: {len(data)}")
    
    print("\n✅ 接口逻辑说明:")
    print("- 如果 enable_work_order = true: 返回有新工单编号的数据")
    print("- 如果 enable_work_order = false: 返回空数组 []")
    
except Exception as e:
    print(f"❌ 请求失败: {e}")

print("\n" + "=" * 80)
