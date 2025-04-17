# load_csv.py
import os
import pandas as pd

def load_latest_csv_as_dataframe(output_dir):
    """주어진 디렉토리에서 가장 최근 수정된 CSV 파일을 읽어 DataFrame으로 반환합니다."""
    csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
    if not csv_files:
        return pd.DataFrame()

    csv_files.sort(key=lambda f: os.path.getmtime(os.path.join(output_dir, f)), reverse=True)
    latest_csv_path = os.path.join(output_dir, csv_files[0])
    try:
        print(f"최신 CSV 파일 로드 중: {latest_csv_path}")
        return pd.read_csv(latest_csv_path, encoding="utf-8-sig")
    except Exception as e:
        print(f"[경고] CSV 파일 로드 실패: {e}")
        return pd.DataFrame()

# 테스트
if __name__ == '__main__':
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    df = load_latest_csv_as_dataframe(data_dir)
    if not df.empty:
        print("최신 CSV 파일 내용:")
        print(df.head())
    else:
        print("CSV 파일이 없거나 로드에 실패했습니다.")