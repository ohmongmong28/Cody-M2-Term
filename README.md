# Cody-M2-Term
코디세이 네이티브 팀미션2
---

# 🎨 AI 브랜드 생성기 (AI Brand Generator)

> OpenAI API를 활용한 자동 브랜드 아이덴티티 생성 CLI 프로젝트  
> Codyssey Native Team Mission 2

---

## 📌 프로젝트 소개

브랜드 정보를 입력하면 AI가 자동으로  
**브랜드 네이밍 → 슬로건 → 스토리 → 컬러 팔레트 → 로고 → 광고 카피 → 메뉴명 → 다국어**  
까지 한 번에 생성해주는 CLI 도구입니다.

---

## ⚙️ 주요 기능

| 기능 | 설명 |
|------|------|
| ✅ 브랜드 네이밍 | 3~5개 후보 + 의미 설명 자동 생성 |
| ✅ 슬로건 & 스토리 | 브랜드 정체성 기반 자동 작성 |
| ✅ 광고 카피 | 10개 자동 생성 |
| ✅ 메뉴 네이밍 | 트렌디형 / 프리미엄형 각 5개 |
| ✅ 다국어 지원 | 영어 / 일본어 변환 |
| ✅ 컬러 팔레트 | PNG 시각화 자동 저장 |
| ✅ 로고 시안 | matplotlib + DALL-E 이미지 생성 |
| ✅ 파일 저장 | TXT / PDF / JSON 자동 저장 |

---

## 🛠️ 사용 기술

| 기술 | 용도 |
|------|------|
| Python | 메인 언어 |
| OpenAI API (GPT-4o / DALL-E) | 텍스트 & 이미지 생성 |
| matplotlib | 로고 & 컬러 팔레트 시각화 |
| fpdf | PDF 보고서 저장 |
| json | 구조화 데이터 저장 |
| VS Code | 개발 환경 |

---

## 📁 프로젝트 파일 구조

```
Term_Project_mybrand_project/
│
├── brand_generator/              # 핵심 모듈 폴더
│   ├── api_client.py             # OpenAI API 연결 및 호출
│   ├── brand_generator.py        # 브랜드 생성 메인 로직
│   ├── main.py                   # CLI 진입점
│   ├── prompt_templates.py       # 프롬프트 템플릿 관리
│   └── storage.py                # 결과 저장 및 출력
│
├── brand_output/                 # 생성 결과물 폴더
│   ├── brand_output.pdf          # PDF 결과 보고서
│   ├── brand_output.txt          # 텍스트 결과
│   ├── brand_result.json         # JSON 결과 데이터
│   ├── color_palette.png         # 컬러 팔레트 이미지
│   ├── logo_concept_1.png        # 로고 컨셉 이미지
│   ├── logo_dalle_1.png          # DALL-E 생성 로고 1
│   ├── logo_dalle_2.png          # DALL-E 생성 로고 2
│   └── logo_dalle_3.png          # DALL-E 생성 로고 3
│
├── docs/                         # 문서 및 스크린샷
│   ├── screenshot_1.png
│   ├── screenshot_2.png
│   └── screenshot_3.png
│
├── README.md                     # 프로젝트 설명서
├── brand_generator.py            # 루트 실행 파일
└── brand_result.json             # 루트 결과 데이터
```

---

### 📍 "모듈 책임 분리 원칙"

```markdown
### 모듈 책임 분리 원칙
각 기능을 **독립 함수**로 분리하여 유지보수성과 재사용성을 높였습니다.

[brand_generator.py]
    │
    ├── load_brief()                  → brief.json 읽기
    │
    ├── generate_naming()             → 네이밍 결과 → brand_result 저장
    ├── generate_slogan()             → 슬로건 → brand_result 저장
    ├── generate_brand_story()        → 브랜드 스토리 → brand_result 저장
    ├── generate_color_palette()      → 컬러 정보 + PNG → brand_result 저장
    ├── generate_logo_images()        → 로고 이미지 경로 → brand_result 저장
    ├── generate_ad_copy()            → 광고 카피 → brand_result 저장
    ├── generate_menu_naming()        → 메뉴명 → brand_result 저장
    ├── generate_menu_naming_styles() → 메뉴 스타일 → brand_result 저장
    └── generate_multilingual()       → 다국어 결과 → brand_result 저장
            │
            ▼
    brand_result.json 최종 저장
    (errors 필드 포함)

```

