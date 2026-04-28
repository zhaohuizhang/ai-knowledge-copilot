## MODIFIED Requirements

### Requirement: AI 多步推理调度
系统 SHALL 使用 Agent 引擎（基于 LangChain 或 LangGraph）处理用户请求，识别意图并协调多个底层工具（API 和向量检索）的调用，输出最终综合答案。**对于 Gemini 3 模型，系统 SHALL 针对其特定的 Function Calling 规范优化 Prompt 结构。**

#### Scenario: 复杂意图的路由与执行 (Gemini 3 优化)
- **WHEN** 用户在 UI 中选择了 Gemini 3 并提出复杂混合查询
- **THEN** 系统 SHALL 启动经过 Gemini 3 适配的 AgentExecutor，确保其在调用 CRM 和 RAG 工具时具有比 1.5 版本更高的稳定性和推理连贯性。
