# Clawith 二次开发结构分析与改造建议

## 1. 项目结构分析（核心模块）

## 1.1 顶层结构
- `frontend/`：React + TypeScript 前端应用（页面、组件、国际化、主题样式）。
- `backend/`：FastAPI 后端（鉴权、Agent 生命周期、工具/技能/模板、租户与组织管理）。
- `backend/agent_template/`：新建 Agent 时复制的默认工作区模板（包含默认 `soul.md`）。
- `assets/`：仓库文档展示用品牌素材（README 中的 slogan、二维码等）。

## 1.2 前端核心模块
- 路由与页面入口：`frontend/src/App.tsx`
  - 包含登录页 `/login`、组织初始化页 `/setup-company`、主后台 Layout 与业务页路由。
- 鉴权与 API 调用：
  - `frontend/src/stores/index.ts`（token/user 状态）
  - `frontend/src/services/api.ts`（所有 API 封装）
- 视觉与品牌层：
  - `frontend/src/index.css`（全局 CSS 变量、主色、暗/亮主题）
  - `frontend/public/logo*.png|svg`（logo 资源）
  - `frontend/index.html`（浏览器标题、favicon、meta description）
- 文案与国际化：
  - `frontend/src/i18n/en.json`
  - `frontend/src/i18n/zh.json`

## 1.3 后端核心模块
- 应用入口与路由装配：`backend/app/main.py`
  - 启动时执行建表/种子/后台任务，并挂载 API 路由。
- 鉴权与注册登录：`backend/app/api/auth.py`
  - `POST /auth/register`、`POST /auth/login`。
- 租户/组织注册策略：`backend/app/api/tenants.py`
  - 公司自创建开关、邀请码加入流程。
- 系统配置：`backend/app/config.py`
  - 应用名、数据库、Redis、CORS、Agent 数据目录等。
- Agent 初始化链路（与 soul 相关）：
  1. `backend/agent_template/soul.md`：文件模板基线。
  2. `backend/app/services/agent_manager.py`：创建 Agent 时拷贝模板并替换变量。
  3. `backend/app/services/template_seeder.py`：内置 AgentTemplate（数据库层 soul_template）。
  4. `backend/app/services/agent_seeder.py`：默认演示 Agent（Morty/Meeseeks）的 soul 内容。

---

## 2. 需要修改的关键文件清单（按你关注的类别）

## 2.1 品牌相关（logo / 名称 / 配色）

### A) Logo 与站点基础品牌
- `frontend/public/logo.png`
- `frontend/public/logo-black.png`
- `frontend/public/logo-white.png`
- `frontend/public/logo.svg`
- `frontend/index.html`
  - `<link rel="icon" href="/logo.png">`
  - `<meta name="description" ...>`
  - `<title>Clawith</title>`

### B) 页面中直接写死的品牌名称
- `frontend/src/pages/Layout.tsx`
  - 侧边栏品牌文字 `Clawith`。
- `frontend/src/pages/Login.tsx`
  - 登录卡片品牌文字 `Clawith`。
- `frontend/src/pages/CompanySetup.tsx`
  - 使用 logo，建议与登录页统一换新品牌。

### C) 多语言品牌文案（强烈建议统一）
- `frontend/src/i18n/en.json`
  - `app.name`、`login.hero.title`、`login.hero.subtitle`、`login.hero.description` 等。
- `frontend/src/i18n/zh.json`
  - 对应中文品牌字段。

### D) 全局配色 / 主题
- `frontend/src/index.css`
  - 重点变量：`--accent-primary`、`--bg-*`、`--text-*`。
- `frontend/src/utils/theme.ts`
  - 支持动态 accent 色保存/应用；如要固定商业品牌主色，可在此限制或重置策略。

### E) 后端品牌名（服务元信息）
- `backend/app/config.py`
  - `APP_NAME = "Clawith"`。
- `backend/pyproject.toml`
  - `description` 含 Clawith。

### F) 文档与对外信息（可后置）
- `README.md` 及多语言 README
- `assets/Clawith_slogan.png`
- `.env.example` 注释头中的品牌名

## 2.2 默认 Agent 模板（`soul.md`）

