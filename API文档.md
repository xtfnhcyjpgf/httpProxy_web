# 工单查询API接口文档

## 概述
本文档描述了工单管理系统的对外查询接口，所有接口均返回 order.txt 格式的 JSON 数据。

---

## 接口列表

### 1. 按工单编号查询详情
**接口地址：** `GET /api/work-orders/by-orderid/<orderid>`

**功能描述：** 根据工单编号（orderid）查询单个工单的完整详情信息。

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| orderid | String | 是 | 工单编号 |

**请求示例：**
```http
GET /api/work-orders/by-orderid/260403023790002
```

**响应格式：**
```json
{
  "success": true,
  "data": {
    "orderid": "工单编号",
    "searchWorkOrderListEs": [...],
    "searchWorkOrderDetail": [...],
    "getWorkOrderDetailList": [...],
    "searchWorkOrderNodeResp": [...],
    "searchAzWgmxDetail": [...],
    "download": [...]
  },
  "message": ""
}
```

**错误响应：**
| HTTP状态码 | 说明 |
|------------|------|
| 404 | 工单不存在 |

---

### 2. 批量查询工单（按工单号）
**接口地址：** `POST /api/work-orders/query`

**功能描述：** 支持按工单号批量查询多个工单，返回 order.txt 格式的数据数组。

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| orderIds | Array | 是 | 工单编号数组 |

**请求示例：**
```http
POST /api/work-orders/query
Content-Type: application/json

{
  "orderIds": ["260403023790001", "260403023790002", "260403023790003"]
}
```

**响应格式：**
```json
{
  "success": true,
  "orders": [
    {
      "orderid": "260403023790001",
      "searchWorkOrderListEs": [...],
      "searchWorkOrderDetail": [...],
      "getWorkOrderDetailList": [...],
      "searchWorkOrderNodeResp": [...],
      "searchAzWgmxDetail": [...],
      "download": [...]
    },
    {
      "orderid": "260403023790002",
      ...
    }
  ],
  "all_url": [
    {"key": "searchWorkOrderListEs", "Method": "POST", "url": "https://sms.gree.com/api/sso/sms-server-order/api/workOrderSearch/searchWorkOrderListEs", "info": "查询工单列表"},
    {"key": "searchWorkOrderDetail", "Method": "GET", "url": "https://sms.gree.com/api/sso/sms-server-order/api/workOrderSearch/searchWorkOrderDetail", "info": "查询工单详情"},
    {"key": "getWorkOrderDetailList", "Method": "POST", "url": "https://sms.gree.com/api/sso/sms-server-order/api/workOrderSearch/getWorkOrderDetailList", "info": "查询工单详情列表详情"},
    {"key": "searchWorkOrderNodeResp", "Method": "GET", "url": "https://sms.gree.com/api/sso/sms-server-order/api/workOrderSearch/searchWorkOrderNodeResp", "info": "查询工单节点详情"},
    {"key": "searchAzWgmxDetail", "Method": "POST", "url": "https://sms.gree.com/api/sso/autoapp-default-server-installaccounts/mvp/azwgmx/searchAzWgmxDetail", "info": "查询工单详情列表"},
    {"key": "download", "Method": "GET", "url": "https://sms.gree.com/api/pub/nts-foundation-attachmentmanager/api/v2/attachment/download", "info": "下载图片"}
  ],
  "message": ""
}
```

**错误响应：**
| HTTP状态码 | 说明 |
|------------|------|
| 400 | 请求数据无效，缺少 orderIds 数组 |

---

### 3. 第三方上传工单
**接口地址：** `POST /api/work-orders/upload-external`

**功能描述：** 供第三方系统上传工单数据，数据格式与 order.txt 格式一致。上传成功后可使用查询接口验证数据。

**请求参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| orderid | String | 是 | 工单编号 |
| searchWorkOrderListEs | Array | 是 | 基本信息数组 |
| searchWorkOrderDetail | Array | 否 | 详细信息数组（含操作记录） |
| getWorkOrderDetailList | Array | 否 | 产品信息数组 |
| searchWorkOrderNodeResp | Array | 否 | 节点记录数组 |
| searchAzWgmxDetail | Array | 否 | 结算记录数组 |
| download | Array | 否 | 附件数组 |

**请求示例：**
```http
POST /api/work-orders/upload-external
Content-Type: application/json

{
  "orderid": "260403023790099",
  "searchWorkOrderListEs": [
    {"key": "newOrderid", "value": "260403023799999", "path": "data", "info": "新工单编号"},
    {"key": "contactName", "value": "张三", "path": "data", "info": "联系人姓名"},
    {"key": "contactPhone", "value": "13800138000", "path": "data", "info": "联系人手机号"}
  ],
  "searchWorkOrderDetail": [
    {"key": "lastModifiedDate", "value": "2026-04-29T16:00:00.000Z", "path": "data.workOrderFeedbackRespList[0]", "info": "操作记录时间1"},
    {"key": "content", "value": "签到定位", "path": "data.workOrderFeedbackRespList[0]", "info": "操作内容1"}
  ],
  "download": [
    {
      "imgreplace": [
        {"annexName": "外机条码图", "imageFilePath": "http://example.com/image.png"}
      ]
    }
  ]
}
```

