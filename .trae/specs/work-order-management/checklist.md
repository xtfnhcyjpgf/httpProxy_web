# Checklist

## 开发检查清单

### 数据库
- [x] work_orders表字段完整（包含所有固定字段）
- [x] work_order_details表字段完整
- [x] work_order_feedbacks表支持动态索引
- [x] work_order_products表支持动态索引
- [x] work_order_nodes表支持多种节点类型
- [x] work_order_settlements表支持动态索引
- [x] work_order_attachments表支持多组多附件
- [x] 无外键约束（遵循规格要求）

### 后端API
- [x] GET /api/work-orders 返回工单列表
- [x] GET /api/work-orders/:id 返回order.txt格式详情
- [x] POST /api/work-orders 正确创建工单及关联数据
- [x] PUT /api/work-orders/:id 正确更新工单
- [x] DELETE /api/work-orders/:id 正确删除（含关联数据和图片文件）
- [x] GET /api/work-orders/search 支持条件查询
- [x] POST /api/work-orders/upload 支持图片上传
- [x] POST /api/work-orders/query 批量查询返回order.txt格式
- [x] 会话验证中间件保护所有工单API

### 批量查询API
- [x] 接受orderids数组参数
- [x] 返回数组按orderid从小到大排序
- [x] 动态数组按索引从小到大排序
- [x] 格式与order.txt完全一致

### 前端页面

#### 工单列表页 (WorkOrderList.vue)
- [x] 搜索栏支持工单ID、手机号查询
- [x] 表格展示工单列表
- [x] 操作列：查看、编辑、删除按钮

#### 工单表单页 (WorkOrderForm.vue)
- [x] 单页面设计，所有数据在同一界面录入
- [x] 基本信息Section：orderid、联系人、时间等固定字段
- [x] 详情信息Section：评价时间、期望上门时间等
- [x] 操作记录：动态添加/删除操作记录行
- [x] 产品信息：动态添加/删除产品行
- [x] 节点信息：网点完工（4条）、创建（1条）、服务中（3条）、派单（3条）
- [x] 结算信息：动态添加/删除结算记录
- [x] 附件上传：支持多组多图片上传
- [x] 左侧目录导航，右侧表单主体
- [x] 底部固定保存/取消按钮
- [x] 保存成功后正确跳转

### 图片处理
- [x] 图片上传到服务器本地uploads目录
- [x] 图片路径正确存储到数据库
- [x] 删除工单时图片文件一并删除

### 格式一致性
- [x] 工单详情API返回格式与order.txt一致
- [x] 动态数组索引正确递增
- [x] 特殊节点类型自动创建多条记录

### 安全
- [x] 工单API有会话验证
- [x] 无硬编码配置信息
