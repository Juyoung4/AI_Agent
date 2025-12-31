from datetime import datetime
import pytz # 타임존 설정 라이브러리

def get_current_time(timezone: str = "Asia/Seoul"):
    """ 현재 시간(YYYY-MM-DD HH:MM:SS) 반환 """
    try:
        tz = pytz.timezone(timezone)
    except pytz.UnknownTimeZoneError:
        tz = pytz.timezone("Asia/Seoul")  # 기본값으로 설정

    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    print(current_time)
    return current_time

# function calling 기능으로 사용하기 위한 설명 추가
tools = [
    {
        "type": "function",
        "function" : {
            "name" : "get_current_time",
            'description': '현재 시간을 YYYY-MM-DD HH:MM:SS 형식으로 반환합니다. 선택적으로 타임존을 지정할 수 있습니다. 예: Asia/Seoul, America/New_York 등.',
            'parameters': {
                'type': "object",
                'properties': {
                    'timezone': {
                        'type': 'string',
                        'description': '타임존 이름 (예: Asia/Seoul, America/New_York). 기본값은 Asia/Seoul입니다.'
                    }
                },
                'required': ['timezone']
            }
        }
    },
]

if __name__ == "__main__" : 
    get_current_time("Asia/Seoul")