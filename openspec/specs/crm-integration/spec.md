# crm-integration Specification

## Purpose
TBD - created by archiving change ai-knowledge-copilot-mvp. Update Purpose after archive.
## Requirements
### Requirement: CRM 客户数据查询 API
系统 SHALL 提供并通过预定义的 API endpoint 从 MySQL 数据库中获取目标客户的关键画像与保单数据。系统禁止直接的 Text-to-SQL 操作，必须通过代码逻辑封装查询。

#### Scenario: 提取特定客户信息
- **WHEN** Agent 判断需要获取客户信息并调用 CRM API 时
- **THEN** 系统从 `bank_clients` 表中检索对应名称的记录，并返回标准化的 JSON 响应（包含年龄、职业、资产状况、风险等级等），供大模型作为强上下文逻辑约束。

