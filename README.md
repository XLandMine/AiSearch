# 医疗病例相似度搜索系统

这是一个基于语义向量的医疗病例搜索系统，可以根据输入的症状描述找到相似的历史病例。

## 安装说明

1. 确保已安装Python 3.7+

2. 克隆项目后，安装依赖：

```bash
pip install -r requirements.txt
```

## 项目结构

AiSearch/
├── init.py
├── main.py # FastAPI服务器入口
├── medical_search.py # 搜索核心实现
├── database.py # 数据库访问层
├── .gitignore # Git忽略配置
├── data/ # 数据目录（不提交到Git）
│ └── mock_cases.json # 模拟病例数据
└── tools/ # 工具脚本
├── generate_mock_data.py # 生成模拟数据
└── process_cases.py # 处理病例数据

## 数据目录说明

项目的`data/`目录用于存储：
- 模拟病例数据 (mock_cases.json)
- 处理后的向量数据 (processed_cases.pkl)
- 其他临时数据文件

注意：这些数据文件不会提交到Git仓库，需要在首次运行时通过脚本生成。

## 使用说明

1. 首次使用需要生成模拟数据（或配置实际数据库）：

```bash
python tools/generate_mock_data.py
```

2. 处理病例数据（生成向量索引）：

```bash
python tools/process_cases.py
```

3. 启动FastAPI服务器：

```bash
python main.py
```

4. 访问API：
- API文档：http://localhost:8000/docs
- 搜索接口：POST http://localhost:8000/search

## API示例

搜索相似病例：

```bash
curl -X POST "http://localhost:8000/search" -H "Content-Type: application/json" -d '{"query": "持续发热、咳嗽、呼吸困难"}'
```

## 环境变量配置

创建`.env`文件并配置以下变量：
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=medical_cases

## 数据库配置

如果使用实际数据库，需要创建以下表结构：

```sql
CREATE TABLE medical_cases (
case_id INT PRIMARY KEY AUTO_INCREMENT,
symptoms TEXT NOT NULL,
diagnosis VARCHAR(255) NOT NULL,
treatment TEXT NOT NULL,
notes TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 开发说明

- 使用`sentence-transformers`进行文本向量化
- 支持中文医疗文本处理
- 使用余弦相似度计算病例相似度
- 支持模拟数据和实际数据库两种模式

## 注意事项

1. 首次运行时需要下载预训练模型，请确保网络连接正常
2. 处理大量病例数据时可能需要较长时间
3. 建议在生产环境使用实际数据库而不是模拟数据