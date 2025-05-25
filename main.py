from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers.health import router as health_router
from routers.recommend import router as recommend_router
from routers.paper import router as paper_router
from routers.auth import router as auth_router
from routers.mypage import router as mypage_router

# 슬래시 자동 리디렉션 비활성화
app = FastAPI(redirect_slashes=False)

# 라우터 등록 (prefix는 routers에서 설정)
app.include_router(health_router)
app.include_router(recommend_router)
app.include_router(paper_router)
app.include_router(auth_router)
app.include_router(mypage_router)

# 정적 파일 제공
app.mount("/static", StaticFiles(directory="static"), name="static")

# SPA 진입점
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse("static/index.html")

# Uvicorn 실행 지원
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