**响应格式：**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "orderid": "260403023790099"
  },
  "message": "工单创建成功"
}
```

**错误响应：**
| HTTP状态码 | 说明 |
|------------|------|
| 400 | 请求数据无效或工单编号为空 |
| 409 | 工单编号已存在 |
| 500 | 创建工单失败 |

---

## 数据结构说明

### order.txt 格式结构

```json
{
  "orderid": "工单编号",
  "searchWorkOrderListEs": [
    {
      "key": "newOrderid",
      "value": "新工单编号",
      "path": "data",
      "info": "新工单编号"
    },
    {
      "key": "contactName",
      "value": "联系人姓名",
      "path": "data",
      "info": "联系人姓名"
    },
    {
      "key": "contactPhone",
      "value": "联系人手机号",
      "path": "data",
      "info": "联系人手机号"
    }
  ],
  "searchWorkOrderDetail": [
    {
      "key": "lastModifiedDate",
      "value": "操作记录时间",
      "path": "data.workOrderFeedbackRespList[0]",
      "info": "操作记录时间1"
    },
    {
      "key": "content",
      "value": "操作内容",
      "path": "data.workOrderFeedbackRespList[0]",
      "info": "操作内容1"
    }
  ],
  "getWorkOrderDetailList": [
    {
      "key": "buyTime",
      "value": "产品购买时间",
      "path": "data.workOrderDetailProductInfoVOList[0]",
      "info": "产品1购买时间"
    }
  ],
  "searchWorkOrderNodeResp": [
    {
      "key": "createdDate",
      "value": "创建时间",
      "path": "data.createdFeedbackList[0]",
      "info": "创建时间"
    }
  ],
  "searchAzWgmxDetail": [
    {
      "key": "fksj",
      "value": "操作时间",
      "path": "data.azdMxSpgcList[0]",
      "info": "结算单查询-操作时间1"
    },
    {
      "key": "gmsj",
      "value": "购买时间",
      "path": "data",
      "info": "结算单查询-购买时间"
    },
    {
      "key": "scazsj",
      "value": "安装时间",
      "path": "data",
      "info": "结算单查询-安装时间"
    }
  ],
  "download": [
    {
      "imgreplace": [
        {
          "annexName": "附件名称",
          "imageFilePath": "http://127.0.0.1:5000/api/work-orders/uploads/abc123.jpg"
        }
      ]
    }
  ]
}
```

---

## 公共响应格式

### 成功响应
```json
{
  "success": true,
  "data": {...},
  "message": ""
}
```

### 失败响应
```json
{
  "success": false,
  "data": null,
  "message": "错误信息"
}
```

---

## 注意事项

1. **批量查询接口**：如果某个工单号不存在，返回结果中会忽略该工单
2. **上传接口**：工单号重复时返回409错误
3. **图片访问**：附件中的 `imageFilePath` 字段返回完整的HTTP访问地址（如：`http://127.0.0.1:5000/api/work-orders/uploads/abc123.jpg`），可直接在浏览器中访问
4. **时间格式**：所有时间字段均采用 ISO 8601 格式（如：`2026-04-04T17:43:50.000Z`）

---

## 示例代码（Python）

### 按工单编号查询示例
```python
import requests

orderid = "260403023790002"
url = f"http://127.0.0.1:5000/api/work-orders/by-orderid/{orderid}"

response = requests.get(url)
result = response.json()

if result["success"]:
    print(result["data"])
else:
    print("查询失败:", result["message"])
```

### 批量查询示例
```python
import requests

url = "http://127.0.0.1:5000/api/work-orders/query"
data = {
    "orderIds": ["260403023790001", "260403023790002"]
}

response = requests.post(url, json=data)
result = response.json()

if result["success"]:
    for order_data in result["orders"]:
        print(f"工单 {order_data['orderid']}:")
        print(order_data)
else:
    print("查询失败:", result["message"])
```

### 第三方上传工单示例
```python
import requests

url = "http://127.0.0.1:5000/api/work-orders/upload-external"
data = {
    "orderid": "260403023790099",
    "searchWorkOrderListEs": [
        {"key": "newOrderid", "value": "260403023799999", "path": "data", "info": "新工单编号"},
        {"key": "contactName", "value": "张三", "path": "data", "info": "联系人姓名"},
        {"key": "contactPhone", "value": "13800138000", "path": "data", "info": "联系人手机号"}
    ],
    "searchWorkOrderDetail": [
        {"key": "lastModifiedDate", "value": "2026-04-29T16:00:00.000Z", "path": "data.workOrderFeedbackRespList[0]", "info": "操作记录时间1"},
        {"key": "content", "value": "签到定位", "path": "data.workOrderFeedbackRespList[0]", "info": "操作内容1"}
    ],
    "download": [
        {
            "imgreplace": [
                {"annexName": "外机条码图", "imageFilePath": "http://example.com/image.png"}
            ]
        }
    ]
}

response = requests.post(url, json=data)
result = response.json()

if result["success"]:
    print("上传成功！工单ID:", result["data"]["id"])
else:
    print("上传失败:", result["message"])
```
