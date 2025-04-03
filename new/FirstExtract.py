import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import json
import os
import datetime

# 크롤링할 공지사항 URL (게시글 상세보기)
url = "https://cse.kangwon.ac.kr/cse/community/undergraduate-notice.do?mode=view&articleNo=477622&article.offset=0&articleLimit=10#!/list"

# 웹페이지 가져오기
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")

# 공지사항 데이터 저장 리스트
notices_data = []

# 공지 제목
title_tag = soup.select_one("p.b-title-box span:nth-of-type(2)")
title = title_tag.text.strip() if title_tag else "제목 없음"

# 게시 날짜
date_tag = soup.select_one("div.b-etc-box li.b-date-box")
date = re.sub(r"작성일\s*", "", date_tag.text.strip()) if date_tag else "날짜 없음"

# 공지 내용
content_tag = soup.select_one("div.b-content-box div.fr-view")
if content_tag:
    content = re.sub(r"\s+", " ", content_tag.text.strip())  # 여러 개의 공백을 하나로
    content = content.replace("\u00a0", " ")  # `NBSP` 제거
else:
    content = "내용 없음"

# JSON 형식의 데이터 구조
notice_data = {
    "title": title,
    "date": date,
    "content": content,
    "last_crawled": datetime.datetime.now(datetime.UTC).isoformat(),
    "status": "active",
    "crawl_frequency": "daily",
    "crawl_timeout": 30,
    "crawl_delay": 5
}

notices_data.append(notice_data)

# JSON 파일로 저장
with open("notices.json", "w", encoding="utf-8") as f:
    json.dump(notices_data, f, ensure_ascii=False, indent=4)

print("notices.")