from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import UserForm
from .models import User
from  django.contrib import messages



def signup(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)  # 사용자 인증
            # login(request, user)  # 로그인
            return redirect('users:signupOK')
            # return render(request, 'users/signupOK.html')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('diary:main')


    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']
        try:
            # USER 정보 확인
            user = User.objects.get(email=email)
        except:
            messages.error(request, '회원정보를 찾을 수 없습니다.')

        user = authenticate(request,email=email,password=password)

        if user is not None:
            messages.success(request,'로그인 되었습니다.')
            login(request,user)
            # return redirect('users:loginOK')
            goal = User.objects.filter(id=request.user.id).first()
            if goal.goal_set==0:
                messages.error(request, '목표설정이 되어있지 않습니다, 서비스 이용을 위해서 목표 설정을 해주세요')
                return redirect('setting:goal')
            return redirect('diary:main')
            # return render(request, 'users/main.html')
        else:
            messages.error(request,'아이디 혹은 비밀번호가 틀렸습니다.')

    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    messages.success(request,'로그아웃 되었습니다')
    # return render(request, 'users/login.html')
    return redirect('users:login')

def signupOK(request):
    return render(request, 'users/signupOK.html')

def loginOK(request):
    return render(request, 'users/main.html')
