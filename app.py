import streamlit as st
import pandas as pd
import datetime

# 1. 앱 페이지 설정 (모바일 최적화 레이아웃)
st.set_page_config(page_title="LessonEasy - 프리미엄 피아노 레슨 플랫폼", page_icon="🎹", layout="centered")

# 2. 압도적인 시각 효과를 주는 프리미엄 CSS (발표용 하이엔드 UI)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
    }
    h1, h2, h3 {
        color: #2DD4BF !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    /* 네온 민트 그라데이션 카드 */
    .hero-card {
        background: linear-gradient(135deg, #0D9488 0%, #065F46 100%);
        padding: 28px;
        border-radius: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 20px 25px -5px rgba(13, 148, 136, 0.4);
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* 글래스모피즘 콘텐츠 카드 */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    /* 버튼 입체 효과 */
    .stButton>button {
        border-radius: 14px;
        font-weight: 700;
        background: linear-gradient(135deg, #14B8A6 0%, #0D9488 100%);
        color: white;
        border: none;
        padding: 0.8rem 1rem;
        box-shadow: 0 4px 15px rgba(20, 184, 166, 0.4);
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2DD4BF 0%, #14B8A6 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(45, 212, 191, 0.6);
    }
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(15, 23, 42, 0.5);
        padding: 6px;
        border-radius: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #334155;
        border-radius: 10px;
        padding: 10px 20px;
        color: #94A3B8;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0D9488 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 커리큘럼 데이터 초기화
if "curriculum" not in st.session_state:
    st.session_state.curriculum = {
        "Lv. 1": {
            "title": "코드반주 입문 (기초 다지기 및 보이싱)",
            "contents": ["코드개념, 보이싱과 패턴의 개념", "메이저7, 마이너7, 도미넌트7 코드 배우기", "기본 자리바꿈 연습", "4비트/8비트 정박 리듬 연주"],
            "youtube_title": "🎹 [추천 강의] 기초 코드 및 보이싱 마스터하기",
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        },
        "Lv. 2": {
            "title": "느린곡 패턴 (중급 진입)",
            "contents": ["아르페지오 패턴과 리듬 적용하기", "발라드 곡 감성 표현법"],
            "youtube_title": "🎹 [추천 강의] 발라드 아르페지오 주법 완벽 가이드",
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        },
        "Lv. 3": {
            "title": "재즈/가요 반주의 꽃, 투파이브원 (응용)",
            "contents": ["다이아토닉 코드와 2-5-1 진행 이해하기", "보사노바 및 셔플 리듬 소화하기"],
            "youtube_title": "🎹 [추천 강의] 투파이브원(2-5-1) 보이싱 총정리",
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
    }

# 4. 레슨생 데이터 초기화
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame([
        {"이름": "김철수", "현재레벨": "Lv. 1", "현재회차": 2, "마지막수업일": "2026-10-15", "누적연습시간": 2.5, "요청곡_및_특이사항": "봄이 좋냐?? 반주 연습 중"},
        {"이름": "이영희", "현재레벨": "Lv. 3", "현재회차": 4, "마지막수업일": "2026-10-18", "누적연습시간": 5.0, "요청곡_및_특이사항": "재즈 발라드 악보 지참"}
    ])

# 5. 사이드바 네비게이션
st.sidebar.title("🎹 LessonEasy")
st.sidebar.markdown("프리미엄 음악 레슨 관리 플랫폼")
mode = st.sidebar.radio("접속 모드 선택:", ["📱 레슨생 모드 (User)", "💻 강사 전용 제어탑 (Admin)"])

df = st.session_state.students
curriculum = st.session_state.curriculum

# ==========================================
# [모드 1] 레슨생 모드
# ==========================================
if mode == "📱 레슨생 모드 (User)":
    st.markdown("""
        <div class="hero-card">
            <h2 style="color: white !important; margin: 0; font-size: 26px;">🎹 LessonEasy Smart Practice</h2>
            <p style="margin: 8px 0 0 0; opacity: 0.9;">오늘도 음악과 함께 성장하는 스마트한 연습 공간</p>
        </div>
    """, unsafe_allow_html=True)

    student_list = df["이름"].unique().tolist() + ["+ 신규 레슨생 등록"]
    name = st.selectbox("레슨생 프로필 선택:", student_list)
    
    if name == "+ 신규 레슨생 등록":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        new_name = st.text_input("레슨생 성함:")
        selected_level = st.selectbox("초기 배정 레벨:", list(curriculum.keys()))
        note = st.text_area("희망곡 및 특이사항:")
        
        if st.button("🚀 스마트 레슨 시작하기"):
            if new_name:
                new_row = {
                    "이름": new_name, "현재레벨": selected_level, "현재회차": 1, 
                    "마지막수업일": str(datetime.date.today()), "누적연습시간": 0.0, 
                    "요청곡_및_특이사항": note
                }
                st.session_state.students = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"✨ {new_name}님 환영합니다! 레슨 프로필이 생성되었습니다.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        student_idx = df.index[df["이름"] == name][0]
        student_row = df.loc[student_idx]
        current_lvl = student_row["현재레벨"]
        
        st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid #2DD4BF;">
                <h4 style="margin:0; color: #2DD4BF;">👤 {name} 레슨생님, 환영합니다!</h4>
                <p style="margin: 6px 0 0 0; color: #CBD5E1;">현재 진도: <b>{current_lvl} - {curriculum[current_lvl]['title']}</b></p>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📖 커리큘럼 & 레퍼런스 영상", "⏱️ 실시간 연습 시간 기록"])
        
        with tab1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader(f"[{current_lvl}] {curriculum[current_lvl]['title']}")
            for item in curriculum[current_lvl]["contents"]:
                st.markdown(f"- {item}")
            
            st.markdown("---")
            st.markdown(f"### {curriculum[current_lvl]['youtube_title']}")
            try:
                st.video(curriculum[current_lvl]["youtube_url"])
            except:
                st.markdown(f"👉 [영상 바로가기 링크]({curriculum[current_lvl]['youtube_url']})")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("⏱️ 연습 시간 기록 및 전송")
            st.metric("누적 연습 시간", f"{student_row['누적연습시간']} 시간")
            
            add_hours = st.selectbox(
                "오늘 연습한 시간:", 
                [0.5, 1.0, 1.5, 2.0, 3.0], 
                format_func=lambda x: f"{int(x)}시간" if x == int(x) else f"{int(x)}시간 30분"
            )
            
            current_note = str(student_row["요청곡_및_특이사항"])
            new_note = st.text_area("선생님 피드백 요청 / 특이사항:", value=current_note)
            
            if st.button("✅ 연습 완료 및 서버 전송"):
                st.session_state.students.loc[student_idx, "누적연습시간"] += add_hours
                st.session_state.students.loc[student_idx, "요청곡_및_특이사항"] = new_note
                st.success("🎉 연습 기록이 안전하게 저장되었습니다!")
                st.rerun()
                
            st.markdown("---")
            st.subheader("💬 강사님께 카카오톡 보고 텍스트 생성")
            report_text = f"[레슨 보고] {name} 학생 오늘 {add_hours}시간 연습 완료! (총 누적: {student_row['누적연습시간']}시간) - 요청사항: {new_note}"
            st.text_area("아래 내용을 복사해서 전송하세요:", value=report_text, height=90)
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# [모드 2] 강사 전용 관리자 대시보드
# ==========================================
else:
    st.markdown("""
        <div class="hero-card" style="background: linear-gradient(135deg, #334155 0%, #1E293B 100%);">
            <h2 style="color: white !important; margin: 0; font-size: 26px;">💻 Instructor Control Tower</h2>
            <p style="margin: 8px 0 0 0; opacity: 0.9;">모든 레슨생의 진도, 연습량 및 결제 주기를 한눈에 관리하세요.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("총 수강생", f"{len(df)}명")
    due_count = len(df[df["현재회차"] >= 4])
    col2.metric("결제/재등록 대상", f"{due_count}명", delta="주의" if due_count > 0 else "안정")
    col3.metric("평균 연습 시간", f"{df['누적연습시간'].mean():.1f}시간")

    st.markdown("---")
    st.subheader("📋 수강생 통합 관리 시트")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 전체 데이터베이스 저장"):
        st.session_state.students = edited_df
        st.success("성공적으로 저장되었습니다!")

    st.markdown("---")
    st.subheader("🎥 커리큘럼별 유튜브 레퍼런스 관리")
    edit_lv = st.selectbox("편집할 레벨 선택:", list(curriculum.keys()))
    
    with st.form("admin_yt_form"):
        new_title = st.text_input("영상 타이틀:", value=curriculum[edit_lv]["youtube_title"])
        new_url = st.text_input("유튜브 링크(URL):", value=curriculum[edit_lv]["youtube_url"])
        if st.form_submit_button("🔄 즉시 반영하기"):
            st.session_state.curriculum[edit_lv]["youtube_title"] = new_title
            st.session_state.curriculum[edit_lv]["youtube_url"] = new_url
            st.success("✨ 레퍼런스 영상이 업데이트되었습니다!")
            st.rerun()

    st.markdown("---")
    st.subheader("🚨 4회차 결제 대상 리스트")
    alert_found = False
    for _, row in edited_df.iterrows():
        if row["현재회차"] >= 4:
            alert_found = True
            st.warning(f"⚠️ **{row['이름']}** 수강생이 현재 **{row['현재회차']}회차**입니다. 재등록 안내가 필요합니다.")
    if not alert_found:
        st.info("💡 현재 재등록 대상 수강생이 없습니다.")
