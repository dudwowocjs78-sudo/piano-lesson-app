import streamlit as st
import pandas as pd
import datetime

# 1. 앱 페이지 설정
st.set_page_config(page_title="레슨이지 피아노 매니저", page_icon="🎹", layout="centered")

# 2. 감성적인 민트/청록 톤 & 모바일 앱 스타일 CSS 적용
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 부드럽게 */
    .stApp {
        background-color: #F4F7F6;
    }
    
    /* 상단 타이틀 영역 스타일 */
    h1, h2, h3 {
        color: #0F766E !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* 민트/청록색 포인트 카드 박스 */
    .mint-card {
        background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
        padding: 24px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(13, 148, 136, 0.3);
        margin-bottom: 20px;
    }

    /* 일반 콘텐츠 카드 */
    .content-card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 16px;
        border: 1px solid #E5E7EB;
    }

    /* 둥글고 예쁜 메인 버튼 스타일 */
    .stButton>button {
        border-radius: 14px;
        font-weight: 700;
        background-color: #0D9488;
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        box-shadow: 0 4px 10px rgba(13, 148, 136, 0.3);
        width: 100%;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #0F766E;
        color: white;
        transform: translateY(-1px);
    }

    /* 탭 디자인 개선 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #E2E8F0;
        border-radius: 10px;
        padding: 8px 16px;
        color: #475569;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0D9488 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 5단계 커리큘럼 정의
curriculum = {
    "Lv. 1": {
        "title": "코드반주 입문 (기초 다지기 및 보이싱)",
        "contents": [
            "코드개념, 보이싱과 패턴의 개념",
            "메이저7, 마이너7, 도미넌트7 코드 배우기",
            "기본 자리바꿈(Inversion) 연습으로 손모양 잡기",
            "4비트, 8비트 정박 리듬으로 쉬운 곡 연주하기"
        ]
    },
    "Lv. 2": {
        "title": "느린곡 패턴 (중급 진입)",
        "contents": [
            "기본 자리바꿈 연습으로 손모양 잡기",
            "아르페지오(분산화음) 패턴과 리듬 적용하기",
            "발라드 곡에서 웅장하거나 부드러운 분위기 내는 법"
        ]
    },
    "Lv. 3": {
        "title": "재즈/가요 반주의 꽃, 투파이브원 (응용)",
        "contents": [
            "다이아토닉 코드와 2-5-1 진행 이해하기",
            "보사노바, 셔플, 16비트 등 다양한 리듬 스타일 소화하기",
            "코드 간의 부드러운 연결(보이싱) 연습"
        ]
    },
    "Lv. 4": {
        "title": "카피연습",
        "contents": [
            "여러가지 영상을 보며 귀카피",
            "귀로 들은 대로 악보 그리기 및 연주"
        ]
    },
    "Lv. 5": {
        "title": "리하모니제이션 및 프로페셔널 반주 (고급)",
        "contents": [
            "백도어/세컨더리 도미넌트 활용하기",
            "2-5-1 활용 및 대리코드 활용",
            "곡의 분위기를 확 바꾸는 리하모니제이션(편곡)"
        ]
    }
}

# 4. 앱 내부 데이터베이스 초기화
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame([
        {"이름": "김철수", "현재레벨": "Lv. 1", "현재회차": 2, "마지막수업일": "2026-10-15", "누적연습시간": 1.5, "요청곡_및_특이사항": "봄이 좋냐?? 반주 연습 중"},
        {"이름": "이영희", "현재레벨": "Lv. 3", "현재회차": 4, "마지막수업일": "2026-10-18", "누적연습시간": 3.0, "요청곡_및_특이사항": "재즈 발라드 악보 가져옴"}
    ])

# 5. 사이드바 메뉴 (모드 선택)
st.sidebar.title("🎹 피아노 레슨 매니저")
mode = st.sidebar.radio("접속 모드를 선택하세요:", ["📱 레슨생 모드", "💻 강사(선생님) 관리 모드"])

df = st.session_state.students

# ==========================================
# [모드 1] 레슨생 전용 화면
# ==========================================
if mode == "📱 레슨생 모드":
    # 상단 배너 카드 (레슨이지 스크린샷의 청록색 감성 재현)
    st.markdown("""
        <div class="mint-card">
            <h2 style="color: white !important; margin: 0; font-size: 24px;">🎹 피아노 레슨 스마트 공간</h2>
            <p style="margin: 8px 0 0 0; opacity: 0.9;">오늘도 즐겁게 연주하고 연습 시간을 기록해 보세요!</p>
        </div>
    """, unsafe_allow_html=True)

    student_list = df["이름"].unique().tolist() + ["+ 신규 등록"]
    name = st.selectbox("본인 이름을 선택하세요:", student_list)
    
    if name == "+ 신규 등록":
        with st.container():
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            new_name = st.text_input("새로운 이름을 입력하세요:")
            selected_level = st.selectbox("시작 레벨 선택:", list(curriculum.keys()))
            note = st.text_area("요청곡 또는 특이사항:")
            
            if st.button("등록하기"):
                if new_name:
                    new_row = {
                        "이름": new_name, "현재레벨": selected_level, "현재회차": 1, 
                        "마지막수업일": str(datetime.date.today()), "누적연습시간": 0.0, 
                        "요청곡_및_특이사항": note
                    }
                    st.session_state.students = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    st.success(f"✨ {new_name}님 환영합니다! 등록 완료되었습니다.")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        student_idx = df.index[df["이름"] == name][0]
        student_row = df.loc[student_idx]
        current_lvl = student_row["현재레벨"]
        
        st.markdown(f"""
            <div class="content-card" style="border-left: 5px solid #0D9488;">
                <h4 style="margin:0; color: #0F766E;">👤 {name}님 환영합니다!</h4>
                <p style="margin: 5px 0 0 0; color: #4B5563;">현재 진도: <b>{current_lvl} - {curriculum[current_lvl]['title']}</b></p>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📖 내 레벨 커리큘럼", "⏱️ 연습 시간 기록"])
        
        with tab1:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.subheader(f"[{current_lvl}] {curriculum[current_lvl]['title']}")
            for item in curriculum[current_lvl]["contents"]:
                st.markdown(f"- {item}")
                
            with st.expander("📚 전체 Lv.1 ~ Lv.5 커리큘럼 전체보기"):
                for lv_key, lv_info in curriculum.items():
                    st.markdown(f"**{lv_key}: {lv_info['title']}**")
                    for c in lv_info["contents"]:
                        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;· {c}")
                    st.markdown("---")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.subheader("⏱️ 연습 시간 기록 및 확인")
            st.metric("현재까지 총 누적 연습 시간", f"{student_row['누적연습시간']} 시간")
            
            st.markdown("---")
            st.write("🎹 **오늘 연습하신 양을 선택하고 아래 버튼을 눌러주세요!**")
            
            add_hours = st.selectbox(
                "오늘 연습 시간 선택:", 
                [0.5, 1.0, 1.5, 2.0, 2.5, 3.0], 
                format_func=lambda x: f"{int(x)}시간" if x == int(x) else f"{int(x)}시간 30분"
            )
            
            current_note = str(student_row["요청곡_및_특이사항"])
            new_note = st.text_area("선생님께 남길 요청곡 / 특이사항:", value=current_note)
            
            if st.button("✅ 연습 시간 및 요청사항 반영하기", type="primary"):
                st.session_state.students.loc[student_idx, "누적연습시간"] += add_hours
                st.session_state.students.loc[student_idx, "요청곡_및_특이사항"] = new_note
                st.success(f"🎉 성공적으로 반영되었습니다! (총 연습 시간: {st.session_state.students.loc[student_idx, '누적연습시간']} 시간)")
                st.rerun()
                
            st.markdown("---")
            st.subheader("💬 선생님께 보낼 연습 보고 복사하기")
            report_text = f"[피아노 레슨 보고] {name} 학생입니다! 오늘 {add_hours}시간 연습 완료했습니다. 🎹 (누적: {student_row['누적연습시간']}시간) 특이사항: {new_note}"
            st.text_area("아래 텍스트를 복사해서 선생님께 카톡을 보내보세요!", value=report_text, height=100)
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# [모드 2] 강사 전용 관리자 대시보드
# ==========================================
else:
    st.markdown("""
        <div class="mint-card" style="background: linear-gradient(135deg, #1E293B 100%, #334155 0%);">
            <h2 style="color: white !important; margin: 0; font-size: 24px;">💻 강사 전용 제어탑</h2>
            <p style="margin: 8px 0 0 0; opacity: 0.9;">레슨생 현황과 결제 주기를 한눈에 관리하세요.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("총 레슨생 수", f"{len(df)}명")
    payment_due_count = len(df[df["현재회차"] >= 4])
    col2.metric("결제/재등록 대상", f"{payment_due_count}명", delta="확인 필요" if payment_due_count > 0 else "정상")
    avg_practice = df["누적연습시간"].mean()
    col3.metric("평균 누적 연습", f"{avg_practice:.1f}시간")

    st.markdown("---")
    st.subheader("📋 레슨생 통합 관리 대시보드")
    
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 변경사항 전체 저장"):
        st.session_state.students = edited_df
        st.success("모든 변경사항이 안전하게 저장되었습니다!")

    st.markdown("### 🚨 4회차 결제 및 재등록 체크 리스트")
    alert_triggered = False
    for idx, row in edited_df.iterrows():
        if row["현재회차"] >= 4:
            alert_triggered = True
            st.warning(f"⚠️ **{row['이름']}** 학생이 현재 **{row['현재회차']}회차**입니다. 수강료 재등록 안내를 진행해주세요!")
            
    if not alert_triggered:
        st.info("💡 현재 4회차에 도달하여 재등록이 필요한 레슨생이 없습니다.")