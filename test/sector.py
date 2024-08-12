import os

import pandas as pd
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
import FinanceDataReader as fdr
from datetime import datetime, timedelta

from comments.views import get_comments

def theme_stocks(request):
    if request.method != 'POST':
        krx_stocks = fdr.StockListing('KRX')

        # Theme를 fdr에 merge
        theme_df = pd.read_excel('test/theme.xlsx')

        krx_stocks = krx_stocks.merge(theme_df[['Code', 'Theme']], on='Code', how='left')

        # NaN 값을 가진 행 제거
        krx_stocks = krx_stocks.dropna(subset=['Theme'])

        # 테마별 평균 등락률 계산
        theme_avg_change = krx_stocks.groupby('Theme')['ChagesRatio'].mean().reset_index()
        theme_avg_change = theme_avg_change.sort_values('ChagesRatio', ascending=False)

        # DataFrame을 딕셔너리 리스트로 변환
        theme_avg_change_list = theme_avg_change.to_dict('records')

        # 페이지네이션
        paginator = Paginator(theme_avg_change_list, 10)  # 10개씩 페이지 나누기
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {'page_obj': page_obj}
        return render(request, 'stock/theme_stocks.html', context)