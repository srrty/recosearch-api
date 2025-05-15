import requests
import xml.etree.ElementTree as ET

def search_documents(keyword: str, api_key: str, page: int = 1, count: int = 10) -> list[dict]:
    url = "http://api.dbpia.co.kr/v2/search/search.xml"
    params = {
        "key": api_key,
        "target": "se",
        "searchall": keyword,
        "page": page,
        "count": count
    }
    resp = requests.get(url, params=params, timeout=10.0)
    resp.raise_for_status()

    root = ET.fromstring(resp.text)
    items = []
    for item in root.findall(".//item"):
        title = item.findtext("title") or ""
        link = item.findtext("link_url") or ""
        lang = "ko" if any("\uAC00" <= ch <= "\uD7AF" for ch in title) else "en"
        items.append({"title": title, "link": link, "language": lang})
    return items
