from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=api_key)

def get_ai_response(messages):
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "너는 사용자를 도와주는 상담사야."}, 
    ]

    while True:
        user_input = input("사용자: ")
        if user_input.lower() in ["종료", "끝", "exit", "quit"]:
            print("상담을 종료합니다. 안녕히 가세요!")
            break

        messages.append({"role": "user", "content": user_input})
        ai_response = get_ai_response(messages)
        messages.append({"role": "assistant", "content": ai_response})
        print("AI: " + ai_response)