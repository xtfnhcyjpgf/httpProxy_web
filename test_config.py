import requests
import json

print("=" * 80)
print("测试系统配置接口")
print("=" * 80)

base_url = "http://127.0.0.1:5000"

print("\n--- 测试1：获取系统配置（无需鉴权） ---")
try:
    response = requests.get(f"{base_url}/api/config/system")
    print(f"响应状态码: {response.status_code}")
    result = response.json()
    print(f"响应数据:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result.get("success"):
        print("✅ 获取配置成功")
        current_value = result.get("data", {}).get("enable_work_order")
        print(f"当前配置: enable_work_order = {current_value}")
except Exception as e:
    print(f"❌ 请求失败: {e}")

print("\n--- 测试2：尝试在无登录情况下设置配置（应该失败） ---")
try:
    response = requests.put(f"{base_url}/api/config/system", json={
        "enable_work_order": True
    })
    print(f"响应状态码: {response.status_code}")
    result = response.json()
    print(f"响应数据:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if not result.get("success") and response.status_code in [401, 302]:
        print("✅ 未登录时设置配置被正确拒绝")
except Exception as e:
    print(f"❌ 请求失败: {e}")

print("\n" + "=" * 80)
print("测试完成！")
print("=" * 80)
