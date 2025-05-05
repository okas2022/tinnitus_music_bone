import streamlit as st

# ✅ 반드시 최상단에 위치해야 함!
st.set_page_config(page_title="Tinnitus Therapy", layout="centered")

import pandas as pd
import datetime
import os
import csv
import json
from pydub import AudioSegment
import numpy as np
import scipy.signal

# 🔽 step 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 0

# 로그인 기능
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
st.markdown("<style> @keyframes fadein { from {opacity:0;} to {opacity:1;} } .slide { animation: fadein 1s ease-in-out; } </style>", unsafe_allow_html=True)

# 🔧 세션 변수 초기화
for var, default in {
    "mode": None,
    "tinnitus_level": 5,
    "audio_file": None,
    "user_info": {},
    "health_info": {},
    "thi_results": {},
    "treatment_history": [],
    "feedback_log": {},
    "thi_score": 0,
    "matching_info": {},
    "filter_type": "Amplitude Modulation"
}.items():
    if var not in st.session_state:
        st.session_state[var] = default

# 🎛️ 필터 함수 정의

def apply_notch_filter(input_path, output_path, freq=1000, q=30):
    sound = AudioSegment.from_file(input_path)
    samples = np.array(sound.get_array_of_samples())
    fs = sound.frame_rate
    b, a = scipy.signal.iirnotch(freq / (fs / 2), q)
    filtered = scipy.signal.filtfilt(b, a, samples).astype(np.int16)
    filtered_audio = sound._spawn(filtered.tobytes())
    filtered_audio.export(output_path, format="wav")

def apply_amplitude_modulation(input_path, output_path, rate=5):
    sound = AudioSegment.from_file(input_path)
    samples = np.array(sound.get_array_of_samples())
    fs = sound.frame_rate
    duration = len(samples) / fs
    t = np.linspace(0, duration, num=len(samples))
    modulator = 0.5 * (1 + np.sin(2 * np.pi * rate * t))
    modulated = samples * modulator
    modulated = np.clip(modulated, -2**15, 2**15-1)
    modulated_audio = sound._spawn(modulated.astype(np.int16).tobytes())
    modulated_audio.export(output_path, format="wav")

# 🔄 Pitch 주파수 맵
pitch_freq_map = {
    "125Hz": 125,
    "250Hz": 250,
    "500Hz": 500,
    "1kHz": 1000,
    "2kHz": 2000,
    "4kHz": 4000,
    "8kHz": 8000
}

# 🔁 치료 기능
if st.session_state.step == 4:
    st.header("🎧 [치료 기능] 맞춤형 음원 치료")
    st.markdown("""
Pitch 및 Loudness 측정 결과를 기반으로
맞춤형 사운드가 적용됩니다. 골전도 또는 일반 이어폰으로 사용 가능합니다.
""")

    st.subheader("🎵 음원 선택")
    uploaded = st.file_uploader("🎶 좋아하는 음악 업로드 (mp3, wav)", type=["mp3", "wav"])
    if uploaded is not None:
        path = f"uploaded_{uploaded.name}"
        with open(path, "wb") as f:
            f.write(uploaded.read())
        st.session_state.audio_file = path
        st.audio(path)

    if st.session_state.audio_file:
        st.subheader("⚙️ Modulation 설정")
        st.session_state.filter_type = st.radio("필터 타입 선택", ["Amplitude Modulation", "Notch Filtering"])
        mod_rate = st.slider("Modulation Rate (Hz)", 1, 20, 5)
        q_value = st.slider("Notch Filter Q 값", 5, 100, 30)
        duration = st.slider("치료 시간 (분)", 5, 60, 15)

        output_path = "modulated_audio.wav"
        intermediate_path = "notch_filtered.wav"

        pitch = st.session_state.matching_info.get("Pitch", "1kHz")
        notch_freq = pitch_freq_map.get(pitch, 1000)

        if st.button("치료 시작"):
            if st.session_state.filter_type == "Notch Filtering":
                apply_notch_filter(st.session_state.audio_file, intermediate_path, freq=notch_freq, q=q_value)
                apply_amplitude_modulation(intermediate_path, output_path, rate=mod_rate)
            else:
                apply_amplitude_modulation(st.session_state.audio_file, output_path, rate=mod_rate)

            st.audio(output_path)
            st.success(f"{duration}분 치료를 시작합니다. 음원: {st.session_state.audio_file}")

