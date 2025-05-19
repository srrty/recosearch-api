import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="Recosearch API")

# 1) 기존 정적 서빙 (optional)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# 2) 루트 요청 시 index.html 반환
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))
