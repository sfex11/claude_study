# 🤗 Hugging Face Spaces 빠른 배포 가이드

이 가이드는 AI 학습 프로그램 생성기를 Hugging Face Spaces에 배포하는 방법을 단계별로 설명합니다.

## 📋 사전 준비

- [ ] Hugging Face 계정 (무료)
- [ ] Google Gemini API 키 (무료)
- [ ] (선택) Supabase 계정 및 프로젝트

---

## 🚀 단계별 배포

### 1단계: Hugging Face Space 생성

1. **Hugging Face 로그인**
   - https://huggingface.co/ 방문
   - 계정이 없다면 무료로 가입

2. **새 Space 생성**
   - https://huggingface.co/new-space 방문
   - 또는 프로필 → "Spaces" → "Create new Space"

3. **Space 설정**
   ```
   Owner: [Your Username]
   Space name: ai-learning-program-generator (원하는 이름)
   License: MIT
   Select the Space SDK: Streamlit ⭐ 중요!
   Space hardware: CPU basic (Free)
   Visibility: Public 또는 Private
   ```

4. **"Create Space" 클릭**

---

### 2단계: 파일 업로드

#### 방법 A: Git을 통한 배포 (추천) 🎯

```bash
# 1. Hugging Face Space 리포지토리 클론
git clone https://huggingface.co/spaces/[YOUR_USERNAME]/ai-learning-program-generator
cd ai-learning-program-generator

# 2. 프로젝트 파일 복사
# 현재 claude_study 디렉토리에서:
cp app.py ../ai-learning-program-generator/
cp requirements.txt ../ai-learning-program-generator/
cp README.md ../ai-learning-program-generator/
cp -r .streamlit ../ai-learning-program-generator/

# 3. (선택) 추가 파일 복사
cp .huggingface.yml ../ai-learning-program-generator/
cp supabase_schema.sql ../ai-learning-program-generator/

# 4. 커밋 및 푸시
cd ../ai-learning-program-generator
git add .
git commit -m "Initial deployment: AI Learning Program Generator"
git push
```

#### 방법 B: 웹 인터페이스를 통한 배포

1. Space 페이지 → "Files and versions" 탭
2. "Add file" → "Upload files" 클릭
3. 다음 파일들을 드래그 앤 드롭:
   - `app.py` ✅ 필수
   - `requirements.txt` ✅ 필수
   - `README.md` (선택)
   - `.streamlit/config.toml` (선택)
4. "Commit changes to main" 클릭

---

### 3단계: 환경 변수 설정 (Secrets) 🔐

**매우 중요!** API 키를 설정해야 앱이 작동합니다.

1. **Settings 페이지 이동**
   - Space 페이지에서 "Settings" 탭 클릭

2. **Repository secrets 추가**

   스크롤해서 "Repository secrets" 섹션 찾기

   **필수 Secret:**
   ```
   Name: GOOGLE_API_KEY
   Value: [Your Google Gemini API Key]
   ```
   "Add a secret" 클릭

   **선택 Secrets (Supabase 사용 시):**
   ```
   Name: SUPABASE_URL
   Value: https://xxxxx.supabase.co
   ```
   "Add a secret" 클릭

   ```
   Name: SUPABASE_KEY
   Value: [Your Supabase Anon Key]
   ```
   "Add a secret" 클릭

3. **Secrets 저장 확인**
   - 각 secret 추가 후 목록에 표시되는지 확인
   - ⚠️ 값은 보안상 표시되지 않음 (정상)

---

### 4단계: 배포 확인 ✅

1. **자동 빌드 대기**
   - Space 페이지로 돌아가기
   - "Building..." 메시지 확인
   - 보통 2-3분 소요

2. **앱 실행 확인**
   - 빌드 완료 후 앱이 자동으로 로드됨
   - URL: `https://huggingface.co/spaces/[YOUR_USERNAME]/ai-learning-program-generator`

3. **테스트**
   - "새 프로그램 생성" 탭에서 간단한 주제 입력
   - 프로그램 생성이 정상 작동하는지 확인

---

## 🎉 완료!

이제 다음이 가능합니다:

- ✅ 전 세계 어디서나 앱 접속 가능
- ✅ GitHub 저장소 push 시 자동 재배포
- ✅ 리부팅 없이 즉시 변경사항 반영
- ✅ Hugging Face 커뮤니티에 앱 공유

---

## 🔧 문제 해결

### 앱이 실행되지 않는 경우

1. **로그 확인**
   - Space 페이지 하단의 "Logs" 탭 확인
   - 에러 메시지 확인

2. **흔한 문제들**

   **문제: "GOOGLE_API_KEY가 설정되지 않았습니다"**
   ```
   해결: Settings → Repository secrets에서
   GOOGLE_API_KEY가 올바르게 추가되었는지 확인
   ```

   **문제: "Module not found: streamlit"**
   ```
   해결: requirements.txt 파일이 업로드되었는지 확인
   Space 설정에서 SDK가 "Streamlit"로 선택되었는지 확인
   ```

   **문제: 앱이 로딩 중 멈춤**
   ```
   해결: Space 페이지에서 "Restart this Space" 클릭
   또는 Settings에서 "Factory reboot" 실행
   ```

3. **재시작 방법**
   - Settings → "Factory reboot" → "Reboot Space"

---

## 📝 업데이트 방법

### Git을 사용하는 경우

```bash
cd ai-learning-program-generator
# 파일 수정 후
git add .
git commit -m "Update: [변경 내용 설명]"
git push
# 자동으로 재배포됨 (30초~1분)
```

### 웹 인터페이스를 사용하는 경우

1. Space 페이지 → "Files and versions"
2. 수정할 파일 클릭
3. 우측 상단 "Edit" 클릭
4. 수정 후 "Commit changes to main"

---

## 🌟 추가 기능

### Space를 Public으로 만들기

Settings → "Space visibility" → "Public"로 변경

### Space 카드 커스터마이징

README.md 상단에 메타데이터 추가:

```yaml
---
title: AI 학습 프로그램 생성기
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.31.0
app_file: app.py
pinned: false
---
```

### 커뮤니티 공유

- Hugging Face 피드에 Space 공유
- Twitter, LinkedIn 등에 링크 공유
- README에 데모 링크 추가

---

## 🆚 Streamlit Cloud vs Hugging Face Spaces

| 항목 | Streamlit Cloud | Hugging Face Spaces |
|------|-----------------|---------------------|
| 배포 속도 | 빠름 | 빠름 |
| 자동 재배포 | ✅ | ✅ |
| 리부팅 필요 | ⚠️ 때때로 | ❌ 불필요 |
| 무료 티어 | 제한적 | 관대함 |
| 커뮤니티 | Streamlit | AI/ML 전문 |
| 난이도 | 매우 쉬움 | 쉬움 |
| 추천도 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 📞 도움말

- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces
- **Streamlit Docs**: https://docs.streamlit.io/
- **프로젝트 Issues**: GitHub Issues에 문의

---

**축하합니다! 🎉**

이제 AI 학습 프로그램 생성기가 전 세계에 공개되었습니다!
