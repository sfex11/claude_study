import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="AI 학습 프로그램 생성기",
    page_icon="📚",
    layout="wide"
)

# 세션 스테이트 초기화
if 'learning_programs' not in st.session_state:
    st.session_state.learning_programs = []
if 'current_program' not in st.session_state:
    st.session_state.current_program = None
if 'progress' not in st.session_state:
    st.session_state.progress = {}
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'daily_materials' not in st.session_state:
    st.session_state.daily_materials = {}  # {program_id: {day_number: content}}
if 'current_day' not in st.session_state:
    st.session_state.current_day = None

# Supabase 클라이언트 초기화
@st.cache_resource
def get_supabase_client():
    """Supabase 클라이언트를 초기화하고 캐시합니다."""
    supabase_url = os.getenv('SUPABASE_URL') or st.secrets.get('SUPABASE_URL', '')
    supabase_key = os.getenv('SUPABASE_KEY') or st.secrets.get('SUPABASE_KEY', '')

    if not supabase_url or not supabase_key:
        return None

    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        st.error(f"Supabase 연결 실패: {str(e)}")
        return None

# Supabase에 학습 프로그램 저장
def save_program_to_supabase(program):
    """학습 프로그램을 Supabase에 저장합니다."""
    supabase = get_supabase_client()
    if not supabase:
        return None

    try:
        data = {
            'topic': program['topic'],
            'level': program['level'],
            'duration': program['duration'],
            'learning_style': program['learning_style'],
            'content': program['content']
        }

        # 기존 프로그램이면 업데이트, 아니면 삽입
        if 'supabase_id' in program and program['supabase_id']:
            result = supabase.table('learning_programs').update(data).eq('id', program['supabase_id']).execute()
        else:
            result = supabase.table('learning_programs').insert(data).execute()
            if result.data and len(result.data) > 0:
                return result.data[0]['id']

        return program.get('supabase_id')
    except Exception as e:
        st.error(f"프로그램 저장 실패: {str(e)}")
        return None

# Supabase에서 학습 프로그램 로드
def load_programs_from_supabase():
    """Supabase에서 모든 학습 프로그램을 로드합니다."""
    supabase = get_supabase_client()
    if not supabase:
        return []

    try:
        result = supabase.table('learning_programs').select('*').order('created_at', desc=True).execute()
        programs = []

        for idx, item in enumerate(result.data):
            program = {
                'id': idx,
                'supabase_id': item['id'],
                'topic': item['topic'],
                'level': item['level'],
                'duration': item['duration'],
                'learning_style': item['learning_style'],
                'content': item['content'],
                'created_at': item['created_at']
            }
            programs.append(program)

        return programs
    except Exception as e:
        st.error(f"프로그램 로드 실패: {str(e)}")
        return []

# Supabase에 진행도 저장
def save_progress_to_supabase(program_id, supabase_id, progress_data):
    """학습 진행도를 Supabase에 저장합니다."""
    supabase = get_supabase_client()
    if not supabase or not supabase_id:
        return

    try:
        data = {
            'program_id': supabase_id,
            'completed_weeks': json.dumps(progress_data.get('completed_weeks', [])),
            'notes': progress_data.get('notes', '')
        }

        # 기존 진행도 확인
        existing = supabase.table('learning_progress').select('*').eq('program_id', supabase_id).execute()

        if existing.data and len(existing.data) > 0:
            # 업데이트
            supabase.table('learning_progress').update(data).eq('program_id', supabase_id).execute()
        else:
            # 삽입
            supabase.table('learning_progress').insert(data).execute()
    except Exception as e:
        st.error(f"진행도 저장 실패: {str(e)}")

