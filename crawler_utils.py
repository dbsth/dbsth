# crawler_utils.py (유틸리티 함수)
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

class CrawlerUtils:
    @staticmethod
    def get_full_url(base_url, path):
        return urljoin(base_url, path)

    @staticmethod
    def make_request(url, timeout=30):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise ConnectionError(f"Request failed: {e}")
