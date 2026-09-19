import base64
import json
import os
import re
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from openai import OpenAI
from dotenv import load_dotenv
from fpdf import FPDF

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

# ─────────────────────────────────────────
# 📂 브리프 로드
# ─────────────────────────────────────────
def load_brief(file_path):
    """JSON 브리프 파일 로드"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        exit(1)
    except json.JSONDecodeError:
        print(f"❌ JSON 형식이 잘못되었습니다: {file_path}")
        exit(1)

# ─────────────────────────────────────────
# ✨ 브랜드 네이밍 생성 (신규 추가)
# ─────────────────────────────────────────
def generate_naming(brief):
    """브랜드 네이밍 후보 3~5개 + 의미 생성"""
    print("\n🏷️  [1단계] 브랜드 네이밍 생성 중...")
    try:
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": "당신은 전문 브랜드 네이밍 전략가입니다."},
                {"role": "user", "content": f"""
아래 브랜드 정보를 바탕으로 브랜드명 후보를 만들어주세요.

업종: {brief.get('industry', '')}
타겟: {brief.get('target_audience', brief.get('target', ''))}
핵심가치: {', '.join(brief.get('values', brief.get('keywords', [])))}
톤앤매너: {brief.get('tone', '')}

요구사항:
- 한글 네이밍 3~5개를 제안해주세요
- 각 네이밍마다 영문 네이밍도 함께 제안해주세요
- 각 네이밍의 의미와 유래를 설명해주세요

형식:
1. [한글명] / [영문명]
   의미: (설명)

2. [한글명] / [영문명]
   의미: (설명)
"""}
            ]
        )
        result = response.choices[0].message.content
        print(result)
        return result
    except Exception as e:
        print(f"❌ 네이밍 생성 실패: {e}")
        return "네이밍 생성에 실패했습니다."

# ─────────────────────────────────────────
# 💬 슬로건 생성
# ─────────────────────────────────────────
def generate_slogan(brief):
    """슬로건/태그라인 3개 생성"""
    print("\n💬 [2단계] 슬로건 생성 중...")
    try:
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": "당신은 전문 브랜드 카피라이터입니다."},
                {"role": "user", "content": f"""
아래 브랜드 정보를 바탕으로 슬로건/태그라인 3개를 만들어주세요.

브랜드명: {brief.get('brand_name', '')}
업종: {brief.get('industry', '')}
타겟: {brief.get('target_audience', brief.get('target', ''))}
톤앤매너: {brief.get('tone', '')}

요구사항:
- 브랜드 톤앤매너에 맞는 문구
- 짧고 기억에 남는 문장
- 번호를 붙여서 3개 작성
"""}
            ]
        )
        result = response.choices[0].message.content
        print(result)
        return result
    except Exception as e:
        print(f"❌ 슬로건 생성 실패: {e}")
        return "슬로건 생성에 실패했습니다."

# ─────────────────────────────────────────
# 📖 브랜드 스토리 생성
# ─────────────────────────────────────────
def generate_brand_story(brief):
    """브랜드 스토리 300자 내외 생성"""
    print("\n📖 [3단계] 브랜드 스토리 생성 중...")
    try:
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": "당신은 브랜드 스토리텔링 전문가입니다."},
                {"role": "user", "content": f"""
아래 브랜드 정보를 바탕으로 브랜드 스토리를 작성해주세요.

브랜드명: {brief.get('brand_name', '')}
업종: {brief.get('industry', '')}
타겟: {brief.get('target_audience', brief.get('target', ''))}
핵심가치: {', '.join(brief.get('values', brief.get('keywords', [])))}
톤앤매너: {brief.get('tone', '')}

