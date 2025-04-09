# myapp/urls.py
from django.urls import path
from .views import chatgpt  # 导入你的视图函数

urlpatterns = [
    path('', chatgpt.as_view(), name='chatgpt'),  # 配置 'chatgpt/' 路由
]
