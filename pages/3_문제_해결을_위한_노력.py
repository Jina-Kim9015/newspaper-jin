import streamlit as st
import openai
import pandas as pd
import datetime
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="문제 해결을 위한 노력", page_icon="💡", layout="centered")
st.title("💡 문제 해결을 위한 노력")

CSV_FILE = "submitted_data.csv"

# 세션 상태 초기화
for key in ["personal_chat", "national_chat", "global_chat"]:
    if key not in st.session_state:
        st.session_state[key] = []

def ask_gpt(role, user_input):
    initial_prompts = {
        "personal": "생물 다양성을 지키기 위한 개인적 노력에는 어떤 것이 있을까요?",
        "national": "생태계를 보호하기 위한 국가의 노력에는 어떤 것이 있을까요?",
        "global": "국제적으로 협력하여 생물 다양성을 지키기 위한 노력에는 무엇이 있을까요?"
    }

    default_reask = {
        "personal": "그 행동이 환경이나 생물 다양성과 어떤 관련이 있을까요?",
        "national": "그 정책이 어떤 생태계 문제를 해결할 수 있다고 보시나요?",
        "global": "이 협력이 왜 생물 다양성 보호에 중요하다고 생각하나요?"
    }

    try:
        messages = [
            {"role": "system", "content": f"당신은 학생과 대화하며, 생물 다양성과 환경 보호를 위한 {role}적 노력에 대해 질문을 던지고 생각을 유도하는 역할입니다. 답을 제공하지 마세요."},
            {"role": "user", "content": user_input}
        ]

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()

        # GPT가 너무 설명식으로 답하면, 다시 질문 유도
        if any(x in reply for x in ["입니다", "할 수 있습니다", "좋은 방법입니다", "중요합니다"]):
            return default_reask[role]
        return reply
    except Exception as e:
        return f"GPT 호출 실패: {e}"

def chat_section(role, label):
    st.subheader(f"💬 {label}에 대한 생각 확장하기")

    # 초기 질문
    default_question = {
        "personal": "생물 다양성을 지키기 위해 개인이 할 수 있는 노력에는 어떤 것이 있을까요?",
        "national": "생태계를 지키기 위한 국가의 노력에는 어떤 것들이 있을까요?",
        "global": "국제적으로 협력하여 생물 다양성을 지키기 위해 어떤 노력이 필요할까요?"
    }

    # 대화 출력
    if len(st.session_state[role + "_chat"]) == 0:
        st.markdown(f"🤖 {default_question[role]}")
    else:
        for speaker, msg in st.session_state[role + "_chat"]:
            icon = "🧑" if speaker == "user" else "🤖"
            st.markdown(f"{icon} {msg}")

    # 입력창
    user_input = st.text_input(f"{label}에 대한 아이디어를 입력하세요", key=f"{role}_input")
    if st.button("💬 대화하기", key=f"{role}_submit"):
        if user_input:
            st.session_state[role + "_chat"].append(("user", user_input))
            reply = ask_gpt(role, user_input)
            st.session_state[role + "_chat"].append(("assistant", reply))
            st.rerun()

    st.text_area(f"📌 {label} 최종 정리", key=f"{role}_final", height=100)

# 대화형 섹션
chat_section("personal", "개인적 노력")
chat_section("national", "국가적 노력")
chat_section("global", "국제적 노력")

# 느낀 점
st.subheader("📝 느낀 점 정리")
reflection = st.text_area("이번 활동을 통해 느낀 점, 새롭게 알게 된 점 등을 적어보세요.", key="reflection")

# 제출 버튼 및 저장
st.markdown("---")
if st.button("📤 최종 제출"):
    try:
        article_data = st.session_state.get("article_data", {})
        combined_data = {
            **article_data,
            "effort_personal_final": st.session_state.get("personal_final", ""),
            "effort_national_final": st.session_state.get("national_final", ""),
            "effort_global_final": st.session_state.get("global_final", ""),
            "reflection": st.session_state.get("reflection", "")
        }

        df_new = pd.DataFrame([combined_data])
        if os.path.exists(CSV_FILE):
            df_exist = pd.read_csv(CSV_FILE)
            df_combined = pd.concat([df_exist, df_new], ignore_index=True)
        else:
            df_combined = df_new

        df_combined.to_csv(CSV_FILE, index=False)
        st.success("✅ 제출이 완료되었습니다. 감사합니다!")
    except Exception as e:
        st.error(f"제출 중 오류 발생: {e}")
