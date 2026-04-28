import json
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool, create_tool_calling_agent, AgentExecutor

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
    if not os.getenv("OPENAI_API_KEY"):
        return "Knowledge base search is currently unavailable (Missing OpenAI API Key for embeddings)."
        
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

You MUST think step-by-step and provide your reasoning before calling any tools.

Example JSON structures:
1. Recommendation Card:
```json
{{
  "ui_type": "product_card",
  "data": {{
    "products": ["Product Name 1", "Product Name 2"],
    "reason": "Detailed reason for recommendation based on client profile."
  }}
}}
```

2. Normal Text:
```json
{{
  "ui_type": "text",
  "data": {{
    "content": "Just a normal text response."
  }}
}}
```
"""

# Cache for agent executors to avoid re-initializing on every request
_agent_cache = {}

def get_agent_executor(model_name: str):
    if model_name in _agent_cache:
        return _agent_cache[model_name]
    
    llm = None
    if "gpt" in model_name.lower():
        if os.getenv("OPENAI_API_KEY"):
            llm = ChatOpenAI(model=model_name, temperature=0)
    elif "gemini" in model_name.lower():
        if os.getenv("GOOGLE_API_KEY"):
            # Using gemini-2.5-flash as it is the most advanced version that supports tool calling 
            # without the mandatory 'thought_signature' requirement of Gemini 3.0+ models in this SDK version.
            actual_model = "gemini-2.5-flash"
            llm = ChatGoogleGenerativeAI(model=actual_model, temperature=0, convert_system_message_to_human=True)
    
    if not llm:
        return None

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)
    _agent_cache[model_name] = executor
    return executor

def run_agent(user_input: str, chat_history: list = None, model_name: str = "gpt-3.5-turbo"):
    if chat_history is None:
        chat_history = []

    # Use mock if explicitly requested or if no API keys are available
    if model_name == "mock" or (not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY")):
        if mock_run_agent:
            return mock_run_agent(user_input, chat_history)
        return "Error: No API keys found and mock_llm not available."

    executor = get_agent_executor(model_name)
    if not executor:
        # Fallback to mock if requested model fails to initialize
        if mock_run_agent:
            return mock_run_agent(user_input, chat_history)
        return f"Error: Failed to initialize model {model_name}."
    
    response = executor.invoke({
        "input": user_input,
        "chat_history": chat_history
    })
    
    return response["output"]
