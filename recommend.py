# recommend.py
from search import search_documents

def recommend_related(query: str, pyear: str = "", pmonth: str = "", subject_cd: str = "") -> list[dict]:
    # 지금은 단순히 검색 결과를 그대로 리턴
    return search_documents(query, pyear, pmonth, subject_cd)