# Supabase에서 진행도 로드
def load_progress_from_supabase(supabase_id):
    """Supabase에서 특정 프로그램의 진행도를 로드합니다."""
    supabase = get_supabase_client()
    if not supabase or not supabase_id:
        return {'completed_weeks': [], 'notes': ''}

    try:
        result = supabase.table('learning_progress').select('*').eq('program_id', supabase_id).execute()

        if result.data and len(result.data) > 0:
            item = result.data[0]
            return {
                'completed_weeks': json.loads(item['completed_weeks']) if isinstance(item['completed_weeks'], str) else item['completed_weeks'],
                'notes': item['notes']
            }

        return {'completed_weeks': [], 'notes': ''}
    except Exception as e:
        st.error(f"진행도 로드 실패: {str(e)}")
        return {'completed_weeks': [], 'notes': ''}

# Supabase에 일자별 학습자료 저장
def save_daily_material_to_supabase(supabase_id, day_number, content):
    """일자별 학습자료를 Supabase에 저장합니다."""
    supabase = get_supabase_client()
    if not supabase or not supabase_id:
        return False

    try:
        data = {
            'program_id': supabase_id,
            'day_number': day_number,
            'content': content
        }

        # 기존 자료 확인
        existing = supabase.table('daily_materials').select('*').eq('program_id', supabase_id).eq('day_number', day_number).execute()

        if existing.data and len(existing.data) > 0:
            # 업데이트
            supabase.table('daily_materials').update(data).eq('program_id', supabase_id).eq('day_number', day_number).execute()
        else:
            # 삽입
            supabase.table('daily_materials').insert(data).execute()

        return True
    except Exception as e:
        st.error(f"일자별 학습자료 저장 실패: {str(e)}")
        return False

# Supabase에서 일자별 학습자료 로드
def load_daily_materials_from_supabase(supabase_id):
    """Supabase에서 특정 프로그램의 모든 일자별 학습자료를 로드합니다."""
    supabase = get_supabase_client()
    if not supabase or not supabase_id:
        return {}

    try:
        result = supabase.table('daily_materials').select('*').eq('program_id', supabase_id).order('day_number').execute()

        materials = {}
        for item in result.data:
            materials[item['day_number']] = item['content']

        return materials
    except Exception as e:
        st.error(f"일자별 학습자료 로드 실패: {str(e)}")
        return {}

# 앱 시작 시 데이터 로드
if not st.session_state.data_loaded:
    programs = load_programs_from_supabase()
    if programs:
        st.session_state.learning_programs = programs
        # 진행도와 일자별 학습자료 로드
        for program in programs:
            if 'supabase_id' in program:
                progress = load_progress_from_supabase(program['supabase_id'])
                st.session_state.progress[program['id']] = progress

                # 일자별 학습자료 로드
                materials = load_daily_materials_from_supabase(program['supabase_id'])
                if materials:
                    st.session_state.daily_materials[program['id']] = materials
    st.session_state.data_loaded = True

# Google Gemini API 초기화
def get_gemini_model():
    api_key = os.getenv('GOOGLE_API_KEY') or st.secrets.get('GOOGLE_API_KEY', '')
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEY가 설정되지 않았습니다. .env 파일 또는 Streamlit secrets를 확인해주세요.")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash-lite')

# Google Gemini API를 사용한 학습 프로그램 생성
def generate_learning_program(topic, level, duration, learning_style):
    model = get_gemini_model()

    prompt = f"""당신은 교육 전문가입니다. 다음 주제에 대한 체계적인 학습 프로그램을 만들어주세요.

주제: {topic}
학습자 수준: {level}
학습 기간: {duration}
학습 스타일: {learning_style}

다음 형식으로 상세한 학습 프로그램을 작성해주세요:

1. 학습 목표
2. 주차별 커리큘럼 (각 주차마다 구체적인 학습 내용과 활동 포함)
3. 추천 학습 자료 (온라인 강의, 책, 웹사이트 등)
4. 실습 과제
5. 평가 방법
6. 학습 팁

JSON 형식이 아닌 읽기 쉬운 마크다운 형식으로 작성해주세요."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"프로그램 생성 중 오류 발생: {str(e)}")
        return None

# 학습 기간을 일수로 변환
def get_duration_in_days(duration):
    """학습 기간을 일수로 변환합니다."""
    duration_map = {
        "1주일": 7,
        "2주일": 14,
        "1개월": 30,
        "2개월": 60,
        "3개월": 90,
        "6개월": 180
    }
    return duration_map.get(duration, 30)

# 일자별 학습자료 생성
def generate_daily_material(topic, level, duration, learning_style, day_number, total_days):
    """특정 일자의 학습자료를 생성합니다."""
    model = get_gemini_model()

    prompt = f"""당신은 교육 전문가입니다. 다음 학습 프로그램의 {day_number}일차 학습자료를 만들어주세요.

