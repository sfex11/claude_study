import streamlit as st
import anthropic
import os
import json
from datetime import datetime
from dotenv import load_dotenv

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

# Claude API 클라이언트 초기화
def get_claude_client():
    api_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        st.error("⚠️ ANTHROPIC_API_KEY가 설정되지 않았습니다. .env 파일 또는 Streamlit secrets를 확인해주세요.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)

# Claude API를 사용한 학습 프로그램 생성
def generate_learning_program(topic, level, duration, learning_style):
    client = get_claude_client()

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
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        st.error(f"프로그램 생성 중 오류 발생: {str(e)}")
        return None

# 메인 UI
st.title("📚 AI 학습 프로그램 생성기")
st.markdown("---")

# 사이드바 - 설정
with st.sidebar:
    st.header("⚙️ 설정")

    # API 키 상태 확인
    api_key = os.getenv('ANTHROPIC_API_KEY') or st.secrets.get('ANTHROPIC_API_KEY', '')
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
tab1, tab2, tab3 = st.tabs(["🎯 새 프로그램 생성", "📖 현재 프로그램", "📈 진행도 관리"])

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
    else:
        st.info("👈 왼쪽에서 프로그램을 선택하거나 새로 생성해주세요.")

with tab3:
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
            st.success("✅ 진행도가 저장되었습니다!")

    else:
        st.info("👈 학습 프로그램을 먼저 선택해주세요.")

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Made with ❤️ using Claude AI & Streamlit</p>
    <p>💡 Tip: Streamlit Cloud에 배포하여 어디서든 접속 가능합니다!</p>
</div>
""", unsafe_allow_html=True)
