import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

with st.sidebar:
    api_key = os.getenv("OPEN_AI_API_KEY")
    
    "[OpenAI API Key 설정하기](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("간단한 Streamlit 챗봇")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "무엇을 도와드릴까요?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    if not api_key:
        st.info("OpenAI API Key가 설정되지 않았습니다. 사이드바에서 설정해주세요.")
        st.stop()

    client = OpenAI(api_key=api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=st.session_state.messages
    )

    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)