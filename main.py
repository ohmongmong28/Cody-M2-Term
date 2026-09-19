# main.py
import os
from brand_generator import (
    load_brief,
    generate_naming,
    generate_slogan,
    generate_brand_story,
    generate_color_palette,
    generate_logo_images,
    generate_ad_copy,
    generate_menu_naming,
    generate_menu_naming_styles,
    generate_multilingual,
    save_txt,
    save_pdf,
    save_json
)

def main():
    print("🚀 AI 브랜드 생성기 시작!")
    print("=" * 50)

    output_folder = "brand_output"
    os.makedirs(output_folder, exist_ok=True)

    # 브리프 로드 (main.py 기준 경로)
    brief = load_brief("brief.json")
    print(f"📋 브랜드 정보 로드 완료: {brief.get('brand_name', '')}")

    brand_result = {
        "brand_name": brief.get("brand_name", ""),
        "industry": brief.get("industry", ""),
        "generated_content": {},
        "errors": []
    }

    all_text = ""

    # ── 1. 브랜드 네이밍 ──
    naming = generate_naming(brief)
    if "실패" in naming:
        brand_result["errors"].append({"step": "naming", "message": "브랜드 네이밍 생성 실패"})
    brand_result["generated_content"]["naming"] = naming
    all_text += "=" * 50 + "\n🏷️  브랜드 네이밍\n" + "=" * 50 + "\n" + naming + "\n\n"

    # ── 2. 슬로건 ──
    slogan = generate_slogan(brief)
    if "실패" in slogan:
        brand_result["errors"].append({"step": "slogan", "message": "슬로건 생성 실패"})
    brand_result["generated_content"]["slogan"] = slogan
    all_text += "=" * 50 + "\n💬 슬로건\n" + "=" * 50 + "\n" + slogan + "\n\n"

    # ── 3. 브랜드 스토리 ──
    story = generate_brand_story(brief)
    if "실패" in story:
        brand_result["errors"].append({"step": "brand_story", "message": "브랜드 스토리 생성 실패"})
    brand_result["generated_content"]["brand_story"] = story
    all_text += "=" * 50 + "\n📖 브랜드 스토리\n" + "=" * 50 + "\n" + story + "\n\n"

    # ── 4. 컬러 팔레트 ──
    color_data = generate_color_palette(brief, output_folder)
    if not color_data:
        brand_result["errors"].append({"step": "color_palette", "message": "컬러 팔레트 생성 실패"})
    brand_result["generated_content"]["color_palette"] = color_data
    all_text += "=" * 50 + "\n🎨 컬러 팔레트\n" + "=" * 50 + "\n"
    if color_data:
        all_text += f"메인: {color_data.get('main_color', {}).get('hex', '')} "
        all_text += f"({color_data.get('main_color', {}).get('name', '')})\n"
        for sc in color_data.get('sub_colors', []):
            all_text += f"서브: {sc.get('hex', '')} ({sc.get('name', '')})\n"
    all_text += "\n"

    # ── 5. 로고 시안 ──
    logo_paths = generate_logo_images(brief, output_folder, count=2)
    if not logo_paths:
        brand_result["errors"].append({"step": "logo", "message": "로고 이미지 생성 실패"})
    brand_result["generated_content"]["logo_image_paths"] = logo_paths
    all_text += "=" * 50 + "\n🖼️  로고 시안\n" + "=" * 50 + "\n"
    for p in logo_paths:
        all_text += f"저장 경로: {p}\n"
    all_text += "\n"

    # ── 6. 광고 카피 ──
    ad_copy = generate_ad_copy(brief)
    if "실패" in ad_copy:
        brand_result["errors"].append({"step": "ad_copy", "message": "광고 카피 생성 실패"})
    brand_result["generated_content"]["ad_copy"] = ad_copy
    all_text += "=" * 50 + "\n📢 광고 카피\n" + "=" * 50 + "\n" + ad_copy + "\n\n"

    # ── 7. 메뉴 네이밍 ──
    menu = generate_menu_naming(brief)
    if "실패" in menu:
        brand_result["errors"].append({"step": "menu_naming", "message": "메뉴 네이밍 생성 실패"})
    brand_result["generated_content"]["menu_naming"] = menu
    all_text += "=" * 50 + "\n🍔 메뉴 네이밍\n" + "=" * 50 + "\n" + menu + "\n\n"

    # ── 8. 메뉴 네이밍 스타일 ──
    menu_styles = generate_menu_naming_styles(brief)
    if "실패" in menu_styles:
        brand_result["errors"].append({"step": "menu_naming_styles", "message": "메뉴 네이밍 스타일 생성 실패"})
    brand_result["generated_content"]["menu_naming_styles"] = menu_styles
    all_text += "=" * 50 + "\n🍀 메뉴 네이밍 스타일\n" + "=" * 50 + "\n" + menu_styles + "\n\n"

    # ── 9. 다국어 ──
    result_en = generate_multilingual(brief, "en")
    result_ja = generate_multilingual(brief, "ja")
    if "실패" in result_en:
        brand_result["errors"].append({"step": "multilingual_en", "message": "영어 다국어 생성 실패"})
    if "실패" in result_ja:
        brand_result["errors"].append({"step": "multilingual_ja", "message": "일본어 다국어 생성 실패"})
    brand_result["generated_content"]["multilingual"] = {
        "english": result_en,
        "japanese": result_ja
    }
    all_text += "=" * 50 + "\n🌍 English Version\n" + "=" * 50 + "\n" + result_en + "\n\n"
    all_text += "=" * 50 + "\n🌏 日本語バージョン\n" + "=" * 50 + "\n" + result_ja + "\n\n"

    # ── 저장 ──
    print("\n" + "=" * 50)
    print("💾 결과 저장 중...")
    print("=" * 50)

    save_txt(all_text, os.path.join(output_folder, "brand_output.txt"))
    save_pdf(all_text, os.path.join(output_folder, "brand_output.pdf"))
    save_json(brand_result, os.path.join(output_folder, "brand_result.json"))

    print("\n" + "=" * 50)
    print("🎉 브랜드 생성 완료!")
    print("=" * 50)
    print(f"📁 저장 폴더: {output_folder}/")
    print(f"   ├── brand_output.txt")
    print(f"   ├── brand_output.pdf")
    print(f"   ├── brand_result.json")
    print(f"   ├── color_palette.png")
    print(f"   ├── logo_concept_1.png")
    print(f"   └── logo_concept_2.png")
    print("=" * 50)

    if brand_result["errors"]:
        print(f"\n⚠️ 발생한 에러 ({len(brand_result['errors'])}건):")
        for err in brand_result["errors"]:
            print(f"  - [{err['step']}] {err['message']}")
    else:
        print("✅ 에러 없이 완료!")

    return brand_result

if __name__ == "__main__":
    main()