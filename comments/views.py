from django.shortcuts import redirect, render
from .models import Comment
from django.contrib import messages


def add_comment(request, stock_code):
    if request.method == 'POST':
        if not request.session.get('user_id'):
            messages.error(request, "로그인이 필요한 서비스입니다.")
            return redirect('signin')

        content = request.POST.get('content')
        user_id = request.session.get('user_id')

        Comment.objects.create(
            user_id=user_id,
            stock_code=stock_code,
            content=content
        )
    return redirect('info', stock_code=stock_code)


def get_comments(stock_code):
    return Comment.objects.filter(stock_code=stock_code).order_by('-created_at').values(
        'id', 'user_id', 'content', 'created_at'
    )