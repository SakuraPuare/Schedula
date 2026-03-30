# Schedula

`Schedula` 是一个课程、排课、选课与成绩管理一体化平台的单仓库工程。

## 目录结构
- `backend`: FastAPI 后端、调度服务、数据库脚本、部署配置
- `frontend`: React 前端、Nginx 静态发布资源、前端部署配置
- `docs`: 架构、部署、开发与来源说明文档

## 技术栈
- 后端：FastAPI、SQLAlchemy、MySQL、gRPC
- 前端：React、Vite、Ant Design
- 调度：PuLP、NumPy
- 部署：Docker、Nginx

## 快速启动
在根目录执行：

```shell
docker-compose up -d
```

## 文档
- [系统架构](./docs/architecture.md)
- [后端说明](./docs/backend.md)
- [前端说明](./docs/frontend.md)
- [部署指南](./docs/deployment.md)
- [来源说明](./docs/origins.md)

## 子系统说明
- 后端入口见 [backend/README.md](./backend/README.md)
- 前端入口见 [frontend/README.md](./frontend/README.md)

## 致谢与来源
当前仓库不是 fork，而是基于两个独立上游仓库整理、重构并合并而来：
- 后端来源：`https://github.com/NaClCode/whut_database_backend`
- 前端来源：`https://github.com/NaClCode/whut_database_frondend`
