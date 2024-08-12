import requests
import pandas as pd
import io

def get_stock_sector():
    gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    gen_otp_data = {
        'mktId': 'STK',
        'trdDd': '20230629',
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT03901'
    }
    
    headers = {'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader'}
    otp = requests.post(gen_otp_url, gen_otp_data, headers=headers).text
    
    down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
    down_data = {'code': otp}
    
    r = requests.post(down_url, down_data, headers=headers)
    
    df = pd.read_csv(io.BytesIO(r.content), encoding='EUC-KR')
    print(df.columns)  # 열 이름 출력
    return df

def get_stock_info(stock_code):
    df = get_stock_sector()
    # 종목코드 열의 실제 이름을 확인하고 수정
    code_column = '종목코드'  # 또는 'ISU_CD' 등 실제 열 이름으로 수정
    if code_column not in df.columns:
        print(f"Available columns: {df.columns}")
        return None
    
    # 종목코드를 문자열로 변환하고 앞에 0을 채워 6자리로 만듦
    stock_code = str(stock_code).zfill(6)
    stock_info = df[df[code_column] == stock_code]
    
    if not stock_info.empty:
        return {
            'name': stock_info['종목명'].values[0] if '종목명' in df.columns else 'N/A',
            'sector': stock_info['업종명'].values[0] if '업종명' in df.columns else 'N/A',
            'industry': stock_info['산업군'].values[0] if '산업군' in df.columns else 'N/A'
        }
    return None

# 사용 예
stock_info = get_stock_info('005930')  # 삼성전자의 정보
if stock_info:
    print(f"종목명: {stock_info['name']}")
    print(f"업종: {stock_info['sector']}")
    print(f"산업군: {stock_info['industry']}")
else:
    print("종목 정보를 찾을 수 없습니다.")