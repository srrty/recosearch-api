# recommend.py

import os
import requests
import xml.etree.ElementTree as ET

API_KEY = os.getenv("DBPIA_API_KEY")
RECOMMEND_XML = "http://api.dbpia.co.kr/v2/search/search.xml"

def recommend_related(query: str, pyear: str, pmonth: str, category: str):
    # 오직 추천 API만 사용
    params = {"key": API_KEY, "target": "rated_art"}
    if pyear and pmonth:
        params["pyear"], params["pmonth"] = pyear, pmonth
    if category:
        params["category"] = category

    resp = requests.get(RECOMMEND_XML, params=params)
    resp.raise_for_status()

    root = ET.fromstring(resp.text)
    items = []
    for node in root.findall(".//item"):
        # 필요한 필드만 추출
        items.append({
            "title": node.findtext("title"),
            "link":  node.findtext("link_url"),
            "authors": [a.get("name") for a in node.findall(".//author")]
        })
    return items
