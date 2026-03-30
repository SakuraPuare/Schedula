# 后端说明

## 核心能力
- 用户认证、注册、邮箱验证、反馈提交
- 学生资料、教师资料管理
- 课程计划、课程班级、选课记录、课表、成绩查询
- 教师排课、排课报告、排课删除
- 管理员时间窗口配置

## 入口
- 主服务入口：`backend/main.py`
- 应用装配：`backend/app/application.py`
- 调度服务入口：`backend/scheduler/main.py`

## 关键目录
- `backend/app/`: 当前主实现
- `backend/model/`: ORM 模型
- `backend/crud/`: 兼容旧数据访问逻辑
- `backend/sql/`: 初始化 SQL 与数据文件
- `backend/utils/`: 兼容工具和调度客户端

## 配置
主要配置放在：
- `backend/docker.env`
- `backend/docker.env.example`

关键变量包括：
- 数据库连接
- JWT 密钥
- 邮件服务
- `schedule_address`
- `public_base_url`

## 运行
开发或单独部署时可在 `backend/` 目录执行：

```shell
docker-compose up -d
```

统一部署推荐在根目录执行。