---

### 📍 "파이프라인 실행 흐름"

```markdown
## 🔄 파이프라인 실행 흐름
### 단계별 실행 순서

1단계: brief.json 읽기 (load_brief)
        ↓
2단계: 브랜드 네이밍 생성 (generate_naming)
        ↓
3단계: 슬로건 생성 (generate_slogan)
        ↓
4단계: 브랜드 스토리 생성 (generate_brand_story)
        ↓
5단계: 컬러 팔레트 생성 & 시각화 (generate_color_palette)
        ↓
6단계: 로고 시안 생성 (generate_logo_images)
        ↓
7단계: 광고 카피 생성 (generate_ad_copy)
        ↓
8단계: 메뉴 네이밍 생성 (generate_menu_naming)
        ↓
9단계: 메뉴 네이밍 스타일 생성 (generate_menu_naming_styles)
        ↓
10단계: 다국어 변환 (generate_multilingual)
        ↓
11단계: TXT / PDF / JSON 저장 (save_txt / save_pdf / save_json)
```


---

### 📍 "컨텍스트 체인" 

```markdown
## 🔗 결과 저장 구조 (brand_result)

각 단계는 **brand_result 딕셔너리**에 결과를 누적 저장합니다.

```python
# brand_result 구조
brand_result = {
    "brand_name": "그린버거",        # brief.json에서 로드
    "industry": "친환경 패스트푸드",  # brief.json에서 로드
    "generated_content": {
        "naming": "...",             # generate_naming() 실행 후 저장
        "slogan": "...",             # generate_slogan() 실행 후 저장
        "brand_story": "...",        # generate_brand_story() 실행 후 저장
        "color_palette": {...},      # generate_color_palette() 실행 후 저장
        "logo_image_paths": [...],   # generate_logo_images() 실행 후 저장
        "ad_copy": "...",            # generate_ad_copy() 실행 후 저장
        "menu_naming": "...",        # generate_menu_naming() 실행 후 저장
        "menu_naming_styles": "...", # generate_menu_naming_styles() 실행 후 저장
        "multilingual": {
            "english": "...",        # generate_multilingual(brief, "en") 실행 후 저장
            "japanese": "..."        # generate_multilingual(brief, "ja") 실행 후 저장
        }
    },
    "errors": []  # 실패한 단계 기록
}
```

### 단계 간 데이터 흐름 예시

```
generate_naming() 실행
    → brand_result["generated_content"]["naming"] = "1. 초록한입 / Green Bite ..."
        ↓
generate_slogan() 실행
    → brand_result["generated_content"]["slogan"] = "맛있게, 가볍게, 그린버거 ..."
        ↓
generate_ad_copy() 실행
    → brand_result["generated_content"]["ad_copy"] = "1. 맛있게, 지구답게 ..."
        ↓
save_json() 실행
    → brand_result.json 최종 저장
```


## 🤖 프롬프트 엔지니어링 전략

### 1. 톤앤매너 고정
모든 프롬프트에 브랜드 톤을 명시하여 일관된 결과를 유도했습니다.


```python
prompt = f"""
브랜드명: {brand_name}
업종: {industry}
타겟: 20~30대 환경 관심 직장인
톤앤매너: 친근하고 트렌디하며 가볍지만 진정성 있는 어조

위 정보를 바탕으로 브랜드 슬로건 3개를 생성하세요.
"""
```

### 2. JSON 출력 강제화
GPT 응답을 JSON으로 고정하여 파싱 오류를 방지했습니다.

```python
prompt = f"""
반드시 아래 JSON 형식으로만 응답하세요. 다른 텍스트는 포함하지 마세요.

{{
  "main_color": {{
    "hex": "#색상코드",
    "name": "색상명",
    "reason": "선택 이유"
  }},
  "sub_colors": [...]
}}
"""
```

### 3. 포맷 제약 설계

출력 품질을 높이기 위해 개수, 형식, 언어를 명시했습니다.

```python
# 예: 광고 카피 10개 고정 출력
prompt = """
광고 카피를 정확히 10개 생성하세요.
형식: 번호. 카피 내용
예시:
1. 맛있게, 지구답게
2. 오늘 점심은 그린하게
"""
```

---

## 🛡️ 에러 핸들링 & 안정성 전략

### 1. API 실패 시 재시도 로직 (Retry + Backoff)

```python
import time

