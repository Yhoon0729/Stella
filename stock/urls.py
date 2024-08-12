from django.urls import path
from stock import views


urlpatterns = [
    path('info/<str:stock_code>/', views.stock_info, name='info'),
    path('api/<str:stock_code>/chart-data/', views.chart_data, name='chart_data'),
    path("search_page/", views.search_page, name='search_page'),
    path("search_stocks/", views.search_stocks, name='search_stocks'),
    path('redirect/', views.stock_redirect, name='stock_redirect'),

]