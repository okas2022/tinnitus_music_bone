import streamlit as st
import pandas as pd
import datetime
import os
import csv
import json
from pydub import AudioSegment
import scipy.signal
import numpy as np

# ✅ 반드시 첫 줄에 위치해야 함!
st.set_page_config(page_title="Tinnitus Therapy", layout="centered")

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

# 앱 제목 및 안내
st.title("🎵 음악으로 이명 치료하다")
st.markdown("## 🎧 Tinnitus Sound Therapy App")
st.markdown("<style> @keyframes fadein { from {opacity:0;} to {opacity:1;} } .slide { animation: fadein 1s ease-in-out; } </style>", unsafe_allow_html=True)

# 사용자 정보 저장 파일 경로
data_file = "user_data.csv"
if not os.path.exists(data_file):
    with open(data_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["이름", "전화번호", "이메일", "생년월일", "저장일시"])

# 사용자 정보 입력 및 저장
if st.session_state.step == 0:
    st.header("👤 사용자 정보 입력")
    name = st.text_input("이름")
    phone = st.text_input("전화번호")
    email = st.text_input("이메일 (선택사항)")
    birth = st.date_input("생년월일", value=datetime.date(1990, 1, 1))

    if st.button("정보 저장 및 다음으로 이동"):
        with open(data_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, phone, email, str(birth), str(datetime.datetime.now())])
        st.session_state.user_info = {
            "이름": name,
            "전화번호": phone,
            "이메일": email,
            "생년월일": str(birth)
        }
        st.success("사용자 정보가 저장되었습니다.")
        st.session_state.step = 1

# 설문
if st.session_state.step == 1:
    st.header("📋 이명 관련 간단 설문")
    q1 = st.radio("최근 1주일 간 이명으로 인해 불편함을 느끼셨나요?", ["예", "아니오"])
    q2 = st.radio("하루 중 이명이 가장 심하게 느껴지는 시간대는 언제인가요?", ["아침", "낮", "저녁", "밤", "일관되게 지속됨"])
    q3 = st.slider("현재 느끼는 이명의 강도는 어느 정도인가요? (0=전혀 없음, 10=매우 심함)", 0, 10, 5)

    if st.button("설문 저장 및 다음 단계로 이동"):
        st.session_state.survey_result = {
            "이명 불편 여부": q1,
            "이명 시간대": q2,
            "이명 강도": q3,
            "응답 시간": str(datetime.datetime.now())
        }
        st.success("설문이 저장되었습니다. 다음 단계로 이동하세요.")
        st.session_state.step = 2

# 설문 결과 확인
if st.session_state.step == 2:
    st.header("📊 설문 결과 확인")
    st.write(pd.DataFrame([st.session_state.survey_result]))
    st.info("다음 단계 기능은 추후 추가 가능합니다.")

# 저장된 사용자 목록 확인
with st.expander("📁 저장된 사용자 목록 보기"):
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
        st.dataframe(df)
    else:
        st.warning("아직 저장된 사용자가 없습니다.")

# 앱 초기 설정
st.set_page_config(page_title="Tinnitus Therapy", layout="centered")
st.title("🎵 음악으로 이명 치료하다")
st.markdown("## 🎧 Tinnitus Sound Therapy App")
st.markdown("<style> @keyframes fadein { from {opacity:0;} to {opacity:1;} } .slide { animation: fadein 1s ease-in-out; } </style>", unsafe_allow_html=True)

slide_images = [
    ("https://cdn.pixabay.com/photo/2017/03/15/11/18/music-2147801_960_720.jpg", "Step 1: 음악을 통한 이명 이해"),
    ("https://cdn.pixabay.com/photo/2016/11/29/06/18/sound-1868958_960_720.jpg", "Step 2: 개인별 Pitch와 강도 분석"),
    ("https://cdn.pixabay.com/photo/2015/01/09/11/11/headphones-594183_960_720.jpg", "Step 3: 골전도 디바이스로 소리치료")
]
slide_idx = st.slider("슬라이드 보기", 0, len(slide_images)-1, 0)
img_url, caption = slide_images[slide_idx]
st.image(img_url, caption=caption, use_column_width=True)

