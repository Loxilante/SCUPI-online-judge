from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.shortcuts import render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView #继承了ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet,ViewSet,ModelViewSet
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

class CourseSerializer(serializers.Serializer):
    course_name = serializers.CharField(required = True, max_length=100)
    students_list = serializers.ListField(child = serializers.CharField(max_length = 20))
    
class CourseView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if this_user.groups.filter(name="administrator").exists():
            #只有管理员能创建班级
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                course = serializer.validated_data
                course_name = course['course_name']
                students_list = course['students_list']
                
                if course_name == 'teacher' or course_name == 'student' or course_name == 'administrator':
                    return Response({"error": "Invalid course name"}, status=status.HTTP_400_BAD_REQUEST)
                new_course, created = Group.objects.get_or_create(name=course_name)
                for student in students_list:
                    new_student = User.objects.filter(username=student).first()
                    if new_student is not None:
                        new_course.user_set.add(new_student)
                    else:
                        new_course.delete()
                        return Response({"error": "fail to create this course"}, status=status.HTTP_400_BAD_REQUEST)  
                        
                return Response({"success": "Course created successfully"}, status=status.HTTP_200_OK)
                
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
        else:
            return Response({"error": "You don't have permission to create course"}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, *args, **kwargs):
        this_user = User.objects.filter(username=request.session.get('username')).first()        
        if this_user.groups.filter(name="administrator").exists():
            #只有管理员可以删除课程
            course_name = request.data.get('course_name')
            if course_name is not None and course_name != 'teacher' and course_name != 'student' and course_name != 'administrator':
                try:   
                    course = Group.objects.get(name=course_name)
                    course.delete()
                    return HttpResponse({"success": "Group deleted successfully"}, status=status.HTTP_400_BAD_REQUEST)
                except Group.DoesNotExist:
                    return HttpResponse({"error": "Group not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"error": "course name error"}, status=status.HTTP_400_BAD_REQUEST)     
                       
        else:
            return Response({"error": "You don't have permission to delete course"}, status=status.HTTP_403_FORBIDDEN)    
           
    