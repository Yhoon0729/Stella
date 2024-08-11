from django.shortcuts import render
import FinanceDataReader as fdr

def index(request):
    # KOSPI 주식 목록 가져오기
    kospi_stocks = fdr.StockListing('KOSPI')

    # 상위 3개 종목 선택 (등락률 기준)
    top_3_ChagesRatio = kospi_stocks.sort_values(by='ChagesRatio', ascending=False).head(3)

    # 등락 상위 3개 종목 주식 데이터 리스트로 준비
    top_3_stocks = []
    for i in range(len(top_3_ChagesRatio)):
        stock_data = {
            'code': top_3_ChagesRatio.iloc[i].Code,
            'name': top_3_ChagesRatio.iloc[i].Name,
            'close': top_3_ChagesRatio.iloc[i].Close,
            'change': top_3_ChagesRatio.iloc[i].Changes,
            'chagesRatio':top_3_ChagesRatio.iloc[i].ChagesRatio,
        }
        top_3_stocks.append(stock_data)

    context = {
        'top_3_stocks' : top_3_stocks,
    }
    return render(request, 'index.html', context)