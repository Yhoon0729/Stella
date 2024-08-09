from django.contrib import auth
from django.shortcuts import render, redirect

from users.models import User


# Create your views here.

def signup(request) :
    if 'user_id' in request.session:
        return redirect('index')

    if request.method != 'POST' :
        return render(request, "users/signup.html")
    else :
        user_id = request.POST['user_id']
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        user_password = request.POST['user_password']
        confirm_password = request.POST['confirm_password']
        gender = request.POST['gender']
        
        if User.objects.filter(user_id=user_id).exists():
            context = {"msg" : "이미 존재하는 아이디 이니다", "url" : "/users/signup"}
            return render(request, "alert.html", context)
        elif len(user_id) > 20 :
            context = {"msg" : "아이디는 20자 이내로 작성", "url" : "/users/signup"}
            return render(request, "alert.html", context)
        elif user_password != confirm_password :
            context = {"msg" : "비밀번호가 틀립니다", "url" : "/users/signup"}
            return render(request, "alert.html", context)
        else :
            user = User(
                user_id = user_id,
                user_name = user_name,
                user_email = user_email,
                user_password=user_password,
                gender = gender
            )

            user.save()
            context = {"msg" : f"{user_id}님의 회원가입을 환영합니다", "url" : "/users/signin"}
            return render(request, "alert.html", context)

def signin(request) :
    if request.method != 'POST' :
        return render(request, "users/signin.html")
    else :
        user_id = request.POST['user_id']
        user_password = request.POST['user_password']
        try :
            user = User.objects.get(user_id=user_id)
        except :
            context = {"msg" : "아이디를 확인하세요", "url" : "/users/signin"}
            return render(request, "alert.html", context)
        if user_password != user.user_password :
            context = {"msg" : "비밀번호를 확인하세요", "url" : "/users/signin"}
            return render(request, "alert.html", context)
        else :
            request.session['user_id'] = user.user_id
            request.session['user_name'] = user.user_name
            context = {"msg" : f"{user.user_name}님, 환영합니다!", "url" : "/"}
            return render(request, "alert.html", context)

def signout(request) :
    if 'user_id' not in request.session:
        return redirect('index')
    auth.logout(request)
    context = {"msg" : "ㅂㅇㅂㅇ", "url" : "/users/signin"}
    return render(request, "alert.html", context)

def userinfo(request) :
    if 'user_id' not in request.session:
        context = {"msg" : "로그인 하셔야 됩니다!!", "url" : "/users/signin"}
        return render(request, "alert.html", context)

    user = User.objects.get(user_id=request.session['user_id'])
    return render(request, 'users/userinfo.html', {'user': user})