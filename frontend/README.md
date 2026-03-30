# Schedula Frontend
<p align="center">Schedula 前端界面</p>
<p align="center">
    <img src="https://img.shields.io/static/v1?label=%E5%BC%80%E5%8F%91%E6%97%B6%E9%97%B4&message=2024-2025&color=007bff"/>
    <img src="https://img.shields.io/static/v1?label=Python&message=3.10&color=e83e8c"/>
    <img src="https://img.shields.io/static/v1?label=MySQL&message=8.0.28&color=fd7e14"/>
    <img src="https://img.shields.io/static/v1?label=%E7%B1%BB%E5%9E%8B&message=frontend&color=20c997"/>
</p>

## 简介
- 本目录包含 Schedula 的 Web 前端、静态资源和 Nginx 发布配置
- 前端基于 React、Vite 和 Ant Design 构建
- 接口与运行方式见根目录与 `docs/`

## 运行
1. 配置 [config.js](./nginx/html/js/config.js)
2. 运行前端本地编排文件或根目录统一编排文件
```shell
docker-compose up -d
```

## 文档
- [系统架构](../docs/architecture.md)
- [前端说明](../docs/frontend.md)
- [部署指南](../docs/deployment.md)
- [来源说明](../docs/origins.md)

## 来源
- 原始前端远程仓库：`https://github.com/NaClCode/whut_database_frondend`
