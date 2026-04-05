# Tasks

## 任务清单

- [x] Task 1: 项目初始化和环境配置
  - [x] SubTask 1.1: 创建项目目录结构
  - [x] SubTask 1.2: 创建 requirements.txt（Flask、bcrypt等Python依赖）
  - [x] SubTask 1.3: 创建 config.py 配置文件
  - [x] SubTask 1.4: 初始化Vue.js前端项目（package.json、vite.config.js）

- [x] Task 2: 数据库设计和实现
  - [x] SubTask 2.1: 创建数据库模型 (users表，无外键)
  - [x] SubTask 2.2: 实现数据库初始化脚本（含初始账号admin/admin123）

- [x] Task 3: 后端API开发
  - [x] SubTask 3.1: 实现用户登录API (POST /api/login)
  - [x] SubTask 3.2: 实现用户退出API (POST /api/logout)
  - [x] SubTask 3.3: 实现账号列表API (GET /api/accounts)
  - [x] SubTask 3.4: 实现添加账号API (POST /api/accounts)
  - [x] SubTask 3.5: 实现修改密码API (PUT /api/accounts/:id/password)
  - [x] SubTask 3.6: 实现删除账号API (DELETE /api/accounts/:id)
  - [x] SubTask 3.7: 实现会话验证中间件

- [x] Task 4: 前端页面开发（Vue.js 3 + Element Plus）
  - [x] SubTask 4.1: 创建登录页面 (Login.vue)，使用Element Plus表单组件
  - [x] SubTask 4.2: 创建管理主页框架 (Index.vue)，使用Element Plus布局容器
  - [x] SubTask 4.3: 创建账号管理页面 (Account.vue)，使用Element Plus表格和对话框
  - [x] SubTask 4.4: 创建布局组件 (Layout.vue)，包含侧边栏和顶部导航
  - [x] SubTask 4.5: 配置Vue Router路由
  - [x] SubTask 4.6: 封装API调用模块 (api/index.js)
  - [x] SubTask 4.7: 实现认证状态管理 (stores/auth.js)

- [x] Task 5: Flask应用整合
  - [x] SubTask 5.1: 创建Flask应用入口 (app.py)
  - [x] SubTask 5.2: 配置CORS跨域支持
  - [x] SubTask 5.3: 配置会话管理（Flask session + cookie）
  - [x] SubTask 5.4: 配置静态文件serve（dist目录）

- [x] Task 6: 接口测试
  - [x] SubTask 6.1: 编写登录接口测试用例（正确账号、错误账号）
  - [x] SubTask 6.2: 编写账号管理接口测试用例（列表、添加、修改、删除）
  - [x] SubTask 6.3: 编写会话验证接口测试用例（未登录访问）
  - [x] SubTask 6.4: 运行测试并验证所有用例通过

- [x] Task 7: 前端构建和部署验证
  - [x] SubTask 7.1: 前端构建测试（npm run build）
  - [x] SubTask 7.2: 验证Flask serve静态文件
  - [x] SubTask 7.3: 整体功能验证

## 任务依赖关系

- Task 3 依赖 Task 1 和 Task 2
- Task 4 依赖 Task 3 (API开发完成)
- Task 5 依赖 Task 3 和 Task 4
- Task 6 依赖 Task 3 和 Task 5
- Task 7 依赖 Task 5

## UI设计说明（Element Plus）

### 登录页面
- 居中卡片式登录框
- 输入框：用户名、密码（el-input）
- 按钮：登录（el-button type="primary"）
- 错误提示：el-alert

### 管理主页
- 左侧固定侧边栏（el-menu）
  - LOGO区域
  - 首页
  - 账号管理
- 右侧主内容区（el-main）
  - 顶部欢迎信息

### 账号管理页面
- 顶部操作栏
  - 添加账号按钮（el-button type="primary"）
- 数据表格（el-table）
  - 列：ID、用户名、创建时间、操作
  - 操作：修改密码、删除
- 添加/修改密码对话框（el-dialog）
  - 表单：用户名/密码输入框

## 接口测试用例

### 登录接口 (POST /api/login)
| 用例 | 输入 | 预期结果 |
|------|------|----------|
| 正常登录 | admin/admin123 | 返回200，session包含user_id |
| 错误密码 | admin/wrongpass | 返回401，错误提示 |
| 用户不存在 | unknown/anypass | 返回401，错误提示 |

### 账号管理接口
| 用例 | 输入 | 预期结果 |
|------|------|----------|
| 获取列表 | GET /api/accounts | 返回200，账号列表数组 |
| 添加账号 | POST /api/accounts | 返回201，新账号信息 |
| 修改密码 | PUT /api/accounts/1/password | 返回200，成功 |
| 删除账号 | DELETE /api/accounts/1 | 返回200，成功 |
| 未登录访问 | 无session | 返回401，未授权 |
