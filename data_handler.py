# data_handler.py
import csv
import json
import os
from datetime import datetime

class DataHandler:
    @staticmethod
    def _ensure_directory(file_path):
        """디렉토리 존재 여부 확인"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 기능 만들어두었기에 코드로 구현은 하였지만 현재 프로젝트에서는 미사용
    # @staticmethod
    # def save_to_json(data, file_path="data/notices.json"):
    #     """JSON 저장 로직 (기존 기능 유지)"""
    #     DataHandler._ensure_directory(file_path)
    #     existing_data = []
        
    #     if os.path.exists(file_path):
    #         try:
    #             with open(file_path, "r", encoding="utf-8") as f:
    #                 existing_data = json.load(f)
    #                 if not isinstance(existing_data, list):
    #                     existing_data = [existing_data]
    #         except (json.JSONDecodeError, FileNotFoundError):
    #             existing_data = []
        
    #     if not any(n["title"] == data["title"] and n["date"] == data["date"] 
    #               for n in existing_data):
    #         existing_data.append(data)
            
    #     with open(file_path, "w", encoding="utf-8") as f:
    #         json.dump(existing_data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def export_to_csv(data_list, output_dir="data", filename=None):
        """CSV 저장 로직 개선"""
        DataHandler._ensure_directory(output_dir)
        
        if not data_list:
            print("⚠️ 내보낼 데이터가 없습니다")
            return

        # 파일명 생성 전략
        final_filename = filename or "posts.csv"
        csv_path = os.path.join(output_dir, final_filename)

        fieldnames = [
            'title', 'date', 'content', 
            'last_crawled', 'status',
            'crawl_frequency', 'crawl_timeout', 'crawl_delay'
        ]

        try:
            with open(csv_path, "w", encoding="utf-8", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data_list)
            print(f"✅ CSV 저장 완료: {csv_path}")
        except Exception as e:
            print(f"❌ CSV 저장 실패: {e}")