# crm-integration Specification

## Purpose
TBD - created by archiving change ai-knowledge-copilot-mvp. Update Purpose after archive.
## Requirements
### Requirement: CRM 客户数据查询 API
系统 SHALL 提供并通过预定义的 API endpoint 从内部 CRM 系统中获取目标客户的关键画像与保单数据，拒绝直接的 Text-to-SQL 操作。

#### Scenario: 提取特定客户信息
- **WHEN** Agent 判断需要获取客户“张总”信息，从而调用该 CRM API 时
- **THEN** API 根据参数准确返回目标客户的标准化 JSON 响应（包含年龄、交费年限、风险等级等），供大模型作为强上下文逻辑约束。

