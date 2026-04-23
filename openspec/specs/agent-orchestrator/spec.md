# agent-orchestrator Specification

## Purpose
TBD - created by archiving change ai-knowledge-copilot-mvp. Update Purpose after archive.
## Requirements
### Requirement: AI 多步推理调度
系统 SHALL 使用 Agent 引擎（基于 LangChain 或 LangGraph）处理用户请求，识别意图并协调多个底层工具（API 和向量检索）的调用，输出最终综合答案。

#### Scenario: 复杂意图的路由与执行
- **WHEN** 用户提出涉及 CRM 与政策组合的混合查询（例如“给50岁的客户推荐稳健的养老险”）
- **THEN** 系统先触发 CRM 工具获取目标客户画像参数，利用该参数改写查询，去 RAG 知识库检索相关的产品片段，最后整合生成推荐回答与 UI 渲染数据。

