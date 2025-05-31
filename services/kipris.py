import requests
import os

KIPRIS_API_KEY = os.getenv("KIPRIS_API_KEY")

def fetch_patents(pyear, pmonth, category):
    # 특허 API 포맷에 맞는 URL 구성
    url = f"https://openapi.kipris.or.kr/openapi/service/kpat/kpatSearchInfoSearchService/getKpatListSearch"
    params = {
        "ServiceKey": KIPRIS_API_KEY,
        "applicationDate": f"{pyear}{str(pmonth).zfill(2)}",
        "inventionTitle": category,
        "numOfRows": 10,
        "pageNo": 1,
    }
    response = requests.get(url, params=params)
    return {"patents": response.text}  # 테스트 중엔 JSON 파싱 전 응답 원문 반환
