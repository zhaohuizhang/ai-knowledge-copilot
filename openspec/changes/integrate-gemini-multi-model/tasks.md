## 1. 后端依赖与配置准备

- [x] 1.1 在 `backend/requirements.txt` 中添加 `langchain-google-genai` 依赖。
- [x] 1.2 执行依赖安装命令以引入 Gemini SDK。

## 2. 后端核心逻辑重构

- [x] 2.1 修改 `backend/main.py`，扩展 `ChatRequest` 的 Pydantic 模型以支持接收 `model` 参数。
- [x] 2.2 修改 `backend/agent.py`，引入模型工厂缓存字典 `_agent_cache`。
- [x] 2.3 在 `agent.py` 中实现 `get_agent_executor(model_name)` 方法，根据模型名称动态实例化 `ChatOpenAI` 或 `ChatGoogleGenerativeAI`，并统一使用 `create_tool_calling_agent`。
- [x] 2.4 重构 `run_agent` 方法，处理模型参数传递、API 密钥缺失检查，并添加对 Mock 模型的安全回退逻辑。

## 3. 前端界面与交互升级

- [x] 3.1 修改 `frontend/src/App.tsx`，在组件中引入 `selectedModel` 状态。
- [x] 3.2 在 Header 区域添加 `<select>` 下拉框组件，绑定可选模型列表（GPT-3.5, Gemini 1.5, Mock）。
- [x] 3.3 修改 `handleSend` 函数，确保 POST 请求的 `body` 中包含当前选中的 `model` 字段。
- [x] 3.4 修改 `frontend/src/App.css`，为新增的模型选择器添加符合整体设计语言的高级感样式。

## 4. 集成与功能验证

- [x] 4.1 启动后端与前端服务，验证默认情况下的对话流程。
- [x] 4.2 提供有效的 `GOOGLE_API_KEY`，在前端切换至 Gemini 模型，验证对话和工具调用是否正常。
- [x] 4.3 移除 API 密钥或选择 Mock 模型，验证系统的优雅降级机制是否生效。
