import random
import string

from django.contrib import auth, messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from users.models import User

'''
def generate_verification_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def send_verification_email(email, code):
    subject = 'Stella - 인증 코드'
    message = f'귀하의 인증 코드는 {code}입니다.'
    from_email = 'vfdgy0729@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
'''

def signup(request) :
    if 'user_id' in request.session:
        context = {"msg": "로그아웃 하셔야 됩니다!!", "url": "/"}
        return render(request, "alert.html", context)

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
            context = {"msg" : "이미 존재하는 아이디 입니다", "url" : "/users/signup"}
            return render(request, "alert.html", context)
        elif len(user_id) > 20 :
            context = {"msg" : "아이디는 20자 이내로 작성", "url" : "/users/signup"}
            return render(request, "alert.html", context)
        elif User.objects.filter(user_email=user_email).exists():
            context = {"msg" : "이미 사용중인 이메일 입니다.", "url" : "/users/signup"}
            return render(request, "alert.html", context)
        elif user_password != confirm_password :
            context = {"msg" : "비밀번호가 틀립니다", "url" : "/users/signup"}
            return render(request, "alert.html", context)
        else:
            user = User(
                user_id=user_id,
                user_name=user_name,
                user_email=user_email,
                user_password=user_password,
                gender=gender
            )
            user.save()

            context = {"msg": f"{user.user_id}님의 회원가입을 환영합니다", "url": "/users/signin"}
            return render(request, "alert.html", context)

            '''
            # 이메일 인증 코드 생성 및 전송
            verification_code = generate_verification_code()
            send_verification_email(user_email, verification_code)

            # 세션에 사용자 정보 임시 저장
            request.session['temp_user_data'] = {
                'user_id': user_id,
                'user_name': user_name,
                'user_email': user_email,
                'user_password': user_password,
                'gender': gender,
                'verification_code': verification_code
            }

            context = {
                "msg" : "입력하신 이메일로 인증번호를 보냈습니다.",
                "url" : "/users/verify_email"
            }
            return render(request, "alert.html", context)
            '''


'''
def verify_email(request):
    if 'temp_user_data' not in request.session:
        return redirect('signup')

    if request.method != 'POST':
        return render(request, "users/verify_email.html")
    else :
        entered_code = request.POST.get('verification_code')
        temp_user_data = request.session['temp_user_data']

        if entered_code == temp_user_data['verification_code']:
            # 인증 성공, 사용자 생성
            user = User(
                user_id=temp_user_data['user_id'],
                user_name=temp_user_data['user_name'],
                user_email=temp_user_data['user_email'],
                user_password=temp_user_data['user_password'],
                gender=temp_user_data['gender']
            )
            user.save()

            del request.session['temp_user_data']

            context = {"msg": f"{user.user_id}님의 회원가입을 환영합니다", "url": "/users/signin"}
            return render(request, "alert.html", context)
        else:
            context = {"msg": "인증 코드가 올바르지 않습니다", "url": "/users/verify_email"}
            return render(request, "alert.html", context)
'''

def signin(request) :
    if 'user_id' in request.session:
        return redirect('index')

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
    context = {"msg" : "로그아웃 되었습니다.", "url" : "/users/signin"}
    return render(request, "alert.html", context)

def userinfo(request) :
    if 'user_id' not in request.session:
        context = {"msg" : "로그인 하셔야 됩니다!!", "url" : "/users/signin"}
        return render(request, "alert.html", context)

    user = User.objects.get(user_id=request.session['user_id'])
    return render(request, 'users/userinfo.html', {'user': user})

def userupdate(request) :
    if 'user_id' not in request.session:
        return redirect('index')

    user = User.objects.get(user_id=request.session['user_id'])

    if request.method != 'POST' :
        context = {"user" : user}
        return render(request, "users/userupdate.html", context)
    else :
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        gender = request.POST.get('gender')

        # 간단한 서버 측 유효성 검사
        if not user_name or not user_email:
            context = {"msg" : "모두 입력해 주세요", "url" : "/users/userupdate", "user" : user}
            return render(request, 'alert.html', context)

        # 사용자 정보 업데이트
        user.user_name = user_name
        user.user_email = user_email
        user.gender = gender
        user.save()

        context = {"msg" : "회원 정보가성공적으로 수정되었습니다", "url" : "/users/userinfo", "user" : user}
        return render(request, 'alert.html', context)

