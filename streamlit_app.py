import streamlit as st

st.set_page_config(page_title="생물 다양성 퀴즈", page_icon="🧬")
st.title("🧬 생물 다양성 퀴즈")

# 문항 이미지
st.subheader("1.")
st.image("images/다양성.png", caption="문항 이미지", use_container_width=True)

# 선택지를 가로로 표시
options = ["① ㄱ", "② ㄴ", "③ ㄱ, ㄴ", "④ ㄴ, ㄷ", "⑤ ㄱ, ㄴ, ㄷ"]
cols = st.columns(len(options))

selected = None
for i, col in enumerate(cols):
    if col.button(options[i]):
        selected = options[i]
        st.session_state["q1"] = selected  # 저장

# 정답 확인 버튼
if st.button("정답 확인", key="check_q1"):
    if st.session_state.get("q1") == "⑤ ㄱ, ㄴ, ㄷ":
        st.success("정답입니다! 🎉")
    else:
        st.error("틀렸습니다. 다시 풀어보세요.")
