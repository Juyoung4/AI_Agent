from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st

from get_finance_functions2 import tools, get_company_info, get_historical_data, get_recommendations

TOOL_DISPATCHER = {
    "get_company_info": get_company_info,
    "get_historical_data": get_historical_data,
    "get_recommendations": get_recommendations,
}

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
    
    # streamlit chat message 렌더링
    for message in st.session_state.messages:
        if message["role"] == "assistant" or message["role"] == "user": # assistant 혹은 user 메시지인 경우만
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
            # ai가 호출하는 call_tool이 있으면 반드시 message에 추가
            #st.session_state.messages.append(ai_message)
            # ✅ 여기! 객체 그대로 넣지 말고 model_dump로 dict로 변환해서 저장
            st.session_state.messages.append(
                ai_message.model_dump(exclude_none=True)
            )

            tool_calls_list = ai_message.tool_calls

            # ai가 요청한 tool_calls들 처리하기 위한 부분
            for tool_call in tool_calls_list:
                tool_name = tool_call.function.name
                tool_id = tool_call.id
                arguments = json.loads(tool_call.function.arguments)

                if tool_name not in TOOL_DISPATCHER:
                    print(f"알 수 없는 도구 호출: {tool_name}")
                    raise ValueError(f"알 수 없는 도구 호출: {tool_name}")
            
                result = TOOL_DISPATCHER[tool_name](**arguments)
                
                # tool 호출 결과를 message에 추가
                st.session_state.messages.append({
                    "role": "tool",
                    "tool_call_id" : tool_id,
                    "content" : result,
                })

            # 도구 호출 결과를 바탕으로 다시 ai에게 응답을 얻기 위해서 요청
            st.session_state.messages.append({'role': "system", "content": "주어진 결과를 바탕으로 답변해야 한다"})
            ai_response = get_ai_response(st.session_state.messages, tools=tools)
            ai_message = ai_response.choices[0].message

        # Final AI response 추가
        st.session_state.messages.append({"role": "assistant", "content": ai_message.content})
        print("AI\t:", ai_message.content)
        st.chat_message("assistant").write(ai_message.content)