# 📚 AI 학습 프로그램 생성기

Google Gemini AI를 활용한 맞춤형 학습 프로그램 자동 생성 및 관리 웹 앱입니다.

## ✨ 주요 기능

- 🎯 **맞춤형 학습 프로그램 생성**: 주제, 수준, 기간, 학습 스타일에 따른 AI 기반 커리큘럼 자동 생성
- 📖 **체계적인 커리큘럼**: 주차별 학습 내용, 추천 자료, 실습 과제 포함
- 📈 **진행도 추적**: 주차별 체크리스트와 학습 노트 기능
- 💾 **프로그램 저장**: 생성된 학습 프로그램을 Markdown 파일로 다운로드
- 🔄 **여러 프로그램 관리**: 동시에 여러 학습 주제를 관리

## 🚀 빠른 시작 (로컬 실행)

### 1. 저장소 클론

```bash
git clone <repository-url>
cd claude_study
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 API 키를 입력하세요:

```bash
cp .env.example .env
```

`.env` 파일을 열어 다음과 같이 설정:

```
GOOGLE_API_KEY=your_actual_api_key_here
```

**Google Gemini API 키 발급 방법 (무료!):**
1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. Google 계정으로 로그인
3. "Get API Key" 또는 "Create API Key" 버튼 클릭
4. 생성된 키를 복사하여 `.env` 파일에 붙여넣기

💡 **참고**: Gemini API는 무료 티어를 제공하여 비용 걱정 없이 사용할 수 있습니다!

### 5. 앱 실행

```bash
streamlit run app.py
```

브라우저가 자동으로 열리며 `http://localhost:8501`에서 앱을 확인할 수 있습니다.

## ☁️ Streamlit Cloud 배포 (무료)

### 1. GitHub 저장소 준비

```bash
git add .
git commit -m "Initial commit: AI Learning Program Generator"
git push origin main
```

### 2. Streamlit Cloud 배포

1. [Streamlit Cloud](https://share.streamlit.io/) 접속
2. GitHub 계정으로 로그인
3. "New app" 버튼 클릭
4. 저장소 선택:
   - Repository: `your-username/claude_study`
   - Branch: `main`
   - Main file path: `app.py`
5. "Deploy!" 클릭

### 3. API 키 설정 (Secrets)

배포 후 앱 설정에서:

1. 앱 대시보드에서 "Settings" 클릭
2. "Secrets" 탭 선택
3. 다음 내용 입력:

```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```

4. "Save" 클릭
5. 앱이 자동으로 재시작됩니다

### 4. 배포 완료!

몇 분 후 `https://your-app-name.streamlit.app` 형태의 URL로 접속 가능합니다.

## 📋 사용 방법

### 1. 새 학습 프로그램 생성

1. **"새 프로그램 생성"** 탭 선택
2. 학습 주제 입력 (예: "파이썬 프로그래밍", "머신러닝 기초")
3. 현재 수준 선택 (초급/중급/고급)
4. 학습 기간 선택 (1주일~6개월)
5. 학습 스타일 선택 (이론/실습/프로젝트/혼합)
6. **"학습 프로그램 생성하기"** 버튼 클릭
7. AI가 맞춤형 커리큘럼을 생성합니다

### 2. 프로그램 확인

- **"현재 프로그램"** 탭에서 생성된 커리큘럼 확인
- 주차별 학습 내용, 추천 자료, 실습 과제 등 포함
- Markdown 파일로 다운로드 가능

### 3. 진행도 관리

- **"진행도 관리"** 탭 선택
- 주차별 체크박스로 완료 표시
- 진행률 자동 계산
- 학습 노트 작성 기능

## 🛠️ 기술 스택

- **Frontend/Backend**: Streamlit
- **AI**: Google Gemini Pro (무료!)
- **Language**: Python 3.8+
- **Deployment**: Streamlit Cloud

## 📁 프로젝트 구조

```
claude_study/
├── app.py                      # 메인 Streamlit 앱
├── requirements.txt            # Python 패키지 의존성
├── .env.example               # 환경 변수 예시
├── .gitignore                 # Git 무시 파일
├── .streamlit/
│   ├── config.toml            # Streamlit 설정
│   └── secrets.toml.example   # Secrets 예시
└── README.md                  # 프로젝트 문서
```

## 🔒 보안

- API 키는 절대 코드에 직접 입력하지 마세요
- 로컬: `.env` 파일 사용 (`.gitignore`에 포함됨)
- 배포: Streamlit Cloud Secrets 사용
- `.env` 파일은 절대 Git에 커밋하지 마세요

## 💡 사용 팁

1. **구체적인 주제 입력**: "프로그래밍" 보다 "Python 웹 크롤링"처럼 구체적으로 입력
2. **현실적인 기간 설정**: 주제의 난이도에 맞게 충분한 기간 설정
3. **정기적인 진행도 업데이트**: 매주 진행도를 업데이트하여 동기 부여
4. **학습 노트 활용**: 배운 내용, 질문, 어려운 점 등을 기록

## 🆘 문제 해결

### API 키 오류
```
⚠️ GOOGLE_API_KEY가 설정되지 않았습니다
```
- `.env` 파일 또는 Streamlit Secrets에 API 키가 올바르게 설정되었는지 확인
- API 키가 유효한지 [Google AI Studio](https://makersuite.google.com/app/apikey)에서 확인

### 패키지 설치 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Streamlit Cloud 배포 오류
- `requirements.txt`가 저장소 루트에 있는지 확인
- Secrets가 올바르게 설정되었는지 확인
- 앱 로그를 확인하여 구체적인 오류 메시지 파악

## 🔄 업데이트 및 개선 계획

- [ ] 웹 검색 통합 (실시간 학습 자료 검색)
- [ ] 사용자 인증 시스템
- [ ] 학습 통계 및 분석 대시보드
- [ ] 모바일 최적화
- [ ] 다국어 지원

## 📄 라이선스

MIT License

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

## 📞 문의

프로젝트 관련 질문이나 제안사항이 있으시면 이슈를 등록해주세요.

---

Made with ❤️ using Google Gemini AI & Streamlit
