import yfinance as yf

def get_company_info(ticker: str) -> str:
    """ 주식 티커(symbol)를 입력받아 해당 회사의 기본 정보 반환 """
    ticketer = yf.Ticker(ticker)
    print("ticker info : ", ticketer.info)
    return str(ticketer.info)

def get_historical_data(ticker: str, period: str  = "1day"):
    """ 주식 티커와 일자를 입력으로 받아 해당 회사의 최근 주가 정보 반환"""
    ticketer = yf.Ticker(ticker)
    history = ticketer.history(period=period)
    print(f"ticker history : {history}") # 데이터프레임 정보를 마크다운으로 정보 변환
    return history.to_markdown()

def get_recommendations(ticker: str):
    """ 입력 받은 주식 티커의 애널리스트 투자 의견 이력을 조회하여 정보 반환"""
    ticketer = yf.Ticker(ticker)
    recommendations = ticketer.recommendations
    print(f"ticker = {ticker}, recommendations : {recommendations}")
    return recommendations.to_markdown() # 데이터프레임 정보를 마크다운으로 정보 변환


# function calling 기능으로 사용하기 위한 설명 추가
tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "get_company_info",
            "description" : "주식 티커(symbol)를 입력받아 해당 회사의 기본 정보를 반환합니다. 예: MSFT, AAPL 등",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "ticker" : {
                        "type" : "string",
                        "description" : "주식 티커(symbol) (예: MSFT, AAPL 등)"
                    },
                },
                "required" : ["ticker"]
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "get_historical_data",
            "description" : "주식 티커와 일자를 입력으로 받아 해당 회사의 최근 주가 정보 반환합니다. 예: MSFT, AAPL 등",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "ticker" : {
                        "type" : "string",
                        "description" : "주식 티커(symbol) (예: MSFT, AAPL 등)"
                    },
                    "period" : {
                        "type" : "string",
                        "description" : "주가 정보 조회할 기간 (예: 2d(지난 2일간), 2mo(지난 2달간) 등)"
                    },
                },
                "required" : ["ticker", "period"]
            }
        }
    },
    {
        "type" : "function",
        "function" : {
            "name" : "get_recommendations",
            "description" : "입력 받은 주식 티커의 애널리스트 투자 의견 이력을 조회하여 반환합니다.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "ticker" : {
                        "type" : "string",
                        "description" : "주식 티커(symbol) (예: MSFT, AAPL 등)"
                    },
                },
                "required" : ["ticker"]
            }
        }
    }
]


if __name__ == "__main__":
    get_company_info("MSFT")
    print("----------------")
    get_historical_data("AAPL", "2d")
    print("----------------")
    get_recommendations("AAPL")