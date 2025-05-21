# search.py
import os
import requests

DBPIA_API_KEY = os.getenv("bc68bf65d0e5e2f183604d447ba5ea7e")
SEARCH_URL = "http://api.dbpia.co.kr/v2/search/search.json"

def search_documents(query: str, pyear: str = "", pmonth: str = "", subject_cd: str = "") -> list[dict]:
    """
    DBpia Open API 를 호출해서 검색 결과 리스트를 반환.
    """
    params = {
        "key": DBPIA_API_KEY,
        "target": "se",
        "searchall": query,
        "pyear": pyear,
        "pmonth": pmonth,
        "subject_cd": subject_cd,
        "currpage": 1,
        "rows": 10,
    }
    resp = requests.get(SEARCH_URL, params=params)
    resp.raise_for_status()
    data = resp.json()

    # JSON 구조에 맞춰 결과 item 추출
    items = data.get("item", [])  # 혹은 data.get("result", {}).get("item", [])
    results = []
    for it in items:
        results.append({
            "title": it.get("title") or it.get("ARTICLETITLE"),
            "authors": it.get("author") or it.get("authors"),
            "link": it.get("article_link") or it.get("link"),
        })
    return results
