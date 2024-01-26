#from typing import AbstractSet
from django.db import models

# #创建一些新的permission
# class NewPermission(models.Model):
    
#         class Meta:
#             permissions = [
#                 ('view_all','Can view all information'),
#             ]
#             #自定义了一个auth_permission 暂时不会用到auth的permission功能
#             #因为用户分类简单，直接判断群组就可以了，不用使用复杂的permission