import os
from database import engine, Base
from rag_utils import init_collection, inject_knowledge
from mock_llm import MockEmbeddings

def main():
    # 1. Init MySQL
    print("Initializing MySQL tables...")
    Base.metadata.create_all(bind=engine)
    print("MySQL initialized.")

    # 2. Init Milvus and inject data
    print("Initializing Milvus collection...")
    init_collection()
    
    mock_texts = [
        "金满钵养老年金：适合50岁以上稳健型客户，长期复利增值，年化收益演示最高达 3.5%。",
        "2025新规重疾险：免赔额大幅降低，针对高风险客户群体放宽投保年龄至 65 岁。",
        "客户经营建议：对于高净值客户，建议定期发送保险资产配置报告，提升服务粘性。",
        "平安E生保2025版：涵盖质子重离子治疗，最高保额达400万，适合家庭全员投保。"
    ]
    
    print("Injecting mock knowledge into Milvus...")
    inject_knowledge(mock_texts, MockEmbeddings())
    print("Milvus initialized and data injected.")

if __name__ == "__main__":
    main()
