from django.shortcuts import render, redirect
from .forms import GoalForm, BodyForm
from django.utils import timezone
from .models import Diet, Weight
from users.models import User
from django.utils import timezone
from django.contrib import messages


# Create your views here.
def main(request):
    goal = User.objects.filter(id=request.user.id).first()
    if goal.goal_set == 0:
        messages.error(request, '목표설정이 되어있지 않습니다, 서비스 이용을 위해서 목표 설정을 해주세요')
        return redirect('setting:goal')
    return render(request, 'setting/main.html')


def body(request):
    # Weight 모델의 weight_user 필드에는 User 인스턴스를 할당해야 함. Foreign Key이기 때문
    user_id = request.user.id
    user_instance = User.objects.get(id=user_id)

    if request.method == 'POST':
        weight_current = request.POST.get('weight_current', None)
        diet_user_height = request.POST.get('diet_user_height', None)
        diet_exercise = request.POST.get('diet_exercise', None)

        Weight.objects.create(weight_current=weight_current, weight_recorded=timezone.now(), weight_user=user_instance)

        # Diet 모델 업데이트
        diet_instance = Diet.objects.filter(diet=user_instance).first()
        if diet_instance:
            diet_instance.diet_user_height = diet_user_height
            diet_instance.diet_exercise = diet_exercise
            diet_instance.save()

        return redirect('setting:main')

    form = BodyForm()
    body = {'weight_current': Weight.objects.filter(weight_user_id=user_instance).order_by(
        '-weight_recorded').first().weight_current,
            'diet_user_height': Diet.objects.filter(diet=user_instance).first().diet_user_height,
            'diet_exercise': Diet.objects.filter(diet=user_instance).first().diet_exercise}
    context = {'form': form, 'body': body}

    return render(request, 'setting/body.html', context)


def goal(request):
    # Weight 모델의 weight_user 필드에는 User 인스턴스를 할당해야 함. Foreign Key이기 때문
    user_id = request.user.id
    user_instance = User.objects.get(id=user_id)

    if request.method == 'POST':
        form_data = {
            'diet': request.user.id,
            'diet_start_weight': request.POST['diet_start_weight'],
            'diet_target_weight': request.POST['diet_target_weight'],
            'diet_exercise': request.POST['diet_exercise'],
            'diet_user_height': request.POST['diet_user_height'],
        }
        # 이미 존재하는 데이터인지 확인
        existing_diet = Diet.objects.filter(diet=request.user.id).first()

        if existing_diet:
            # 이미 데이터가 존재하는 경우, 해당 데이터를 업데이트
            form = GoalForm(form_data, instance=existing_diet)
        else:
            # 데이터가 존재하지 않는 경우, 새로운 데이터를 생성
            form = GoalForm(form_data)

        if form.is_valid():
            form.save()
            goal_settting = User.objects.filter(id=request.user.id).first()
            goal_settting.goal_set = 1
            goal_settting.save()
            return redirect('setting:main')
        else:
            print('폼에러')
            messages.error(request, '입력된 값이 없거나 범위를 벗어났습니다. 1000미만, 그리고 소수점 한자리까지 입력 가능합니다.')
            return redirect('setting:goal')

    form = GoalForm()
    goal = Diet.objects.filter(diet=user_instance).first()
    context = {'form': form, 'goal': goal}

    return render(request, 'setting/goal.html', context)


def myinfo(request):
    return render(request, 'setting/myinfo.html')


def withdrawal(request):
    return render(request, 'setting/withdrawal.html')
