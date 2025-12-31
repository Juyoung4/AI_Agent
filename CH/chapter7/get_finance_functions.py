import yfinance as yf

def get_company_info(ticker: str) -> str:
    """ 주식 티커(symbol)를 입력받아 해당 회사의 기본 정보 반환 """
    ticketer = yf.Ticker(ticker)
    print("ticker info : ", ticketer.info)
    return str(ticketer.info)


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
    }
]


if __name__ == "__main__":
    get_company_info("MSFT")