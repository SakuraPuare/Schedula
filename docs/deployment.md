# 部署指南

## 根目录统一部署
推荐在项目根目录执行：

```shell
docker-compose up -d
```

将启动：
- `mysql`
- `scheduler`
- `backend`
- `frontend`

## 端口
- 前端：`81`
- 后端：`8000`
- 调度服务：`50051`
- MySQL 映射：`3307`

## 初始化准备
1. 复制 `backend/docker.env.example` 为 `backend/docker.env`
2. 填写数据库、JWT、邮件相关配置
3. 确认 Docker 可用

## 单独子系统运行
后端：

```shell
cd backend
docker-compose up -d
```

前端：

```shell
cd frontend
docker-compose up -d
```

## 常见问题
- 前端资源更新后需要重新执行构建
- 排课能力依赖 `scheduler` 服务在线
- 邮件验证能力依赖 SMTP 配置完整
