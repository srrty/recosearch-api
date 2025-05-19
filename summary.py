<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import pipeline
from langdetect import detect

app = FastAPI()

# 1) 정적 파일 서빙 설정 (static/index.html, .js, .css 등)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# 2) 요약 모델 로드
summarizer_en = pipeline("summarization", model="facebook/bart-large-cnn")
summarizer_ko = pipeline("summarization", model="digit82/kobart-summarization")

class SummaryRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize(req: SummaryRequest):
    text = req.text.strip()
    if not text:
        return {"summary": "❗ 입력된 텍스트가 비어 있습니다."}

    try:
        lang = detect(text)
    except:
        lang = "unknown"

    if lang == "ko":
        out = summarizer_ko(text, max_length=25, min_length=5, do_sample=False)
    else:
        out = summarizer_en(text, max_length=25, min_length=5, do_sample=False)

    return {"language": lang, "summary": out[0]["summary_text"]}
=======
from fastapi import FastAPI, Body
from pydantic import BaseModel
from transformers import pipeline
from langdetect import detect

# FastAPI 앱 객체 생성
app = FastAPI()

# 요약 모델 로드 (한 번만)
summarizer_en = pipeline("summarization", model="facebook/bart-large-cnn")
summarizer_ko = pipeline("summarization", model="digit82/kobart-summarization")

# 요청 바디 구조 정의
class SummaryRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize(req: SummaryRequest):
    text = req.text.strip()
    if not text:
        return {"summary": "❗ 입력된 텍스트가 비어 있습니다."}

    # 언어 감지
    try:
        lang = detect(text)
    except:
        lang = "unknown"

    # 모델 선택 및 요약
    if lang == "ko":
        summary = summarizer_ko(text, max_length=25, min_length=5, do_sample=False)
    else:
        summary = summarizer_en(text, max_length=25, min_length=5, do_sample=False)

    return {
        "language": lang,
        "summary": summary[0]['summary_text']
    }
>>>>>>> c9bb22ce1aa5baaa69882c99f88acef2b9b363da
