# rag-knowledge-base Specification

## Purpose
TBD - created by archiving change ai-knowledge-copilot-mvp. Update Purpose after archive.
## Requirements
### Requirement: 向量化查询与时间戳过滤
系统 SHALL 提供针对保险和金融政策的知识库查询能力，依靠 Milvus 检索知识，并基于时间戳过滤过期内容。

#### Scenario: 时效性政策检索
- **WHEN** 向量库中存在同一产品的不同年份政策文档，且系统进行知识检索
- **THEN** 检索模块利用 metadata 里的时间戳进行前置或后置过滤，仅返回处于最新有效时间范围内的文档片段供大模型参考。