# 온보딩 단계 (Step -1)
if st.session_state.step == -1:
    st.header("당신의 이명을 이해합니다")
    st.subheader("오늘, 그 소리에 작별을 시작해보세요.")
    st.markdown("이 앱은 당신의 이명을 진심으로 이해하고, 당신만을 위한 맞춤형 치료 여정을 돕습니다.")
    st.markdown("---")
    st.markdown("✅ 간단한 이명 자가진단")
    st.markdown("✅ 청력 확인용 간이 테스트")
    st.markdown("✅ 이명 강도 및 주파수 매칭")
    st.markdown("---")
    if st.button("시작하기"):
        st.session_state.step = 0

# 세션 상태 초기화
if "mode" not in st.session_state:
    st.session_state.mode = None
if "step" not in st.session_state:
    st.session_state.step = -1
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
        st.session_state.step = 6

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

# 순음 청력검사
elif st.session_state.step == 1.5:
    st.header("🎧 순음 청력검사")
    st.markdown("500Hz, 2000Hz, 4000Hz, 8000Hz에서 20~80dB의 소리에 반응하는지 입력해주세요.")
    thresholds = [20, 40, 60, 80]
    freqs = [500, 2000, 4000, 8000]
    hearing_result = {}
    for f in freqs:
        st.subheader(f"주파수: {f}Hz")
        for t in thresholds:
            key = f"hearing_{f}_{t}"
            heard = st.radio(f"{t}dB에서 들리셨나요?", ["예", "아니오"], key=key)
            hearing_result[key] = heard
    st.session_state.health_info['pure_tone_test'] = hearing_result
    threshold_values = [(int(k.split("_")[1]), int(k.split("_")[2])) for k, v in hearing_result.items() if v == "예"]
    if threshold_values:
        df_thresh = pd.DataFrame(threshold_values, columns=["freq", "db"])
        avg_thresh = df_thresh.groupby("freq")["db"].min().mean()
        if avg_thresh < 40:
            st.session_state.tinnitus_level = 3
        elif avg_thresh < 60:
            st.session_state.tinnitus_level = 5
        elif avg_thresh < 80:
            st.session_state.tinnitus_level = 7
        else:
            st.session_state.tinnitus_level = 9
        st.markdown(f"👉 평균 청력 역치: {avg_thresh:.1f} dB → 이명 강도 조정: {st.session_state.tinnitus_level}")
        if st.button("다음 (난청 설문)"):
            st.session_state.step = 2

    if st.button("다음 (난청 설문)"):
        st.session_state.step = 2

# 건강 설문
elif st.session_state.step == 2:
    st.header("🦻 난청 관련 설문")
    hearing_questions = [
        "양쪽 귀 중 한쪽 귀만 잘 들리시나요?",
        "일상 대화 중 TV 또는 라디오 음량을 높여야 하나요?",
        "조용한 환경에서는 대화가 가능하나, 시끄러운 환경에서는 어려움이 있으신가요?",
        "사람들의 말을 자주 되묻거나 오해하신 적이 있나요?",
        "전화 통화 시 상대방 말소리를 듣기 어려운 편인가요?",
        "최근 청력 저하를 느낀 적이 있나요?"
    ]
    hearing_responses = {q: st.radio(q, ["예", "아니오"], key=f"hear_{i}") for i, q in enumerate(hearing_questions)}
    col1, col2 = st.columns([1,1])
    if col1.button("이전 (사용자 정보)"):
        st.session_state.step = 1
    if col2.button("다음 (어지러움 설문)"):
        st.session_state.health_info.update(hearing_responses)
        st.session_state.step = 2.1

