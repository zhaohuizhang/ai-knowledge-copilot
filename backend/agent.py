import json
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool, create_openai_tools_agent, AgentExecutor

from crm_api import MOCK_CRM_DATA
from rag_utils import search_knowledge
try:
    from mock_llm import mock_run_agent
except ImportError:
    mock_run_agent = None

# Define Tools
@tool
def get_client_profile_tool(name: str) -> str:
    """
    Fetch client profile from CRM. 
    Input should be the client's name.
    """
    if name in MOCK_CRM_DATA:
        return json.dumps(MOCK_CRM_DATA[name], ensure_ascii=False)
    return "Client not found in CRM."

@tool
def search_knowledge_tool(query: str) -> str:
    """
    Search the knowledge base for insurance products and policies.
    Input should be a search query.
    """
    embeddings = OpenAIEmbeddings()
    results = search_knowledge(query, embeddings, top_k=3)
    if not results:
        return "No relevant information found in the knowledge base."
    return "\n\n".join(results)

tools = [get_client_profile_tool, search_knowledge_tool]

# System Prompt
system_prompt = """You are an AI Knowledge Copilot for insurance business managers.
You can use tools to query CRM data for client profiles and search the knowledge base for insurance products and policies.

CRITICAL INSTRUCTION:
For every response, you MUST output a JSON block wrapped in ```json ... ``` at the very end of your response. 
The JSON block should represent the structured metadata for UI rendering. 

Example JSON structures:
1. Recommendation Card:
```json
{
  "ui_type": "product_card",
  "data": {
    "products": ["Product Name 1", "Product Name 2"],
    "reason": "Detailed reason for recommendation based on client profile."
  }
}
```

2. Normal Text:
```json
{
  "ui_type": "text",
  "data": {
    "content": "Just a normal text response."
  }
}
```
"""

# Initialize LLM and Agent (if key is present)
llm = None
agent_executor = None

if os.getenv("OPENAI_API_KEY"):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

def run_agent(user_input: str, chat_history: list = None):
    if not os.getenv("OPENAI_API_KEY"):
        if mock_run_agent:
            return mock_run_agent(user_input, chat_history)
        return "Error: OPENAI_API_KEY not set and mock_llm not found."

    if chat_history is None:
        chat_history = []
    
    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    
    return response["output"]
