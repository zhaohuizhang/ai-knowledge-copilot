## 1. 后端逻辑升级

- [x] 1.1 修改 `backend/agent.py` 中的模型映射字典，将 `gemini` 相关请求路由至 `gemini-3-flash-preview`。
- [x] 1.2 在 `agent.py` 中更新工具调用协议处理，确保 Gemini 3 能够稳定触发 CRM 和 RAG 工具而不会抛出 400 错误。

## 2. 前端界面同步

- [x] 2.1 修改 `frontend/src/App.tsx` 中的 `selectedModel` 选项列表，更新显示名称为 "Google Gemini 3 Flash"。

## 3. 集成验证

- [x] 3.1 使用 `test_agent.py` 脚本针对 `gemini-3-flash-preview` 进行冒烟测试。
- [x] 3.2 在本地环境启动全栈服务，验证前端模型切换后的端到端对话流程。
