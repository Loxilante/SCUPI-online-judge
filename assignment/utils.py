import os
import http.client
import json
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
from .models import Assignment, Problem, Submission, CodeAnswer
import re
from django.utils import timezone
import tempfile
from django.http import JsonResponse

def is_in_group(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            this_user = User.objects.get(username = request.session.get('username'))
            this_group = Group.objects.get(name = kwargs.get('coursename'))
            if not this_group in this_user.groups.all() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return func(self, request, *args, **kwargs)
        
    return wrapper

def is_teacher_or_administrator(func):
    def wrapper(self, request, *args, **kwargs):
        if request.session.get('role') != 'teacher' and request.session.get('role') != 'administrator':
            return Response(status=status.HTTP_403_FORBIDDEN)
        return func(self, request, *args, **kwargs)
        
    return wrapper