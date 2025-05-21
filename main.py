# main.py

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from recommend import recommend_related

# 1) 환경 변수 로드 & 키 검증
load_dotenv()
if not os.getenv("DBPIA_API_KEY"):
    raise RuntimeError("환경변수 DBPIA_API_KEY가 설정되어 있지 않습니다.")

# 2) FastAPI 앱 생성
app = FastAPI(title="Recosearch API")

# 3) /recommend API 라우트 (StaticFiles 전에 정의)
@app.get("/recommend")
async def recommend(query: str = "", pyear: str = "", pmonth: str = "", subject_cd: str = ""):
    try:
        papers = recommend_related(query, pyear, pmonth, subject_cd)
        return JSONResponse(content=papers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4) static 폴더를 "/"에 마운트 (fallback)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/",
    StaticFiles(directory=os.path.join(BASE_DIR, "static"), html=True),
    name="static"
)

