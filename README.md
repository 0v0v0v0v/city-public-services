# 城市公共便民点位整合平台

基于 `proposal.md` 搭建的课程项目框架，采用前后端分离结构：

- `backend/`: `FastAPI + SQLite + SQLAlchemy + JWT`
- `frontend/`: `Vue 3 + Vite + Tailwind CSS + Pinia`

项目围绕公益性城市公共服务资源整合展开，首版重点包含分类浏览、关键词搜索、点位详情、资讯展示与后台录入管理。

## 本地启动

### 1. 启动后端

```bash
cd backend
uv venv --python 3.13
source .venv/bin/activate
uv sync --dev
uv run uvicorn app.main:app --reload
```

后端默认地址为 `http://127.0.0.1:8000`。

首次启动会自动创建 `app.db` 并写入演示数据。

默认管理员账号：

- 用户名：`admin`
- 密码：`admin123`

### 2. 启动前端

```bash
cd frontend
pnpm install
pnpm run dev
```

前端默认地址为 `http://127.0.0.1:5173`。

## VS Code F5 调试

项目已提供 `.vscode/launch.json` 和 `.vscode/tasks.json`。

首次使用建议先执行一次：

```bash
cd backend
uv venv --python 3.13
```

然后在 VS Code 中：

```text
Terminal -> Run Task -> Bootstrap Dev Environment
Run and Debug -> Full Stack Dev -> F5
```

说明：

- `Backend: FastAPI` 会使用 `backend/.venv/bin/python` 启动 `uvicorn --reload`
- `Frontend: Vite` 会启动 `npm run dev`
- Vue 和 Tailwind 的热更新由 Vite 原生提供，保存前端文件后页面会自动刷新
- `Full Stack Dev` 会同时启动前后端，按一次 `Shift+F5` 可一起停止

## 已实现能力

- 前台页面
  - 首页聚合接口 `/api/home`
  - 分类浏览 `/categories`
  - 点位列表与筛选 `/points`
  - 点位详情 `/points/:id`
  - 资讯列表与详情 `/news`
  - 项目介绍 `/about`
- 后台页面
  - 管理员登录 `/admin/login`
  - 后台总览 `/admin`
  - 分类、点位、资讯新增录入
- 后端 API
  - 公共接口：`/api/categories`、`/api/points`、`/api/points/{id}`、`/api/news`、`/api/news/{id}`、`/api/home`
  - 管理接口：`/api/admin/auth/login`、`/api/admin/categories`、`/api/admin/points`、`/api/admin/news`

## 运行测试

```bash
cd backend
uv run pytest
```
