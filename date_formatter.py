# date_formatter.py
from datetime import datetime

class DateFormatter:
    @staticmethod
    def get_current_date(format_str="%Y-%m-%d_%H%M"):
        """유연한 날짜 포맷 제공"""
        return datetime.now().strftime(format_str)

    @staticmethod
    def get_timestamp_filename():
        """CSV 파일명 생성 전문 메서드"""
        return f"posts_{DateFormatter.get_current_date()}.csv"
