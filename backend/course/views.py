from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .models import Message, MessageRead

"""班级系统
    班级系统分为班级的增删改查，增删改为administrator权限，查根据角色不同可以得到的信息不同
"""
class CourseSerializer(serializers.Serializer):
    course_name = serializers.CharField(required=True, max_length=100)
    students_list = serializers.ListField(child=serializers.CharField(max_length=20))


# 序列化器还有预留位
class GroupSerializer(serializers.Serializer):
    course_name = serializers.CharField(source='name', max_length=100)

# 序列化器还有预留位
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        fields = ['username', 'first_name']

class CourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        创建班级
        权限：administrator
        路由：home/
        api编号：09
        """
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if this_user.groups.filter(name="administrator").exists():
            # 只有管理员能创建班级
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                course = serializer.validated_data
                course_name = course['course_name']
                students_list = course['students_list']

                if Group.objects.filter(name=course_name).exists():
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
        """
        删除班级
        权限：administrator
        路由：home/
        编号：10
        """
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if this_user.groups.filter(name="administrator").exists():
            # 只有管理员可以删除课程
            course_name = request.data.get('course_name')
            if course_name is not None and course_name != 'teacher' and course_name != 'student' and course_name != 'administrator':
                try:
                    course = Group.objects.get(name=course_name)
                    course.delete()
                    return Response({"success": "Course deleted successfully"}, status=status.HTTP_200_OK)
                except Group.DoesNotExist:

                    return Response({"error": "Group not found"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"error": "course name error"}, status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response({"error": "You don't have permission to delete course"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        """
        编辑班级成员
        权限：administrator
        路由：home/<str:coursename>/member/
        api编号：11
        """
        if request.session.get('role') == 'administrator':
            #只有管理员能编辑班级成员

            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    course = serializer.validated_data
                    course_name = kwargs.get('coursename')
                    students_list = course['students_list']

                    if not Group.objects.filter(name=course_name).exists():

                        return Response({"error": "Invalid course not exist"}, status=status.HTTP_400_BAD_REQUEST)

                    course = Group.objects.get(name=course_name)
                    old_student = course.user_set.values_list('username', flat=True)

                    students_to_add = list(set(students_list) - set(old_student))
                    students_to_delete = list(set(old_student) - set(students_list))

                    for student in students_to_add:
                        if not User.objects.filter(username=student):
                            return Response({"success": "Students to add not exist"},
                                            status=status.HTTP_400_BAD_REQUEST)
                            
                    for student in students_to_add:
                        user = User.objects.get(username=str(student))
                        course.user_set.add(user)

                    for student in students_to_delete:
                        print(student)
                        user = User.objects.get(username=str(student))
                        course.user_set.remove(user)  

                    return Response({"success": "Group update successfully"}, status=status.HTTP_200_OK)

                except:
                    return Response({"error": "Students to add not exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You don't have permission to create course"}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, *args, **kwargs):
        """
        1.获取班级中的成员
        权限：student，teacher，administrator
        路由：home/<str:coursename>/member/
        api编号：12
        
        2.获取用户所加入的班级
        权限：studnet，teacher，administrator（管理员可以获得系统中所有课程）
        路由：home/
        api编号：13
        """
        course_name = kwargs.get('coursename')
        this_user = User.objects.get(username=request.session.get('username'))
        if course_name is not None:
            try:
                course = Group.objects.get(name=course_name)
            except:
                return Response({"error": "course not exist"}, status=status.HTTP_400_BAD_REQUEST)
            if course is None or (not this_user.groups.filter(name=course_name).exists() and request.session.get(
                    'role') != 'administrator'):
                # 课程不存在或（用户不在课程中且用户不是管理员）
                return Response({"error": "You don't have permission to visit this course"},
                                status=status.HTTP_403_FORBIDDEN)

            course = Group.objects.get(name=course_name)
            students_list = course.user_set.values_list('username', flat=True)
            students = User.objects.filter(username__in=students_list)
            serializer = UserSerializers(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # 管理员有权查看所有课程,teacher和student只能查看自己所在的课程
            course_name = Group.objects.all() if request.session.get('role') == 'administrator' else this_user.groups.all()
            course_name = course_name.exclude(name='administrator')
            course_name = course_name.exclude(name='teacher')
            course_name = course_name.exclude(name='student')
            serializer = GroupSerializer(course_name, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

#########################消息系统########################################
"""消息系统
    消息系统不是聊天室，其类似于邮件，可以实现用户的单对单，但对多信息的发送
    
    暂时没有接入权限系统
