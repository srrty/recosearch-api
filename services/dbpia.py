# services/dbpia.py

import os
import requests
import xml.etree.ElementTree as ET
from models.paper import Recommendation, RecommendationResponse

# 환경변수에서 API 키 읽기
API_KEY = os.getenv("DBPIA_API_KEY")
if not API_KEY:
    raise RuntimeError("DBPIA_API_KEY 환경변수가 설정되지 않았습니다.")

# DBpia XML API 엔드포인트
DBPIA_URL = "http://api.dbpia.co.kr/v2/search/search.xml"


def fetch_recommendations(
    pyear: str = "",
    pmonth: str = "",
    category: str = "",
    page: int = 1,
    per_page: int = 20,
) -> RecommendationResponse:
    """
    DBpia API를 호출하여 추천 논문 데이터를 가져옵니다.

    :param pyear: 연도(YYYY)
    :param pmonth: 월(MM)
    :param category: 주제 코드
    :param page: 페이지 번호 (1부터 시작)
    :param per_page: 페이지당 결과 수
    :return: RecommendationResponse 객체
    """
    # 1) 파라미터 설정
    params = {
        "key": API_KEY,
        "target": "rated_art",
        "page": str(page),
        "perPage": str(per_page),
    }
    if pyear:
        params.update({"pyear": pyear, "pmonth": pmonth})
    if category:
        params["category"] = category

    # 2) API 호출 (타임아웃 설정)
    resp = requests.get(DBPIA_URL, params=params, timeout=5)
    resp.raise_for_status()

    # 3) XML 파싱
    root = ET.fromstring(resp.text)
    if root.tag == "error":
        code = root.findtext(".//Code") or "Unknown"
        # E0016: 검색 결과 없음 → 빈 응답
        if code == "E0016":
            return RecommendationResponse(
                totalcount=0,
                pyymm=None,
                recommendations=[]
            )
        # 그 외 오류는 예외로 처리
        raise RuntimeError(f"DBpia 오류 코드: {code}")

    # 4) 데이터 추출
    totalcount = int(root.findtext(".//totalcount") or 0)
    pyymm = root.findtext(".//pyymm")

    items = []
    for node in root.findall(".//item"):
        # authors 파싱
        authors = []
        ap = node.find("authors")
        if ap is not None:
            for a in ap.findall("author"):
                name = a.get("name") or a.findtext("name")
                if name:
                    authors.append({
                        "order": a.get("order"),
                        "url": a.get("url"),
                        "name": name
                    })
            if not authors and ap.text:
                for nm in ap.text.split(","):
                    nm = nm.strip()
                    if nm:
                        authors.append({"order": None, "url": None, "name": nm})

        # publisher 파싱
        pubr = node.find("publisher")
        publisher = {
            "url": (pubr.get("url") if pubr is not None else None) or (pubr.findtext("url") if pubr is not None else None),
            "name": (pubr.get("name") if pubr is not None else None) or (pubr.findtext("name") if pubr is not None else None)
        }

        # publication 파싱
        publ = node.find("publication")
        publication = {
            "url": (publ.get("url") if publ is not None else None) or (publ.findtext("url") if publ is not None else None),
            "name": (publ.get("name") if publ is not None else None) or (publ.findtext("name") if publ is not None else None)
        }

        # 기타 필드
        items.append({
            "title": node.findtext("title"),
            "authors": authors,
            "publisher": publisher,
            "publication": publication,
            "issue_yymm": node.findtext("issue_yymm"),
            "pages": node.findtext("pages"),
            "free_yn": node.findtext("free_yn"),
            "price": node.findtext("price"),
            "preview_yn": node.findtext("preview_yn"),
            "preview": node.findtext("preview"),
            "link_url": node.findtext("link_url"),
            "link_api": node.findtext("link_api")
        })

    # 5) Pydantic 모델로 반환
    recs = [Recommendation(**item) for item in items]
    return RecommendationResponse(
        totalcount=totalcount,
        pyymm=pyymm,
        recommendations=recs
    )
