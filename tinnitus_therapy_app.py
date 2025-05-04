import streamlit as st
import pandas as pd
import datetime

# 앱 초기 설정
st.set_page_config(page_title="Tinnitus Therapy", layout="centered")
st.title("🎧 Tinnitus Sound Therapy App")

# 세션 상태 초기화
if "mode" not in st.session_state:
    st.session_state.mode = None
if "step" not in st.session_state:
    st.session_state.step = 0
if "tinnitus_level" not in st.session_state:
    st.session_state.tinnitus_level = 5
if "audio_file" not in st.session_state:
    st.session_state.audio_file = None
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "health_info" not in st.session_state:
    st.session_state.health_info = {}
if "thi_results" not in st.session_state:
    st.session_state.thi_results = {}

# 모드 선택
if st.session_state.step == 0:
    st.header("시작하기 전에...")
    st.markdown("설문을 먼저 진행하거나, 바로 치료 세션으로 들어갈 수 있습니다.")
    if st.button("👤 사용자 정보 및 설문 시작"):
        st.session_state.mode = "survey"
        st.session_state.step = 1
    elif st.button("🎧 바로 치료 시작"):
        st.session_state.mode = "therapy"
        st.session_state.step = 4

# 사용자 정보 입력
if st.session_state.step == 1:
    st.header("사용자 정보 입력")
    name = st.text_input("이름")
    phone = st.text_input("전화번호")
    email = st.text_input("이메일")
    birth = st.date_input("생년월일", value=datetime.date(1990, 1, 1))
    if st.button("다음"):
        st.session_state.user_info = {
            "이름": name,
            "전화번호": phone,
            "이메일": email,
            "생년월일": str(birth)
        }
        st.session_state.step += 1

# 건강 설문
elif st.session_state.step == 2:
    st.header("🩺 건강 설문")

    hearing_questions = [
        "양쪽 귀 중 한쪽 귀만 잘 들리시나요?",
        "일상 대화 중 TV 또는 라디오 음량을 높여야 하나요?",
        "조용한 환경에서는 대화가 가능하나, 시끄러운 환경에서는 어려움이 있으신가요?",
        "사람들의 말을 자주 되묻거나 오해하신 적이 있나요?",
        "전화 통화 시 상대방 말소리를 듣기 어려운 편인가요?",
        "최근 청력 저하를 느낀 적이 있나요?"
    ]

    dizziness_questions = [
        "최근 1개월 내 어지러움을 느끼신 적이 있나요?",
        "자세를 바꿀 때 순간적으로 어지러움을 느끼시나요?",
        "걸을 때 중심을 잃거나 휘청거린 적이 있나요?",
        "어지럼증과 함께 메스꺼움이나 구토가 동반된 적이 있나요?",
        "어지럼증으로 일상 활동에 제한이 있었나요?",
        "최근 쓰러지거나 낙상한 경험이 있으신가요?"
    ]

    chronic_questions = [
        ("고혈압 진단을 받은 적이 있나요?", ["예", "아니오"]),
        ("당뇨병 또는 혈당 조절 장애가 있나요?", ["예", "아니오"]),
        ("고지혈증이나 콜레스테롤 문제로 치료 중이신가요?", ["예", "아니오"]),
        ("심혈관 질환 진단을 받은 적이 있나요?", ["예", "아니오"]),
        ("현재 복용 중인 만성질환 관련 약물이 있나요?", ["예", "아니오"]),
        ("하루 평균 몇 시간 정도 수면을 취하시나요?", "number"),
        ("흡연 여부", ["흡연", "금연", "비흡연"]),
        ("음주 습관", ["주 1회 이하", "주 2~3회", "거의 매일"]),
        ("규칙적인 운동을 하고 계신가요?", ["예", "아니오"])
    ]

    hearing_responses = {q: st.radio(q, ["예", "아니오"], key=f"hear_{i}") for i, q in enumerate(hearing_questions)}
    dizziness_responses = {q: st.radio(q, ["예", "아니오"], key=f"dizzy_{i}") for i, q in enumerate(dizziness_questions)}
    chronic_responses = {}
    for i, (q, opt) in enumerate(chronic_questions):
        if opt == "number":
            chronic_responses[q] = st.number_input(q, min_value=0, max_value=24, key=f"chronic_{i}")
        else:
            chronic_responses[q] = st.radio(q, opt, key=f"chronic_{i}")

    if st.button("다음 (THI 설문)"):
        st.session_state.health_info = {
            **hearing_responses,
            **dizziness_responses,
            **chronic_responses
        }
        st.session_state.step += 1

