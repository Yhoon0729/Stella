from django.shortcuts import redirect, render
from .models import Comment

def add_comment(request, stock_code):
    if request.method == 'POST' and not request.session.get('user_id'):
        context = {"msg":"로그인이 필요한 서비스 입니다.", "url":"signin"}
        return render(request, "alert.html", context)
    elif request.method == 'POST' and request.session.get('user_id'):
        content = request.POST.get('content')
        user_id = request.session.get('user_id')
        Comment.objects.create(user_id=user_id, stock_code=stock_code, content=content)
    return redirect('info', stock_code=stock_code)

def get_comments(stock_code):
    return Comment.objects.filter(stock_code=stock_code).values('id', 'user_id', 'content', 'created_at')