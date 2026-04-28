## Context

系统在集成 Gemini 1.5 Flash 过程中遇到了工具调用兼容性问题（400 错误，提示 `thought_signature` 缺失）。为了利用更现代的 AI 推理能力并解决这些协议层面的错误，我们需要将模型驱动升级为 Google 发布的最新 Gemini 3 Flash 预览版。

## Goals / Non-Goals

**Goals:**
- 实现后端 Agent 逻辑向 `gemini-3-flash-preview` 的平滑迁移。
- 解决工具调用时的协议兼容性问题，确保知识库检索和 CRM 查询功能在 Gemini 3 下正常工作。
- 提升系统响应的准确性和结构化数据的产出质量。

**Non-Goals:**
- 不涉及 Embedding 模型或 Milvus 存储结构的修改。
- 不对现有的多模型路由框架进行大规模重构。

## Decisions

### Decision 1: 采用 `gemini-3-flash-preview` 作为默认 Gemini 引擎
- **Rationale**: 该模型是目前 Google 提供的最先进的轻量级模型，在处理多步骤推理和工具调用方面比 1.5 系列有显著改进。
- **Alternatives**: 继续保留 1.5 Flash 并尝试通过手动补全协议头来修复（实现复杂度高且收益有限）。

### Decision 2: 动态模型映射增强
- **Rationale**: 在 `agent.py` 中增加更细致的映射逻辑，确保前端传来的 `gemini` 标识符能够精准指向后端支持的最优版本。

## Risks / Trade-offs

- **[Risk] 预览版模型的不稳定性** → **Mitigation**: 保留 Mock 模型作为安全回退方案，并在 `.env` 中提供灵活的 Key 配置。
- **[Risk] Prompt 敏感度差异** → **Mitigation**: 针对 Gemini 3 优化 System Prompt，特别是在处理工具调用返回值的上下文注入方面进行微调。