elif st.session_state.step == 2.1:
    st.header("🌀 어지러움/균형 관련 설문")
    dizziness_questions = [
        "최근 1개월 내 어지러움을 느끼신 적이 있나요?",
        "자세를 바꿀 때 순간적으로 어지러움을 느끼시나요?",
        "걸을 때 중심을 잃거나 휘청거린 적이 있나요?",
        "어지럼증과 함께 메스꺼움이나 구토가 동반된 적이 있나요?",
        "어지럼증으로 일상 활동에 제한이 있었나요?",
        "최근 쓰러지거나 낙상한 경험이 있으신가요?"
    ]
    dizziness_responses = {q: st.radio(q, ["예", "아니오"], key=f"dizzy_{i}") for i, q in enumerate(dizziness_questions)}
    col1, col2 = st.columns([1,1])
    if col1.button("이전 (난청 설문)"):
        st.session_state.step = 2
    if col2.button("다음 (만성질환 설문)"):
        st.session_state.health_info.update(dizziness_responses)
        st.session_state.step = 2.2

elif st.session_state.step == 2.2:
    st.header("🧬 만성질환 및 생활습관 설문")
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
    chronic_responses = {}
    for i, (q, opt) in enumerate(chronic_questions):
        if opt == "number":
            chronic_responses[q] = st.number_input(q, min_value=0, max_value=24, key=f"chronic_{i}")
        else:
            chronic_responses[q] = st.radio(q, opt, key=f"chronic_{i}")
    col1, col2 = st.columns([1,1])
    if col1.button("이전 (어지러움 설문)"):
        st.session_state.step = 2.1
    if col2.button("다음 (THI 설문)"):
        st.session_state.health_info.update(chronic_responses)
        st.session_state.step = 3
        st.session_state.health_info.update(chronic_responses)
        st.session_state.step = 3
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

# 치료 결과 분석용 데이터 저장 리스트 초기화
if 'treatment_history' not in st.session_state:
    st.session_state.treatment_history = []
from pydub import AudioSegment
import scipy.signal
import numpy as np
import numpy as np

# Notch filtering 함수 추가

def apply_notch_filter(input_path, output_path, freq=1000, q=30):
    sound = AudioSegment.from_file(input_path)
    samples = np.array(sound.get_array_of_samples())
    fs = sound.frame_rate
    b, a = scipy.signal.iirnotch(freq / (fs / 2), q)
    filtered = scipy.signal.filtfilt(b, a, samples).astype(np.int16)
    filtered_audio = sound._spawn(filtered.tobytes())
    filtered_audio.export(output_path, format="wav")

# 간단한 amplitude modulation 예시 함수
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

if st.session_state.step == 4:
    st.header("🔎 [2단계] 맞춤 치료 설정")
    st.markdown("""
    당신만의 이명 소리 특성을 기반으로 맞춤형 사운드 처방이 제공됩니다.
    아래 정보를 입력해주세요.
    """)

    st.subheader("📌 Pitch & Loudness Matching")
    st.session_state.tinnitus_level = st.slider("이명 강도 (0~10)", 0, 10, st.session_state.tinnitus_level)
    tinnitus_pitch = st.select_slider("이명 주파수 대역", options=["125Hz", "250Hz", "500Hz", "1kHz", "2kHz", "4kHz", "8kHz"])
    ear_side = st.radio("이명이 더 많이 느껴지는 쪽", ["왼쪽", "오른쪽", "양쪽"])

    st.subheader("🎧 소리 치료 타입 선택")
    sound_type = st.radio("청력 유형에 따라 추천되는 사운드 치료 타입", ["TMNMT (특정 주파수 제거형)", "Broadband (전체 대역 소리)"])

    if st.button("다음 (치료 세션 시작)"):
        st.session_state.matching_info = {
            "Pitch": tinnitus_pitch,
            "Ear Side": ear_side,
            "Sound Type": sound_type
        }
        st.session_state.step += 1

