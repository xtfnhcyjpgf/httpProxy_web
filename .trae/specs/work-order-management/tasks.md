# Tasks

## 任务清单

- [x] Task 1: 数据库设计和实现
  - [x] SubTask 1.1: 扩展 database.py 添加工单相关表
  - [x] SubTask 1.2: 创建工单表 (work_orders)
  - [x] SubTask 1.3: 创建工单详情表 (work_order_details)
  - [x] SubTask 1.4: 创建工单反馈表 (work_order_feedbacks)
  - [x] SubTask 1.5: 创建工单产品表 (work_order_products)
  - [x] SubTask 1.6: 创建工单节点表 (work_order_nodes)
  - [x] SubTask 1.7: 创建工单结算表 (work_order_settlements)
  - [x] SubTask 1.8: 创建工单附件表 (work_order_attachments)
  - [x] SubTask 1.9: 实现数据初始化脚本

- [x] Task 2: 后端API开发
  - [x] SubTask 2.1: 实现获取工单列表API (GET /api/work-orders)
  - [x] SubTask 2.2: 实现获取工单详情API (GET /api/work-orders/:id) - 返回order.txt格式
  - [x] SubTask 2.3: 实现创建工单API (POST /api/work-orders)
  - [x] SubTask 2.4: 实现更新工单API (PUT /api/work-orders/:id)
  - [x] SubTask 2.5: 实现删除工单API (DELETE /api/work-orders/:id)
  - [x] SubTask 2.6: 实现条件查询工单API (GET /api/work-orders/search)
  - [x] SubTask 2.7: 实现图片上传API (POST /api/work-orders/upload)
  - [x] SubTask 2.8: 实现批量查询工单API (POST /api/work-orders/query) - 返回order.txt格式
  - [x] SubTask 2.9: 实现数据组装函数 - 将多表数据组合成order.txt格式

- [x] Task 3: 前端页面开发（Vue.js 3 + Element Plus）
  - [x] SubTask 3.1: 创建工单列表页面 (WorkOrderList.vue)
  - [x] SubTask 3.2: 创建工单表单页面 (WorkOrderForm.vue) - 包含所有固定字段
  - [x] SubTask 3.3: 实现动态数组字段的添加/删除（操作记录、产品、结算单等）
  - [x] SubTask 3.4: 实现图片上传组件
  - [x] SubTask 3.5: 配置工单路由

- [x] Task 4: 系统集成
  - [x] SubTask 4.1: 更新Flask路由注册
  - [x] SubTask 4.2: 配置图片上传目录
  - [x] SubTask 4.3: 更新Layout侧边栏添加工单菜单

- [x] Task 5: 测试验证
  - [x] SubTask 5.1: 验证工单CRUD功能
  - [x] SubTask 5.2: 验证动态数组字段录入
  - [x] SubTask 5.3: 验证图片上传功能
  - [x] SubTask 5.4: 验证工单详情返回格式与order.txt一致

## 任务依赖关系

- Task 2 依赖 Task 1
- Task 3 依赖 Task 2 (API开发完成)
- Task 4 依赖 Task 2 和 Task 3
- Task 5 依赖 Task 4

## 工单表单字段说明

### 固定字段（searchWorkOrderListEs）
- contactName: 联系人姓名
- contactPhone: 联系人手机号
- createdDate: 创建时间
- appointBeginTime: 预约开始时间
- appointEndTime: 预约结束时间
- workOrderCompleteTime: 完工时间
- lastEvaluationTime: 评价时间

### 固定字段（searchWorkOrderDetail）
- evaluationTime: 评价时间
- appointBeginTime/EndTime: 预约开始/结束时间
- expectDoorToDoorBeginTime/EndTime: 期望上门时间
- deliveryTime: 出库时间
- signInLocation: 签到定位

### 动态数组字段
- workOrderFeedbackRespList: 操作记录（可添加多条）
- workOrderDetailProductInfoVOList: 产品购买时间（可添加多条）
- completeFeedbackList: 网点完工时间（自动创建4条相同）
- createdFeedbackList: 创建时间
- inServiceFeedbackList: 服务中时间（自动创建3条相同）
- sendOrdersFeedbackList: 派单时间（自动创建3条相同）
- azdMxSpgcList: 结算单操作时间（可添加多条）
- imgreplace: 图片附件（可添加多组，每组可添加多张）

## UI设计说明

### 工单列表页面
- 搜索栏：工单ID、联系人手机号搜索
- 表格：展示工单列表
- 操作：查看详情、编辑、删除

### 工单表单页面（单页面设计）
采用分Section区域布局，所有数据在同一页面录入：

**Section 1: 基本信息**
- 工单编号（orderid）
- 联系人姓名、联系人手机号
- 创建时间、预约开始时间、预约结束时间
- 完工时间、评价时间

**Section 2: 详情信息**
- 评价时间、期望上门开始/结束时间
- 出库时间、签到定位

**Section 3: 操作记录（动态表格）**
- 操作记录时间、操作内容
- 点击"添加操作记录"按钮新增一行

**Section 4: 产品信息（动态表格）**
- 产品购买时间
- 点击"添加产品"按钮新增一行

**Section 5: 节点信息（网点完工、服务中、派单）**
- 网点完工时间（自动创建4条）
- 创建时间
- 服务中时间（自动创建3条）
- 派单时间（自动创建3条）

**Section 6: 结算信息（动态表格）**
- 操作时间、购买时间、安装时间
- 点击"添加结算记录"按钮新增一行

**Section 7: 附件上传（分组多图片）**
- 附件组1: 内机条码图、抽真空图、外机条码图、内机上墙图
- 附件组2: ...
- 点击"添加附件组"按钮新增一组
- 每组内可添加多张图片

布局方式：
- 左侧可折叠的目录导航（类似Element Plus Anchor）
- 右侧为表单主体区域
- 每个Section之间可滚动定位
- 底部固定"保存"和"取消"按钮