학습 프로그램 정보:
- 주제: {topic}
- 학습자 수준: {level}
- 전체 학습 기간: {duration} (총 {total_days}일)
- 학습 스타일: {learning_style}
- 현재 일차: {day_number}일차

다음 형식으로 오늘의 학습자료를 작성해주세요:

# Day {day_number}: [오늘의 주제]

## 📚 오늘의 학습 목표
- 구체적인 학습 목표 3-5개

## 📖 학습 내용
- 오늘 배울 핵심 개념과 상세 설명
- 예제 코드나 사례 포함

## 💻 실습 과제
- 직접 해볼 수 있는 실습 과제 2-3개
- 난이도별로 제시

## ❓ 퀴즈
- 오늘 배운 내용을 확인할 수 있는 퀴즈 3-5개 (객관식 또는 단답형)
- 정답 포함

## 🔗 참고자료
- 추천 온라인 강의, 문서, 블로그 포스트 등
- 실제 링크 또는 검색 키워드 제공

## 💡 학습 팁
- 오늘 학습을 효과적으로 진행할 수 있는 팁

마크다운 형식으로 작성해주세요."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"일자별 학습자료 생성 중 오류 발생: {str(e)}")
        return None

# 프로그램 개선
def improve_learning_program(current_program, improvement_request):
    """사용자 요청에 따라 학습 프로그램을 개선합니다."""
    model = get_gemini_model()

    prompt = f"""당신은 교육 전문가입니다. 다음 학습 프로그램을 사용자의 요청에 따라 개선해주세요.

현재 학습 프로그램:
{current_program['content']}

사용자 개선 요청사항:
{improvement_request}

위 개선 요청사항을 반영하여 학습 프로그램을 수정해주세요.
기존 프로그램의 좋은 부분은 유지하면서 요청사항만 개선하세요.

다음 형식으로 작성해주세요:
1. 학습 목표
2. 주차별 커리큘럼 (각 주차마다 구체적인 학습 내용과 활동 포함)
3. 추천 학습 자료 (온라인 강의, 책, 웹사이트 등)
4. 실습 과제
5. 평가 방법
6. 학습 팁

JSON 형식이 아닌 읽기 쉬운 마크다운 형식으로 작성해주세요."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"프로그램 개선 중 오류 발생: {str(e)}")
        return None

# 메인 UI
st.title("📚 AI 학습 프로그램 생성기")
st.markdown("---")

# 사이드바 - 설정
with st.sidebar:
    st.header("⚙️ 설정")

    # API 키 상태 확인
    api_key = os.getenv('GOOGLE_API_KEY') or st.secrets.get('GOOGLE_API_KEY', '')
    if api_key:
        st.success("✅ API 키 연결됨")
    else:
        st.error("❌ API 키 미연결")
        st.info("Streamlit Cloud에서는 Secrets를 사용하세요.")

    st.markdown("---")
    st.header("📊 내 학습 프로그램")
    if st.session_state.learning_programs:
        for idx, prog in enumerate(st.session_state.learning_programs):
            if st.button(f"📖 {prog['topic'][:20]}...", key=f"prog_{idx}"):
                st.session_state.current_program = prog
    else:
        st.info("아직 생성된 프로그램이 없습니다.")

# 메인 컨텐츠
tab1, tab2, tab3, tab4 = st.tabs(["🎯 새 프로그램 생성", "📖 현재 프로그램", "📅 오늘의 학습", "📈 진행도 관리"])

with tab1:
    st.header("새로운 학습 프로그램 만들기")

    col1, col2 = st.columns(2)

    with col1:
        topic = st.text_input("📝 학습 주제를 입력하세요",
                             placeholder="예: 파이썬 프로그래밍, 머신러닝, 웹 개발")

        level = st.selectbox("🎓 현재 수준",
                            ["초급 (처음 시작)", "중급 (기본 지식 보유)", "고급 (심화 학습)"])

    with col2:
        duration = st.selectbox("⏱️ 학습 기간",
                               ["1주일", "2주일", "1개월", "2개월", "3개월", "6개월"])

        learning_style = st.selectbox("🎨 선호하는 학습 방식",
                                     ["이론 중심", "실습 중심", "프로젝트 기반", "혼합형"])

    st.markdown("---")

    if st.button("🚀 학습 프로그램 생성하기", type="primary", use_container_width=True):
        if not topic:
            st.warning("학습 주제를 입력해주세요!")
        else:
            with st.spinner("AI가 맞춤형 학습 프로그램을 생성하고 있습니다... 🤖"):
                program_content = generate_learning_program(topic, level, duration, learning_style)

                if program_content:
                    program = {
                        'id': len(st.session_state.learning_programs),
                        'topic': topic,
                        'level': level,
                        'duration': duration,
                        'learning_style': learning_style,
                        'content': program_content,
                        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    # Supabase에 저장
                    supabase_id = save_program_to_supabase(program)
                    if supabase_id:
                        program['supabase_id'] = supabase_id

                    st.session_state.learning_programs.append(program)
                    st.session_state.current_program = program
                    st.session_state.progress[program['id']] = {
                        'completed_weeks': [],
                        'notes': ''
                    }

                    st.success("✅ 학습 프로그램이 생성되었습니다!")
                    st.balloons()
                    st.rerun()

with tab2:
    st.header("현재 학습 프로그램")

    if st.session_state.current_program:
        prog = st.session_state.current_program

        st.subheader(f"📚 {prog['topic']}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("수준", prog['level'])
        with col2:
            st.metric("기간", prog['duration'])
        with col3:
            st.metric("학습 방식", prog['learning_style'])
        with col4:
            st.metric("생성일", prog['created_at'].split()[0])

        st.markdown("---")
        st.markdown(prog['content'])

        # 프로그램 저장 기능
        st.markdown("---")
        if st.button("💾 프로그램 다운로드 (Markdown)"):
            file_content = f"""# {prog['topic']}

