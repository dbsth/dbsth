# web_crawler/post_extractor.py
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import re
from crawler_utils import CrawlerUtils

class PostExtractor:
    def __init__(self, base_url="https://cse.kangwon.ac.kr"):
        self.base_url = base_url

    def extract_article_no(self, url, site=None):
        """URL에서 게시물 번호를 추출합니다. site 정보에서 파라미터 키를 가져올 수 있습니다."""
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        article_id_param = site.get("article_id_param", "articleNo") if site else "articleNo"
        return query.get(article_id_param, [None])[0]

    def extract_post_data(self, post_url, html_content, site):
        """HTML 내용과 사이트 설정에서 게시물 상세 정보를 추출합니다."""
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            title_selector = site.get("title_path")
            title_tag = soup.select_one(title_selector)
            title = title_tag.get_text(strip=True) if title_tag else None
            # print(f"    📜 제목: {title}")

            writer_selector = site.get("writer_path")
            writer_tag = soup.select_one(writer_selector)
            author = writer_tag.text.strip() if writer_tag else None
            # print(f"    ✍️ 작성자: {author}")

            date_selector = site.get("date_path")
            date_tag = soup.select_one(date_selector)
            date = date_tag.text.strip() if date_tag else None
            # print(f"    📅 날짜: {date}")
            
            content_selector = site.get("content_path")
            content_tag = soup.select_one(content_selector)
            if content_tag:
                content = re.sub(r"\s+", " ", content_tag.text.strip())  # 여러 개의 공백을 하나로
                content = content.replace("\u00a0", " ")  # `NBSP` 제거
            else:
                content = "no content"
            # print(f"    📄 내용: {content[:10]}")

            attachment_selector = site.get("attachment_path")
            attachment_tags = soup.select(attachment_selector)
            attachments = [CrawlerUtils.get_full_url(self.base_url, a['href'])
                           for a in attachment_tags if a.has_attr('href')]
            # print(f"    📎 첨부파일: {attachments}")

            articleNo = self.extract_article_no(post_url, site)

            return {
                "title": title,
                "date": date,
                "author": author,
                "articleNo": articleNo,
                "content": content,
                "link": post_url,
                "attachments": attachments,
                "university": site.get('university'),
                "department": site.get('department')
            }
        except Exception as e:
            print(f"❌ 게시물 데이터 추출 실패: {post_url} - {str(e)}")
            return None