def call_api_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(...)
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 1초 → 2초 → 4초
                print(f"재시도 {attempt+1}/{max_retries} ({wait_time}초 대기)")
                time.sleep(wait_time)
            else:
                return None  # 최종 실패 시 None 반환
```

### 2. errors 필드로 실패 기록

API 호출 실패 시 결과 JSON의 `errors` 배열에 기록합니다.

```python
brand_result = {
    "brand_name": brand_name,
    "generated_content": {},
    "errors": []   # 초기화
}

# 각 단계 실행 시
try:
    result = generate_naming(brand_name)
    brand_result["generated_content"]["naming"] = result
except Exception as e:
    brand_result["errors"].append({
        "step": "naming",
        "message": str(e)
    })
```

**errors 필드 예시**

| 상황 | errors 필드 |
|------|-------------|
| 모든 단계 성공 | `"errors": []` |
| naming 단계 실패 | `"errors": [{"step": "naming", "message": "API timeout"}]` |
| 여러 단계 실패 | `"errors": [{"step": "naming", ...}, {"step": "logo", ...}]` |

### 3. 대체값(Fallback) 전략

API 실패 시 기본값을 사용하여 파이프라인이 중단되지 않도록 했습니다.

```python
result = generate_naming(brand_name)
if result is None:
    result = f"{brand_name} 브랜드 네이밍 생성 실패 - 기본값 사용"
```

---

## 📊 JSON 스키마 정의

`brand_result.json`의 전체 구조입니다.

```json
{
  "brand_name": "string",
  "industry": "string",
  "generated_content": {
    "naming": "string",
    "slogan": "string",
    "brand_story": "string",
    "color_palette": {
      "main_color": {
        "hex": "string (#RRGGBB)",
        "name": "string",
        "reason": "string"
      },
      "sub_colors": [
        {
          "hex": "string (#RRGGBB)",
          "name": "string",
          "reason": "string"
        }
      ]
    },
    "logo_image_paths": ["string"],
    "ad_copy": "string",
    "menu_naming": "string",
    "menu_naming_styles": "string",
    "multilingual": {
      "english": "string",
      "japanese": "string"
    }
  },
  "errors": [
    {
      "step": "string",
      "message": "string"
    }
  ],
  "metadata": {
    "generated_at": "string (YYYY-MM-DD HH:MM:SS)",
    "pipeline_version": "string",
    "status": "string (completed | partial | failed)"
  }
}
```

---

```markdown
## 🚀 단계별 작업 과정

### 1단계 - 환경 준비 (강민수 / 오승욱)
- Python 설치 확인
- VS Code 개발 환경 세팅
- 필요한 라이브러리 설치

```bash
pip install openai matplotlib fpdf requests
```

### 2단계 - OpenAI API 연결 (오승욱)
- API 키 발급 및 환경 설정
- baseURL 설정 및 GPT 모델 연결
- `brief.json` 파일로 브랜드 정보 입력 구조 설계

### 3단계 - 텍스트 콘텐츠 생성 (노현우 / 오승욱)
- 브랜드 네이밍 3~5개 + 의미 생성
- 슬로건 3개 생성
- 브랜드 스토리 작성
- 광고 카피 10개 생성
- 로고 컨셉 텍스트 생성

### 4단계 - 메뉴 네이밍 & 다국어 (오승욱 / 노현우)
- 트렌디형 / 프리미엄형 메뉴명 생성
- 영어 / 일본어 다국어 변환 기능 추가

