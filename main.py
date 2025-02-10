from fastapi import FastAPI
from pydantic import BaseModel
from medical_search import MedicalSearch
from sentence_transformers import SentenceTransformer

app = FastAPI(title="医疗病例搜索系统")

# 初始化搜索系统
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
search_system = MedicalSearch(model)

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@app.post("/search")
async def search_cases(request: SearchRequest):
    """
    搜索相似病例
    
    参数:
        - query: 查询文本（症状描述等）
        - top_k: 返回结果数量
    """
    results = search_system.search(request.query, request.top_k)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 