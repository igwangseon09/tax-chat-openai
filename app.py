import streamlit as st
from openai import OpenAI

# secrets에서 API 키 불러오기
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Streamlit Chatbot", page_icon="💬")
st.title("💬 Streamlit + OpenAI Chatbot")

# 세션 상태로 대화 기록 유지
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# 이전 대화 표시
for msg in st.session_state["messages"][1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 모델 응답 생성
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state["messages"]
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # 대화 기록에 추가
    st.session_state["messages"].append({"role": "assistant", "content": reply})
