## Why

系统当前集成的 Gemini 模型版本较低（1.5-flash），且在调用工具时遇到 `thought_signature` 缺失导致的 400 错误。为了提升性能并解决兼容性问题，需要迁移至最新的 Gemini 3 Flash 模型，该模型提供了更强的推理能力和更好的工具调用支持。

## What Changes

- **模型版本更新**：将后端集成的 Gemini 模型从 `gemini-1.5-flash` 升级为 `gemini-3-flash-preview`。
- **工具调用适配**：调整后端逻辑以兼容 Gemini 3 系列的 Function Calling 协议，解决之前遇到的 `thought_signature` 缺失问题。
- **前端配置同步**：更新前端 UI 中的模型选择项，将 "Google Gemini 1.5 Flash" 替换为 "Google Gemini 3 Flash"。

## Capabilities

### New Capabilities
- 无

### Modified Capabilities
- `multi-llm-routing`: 更新路由逻辑，将 Gemini 请求映射至 `gemini-3-flash-preview`。
- `agent-orchestrator`: 优化代理编排器以利用 Gemini 3 的原生工具调用能力。

## Impact

- **后端代码**：主要修改 `agent.py` 中的模型映射和初始化参数。
- **前端代码**：修改 `App.tsx` 中的模型选项配置。
- **依赖**：确保环境中的 `langchain-google-genai` 版本支持最新模型。
