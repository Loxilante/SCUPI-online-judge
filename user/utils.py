from rest_framework.permissions import BasePermission
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status

class OrPermission(BasePermission):
    """
    如果给定的权限类中的任何一个返回 True，则返回 True。
    """
    def __init__(self, *permissions):
        self.permissions = [permission() for permission in permissions]

    def has_permission(self, request, view):
        return any(permission.has_permission(request, view) for permission in self.permissions)

    def has_object_permission(self, request, view, obj):
        return any(permission.has_object_permission(request, view, obj) for permission in self.permissions)




        
        
