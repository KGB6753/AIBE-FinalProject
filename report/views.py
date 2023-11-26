from django.shortcuts import render,redirect
from  django.contrib import messages
from users.models import User
# Create your views here.

def main(request):
    goal = User.objects.filter(id=request.user.id).first()
    if goal.goal_set == 0:
        messages.error(request, '목표설정이 되어있지 않습니다, 서비스 이용을 위해서 목표 설정을 해주세요')
        return redirect('setting:goal')

    return render(request, 'report/main.html')