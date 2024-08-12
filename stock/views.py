from django.shortcuts import render, redirect
from django.http import JsonResponse
import FinanceDataReader as fdr
from datetime import datetime, timedelta

from comments.views import get_comments


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def stock_info(request, stock_code):
    user_id = request.session.get('user_id')

    # KOSPI 목록 가져오기
    krx_stocks = fdr.StockListing('KRX')

    # 해당 stock_code의 주식 정보 찾기
    stock_info = krx_stocks[krx_stocks['Code'] == stock_code]

    if stock_info.empty:
        # 주식 코드가 KOSPI 목록에 없는 경우
        stock_data = {
            'code': stock_code,
            'name': 'Unknown',
            'price': 'N/A',
            'change': 'N/A',
            'change_percent': 'N/A',
            'volume': 'N/A',
        }
    else:
        # 주식 코드가 KOSPI 목록에 있는 경우
        stock_data = {
            'code': stock_code,
            'name': stock_info['Name'].values[0],
            'price': stock_info['Close'].values[0],
            'change': stock_info['Changes'].values[0],
            'change_percent': stock_info['ChagesRatio'].values[0],
            'volume': stock_info['Volume'].values[0],
        }

    comments = get_comments(stock_code)

    return render(request, 'stock/info.html', {
        'user_id': user_id,
        'stock': stock_data,
        'comments': comments,
    })


def chart_data(request, stock_code):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    df = fdr.DataReader(stock_code, start_date, end_date)

    data = {
        'labels': df.index.strftime('%Y-%m-%d').tolist(),
        'prices': df['Close'].tolist(),
    }
    return JsonResponse(data)


def search_stocks(request):
    query = request.GET.get('query', '').strip()
    if query:
        try:
            # KRX 주식 목록을 가져옵니다
            all_stocks = fdr.StockListing('KRX')

            # 주식 코드가 query로 시작하는 항목을 필터링합니다
            results = all_stocks[all_stocks['Code'].str.startswith(query)]


            # 결과를 리스트로 변환합니다 (최대 5개)
            stocks = [{'code': row['Code'], 'name': row['Name']}
                      for _, row in results.head(5).iterrows()]

            return JsonResponse({'stocks': stocks})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'stocks': []})


def stock_redirect(request):
    query = request.GET.get('query', '')
    krx_stocks = fdr.StockListing('KRX')

    # 정확한 종목코드 매치
    if query in krx_stocks['Code'].values:
        return redirect('info', stock_code=query)

    # 정확한 종목명 매치
    exact_match = krx_stocks[krx_stocks['Name'] == query]
    if not exact_match.empty:
        return redirect('info', stock_code=exact_match.iloc[0]['Code'])

    # 매치되는 결과가 없으면 검색 페이지에 쿼리와 함께 렌더링
    return render(request, 'stock/search_stocks.html', {'query': query})


def search_page(request):
    return render(request, 'stock/search_stocks.html')