# THI 설문
elif st.session_state.step == 3:
    st.header("📝 Tinnitus Handicap Inventory (THI)")
    thi_questions = [
        "이명 때문에 집중하기가 어렵습니까?",
        "이명의 크기로 인해 다른 사람이 말하는 것을 듣기가 어렵습니까?",
        "이명으로 인해 화가 날 때가 있습니까?",
        "이명으로 인해 난처한 경우가 있습니까?",
        "이명이 절망적인 문제라고 생각하십니까?",
        "이명에 대해 많이 불평하는 편이십니까?",
        "이명 때문에 밤에 잠을 자기가 어려우십니까?",
        "이명에서 벗어날 수 없다고 생각하십니까?",
        "이명으로 인해 사회적 활동에 방해를 받습니까?",
        "이명 때문에 좌절감을 느끼는 경우가 있습니까?",
        "이명이 심각한 질병이라고 생각하십니까?",
        "이명으로 인해 삶의 즐거움이 감소됩니까?",
        "이명으로 인해 업무나 가사 일을 하는데 방해를 받습니까?",
        "이명 때문에 종종 짜증나는 경우가 있습니까?",
        "이명 때문에 책을 읽는 것이 어렵습니까?",
        "이명으로 인해 기분이 몹시 상하는 경우가 있습니까?",
        "이명이 가족이나 친구 관계에 스트레스를 준다고 느끼십니까?",
        "이명에서 벗어나 다른 일들에 주의를 집중하기가 어렵습니까?",
        "이명을 자신이 통제할 수 없다고 생각하십니까?",
        "이명 때문에 종종 피곤감을 느끼십니까?",
        "이명 때문에 우울감을 느끼십니까?",
        "이명으로 인해 불안감을 느끼십니까?",
        "이명에 더 이상 대처할 수 없다고 생각하십니까?",
        "스트레스를 받으면 이명이 더 심해집니까?",
        "이명으로 인해 불안정한 기분을 느끼십니까?"
    ]

    responses = {}
    for i, question in enumerate(thi_questions):
        responses[question] = st.radio(question, ["아니다", "가끔 그렇다", "그렇다"], key=f"thi_q{i}")

    if st.button("Submit THI Survey"):
        st.session_state.thi_results = responses
        st.session_state.step += 1

# 치료 시작
elif st.session_state.step == 4:
    st.header("🎶 치료 세션 시작")
    st.session_state.tinnitus_level = st.slider("이명 강도 (0~10)", 0, 10, st.session_state.tinnitus_level)
    uploaded_file = st.file_uploader("치료용 사운드 파일 업로드", type=["mp3", "wav", "ogg"])
    if uploaded_file:
        st.session_state.audio_file = uploaded_file
        st.audio(uploaded_file, format='audio/mp3')
    st.markdown("🔗 블루투스 기기 연결은 스마트폰 설정에서 별도 진행해주세요.")
    if st.button("치료 종료 및 결과 보기"):
        st.session_state.step += 1

# 결과 요약
elif st.session_state.step == 5:
    st.header("📋 설문 결과 종합 요약")
    st.subheader("👤 사용자 정보")
    st.write(pd.DataFrame([st.session_state.user_info]))

    if st.session_state.mode == "survey":
        st.subheader("🩺 건강 설문 결과")
        st.write(pd.DataFrame([st.session_state.health_info]))

        st.subheader("📝 THI 설문 결과")
        thi_df = pd.DataFrame({
            "문항": list(st.session_state.thi_results.keys()),
            "응답": list(st.session_state.thi_results.values())
        })
        thi_df["점수"] = thi_df["응답"].map({"아니다": 0, "가끔 그렇다": 2, "그렇다": 4})
        st.dataframe(thi_df)
        st.bar_chart(thi_df.set_index("문항")["점수"])
        total_score = thi_df["점수"].sum()
        st.markdown(f"### 총 THI 점수: **{total_score} / 100**")
        st.download_button("📥 설문 결과 다운로드 (CSV)", data=thi_df.to_csv(index=False), file_name="Tinnitus_Survey_Results.csv")
