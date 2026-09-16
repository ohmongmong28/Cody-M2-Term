# storage.py
import json
import os
from datetime import datetime

# ─────────────────────────────────────────
# 📁 저장 경로 설정
# ─────────────────────────────────────────
SAVE_DIR = "brand_results"

def ensure_dir():
    """저장 폴더 없으면 생성"""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

# ─────────────────────────────────────────
# 💾 브랜드 결과 저장
# ─────────────────────────────────────────
def save_brand_result(brand_result: dict) -> str:
    """
    brand_result 딕셔너리를 JSON으로 저장
    errors 배열 포함 (FAIL #6)
    """
    ensure_dir()

    # errors 필드 없으면 빈 배열 추가
    if "errors" not in brand_result:
        brand_result["errors"] = []

    # 저장 시각 기록
    brand_result["saved_at"] = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 파일명 생성
    timestamp = brand_result["saved_at"]
    brand_name = brand_result.get("brand_name", "unknown")
    filename = f"{SAVE_DIR}/{timestamp}_{brand_name}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(brand_result, f, ensure_ascii=False, indent=2)

    print(f"  ✅ 저장 완료: {filename}")
    return filename

# ─────────────────────────────────────────
# 📂 저장된 결과 불러오기
# ─────────────────────────────────────────
def load_brand_result(filename: str) -> dict:
    """저장된 JSON 파일 불러오기"""
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# ─────────────────────────────────────────
# 📋 저장 목록 조회
# ─────────────────────────────────────────
def list_saved_results() -> list:
    """저장된 브랜드 결과 목록 반환"""
    ensure_dir()
    files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
    files.sort(reverse=True)  # 최신순 정렬
    return files

# ─────────────────────────────────────────
# ❌ 에러 기록 함수
# ─────────────────────────────────────────
def record_error(brand_result: dict, step: str, error_msg: str):
    """
    brand_result["errors"] 배열에 에러 기록
    
    사용 예시:
    record_error(brand_result, "naming", "API 응답 없음")
    """
    if "errors" not in brand_result:
        brand_result["errors"] = []

    brand_result["errors"].append({
        "step": step,
        "message": error_msg,
        "time": datetime.now().strftime("%H:%M:%S")
    })
    print(f"  ⚠️ 에러 기록 [{step}]: {error_msg}")