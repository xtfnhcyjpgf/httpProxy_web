# 子信息阅读栏需求实施计划

## 1. 需求概述

在工单管理系统中增加"子信息阅读栏"功能，具体要求：

1. 在工单编辑界面增加子信息阅读栏，支持多行数据
2. 每行数据包括：
   - 子信息类型（serviceRequireTypeDesc）
   - 子信息内容（serviceRequireContent）
   - 操作时间（createdDate）
3. 不影响历史数据，使用独立的关联表存储
4. 支持第三方上传数据格式中的 `getServiceRequireByPage` 字段
5. 批量查询和单个查询接口返回数据时包含子信息阅读栏
6. 更新接口文档

## 2. 代码库研究结论

### 2.1 现有数据库结构
- 数据库使用SQLite，无外键设计
- 已有的工单相关表：
  - `work_orders`：工单主表
  - `work_order_details`：工单详情表
  - `work_order_feedbacks`：操作记录表
  - `work_order_products`：产品信息表
  - `work_order_nodes`：节点记录表
  - `work_order_settlements`：结算记录表
  - `work_order_attachments`：附件表
  - `system_config`：系统配置表

### 2.2 现有API结构
- 后端框架：Flask
- 前端框架：Vue 3 + Element Plus
- 主要API路由：
  - `GET /api/work-orders`：获取工单列表
  - `GET /api/work-orders/<id>`：获取工单详情
  - `POST /api/work-orders`：创建工单
  - `PUT /api/work-orders/<id>`：更新工单
  - `DELETE /api/work-orders/<id>`：删除工单
  - `POST /api/work-orders/upload-external`：第三方上传工单
  - `GET /api/work-orders/by-orderid/<orderid>`：按工单编号查询
  - `POST /api/work-orders/query`：批量查询工单

### 2.3 第三方上传数据格式分析
从 `第三方上传数据格式.json` 中可以看到：
- `getServiceRequireByPage` 是一个数组
- 格式为多行的 `{key, value, path, info}` 结构
- 每3个元素组成一行数据：
  - serviceRequireTypeDesc（子信息类型）
  - serviceRequireContent（子信息内容）
  - createdDate（操作时间）

### 2.4 现有工单编辑界面
- 文件：`frontend/src/views/WorkOrderForm.vue`
- 已有侧边栏导航：基本信息、详情信息、操作记录、产品信息、节点信息、结算信息、附件上传
- 表单数据使用Vue的reactive进行响应式管理

## 3. 实施步骤

### 3.1 数据库层修改

#### 步骤3.1.1：创建新的数据库表
在 `database.py` 的 `init_database()` 函数中添加 `work_order_service_requirements` 表：

```sql
CREATE TABLE IF NOT EXISTS work_order_service_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    work_order_id INTEGER NOT NULL,
    requirement_index INTEGER NOT NULL,
    service_require_type_desc TEXT DEFAULT '',
    service_require_content TEXT DEFAULT '',
    created_date TEXT DEFAULT ''
)
```

#### 步骤3.1.2：添加数据库操作函数
在 `database.py` 中添加以下函数：

1. `get_work_order_service_requirements(work_order_id)`：获取工单的子信息阅读栏数据
2. `create_work_order_service_requirements(work_order_id, requirements_list)`：创建子信息阅读栏数据
3. `update_work_order_service_requirements(work_order_id, requirements_list)`：更新子信息阅读栏数据
4. `delete_work_order_service_requirements(work_order_id)`：删除子信息阅读栏数据

### 3.2 后端API层修改

#### 步骤3.2.1：修改工单创建/更新逻辑
- 在 `create_work_order()` 和 `update_work_order()` 函数中添加对子信息阅读栏数据的处理
- 在 `create_work_order_from_upload()` 函数中添加对第三方上传格式中 `getServiceRequireByPage` 字段的解析

#### 步骤3.2.2：修改工单详情查询逻辑
- 在 `get_work_order_by_id()` 函数中添加子信息阅读栏数据的获取
- 在 `get_work_order_by_orderid()` 函数中添加子信息阅读栏数据的获取
- 在 `batch_query_work_orders()` 函数中添加子信息阅读栏数据的获取

#### 步骤3.2.3：修改API响应格式
- 在 `app.py` 中修改工单详情返回格式，添加 `getServiceRequireByPage` 字段
- 格式与第三方上传数据格式保持一致

### 3.3 前端界面修改

#### 步骤3.3.1：修改工单编辑表单
在 `WorkOrderForm.vue` 中：

1. 在侧边栏导航中添加"子信息阅读栏"菜单项
2. 在表单主体中添加子信息阅读栏的表单区域
3. 在 `formData` 中添加 `serviceRequirements` 数组
4. 添加"添加子信息"和"删除子信息"的按钮和函数
5. 在 `loadWorkOrderDetail()` 函数中加载子信息阅读栏数据
6. 在 `handleSubmit()` 函数中提交子信息阅读栏数据
7. 在 `resetForm()` 函数中重置子信息阅读栏数据

### 3.4 接口文档更新

#### 步骤3.4.1：更新API文档.md
在 `API文档.md` 中：

1. 更新数据结构说明，添加 `getServiceRequireByPage` 字段说明
2. 更新所有相关接口的请求和响应示例
3. 添加子信息阅读栏数据格式的详细说明

## 4. 需要修改的文件清单

| 文件路径 | 修改内容 |
|---------|---------|
| `database.py` | 创建新表、添加数据库操作函数、修改现有函数 |
| `app.py` | 修改API响应格式、处理子信息阅读栏数据 |
| `frontend/src/views/WorkOrderForm.vue` | 添加子信息阅读栏UI和逻辑 |
| `API文档.md` | 更新接口文档 |

## 5. 潜在风险和注意事项

### 5.1 数据兼容性
- 新表 `work_order_service_requirements` 独立存在，不影响现有数据
- 历史工单不会有子信息阅读栏数据，查询时返回空数组

### 5.2 数据格式一致性
- 确保第三方上传数据格式与API返回格式完全一致
- 确保前端提交格式与后端接收格式一致
- 字段名是 `getServiceRequireByPage`（不是 serviceRequireTypeDesc）

### 5.3 索引管理
- `requirement_index` 用于标识子信息的顺序，从0开始递增
- 更新时先删除旧数据再插入新数据，确保索引正确

### 5.4 性能考虑
- 子信息阅读栏数据量预计不大，当前实现方式足够
- 查询时使用 `work_order_id` 过滤，效率较高

## 6. 验收标准

1. 数据库成功创建 `work_order_service_requirements` 表
2. 工单编辑界面可以正常添加、编辑、删除子信息阅读栏数据
3. 第三方上传工单时可以正确解析 `getServiceRequireByPage` 字段
4. 按工单编号查询和批量查询接口可以正确返回子信息阅读栏数据（字段名为 `getServiceRequireByPage`）
5. 接口文档已更新，包含子信息阅读栏的说明
6. 历史工单不受影响，查询时返回空的子信息阅读栏数据
