# chat-session-mgmt Specification

## Purpose
TBD - created by archiving change ai-knowledge-copilot-mvp. Update Purpose after archive.
## Requirements
### Requirement: 消息状态持久化与截断
系统 SHALL 在数据库中保存对话 session 和带有扩展属性的 message 数据，并在组装多轮对话 Prompt 时有效截断历史上下文。

#### Scenario: 上下文滑动截断
- **WHEN** 用户在同一 session 中发送超出截断阈值的消息（如第 15 轮次对话）
- **THEN** 系统仅提取最近 10 条有效对话记录进行 Prompt 拼装，丢弃更早的上下文以节省 Token 并保证稳定性。

### Requirement: 富文本 UI Metadata
系统 SHALL 能够在数据库的 `chat_message.metadata` (JSON 类型) 字段中存储 Agent 返回的复杂 UI 卡片类型、参数及相关的工具调用栈记录。

#### Scenario: 卡片渲染数据的记录
- **WHEN** Agent 生成并向前端返回了一款具体的理财产品推荐卡片
- **THEN** 当前 message 对应的数据表记录中的 `metadata` 字段将保存类似 `{"ui_type": "product_card", "data": {...}}` 的结构，确保前端刷新历史记录时能准确还原对应的可视化组件。

