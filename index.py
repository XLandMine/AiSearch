from sentence_transformers import SentenceTransformer
import pandas as pd
from database import DatabaseManager

# 初始化数据库管理器
db_manager = DatabaseManager()

# 从数据库获取病例数据
def get_cases():
    return db_manager.get_all_cases()

# 合并文本字段
def preprocess_case(case):
    return f"""
    症状：{case['symptoms']}
    诊断：{case['diagnosis']}
    治疗：{case['treatment']}
    备注：{case['notes']}
    """

# 初始化Embedding模型
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

# 处理所有病例数据
def process_all_cases():
    cases = get_cases()
    processed_cases = []
    
    for case in cases:
        processed_text = preprocess_case(case)
        embedding = model.encode(processed_text)
        processed_cases.append({
            'case_id': case['case_id'],
            'text': processed_text,
            'embedding': embedding
        })
    
    return processed_cases