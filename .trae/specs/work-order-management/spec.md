# 工单管理模块 Spec

## Why
需要开发一个工单管理模块，用于录入、查询和管理工单数据。录入的数据供后期API查询使用，查询返回格式需与 order.txt 中的 JSON 结构一致。

## What Changes
- 新增工单管理功能模块到现有Web管理系统
- 工单数据以 order.txt 中的 JSON 格式存储
- 支持完整的 CRUD 操作（创建、读取、更新、删除）
- 图片文件存储在服务器本地目录
- 后期可通过API按 order.txt 格式返回工单数据

## Impact
- 新增系统能力：工单数据管理
- 涉及代码：后端API、前端页面、数据库模型
- 新增数据库表：工单表(work_orders)、工单详情表(work_order_details)、工单反馈表(work_order_feedbacks)、工单产品表(work_order_products)、工单附件表(work_order_attachments)

## 技术方案

### 数据存储策略
工单数据拆分为多表存储以支持动态数组，但通过视图或API组合成 order.txt 格式：

| order.txt 中的 path | 存储表 | 说明 |
|---------------------|--------|------|
| data | work_orders | 工单主表 |
| data.workOrderResp | work_order_details | 工单详情 |
| data.workOrderEvaluationRespList | work_order_evaluations | 评价列表 |
| data.workOrderFeedbackRespList | work_order_feedbacks | 反馈列表（动态） |
| data.workOrderDetailProductInfoVOList | work_order_products | 产品列表（动态） |
| data.completeFeedbackList | work_order_nodes | 网点完工记录 |
| data.createdFeedbackList | work_order_nodes | 创建记录 |
| data.inServiceFeedbackList | work_order_nodes | 服务中记录 |
| data.sendOrdersFeedbackList | work_order_nodes | 派单记录 |
| data.azdMxSpgcList | work_order_settlements | 结算单记录 |
| imgreplace | work_order_attachments | 附件表（图片） |

### 固定字段 vs 动态字段
- **固定字段**：直接在表中创建对应列（如 contactName, contactPhone）
- **动态数组字段**：创建关联表，通过外键关联工单ID

### 图片存储
- 图片存储在服务器本地 `uploads/` 目录
- 数据库中只存储图片路径

## ADDED Requirements

### Requirement: 工单列表查看
系统 SHALL 提供工单列表页面，展示所有已录入的工单。

#### Scenario: 查看工单列表
- **WHEN** 用户访问工单管理页面
- **THEN** 系统展示工单列表，包含工单ID、联系人、创建时间等关键信息

### Requirement: 工单录入
系统 SHALL 提供工单录入功能，用户按 order.txt 格式录入工单数据。

#### Scenario: 单页面录入
- **WHEN** 用户打开工单录入页面
- **THEN** 系统显示单页面表单，包含所有数据区域（基本信息、详情、操作记录、产品、节点、结算、附件）
- **AND** 左侧显示目录导航，点击可滚动到对应区域
- **AND** 底部固定保存/取消按钮

#### Scenario: 录入固定字段
- **WHEN** 用户录入 contactName、contactPhone 等固定字段
- **THEN** 系统将数据存入 work_orders 表对应字段

#### Scenario: 录入动态数组字段
- **WHEN** 用户添加多条操作记录（workOrderFeedbackRespList）
- **THEN** 系统为每条记录在 work_order_feedbacks 表中创建一行，索引自动递增

#### Scenario: 录入图片附件
- **WHEN** 用户上传图片并填写附件名称
- **THEN** 图片保存到服务器本地，路径存入 work_order_attachments 表

### Requirement: 工单详情查看
系统 SHALL 提供工单详情页面，按 order.txt 格式展示完整工单数据。

#### Scenario: 查看工单详情
- **WHEN** 用户点击工单查看详情
- **THEN** 系统以 order.txt 中的 JSON 结构展示所有数据

### Requirement: 工单编辑
系统 SHALL 提供工单编辑功能，用户可修改工单数据。

### Requirement: 工单删除
系统 SHALL 提供工单删除功能，用户可删除工单及相关数据。

#### Scenario: 删除工单
- **WHEN** 用户删除工单
- **THEN** 系统删除工单主表及所有关联表数据（包括图片文件）

### Requirement: 工单查询
系统 SHALL 提供工单查询功能，用户可按条件搜索工单。

#### Scenario: 按条件查询
- **WHEN** 用户输入查询条件（如工单ID、联系人手机号）
- **THEN** 系统返回符合条件的工单列表

### Requirement: 工单批量查询API
系统 SHALL 提供工单批量查询API，供外部系统调用。

