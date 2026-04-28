## ADDED Requirements

### Requirement: 动态模型路由机制 (Gemini 3 适配)
后端系统 SHALL 能够解析 HTTP 请求体中携带的 `model` 参数，并据此将对话请求精准路由到最新的 Google Gemini 3 系列模型。

#### Scenario: 路由至 Google Gemini 3 Flash
- **WHEN** 收到包含 `model: "gemini-3-flash"` 的请求
- **THEN** 系统 SHALL 自动映射并初始化 `gemini-3-flash-preview` 实例，利用最新的协议进行对话。

### Requirement: 工具调用协议兼容性
系统 SHALL 确保在调用 Gemini 3 模型时，自动补全或适配所需的 `thought_signature` 或其他元数据，以避免 API 返回 400 错误。

#### Scenario: 成功的跨模型工具调用
- **WHEN** Gemini 3 模型决定调用 `search_knowledge_tool`
- **THEN** 系统 SHALL 正确处理请求头和响应体，确保推理链不中断。
