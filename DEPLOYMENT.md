# 배포 가이드

## Hugging Face Spaces 배포 (추천)

### 1. 사전 준비
```bash
# README.md에 앱 설명 추가 (이미 존재함)
# requirements.txt 확인 (이미 존재함)
```

### 2. Hugging Face Spaces 설정

1. https://huggingface.co/spaces 방문
2. "Create new Space" 클릭
3. 설정:
   - Space name: `claude-study`
   - SDK: **Streamlit**
   - License: MIT
   - Visibility: Public (또는 Private)

### 3. 파일 업로드

**방법 A: GitHub 연동 (추천)**
```bash
# Hugging Face Space의 Git 리포지토리 클론
git clone https://huggingface.co/spaces/[YOUR_USERNAME]/claude-study
cd claude-study

# 현재 프로젝트 파일 복사
cp /path/to/claude_study/app.py .
cp /path/to/claude_study/requirements.txt .
cp /path/to/claude_study/supabase_schema.sql .

# 커밋 및 푸시
git add .
git commit -m "Initial deployment"
git push
```

**방법 B: 웹 인터페이스**
- Hugging Face Spaces 대시보드에서 직접 파일 업로드

### 4. 환경 변수 설정

Hugging Face Spaces 설정 페이지에서:
- Settings > Repository secrets
- 다음 변수 추가:
  - `GOOGLE_API_KEY`: [Your API Key]
  - `SUPABASE_URL`: [Your Supabase URL]
  - `SUPABASE_KEY`: [Your Supabase Key]

### 5. 자동 배포

- GitHub에 push하면 자동으로 재배포
- 보통 30초 내 반영
- 리부팅 불필요

---

## Render 배포

### 1. render.yaml 생성

```yaml
services:
  - type: web
    name: claude-study
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
    envVars:
      - key: GOOGLE_API_KEY
        sync: false
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
```

### 2. Render 설정

1. https://render.com 방문
2. GitHub 연동
3. "New Web Service" 선택
4. 리포지토리 선택
5. 환경 변수 입력
6. "Create Web Service" 클릭

### 3. 주의사항

- 무료 티어는 15분 비활성 시 슬립
- 첫 요청 시 30초~1분 대기 (콜드 스타트)
- 개인 프로젝트에는 충분함

---

## Streamlit Cloud (현재)

### 장점
- 가장 쉬움
- Streamlit 공식
- GitHub 자동 연동

### 단점
- 리부팅 필요할 수 있음
- 캐시 문제

### 권장 워크플로우
```bash
# 1. 코드 수정 후 커밋
git add .
git commit -m "Update feature"
git push

# 2. Streamlit Cloud 대시보드에서 확인
# 3. 필요시 "Reboot app" 클릭
# 4. 브라우저 하드 리프레시 (Ctrl+Shift+R)
```

---

## 플랫폼 비교표

| 플랫폼 | 무료 티어 | 자동 배포 | 리부팅 필요 | 난이도 | 추천도 |
|--------|-----------|-----------|-------------|--------|--------|
| Hugging Face | ✅ 넉넉함 | ✅ | ❌ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Render | ✅ 제한적 | ✅ | ❌ | ⭐⭐ | ⭐⭐⭐⭐ |
| Streamlit Cloud | ✅ | ✅ | ⚠️ 때때로 | ⭐ | ⭐⭐⭐ |
| Railway | ❌ 유료 | ✅ | ❌ | ⭐⭐ | ⭐⭐ |
| Google Cloud Run | ✅ 넉넉함 | ⚠️ 복잡 | ❌ | ⭐⭐⭐⭐ | ⭐⭐ |

---

## 추천 결론

### 최우선 추천: Hugging Face Spaces
- Streamlit 완벽 지원
- 무료 티어 관대
- 리부팅 문제 없음
- AI/ML 커뮤니티 노출

### 차선책: Render
- 슬립 모드 있지만 개인 프로젝트에 충분
- 설정 간단
- 프로덕션 레벨

### 현재 유지: Streamlit Cloud
- 리부팅 문제 감수하면 가장 쉬움
- 버전 표시 추가로 혼란 방지