**수준**: {prog['level']}
**기간**: {prog['duration']}
**학습 방식**: {prog['learning_style']}
**생성일**: {prog['created_at']}

---

{prog['content']}
"""
            st.download_button(
                label="다운로드",
                data=file_content,
                file_name=f"learning_program_{prog['topic']}.md",
                mime="text/markdown"
            )

        # 프로그램 개선 기능
        st.markdown("---")
        st.subheader("🔧 프로그램 개선")
        improvement_request = st.text_area(
            "개선하고 싶은 내용을 입력하세요",
            placeholder="예: 더 많은 실습 과제를 추가해주세요\n예: 초보자를 위한 설명을 더 자세히 해주세요\n예: 프로젝트 기반 학습으로 변경해주세요",
            height=100,
            key="improvement_request"
        )

        if st.button("✨ 프로그램 개선하기", type="primary"):
            if improvement_request:
                with st.spinner("AI가 프로그램을 개선하고 있습니다... 🤖"):
                    improved_content = improve_learning_program(prog, improvement_request)

                    if improved_content:
                        # 프로그램 업데이트
                        prog['content'] = improved_content

                        # Supabase에 저장
                        if 'supabase_id' in prog:
                            save_program_to_supabase(prog)

                        # 세션 스테이트 업데이트
                        for idx, p in enumerate(st.session_state.learning_programs):
                            if p['id'] == prog['id']:
                                st.session_state.learning_programs[idx] = prog
                                break

                        st.success("✅ 프로그램이 개선되었습니다!")
                        st.rerun()
            else:
                st.warning("개선 요청사항을 입력해주세요!")

        # 일자별 학습 버튼
        st.markdown("---")
        st.subheader("📅 일자별 학습")

        total_days = get_duration_in_days(prog['duration'])
        st.write(f"총 {total_days}일 학습 프로그램")

        # 프로그램 ID로 일자별 학습자료 가져오기
        prog_id = prog['id']
        if prog_id not in st.session_state.daily_materials:
            st.session_state.daily_materials[prog_id] = {}

        # 일자 버튼들 (스크롤 가능한 한 줄)
        st.write("학습하고 싶은 날짜를 선택하세요:")

        # 버튼 스타일 추가
        st.markdown("""
        <style>
        .day-button-container {
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)

        # 버튼 컨테이너
        cols = st.columns(min(10, total_days))
        for day in range(1, min(11, total_days + 1)):
            with cols[day - 1]:
                # 이미 생성된 자료인지 확인
                is_generated = day in st.session_state.daily_materials[prog_id]
                button_label = f"Day {day}"

                if is_generated:
                    if st.button(f"✅ {button_label}", key=f"day_{prog_id}_{day}", type="secondary"):
                        st.session_state.current_day = day
                        st.rerun()
                else:
                    if st.button(f"📝 {button_label}", key=f"day_{prog_id}_{day}"):
                        # 학습자료 생성
                        with st.spinner(f"Day {day} 학습자료를 생성하고 있습니다... 🤖"):
                            material = generate_daily_material(
                                prog['topic'],
                                prog['level'],
                                prog['duration'],
                                prog['learning_style'],
                                day,
                                total_days
                            )

                            if material:
                                # 메모리에 저장
                                st.session_state.daily_materials[prog_id][day] = material

                                # Supabase에 저장
                                if 'supabase_id' in prog:
                                    save_daily_material_to_supabase(prog['supabase_id'], day, material)

                                st.session_state.current_day = day
                                st.success(f"✅ Day {day} 학습자료가 생성되었습니다!")
                                st.rerun()

        # 11일차 이상일 경우 추가 버튼 표시
        if total_days > 10:
            st.markdown("---")
            remaining_days = list(range(11, total_days + 1))
            selected_day = st.selectbox(
                f"Day 11 ~ Day {total_days} 선택",
                remaining_days,
                format_func=lambda x: f"Day {x}" + (" ✅" if x in st.session_state.daily_materials[prog_id] else "")
            )

            if st.button(f"Day {selected_day} 학습 시작", key=f"day_select_{selected_day}"):
                if selected_day not in st.session_state.daily_materials[prog_id]:
                    # 학습자료 생성
                    with st.spinner(f"Day {selected_day} 학습자료를 생성하고 있습니다... 🤖"):
                        material = generate_daily_material(
                            prog['topic'],
                            prog['level'],
                            prog['duration'],
                            prog['learning_style'],
                            selected_day,
                            total_days
                        )

                        if material:
                            st.session_state.daily_materials[prog_id][selected_day] = material

                            if 'supabase_id' in prog:
                                save_daily_material_to_supabase(prog['supabase_id'], selected_day, material)

                st.session_state.current_day = selected_day
                st.rerun()

    else:
        st.info("👈 왼쪽에서 프로그램을 선택하거나 새로 생성해주세요.")

