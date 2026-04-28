from dotenv import load_dotenv
load_dotenv()

from agent import run_agent
import traceback

try:
    print(run_agent("平安银行理财产品推荐", [], "gemini-3"))
except Exception as e:
    print("Error:")
    traceback.print_exc()
