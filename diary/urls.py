from django.urls import path
from django.contrib.auth import views as auth_views
# from .forms import CustomAuthenticationForm
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name='diary'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('search/', views.search, name='search'),
    path('photo/', views.photo, name='photo'),
    path('meal/<int:food_id>/',views.meal,name='meal'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)