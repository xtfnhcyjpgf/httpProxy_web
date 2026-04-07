import requests
import json

print("=" * 80)
print("测试查询工单编号和新工单编号接口")
print("=" * 80)

base_url = "http://127.0.0.1:5000"

print("\n--- 测试：获取当前配置 ---")
try:
    response = requests.get(f"{base_url}/api/config/system")
    result = response.json()
    if result.get("success"):
        enable_work_order = result.get("data", {}).get("enable_work_order")
        print(f"当前配置: enable_work_order = {enable_work_order}")
    else:
        print("获取配置失败")
except Exception as e:
    print(f"❌ 获取配置失败: {e}")

print("\n--- 测试：查询工单编号和新工单编号 ---")
try:
    response = requests.get(f"{base_url}/api/work-orders/new-orderids")
    print(f"响应状态码: {response.status_code}")
    result = response.json()
    print(f"响应数据:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result.get("success"):
        print("✅ 查询成功")
        data = result.get("data", [])
        print(f"返回 {len(data)} 条数据")
        
        enable_work_order = None
        try:
            config_resp = requests.get(f"{base_url}/api/config/system")
            config_result = config_resp.json()
            if config_result.get("success"):
                enable_work_order = config_result.get("data", {}).get("enable_work_order")
        except:
            pass
        
        if enable_work_order is False or enable_work_order is None:
            if len(data) == 0:
                print("✅ 禁用时返回空数组，符合预期")
            else:
                print(f"❌ 禁用时返回了 {len(data)} 条数据，不符合预期")
        
        for i, order in enumerate(data, 1):
            print(f"  {i}. 工单编号: {order.get('orderid')}, 新工单编号: {order.get('neworderid')}")
    else:
        print("❌ 查询失败")
except Exception as e:
    print(f"❌ 请求失败: {e}")

print("\n" + "=" * 80)
print("测试完成！")
print("=" * 80)
print("\n说明：")
print("- 如果 enable_work_order = false，应该返回空数组")
print("- 如果 enable_work_order = true，应该返回有新工单编号的数据")
print("- 请在首页手动切换开关来测试两种情况")