elif st.session_state.step == 7:
    st.header("📈 [5단계] 정량적 진척 확인 및 동기 강화")
    st.markdown("""
3일 연속 치료 성공!
평균 이명 강도 20% 감소했어요.
""")

    st.subheader("📊 주간/월간 리포트")
    st.markdown("(예시) 이번 주 평균 이명 강도: 4.2 → 지난 주 대비 ▼ 18% 감소")

    st.subheader("🎮 점수 기반 레벨업")
    st.markdown("현재 레벨: Lv.2 👂 이명 탐험가")
    st.progress(60)

    st.subheader("👥 커뮤니티 포럼")
    st.markdown("비슷한 경험을 가진 사람들과 이야기 나누어보세요. (준비 중)")

    if st.button("다음 (전문가 연결 단계)"):
        st.session_state.step += 1

elif st.session_state.step == 8:
    st.header("🏥 [6단계] 전문가 연계 및 기기 업그레이드")
    st.markdown("""
이명이 지속된다면 전문가의 진료를 받아보는 것이 도움이 됩니다.
필요 시 병원 예약 및 보조기기 구입 연계 서비스를 안내드립니다.
""")

    st.subheader("🔗 병원 연계 예약 시스템")
    st.markdown("원하시는 경우 가까운 이비인후과 전문의를 예약해드립니다.")
    st.button("병원 예약 연결하기 (준비 중)")

    st.subheader("🎧 골전도 헤드셋 구매")
    st.markdown("치료 효과를 높이기 위한 전용 골전도 기기를 안내해드립니다.")
    st.button("기기 구매하러 가기 (준비 중)")

    st.subheader("📄 진료 참고용 PDF 리포트")
    st.markdown("이 앱에서 입력한 정보와 설문 결과를 요약하여 병원에 전달할 수 있습니다.")
    st.button("PDF 리포트 다운로드 (준비 중)")

# 사용자 이력 저장 함수
import json

def save_user_history():
    user_data = {
        "user": st.session_state.user_info,
        "health": st.session_state.health_info,
        "thi": st.session_state.thi_results,
        "timestamp": str(datetime.datetime.now())
    }
    user_file = f"history_{st.session_state.user_email.replace('@', '_at_')}.json"
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            existing = json.load(f)
    else:
        existing = []
    existing.append(user_data)
    with open(user_file, 'w') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

# 사용자 이력 불러오기
st.sidebar.markdown("---")
st.sidebar.subheader("📂 내 설문 이력 보기")
if st.sidebar.button("이전 설문 불러오기"):
    user_file = f"history_{st.session_state.user_email.replace('@', '_at_')}.json"
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            history_data = json.load(f)
        st.session_state.history_data = history_data
        st.sidebar.success(f"{len(history_data)}개의 이력이 불러와졌습니다.")
    else:
        st.sidebar.error("이전 이력이 없습니다.")

if "history_data" in st.session_state:
    st.sidebar.selectbox("📅 불러올 이력 선택", options=[f["timestamp"] for f in st.session_state.history_data], key="history_selected")
    selected = [h for h in st.session_state.history_data if h["timestamp"] == st.session_state.history_selected][0]
    if st.sidebar.button("이력 보기"):
        st.header("📜 저장된 이력 보기")
        st.subheader("👤 사용자 정보")
        st.write(pd.DataFrame([selected["user"]]))
        st.subheader("🩺 건강 설문")
        st.write(pd.DataFrame.from_dict(selected["health"], orient='index', columns=["응답"]))
        st.subheader("📝 THI 결과")
        st.write(pd.DataFrame.from_dict(selected["thi"], orient='index', columns=["응답"]))

