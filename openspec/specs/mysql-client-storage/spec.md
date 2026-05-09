# mysql-client-storage Specification

## Purpose
TBD - created by archiving change implement-mysql-crm. Update Purpose after archive.
## Requirements
### Requirement: 银行客户数据库表结构
系统 SHALL 在 MySQL 中维护一个名为 `bank_clients` 的表，用于存储银行客户的画像信息。

#### Scenario: 表结构定义
- **WHEN** 数据库初始化或迁移时
- **THEN** 系统创建包含 `id`, `name`, `age`, `gender`, `occupation`, `risk_level`, `total_assets`, `insurance_preferences` 等字段的表

### Requirement: 客户数据持久化
系统 SHALL 支持对银行客户数据的增删改查操作，确保数据在服务重启后依然可用。

#### Scenario: 存储新客户信息
- **WHEN** 管理员通过后台或脚本录入新客户“王五”
- **THEN** 客户数据被正确写入 `bank_clients` 表中