你至少要看三层：
1. **文件模板层**（新 Agent 工作区物理文件）
   - `backend/agent_template/soul.md`
2. **数据库模板层**（创建 Agent 可选内置职业模板）
   - `backend/app/services/template_seeder.py`（`DEFAULT_TEMPLATES[*].soul_template`）
3. **默认演示 Agent 层**（首个管理员注册后自动生成）
   - `backend/app/services/agent_seeder.py`（`MORTY_SOUL`、`MEESEEKS_SOUL`）

> 说明：如果只改 `backend/agent_template/soul.md`，内置模板和已创建的默认 Agent 人设仍会带原始风格。

## 2.3 登录/注册页面

### 前端页面
- `frontend/src/pages/Login.tsx`
  - 登录/注册切换是同一个页面（`isRegister` 控制）。
  - 品牌视觉主入口（Hero 区 + Logo + 标题）。
- `frontend/src/index.css`
  - 登录页和表单样式在全局 CSS 中定义。

### 后端接口
- `backend/app/api/auth.py`
  - `/auth/register`、`/auth/login` 具体规则。
  - 首注册用户自动设为 platform_admin。
- `backend/app/schemas/schemas.py`
  - `UserRegister`、`UserLogin` 字段约束。

### 注册后公司接入流程（常被忽略）
- `frontend/src/pages/CompanySetup.tsx`
- `backend/app/api/tenants.py`
  - 注册后是否允许「自建公司 / 邀码入驻」由这里控制。

## 2.4 配置文件

### 后端运行配置（最高优先级）
- `.env.example`
  - 商业化部署前，建议整理成你的品牌默认值与接入说明。
- `backend/app/config.py`
  - 所有运行时关键参数（DB、Redis、CORS、APP_NAME、沙箱等）。

### 前端构建与运行配置
- `frontend/vite.config.ts`
- `frontend/nginx.conf`
- `docker-compose.yml`
  - 如你要改域名、反向代理、部署端口、跨域策略，这三处通常要联动。

### 容器与启动脚本
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `setup.sh` / `restart.sh`
  - 打包成商业产品时，需要在这里固化默认部署行为。

---

## 3. 修改优先级建议（从“最快可品牌化上线”角度）

## P0（必须先做，影响对外品牌与可用性）
1. 替换前端 logo 与站点标题
   - `frontend/public/logo*`、`frontend/index.html`、`Login.tsx`、`Layout.tsx`。
2. 替换 i18n 中品牌名称与 slogan
   - `frontend/src/i18n/en.json`、`zh.json`。
3. 核查注册/登录流程在你商业模式下可用
   - `frontend/src/pages/Login.tsx`、`backend/app/api/auth.py`。
4. 初始化配置安全化
   - `.env.example`、`backend/app/config.py`（尤其 SECRET/JWT/CORS/数据库配置说明）。

## P1（强烈建议，影响产品一致性与“默认体验”）
1. 统一默认 Agent 人设与 `soul.md`
   - `backend/agent_template/soul.md`
   - `backend/app/services/template_seeder.py`
   - `backend/app/services/agent_seeder.py`
2. 统一公司接入策略（自建公司/邀请码）
   - `backend/app/api/tenants.py` + `CompanySetup.tsx`。
3. 统一主配色与主题策略
   - `frontend/src/index.css` + `frontend/src/utils/theme.ts`。

## P2（上线后持续优化）
1. 文档品牌替换与对外仓库信息更新
   - README、多语言文档、assets。
2. 商业化部署脚本与镜像规范化
   - Dockerfile、compose、setup/restart。
3. “Clawith/OpenClaw”历史术语清理（包括文案、placeholder、帮助文本）
   - 前后端全局检索替换并回归测试。

---

## 4. 实施建议（落地顺序）
1. **先做品牌壳替换**（Logo/名称/标题/i18n/P0），1~2 天内即可产出可演示版本。
2. **再做默认内容替换**（soul + 模板 + demo agents/P1），保证新建账号体验即是你的产品风格。
3. **最后做配置与部署固化**（env + docker + 域名 + CORS + 安全策略），进入商用可交付状态。

