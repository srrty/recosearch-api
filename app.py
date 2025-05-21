import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="Recosearch API")

# 지금처럼 "/static" 이 아니라, "/" 에 바로 마운트
app.mount(
    "/",
    StaticFiles(directory=os.path.join(BASE_DIR, "static"), html=True),
    name="static"
)


# 2) 루트 요청 시 index.html 반환
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "static", "index.html"))
