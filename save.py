import numpy as np
from qdrant_client import QdrantClient
from index import process_all_cases, model
import pickle

# 生成向量并存储
client = QdrantClient("localhost", port=6333)

vectors = []
payloads = []
for case in process_all_cases():
    text = case
    vector = model.encode(text).tolist()
    vectors.append(vector)
    payloads.append(case)

# 创建向量数据库集合
client.recreate_collection(
    collection_name="medical_cases",
    vector_size=768  # 根据模型输出维度调整
)

# 批量插入数据
client.upsert(
    collection_name="medical_cases",
    points=[
        {
            "id": idx, 
            "vector": vector,
            "payload": payload
        } for idx, (vector, payload) in enumerate(zip(vectors, payloads))
    ]
)

def save_processed_cases(output_file='processed_cases.pkl'):
    """
    处理并保存所有病例数据
    """
    # 获取处理后的病例数据
    processed_cases = process_all_cases()
    
    # 保存处理后的数据
    with open(output_file, 'wb') as f:
        pickle.dump(processed_cases, f)
    
    print(f"已保存 {len(processed_cases)} 条处理后的病例数据到 {output_file}")

def load_processed_cases(input_file='processed_cases.pkl'):
    """
    加载处理后的病例数据
    """
    try:
        with open(input_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print(f"找不到文件 {input_file}，请先运行 save_processed_cases()")
        return []