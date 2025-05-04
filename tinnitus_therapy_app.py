import streamlit as st
import pandas as pd
import datetime

# 앱 초기 설정 (반드시 최상단에 위치해야 함)
st.set_page_config(page_title="Tinnitus Therapy", layout="centered")

# 로그인 기능
import os
import csv
user_file = "user_credentials.csv"
if not os.path.exists(user_file):
    with open(user_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "password"])

st.sidebar.markdown("---")
st.sidebar.subheader("🔐 계정이 없으신가요?")
new_email = st.sidebar.text_input("신규 이메일", key="reg_email")
new_pw = st.sidebar.text_input("신규 비밀번호", type="password", key="reg_pw")
if st.sidebar.button("회원가입"):
    with open(user_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([new_email, new_pw])
    st.sidebar.success("회원가입 완료. 로그인 해주세요!")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 로그인")
    email = st.text_input("이메일을 입력하세요")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        with open(user_file, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
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

# (이하 앱의 나머지 코드가 이어짐...)
