import os
import sys
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer
from medical_search import MedicalSearch
import json
from database import DatabaseManager

class MockDatabaseManager(DatabaseManager):
    def __init__(self):
        super().__init__()
        self.mock_cases = self.load_mock_cases()
    
    def load_mock_cases(self):
        try:
            with open('data/mock_cases.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("未找到模拟数据文件，请先运行 generate_mock_data.py")
            return []
    
    def get_all_cases(self):
        """覆盖原方法，返回模拟数据"""
        return self.mock_cases

class MockMedicalSearch(MedicalSearch):
    def __init__(self, model: SentenceTransformer):
        self.model = model
        self.db_manager = MockDatabaseManager()  # 使用模拟数据管理器
        self.cases = []
        self.embeddings = None
        self.load_or_initialize_cases()

def main():
    """处理并保存病例数据的命令行工具"""
    print("开始处理模拟病例数据...")
    
    # 初始化模型和搜索系统
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    # search_system = MedicalSearch(model)
    search_system = MockMedicalSearch(model)
    
    # 强制重新初始化病例数据
    search_system.initialize_cases()
    
    print("模拟病例数据处理完成并保存")

if __name__ == "__main__":
    main() 