#### Scenario: 批量查询工单
- **WHEN** 调用方传入多个工单编号数组
- **THEN** 系统返回工单数组，格式与 order.txt 完全一致，数组中的索引按从小到大排序
- **AND** 如果某个工单不存在，该工单编号的返回数据为空对象或null
- **AND** 所有动态数组按索引从小到大排序

#### Scenario: 外部API调用
- **WHEN** 外部系统调用 POST /api/work-orders/query
- **THEN** 系统验证请求格式，返回符合 order.txt 格式的 JSON 数据

## MODIFIED Requirements

无

## REMOVED Requirements

无

## 数据库设计

### 工单主表 (work_orders)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 工单ID |
| orderid | TEXT UNIQUE | 工单订单号 |
| contact_name | TEXT | 联系人姓名 |
| contact_phone | TEXT | 联系人手机号 |
| created_date | TEXT | 创建时间 |
| appoint_begin_time | TEXT | 预约开始时间 |
| appoint_end_time | TEXT | 预约结束时间 |
| work_order_complete_time | TEXT | 完工时间 |
| last_evaluation_time | TEXT | 评价时间 |
| created_at | TIMESTAMP | 记录创建时间 |

### 工单详情表 (work_order_details)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 详情ID |
| work_order_id | INTEGER | 关联工单ID |
| evaluation_time | TEXT | 评价时间 |
| expect_door_to_door_begin_time | TEXT | 期望上门开始时间 |
| expect_door_to_door_end_time | TEXT | 期望上门结束时间 |
| delivery_time | TEXT | 出库时间 |
| sign_in_location | TEXT | 签到定位 |

### 工单反馈表 (work_order_feedbacks)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 反馈ID |
| work_order_id | INTEGER | 关联工单ID |
| feedback_index | INTEGER | 数组索引 |
| last_modified_date | TEXT | 操作记录时间 |
| content | TEXT | 操作内容 |

### 工单产品表 (work_order_products)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 产品ID |
| work_order_id | INTEGER | 关联工单ID |
| product_index | INTEGER | 数组索引 |
| buy_time | TEXT | 购买时间 |

### 工单节点表 (work_order_nodes)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 节点ID |
| work_order_id | INTEGER | 关联工单ID |
| node_type | TEXT | 节点类型(complete/created/inService/sendOrders) |
| node_index | INTEGER | 数组索引 |
| created_date | TEXT | 时间 |

### 工单结算表 (work_order_settlements)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 结算ID |
| work_order_id | INTEGER | 关联工单ID |
| settlement_index | INTEGER | 数组索引 |
| fksj | TEXT | 操作时间 |
| gmsj | TEXT | 购买时间 |
| scazsj | TEXT | 安装时间 |

### 工单附件表 (work_order_attachments)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PRIMARY KEY | 附件ID |
| work_order_id | INTEGER | 关联工单ID |
| attachment_group | INTEGER | 附件组索引 |
| annex_name | TEXT | 附件名称 |
| image_file_path | TEXT | 图片路径 |

## API设计

### 工单管理API
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/work-orders | 获取工单列表 |
| GET | /api/work-orders/:id | 获取工单详情(order.txt格式) |
| POST | /api/work-orders | 创建工单 |
| PUT | /api/work-orders/:id | 更新工单 |
| DELETE | /api/work-orders/:id | 删除工单 |
| GET | /api/work-orders/search | 条件查询工单 |
| POST | /api/work-orders/query | 批量查询工单（外部API，返回order.txt格式） |

### 批量查询API详细规范
**POST /api/work-orders/query**

请求体：
```json
{
  "orderids": ["工单编号1", "工单编号2", "工单编号3"]
}
```

响应体（与order.txt格式完全一致）：
```json
[
  {
    "orderid": "工单编号1",
    "searchWorkOrderListEs": [...],
    "searchWorkOrderDetail": [...],
    "getWorkOrderDetailList": [...],
    "searchWorkOrderNodeResp": [...],
    "searchAzWgmxDetail": [...],
    "download": [...]
  },
  {
    "orderid": "工单编号2",
    "searchWorkOrderListEs": [...],
    ...
  }
]
```

返回规则：
- 工单按orderid从小到大排序返回
- 动态数组（workOrderFeedbackRespList等）按索引从小到大排序
- 如果工单不存在，返回空对象 `{}` 或从数组中省略

## 项目结构
```
httpProxy_web/
├── app.py                  # Flask应用入口
├── config.py               # 配置文件
├── database.py             # 数据库模块
├── requirements.txt        # Python依赖
├── frontend/               # 前端项目
│   └── src/
│       └── views/
│           ├── WorkOrderList.vue   # 工单列表页
│           └── WorkOrderForm.vue   # 工单录入/编辑页
├── uploads/                # 图片上传目录
└── work_order.db          # SQLite数据库
```
