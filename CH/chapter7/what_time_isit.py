from openai import OpenAI
from dotenv import load_dotenv
from get_functions import tools, get_current_time
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

def get_ai_response(messages, tools=None):

    # ① tools를 LLM에게 전달
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
            ai_message = ai_response.choices[0].message # 이전까지는 text로 출력했지만, 이제는 function calling 떄문에 객체 형태로 받을 수 있음!
            print("AI\t:", ai_message)

            # ② 모델이 “함수 호출이 필요하다”고 판단하면
            if ai_message.tool_calls:
                
                # 1️⃣ assistant (tool_calls 포함) — 모델이 반환
                messages.append(ai_message)

                tool_name = ai_message.tool_calls[0].function.name
                tool_id = ai_message.tool_calls[0].id # fucntion calling의 고유 id 의미
                
                if tool_name == "get_current_time":
                    # 2️⃣ tool — 개발자가 실행 결과 전달 (정답)
                    messages.append({
                        "role": "tool",
                        "tool_call_id" : tool_id,
                        "content" : get_current_time(), # ③ 개발자가 실제 Python 함수 실행, ④ 실행 결과를 다시 모델에게 전달 (즉 get_current_time을 호출하고 그 결과를 실어 보냄)
                    })
                # 3️⃣ 다시 모델 호출 → 최종 assistant 응답 생성
                ai_response = get_ai_response(messages, tools=tools)
                ai_message = ai_response.choices[0].message
            messages.append(ai_message)
            print("AI\t:", ai_message.content)