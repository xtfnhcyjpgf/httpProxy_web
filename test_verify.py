import requests
import json

print("=" * 80)
print("验证上传数据")
print("=" * 80)

url = "http://127.0.0.1:5000/api/work-orders/by-orderid/260403023790099"

try:
    response = requests.get(url)
    result = response.json()

    if result.get("success"):
        data = result.get("data", {})
        print("✅ 工单数据查询成功！")
        print(f"\n工单编号: {data.get('orderid')}")

        print("\n--- 基本信息 ---")
        for item in data.get('searchWorkOrderListEs', []):
            print(f"  {item.get('key')}: {item.get('value')}")

        print("\n--- 详细信息 ---")
        for item in data.get('searchWorkOrderDetail', []):
            print(f"  {item.get('key')}: {item.get('value')}")

        print("\n--- 产品信息 ---")
        for item in data.get('getWorkOrderDetailList', []):
            print(f"  {item.get('key')}: {item.get('value')}")

        print("\n--- 节点记录 ---")
        for item in data.get('searchWorkOrderNodeResp', []):
            print(f"  {item.get('path')}: {item.get('value')}")

        print("\n--- 结算记录 ---")
        for item in data.get('searchAzWgmxDetail', []):
            print(f"  {item.get('key')}: {item.get('value')}")

        print("\n--- 附件 ---")
        for group in data.get('download', []):
            for img in group.get('imgreplace', []):
                print(f"  {img.get('annexName')}: {img.get('imageFilePath')}")

    else:
        print(f"❌ 查询失败: {result.get('message')}")

except Exception as e:
    print(f"❌ 发生异常: {e}")

print("=" * 80)