### 5단계 - 시각화 & 파일 저장 (오승욱 / 노현우)
- matplotlib으로 컬러 팔레트 PNG 생성
- matplotlib으로 로고 시안 PNG 생성
- DALL-E로 AI 이미지 생성
- 결과물 TXT / PDF / JSON 자동 저장

### 6단계 - 결과물 정리 & GitHub 업로드 (오승욱)
- 전체 결과물 폴더 정리
- README.md 작성
- GitHub 포트폴리오 업로드

---

## 📸 결과물 예시


![프로그램 실행] 
<img width="762" height="494" alt="screentshot_1" src="https://github.com/user-attachments/assets/24acaede-c584-46ef-8b98-909a08bb4b7b" />  

![실행 화면]
<img width="926" height="3549" alt="screenshot_2" src="https://github.com/user-attachments/assets/2193804c-5586-45b5-9d83-6f5e5a41d224" />

![컬러 팔레트]
<img width="1485" height="619" alt="color_palette" src="https://github.com/user-attachments/assets/853094a5-d72b-4c8f-a8a7-1e0c53937b80" />

![로고 시안 1]
<img width="1024" height="1024" alt="logo_concept_1" src="https://github.com/user-attachments/assets/6e125069-4fee-475a-bb72-179ccf09fa3c" />

![로고 시안 2]
<img width="1024" height="1024" alt="logo_dalle_1" src="https://github.com/user-attachments/assets/97a1cafa-1748-4d72-801b-0ac7444ae024" />

![결과 화면]
<img width="438" height="236" alt="screentshot_3" src="https://github.com/user-attachments/assets/1cdae8b3-065f-46c8-bc8b-95910e76498e" />

---

## ⚠️ 작업 중 어려웠던 점 & 해결 과정

### 🔑 1. API 키 설정 문제
- 처음에 API 키 연결 방법을 몰라 오류 발생
- baseURL 설정 방식을 학습하여 해결

### 🖼️ 2. DALL-E 이미지 생성 오류
- 이미지 생성 요청 시 오류 반복 발생
- 오류 메시지를 분석하고 파라미터를 수정하여 해결

### 🔄 3. JSON 파싱 오류
- GPT 응답이 JSON 형식이 아닐 때 파싱 실패 발생
- 프롬프트에 JSON 형식 강제화 지시 추가로 해결

### 🐍 4. Python 코드 작성의 어려움
- 처음 접하는 라이브러리 사용법 숙지 필요
- 오류가 발생할 때마다 원인을 파악하고 수정하는 과정 반복

---

## 💡 배운 점

| 분야 | 배운 내용 |
|------|----------|
| 🔑 API 활용 | OpenAI API 키 발급, 연결, 호출 방법 |
| 💻 VS Code | 개발 환경 설정, 터미널 활용, 파일 관리 |
| 🐍 Python | 라이브러리 설치 및 활용, 파일 입출력, 오류 처리 |
| 🤖 AI 활용 | GPT 프롬프트 설계, DALL-E 이미지 생성 |
| 🛠️ 문제 해결 | 오류 메시지 분석 및 대처, 디버깅 능력 향상 |
| 📁 협업 도구 | GitHub 레포지토리 생성 및 포트폴리오 관리 |
| 🔗 모듈 설계 | 기능별 파일 분리, shared_state 컨텍스트 공유 |
| 🛡️ 안정성 | 재시도 로직, 에러 핸들링, fallback 전략 |

이 프로젝트를 통해 단순히 코드를 작성하는 것을 넘어,  
**오류를 스스로 분석하고 해결하는 능력**과  
**AI API를 활용한 실전 파이프라인 설계 경험**을 쌓을 수 있었습니다. 🚀

---

## 👤 팀 프로젝트 인원

| 이름 | 역할 |
|------|------|
| 오승욱 | API 연결, 전체 파이프라인 설계, GitHub 관리 |
| 노현우 | 텍스트 콘텐츠 생성, 메뉴 네이밍, 다국어 |
| 강민수 | 환경 세팅, 시각화, 파일 저장 |
