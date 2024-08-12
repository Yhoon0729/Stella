import requests
from bs4 import BeautifulSoup

def get_stock_industry(stock_code):
    url = f"https://finance.naver.com/item/main.nhn?code={stock_code}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 산업 정보를 포함하는 테이블을 찾습니다
    table = soup.select_one('table.table_dot_h')
    
    if table:
        # 테이블의 모든 행을 순회합니다
        for row in table.select('tr'):
            th = row.select_one('th')
            td = row.select_one('td')
            if th and td and '산업' in th.text:
                return td.text.strip()
    
    return "정보 없음"

# 사용 예
stock_code = '005930'  # 삼성전자
industry = get_stock_industry(stock_code)
print(f"종목코드 {stock_code}의 산업: {industry}")