"""
class MessageSerializer(serializers.Serializer):
    level = serializers.CharField(max_length=10)
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    receiver = serializers.ListField(child=serializers.CharField(max_length=20), required=False, allow_null=True)
    receive_group = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True)

class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        1.获取用户发送的信息
        路由： message/0/
        api编号：14
        
        2.获取用户接收的信息
        路由：message/1/
        api编号：15
        """
        received = bool(kwargs.get('received'))
        try:
            this_user = User.objects.get(username=request.session.get('username'))
        except:
            return Response({'error': 'invalid user,please login or register'}, status=status.HTTP_401_UNAUTHORIZED)
        if received == True: #用户收到的信息
            try:
                message_read = list(MessageRead.objects.filter(user=this_user))
                message_set = []
                for i in message_read:
                    message = i.message
                    this_message = message.to_dict()
                    this_message['id'] = message.id
                    this_message['is_read'] = i.is_read
                    message_set.append(this_message)
            except:
                return Response({'error': 'can not find received message'}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse(message_set, safe=False, status=status.HTTP_200_OK)
        elif received == False: #用户发送的信息
            try:
                message = Message.objects.filter(sender=this_user)
                message_set = []
                for i in message:
                    this_message=i.to_dict()
                    this_message['id']=i.id
                    message_set.append(this_message)
            except:
                return Response({'error': 'can not find sent message'}, status=status.HTTP_404_NOT_FOUND)
            return JsonResponse(message_set, safe=False, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        创建新信息
        路由：message/
        api编号：16
        注意单发和群发body的不同之处，api文档中有说明
        """
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            if 'receiver' in serializer.validated_data:
                if not all(
                        User.objects.filter(username=name).exists() for name in serializer.validated_data['receiver']):
                    return Response({'error': 'user not exist'}, status=status.HTTP_404_NOT_FOUND)
                try:
                    this_user = User.objects.get(username=request.session.get('username'))
                    message = Message()
                    message.level = serializer.validated_data['level']
                    message.title = serializer.validated_data['title']
                    message.content = serializer.validated_data['content']
                    message.sender = this_user
                    message.save()
                except:
                    return Response({'error': 'message save error'}, status=status.HTTP_400_BAD_REQUEST)
                for receiver_name in serializer.validated_data['receiver']:
                    try:
                        receiver = User.objects.get(username=receiver_name)
                        message_read = MessageRead()
                        message_read.message = message
                        message_read.user = receiver
                        message_read.save()
                    except:
                        return Response({'error': 'receiver save error'}, status=status.HTTP_404_NOT_FOUND)

                return Response({"success": "Create message successfully"}, status=status.HTTP_200_OK)

            elif 'receive_group' in serializer.validated_data:
                if not all(Group.objects.filter(name=name).exists() for name in
                           serializer.validated_data['receive_group']):
                    return Response({'error': 'group not exist'}, status=status.HTTP_404_NOT_FOUND)
                try:
                    this_user = User.objects.get(username=request.session.get('username'))
                    message = Message()
                    message.level = serializer.validated_data['level']
                    message.title = serializer.validated_data['title']
                    message.content = serializer.validated_data['content']
                    message.sender = this_user
                    message.save()
                except:
                    return Response({'error': 'message save error'}, status=status.HTTP_404_NOT_FOUND)
                for group_name in serializer.validated_data['receive_group']:
                    try:
                        group = Group.objects.get(name=group_name)
                        users = group.user_set.all()
                        for receiver in users:
                            message_read = MessageRead()
                            message_read.message = message
                            message_read.user = receiver
                            message_read.save()
                    except:
                        return Response({'error': 'receive_group save error'}, status=status.HTTP_404_NOT_FOUND)
                return Response({"success": "Create message successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "invalid request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """
        修改信息为已读
        路由：message/
        api编号： 17
        """
        try:
            this_user = User.objects.get(username=request.session.get('username'))
        except:
            return Response({'error': 'invalid user,please login or register'}, status=status.HTTP_401_UNAUTHORIZED)
        message_id = request.data.get('message_id')
        try:
            this_message = Message.objects.get(id=message_id)
        except:
            return Response({'error': 'message not exist'}, status=status.HTTP_404_NOT_FOUND)
        if not this_message.messageread_set.filter(user = this_user).exists():
            return Response({'error': 'message not exist'}, status=status.HTTP_404_NOT_FOUND)
        message_read = this_message.messageread_set.get(user = this_user)
        message_read.is_read = True
        message_read.save()
        return Response({"success": "change is_read to True"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        删除信息
        路由：message/
        api编号：18
        """
        try:
            message_id = request.data.get('message_id')
            this_message = Message.objects.get(id=message_id)
        except:
            return Response({'error': 'message not found'}, status=status.HTTP_404_NOT_FOUND)

        
        if this_message.sender.username != request.session.get("username"):
            return Response({"error": "You do not have permission to delete this message"},
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            this_message.delete()
        return Response({"success": "Delete message successfully"}, status=status.HTTP_204_NO_CONTENT)
