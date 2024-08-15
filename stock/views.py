import base64
import io
import json
import os
import time
from functools import lru_cache

import seaborn as sns
import pandas as pd
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
import FinanceDataReader as fdr
from datetime import datetime, timedelta

import matplotlib
matplotlib.use('Agg') # 이 설정은 Tkinter 대신 non-interactive한 Agg 백엔드를 사용하도록 함
from matplotlib import pyplot as plt

from pykrx import stock

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

    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)

    # KOSPI와 KOSDAQ 지수 최신 데이터 가져오기
    latest_kospi_data = fdr.DataReader('KS11', start_date, end_date)
    latest_kosdaq_data = fdr.DataReader('KQ11', start_date, end_date)

    kospi_data = {
        'current': latest_kospi_data.iloc[-1]['Close'],
        'comp': latest_kospi_data.iloc[-1]['Comp'],
        'change': (latest_kospi_data.iloc[-1]['Change']) * 100
    }

    kosdaq_data = {
        'current': latest_kosdaq_data.iloc[-1]['Close'],
        'comp': latest_kosdaq_data.iloc[-1]['Comp'],
        'change': (latest_kosdaq_data.iloc[-1]['Change']) * 100
    }

    context = {
        'top_3_stocks' : top_3_stocks,
        'kospi': kospi_data,
        'kosdaq': kosdaq_data
    }
    return render(request, 'index.html', context)

def market_list(request, market):
    # 캐시된 KRX 리스팅 가져오기
    krx_stocks = get_krx_listing()

    if market == 'KOSPI':
        stocks = krx_stocks[krx_stocks['Market'] == 'KOSPI']
    elif market == 'KOSDAQ':
        stocks = krx_stocks[krx_stocks['Market'] == 'KOSDAQ']
    else:
        stocks = []  # 잘못된 시장 이름이 주어진 경우

    # 페이지네이션
    paginator = Paginator(stocks.to_dict('records'), 20)  # 한 페이지에 20개 종목
    pageNum = request.GET.get('page', '1')
    page_obj = paginator.get_page(pageNum)

    # 페이지네이션 관련 변수 계산
    totalcount = len(stocks)
    bottomLine = 5  # 한 페이지 그룹에 표시할 페이지 수
    currentPage = int(pageNum)
    startpage = (currentPage - 1) // bottomLine * bottomLine + 1
    endpage = startpage + bottomLine - 1
    maxpage = paginator.num_pages
    pagelist = range(startpage, min(endpage, maxpage) + 1)

    context = {
        'market': market,
        'page_obj': page_obj,
        'totalcount': totalcount,
        'pageNum': currentPage,
        'startpage': startpage,
        'endpage': endpage,
        'bottomLine': bottomLine,
        'maxpage': maxpage,
        'pagelist': pagelist,
    }

    return render(request, 'stock/market_list.html', context)

