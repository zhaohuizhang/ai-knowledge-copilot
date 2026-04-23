import os
import time
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

# Milvus Config
MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
COLLECTION_NAME = "insurance_knowledge"
DIMENSION = 1536 # Example for OpenAI text-embedding-3-small

def connect_milvus():
    connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

def init_collection():
    connect_milvus()
    if utility.has_collection(COLLECTION_NAME):
        return Collection(COLLECTION_NAME)
    
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="timestamp", dtype=DataType.INT64), # For timestamp filtering
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
    ]
    schema = CollectionSchema(fields, "Insurance Knowledge Base")
    collection = Collection(COLLECTION_NAME, schema)
    
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 1024}
    }
    collection.create_index(field_name="vector", index_params=index_params)
    return collection

def simulate_pdf_parsing(file_path: str):
    """
    Task 3.1: Simulate third-party parsing of PDF and tables.
    """
    print(f"Simulating parsing of {file_path} using 3rd party tool...")
    return [
        "金满钵养老年金：适合50岁以上稳健型客户，长期复利增值，年化收益演示最高达 3.5%。",
        "2025新规重疾险：免赔额大幅降低，针对高风险客户群体放宽投保年龄至 65 岁。"
    ]

def inject_knowledge(texts: list, embeddings_model):
    """
    Task 3.2: Inject parsed texts with timestamp metadata.
    """
    collection = init_collection()
    
    vectors = embeddings_model.embed_documents(texts)
    
    current_ts = int(time.time())
    timestamps = [current_ts] * len(texts)
    
    data = [
        texts,
        timestamps,
        vectors
    ]
    
    collection.insert(data)
    collection.flush()
    print("Knowledge injected successfully.")

def search_knowledge(query: str, embeddings_model, top_k=3, min_timestamp=0):
    """
    Task 3.3: Retrieve knowledge from Milvus with metadata filtering.
    """
    collection = init_collection()
    collection.load()
    
    query_vector = embeddings_model.embed_query(query)
    
    # Metadata filtering based on timestamp
    expr = f"timestamp >= {min_timestamp}"
    
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(
        data=[query_vector],
        anns_field="vector",
        param=search_params,
        limit=top_k,
        expr=expr,
        output_fields=["text", "timestamp"]
    )
    
    retrieved_texts = []
    for hits in results:
        for hit in hits:
            retrieved_texts.append(hit.entity.get('text'))
            
    return retrieved_texts
