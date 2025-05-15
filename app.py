import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from search import search_documents
from translate import translate_to_korean
from recommend import recommend_related
from database import init_db, save_search

# 환경변수 로드
load_dotenv()
DBPIA_API_KEY = os.getenv("DBPIA_API_KEY")
DB_PATH        = os.getenv("DB_PATH", "searches.db")
if not DBPIA_API_KEY:
    raise RuntimeError("환경변수 DBPIA_API_KEY가 설정되어 있지 않습니다.")

# DB 초기화 (최초 1회만 수행됩니다)
init_db(DB_PATH)

# FastAPI 인스턴스 이름은 반드시 `app`이어야 uvicorn이 찾습니다
app = FastAPI(title="Recosearch API")

# 요청·응답 모델 정의
class SearchRequest(BaseModel):
    keyword: str

class Document(BaseModel):
    title: str
    link: str
    language: str

class SearchResponse(BaseModel):
    results: list[Document]
    recommendations: list[str]

@app.get("/", response_model=dict)
async def root():
    return {"message": "API가 정상적으로 작동 중입니다!"}

@app.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest):
    keyword = req.keyword.strip()
    if not keyword:
        raise HTTPException(400, "keyword를 전달해주세요.")

    # 1) 논문 검색
    try:
        results = search_documents(keyword, DBPIA_API_KEY)
    except Exception as e:
        raise HTTPException(500, f"검색 실패: {e}")

    # 2) 번역
    for r in results:
        if r["language"] != "ko":
            r["title"] = translate_to_korean(r["title"])

    # 3) 검색 기록 저장
    save_search(keyword, results, DB_PATH)

    # 4) 연관 추천
    recs = recommend_related(keyword, DB_PATH)

    return {"results": results, "recommendations": recs}
