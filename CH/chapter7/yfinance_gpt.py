from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st

from get_finance_functions import tools, get_company_info

load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

def get_ai_response(messages, tools=None):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
        tools=tools,
    )

    return response


if __name__ == "__main__":

    st.title("AI 주식 투자 상담")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content" : "넌 친절한 주식 투자 관련된 전문적인 상담사야."}
        ]
        
    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])
    
    if user_prompt := st.chat_input("사용자\t: "):

        if user_prompt in ["종료", "exit", "quit"]:
            print("상담을 종료합니다.")
    
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.chat_message("user").write(user_prompt)

        ai_response = get_ai_response(st.session_state.messages, tools=tools)
        ai_message = ai_response.choices[0].message
        print("AI\t:", ai_message)

        if ai_message.tool_calls:
            # ai tool_Call 추가
            st.session_state.messages.append(ai_message)

            tool_calls_list = ai_message.tool_calls

            # tool_calls 별로 처리하기 위한 부분
            for tool_call in tool_calls_list:
                tool_name = tool_call.function.name
                tool_id = tool_call.id

                if tool_name == "get_company_info":
                    arguments = json.loads(tool_call.function.arguments)
                    print("AI 요청 인자:", arguments)

                    st.session_state.messages.append({
                        "role": "tool",
                        "tool_call_id" : tool_id,
                        "content" : get_company_info(arguments['ticker']), # ③ 개발자가 실제 Python 함수 실행, ④ 실행 결과를 다시 모델에게 전달
                    })
            st.session_state.messages.append({'role': "system", "content": "주어진 결과를 바탕으로 답변해야 한다"})
            ai_response = get_ai_response(st.session_state.messages, tools=tools)
            ai_message = ai_response.choices[0].message
        st.session_state.messages.append({"role": "assistant", "content": ai_message.content})
        print("AI\t:", ai_message.content)
        st.chat_message("assistant").write(ai_message.content)