with tab3:
    st.header("오늘의 학습")

    if st.session_state.current_program and st.session_state.current_day:
        prog = st.session_state.current_program
        prog_id = prog['id']
        day = st.session_state.current_day

        # 학습자료가 있는지 확인
        if prog_id in st.session_state.daily_materials and day in st.session_state.daily_materials[prog_id]:
            st.subheader(f"📚 {prog['topic']} - Day {day}")

            # 학습자료 표시
            st.markdown(st.session_state.daily_materials[prog_id][day])

            # 이전/다음 버튼
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                if day > 1:
                    if st.button("⬅️ 이전 날짜"):
                        st.session_state.current_day = day - 1
                        st.rerun()

            with col3:
                total_days = get_duration_in_days(prog['duration'])
                if day < total_days:
                    if st.button("다음 날짜 ➡️"):
                        next_day = day + 1
                        # 다음 날짜 자료가 없으면 생성
                        if next_day not in st.session_state.daily_materials[prog_id]:
                            with st.spinner(f"Day {next_day} 학습자료를 생성하고 있습니다... 🤖"):
                                material = generate_daily_material(
                                    prog['topic'],
                                    prog['level'],
                                    prog['duration'],
                                    prog['learning_style'],
                                    next_day,
                                    total_days
                                )

                                if material:
                                    st.session_state.daily_materials[prog_id][next_day] = material

                                    if 'supabase_id' in prog:
                                        save_daily_material_to_supabase(prog['supabase_id'], next_day, material)

                        st.session_state.current_day = next_day
                        st.rerun()
        else:
            st.info("학습자료가 생성되지 않았습니다. '현재 프로그램' 탭에서 날짜를 선택해주세요.")
    else:
        st.info("학습할 프로그램과 날짜를 선택해주세요.")

