# routers/summary.py
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/summary")
def get_summary(paper_id: int = Query(..., ge=1)):
    url = f"https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE{paper_id}"
    res = requests.get(url, timeout=5)
    soup = BeautifulSoup(res.text, "html.parser")

    topic = "정보 없음"
    for dl in soup.find_all("dl"):
        dt = dl.find("dt")
        if dt and "연구주제" in dt.text:
            dd = dl.find("dd")
            topic = dd.text.strip() if dd else "정보 없음"
            break

    return {"research_topic": topic}
