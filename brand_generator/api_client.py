# api_client.py
import os
import time
from functools import wraps
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://copa.codyssey.kr/api/v1"
)

# ─────────────────────────────────────────
# 🔄 재시도 데코레이터
# ─────────────────────────────────────────
def retry_with_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    delay = base_delay * (2 ** attempt)
                    print(f"  ⚠️ 재시도 {attempt+1}/{max_retries} ({delay}초 후)")
                    time.sleep(delay)
        return wrapper
    return decorator

# ─────────────────────────────────────────
# 📡 공통 API 호출 함수
# ─────────────────────────────────────────
@retry_with_backoff(max_retries=3)
def chat(messages, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

# ─────────────────────────────────────────
# ✅ 응답 검증 함수
# ─────────────────────────────────────────
def validate_response(response, min_length=50, required_keywords=None):
    if not response or len(response) < min_length:
        return False, "응답이 너무 짧습니다"
    if required_keywords:
        for kw in required_keywords:
            if kw not in response:
                return False, f"필수 키워드 누락: {kw}"
    return True, "OK"