# brand_generator.py
from api_client import chat, validate_response
from prompt_templates import (
    NAMING_PROMPT, SLOGAN_PROMPT,
    STORY_PROMPT, COLOR_PROMPT, LOGO_PROMPT
)
from storage import record_error

# ─────────────────────────────────────────
# 🔗 공유 컨텍스트 
# ─────────────────────────────────────────
def create_shared_state(user_input: dict) -> dict:
    """단계별 결과를 누적하는 공유 상태 딕셔너리"""
    return {
        "brand_name": user_input.get("brand_name", ""),
        "industry": user_input.get("industry", ""),
        "target": user_input.get("target", ""),
        "concept": user_input.get("concept", ""),
        "keywords": user_input.get("keywords", ""),
        "mood": user_input.get("mood", ""),
        "core_value": user_input.get("core_value", ""),
        # 단계별 결과 누적
        "prev_naming": "",
        "prev_slogan": "",
        "prev_story": "",
        "prev_color": "",
        "errors": []
    }

# ─────────────────────────────────────────
# 1️⃣ 브랜드 네이밍 
# ─────────────────────────────────────────
def generate_naming(shared_state: dict, brand_result: dict) -> str:
    max_retries = 2
    for attempt in range(max_retries):
        try:
            prompt = NAMING_PROMPT.format(**shared_state)
            messages = [{"role": "user", "content": prompt}]
            response = chat(messages)

            # 검증 (FAIL #16)
            valid, reason = validate_response(
                response,
                min_length=50,
                required_keywords=["1.", "2.", "3."]
            )
            if not valid:
                print(f"  ⚠️ 네이밍 검증 실패: {reason} → 재시도")
                continue

            # 컨텍스트 갱신 (FAIL #11)
            shared_state["prev_naming"] = response
            print("  ✅ 네이밍 완료")
            return response

        except Exception as e:
            record_error(brand_result, "naming", str(e))

    return "네이밍 생성 실패"

# ─────────────────────────────────────────
# 2️⃣ 슬로건
# ─────────────────────────────────────────
def generate_slogan(shared_state: dict, brand_result: dict) -> str:
    max_retries = 2
    for attempt in range(max_retries):
        try:
            prompt = SLOGAN_PROMPT.format(**shared_state)
            messages = [{"role": "user", "content": prompt}]
            response = chat(messages)

            valid, reason = validate_response(
                response,
                min_length=50,
                required_keywords=["1.", "2.", "3."]
            )
            if not valid:
                print(f"  ⚠️ 슬로건 검증 실패: {reason} → 재시도")
                continue

            shared_state["prev_slogan"] = response
            print("  ✅ 슬로건 완료")
            return response

        except Exception as e:
            record_error(brand_result, "slogan", str(e))

    return "슬로건 생성 실패"

# ─────────────────────────────────────────
# 3️⃣ 브랜드 스토리 
# ─────────────────────────────────────────
def generate_story(shared_state: dict, brand_result: dict) -> str:
    max_retries = 2
    for attempt in range(max_retries):
        try:
            prompt = STORY_PROMPT.format(**shared_state)
            messages = [{"role": "user", "content": prompt}]
            response = chat(messages)

            valid, reason = validate_response(
                response,
                min_length=100
            )
            if not valid:
                print(f"  ⚠️ 스토리 검증 실패: {reason} → 재시도")
                continue

            shared_state["prev_story"] = response
            print("  ✅ 스토리 완료")
            return response

        except Exception as e:
            record_error(brand_result, "story", str(e))

    return "스토리 생성 실패"

# ─────────────────────────────────────────
# 4️⃣ 컬러 팔레트 
# ─────────────────────────────────────────
def generate_color(shared_state: dict, brand_result: dict) -> str:
    max_retries = 2
    for attempt in range(max_retries):
        try:
            prompt = COLOR_PROMPT.format(**shared_state)
            messages = [{"role": "user", "content": prompt}]
            response = chat(messages)

            valid, reason = validate_response(
                response,
                min_length=50,
                required_keywords=["#"]
            )
            if not valid:
                print(f"  ⚠️ 컬러 검증 실패: {reason} → 재시도")
                continue

            shared_state["prev_color"] = response
            print("  ✅ 컬러 완료")
            return response

        except Exception as e:
            record_error(brand_result, "color", str(e))

    return "컬러 생성 실패"

# ─────────────────────────────────────────
# 5️⃣ 로고 프롬프트 생성
# ─────────────────────────────────────────
def generate_logo_prompt(shared_state: dict, brand_result: dict) -> str:
    max_retries = 2
    for attempt in range(max_retries):
        try:
            prompt = LOGO_PROMPT.format(**shared_state)
            messages = [{"role": "user", "content": prompt}]
            response = chat(messages)

            valid, reason = validate_response(
                response,
                min_length=30
            )
            if not valid:
                print(f"  ⚠️ 로고 검증 실패: {reason} → 재시도")
                continue

            print("  ✅ 로고 프롬프트 완료")
            return response

        except Exception as e:
            record_error(brand_result, "logo_prompt", str(e))

    return "로고 프롬프트 생성 실패"

# ─────────────────────────────────────────
# 🖼️ 로고 이미지 생성 
# ─────────────────────────────────────────
def generate_logo_images(logo_prompt: str, brand_result: dict) -> list:
    """
    로고 이미지 3개 생성
    return문을 루프 밖으로 이동 (FAIL #4 핵심 수정)
    """
    from api_client import client
    image_urls = [] 

    for i in range(3):
        try:
            print(f"  🎨 로고 이미지 생성 중 {i+1}/3...")
            response = client.images.generate(
                model="dall-e-3",
                prompt=logo_prompt,
                size="1024x1024",
                n=1
            )
            url = response.data[0].url
            image_urls.append(url) 
            print(f"  ✅ 이미지 {i+1} 완료")

        except Exception as e:
            record_error(brand_result, f"logo_image_{i+1}", str(e))
            print(f"  ❌ 이미지 {i+1} 실패: {e}")

    return image_urls