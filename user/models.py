#from typing import AbstractSet
from django.db import models

# 定义用户角色和性别的选择
# class UserRole(models.TextChoices):
#     ADMINISTRATOR = 'administrator'
#     TEACHER = 'teacher'
#     STUDENT = 'student'

# 用户模型
# class UserInfo(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=60)
#     role = models.CharField(max_length=50, choices=UserRole.choices)
#     email = models.EmailField(unique=True, max_length=100)
#     password_hash = models.CharField(max_length=256)

 #课程模型
# class Course(models.Model):
#     course_id = models.AutoField(primary_key=True)
#     course_name = models.CharField(max_length=64)
#     # 其他字段...

# # 用户课程关系模型
# class UserCourse(models.Model):
#     user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('user', 'course')