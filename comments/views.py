from django.shortcuts import redirect, render
from django.db import connection

def add_comment(request, stock_code):
    if request.method == 'POST' and not request.session.get('user_id'):
        context = {"msg":"로그인이 필요한 서비스 입니다.", "url":"signin"}
        return render(request, "alert.html", context)
    elif request.method == 'POST' and request.session.get('user_id'):
        content = request.POST.get('content')
        user_id = request.session.get('user_id')
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO comments (user_id, stock_code, content)
                VALUES (%s, %s, %s)
            """, [user_id, stock_code, content])
    return redirect('info', stock_code=stock_code)

def get_comments(stock_code):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, user_id, content, created_at
            FROM comments
            WHERE stock_code = %s
            ORDER BY created_at DESC
        """, [stock_code])
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]