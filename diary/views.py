from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from  django.contrib import messages
from .models import Food
from .models import Menu
from .models import Photo
from .models import User
from setting.models import Diet,Weight
from django.db.models import Q
from .forms import MenuForm
from datetime import datetime
from django.urls import reverse
import torch
from django.http import JsonResponse
from PIL import Image
import io
import json
from django.utils import timezone
from decimal import Decimal
import numpy as np

# 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='diary/weights/detect.pt')

def recommendation(kcal_available):
    carbs = kcal_available.get('carbs')
    proteins = kcal_available.get('proteins')
    fats = kcal_available.get('fats')
    carbs = carbs / proteins
    fats = fats / proteins
    proteins = proteins / proteins
    print('추천!')
    print(carbs, proteins, fats)




    # 유사성 - 유클리디안 거리 계산법
    def euclidean_distance(point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))

    # U의 좌표
    u_coordinates = (carbs, fats)

    # 다른 개체들의 좌표 리스트
    food_list = Food.objects.all()
    other_objects=[]
    for food in food_list:
        carbs = float(food.food_carbs / food.food_proteins)
        fats = float(food.food_fats / food.food_proteins)
        other_objects.append((carbs,fats))
    # print('리스트 비율계산')
    # print(other_objects)

    # 각 개체와 U 사이의 유클리디안 거리 계산
    distances = [euclidean_distance(u_coordinates, obj) for obj in other_objects]

    # 거리가 가장 작은 개체 찾기
    # most_similar_object_index = distances.index(min(distances))
    # most_similar_object = other_objects[most_similar_object_index]
    # print(f"The most similar object has coordinates: {most_similar_object}")
    # most_similar_object = food_list[most_similar_object_index]
    # print(f"The most similar object has coordinates: {most_similar_object}")
    # print(most_similar_object.food_name)

    # 거리가 가장 작은 상위 3개 개체 찾기
    most_similar_objects_indices = sorted(range(len(distances)), key=lambda k: distances[k])[:3]
    # most_similar_objects = [other_objects[i] for i in most_similar_objects_indices]
    # print(f"The 3 most similar objects have coordinates: {most_similar_objects}")
    most_similar_objects = [food_list[i] for i in most_similar_objects_indices]
    # print(f"The 3 most similar objects have coordinates: {most_similar_objects}")
    # for object in most_similar_objects:
    #     print(object.food_name)




    return most_similar_objects

def get_menu_list(user_id,day):
    # 필요 - 음식 이미지 url,음식 이름, 식사종류(아점저간야), 시간, 칼로리, 탄수화물, 단백질, 지방
    menus = Menu.objects.filter(menu_date__date=day,menu_user=user_id).order_by('menu_date')
    menu_list = []
    for menu in menus:
        menu_instance = {}
        food = Food.objects.filter(food_id=menu.menu_food.food_id).first()

        if menu.menu_photo:
            foodimage = Photo.objects.filter(photo_id=menu.menu_photo.photo_id).first()
            foodimage = foodimage.photo_url
        else:
            foodimage = None

        foodname = food.food_name

        time = timezone.localtime(menu.menu_date)
        time = time.strftime('%H시 %M분')

        kcal = int(food.food_kcal * menu.menu_weight)

        carbs = int(food.food_carbs * menu.menu_weight)

        proteins = int(food.food_proteins * menu.menu_weight)

        fats = int(food.food_fats * menu.menu_weight)

        category = menu.menu_category
        if category=='1':
            category='아침'
        elif category =='2':
            category='점심'
        elif category =='3':
            category='저녁'
        elif category =='4':
            category='간식'
        elif category =='5':
            category='야식'

        menu_instance = {'foodimage':foodimage,'category':category,'foodname':foodname,'time':time,'kcal':kcal,'carbs':carbs,'proteins':proteins,'fats':fats}
        print(menu_instance)
        menu_list.append(menu_instance)

    return menu_list
def available_kcal(total,current):

    kcal = total.get('kcal') - current.get('kcal')
    carbs = total.get('carbs') - current.get('carbs')
    proteins = total.get('proteins') - current.get('proteins')
    fats = total.get('fats') - current.get('fats')

    available = {'kcal':kcal,'carbs':carbs,'proteins':proteins,'fats':fats}
    return available
def day_kcal_calc(menu_list):
    kcal = 0
    carbs = 0
    proteins = 0
    fats = 0

    for menu in menu_list:
        print(menu)
        kcal += menu.get('kcal')
        carbs += menu.get('carbs')
        proteins += menu.get('proteins')
        fats += menu.get('fats')
    kcal_result = {'kcal':kcal,'carbs':carbs,'proteins':proteins,'fats':fats}
    return kcal_result
