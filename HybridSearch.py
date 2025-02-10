from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from MedicalSearch import MedicalSearch
from save import cases, preprocess_case

class HybridSearch:
    def __init__(self):
        self.tfidf = TfidfVectorizer()
        self.texts = [preprocess_case(c) for c in cases]
        self.tfidf_matrix = self.tfidf.fit_transform(self.texts)
    
    def hybrid_search(self, query: str, alpha=0.7):
        # 语义搜索
        semantic_results = MedicalSearch().search(query)
        
        # 关键词搜索
        query_vec = self.tfidf.transform([query])
        keyword_scores = np.dot(query_vec, self.tfidf_matrix.T).toarray()[0]
        
        # 混合排序
        combined_scores = {}
        for idx, score in enumerate(keyword_scores):
            combined_scores[idx] = alpha * score
        
        for res in semantic_results:
            idx = res['case_id'] - 1  # 假设case_id从1开始
            combined_scores[idx] += (1 - alpha) * res['score']
        
        sorted_indices = sorted(combined_scores.items(), 
                              key=lambda x: x[1], 
                              reverse=True)
        
        return [cases[idx] for idx, _ in sorted_indices[:10]]