def stock_info(request, stock_code):
    user_id = request.session.get('user_id')
    krx_stocks = get_krx_listing()
    stock_info = krx_stocks[krx_stocks['Code'] == stock_code]
    theme_df = pd.read_excel('test/theme.xlsx')

    # 'Code' 열을 문자열로 변환
    # theme.xlsx에 새로 상장된 주식을 넣으면 datatype이 달라져서
    stock_info['Code'] = stock_info['Code'].astype(str)
    theme_df['Code'] = theme_df['Code'].astype(str)
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
        marcap = stock_info['Marcap'].values[0]
        marcap_in_won = marcap / 1e8  # 시가총액을 억 단위로 변환

        volume = stock_info['Volume'].values[0]
        formatted_volume = f"{volume:,}"  # 천 단위 구분 기호 포함

        stock_data = {
            'code': stock_code,
            'name': stock_info['Name'].values[0],
            'market' : stock_info['Market'].values[0],
            'theme': stock_info['Theme'].values[0],
            'price': stock_info['Close'].values[0],
            'change': stock_info['Changes'].values[0],
            'change_percent': stock_info['ChagesRatio'].values[0],
            'volume': formatted_volume,
            'marcap': f"{marcap_in_won:,.0f}억",
        }

        # 날짜 가져오기
        start_date = request.GET.get('start_date', (datetime.today() - timedelta(days=7)).strftime("%Y%m%d"))
        end_date = request.GET.get('end_date', datetime.today().strftime("%Y%m%d"))

        try:
            # 일중 데이터 가져오기
            df = stock.get_market_ohlcv(start_date, end_date, stock_code)
            time.sleep(1)

            # 주말 제외
            df = df[df.index.dayofweek < 5]

            # 그래프 생성
            plt.figure(figsize=(12, 6))
            sns.set(style="darkgrid")  # set_style 대신 set 사용
            sns.lineplot(x=df.index.strftime('%Y-%m-%d'), y=df['종가'])
            plt.title(f"{stock_data['name']} ({stock_code}) 주가 추이")
            plt.xlabel("날짜")
            plt.ylabel("종가 (원)")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # 그래프를 이미지로 저장
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()

            # 이미지를 base64로 인코딩
            graphic = base64.b64encode(image_png).decode('utf-8')

            # 컨텍스트에 그래프 데이터 추가
            stock_data['graph'] = graphic

        except Exception as e:
            print(f"그래프 생성 중 오류 발생: {e}")
            stock_data['graph'] = None
        finally:
            plt.close()  # 항상 figure를 닫아주세요

    comments = get_comments(stock_code)
    context = {
        'user_id': user_id,
        'stock': stock_data,
        'comments': comments,
    }

    return render(request, 'stock/info.html', context)

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
            results = all_stocks[
                (all_stocks['Code'].str.startswith(query)) |
                (all_stocks['Name'].str.contains(query, case=False, na=False))
            ]
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

        # 'Code' 열을 문자열로 변환
        krx_stocks['Code'] = krx_stocks['Code'].astype(str)
        theme_df['Code'] = theme_df['Code'].astype(str)

        krx_stocks = krx_stocks.merge(theme_df[['Code', 'Theme']], on='Code', how='left')
        krx_stocks = krx_stocks.dropna(subset=['Theme'])
        theme_avg_change = krx_stocks.groupby('Theme')['ChagesRatio'].mean().reset_index()
        theme_avg_change = theme_avg_change.sort_values('ChagesRatio', ascending=False)
        theme_leaders = krx_stocks.loc[krx_stocks.groupby('Theme')['ChagesRatio'].idxmax()]
        theme_result = theme_avg_change.merge(theme_leaders[['Theme', 'Name', 'Code', 'ChagesRatio']], on='Theme',
                                              suffixes=('_avg', '_leader'))
        theme_result = theme_result.sort_values('ChagesRatio_avg', ascending=False)
        theme_result_list = theme_result.to_dict('records')

        # 페이지네이션
        paginator = Paginator(theme_result_list, 10)  # 한 페이지에 10개 항목
        pageNum = request.GET.get('page', '1')
        page_obj = paginator.get_page(pageNum)

        # 페이지네이션 관련 변수 계산
        totalcount = len(theme_result_list)
        bottomLine = 5  # 한 페이지 그룹에 표시할 페이지 수
        currentPage = int(pageNum)
        startpage = (currentPage - 1) // bottomLine * bottomLine + 1
        endpage = startpage + bottomLine - 1
        maxpage = paginator.num_pages
        pagelist = range(startpage, min(endpage, maxpage) + 1)

        context = {
            'page_obj': page_obj,
            'totalcount': totalcount,
            'pageNum': currentPage,
            'startpage': startpage,
            'endpage': endpage,
            'bottomLine': bottomLine,
            'maxpage': maxpage,
            'pagelist': pagelist,
        }

        return render(request, 'stock/theme_stocks.html', context)


def theme_detail(request, theme):
    krx_stocks = get_krx_listing()
    theme_file_path = os.path.join(settings.BASE_DIR, 'static', 'data', 'theme.xlsx')
    theme_df = pd.read_excel(theme_file_path)

    # 'Code' 열을 문자열로 변환
    krx_stocks['Code'] = krx_stocks['Code'].astype(str)
    theme_df['Code'] = theme_df['Code'].astype(str)

    krx_stocks = krx_stocks.merge(theme_df[['Code', 'Theme']], on='Code', how='left')
    theme_stocks = krx_stocks[krx_stocks['Theme'] == theme].sort_values('ChagesRatio', ascending=False)
    theme_stocks_list = theme_stocks.to_dict('records')

    # 페이지네이션
    paginator = Paginator(theme_stocks_list, 10)  # 한 페이지에 10개 항목
    pageNum = request.GET.get('page', '1')
    page_obj = paginator.get_page(pageNum)

    # 페이지네이션 관련 변수 계산
    totalcount = len(theme_stocks_list)
    bottomLine = 5  # 한 페이지 그룹에 표시할 페이지 수
    currentPage = int(pageNum)
    startpage = (currentPage - 1) // bottomLine * bottomLine + 1
    endpage = startpage + bottomLine - 1
    maxpage = paginator.num_pages
    pagelist = range(startpage, min(endpage, maxpage) + 1)

    context = {
        'theme': theme,
        'page_obj': page_obj,
        'totalcount': totalcount,
        'pageNum': currentPage,
        'startpage': startpage,
        'endpage': endpage,
        'bottomLine': bottomLine,
        'maxpage': maxpage,
        'pagelist': pagelist,
    }

    return render(request, 'stock/theme_detail.html', context)