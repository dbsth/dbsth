# main_crawler.py (실행 로직)
import os
import time
from datetime import datetime

from crawler_config import ConfigLoader
from crawler_utils import CrawlerUtils
from page_processor import PageProcessor
from url_builder import URLBuilder
from data_handler import DataHandler
from date_formatter import DateFormatter
from load_csv import load_latest_csv_as_dataframe
from post_crawler import PostExtractor
from file_manager import FileManager
from urllib.parse import urlparse, parse_qs
import pandas as pd
import re
from bs4 import BeautifulSoup

class NoticeCrawler:
    def __init__(self, config_path, csv_save_directory="data"):
        self.url_list = ConfigLoader.load_urls(config_path)
        self.collected_data = []
        self.csv_save_directory = csv_save_directory
        self.existing_df = self._load_existing_dataframe() # 기존 데이터프레임 로드
        self.post_extractor = PostExtractor() # PostExtractor 인스턴스 생성

    def _load_existing_dataframe(self):
        """기존의 최신 CSV 파일을 로드하거나, 파일이 없으면 빈 DataFrame을 반환합니다."""
        output_dir = os.path.join(os.path.dirname(__file__), "..", self.csv_save_directory)
        try:
            return load_latest_csv_as_dataframe(output_dir)
        except FileNotFoundError:
            print("⚠️ 기존 CSV 파일을 찾을 수 없습니다. 새로운 DataFrame으로 시작합니다.")
            return pd.DataFrame()
        except Exception as e:
            print(f"⚠️ 기존 CSV 파일 로드 실패: {e}")
            return pd.DataFrame()

    def process_site(self, site):
        """crawler_url.json에 정의된 각 사이트를 순회하며 게시물을 처리합니다."""
        base_url = site.get("url", "")
        board_path = site.get("board_path", "")
        crawl_delay = site.get("crawl_delay", 5)
        timeout = site.get("crawl_timeout", 30)
        page = 0

        print(f"\n🔍 {base_url} 크롤링 시작...")

        while True:
            current_url = URLBuilder.build_paginated_url(base_url, page)
            print(f"    🔄 [{page + 1}페이지] 요청 중...")

            try:
                html_content = CrawlerUtils.make_request(current_url, timeout)
                processor = PageProcessor(html_content)

                if not processor.has_content():
                    print(f"⚠️ [{page + 1}페이지] 컨텐츠 없음")
                    break

                posts = processor.extract_posts(board_path)
                newly_collected = self._process_posts(posts, base_url, site)

                if not newly_collected:
                    print(f"⛔ 페이지 {page + 1}에서 새로운 게시물 없음. 해당 URL 크롤링 완료.")
                    break

                self.collected_data.extend(newly_collected)
                page += 1
                time.sleep(crawl_delay)

            except Exception as e:
                print(f"❌ 에러 발생: {e}")
                break

    def _process_posts(self, posts, base_url, site):
        """게시물 목록에서 각 게시물의 링크를 따라가 상세 정보를 추출하고 중복을 확인합니다."""
        newly_collected_posts = []
        new_post_found = False
        duplicate_check_key = site.get("duplicate_check_key", "articleNo")

        # collected_data 중복 확인을 위한 set (튜플 형태로 저장하여 해싱 가능하게 함)
        collected_data_keys = set([(item.get(duplicate_check_key), item.get("university"), item.get("department"))
                                     for item in self.collected_data if item.get(duplicate_check_key)])

        # existing_df 중복 확인을 위한 set (튜플 형태로 저장)
        existing_df_keys = set()
        if not self.existing_df.empty and duplicate_check_key in self.existing_df.columns and \
           "university" in self.existing_df.columns and "department" in self.existing_df.columns:
            existing_df_keys = set(zip(self.existing_df[duplicate_check_key].astype(str),
                                       self.existing_df["university"].astype(str),
                                       self.existing_df["department"].astype(str)))

        for post_element in posts:
            title = "".join(post_element.stripped_strings).strip()
            href = post_element.get("href")

            full_url = CrawlerUtils.get_full_url(base_url, href)

            post_data = self._crawl_and_extract_post(full_url, site)
            if post_data:
                duplicate_key = post_data.get(duplicate_check_key)
                post_university = post_data.get("university")
                post_department = post_data.get("department")

                if duplicate_key:
                    # collected_data 중복 확인
                    current_key = (duplicate_key, post_university, post_department)
                    if current_key in collected_data_keys:
                        # print(f"⚠️ 이번 수집 데이터 중 중복 게시물 발견 ({duplicate_check_key}={duplicate_key}): {title}")
                        continue

                    # existing_df 중복 확인
                    if (str(duplicate_key), str(post_university), str(post_department)) in existing_df_keys:
                        # print(f"⚠️ 기존 데이터 중 중복 게시물 발견 ({duplicate_check_key}={duplicate_key}): {title}")
                        continue

                    newly_collected_posts.append(post_data)
                    collected_data_keys.add(current_key) # 새로 수집된 데이터의 키 추가
                    new_post_found = True
                    # print(f"📌 새 게시물 수집 완료: {title} ({full_url})")

        if new_post_found:
            return newly_collected_posts
        else:
            return None

    def _crawl_and_extract_post(self, post_url, site):
        """주어진 URL의 게시물 상세 정보를 크롤링하고 추출합니다."""
        try:
            response = CrawlerUtils.make_request(post_url)
            return self.post_extractor.extract_post_data(post_url, response, site)
        except Exception as e:
            print(f"❌ 게시물 처리 실패: {post_url} - {str(e)}")
            return None

    def run(self):
        """크롤러를 실행하고 결과를 CSV 파일로 저장합니다."""
        for site in self.url_list:
            self.process_site(site)

        all_collected_df = pd.DataFrame(self.collected_data)

        if not all_collected_df.empty:
            # 기존 데이터프레임과 새로 수집된 데이터를 병합
            final_df = pd.concat([self.existing_df, all_collected_df], ignore_index=True)
        else:
            final_df = self.existing_df # 수집된 데이터가 없으면 기존 데이터프레임 유지

        output_dir = os.path.join(os.path.dirname(__file__), "..", self.csv_save_directory)
        os.makedirs(output_dir, exist_ok=True)
        csv_filename = DateFormatter.get_timestamp_filename()
        output_path = os.path.join(output_dir, csv_filename)

        try:
            final_df.to_csv(output_path, index=False, encoding="utf-8-sig")
            print(f"\n✅ CSV 파일 저장 완료: {output_path}")
        except Exception as e:
            print(f"❌ CSV 파일 저장 실패: {e}")

        # 오래된 CSV 파일 삭제 (현재는 동작하지 않음)
        # FileManager.delete_old_csv_files(output_dir, days_threshold=7)

if __name__ == "__main__":
    crawler = NoticeCrawler("test_crawler_url.json")
    crawler.run()