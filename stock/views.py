from django.shortcuts import render
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
    kospi_stocks = fdr.StockListing('KOSPI')

    # 해당 stock_code의 주식 정보 찾기
    stock_info = kospi_stocks[kospi_stocks['Code'] == stock_code]

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