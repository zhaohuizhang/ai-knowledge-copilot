import os
from dotenv import load_dotenv
load_dotenv()
from database import engine, Base
from rag_utils import init_collection, inject_knowledge, COLLECTION_NAME, connect_milvus, DIMENSION
from mock_llm import MockEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pymilvus import utility

def main():
    # 1. Init MySQL
    print("Initializing MySQL tables...")
    Base.metadata.create_all(bind=engine)
    print("MySQL initialized.")

    # 2. Init Milvus and inject data
    print("Initializing Milvus collection...")
    connect_milvus()
    if utility.has_collection(COLLECTION_NAME):
        print(f"Dropping existing collection {COLLECTION_NAME} for re-initialization...")
        utility.drop_collection(COLLECTION_NAME)
    
    init_collection()
    
    if os.getenv("GOOGLE_API_KEY"):
        print("Using Google embeddings for injection...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI embeddings for injection...")
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()
    else:
        print(f"Using Mock embeddings ({DIMENSION} dim) for injection...")
        embeddings = MockEmbeddings(dimension=DIMENSION)

    mock_texts = [
        "金满钵养老年金：适合50岁以上稳健型客户，长期复利增值，年化收益演示最高达 3.5%。",
        "2025新规重疾险：免赔额大幅降低，针对高风险客户群体放宽投保年龄至 65 岁。",
        "客户经营建议：对于高净值客户，建议定期发送保险资产配置报告，提升服务粘性。",
        "平安E生保2025版：涵盖质子重离子治疗，最高保额达400万，适合家庭全员投保。"
    ]
    
    print("Injecting knowledge into Milvus...")
    inject_knowledge(mock_texts, embeddings)
    print("Milvus initialized and data injected.")

if __name__ == "__main__":
    main()
