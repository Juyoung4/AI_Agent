from openai import OpenAI
from dotenv import load_dotenv
import os

def summarize_text(path: str, client: OpenAI) -> str:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {
                "role": "system",
                "content": f""""당신은 뛰어난 한국어 요약 전문가입니다.아래 글을 읽고, 저자의 문제 인식과 주장을 파악하고, 주요 내용을 요약합니다.
                출력 포맷은 다음과 같습니다.
                # 제목
                ## 저자의 문제 인식 및 주장(15문장 이내)
                ## 저자 소개
                ## 요약문(200~300자 이내)
                ------------------------------------------ 원문 ------------------------------------------
                {text}"""
            }
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

    path = "./CH/chapter4/data/"
    txt_file_name = "KCI_FI003103066s.txt"
    txt_file_path = os.path.join(path, txt_file_name)

    summary = summarize_text(txt_file_path, client)

    with open(os.path.join(path+os.path.split(txt_file_name)[0], "summary.txt"), "w", encoding="utf-8") as f:
        f.write(summary)