# Web管理系统 Spec

## Why
需要一个轻量级的Web管理后台系统，用于账号管理，部署在2C2G资源受限的服务器上。

## What Changes
- 全新开发Web管理系统的后端API和前端界面
- 使用SQLite作为数据库
- 采用轻量级后端框架（Flask API模式）以适应低资源配置
- 采用Vue.js + Element Plus作为前端框架，提供现代化美观界面

## Impact
- 新增系统能力：用户登录、账号管理
- 涉及代码：后端API、前端页面、数据库模型

## 技术选型
- **后端框架**: Flask（轻量级Python Web框架，提供REST API）
- **数据库**: SQLite（零配置、适合轻量部署）
- **前端框架**: Vue.js 3 + Element Plus（现代化UI，美观大方）
- **构建工具**: Vite（快速构建）
- **密码加密**: bcrypt（安全哈希算法）

## 架构设计
采用前后端分离架构：
- **后端**: Flask提供REST API（JSON格式）
- **前端**: Vue.js 3构建，单页应用，通过axios调用后端API
- **部署**: 前端构建为静态文件，由Flask直接serve（简化部署）

## ADDED Requirements

### Requirement: 用户登录功能
系统 SHALL 提供用户登录功能，用户通过账号密码登录系统。

#### Scenario: 登录成功
- **WHEN** 用户输入正确的账号密码
- **THEN** 系统返回登录成功，跳转到管理主页

#### Scenario: 登录失败
- **WHEN** 用户输入错误的账号密码
- **THEN** 系统返回错误提示"账号或密码错误"

### Requirement: 账号管理功能
系统 SHALL 提供账号管理功能，包括添加账号和修改密码。

#### Scenario: 添加账号
- **WHEN** 管理员输入新账号信息（账号名、密码）
- **THEN** 系统创建新账号并返回成功提示

#### Scenario: 修改密码
- **WHEN** 管理员选择账号并输入新密码
- **THEN** 系统更新密码并返回成功提示

#### Scenario: 查看账号列表
- **WHEN** 管理员访问账号管理页面
- **THEN** 系统展示所有账号列表（不显示明文密码）

### Requirement: 会话管理
系统 SHALL 提供会话管理功能，用户登录后保持会话状态。

#### Scenario: 访问受保护页面
- **WHEN** 未登录用户直接访问管理页面
- **THEN** 系统重定向到登录页面

#### Scenario: 退出登录
- **WHEN** 用户点击退出按钮
- **THEN** 系统清除会话并重定向到登录页面

## MODIFIED Requirements

无

## REMOVED Requirements

无

## 数据库设计

### 用户表 (users)
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 用户ID |
| username | TEXT | UNIQUE NOT NULL | 用户名 |
| password_hash | TEXT | NOT NULL | 密码哈希值 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

## 项目结构
```
httpProxy_web/
├── app.py                  # Flask应用入口（API服务）
├── config.py               # 配置文件
├── database.db             # SQLite数据库文件
├── requirements.txt        # Python依赖
├── frontend/               # 前端项目
│   ├── package.json       # 前端依赖
│   ├── vite.config.js     # Vite配置
│   ├── index.html         # 入口HTML
│   ├── src/
│   │   ├── main.js        # Vue应用入口
│   │   ├── App.vue        # 根组件
│   │   ├── router/
│   │   │   └── index.js   # 路由配置
│   │   ├── views/
│   │   │   ├── Login.vue  # 登录页面
│   │   │   ├── Index.vue  # 管理主页
│   │   │   └── Account.vue # 账号管理页面
│   │   ├── components/
│   │   │   └── Layout.vue # 布局组件
│   │   ├── api/
│   │   │   └── index.js   # API调用封装
│   │   └── stores/
│   │       └── auth.js    # 认证状态管理
│   └── public/
└── dist/                   # 前端构建输出目录（由Flaskserve）
```

## API设计

### 认证API
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/login | 用户登录 |
| POST | /api/logout | 用户退出 |
| GET | /api/auth/status | 获取当前登录状态 |

### 账号管理API
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/accounts | 获取账号列表 |
| POST | /api/accounts | 添加新账号 |
| PUT | /api/accounts/:id/password | 修改账号密码 |
| DELETE | /api/accounts/:id | 删除账号 |

## 部署要求
- 系统应能在2C2G服务器上流畅运行
- 数据库文件存储在本地SQLite文件
- 无需额外服务依赖（Redis等）
- 前端构建后作为静态文件由Flask serve
