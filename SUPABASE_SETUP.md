# 🗄️ Supabase 설정 가이드

이 가이드는 학습 프로그램 데이터를 영구적으로 저장하기 위해 Supabase를 설정하는 방법을 설명합니다.

## 📋 Supabase란?

Supabase는 오픈소스 Firebase 대안으로, PostgreSQL 기반의 백엔드 서비스입니다.

**장점:**
- ✅ 무료 티어 제공 (500MB 데이터베이스, 무제한 API 요청)
- ✅ 실시간 데이터 동기화
- ✅ 사용자 인증 지원 (향후 추가 예정)
- ✅ SQL 쿼리 사용 가능

## 🚀 빠른 시작

### 1. Supabase 프로젝트 생성

1. [Supabase](https://supabase.com/) 접속
2. "Start your project" 또는 "New Project" 클릭
3. 조직(Organization) 생성 (없는 경우)
4. 프로젝트 정보 입력:
   - **Name**: `learning-program-generator` (또는 원하는 이름)
   - **Database Password**: 강력한 비밀번호 생성 (저장해두세요!)
   - **Region**: 가장 가까운 지역 선택 (예: Northeast Asia - Seoul)
5. "Create new project" 클릭
6. 프로젝트 생성 완료까지 1-2분 대기

### 2. 데이터베이스 스키마 생성

1. Supabase 프로젝트 대시보드에서 **SQL Editor** 클릭
2. "New query" 클릭
3. `supabase_schema.sql` 파일의 내용을 복사하여 붙여넣기
4. "Run" 또는 `Ctrl+Enter` 실행
5. ✅ 성공 메시지 확인

### 3. API 키 가져오기

1. 프로젝트 대시보드에서 **Settings** (설정) 클릭
2. **API** 섹션 선택
3. 다음 정보를 복사:
   - **Project URL**: `https://xxxxx.supabase.co` 형식
   - **anon public** 키 (Public 아래의 긴 문자열)

⚠️ **주의**: `service_role` 키가 아닌 `anon` 키를 사용하세요!

### 4. 환경 변수 설정

#### 로컬 개발 (.env 파일)

`.env` 파일에 다음 내용 추가:

```bash
GOOGLE_API_KEY=your_google_api_key_here

# Supabase 설정
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_anon_key_here
```

#### Streamlit Cloud 배포

1. Streamlit Cloud 앱 대시보드에서 **Settings** 클릭
2. **Secrets** 탭 선택
3. 다음 내용 추가:

```toml
GOOGLE_API_KEY = "your_google_api_key_here"

SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_KEY = "your_anon_key_here"
```

4. "Save" 클릭

## 🔍 데이터 확인하기

### Table Editor에서 확인

1. Supabase 대시보드에서 **Table Editor** 클릭
2. `learning_programs` 테이블 선택
   - 생성된 학습 프로그램 목록 확인
3. `learning_progress` 테이블 선택
   - 학습 진행도 데이터 확인

### SQL 쿼리로 확인

SQL Editor에서 다음 쿼리 실행:

```sql
-- 모든 학습 프로그램 조회
SELECT * FROM learning_programs ORDER BY created_at DESC;

-- 특정 프로그램의 진행도 조회
SELECT
    lp.topic,
    lprog.completed_weeks,
    lprog.notes
FROM learning_programs lp
LEFT JOIN learning_progress lprog ON lp.id = lprog.program_id
ORDER BY lp.created_at DESC;
```

## 🔧 문제 해결

### 연결 오류

```
Supabase 연결 실패: ...
```

**해결 방법:**
1. SUPABASE_URL과 SUPABASE_KEY가 올바른지 확인
2. Supabase 프로젝트가 활성 상태인지 확인
3. 인터넷 연결 확인

### 데이터가 저장되지 않음

**해결 방법:**
1. SQL Editor에서 `supabase_schema.sql` 실행 여부 확인
2. Table Editor에서 테이블이 생성되었는지 확인
3. anon 키를 사용하는지 확인 (service_role 키 아님)

### 데이터가 로드되지 않음

**해결 방법:**
1. 브라우저를 새로고침하여 앱 재시작
2. Supabase API 키가 올바른지 확인
3. 브라우저 콘솔에서 에러 메시지 확인

## 📊 데이터베이스 스키마

### learning_programs 테이블

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | UUID | 고유 ID (자동 생성) |
| topic | TEXT | 학습 주제 |
| level | TEXT | 학습 수준 |
| duration | TEXT | 학습 기간 |
| learning_style | TEXT | 학습 스타일 |
| content | TEXT | 프로그램 내용 (Markdown) |
| created_at | TIMESTAMP | 생성 시간 |
| updated_at | TIMESTAMP | 수정 시간 |

### learning_progress 테이블

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | UUID | 고유 ID (자동 생성) |
| program_id | UUID | 학습 프로그램 ID (외래키) |
| completed_weeks | JSONB | 완료한 주차 배열 |
| notes | TEXT | 학습 노트 |
| updated_at | TIMESTAMP | 수정 시간 |

## 🔒 보안 (향후 개선)

현재는 모든 사용자가 모든 데이터에 접근 가능합니다.

**향후 계획:**
- 사용자 인증 추가 (Supabase Auth)
- Row Level Security (RLS) 활성화
- 사용자별 데이터 격리

## 💡 유용한 팁

1. **백업**: Supabase는 자동 백업을 제공하지만, 중요한 데이터는 정기적으로 내보내기를 권장합니다.

2. **데이터 내보내기**:
   ```sql
   -- CSV로 내보내기 (Table Editor에서 Export 버튼 사용)
   SELECT * FROM learning_programs;
   ```

3. **무료 티어 제한**:
   - 500MB 데이터베이스
   - 2GB 데이터 전송/월
   - 무제한 API 요청
   - 일반 사용에는 충분합니다!

4. **모니터링**: Settings > Usage에서 사용량 확인 가능

## 📞 추가 도움

- [Supabase 공식 문서](https://supabase.com/docs)
- [Supabase Python 클라이언트 문서](https://supabase.com/docs/reference/python/introduction)
- 이슈가 있다면 GitHub Issues에 등록해주세요

---

이제 학습 프로그램이 클라우드에 안전하게 저장됩니다! 🎉