elif st.session_state.step == 9:
    st.header("🎧 [치료 기능] 맞춤형 음원 치료")
    st.markdown("""
Pitch 및 Loudness 측정 결과를 기반으로
맞춤형 사운드가 적용됩니다. 골전도 또는 일반 이어폰으로 사용 가능합니다.
""")

    st.subheader("🎵 음원 선택")
    st.markdown("관리자 등록 음원을 선택하거나, 본인이 원하는 음악을 업로드할 수 있습니다.")
    user_uploaded = st.file_uploader("🎶 좋아하는 음악 업로드 (mp3, wav)", type=["mp3", "wav"])
    if user_uploaded is not None:
        with open(f"uploaded_{user_uploaded.name}", "wb") as f:
            f.write(user_uploaded.read())
        sound_files.append(f"uploaded_{user_uploaded.name}")
    
    sound_files = os.listdir("music") if os.path.exists("music") else []
    selected_sound = st.selectbox("사용할 음원 선택", sound_files)

    st.subheader("⚙️ Modulation 설정")
    mod_rate = st.slider("Modulation 강도 (Hz)", 1, 20, 5)
    st.session_state.filter_type = st.radio("필터 타입 선택", ["Amplitude Modulation", "Notch Filtering (예정)"])
    q_value = st.slider("Notch Filter Q 값 (좁을수록 깊은 차단)", min_value=5, max_value=100, value=30)

    st.write(f"이명 Pitch: {st.session_state.matching_info['Pitch']}, 강도: {st.session_state.tinnitus_level}")
    st.markdown("""
    *Pitch에 따른 notch-filtering 또는 amplitude modulation 알고리즘이 자동 적용됩니다.*

    예시 알고리즘:
    - Notch Filter: 특정 주파수 대역(예: {st.session_state.matching_info['Pitch']})를 제거하는 필터 적용
    - Amplitude Modulation: 사인파 진폭 조절 (1~10Hz)로 이명 억제 효과 유도

    추후 `pydub`, `scipy`, `librosa` 등 라이브러리를 활용하여 실시간 음원 처리 기능 추가 예정입니다.
    """)

    st.subheader("⏱ 치료 시간 설정")
    duration = st.slider("치료 시간 (분)", 5, 60, 15)

    if selected_sound:
        if os.path.exists(f"uploaded_{selected_sound}"):
            st.audio(f"uploaded_{selected_sound}", format='audio/mp3')
        elif os.path.exists(f"music/{selected_sound}"):
            st.audio(f"music/{selected_sound}", format='audio/mp3')

    if st.button("치료 시작"):
        st.subheader("🔊 음량 조절 및 피드백")
        volume = st.slider("음량 (0.0 ~ 1.0)", 0.0, 1.0, 0.8, step=0.1)
        feedback = st.radio("치료 후 느낌을 선택해주세요", ["개선됨", "변화 없음", "악화됨"])
        st.session_state.feedback_log = {
            "volume": volume,
            "feedback": feedback,
            "note": st.text_area("자유롭게 치료 후 느낀 점을 작성해주세요 (이명 일기)", placeholder="오늘 치료를 마친 후 느낀 점을 적어보세요...")
        }
        st.audio(input_path, format='audio/wav')
        st.markdown("⏯ **치료 시작 전 필터 테스트 시청**")
        st.audio(output_path, format='audio/wav')
        input_path = f"music/{selected_sound}" if os.path.exists(f"music/{selected_sound}") else f"uploaded_{selected_sound}"
intermediate_path = "notch_filtered.wav"
output_path = "modulated_audio.wav"

pitch_freq_map = {
    "125Hz": 125,
    "250Hz": 250,
    "500Hz": 500,
    "1kHz": 1000,
    "2kHz": 2000,
    "4kHz": 4000,
    "8kHz": 8000
}
notch_freq = pitch_freq_map.get(st.session_state.matching_info["Pitch"], 1000)

if st.session_state.filter_type == "Notch Filtering (예정)":
        apply_notch_filter(input_path, intermediate_path, freq=notch_freq, q=q_value)
        apply_amplitude_modulation(intermediate_path, output_path, rate=mod_rate)
else:
    apply_amplitude_modulation(input_path, output_path, rate=mod_rate)
    st.audio(output_path, format='audio/wav')
    st.success(f"{duration}분 치료를 시작합니다. 음원: {selected_sound}")
    

# 결과 요약

