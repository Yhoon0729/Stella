from django.urls import path
from comments import views

app_name = 'comments'

urlpatterns = [
    path('add/<str:stock_code>/', views.add_comment, name='add'),
]