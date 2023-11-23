from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from  django.contrib import messages
from .models import Food
from .models import Menu
from .models import Photo
from django.db.models import Q
from .forms import MenuForm
from datetime import datetime
from django.urls import reverse

# Create your views here.
def main(request):
    # today = datetime.now().strftime("%Y-%m-%d")
    # print(today)
    #
    # menu_list = Menu.objects.order_by('menu_date')
    # menu_list = menu_list.filter(
    #     Q(menu_date__icontains=today)
    # )
    # print(menu_list)
    # context = {'menu_list': menu_list,'today':today}
    # return render(request, 'diary/main.html', context)
    today = datetime.now().date()
    print(today)
    # today = "2023-11-22"
    menu_list = Menu.objects.filter(menu_date__date=today).order_by('menu_date')
    context = {'menu_list': menu_list, 'today': today}
    return render(request, 'diary/main.html', context)


def search(request):
    print("실행")
    if request.session.get('photo_info', {}):
        photo_info = request.session.get('photo_info', {})
        photo_url = photo_info.get('photo_url')
        photo_id = photo_info.get('photo_id')
        del request.session['photo_info']
        new_photo = Photo()
        new_photo.photo_url = photo_url
        new_photo.photo_id = photo_id

        print(photo_url)
        print(photo_id)
        food_list = Food.objects.order_by('food_name')
        kw = request.GET.get('kw', '')
        # if request.GET.get('foodname','')
        #     kw = request.GET.get('foodname','')

        if kw:
            food_list = food_list.filter(
                Q(food_name__icontains=kw)
            ).distinct()
        # context = {'food_list': food_list, 'photo': {'photo_id': photo_id, 'photo_url': photo_url}}
        context = {'food_list': food_list, 'photo': new_photo}
        return render(request,'diary/search.html',context)
    else:
        food_list = Food.objects.order_by('food_name')
        kw = request.GET.get('kw', '')
        # if request.GET.get('foodname','')
        #     kw = request.GET.get('foodname', '')
        if kw:
            food_list = food_list.filter(
                Q(food_name__icontains=kw)
            ).distinct()
        # context = {'food_list': food_list, 'photo': {'photo_id': photo_id, 'photo_url': photo_url}}
        context = {'food_list': food_list}
        return render(request, 'diary/search.html', context)

# def photo(request):
#     if request.method == 'POST':
#         photo_info = Photo()
#         photo_info.photo_url = request.FILES['photo']
#         photo_info.save()
#         # AI 모델으로 음식 이름 빼와서 context에 추가해서 search에서 받을 수 있게 해줘야함
#         # foodname
#         context = {'photo':photo_info}
#
#         return render(request, 'diary/search.html', context)
#
#
#     return render(request,'diary/photo.html')

def photo(request):
    if request.method == 'POST':
        photo_info = Photo()
        photo_info.photo_url = request.FILES['photo']
        photo_info.save()
        # AI 모델으로 음식 이름 빼와서 context에 추가해서 search에서 받을 수 있게 해줘야함
        # foodname
        # context = {'photo':photo_info}
        request.session['photo_info'] = {'photo_url': str(photo_info.photo_url), 'photo_id': photo_info.photo_id}

        return redirect('diary:search')


    return render(request,'diary/photo.html')
def meal(request, food_id):

    food = Food.objects.get(food_id = food_id)
    photo_id = request.GET.get('photo_id', None)

    if photo_id:
        # photo_id가 있을 경우 Photo 객체를 가져옴
        photo_list = get_object_or_404(Photo, pk=photo_id)
    else:
        # photo_id가 없을 경우 기본값으로 설정하거나 다른 로직 수행
        photo_list = None

    context={'food':food,'photo':photo_list}
    form = MenuForm()

    photo_list = Photo.objects

    if request.method == 'POST':

        form_data = {
            'menu_weight': request.POST['menu_weight'],
            'menu_date': request.POST['menu_date'],
            'menu_category': request.POST['menu_category'],
            'menu_food': request.POST['menu_food_id'],
            'menu_photo': request.POST['menu_photo_id'],
            'menu_user': request.user.id,
        }

        form = MenuForm(form_data)
        print(form.errors)
        if form.is_valid():

            # 폼이 유효한 경우, 데이터를 저장하거나 다른 작업을 수행할 수 있습니다.
            form.save()
            # return redirect('success_page')  # 저장이 성공했을 때 이동할 페이지로 리다이렉트
            return redirect('diary:main')

        else:
            print("error")

    # if request.method == 'POST':
    #     form = MenuForm(request.POST)
    #     if form.is_valid():
    #         # 폼이 유효하면 필요한 작업을 수행
    #         image = request.POST.get('image')
    #         # 다른 처리 로직을 여기에 추가
    #         context = {'food': food, 'image': image}
    #         return render(request, 'diary/meal.html', context)
    context['form'] = form
    return render(request,'diary/meal.html',context)



