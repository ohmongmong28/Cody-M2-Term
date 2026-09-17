# Cody-M2-Term
코디세이 네이티브 팀미션2
---

# 🎨 AI 브랜드 생성기 (AI Brand Generator)

> OpenAI API를 활용한 자동 브랜드 아이덴티티 생성 CLI 프로젝트

---

## 📌 프로젝트 소개
브랜드 정보를 입력하면 AI가 자동으로
브랜드 네이밍, 슬로건, 스토리, 광고 카피,
메뉴명, 로고 컨셉까지 한 번에 생성해주는 도구입니다.

---

## ⚙️ 주요 기능
- ✅ 브랜드 네이밍 생성 (3~5개 + 의미 설명)
- ✅ 슬로건 & 브랜드 스토리 생성
- ✅ 광고 카피 10개 자동 생성
- ✅ 메뉴 네이밍 (트렌디형 / 프리미엄형)
- ✅ 다국어 지원 (영어 / 일본어)
- ✅ 로고 컨셉 & 컬러 팔레트 시각화 (PNG)
- ✅ TXT / PDF / JSON 자동 저장
- ✅ DALL-E AI 이미지 생성

---

## 🛠️ 사용 기술

| 기술 | 용도 |
|------|------|
| Python | 메인 언어 |
| OpenAI API (GPT / DALL-E) | 텍스트 & 이미지 생성 |
| matplotlib | 로고 & 컬러 팔레트 시각화 |
| fpdf | PDF 보고서 저장 |
| json | 구조화 데이터 저장 |
| VS Code | 개발 환경 |

---

## 🚀 단계별 작업 과정

### 1단계 - 환경 준비 (강민수/오승욱)
- Python 설치 확인
- VS Code 개발 환경 세팅
- 필요한 라이브러리 설치
- `pip install openai matplotlib fpdf requests`

### 2단계 - OpenAI API 연결 (오승욱)
- API 키 발급 및 환경 설정
- baseURL 설정 및 GPT 모델 연결
- `brief.json` 파일로 브랜드 정보 입력 구조 설계

### 3단계 - 텍스트 콘텐츠 생성 (노현우/오승욱)
- 브랜드 네이밍 3~5개 + 의미 생성
- 슬로건 3개 생성
- 브랜드 스토리 작성
- 광고 카피 10개 생성
- 로고 컨셉 텍스트 생성

### 4단계 - 메뉴 네이밍 & 다국어 (오승욱/노현우)
- 트렌디형 / 프리미엄형 메뉴명 생성
- 영어 / 일본어 다국어 변환 기능 추가

### 5단계 - 시각화 & 파일 저장 (오승욱/노현우)
- matplotlib으로 컬러 팔레트 PNG 생성
- matplotlib으로 로고 시안 PNG 생성
- DALL-E로 AI 이미지 생성
- 결과물 TXT / PDF / JSON 자동 저장

### 6단계 - 결과물 정리 & GitHub 업로드 (오승욱)
- 전체 결과물 폴더 정리
- README.md 작성
- GitHub 포트폴리오 업로드

---

## 📁 결과물 구조

```
brand_output/
├── brand_output.txt    (전체 텍스트)
├── brand_output.pdf    (PDF 보고서)
├── brand_result.json   (구조화 데이터)
├── color_palette.png   (컬러 팔레트)
├── logo_concept_1.png  (로고 시안 1)
└── logo_concept_2.png  (로고 시안 2)
```

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

### 🐍 3. Python 코드 작성의 어려움
- 처음 접하는 라이브러리 사용법 숙지 필요
- 오류가 발생할 때마다 원인을 파악하고 수정하는 과정 반복

---

## 💡 배운 점

| 분야 | 배운 내용 |
|------|-----------|
| 🔑 API 활용 | OpenAI API 키 발급, 연결, 호출 방법 |
| 💻 VS Code | 개발 환경 설정, 터미널 활용, 파일 관리 |
| 🐍 Python | 라이브러리 설치 및 활용, 파일 입출력, 오류 처리 |
| 🤖 AI 활용 | GPT 프롬프트 설계, DALL-E 이미지 생성 |
| 🛠️ 문제 해결 | 오류 메시지 분석 및 대처, 디버깅 능력 향상 |
| 📁 협업 도구 | GitHub 레포지토리 생성 및 포트폴리오 관리 |

> 이 프로젝트를 통해 단순히 코드를 작성하는 것을 넘어,
> **오류를 스스로 분석하고 해결하는 능력**을 키울 수 있었습니다. 🚀

---

## 👤 텀 프로젝트 인원
- **이름**: 오승욱 / 노현우 / 강민수