def passupdate(request) :
    if 'user_id' not in request.session:
        return redirect('index')


    user = User.objects.get(user_id=request.session['user_id'])

    if request.method != 'POST' :
        context = {"user" : user}
        return render(request, "users/passupdate.html", context)
    else :
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # 서버 측 유효성 검사
        if not current_password or not new_password or not confirm_password:
            context = {"msg" : "모든 항목을 입력해주세요", "url" : "/users/passupdate"}
            return render(request, 'alert.html', context)

        if new_password != confirm_password:
            context = {"msg" : "새 비밀번호 학인이 틀렸습니다", "url" : "/users/passupdate"}
            return render(request, 'alert.html', context)

        # 현재 비밀번호 확인
        if current_password != user.user_password:  # 주의: 실제 환경에서는 반드시 해시된 비밀번호를 사용해야 함.
            context = {"msg" : "비밀번호를 잘못 입력하였습니다", "url" : "/users/passupdate"}
            return render(request, 'alert.html', context)

        # 비밀번호 변경
        user.user_password = new_password
        user.save()
        auth.logout(request)
        context = {"msg" : "비밀번호가 변경되었습니다", "url" : "/users/signin"}
        return render(request, 'alert.html', context)

def userdelete(request) :
    if 'user_id' not in request.session:
        return redirect('index')

    user = User.objects.get(user_id=request.session['user_id'])
    user_name = user.user_name

    if request.method != 'POST' :
        context = {"user" : user}
        return render(request, "users/userdelete.html", context)
    else :
        password = request.POST.get('password')

        if user.user_password != password:
            context = {"msg" : "비밀번호를 잘못 입력하였습니다.", "url" : "/users/userdelete"}
            return render(request, 'alert.html', context)

        elif user.user_password == password:
            # 사용자 삭제
            user.delete()

            # 세션 삭제
            request.session.flush()

            context = {"msg" : f"{user_name}님의 탈퇴가 완료되었습니다.", "url":"/users/signin"}
            return render(request, 'alert.html', context)

def finduserid(request) :
    if 'user_id' in request.session:
        return redirect('index')

    if request.method != 'POST' :
        return render(request, "users/finduserid.html")
    else :
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')

    if not user_name or not user_email:
        context = {"msg": "아이디와 이메일을 모두 입력해주세요.", "url": "/users/finduserid"}
        return render(request, 'alert.html', context)

    try:
        user = User.objects.get(user_name=user_name, user_email=user_email)
    except User.DoesNotExist:
        context = {"msg": "입력한 정보와 일치하는 사용자가 없습니다.", "url": "/users/finduserid"}
        return render(request, 'alert.html', context)
    else :
        context = {
            "user_id" : user.user_id,
        }
        return render(request, 'users/showuserid.html', context)

def findpassword(request):
    if 'user_id' in request.session:
        return redirect('index')

    if request.method != 'POST':
        return render(request, "users/findpassword.html")
    else:
        user_id = request.POST.get('user_id')
        user_email = request.POST.get('user_email')

        if not user_id or not user_email:
            context = {"msg": "아이디와 이메일을 모두 입력해주세요.", "url": "/users/findpassword"}
            return render(request, 'alert.html', context)

        try:
            user = User.objects.get(user_id=user_id, user_email=user_email)
        except User.DoesNotExist:
            context = {"msg": "입력한 정보와 일치하는 사용자가 없습니다.", "url": "/users/findpassword"}
            return render(request, 'alert.html', context)

        request.session['reset_email'] = user_email
        request.session['reset_user_id'] = user_id
        return redirect('resetpassword')

'''
def verify_code(request):
    if 'user_id' in request.session:
        return redirect('index')

    if 'reset_email' not in request.session:
        context = {"msg":"이메일 인증을 다시 시작해주세요", "url" : "/users/findpassword"}
        return render(request, 'alert.html', context)

    if request.method != 'POST' :
        return render(request, "users/verify_code.html")
    else :
        code = request.POST.get('code')
        email = request.session.get('reset_email')
        if not email:
            context = {"msg" : "이메일 인증을 다시하세요", "url" : "/users/findpassword"}
            return render(request, 'alert.html', context)
        try:
            user = User.objects.get(user_email=email, reset_password_token=code)
            request.session['user_email'] = user.user_email
            return redirect('resetpassword')
        except User.DoesNotExist:
            context = {"msg" : "인증 코드가 올바르지 않습니다", "url" : "/users/verify_code"}
            return render(request, 'alert.html', context)
'''


def resetpassword(request):
    if 'user_id' in request.session:
        return redirect('index')

    email = request.session.get('reset_email')

    if request.method != 'POST' :
        return render(request, "users/resetpassword.html")
    else :
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, "비밀번호가 일치하지 않습니다")
        else:
            user = User.objects.get(user_email=email)
            user.user_password = new_password
            user.reset_password_token = None
            user.save()
            del request.session['reset_email']
            context = {"msg":"비밀번호가 성공적으로 변경되었습니다", "url":"/users/signin"}
            return render(request, 'alert.html', context)
