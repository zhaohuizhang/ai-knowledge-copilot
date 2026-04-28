## ADDED Requirements

### Requirement: 动态模型路由机制
后端系统 SHALL 能够解析 HTTP 请求体中携带的 `model` 参数，并据此将对话请求精准路由到指定的 LLM 提供商引擎。

#### Scenario: 路由至 Google Gemini
- **WHEN** 收到包含 `model: "gemini-1.5-flash"` 的请求
- **THEN** 系统 SHALL 通过 LangChain 适配器初始化并调用 Google Gemini 1.5 Flash 模型来生成回复。

#### Scenario: 路由至 OpenAI
- **WHEN** 收到包含 `model: "gpt-3.5-turbo"` 的请求
- **THEN** 系统 SHALL 初始化并调用 OpenAI GPT-3.5-Turbo 模型来生成回复。

#### Scenario: 优雅降级与模拟回退
- **WHEN** 请求指定的模型不可用（例如环境变量中缺失对应的 API 密钥）
- **THEN** 系统 SHALL 自动降级并回退到本地的 `mock_llm` 实现，以确保对话服务不被中断，并返回模拟数据。

### Requirement: 跨模型工具调用一致性
系统 SHALL 确保所有被接入的 LLM（无论是 OpenAI 还是 Gemini）都能够通过统一的接口成功调用系统的基础工具集（例如：`get_client_profile_tool`, `search_knowledge_tool`）。

#### Scenario: Gemini 执行工具调用
- **WHEN** Gemini 模型在推理过程中识别出需要调用外部工具
- **THEN** 系统 SHALL 正确捕获该意图，执行相应的系统工具，并将执行结果以符合 Gemini Function Calling 规范的格式返回给模型，以继续后续的推理。
