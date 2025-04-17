# url_builder.py (URL 생성기)
from urllib.parse import urlparse, parse_qs, urlencode

class URLBuilder:
    @staticmethod
    def build_paginated_url(base_url, page, items_per_page=10):
        # URL 구문 분석
        parsed = urlparse(base_url)
        
        # 쿼리 파라미터 추출 및 수정
        query = parse_qs(parsed.query)
        query["article.offset"] = [str(page * items_per_page)]
        query["articleLimit"] = [str(items_per_page)]
        
        # 새로운 쿼리 문자열 생성
        new_query = urlencode(query, doseq=True)
        
        # 수정된 URL 반환
        return parsed._replace(query=new_query).geturl()