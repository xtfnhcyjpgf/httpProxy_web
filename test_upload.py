import requests
import json
import os

url = "http://127.0.0.1:5000/api/work-orders/upload-external"

json_file = os.path.join(os.path.dirname(__file__), 'frontend', '第三方上传数据格式.json')

print("=" * 80)
print("第三方上传接口测试")
print("=" * 80)
print(f"请求URL: {url}")
print(f"测试数据文件: {json_file}")
print("-" * 80)

try:
    with open(json_file, 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    print(f"工单编号: {test_data.get('orderid')}")
    print("-" * 80)

    response = requests.post(url, json=test_data)
    print(f"响应状态码: {response.status_code}")
    print("-" * 80)

    result = response.json()
    print(f"响应数据:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("-" * 80)

    if result.get("success"):
        print("✅ 上传成功！")
        print(f"创建结果: {result.get('data')}")
        print(f"消息: {result.get('message')}")

        print("\n" + "=" * 80)
        print("验证查询")
        print("=" * 80)
        verify_url = f"http://127.0.0.1:5000/api/work-orders/by-orderid/{test_data.get('orderid')}"
        verify_response = requests.get(verify_url)
        verify_result = verify_response.json()

        if verify_result.get("success"):
            data = verify_result.get("data", {})
            print(f"\n工单编号: {data.get('orderid')}")

            print("\n--- 基本信息 ---")
            for item in data.get('searchWorkOrderListEs', []):
                print(f"  {item.get('key')}: {item.get('value')}")

            print("\n--- 详细信息 ---")
            for item in data.get('searchWorkOrderDetail', []):
                if item.get('key') in ['evaluationTime', 'appointBeginTime', 'appointEndTime', 'expectDoorToDoorBeginTime', 'expectDoorToDoorEndTime', 'deliveryTime', 'signInLocation']:
                    print(f"  {item.get('key')}: {item.get('value')}")

            print("\n--- 操作记录 ---")
            for item in data.get('searchWorkOrderDetail', []):
                if item.get('key') in ['lastModifiedDate', 'content']:
                    print(f"  {item.get('key')}: {item.get('value')}")

            print("\n--- 产品信息 ---")
            for item in data.get('getWorkOrderDetailList', []):
                print(f"  {item.get('key')}: {item.get('value')}")

            print("\n--- 结算记录 ---")
            for item in data.get('searchAzWgmxDetail', []):
                print(f"  {item.get('key')}: {item.get('value')}")

            print("\n--- 附件 ---")
            for group in data.get('download', []):
                for img in group.get('imgreplace', []):
                    print(f"  {img.get('annexName')}: {img.get('imageFilePath')}")
        else:
            print(f"❌ 查询失败: {verify_result.get('message')}")

    else:
        print("❌ 上传失败！")
        print(f"错误信息: {result.get('message')}")

except FileNotFoundError:
    print(f"❌ 错误：找不到测试数据文件: {json_file}")
except Exception as e:
    print(f"❌ 发生异常: {e}")

print("=" * 80)