요구사항:
- 300자 내외로 작성
- 브랜드 탄생 배경 포함
- 브랜드 철학과 비전 포함
- 감성적이고 공감가는 문체
"""}
            ]
        )
        result = response.choices[0].message.content
        print(result)
        return result
    except Exception as e:
        print(f"❌ 브랜드 스토리 생성 실패: {e}")
        return "브랜드 스토리 생성에 실패했습니다."

# ─────────────────────────────────────────
# 🎨 컬러 팔레트 생성 (신규 추가)
# ─────────────────────────────────────────
def generate_color_palette(brief, output_folder):
    """HEX 코드 생성 + PNG 시각화 저장"""
    print("\n🎨 [4단계] 컬러 팔레트 생성 중...")
    try:
        # 1) LLM으로 HEX 코드 받기
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": "당신은 브랜드 컬러 전문가입니다. 반드시 HEX 코드만 포함한 JSON으로 답변하세요."},
                {"role": "user", "content": f"""
아래 브랜드에 어울리는 컬러 팔레트를 추천해주세요.

브랜드명: {brief.get('brand_name', '')}
업종: {brief.get('industry', '')}
톤앤매너: {brief.get('tone', '')}
핵심가치: {', '.join(brief.get('values', brief.get('keywords', [])))}

반드시 아래 JSON 형식으로만 답변하세요. 다른 텍스트는 포함하지 마세요:
{{
  "main_color": {{
    "hex": "#XXXXXX",
    "name": "색상 이름",
    "reason": "선택 이유"
  }},
  "sub_colors": [
    {{"hex": "#XXXXXX", "name": "색상 이름", "reason": "선택 이유"}},
    {{"hex": "#XXXXXX", "name": "색상 이름", "reason": "선택 이유"}},
    {{"hex": "#XXXXXX", "name": "색상 이름", "reason": "선택 이유"}}
  ]
}}
"""}
            ]
        )

        raw = response.choices[0].message.content.strip()

        # 2) JSON 파싱 (코드블록 제거)
        raw = re.sub(r"```json|```", "", raw).strip()
        color_data = json.loads(raw)

        print(f"  메인 컬러: {color_data['main_color']['hex']} ({color_data['main_color']['name']})")
        for sc in color_data['sub_colors']:
            print(f"  서브 컬러: {sc['hex']} ({sc['name']})")

        # 3) matplotlib으로 PNG 시각화
        _save_color_palette_image(color_data, output_folder)

        return color_data

    except json.JSONDecodeError:
        print(f"❌ 컬러 팔레트 JSON 파싱 실패. 기본 컬러를 사용합니다.")
        # 기본 컬러 팔레트
        default_data = {
            "main_color": {"hex": "#2C3E50", "name": "다크 네이비", "reason": "기본값"},
            "sub_colors": [
                {"hex": "#E74C3C", "name": "레드", "reason": "기본값"},
                {"hex": "#ECF0F1", "name": "라이트 그레이", "reason": "기본값"},
                {"hex": "#F39C12", "name": "오렌지", "reason": "기본값"}
            ]
        }
        _save_color_palette_image(default_data, output_folder)
        return default_data
    except Exception as e:
        print(f"❌ 컬러 팔레트 생성 실패: {e}")
        return {}

def _save_color_palette_image(color_data, output_folder):
    """컬러 팔레트를 PNG로 저장하는 내부 함수"""
    try:
        main = color_data["main_color"]
        subs = color_data["sub_colors"]

        # 전체 색상 리스트 구성
        all_colors = [main] + subs
        n = len(all_colors)

        fig, axes = plt.subplots(1, n, figsize=(n * 2.5, 4))
        if n == 1:
            axes = [axes]

        for i, (ax, color) in enumerate(zip(axes, all_colors)):
            ax.set_facecolor(color["hex"])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_xticks([])
            ax.set_yticks([])

            # 라벨 표시
            label = "MAIN" if i == 0 else f"SUB {i}"
            ax.text(0.5, 0.85, label,
                    ha='center', va='center',
                    fontsize=10, fontweight='bold',
                    color='white' if _is_dark(color["hex"]) else 'black')
            ax.text(0.5, 0.55, color["name"],
                    ha='center', va='center',
                    fontsize=9,
                    color='white' if _is_dark(color["hex"]) else 'black')
            ax.text(0.5, 0.30, color["hex"],
                    ha='center', va='center',
                    fontsize=9, fontfamily='monospace',
                    color='white' if _is_dark(color["hex"]) else 'black')

        plt.suptitle("Brand Color Palette", fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()

        save_path = os.path.join(output_folder, "color_palette.png")
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  ✅ 컬러 팔레트 저장 완료: {save_path}")

    except Exception as e:
        print(f"❌ 컬러 팔레트 이미지 저장 실패: {e}")

def _is_dark(hex_color):
    """HEX 색상이 어두운지 판단 (텍스트 색상 결정용)"""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    # 밝기 공식
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return brightness < 128

# ─────────────────────────────────────────
# 🖼️ 로고 시안 생성 (신규 추가)
# ─────────────────────────────────────────
def generate_logo_images(brief, output_folder, count=2):
    """DALL-E로 로고 시안 PNG 생성"""
    print(f"\n🖼️  [5단계] 로고 시안 {count}개 생성 중...")

    saved_paths = []

    prompts = [
        f"Minimalist logo design for '{brief.get('brand_name', 'Brand')}', "
        f"a {brief.get('industry', '')} brand. Clean, modern, professional. "
        f"White background, simple icon with brand name. Vector style.",

        f"Premium logo for '{brief.get('brand_name', 'Brand')}' brand. "
        f"Industry: {brief.get('industry', '')}. "
        f"Elegant typography with subtle symbol. Flat design, white background.",

        f"Creative logo concept for '{brief.get('brand_name', 'Brand')}'. "
        f"Target audience: {brief.get('target_audience', brief.get('target', ''))}. "
        f"Bold, memorable, unique. White background, no text except brand name.",
    ]

    for i in range(min(count, len(prompts))):
        try:
            print(f"  🎨 로고 시안 {i+1} 생성 중...")

            img_response = requests.post(
                "https://copa.codyssey.kr/api/v1/images",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
                },
                json={
                    "model": "gpt-image-1-mini",
                    "prompt": prompts[i],
                    "size": "1024x1024",
                    "response_format": "b64_json"
                }
            )

            image_b64 = img_response.json()["result"]["images"][0]["b64_json"]
            save_path = os.path.join(output_folder, f"logo_concept_{i+1}.png")
            with open(save_path, "wb") as f:
                f.write(base64.b64decode(image_b64))
            print(f"  ✅ 로고 시안 {i+1} 저장 완료: {save_path}")
            saved_paths.append(save_path)

        except Exception as e:
            print(f"  ❌ 로고 시안 {i+1} 생성 실패: {e}")

    return saved_paths
    
# ─────────────────────────────────────────
# 📢 광고 카피 생성
# ─────────────────────────────────────────
def generate_ad_copy(brief):
    """광고 카피 10개 생성"""
    print("\n📢 [6단계] 광고 카피 생성 중...")
    try:
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": "당신은 광고 카피라이터입니다."},
                {"role": "user", "content": f"""
