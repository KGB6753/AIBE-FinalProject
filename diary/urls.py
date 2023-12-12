from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'diary'

urlpatterns = [
    # path('analyze-image/', views.analyze_image, name='analyze_image'),
    path('main/', views.main, name='main'),
    path('search/', views.search, name='search'),
    path('photo/', views.photo, name='photo'),
    path('meal/<int:food_id>/', views.meal, name='meal'),
    path('meal/detail/', views.detail, name='detail'),
    path('meal/delete/', views.delete, name='delete'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
