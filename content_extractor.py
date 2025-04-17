# web_crawler/content_extractor.py
from datetime import datetime
from bs4 import BeautifulSoup

class ContentExtractor:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")

    def generate_post_dict(self):
        """기본적인 정보 딕셔너리를 생성합니다."""
        return {}