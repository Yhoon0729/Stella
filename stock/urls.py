from django.urls import path
from stock import views


urlpatterns = [
    path('info/<str:stock_code>/', views.stock_info, name='info'),
    path('api/<str:stock_code>/chart-data/', views.chart_data, name='chart_data'),
]