import os
import requests
from dotenv import load_dotenv

# 환경 변수 로드
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv("DBPIA_API_KEY")
ENDPOINT = "https://api.dbpia.co.kr/v1/search"

def fetch_recommendations(year, month, category):
    """
    DBpia API를 호출해 문헌 추천 데이터를 가져옵니다.
    404 응답은 빈 리스트로 처리합니다.
    year, month가 None일 경우 해당 파라미터를 제외하고 호출합니다.
    """
    params = {}
    if year is not None:
        params["year"] = year
    if month is not None:
        params["month"] = f"{month:02d}"
    if category is not None:
        params["category"] = category
    headers = {"apikey": API_KEY}
    try:
        resp = requests.get(ENDPOINT, headers=headers, params=params)
        if resp.status_code == 404:
            return []
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] DBpia HTTP error: {e}")
        raise
    data = resp.json()
    items = []
    for doc in data.get("documents", []):
        items.append({
            "title": doc.get("title"),
            "authors": [{"name": a} for a in doc.get("authors", [])],
            "publication": {"name": doc.get("journal", "")},
            "link_url": doc.get("url")
        })
    return items
