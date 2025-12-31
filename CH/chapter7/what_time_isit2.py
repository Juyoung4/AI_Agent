from openai import OpenAI
from dotenv import load_dotenv
import os
from get_functions2 import tools, get_current_time
import json

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
    
    messages = [
        {"role": "system", "content" : "넌 친절한 상담사야."}
    ]

    while True:
        if user_prompt := input("사용자\t: "):

            if user_prompt in ["종료", "exit", "quit"]:
                print("상담을 종료합니다.")
                break
        
            messages.append({"role": "user", "content": user_prompt})

            ai_response = get_ai_response(messages, tools=tools)
            ai_message = ai_response.choices[0].message
            print("AI\t:", ai_message)

            if ai_message.tool_calls:
                # ai tool_Call 추가
                messages.append(ai_message)

                tool_name = ai_message.tool_calls[0].function.name
                tool_id = ai_message.tool_calls[0].id

                if tool_name == "get_current_time":
                    arguments = json.loads(ai_message.tool_calls[0].function.arguments)
                    print("AI 요청 인자:", arguments)

                    messages.append({
                        "role": "tool",
                        "tool_call_id" : tool_id,
                        "content" : get_current_time(arguments['timezone']), # ③ 개발자가 실제 Python 함수 실행, ④ 실행 결과를 다시 모델에게 전달 (즉 get_current_time을 호출하고 그 결과를 실어 보냄)
                    })

                ai_response = get_ai_response(messages, tools=tools)
                ai_message = ai_response.choices[0].message
            messages.append(ai_message)
            print("AI\t:", ai_message.content)