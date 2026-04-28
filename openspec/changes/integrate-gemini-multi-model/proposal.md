## Why

当前的 AI Knowledge Copilot 硬编码使用 OpenAI GPT-3.5 模型，这限制了平台的灵活性和测试能力。为了提升竞争力，我们需要让用户能够使用不同的 LLM 提供商（例如 Google Gemini 1.5），以便他们能够对比模型性能、成本和响应质量。此外，在本地开发或无网络/API 密钥的情况下，我们需要一个“Mock（模拟）模型”作为后备选项。

## What Changes

- **后端层**：更新聊天 API (`/api/chat`)，使其能够接收 `model` 参数。实现一个模型路由器（工厂模式），根据请求动态初始化相应的 LLM 实例（OpenAI、Gemini 或 Mock），同时保持底层 Tool Calling 接口和嵌入（Embedding）模型的一致性。
- **前端层**：在应用的 Header 区域增加一个“模型选择器（Model Selector）”下拉菜单，允许用户在 GPT-3.5、Gemini 1.5 Flash 和 Mock 模型之间进行实时切换。前端需要将用户选择的模型持久化到状态中，并在每次对话请求时携带该参数。
- **依赖项**：后端 `requirements.txt` 中新增 `langchain-google-genai` 依赖。

## Capabilities

### New Capabilities
- `multi-llm-routing`: 后端多模型路由能力。根据用户请求中的偏好，动态将对话请求路由给不同的 LLM 提供商（OpenAI, Google），并确保底层 Tool Calling 的行为一致。
- `model-selection-ui`: 前端模型选择能力。提供直观的 UI 组件，允许用户从系统支持的 AI 模型列表中选择并切换他们偏好的模型。

### Modified Capabilities
- `agent-orchestrator`: 代理编排器。需求变更：不再使用硬编码的单例 LLM，而是支持在每次处理请求时，动态注入并使用指定的 LLM 引擎。

## Impact

- **后端代码**：修改 `main.py` (扩展 API Schema) 和 `agent.py` (重构 LLM 初始化和调用逻辑)。
- **前端代码**：修改 `App.tsx` (增加状态管理和下拉框组件) 和 `App.css` (新增组件样式)。
- **配置项**：需要用户在环境中提供 `GOOGLE_API_KEY` 以启用 Gemini 集成。
