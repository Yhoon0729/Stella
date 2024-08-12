import os
from functools import lru_cache

import pandas as pd
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
import FinanceDataReader as fdr
from datetime import datetime, timedelta

from comments.views import get_comments


@lru_cache(maxsize=1)
def get_krx_listing():
    return fdr.StockListing('KRX')


def cached_data_reader(code, start_date, end_date):
    cache_key = f'stock_data_{code}_{start_date}_{end_date}'
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return pd.read_json(cached_data)

    data = fdr.DataReader(code, start_date, end_date)
    cache.set(cache_key, data.to_json(), timeout=60)  # 1분 동안 캐시
    return data

def index(request):
    # KRX 주식 목록 가져오기
    krx_stocks = get_krx_listing()

    # 상위 3개 종목 선택 (등락률 기준)
    top_3_ChagesRatio = krx_stocks.sort_values(by='ChagesRatio', ascending=False).head(3)

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


def stock_info(request, stock_code):
    user_id = request.session.get('user_id')
    krx_stocks = get_krx_listing()
    stock_info = krx_stocks[krx_stocks['Code'] == stock_code]
    theme_df = pd.read_excel('test/theme.xlsx')
    stock_info = stock_info.merge(theme_df[['Code', 'Theme']], on='Code', how='left')

    if stock_info.empty:
        stock_data = {
            'code': stock_code,
            'name': 'Unknown',
            'price': 'N/A',
            'change': 'N/A',
            'change_percent': 'N/A',
            'volume': 'N/A',
        }
    else:
        stock_data = {
            'code': stock_code,
            'name': stock_info['Name'].values[0],
            'theme': stock_info['Theme'].values[0],
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
    df = cached_data_reader(stock_code, start_date, end_date)
    data = {
        'labels': df.index.strftime('%Y-%m-%d').tolist(),
        'prices': df['Close'].tolist(),
    }
    return JsonResponse(data)


def search_stocks(request):
    query = request.GET.get('query', '').strip()
    if query:
        try:
            all_stocks = get_krx_listing()
            results = all_stocks[all_stocks['Code'].str.startswith(query)]
            stocks = [{'code': row['Code'], 'name': row['Name']}
                      for _, row in results.head(5).iterrows()]
            return JsonResponse({'stocks': stocks})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'stocks': []})


def stock_redirect(request):
    query = request.GET.get('query', '')
    krx_stocks = get_krx_listing()
    if query in krx_stocks['Code'].values:
        return redirect('info', stock_code=query)
    exact_match = krx_stocks[krx_stocks['Name'] == query]
    if not exact_match.empty:
        return redirect('info', stock_code=exact_match.iloc[0]['Code'])
    return render(request, 'stock/search_stocks.html', {'query': query})


def search_page(request):
    return render(request, 'stock/search_stocks.html')


def theme_stocks(request):
    if request.method != 'POST':
        krx_stocks = get_krx_listing()
        theme_df = pd.read_excel('test/theme.xlsx')
        krx_stocks = krx_stocks.merge(theme_df[['Code', 'Theme']], on='Code', how='left')
        krx_stocks = krx_stocks.dropna(subset=['Theme'])
        theme_avg_change = krx_stocks.groupby('Theme')['ChagesRatio'].mean().reset_index()
        theme_avg_change = theme_avg_change.sort_values('ChagesRatio', ascending=False)
        theme_leaders = krx_stocks.loc[krx_stocks.groupby('Theme')['ChagesRatio'].idxmax()]
        theme_result = theme_avg_change.merge(theme_leaders[['Theme', 'Name', 'Code', 'ChagesRatio']], on='Theme',
                                              suffixes=('_avg', '_leader'))
        theme_result = theme_result.sort_values('ChagesRatio_avg', ascending=False)
        theme_result_list = theme_result.to_dict('records')
        paginator = Paginator(theme_result_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, 'stock/theme_stocks.html', context)


def theme_detail(request, theme):
    krx_stocks = get_krx_listing()
    theme_file_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'theme.xlsx')
    theme_df = pd.read_excel(theme_file_path)
    krx_stocks = krx_stocks.merge(theme_df[['Code', 'Theme']], on='Code', how='left')
    theme_stocks = krx_stocks[krx_stocks['Theme'] == theme].sort_values('ChagesRatio', ascending=False)
    theme_stocks_list = theme_stocks.to_dict('records')
    paginator = Paginator(theme_stocks_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'theme': theme, 'page_obj': page_obj}
    return render(request, 'stock/theme_detail.html', context)