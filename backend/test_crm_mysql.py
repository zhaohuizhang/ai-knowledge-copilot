from dotenv import load_dotenv
import os
load_dotenv()

from agent import run_agent
import traceback

# Ensure we use a model that supports tool calling
# Based on agent.py, gemini-2.5-flash is used for 'gemini' model name
model = "gemini"

test_prompts = [
    "帮我查一下张三的画像",
    "帮我看看王五的情况，根据他的画像推荐一款保险"
]

for prompt in test_prompts:
    print(f"\n--- Testing Prompt: {prompt} ---")
    try:
        response = run_agent(prompt, [], model)
        print("Agent Response:")
        print(response)
    except Exception as e:
        print(f"Error for prompt '{prompt}':")
        traceback.print_exc()