아래 브랜드 정보를 바탕으로 광고 카피 10개를 만들어주세요.

브랜드명: {brief.get('brand_name', '')}
업종: {brief.get('industry', '')}
타겟: {brief.get('target_audience', brief.get('target', ''))}
핵심가치: {', '.join(brief.get('values', brief.get('keywords', [])))}
톤앤매너: {brief.get('tone', '')}

조건:
- 짧고 강렬하게 (10~20자 내외)
- 각 카피는 다른 감성/상황을 담을 것
- 번호를 붙여서 작성
"""}
            ]
        )
        result = response.choices[0].message.content
        print(result)
        return result
    except Exception as e:
        print(f"❌ 광고 카피 생성 실패: {e}")
        return "광고 카피 생성에 실패했습니다."

# ─────────────────────────────────────────
# 🍔 메뉴 네이밍 생성
# ─────────────────────────────────────────
def generate_menu_naming(brief):
    """메뉴 네이밍 전략 생성"""
    print("\n🍔 [7단계] 메뉴 네이밍 생성 중...")
    try:
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": "당신은 F&B 브랜드 전문가입니다."},
                {"role": "user", "content": f"""
아래 브랜드 정보를 바탕으로 메뉴 네이밍 전략을 제안해주세요.

브랜드명: {brief.get('brand_name', '')}
업종: {brief.get('industry', '')}
타겟: {brief.get('target_audience', brief.get('target', ''))}
핵심가치: {', '.join(brief.get('values', brief.get('keywords', [])))}

