## MODIFIED Requirements

### Requirement: AI 多步推理调度
系统 SHALL 使用 Agent 引擎（基于 LangChain 或 LangGraph）处理用户请求，识别意图并协调多个底层工具（API 和向量检索）的调用，输出最终综合答案。**系统 SHALL 支持根据请求参数动态切换底层 LLM 驱动（如 GPT 或 Gemini）。**

#### Scenario: 复杂意图的动态路由与执行
- **WHEN** 用户提出涉及 CRM 数据查询与产品政策组合的复杂查询，并在界面上指定了特定 LLM（例如 Gemini）
- **THEN** 调度系统先将请求派发给 Gemini，触发其调用 CRM 工具获取客户画像参数；随后利用该参数指导检索操作（RAG）；最后通过该指定的 Gemini 模型整合所有上下文信息，生成结构化的推荐回答与 UI 渲染元数据。
