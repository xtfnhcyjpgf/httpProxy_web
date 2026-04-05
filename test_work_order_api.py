import requests
import json

BASE_URL = "http://127.0.0.1:5000"

test_data = {
    "orderid": "260403023790002",
    "contactName": "刘",
    "contactPhone": "13512335080",
    "createdDate": "2026-04-04T17:29:54.000Z",
    "appointmentStartTime": "2026-04-04T17:29:57.000Z",
    "appointmentEndTime": "2026-04-15T16:00:00.000Z",
    "completeTime": "2026-04-04T17:30:01.000Z",
    "evaluationTime": "2026-04-04T17:30:03.000Z",
    "expectedStartTime": "2026-04-04T17:30:05.000Z",
    "expectedEndTime": "2026-04-04T17:30:06.000Z",
    "outboundTime": "2026-04-04T17:30:08.000Z",
    "signInLocation": "签到定位",
    "operationRecords": [
        {"lastModifiedDate": "2026-04-04T17:30:15.000Z", "content": "111"},
        {"lastModifiedDate": "2026-04-30T16:00:00.000Z", "content": "222"}
    ],
    "products": [
        {"buyTime": "2026-04-23T16:00:00.000Z"},
        {"buyTime": "2026-04-24T16:00:00.000Z"}
    ],
    "completeFeedbackTime": "2026-04-09T16:00:00.000Z",
    "createdFeedbackTime": "2026-04-01T16:00:00.000Z",
    "inServiceFeedbackTime": "2026-05-07T16:00:00.000Z",
    "sendOrdersFeedbackTime": "2026-04-28T16:00:00.000Z",
    "settlementList": [
        {"fksj": "2026-04-04T17:30:37.000Z", "gmsj": "2026-04-04T17:30:39.000Z", "scazsj": "2026-04-04T17:30:40.000Z"}
    ],
    "attachmentGroups": [
        {
            "imgreplace": [
                {"annexName": "抽真空照片", "fileList": []},
                {"annexName": "安装服务确认书", "fileList": []}
            ]
        },
        {
            "imgreplace": [
                {"annexName": "内机上墙图", "fileList": []}
            ]
        }
    ],
    "completeFeedbackList": [
        {"createdDate": "2026-04-09T16:00:00.000Z"},
        {"createdDate": "2026-04-09T16:00:00.000Z"},
        {"createdDate": "2026-04-09T16:00:00.000Z"},
        {"createdDate": "2026-04-09T16:00:00.000Z"}
    ],
    "createdFeedbackList": [
        {"createdDate": "2026-04-01T16:00:00.000Z"}
    ],
    "inServiceFeedbackList": [
        {"createdDate": "2026-05-07T16:00:00.000Z"},
        {"createdDate": "2026-05-07T16:00:00.000Z"},
        {"createdDate": "2026-05-07T16:00:00.000Z"}
    ],
    "sendOrdersFeedbackList": [
        {"createdDate": "2026-04-28T16:00:00.000Z"},
        {"createdDate": "2026-04-28T16:00:00.000Z"},
        {"createdDate": "2026-04-28T16:00:00.000Z"}
    ]
}

def test_api():
    session = requests.Session()

    print("=== 工单接口测试 ===\n")

    # 1. 登录
    print("1. 登录...")
    r = session.post(f"{BASE_URL}/api/login", json={"username": "admin", "password": "admin123"})
    print(f"   状态码: {r.status_code}, 响应: {r.json()}")
    if not r.json().get("success"):
        print("   登录失败，测试终止")
        return
    print()

    # 2. 先查询并删除已存在的工单
    print("2. 清理已存在的工单...")
    r = session.get(f"{BASE_URL}/api/work-orders", params={"search": test_data["orderid"]})
    if r.json().get("success") and r.json().get("data"):
        for order in r.json().get("data", []):
            if order.get("orderid") == test_data["orderid"]:
                old_id = order.get("id")
                r2 = session.delete(f"{BASE_URL}/api/work-orders/{old_id}")
                print(f"   已删除旧工单ID: {old_id}, 状态: {r2.json()}")
    print()

    # 3. 创建工单
    print("3. 创建工单...")
    r = session.post(f"{BASE_URL}/api/work-orders", json=test_data)
    print(f"   状态码: {r.status_code}, 响应: {r.json()}")
    if not r.json().get("success"):
        print(f"   创建失败: {r.json().get('message')}")
        return
    work_order_id = r.json().get("data", {}).get("id")
    print(f"   工单ID: {work_order_id}")
    print()

    # 3. 获取工单详情
    print("3. 获取工单详情...")
    r = session.get(f"{BASE_URL}/api/work-orders/{work_order_id}")
    print(f"   状态码: {r.status_code}")
    if r.json().get("success"):
        data = r.json().get("data", {})
        print(f"   工单编号: {data.get('orderid')}")
        print(f"   联系人: {data.get('contactName')}, {data.get('contactPhone')}")
        print(f"   操作记录数: {len(data.get('operationRecords', []))}")
        print(f"   产品数: {len(data.get('products', []))}")
        print(f"   节点信息:")
        print(f"     - completeFeedbackList: {len(data.get('completeFeedbackList', []))}条")
        print(f"     - createdFeedbackList: {len(data.get('createdFeedbackList', []))}条")
        print(f"     - inServiceFeedbackList: {len(data.get('inServiceFeedbackList', []))}条")
        print(f"     - sendOrdersFeedbackList: {len(data.get('sendOrdersFeedbackList', []))}条")
        print(f"   结算记录数: {len(data.get('settlementList', []))}")
        print(f"   附件组数: {len(data.get('download', []))}")
        print(f"   完整数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"   响应: {r.json()}")
    print()

    print("=== 测试完成（未删除工单，方便检查）===")
    print(f"工单ID: {work_order_id}")

if __name__ == "__main__":
    test_api()
