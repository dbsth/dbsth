# page_processor.py (페이지 처리)
from bs4 import BeautifulSoup

class PageProcessor:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")
    
    def extract_posts(self, selector):
        return self.soup.select(selector)
    
    def has_content(self):
        return bool(self.soup.find())
