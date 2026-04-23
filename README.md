# AI Knowledge Copilot - 综拓业务经理智能助手

AI Knowledge Copilot 是一个为保险业务经理打造的智能问答系统。它结合了大模型（LLM）、向量数据库（RAG）以及 CRM 接口，能够辅助业务经理快速查询保险产品政策、客户画像，并生成个性化的保险方案推荐。

## 核心功能

- **智能 RAG 问答**：基于 Milvus 向量数据库，支持对保险 PDF 政策、产品费率表的精准检索。
- **CRM 数据联动**：通过内置 API 模拟获取客户画像，辅助 Agent 进行上下文感知的方案设计。
- **Multi-step Agent**：使用 LangChain 构建的调度引擎，可自动判断是否需要查询 CRM 或搜索知识库。
- **结构化卡片展示**：前端支持渲染特殊的业务卡片（如产品推荐卡片），提升交互体验。

## 项目结构

```
ai-knowledge-copilot/
├── backend/            # FastAPI 后端 (Python)
├── frontend/           # React 前端 (Vite + TypeScript)
├── docker-compose.yml  # 基础设施配置 (MySQL, Redis, Milvus)
└── openspec/           # 项目规格说明与设计文档
```

## 快速开始

### 1. 环境依赖

确保您的机器上已安装：
- Docker & Docker Compose
- Python 3.9+
- Node.js 18+

### 2. 启动基础设施

在根目录下运行以下命令启动数据库服务：

```bash
docker-compose up -d
```
该命令会启动 MySQL (3306), Redis (6379) 以及 Milvus 向量数据库环境。

### 3. 配置与启动后端

进入 `backend` 目录，安装依赖并初始化数据：

```bash
cd backend
python3 -m pip install -r requirements.txt

# 初始化数据库（创建表并注入模拟知识库数据）
PYTHONPATH=. python3 init_db.py

# 启动服务 (默认端口 8000)
python3 -m uvicorn main:app --reload
```

> **注意**：项目默认开启了 **Mock Mode**。如果您没有配置 `OPENAI_API_KEY` 环境变量，系统将使用模拟的 AI 响应逻辑进行演示。若需使用真实 AI 功能，请设置：
> `export OPENAI_API_KEY=your_key_here`

### 4. 启动前端

进入 `frontend` 目录，启动开发服务器：

```bash
cd frontend
npm install
npm run dev
```
访问 `http://localhost:5173` 即可开始对话。

## 测试用例

您可以尝试以下对话来测试全链路功能：
- **基础问候**：发送 “你好”
- **查询画像**：发送 “帮我查一下张三的画像”
- **方案推荐**：发送 “根据张三的情况，推荐一款合适的养老险” (触发 Product Card 渲染)

## 规格文档

项目详细的设计思路、数据库模型以及 API 规格请参考 `openspec/specs/` 目录。
