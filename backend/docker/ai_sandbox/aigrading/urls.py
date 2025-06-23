# myapp/urls.py
from django.urls import path
from .views import AiGrading

urlpatterns = [
    path('', AiGrading.as_view(), name='aigrading'),  # 配置 'aigrading/' 路由
]
