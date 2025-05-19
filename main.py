from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ✅ 먼저 추천 API를 등록
@app.get("/recommend")
async def recommend(pyear: str = "", pmonth: str = "", subject_cd: str = ""):
    mock_data = [
        {
            "title": "인공지능을 활용한 추천 시스템 연구",
            "authors": "김철수, 이영희",
            "link": "https://example.com/paper1"
        },
        {
            "title": "딥러닝을 이용한 자연어처리 최신 동향",
            "authors": "박지훈",
            "link": "https://example.com/paper2"
        }
    ]
    return JSONResponse(content=mock_data)

# ✅ 마지막에 정적 파일 mount
app.mount("/", StaticFiles(directory="static", html=True), name="static")
