# crawler_config.py (설정 관리)
import json
from urllib.parse import urlparse, parse_qs

class ConfigLoader:
    @staticmethod
    def load_urls(file_path):
        # JSON 파일에서 URL 목록을 로드합니다
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        if "urls" in data:
            return data["urls"]
        elif "url" in data:
            return [data["url"]]
        raise ValueError("JSON 파일에 'url' 또는 'urls' 키가 없습니다")