with tab4:
    st.header("학습 진행도 관리")

    if st.session_state.current_program:
        prog = st.session_state.current_program
        prog_id = prog['id']

        st.subheader(f"📊 {prog['topic']} - 진행 상황")

        # 주차별 체크리스트
        st.write("### 주차별 완료 체크")

        duration_weeks = {
            "1주일": 1, "2주일": 2, "1개월": 4,
            "2개월": 8, "3개월": 12, "6개월": 24
        }
        weeks = duration_weeks.get(prog['duration'], 4)

        progress_data = st.session_state.progress.get(prog_id, {'completed_weeks': [], 'notes': ''})

        cols = st.columns(min(4, weeks))
        for i in range(weeks):
            with cols[i % 4]:
                is_checked = i in progress_data['completed_weeks']
                if st.checkbox(f"Week {i+1}", value=is_checked, key=f"week_{prog_id}_{i}"):
                    if i not in progress_data['completed_weeks']:
                        progress_data['completed_weeks'].append(i)
                else:
                    if i in progress_data['completed_weeks']:
                        progress_data['completed_weeks'].remove(i)

        st.session_state.progress[prog_id] = progress_data

        # 진행률 표시
        progress_percentage = (len(progress_data['completed_weeks']) / weeks) * 100
        st.progress(progress_percentage / 100)
        st.write(f"**진행률**: {progress_percentage:.1f}% ({len(progress_data['completed_weeks'])}/{weeks} 주 완료)")

        # 학습 노트
        st.markdown("---")
        st.write("### 📝 학습 노트")
        notes = st.text_area(
            "학습 내용, 질문, 느낀 점 등을 기록하세요",
            value=progress_data.get('notes', ''),
            height=200,
            key=f"notes_{prog_id}"
        )
        progress_data['notes'] = notes

        if st.button("💾 진행도 저장"):
            # Supabase에 저장
            if 'supabase_id' in prog:
                save_progress_to_supabase(prog_id, prog['supabase_id'], progress_data)
            st.success("✅ 진행도가 저장되었습니다!")

    else:
        st.info("👈 학습 프로그램을 먼저 선택해주세요.")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Made with ❤️ using Google Gemini AI & Streamlit</p>
    <p>💡 Tip: Streamlit Cloud에 배포하여 어디서든 접속 가능합니다!</p>
</div>
""", unsafe_allow_html=True)
