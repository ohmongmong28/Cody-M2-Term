# main.py
from brand_generator import (
    create_shared_state,
    generate_naming,
    generate_slogan,
    generate_story,
    generate_color,
    generate_logo_prompt,
    generate_logo_images
)
from storage import save_brand_result

# ─────────────────────────────────────────
# 🎯 메인 실행 함수
# ─────────────────────────────────────────
def main():
    print("=" * 50)
    print("🎨 브랜드 생성기 시작!")
    print("=" * 50)

    # 사용자 입력
    user_input = {
        "brand_name": input("브랜드명: "),
        "industry": input("업종: "),
        "target": input("타겟 고객: "),
        "concept": input("브랜드 컨셉: "),
        "keywords": input("핵심 키워드: "),
        "mood": input("분위기: "),
        "core_value": input("핵심 가치: ")
    }

    # 공유 상태 초기화 (FAIL #11)
    shared_state = create_shared_state(user_input)

    # 결과 저장용 딕셔너리 (FAIL #6)
    brand_result = {
        "brand_name": user_input["brand_name"],
        "errors": []
    }

    # ─────────────────────────────────────
    # 단계별 생성
    # ─────────────────────────────────────
    print("\n1️⃣ 브랜드 네이밍 생성 중...")
    brand_result["naming"] = generate_naming(shared_state, brand_result)

    print("\n2️⃣ 슬로건 생성 중...")
    brand_result["slogan"] = generate_slogan(shared_state, brand_result)

    print("\n3️⃣ 브랜드 스토리 생성 중...")
    brand_result["story"] = generate_story(shared_state, brand_result)

    print("\n4️⃣ 컬러 팔레트 생성 중...")
    brand_result["color"] = generate_color(shared_state, brand_result)

    print("\n5️⃣ 로고 프롬프트 생성 중...")
    logo_prompt = generate_logo_prompt(shared_state, brand_result)
    brand_result["logo_prompt"] = logo_prompt

    print("\n6️⃣ 로고 이미지 생성 중...")
    brand_result["logo_images"] = generate_logo_images(
        logo_prompt, brand_result
    )

    # ─────────────────────────────────────
    # 결과 저장 
    # ─────────────────────────────────────
    print("\n💾 결과 저장 중...")
    saved_file = save_brand_result(brand_result)

    # ─────────────────────────────────────
    # 최종 출력
    # ─────────────────────────────────────
    print("\n" + "=" * 50)
    print("🎉 브랜드 생성 완료!")
    print("=" * 50)
    print(f"📁 저장 위치: {saved_file}")

    if brand_result["errors"]:
        print(f"\n⚠️ 발생한 에러 ({len(brand_result['errors'])}건):")
        for err in brand_result["errors"]:
            print(f"  - [{err['step']}] {err['message']}")
    else:
        print("✅ 에러 없이 완료!")

    return brand_result

if __name__ == "__main__":
    main()