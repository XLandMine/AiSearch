from index import process_all_cases
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer

class MedicalSearch:
    def __init__(self, model: SentenceTransformer):
        self.model = model
        self.cases = []
        self.embeddings = None
        self.initialize_cases()
    
    def initialize_cases(self):
        """初始化病例数据"""
        processed_cases = process_all_cases()
        self.cases = processed_cases
        self.embeddings = np.array([case['embedding'] for case in processed_cases])
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        搜索相似病例
        
        Args:
            query: 搜索查询文本
            top_k: 返回最相似的结果数量
            
        Returns:
            List[Dict]: 相似病例列表
        """
        # 编码查询文本
        query_embedding = self.model.encode(query)
        
        # 计算相似度
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # 获取最相似的病例索引
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # 返回结果
        results = []
        for idx in top_indices:
            case = self.cases[idx]
            results.append({
                'case_id': case['case_id'],
                'text': case['text'],
                'similarity': float(similarities[idx])
            })
            
        return results