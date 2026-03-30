# 前端说明

## 技术栈
- React 18
- Vite
- Ant Design
- Axios
- React Router

## 关键目录
- `frontend/src/pages`: 页面入口
- `frontend/src/components`: 可复用业务组件
- `frontend/src/service`: API 客户端
- `frontend/public`: 开发环境静态资源
- `frontend/nginx/html`: 生产构建输出

## 配置
运行时配置通过以下文件注入：
- `frontend/public/js/config.js`
- `frontend/nginx/html/js/config.js`

运行时变量命名为：
- `window.__APP_RUNTIME_CONFIG__`

## 运行
开发环境：

```shell
npm install
npm run dev
```

构建生产资源：

```shell
npm run build -- --outDir nginx/html
```

## 前后端协作
- 所有接口统一通过 `frontend/src/service/index.jsx` 调用
- 登录态通过本地存储与请求头自动注入维护
- 管理、教师、学生页面按用户类型控制路由访问
