import streamlit as st
import pandas as pd
import datetime
import os
import csv
import json
import numpy as np
import scipy.signal

# 최상단 필수
st.set_page_config(page_title="Tinnitus Therapy", layout="centered")

# 세션 상태 초기화
for var, default in {
    "step": 0,
    "mode": None,
    "tinnitus_level": 5,
    "audio_file": None,
    "user_info": {},
    "health_info": {},
    "thi_results": {},
    "treatment_history": [],
    "feedback_log": {},
    "thi_score": 0
}.items():
    if var not in st.session_state:
        st.session_state[var] = default

# 로그인 및 회원가입
user_file = "user_credentials.csv"
if not os.path.exists(user_file):
    with open(user_file, mode="w", newline="") as f:
        csv.writer(f).writerow(["email", "password"])

st.sidebar.subheader("🔐 계정이 없으신가요?")
new_email = st.sidebar.text_input("신규 이메일", key="reg_email")
new_pw = st.sidebar.text_input("신규 비밀번호", type="password", key="reg_pw")
if st.sidebar.button("회원가입"):
    with open(user_file, mode="a", newline="") as f:
        csv.writer(f).writerow([new_email, new_pw])
    st.sidebar.success("회원가입 완료. 로그인 해주세요!")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 로그인")
    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        with open(user_file, newline="") as f:
            for row in csv.DictReader(f):
                if row["email"] == email and row["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.success(f"{email} 님, 환영합니다!")
                    st.rerun()
    if not st.session_state.authenticated:
        st.error("이메일 또는 비밀번호가 올바르지 않습니다.")
    st.stop()

st.title("🎵 음악으로 이명 치료하다")
st.markdown("## 🎧 Tinnitus Sound Therapy App")

# 단계 안내
st.sidebar.markdown("---")
if st.sidebar.button("▶️ 다음 단계로"):
    st.session_state.step += 1
if st.sidebar.button("◀️ 이전 단계로"):
    st.session_state.step = max(0, st.session_state.step - 1)

step_titles = ["설문 결과", "음원 설정", "치료 일기"]
if st.session_state.step < len(step_titles):
    st.sidebar.info(f"현재 단계: {step_titles[st.session_state.step]}")
# Step 1 – 설문 결과 시각화
if st.session_state.step == 1:
    st.header("📝 설문 결과 요약")
    if st.session_state["health_info"]:
        st.subheader("건강 설문 결과")
        st.dataframe(pd.DataFrame.from_dict(st.session_state.health_info, orient="index", columns=["응답"]))
    if st.session_state["thi_results"]:
        st.subheader("THI 설문 결과 및 점수")
        score = 0
        for answer in st.session_state["thi_results"].values():
            if answer == "가끔 그렇다":
                score += 2
            elif answer == "그렇다":
                score += 4
        st.session_state.thi_score = score
        st.write(f"총 점수: **{score}점** / 100")
        st.dataframe(pd.DataFrame.from_dict(st.session_state.thi_results, orient="index", columns=["응답"]))

# Step 2 – 음원 업로드 및 선택
if st.session_state.step == 2:
    st.header("🎵 음원 업로드 및 선택")
    uploaded_file = st.file_uploader("치료용 음원을 업로드하세요 (mp3/wav)", type=["mp3", "wav"])
    if uploaded_file is not None:
        filepath = f"uploaded_{uploaded_file.name}"
        with open(filepath, "wb") as f:
            f.write(uploaded_file.read())
        st.session_state.audio_file = filepath
        st.success("음원이 업로드되었습니다!")
    if st.session_state.audio_file:
        st.audio(st.session_state.audio_file)
    else:
        st.warning("아직 음원이 업로드되지 않았습니다. 음원은 필수 입력이 아닙니다.")
# Step 3 – 이명 일기 작성
if st.session_state.step == 3:
    st.header("📔 오늘의 이명 치료 일기")
    st.session_state.feedback_log["date"] = str(datetime.date.today())
    st.session_state.feedback_log["feeling"] = st.radio("치료 후 기분은 어떤가요?", ["개선됨", "변화 없음", "악화됨"])
    st.session_state.feedback_log["note"] = st.text_area("오늘의 소감", placeholder="치료를 마치고 느낀 점을 작성해 주세요.")
    st.session_state.feedback_log["thi_score"] = st.session_state.thi_score
    if st.button("저장"):
        filename = f"diary_{st.session_state.user_email.replace('@','_')}.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                diary = json.load(f)
        else:
            diary = []
        diary.append(st.session_state.feedback_log)
        with open(filename, "w") as f:
            json.dump(diary, f, indent=2, ensure_ascii=False)
        st.success("일기가 저장되었습니다!")

# 이명 일기 열람 (사이드바)
if st.sidebar.button("📖 나의 일기 보기"):
    filename = f"diary_{st.session_state.user_email.replace('@','_')}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            diary = json.load(f)
        st.sidebar.write("### 📅 이명 치료 일기 기록")
        for entry in diary[-5:]:
            st.sidebar.markdown(
                f"**{entry['date']}** — {entry['feeling']} | THI: {entry.get('thi_score', '?')}\n\n{entry['note']}"
            )
    else:
        st.sidebar.warning("저장된 일기가 없습니다.")
