import requests
import json

url = "http://127.0.0.1:5000/api/work-orders/query"
data = {
    "orderIds": ["260403023790001", "260403023790002", "260403023790003"]
}

print("=" * 80)
print("批量查询接口测试")
print("=" * 80)
print(f"请求URL: {url}")
print(f"请求参数: {json.dumps(data, indent=2, ensure_ascii=False)}")
print("-" * 80)

try:
    response = requests.post(url, json=data)
    print(f"响应状态码: {response.status_code}")
    print("-" * 80)
    
    result = response.json()
    print(f"响应数据:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("-" * 80)
    
    if result.get("success"):
        print("✅ 测试成功！")
        data_result = result.get("orders", [])
        print(f"查询到 {len(data_result)} 个工单")
        for order_data in data_result:
            orderid = order_data.get("orderid")
            print(f"  - 工单编号: {orderid}")
            download = order_data.get("download", [])
            if download:
                for idx, item in enumerate(download):
                    imgreplace = item.get("imgreplace", [])
                    if imgreplace:
                        print(f"    附件组 {idx+1}:")
                        for img_idx, img in enumerate(imgreplace):
                            print(f"      图片 {img_idx+1}:")
                            print(f"        annexName: {img.get('annexName')}")
                            print(f"        imageFilePath: {img.get('imageFilePath')}")
    else:
        print("❌ 测试失败！")
        print(f"错误信息: {result.get('message')}")
        
except Exception as e:
    print(f"❌ 发生异常: {e}")

print("=" * 80)
