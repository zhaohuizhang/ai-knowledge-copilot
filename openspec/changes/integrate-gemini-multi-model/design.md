## Context

AI Knowledge Copilot 当前的架构中，OpenAI GPT-3.5 的 Agent 实例化是静态的且与核心逻辑深度耦合。这种紧耦合使得我们无法轻易测试其他基座模型，也缺乏本地开发时的后备机制。此外，系统使用 Milvus 作为向量数据库，目前配置了固定维度（1536），这是为 OpenAI Embeddings 专门优化的。

## Goals / Non-Goals

**Goals:**
- 实现后端模型工厂（Model Factory），支持动态初始化和缓存不同的 LLM（OpenAI, Gemini, Mock）。
- 在前端构建一个模型切换器，实现实时的跨模型对话体验。
- 确保不同模型提供商在调用系统工具（如 CRM 查询、知识检索）时具有一致的行为和输出格式。

**Non-Goals:**
- **不更改 Embedding 模型**：为避免重新索引 Milvus 中的大量向量数据，本次重构仅涉及对话（Chat）模型，检索（RAG）环节将继续固定使用 OpenAI Embeddings。
- 不支持所有的 LLM：本次范围仅限集成 Google Gemini，验证多模型架构的可行性。

## Decisions

### Decision 1: 使用 `ChatGoogleGenerativeAI` (`langchain-google-genai`)
**Rationale**: 这是 LangChain 官方提供的 Google Gemini 集成方案。使用它可以让我们在保留现有 LangChain Prompt Templates 和 Tools 定义的前提下，以最小的代码修改量接入 Gemini。
**Alternatives**: 使用 Google Generative AI 的原生 Python SDK（缺点：存在过多样板代码，且需要重新实现 Tool 抽象，工作量大）。

### Decision 2: 采用模型工厂与缓存模式 (Model Factory & Cache)
**Rationale**: 废弃 `agent.py` 中全局单例的 `llm` 实例，改为 `get_agent_executor(model_name)` 工厂函数。为了提高性能，我们会缓存已实例化的 AgentExecutor。这样设计具备良好的扩展性，未来接入新模型只需在工厂中添加新的分支即可。

### Decision 3: 统一使用 `create_tool_calling_agent`
**Rationale**: 原代码使用的 `create_openai_tools_agent` 是 OpenAI 专属的 API。迁移到更通用的 `create_tool_calling_agent`，可以提供跨模型提供商（OpenAI 和 Gemini）的标准函数调用协议支持，消除底层格式差异。

## Risks / Trade-offs

- **[Risk] 向量维度不匹配导致检索失败** → **Mitigation**: 明确分离 Chat 模型和 Embedding 模型。即使前端选择了 Gemini 作为聊天大脑，底层知识库检索时依然强制调用 `OpenAIEmbeddings`，从而保证与 Milvus 中 1536 维度的向量完美兼容。
- **[Risk] API Key 缺失导致系统崩溃** → **Mitigation**: 系统在运行时进行严格的环境变量校验（`GOOGLE_API_KEY`, `OPENAI_API_KEY`）。如果用户选择的模型缺失对应的 Key，系统将优雅降级（Graceful Degradation），自动回退到 `mock_llm`，并向前端返回友好的错误提示。
- **[Risk] 工具调用返回格式的微小差异** → **Mitigation**: 尽管 Gemini 1.5 系列的 Function Calling 与 GPT 类似，但可能在 JSON 嵌套上存在差异。我们将依赖 LangChain 内置的解析器来抹平这些差异，保证最终输出的 JSON 元数据结构一致。
