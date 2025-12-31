from datetime import datetime

def get_current_time():
    """ 현재 시간(YYYY-MM-DD HH:MM:SS) 반환 """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(current_time)
    return current_time

# function calling 기능으로 사용하기 위한 설명 추가
tools = [
    {
        "type": "function",
        "function" : {
            "name" : "get_current_time",
            'description': '현재 시간을 YYYY-MM-DD HH:MM:SS 형식으로 반환합니다.',
        }
    },
]

if __name__ == "__main__" :
    get_current_time()