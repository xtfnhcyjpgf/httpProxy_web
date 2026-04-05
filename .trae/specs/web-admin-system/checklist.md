# Checklist

## 开发检查清单

### 项目初始化
- [x] 创建了 requirements.txt 并包含所有Python依赖（Flask、bcrypt等）
- [x] 创建了 config.py 配置文件（无硬编码）
- [x] 项目目录结构符合规格要求
- [x] 前端package.json包含Vue.js 3和Element Plus依赖
- [x] Vite构建配置正确

### 数据库
- [x] users表字段设计符合规格（id, username, password_hash, created_at）
- [x] 数据库初始化脚本正常工作
- [x] 无外键约束（遵循规格要求）
- [x] 初始化账号admin/admin123已创建

### 后端API
- [x] 登录API (POST /api/login) 正确验证账号密码
- [x] 登录API使用bcrypt加密验证
- [x] 退出API (POST /api/logout) 正确清除会话
- [x] 账号列表API (GET /api/accounts) 返回所有用户（不包含明文密码）
- [x] 添加账号API (POST /api/accounts) 正确创建用户
- [x] 修改密码API (PUT /api/accounts/:id/password) 正确更新密码
- [x] 删除账号API (DELETE /api/accounts/:id) 正确删除用户
- [x] 会话验证中间件正确拦截未登录请求
- [x] CORS跨域配置正确

### 前端页面（Vue.js 3 + Element Plus）

#### 登录页面 (Login.vue)
- [x] Element Plus居中卡片式登录框
- [x] 用户名输入框 (el-input)
- [x] 密码输入框 (el-input type="password")
- [x] 登录按钮 (el-button type="primary")
- [x] 错误提示使用 el-alert 或 ElMessage

#### 管理主页 (Index.vue + Layout.vue)
- [x] Element Plus布局容器（el-container、el-aside、el-main）
- [x] 左侧固定侧边栏 (el-menu)
- [x] 顶部导航或LOGO区域
- [x] 路由跳转正常

#### 账号管理页面 (Account.vue)
- [x] Element Plus表格组件 (el-table) 展示账号列表
- [x] 表格列：ID、用户名、创建时间、操作按钮
- [x] 添加账号按钮 (el-button type="primary")
- [x] 添加账号对话框 (el-dialog + el-form)
- [x] 修改密码对话框 (el-dialog + el-form)
- [x] 删除账号确认 (ElMessageBox.confirm)
- [x] 操作按钮：修改密码、删除

#### Vue.js功能
- [x] Vue Router路由配置正确
- [x] 路由守卫拦截未登录用户
- [x] API调用模块正确封装 (axios)
- [x] 认证状态管理正常 (Pinia store或provide/inject)

### Flask应用
- [x] app.py正确配置Flask应用
- [x] 会话管理正确配置（Flask session）
- [x] 静态文件正确serve（dist目录）
- [x] CORS中间件配置正确

### 接口测试
- [x] 登录接口测试：正确账号登录成功
- [x] 登录接口测试：错误密码登录失败
- [x] 登录接口测试：不存在用户登录失败
- [x] 账号列表接口测试：返回正确数据格式
- [x] 添加账号接口测试：成功创建新账号
- [x] 修改密码接口测试：成功更新密码
- [x] 删除账号接口测试：成功删除账号
- [x] 会话验证测试：未登录访问被拦截

### 安全
- [x] 密码使用bcrypt加密存储
- [x] 敏感路由有会话验证
- [x] 无硬编码配置信息（使用config.py）

### 部署
- [x] 系统能在2C2G服务器上运行
- [x] 使用SQLite数据库（无需额外服务）
- [x] 前端构建后能正常serve
- [x] requirements.txt包含所有Python依赖
