## ADDED Requirements

### Requirement: 模型选择器 UI 组件
前端界面 SHALL 在全局显眼位置（例如应用的 Header 区域）提供一个用户界面元素（如下拉选择框），以便用户自主选择他们希望对话的 AI 模型。

#### Scenario: 实时切换模型
- **WHEN** 用户在下拉框中从默认模型切换为 "Google Gemini 1.5 Flash"
- **THEN** 前端应用 SHALL 立即更新其内部的 `selectedModel` 状态，并确保在接下来发起的 `/api/chat` 请求中，携带该新的模型标识符。

### Requirement: 模型偏好的会话级持久化
前端应用 SHALL 在用户当前处于活跃状态的会话期间，记住用户的模型选择偏好。

#### Scenario: 页面刷新时的默认行为
- **WHEN** 用户手动刷新了浏览器页面
- **THEN** 系统 SHALL 默认恢复至基础模型配置（例如 "gpt-3.5-turbo"），或者优先读取本地存储中上次记录的模型偏好。
