import mysql.connector
from mysql.connector import Error
from typing import List, Dict
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DatabaseManager:
    def __init__(self):
        # 从环境变量获取数据库配置
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'medical_cases'),
        }
        self.connection = None
        
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            print("数据库连接成功")
        except Error as e:
            print(f"数据库连接错误: {e}")
            
    def disconnect(self):
        """关闭数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("数据库连接已关闭")
            
    def get_all_cases(self) -> List[Dict]:
        """获取所有病例信息"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    case_id,
                    symptoms,
                    diagnosis,
                    treatment,
                    notes
                FROM medical_cases
            """
            cursor.execute(query)
            cases = cursor.fetchall()
            cursor.close()
            return cases
            
        except Error as e:
            print(f"获取病例数据错误: {e}")
            return [] 