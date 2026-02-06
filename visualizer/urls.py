# visualizer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.creator, name='creator'),               # 原来的页面
    path('api/check/', views.check_tileset, name='check_api'), # API 接口
]