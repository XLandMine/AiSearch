import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import random
from typing import List, Dict

# 模拟数据的基础数据集
SYMPTOMS = [
    "发热", "咳嗽", "头痛", "乏力", "咽痛", "腹痛", "呕吐", "腹泻", "胸闷", "气短",
    "肌肉酸痛", "关节疼痛", "盗汗", "食欲不振", "恶心", "头晕", "心悸", "胸痛"
]

DIAGNOSES = [
    "上呼吸道感染", "病毒性感冒", "细菌性肺炎", "支气管炎", "胃炎", "肠胃炎",
    "过敏性鼻炎", "偏头痛", "焦虑症", "高血压", "冠心病", "胃溃疡", "结肠炎"
]

TREATMENTS = [
    "抗生素治疗", "对症支持治疗", "止痛药物", "消炎药物", "退烧药物", "输液治疗",
    "卧床休息", "饮食调理", "中药治疗", "物理治疗", "心理疗法"
]

def generate_case(case_id: int) -> Dict:
    # 随机选择2-4个症状组合
    num_symptoms = random.randint(2, 4)
    symptoms = random.sample(SYMPTOMS, num_symptoms)
    
    # 随机选择1-2个诊断
    num_diagnoses = random.randint(1, 2)
    diagnoses = random.sample(DIAGNOSES, num_diagnoses)
    
    # 随机选择2-3个治疗方案
    num_treatments = random.randint(2, 3)
    treatments = random.sample(TREATMENTS, num_treatments)
    
    # 生成随机体温
    temperature = round(random.uniform(36.5, 39.5), 1)
    
    return {
        "case_id": case_id,
        "symptoms": "、".join(symptoms),
        "diagnosis": "、".join(diagnoses),
        "treatment": "、".join(treatments),
        "notes": f"体温{temperature}度，" + random.choice([
            "病情稳定", "需要继续观察", "建议复查", "症状有所改善",
            "病情有待进一步观察", "建议进一步检查"
        ])
    }

def generate_mock_cases(num_cases: int = 100) -> List[Dict]:
    return [generate_case(i+1) for i in range(num_cases)]

def main():
    # 生成100条模拟病例数据
    mock_cases = generate_mock_cases(100)
    
    # 保存到JSON文件
    with open('data/mock_cases.json', 'w', encoding='utf-8') as f:
        json.dump(mock_cases, f, ensure_ascii=False, indent=2)
    
    print(f"已生成 {len(mock_cases)} 条模拟病例数据")

if __name__ == "__main__":
    import os
    os.makedirs('data', exist_ok=True)
    main() 