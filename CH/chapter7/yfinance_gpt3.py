from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st
from collections import defaultdict

from get_finance_functions2 import tools, get_company_info, get_historical_data, get_recommendations

TOOL_DISPATCHER = {
    "get_company_info": get_company_info,
    "get_historical_data": get_historical_data,
    "get_recommendations": get_recommendations,
}

load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

def get_ai_response(messages, tools=None, stream=True):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        stream=stream,
        messages=messages,
        tools=tools,
    )

    if stream:
        for chunk in response:
            yield chunk # 생성된 응답의 내용을 yield로 순차적으로 반환함
    else:
        return response
    

def tool_list_to_tool_obs(tools):
    tool_call_dict = defaultdict(lambda: {"id": None, "function": {"arguments":"", "name": None}, "type":None})

    for tool_call in tools:
        # id가 None이 아닌 경우 설정
        if tool_call.id is not None:
            tool_call_dict[tool_call.index]["id"] = tool_call.id
        
        # 함수 이름이 None이 아닌 경우 설정
        if tool_call.function.name is not None:
            tool_call_dict[tool_call.index]["function"]["name"] = tool_call.function.name
        
        # 인자추가
        tool_call_dict[tool_call.index]["function"]["arguments"] += tool_call.function.arguments
        
        # type이 None이 아닌 경우 설정
        if tool_call.type is not None:
            tool_call_dict[tool_call.index]["type"] = tool_call.type
    
    tool_calls_list = list(tool_call_dict.values())

    return {"tool_calls" : tool_calls_list}

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
        print("ai_response\t:", ai_response)

        # 이제 응답은 ChatCompletionChunk 객체로 전달하고 그 객체안에 ChoiceDelta객체 안에 content를 뽑아야 chunk단위를 얻을 수 있다
        content = ""
        # function calling 리스트도 마찬가지로 tool_calls로 함수, 인자 등이 chunk로 쪼개져서 오기 떄문에 뽑아야한다.
        tool_chunks = []
        
        with st.chat_message("assistant").empty(): # 챗 메시지 초기화
            # chunk 메시지 마크다운으로 출력
            for chunk in ai_response:
                print(f"chunk : {chunk}")
                content_chunk = chunk.choices[0].delta.content
                if content_chunk: 
                    content += content_chunk
                    st.markdown(content)

                if chunk.choices[0].delta.tool_calls: tool_chunks += chunk.choices[0].delta.tool_calls

        print(f"확인1: {content}")
        print(f"확인2: {tool_chunks}")
        
        tool_obj = tool_list_to_tool_obs(tool_chunks)
        tool_calls = tool_obj.get("tool_calls", [])

        # tool_Calls 메시지 출력부분 빈값으로 보이는거 처리
        if len(tool_calls) > 0:
            tool_call_msg = [tool_call["function"] for tool_call in tool_calls]
            st.write(tool_call_msg)

        if tool_calls:
            # ✅ 먼저 assistant 메시지에 tool_calls를 추가 (tool 메시지 앞에 반드시 와야함)
            st.session_state.messages.append({
                "role": "assistant",
                "content": content,
                "tool_calls": tool_calls
            })
            
            # ai가 요청한 tool_calls들을 처리
            for tool_call in tool_calls:
                # tool_call은 dict 형태로 변환되어 있으므로 dict 접근을 사용
                tool_name = tool_call["function"]["name"]
                tool_id = tool_call["id"]
                arguments = json.loads(tool_call["function"]["arguments"])

                if tool_name not in TOOL_DISPATCHER:
                    print(f"알 수 없는 도구 호출: {tool_name}")
                    raise ValueError(f"알 수 없는 도구 호출: {tool_name}")

                result = TOOL_DISPATCHER[tool_name](**arguments)

                # tool 호출 결과를 message에 추가
                st.session_state.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_id,
                    "content": result,
                })

            # 도구 호출 결과를 바탕으로 다시 ai에게 응답을 얻기 위해서 요청
            st.session_state.messages.append({'role': "system", "content": "주어진 결과를 바탕으로 답변해야 한다"})
            ai_response = get_ai_response(st.session_state.messages, tools=tools)
            #ai_message = ai_response.choices[0].message

            content = ""
            with st.chat_message("assistant").empty(): # 챗 메시지 초기화
                # chunk 메시지 마크다운으로 출력
                for chunk in ai_response:
                    content_chunk = chunk.choices[0].delta.content
                    if content_chunk: 
                        content += content_chunk
                        st.markdown(content)

        # Final AI response 추가
        # 위에 chunk로 받은 결과 넣기
        st.session_state.messages.append({"role": "assistant", "content": content})
        print("AI\t:", content)