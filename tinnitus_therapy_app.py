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
