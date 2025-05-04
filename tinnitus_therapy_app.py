import streamlit as st

# 앱 초기 설정
st.set_page_config(page_title="Tinnitus Therapy", layout="centered")
st.title("🎧 Tinnitus Sound Therapy App")

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 1
if "tinnitus_level" not in st.session_state:
    st.session_state.tinnitus_level = 5
if "audio_file" not in st.session_state:
    st.session_state.audio_file = None

# 단계 제어 함수
def next_step():
    st.session_state.step += 1

# 단계별 UI
if st.session_state.step == 1:
    st.header("Welcome")
    st.markdown("Your journey to sound relief starts here.")
    if st.button("Get Started"):
        next_step()

elif st.session_state.step == 2:
    st.header("Tinnitus Intensity Level")
    st.session_state.tinnitus_level = st.slider("How loud is your tinnitus?", 0, 10, st.session_state.tinnitus_level)
    if st.button("Next"):
        next_step()

elif st.session_state.step == 3:
    st.header("Upload Therapy Music")
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])
    if uploaded_file:
        st.session_state.audio_file = uploaded_file
        st.audio(uploaded_file, format='audio/mp3')
        if st.button("Next"):
            next_step()
    else:
        st.warning("Please upload a sound file to proceed.")

elif st.session_state.step == 4:
    st.header("Session In Progress")
    st.markdown(f"**Tinnitus Intensity Level:** {st.session_state.tinnitus_level}")
    if st.session_state.audio_file:
        st.audio(st.session_state.audio_file, format='audio/mp3')
    st.markdown("🔗 *Bluetooth connection must be managed by the device system*.")
    if st.button("Finish Session"):
        next_step()

elif st.session_state.step == 5:
    st.header("Session Complete 🎉")
    st.success("Great job! Your sound therapy session is complete.")
    if st.button("Start Over"):
        st.session_state.step = 1
