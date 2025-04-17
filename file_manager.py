# web_crawler/file_manager.py
import os
from datetime import datetime, timedelta

class FileManager:
    @staticmethod
    def delete_old_csv_files(directory: str, days_threshold: int) -> None:
        """
        지정한 디렉토리에서 days_threshold일 이상 지난 CSV 파일을 삭제하는 함수
        파일명 형식: posts_YYYY-MM-DD_HHMM.csv
        """
        now = datetime.now()
        # cutoff 이전 날짜에 만들어진 파일 삭제 cutoff에 만든 파일은 생존
        cutoff = now - timedelta(days=days_threshold)

        for filename in os.listdir(directory):
            if filename.startswith("posts_") and filename.endswith(".csv"):
                try:
                    # 날짜 문자열만 추출 (posts_ 이후 ~ .csv 이전까지)
                    date_str = filename[len("posts_"):-len(".csv")]
                    file_datetime = datetime.strptime(date_str, "%Y-%m-%d_%H%M")

                    if file_datetime < cutoff:
                        file_path = os.path.join(directory, filename)
                        os.remove(file_path)
                        print(f"삭제됨: {file_path}")
                except ValueError:
                    print(f"[무시됨] 날짜 파싱 실패: {filename}")

if __name__ == "__main__":
    # 테스트를 위한 임시 디렉토리 생성 및 파일 생성
    test_dir = "test_csv_files"
    os.makedirs(test_dir, exist_ok=True)

    now = datetime.now()
    yesterday = now - timedelta(days=1)
    two_days_ago = now - timedelta(days=2)

    with open(os.path.join(test_dir, f"posts_{yesterday.strftime('%Y-%m-%d_%H%M')}.csv"), "w") as f:
        f.write("test data")
    with open(os.path.join(test_dir, f"posts_{two_days_ago.strftime('%Y-%m-%d_%H%M')}.csv"), "w") as f:
        f.write("old data")
    with open(os.path.join(test_dir, f"other_file.txt"), "w") as f:
        f.write("not a csv")

    print("삭제 전 파일 목록:", os.listdir(test_dir))
    FileManager.delete_old_csv_files(test_dir, days_threshold=1)
    print("삭제 후 파일 목록:", os.listdir(test_dir))

    # 테스트 디렉토리 삭제
    import shutil
    shutil.rmtree(test_dir)