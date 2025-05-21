import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List

# 기준 디렉터리 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# FastAPI 앱 생성
app = FastAPI(title="Recosearch API")

# CORS 허용 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 서비스에서는 정확한 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 임시 논문 데이터 생성 함수
def get_mock_papers(query: str, pyear: str = '', pmonth: str = '') -> List[dict]:
    return [
        {
            "title": f"[{query}] 관련 최신 논문 A ({pyear}/{pmonth})",
            "authors": "홍길동, 김철수",
            "link": "https://example.com/paper1"
        },
        {
            "title": f"[{query}] 관련 논문 B ({pyear}/{pmonth})",
            "authors": "이영희",
            "link": "https://example.com/paper2"
        }
    ]

# 추천 엔드포인트
from fastapi.responses import JSONResponse

@app.get("/recommend")
async def recommend(query: str = "", pyear: str = "", pmonth: str = ""):
    mock_data = [
        {"title": "인공지능을 활용한 추천 시스템 연구", "authors": "김철수", "link": "#"},
        {"title": "딥러닝을 이용한 자연어처리 동향", "authors": "이영희", "link": "#"},
    ]
    return JSONResponse(content=mock_data)


# 루트 요청 시 index.html 반환
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))

# 정적 파일(`/static` 경로) 서빙
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