def kcal_calc(user_id):
    diet_list = Diet.objects.filter(diet=user_id).first()
    weight_list = Weight.objects.filter(weight_user=user_id).order_by('-weight_recorded').first()
    height = float(diet_list.diet_user_height)
    weight = float(weight_list.weight_current)
    exercise = diet_list.diet_exercise
    # 하루 칼로리 섭취량 하루에 500칼로리 적게 먹는 것이 이상적
    bmr = ((weight*10) + (height*6.25) - 230)
    carbs = 0
    proteins = 0
    fats = 0

    if exercise=='1':
        bmr *= 1.2
    elif exercise=='2':
        bmr *= 1.375
    elif exercise=='3':
        bmr *= 1.55
    elif exercise=='4':
        bmr *= 1.725
    elif exercise=='5':
        bmr *= 1.9
    bmr -= 500
    bmr = int(bmr)

    # 하루 단백질 섭취량
    if exercise=='1':
        proteins = weight * 1.2
    elif exercise=='2':
        proteins = weight * 1.4
    elif exercise=='3':
        proteins = weight * 1.6
    elif exercise=='4':
        proteins = weight * 1.8
    elif exercise=='5':
        proteins = weight * 2.0


    proteins = int(proteins)

    # 하루 지방 섭취량
    fats = int(weight)

    # 하루 탄수화물 섭취량
    carbs = (bmr - (proteins*4) - (fats*9))/4
    carbs = int(carbs)
    print(height,weight)

    kcal_info = {'kcal':bmr,'carbs':carbs,'proteins':proteins,'fats':fats}

    return kcal_info

def analyze_image(request):
    if request.method == 'POST' and request.FILES['photo']:
        # 이미지 받기
        image = request.FILES['photo']
        image = Image.open(image)

        # 이미지 분석
        results = model(image)
        results = results.pandas().xyxy[0].to_json(orient="records")  # 결과를 JSON 형식으로 변환

        # 결과 반환
        # return JsonResponse({'result': results})
        return results

    return JsonResponse({'error': '제출된 이미지가 없습니다.'}, status=400)

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


    goal = User.objects.filter(id=request.user.id).first()
    if goal.goal_set == 0:
        messages.error(request, '목표설정이 되어있지 않습니다, 서비스 이용을 위해서 목표 설정을 해주세요')
        return redirect('setting:goal')
    
    # 데이터를 위한 날짜설정
    today = datetime.now().date().strftime('%Y-%m-%d')
    print(today)
    # 비교용 오늘 날짜
    date = datetime.now().date().strftime('%Y-%m-%d')
    print(date)

    if request.GET.get('today',''):
        today = request.GET.get('today','')
        # search_today = timezone.datetime(today)
    user_id = request.user.id
    user_instance = User.objects.get(id=user_id)

    if request.method=='POST':
        Weight.objects.create(weight_current=request.POST.get('today_weight',None), weight_recorded=timezone.now(), weight_user=user_instance)

    record = Weight.objects.filter(weight_user=request.user, weight_recorded__date=today).order_by(
        '-weight_recorded').first()

    if record:
        current_weight = record.weight_current
    else:
        current_weight = "기록 없음"

    body = {'current_weight': current_weight,
            'start_weight': Diet.objects.filter(diet=user_instance).first().diet_start_weight,
            'target_weight': Diet.objects.filter(diet=user_instance).first().diet_target_weight}

    menu_list = get_menu_list(user_id, today)
    print(menu_list)

    # menu_list = Menu.objects.filter(menu_date__date=today,menu_user=user_id).order_by('menu_date')
    # 이 메뉴리스트로 DB에서 불러와서 사진, 각종 정보들을 정확하게 다시 만들어서 보내주게 추가 작업 필요

    # 영양소 칼로리 계산
    kcal_info = kcal_calc(user_instance)
    # 하루 섭취한 영양소 칼로리 계산
    kcal_result = day_kcal_calc(menu_list)
    kcal_available = available_kcal(kcal_info,kcal_result)
    recommendation_list = recommendation(kcal_available)

    context = {'menu_list': menu_list, 'today': today,'date':date, 'body':body,'kcal_info':kcal_info,'kcal_result':kcal_result,'kcal_available':kcal_available,'recommendation_list':recommendation_list}



    return render(request, 'diary/main.html', context)


def search(request):
    print("실행")
    if request.session.get('photo_info', {}):
        photo_info = request.session.get('photo_info', {})
        photo_url = photo_info.get('photo_url')
        photo_id = photo_info.get('photo_id')
        new_photo = Photo()
        new_photo.photo_url = photo_url
        new_photo.photo_id = photo_id

        print(photo_url)
        print(photo_id)
        # 이미지 분석
        # image = "/media/"+ photo_url
        # image = "/media/images/apple_bU4ubn1.jpg"
        # image = Image.open(image)
        # results = model(image)
        # print(results)


        food_list = Food.objects.order_by('food_name')

        kw = request.GET.get('kw', '')

        if request.session.get('food_name', {}):
            food_name = request.session.get('food_name', {})
            if food_name=='sagwa':
                kw = '사과'
            del request.session['food_name']

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
        print("사진저장")
        photo_info = Photo()
        photo_info.photo_url = request.FILES['photo']
        photo_info.save()
        # AI 모델으로 음식 이름 빼와서 context에 추가해서 search에서 받을 수 있게 해줘야함
        # foodname
        # context = {'photo':photo_info}
        result = analyze_image(request)
        result = json.loads(result)
        # result가 리스트인 경우
        if isinstance(result, list):
            # 여기에서 적절한 처리를 수행하거나 원하는 값을 가져옵니다.
            if result:
                result = result[0].get('name', None)
            else:
                result = None
        else:
            # result가 리스트가 아닌 경우 그대로 사용합니다.
            result = result.get('name', None)
        print(result)
        request.session['photo_info'] = {'photo_url': str(photo_info.photo_url), 'photo_id': photo_info.photo_id}
        request.session['food_name'] = result

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

        try:
            if request.session['photo_info']:
                del request.session['photo_info']
        except KeyError:
            # 'photo_info' 키가 없는 경우 처리할 내용
            pass


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