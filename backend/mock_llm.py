import json
import re

class MockChatOpenAI:
    def __init__(self, model, temperature):
        self.model = model
        self.temperature = temperature

    def invoke(self, messages):
        # A very simple mock that detects keywords and returns pre-defined responses with metadata
        # In a real tool-based agent, this would be more complex, but for joint debugging, 
        # we can simulate the final output of the AgentExecutor.
        pass

class MockEmbeddings:
    def embed_documents(self, texts):
        return [[0.1] * 1536 for _ in texts]
    
    def embed_query(self, query):
        return [0.1] * 1536

def mock_run_agent(user_input, chat_history=None):
    user_input = user_input.lower()
    
    if "你好" in user_input or "hello" in user_input:
        content = "你好！我是你的保险知识助手。请问有什么我可以帮您的？"
        metadata = {"ui_type": "text", "data": {"content": content}}
    elif "张三" in user_input and "画像" in user_input:
        content = "为您查询到张三的客户画像：35岁，已婚，有一个孩子，目前年收入约 50w，偏好稳健型投资。"
        metadata = {"ui_type": "text", "data": {"content": content}}
    elif "推荐" in user_input or "金满钵" in user_input:
        content = "根据客户的情况，我为您推荐‘金满钵养老年金’。这款产品收益稳定，非常符合客户的风险偏好。"
        metadata = {
            "ui_type": "product_card",
            "data": {
                "products": ["金满钵养老年金"],
                "reason": "客户属于稳健型投资者，金满钵提供复利增值，且支持灵活领用，适合其家庭养老储备。"
            }
        }
    else:
        content = f"我已经收到您的消息：'{user_input}'。目前正在为您查询相关政策信息。"
        metadata = {"ui_type": "text", "data": {"content": content}}
    
    # Format the output as expected by main.py (including the JSON block)
    return f"{content}\n\n```json\n{json.dumps(metadata, ensure_ascii=False, indent=2)}\n```"
