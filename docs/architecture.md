# 系统架构

## 总览
Schedula 是一个单仓库全栈工程，提供课程查询、选课、成绩管理、教师排课与管理员时间窗口配置能力。

## 工程结构
- `backend/`: API 服务、调度服务、数据库初始化脚本
- `frontend/`: React 前端和 Nginx 静态发布目录
- `docs/`: 架构、部署、开发和来源说明

## 运行时组件
- `frontend`: 浏览器端界面，调用后端 REST API
- `backend`: FastAPI 主服务，负责认证、业务逻辑、数据访问
- `scheduler`: gRPC 调度服务，负责排课优化计算
- `mysql`: 持久化业务数据与初始化脚本

## 后端分层
- `app/controllers`: 控制器与路由装配
- `app/services`: 业务服务层
- `app/repositories`: 仓储层
- `app/core`: 配置、异常、数据库与安全能力
- `model/`: SQLAlchemy 数据模型
- `utils/opt_client`: 调度客户端

## 前端分层
- `src/pages`: 页面级入口
- `src/components`: 业务组件
- `src/service`: API 客户端封装
- `public/` 与 `nginx/html/`: 静态资源与构建结果

## 关键交互
- 浏览器通过 `frontend/src/service` 调用 REST API
- 后端在排课场景下通过 gRPC 调用 `backend/scheduler`
- 管理员可配置选课、排课、成绩时间窗口
- 前端静态资源可直接由 Nginx 托管
