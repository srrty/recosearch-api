# search.py

import os
import requests

DBPIA_API_KEY = os.getenv("DBPIA_API_KEY")
SEARCH_URL = "http://api.dbpia.co.kr/v2/search/search.json"

def search_documents(query: str, pyear: str = "", pmonth: str = "", subject_cd: str = "") -> list[dict]:
    params = {
        "key":       DBPIA_API_KEY,
        "target":    "se",
        "searchall": query,
        "currpage":  1,
        "rows":      10,
    }
    if pyear and pmonth:
        params["pyear"], params["pmonth"] = pyear, pmonth
    if subject_cd:
        params["subject_cd"] = subject_cd

    resp = requests.get(SEARCH_URL, params=params)
    resp.raise_for_status()

    try:
        data = resp.json()
    except ValueError:
        return []

    # data가 리스트인지 dict인지 구분
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get("item") or data.get("result", {}).get("item") or []
    else:
        items = []

    results = []
    for it in items:
        if not isinstance(it, dict):
            continue
        results.append({
            "title":   it.get("title") or it.get("ARTICLETITLE"),
            "authors": it.get("author") or it.get("authors"),
            "link":    it.get("link") or it.get("article_link"),
        })
    return results
