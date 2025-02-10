from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from database import DatabaseManager
import pickle
import os

class MedicalSearch:
    def __init__(self, model: SentenceTransformer):
        self.model = model
        self.db_manager = DatabaseManager()
        self.cases = []
        self.embeddings = None
        self.load_or_initialize_cases()
    
    def load_or_initialize_cases(self):
        """加载或初始化病例数据"""
        if os.path.exists('data/processed_cases.pkl'):
            self.load_processed_cases()
        else:
            self.initialize_cases()
    
    def initialize_cases(self):
        """从数据库获取并处理病例数据"""
        cases = self.db_manager.get_all_cases()
        processed_cases = []
        
        for case in cases:
            processed_text = self._preprocess_case(case)
            embedding = self.model.encode(processed_text)
            processed_cases.append({
                'case_id': case['case_id'],
                'text': processed_text,
                'embedding': embedding,
                'original_case': case
            })
        
        self.cases = processed_cases
        self.embeddings = np.array([case['embedding'] for case in processed_cases])
        self.save_processed_cases()
    
    def _preprocess_case(self, case: Dict) -> str:
        """处理单个病例文本"""
        return f"""
        症状：{case['symptoms']}
        诊断：{case['diagnosis']}
        治疗：{case['treatment']}
        备注：{case['notes']}
        """
    
    def save_processed_cases(self):
        """保存处理后的病例数据"""
        os.makedirs('data', exist_ok=True)
        with open('data/processed_cases.pkl', 'wb') as f:
            pickle.dump({
                'cases': self.cases,
                'embeddings': self.embeddings
            }, f)
    
    def load_processed_cases(self):
        """加载处理后的病例数据"""
        with open('data/processed_cases.pkl', 'rb') as f:
            data = pickle.load(f)
            self.cases = data['cases']
            self.embeddings = data['embeddings']
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """搜索相似病例"""
        query_embedding = self.model.encode(query)
        
        # 计算相似度
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # 获取最相似的病例
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            case = self.cases[idx]
            results.append({
                'case_id': case['case_id'],
                'similarity': float(similarities[idx]),
                'case_info': case['original_case']
            })
        
        return results 