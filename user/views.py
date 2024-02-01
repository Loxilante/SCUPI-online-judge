from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render, HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView  # 继承了ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from .utils import OrPermission
from course.models import Message


class LoginView(APIView):
    """
    API view for user login.

    This view allows users to authenticate and obtain access and refresh tokens.

    Methods:
    - post: Authenticates the user and returns access and refresh tokens.

    Attributes:
    - permission_classes: A list of permission classes applied to the view.
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        username = request.data.get('username')
        password = request.data.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        auth.login(request, user)
        request.session['username'] = username
        if user.groups.filter(name="administrator").exists():
            role = "administrator"
        elif user.groups.filter(name="teacher").exists():
            role = "teacher"
        else:
            role = "student"
        request.session['role'] = role
        refresh = RefreshToken.for_user(user)
        response = Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

        response.set_cookie('username', user.username)
        response.set_cookie('role', role)
        return response


class logoutView(APIView):
    """
    A view for logging out a user.

    Args:
        APIView: The base class for API views.

    Returns:
        Response: A response indicating the success of the logout operation.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        auth.logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_204_NO_CONTENT)


class TokenRefreshView(APIView):
    """
    View for refreshing access token using refresh token.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        return Response({
            'access': str(token.access_token),
        }, status=status.HTTP_200_OK)


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        fields = ['username', 'email', 'first_name']
        extra_kwargs = {
            'username': {'read_only': True},
            'first_name': {'read_only': True},
            'email': {'read_only': True},
        }


class UserView(APIView):
    """_summary_
    user operations, with different permissions
    """
    permission_classes = [IsAuthenticated]

    # 获取用户信息
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if username:
            user = User.objects.filter(username=username).first()

            if not user:
                return Response({"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST)
            if str(username) == str(this_user.username) or this_user.groups.filter(
                    name="teacher").exists() or this_user.groups.filter(name="administrator").exists():
                # 只有本人或者是老师或者是管理员才能查看;
                serializer = UserSerializers(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You don't have permission to view this user"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            if this_user.groups.filter(name="teacher").exists() or this_user.groups.filter(
                    name="administrator").exists():
                # 只有老师或者是管理员才能查看所有用户
                users = User.objects.all()
                serializer = UserSerializers(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You don't have permission to view user"}, status=status.HTTP_403_FORBIDDEN)

    # 修改用户密码
    def put(self, request, *args, **kwargs):  # 修改密码
        this_user = User.objects.filter(username=request.session.get('username')).first()
        username = kwargs.get('username')
        user = User.objects.filter(username=username).first()

        if str(username) == str(this_user.username) or this_user.groups.filter(name="administrator").exists():
            # 只有本人或者是管理员才能修改
            if not user:
                return Response({"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST)

            old_password = request.data.get("old_password")
            new_password = request.data.get("new_password")

            if not old_password or not new_password:
                return Response({"error": "Old password and new password are required."},
                                status=status.HTTP_400_BAD_REQUEST)

            if not check_password(old_password, user.password) and not this_user.groups.filter(
                    name="administrator").exists():
                # 管理员可以不用输入正确的旧密码
                return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            if not this_user.groups.filter(name="administrator").exists():
                # 管理员修改密码不需要重新登录
                auth.logout(request)

            return Response({"success": "Password updated successfully, now logout if you are not admin."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "You don't have permission to update this user"},
                            status=status.HTTP_403_FORBIDDEN)

    # 创建用户
    def post(self, request, *args, **kwargs):
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if this_user.groups.filter(name="administrator").exists():
            # 只有管理员可以创建用户
            try:
                user = User.objects.create_user(username=request.data.get('new_username'),
                                                password=request.data.get('new_user_password'),
                                                email=request.data.get('new_user_email'))
            except:
                return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
            user.first_name = request.data.get('new_user_first_name')
            user.save()
            if (request.data.get('new_user_group') == 'administrator'):
                administrator, created = Group.objects.get_or_create(name='administrator')
                administrator.user_set.add(user)
            elif (request.data.get('new_user_group') == 'teacher'):
                teacher, created = Group.objects.get_or_create(name='teacher')
                teacher.user_set.add(user)
            elif (request.data.get('new_user_group') == 'student'):
                student, created = Group.objects.get_or_create(name='student')
                student.user_set.add(user)

            return Response({"success": "User created successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You don't have permission to create user"}, status=status.HTTP_403_FORBIDDEN)

            # 删除用户

    def delete(self, request, *args, **kwargs):
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if this_user.groups.filter(name="administrator").exists():
            # 只有管理员可以删除用户
            try:
                user = User.objects.get(username=request.data.get('delete_username'))
            except User.DoesNotExist:
                return Response({"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST)

            user.delete()

            return Response({"success": "User deleted successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You don't have permission to delete user"}, status=status.HTTP_403_FORBIDDEN)


class MyNotifications(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        this_username = request.session.get('username')
        this_user = User.objects.filter(username=this_username).first()
        if request.get('messageid').exist():
            request['messageid'] = None
        if not this_username:
            return Response({"error": "You have not logged in,please login or create a new account"},
                            status=status.HTTP_403_FORBIDDEN)
        elif this_user.groups.filter(name="administrator").exists():
            return Response(Message.objects.all())
        else:
            message = []
            message.append(Message.objects.filter(reciever_group=this_user.groups.id))
            message.append(Message.objects.filter(sender=this_user.id))
            return Response(message)

    def post(self, request, *args, **kwargs):
        messageid = request.data.get('messageid')
        if messageid != None:
            return render(request, 'message/{}/.html'.format([messageid]), locals())
        if request.data.get('create') == True:
            return render(request, 'message/create/.html')


class EnterMessage(APIView):
    #包括阅读和删除
    def get(self, request, *args, **kwargs):
        messageid = request.data.get('messageid')
        this_message = Message.objects.get(id=messageid)
        this_message.is_read=True
        return Response(this_message)

    def post(self, request, *args, **kwargs):
        if kwargs.get('delete')==True:
            this_message = Message.objects.get(request.data.get('messageid'))
            this_message.delete()
        elif kwargs.get('return')==True:
            return render(request, 'notifications/.html')


class CreateMessage(APIView):

    def get(self, request, *args, **kwargs):
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if this_user.groups.filter(name='administrator').exist():
            return Response(this_user.groups.all())
        if this_user.groups.filter(name='teacher').exist():
            return Response(this_user.groups.exclude(name='teacher'))
        if this_user.groups.filter(name='student').exist():
            return Response('您未拥有送信的权限')

    def post(self, request, *args, **kwargs):
        Message.objects.create(sender=request.session.get('username'), receiver=kwargs.get('receive_group').user.all(),
                               level=kwargs.get('level'), title=kwargs.get('title'), content=kwargs.get('content'))
        return Response('发信成功')