다음 항목을 작성해주세요:
1. 메뉴 네이밍 원칙 (3가지)
2. 메뉴 이름 예시 5개 (버거 기준)
3. 메뉴판에서 사용할 설명 문구 스타일
"""}
            ]
        )
        result = response.choices[0].message.content
        print(result)
        return result
    except Exception as e:
        print(f"❌ 메뉴 네이밍 생성 실패: {e}")
        return "메뉴 네이밍 생성에 실패했습니다."

# ─────────────────────────────────────────
# 🍀 메뉴 네이밍 스타일
# ─────────────────────────────────────────
def generate_menu_naming_styles(brief):
    """트렌디형/프리미엄형 메뉴 네이밍"""
    print("\n🍀 [8단계] 메뉴 네이밍 스타일 생성 중...")
    try:
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": "당신은 F&B 브랜드 전문 네이밍 디렉터입니다."},
                {"role": "user", "content": f"""
브랜드 정보:
- 브랜드명: {brief.get('brand_name', '')}
- 업종: {brief.get('industry', '')}
- 타겟: {brief.get('target_audience', brief.get('target', ''))}

아래 두 가지 스타일로 버거 메뉴 이름을 각각 5개씩 만들어주세요.

[트렌디형]
- 힙하고 젊은 감성
- SNS에서 공유하고 싶은 이름
- 영어+한글 믹스 가능

[프리미엄형]
- 고급스럽고 격식있는 느낌
- 재료나 조리법이 느껴지는 이름
- 신뢰감을 주는 네이밍

각 메뉴명 옆에 한 줄 설명도 붙여주세요.
"""}
            ]
        )
        result = response.choices[0].message.content
        print(result)
        return result
    except Exception as e:
        print(f"❌ 메뉴 네이밍 스타일 생성 실패: {e}")
        return "메뉴 네이밍 스타일 생성에 실패했습니다."

# ─────────────────────────────────────────
# 🌍 다국어 생성
# ─────────────────────────────────────────
def generate_multilingual(brief, language):
    """다국어 브랜드 콘텐츠 생성"""
    lang_map = {"en": "English", "ja": "Japanese"}
    lang_name = lang_map.get(language, "English")
    lang_emoji = {"en": "🌍", "ja": "🌏"}.get(language, "🌐")
    print(f"\n{lang_emoji} [{language.upper()}] 다국어 버전 생성 중...")

    try:
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": f"You are a brand consultant. Answer in {lang_name} only."},
                {"role": "user", "content": f"""
Brand Info:
- Brand Name: {brief.get('brand_name', '')}
- Industry: {brief.get('industry', '')}
- Target: {brief.get('target_audience', brief.get('target', ''))}
- Values: {', '.join(brief.get('values', brief.get('keywords', [])))}

Please provide in {lang_name}:
1. Brand Slogan (3 options)
2. Brand Story (3-4 sentences)
3. SNS Bio (under 150 characters)

All output must be in {lang_name} only.
"""}
            ]
        )
        result = response.choices[0].message.content
        print(result)
        return result
    except Exception as e:
        print(f"❌ 다국어 생성 실패: {e}")
        return f"{lang_name} 생성에 실패했습니다."

# ─────────────────────────────────────────
# 💾 저장 함수들
# ─────────────────────────────────────────
def save_txt(text, filepath):
    """TXT 저장"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  ✅ TXT 저장: {filepath}")

def save_pdf(text, filepath):
    """PDF 저장"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font("Malgun", "", "C:/Windows/Fonts/malgun.ttf", uni=True)
        pdf.set_font("Malgun", size=12)
        for line in text.split("\n"):
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output(filepath)
        print(f"  ✅ PDF 저장: {filepath}")
    except Exception as e:
        print(f"  ❌ PDF 저장 실패: {e}")

def save_json(data, filepath):
    """JSON 저장 (신규 추가)"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ JSON 저장: {filepath}")