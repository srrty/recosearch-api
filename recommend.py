# recommend.py

import os
import requests
import xml.etree.ElementTree as ET

API_KEY = os.getenv("DBPIA_API_KEY")
XML_URL = "http://api.dbpia.co.kr/v2/search/search.xml"

def recommend_related(query: str, pyear: str, pmonth: str, category: str) -> list[dict]:
    """
    query를 무시하고, pyear+pmonth+category로 인기 논문(rated_art)을 가져옵니다.
    """
    params = {
        "key":    API_KEY,
        "target": "rated_art",
    }
    # pyear, pmonth가 둘 다 있으면 추가
    if pyear and pmonth:
        params["pyear"], params["pmonth"] = pyear, pmonth
    # 주제분류 코드가 있으면 추가
    if category:
        params["category"] = category

    resp = requests.get(XML_URL, params=params)
    resp.raise_for_status()

    # XML 파싱
    root = ET.fromstring(resp.text)
    # 에러 노드 체크
    if root.tag == "error":
        code = root.findtext(".//Code") or "Unknown"
        raise RuntimeError(f"DBpia 오류 코드: {code}")

    items = []
    for node in root.findall(".//item"):
        # 제목
        title = node.findtext("title") or ""
        # 링크
        link  = node.findtext("link_url") or ""
        # 저자 리스트
        authors = []
        for a in node.findall(".//author"):
            name = a.get("name") or a.findtext("name")
            if name:
                authors.append(name)
        items.append({
            "title":   title,
            "link":    link,
            "authors": authors,
        })
    return items
