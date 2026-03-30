# Schedula Backend
<p align="center">Schedula 后端服务</p>
<p align="center">
    <img src="https://img.shields.io/static/v1?label=%E5%BC%80%E5%8F%91%E6%97%B6%E9%97%B4&message=2024-2025&color=007bff"/>
    <img src="https://img.shields.io/static/v1?label=Python&message=3.10&color=e83e8c"/>
    <img src="https://img.shields.io/static/v1?label=MySQL&message=8.0.28&color=fd7e14"/>
    <img src="https://img.shields.io/static/v1?label=%E7%B1%BB%E5%9E%8B&message=backend&color=20c997"/>
</p>

## 简介
- 本目录包含 Schedula 的 API 服务、业务逻辑、数据库脚本和调度子服务
- 后端采用 FastAPI，排课子服务通过 gRPC 与主服务协作
- 配置与部署方式见根目录与 `docs/`

## 运行
1. 复制 [docker.env.example](./docker.env.example) 为 `docker.env`，填入你自己的数据库、JWT 和邮件配置
2. 按照 [docker-compose.yaml](docker-compose.yaml) 配置容器环境变量
3. 运行后端本地编排文件或根目录统一编排文件
```shell
docker-compose up -d
```

## 文档
- [系统架构](../docs/architecture.md)
- [后端说明](../docs/backend.md)
- [部署指南](../docs/deployment.md)
- [来源说明](../docs/origins.md)

## 来源
- 原始后端远程仓库：`https://github.com/NaClCode/whut_database_backend`
