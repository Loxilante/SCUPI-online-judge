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
from .models import Assignment, Problem, Submission, CodeAnswer, Image, Token
import re
from django.utils import timezone
import tempfile
from django.http import JsonResponse
from .utils import is_in_group, is_teacher_or_administrator
from collections import Counter
###################作业操作####################################################
"""
作业系统
作业的增删改查
"""
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['name', 'description', 'created_time', 'due_date', ]
        extra_kwargs = {
            'created_time': {'read_only': True},
        }
        
class AssignmentView(APIView):
        
        permission_classes = [IsAuthenticated]
        
        @is_in_group
        def get(self, request, *args, **kwargs):
            """
            获取课程中布置的作业
            权限：all
            路由：home/<str:coursename>/
            api编号：19
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
            except Group.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            assignments = course.assignments.all()
            serializer = AssignmentSerializer(assignments, many=True)
            
            counter = 0
            for assignment_info in serializer.data:
                this_assignment = course.assignments.get(name = assignment_info["name"])
                problems = this_assignment.problems.all()
                sum_score = 0
                score_get = 0
                for problem in problems:
                    sum_score += problem.score
                    
                    if not problem.submission_set.filter(user=User.objects.get(username=request.session.get("username"))).exists():
                        score_get +=0
                    else:
                        submission = problem.submission_set.filter(user=User.objects.get(username=request.session.get("username"))).order_by('-score').first()
                        print(submission.score)
                        if submission.score is not None:
                            score_get+=submission.score
                serializer.data[counter]['sum_score'] = sum_score
                serializer.data[counter]['score_get'] = score_get
                counter += 1
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        @is_teacher_or_administrator    
        @is_in_group
        def post(self, request, *args, **kwargs):
            """
            布置作业
            权限：teacher，administrator
            路由：home/<str:coursename>/
            api编号：20
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
            except Group.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if course.assignments.filter(name=request.data.get('name')).exists():  #判断作业是否存在
                return Response({'error':'assignment exist'},status=status.HTTP_400_BAD_REQUEST)
        
            serializer = AssignmentSerializer(data=request.data)
            print(request.data)
            if serializer.is_valid():
                serializer.save(course=course) 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        @is_teacher_or_administrator    
        @is_in_group
        def put(self, request, *args, **kwargs):
            """
            更改作业信息
            权限：teacher，administrator
            路由：home/<str:coursename>/
            api编号：21
            """
            
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
                assignment = course.assignments.get(name=request.data.get('name'))
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = AssignmentSerializer(assignment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        @is_teacher_or_administrator    
        @is_in_group
        def delete(self, request, *args, **kwargs):
            """
            删除作业
            权限：teacher，administrator
            路由：home/<str:coursename>/
            api编号：22
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
            except Group.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            try:
                assignment = course.assignments.get(name=request.data.get('name'))
            except Assignment.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            assignment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
###################题目操作############################################
"""
题目系统
题目系统包含题目的增删改查
一共有三种题目，简答题（text），选择题（choice），编程题（programming）
简答题和选择题的答案设置方式一样但是，编程题的答案设置方式不同，详细请阅读api文档
"""
class ProblemSerializer(serializers.ModelSerializer):
        class Meta:
            model = Problem
            fields = ['id', 'title', 'content_problem', 'score', 'type', 'response_limit', 'non_programming_answer', 
                      'allow_ai', 'selected_token', 'sample', 'sample_explanation', 'style_criteria', 'implement_criteria', 'additional']
            extra_kwargs= {
            'id':{'read_only':True},
        }
class ProblemStudentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Problem
            fields = ['id', 'title', 'content_problem', 'score', 'type', 'response_limit']
            extra_kwargs= {
            'id':{'read_only':True},
        }

class ProblemView(APIView):
    
        permission_classes = [IsAuthenticated]       
        
        @is_teacher_or_administrator    
        @is_in_group
        def post(self,request, *args, **kwargs):
            """
            在作业中布置题目
            权限：teacher，administrator
            路由：home/<str:coursename>/<str:assignmentname>/
            api编号：23
            题目答案的设置比较复杂，详见api文档
            只有题目的文字部分，图片的设置在其他api中
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
                assignment = course.assignments.get(name=kwargs.get('assignmentname'))
            except:
                return Response(status=status.HTTP_404_NOT_FOUND) #检查班级与作业是否存在
            
            #检查token属于当前登录用户
            for problem in request.data:
                token_id = problem.get('selected_token')
                if token_id:
                    try:
                        Token.objects.get(id=token_id, user=request.user)
                    except Token.DoesNotExist:
                        return Response(status=status.HTTP_401_UNAUTHORIZED)
            
            serializer = ProblemSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save(assignment=assignment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
        @is_in_group
        def get(self, request, *args, **kwargs):
            """
            获取作业中的题目
            权限：all
            路由：home/<str:coursename>/<str:assignmentname>/
            api编号：24, 44
            只有老师与管理员可以看到题目答案，学生要在作业截止后才能看到答案
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
                assignment = course.assignments.get(name=kwargs.get('assignmentname'))
            
                problem_id = request.query_params.get('problem_id', None)
                problems = assignment.problems.all() if problem_id is None else assignment.problems.filter(id=problem_id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if(request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher' or assignment.due_date <= timezone.now()):
                serializer = ProblemSerializer(problems, many=True)
            else:
                serializer = ProblemStudentSerializer(problems, many=True) #学生要在作业截止后才能看到答案
            
            counter = 0    
            for problem_info in serializer.data:
                this_problem = Problem.objects.get(id=problem_info["id"])
                if not this_problem.submission_set.filter(user=User.objects.get(username=request.session.get("username"))).exists():
                        score_get =0
                else:
                    submission = this_problem.submission_set.filter(user=User.objects.get(username=request.session.get("username"))).order_by('-score').first()
                    print(submission.score)
                    if submission.score is not None:
                        score_get =submission.score
                
                serializer.data[counter]["score_get"] = score_get
                counter += 1
                            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        
        @is_teacher_or_administrator    
        @is_in_group
        def put(self, request, *args, **kwargs):
            """
            修改作业中的题目
            权限：teacher，administrator
            路由：home/<str:coursename>/<str:assignmentname>/
            api编号：25
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
                assignment = course.assignments.get(name=kwargs.get('assignmentname'))
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            updated_problems = []
            
            for problem in request.data:
                problem_id = problem.get('id')
                if problem_id is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                if not assignment.problems.filter(id=problem_id).exists(): #判断题目是否在作业中
                    return Response(status=status.HTTP_404_NOT_FOUND)

                this_problem = assignment.problems.get(id=problem_id)
                serializer = ProblemSerializer(this_problem, data=problem, partial=True)
                token_id = problem.get('selected_token')

                if (token_id):
                    try:
                        Token.objects.get(id=token_id, user=request.user)
                    except Token.DoesNotExist:
                        return Response(status=status.HTTP_401_UNAUTHORIZED)

                if serializer.is_valid():
                    serializer.save()
                    updated_problems.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(updated_problems, status=status.HTTP_200_OK)    
            
        @is_teacher_or_administrator    
        @is_in_group
        def delete(self, request, *args, **kwargs):
            """
            修改作业中的题目
            权限：teacher，administrator
            路由：home/<str:coursename>/<str:assignmentname>/
            api编号：26
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
                assignment = course.assignments.get(name=kwargs.get('assignmentname'))
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            delete_problem = request.data.get('delete_id')
            for delete_id in delete_problem:
                if not assignment.problems.filter(id=delete_id).exists():
                    return Response({"error":f"delete_id {delete_id} doesn't exist"},status = status.HTTP_404_NOT_FOUND)
            
            for delete_id in delete_problem:
                problem = assignment.problems.get(id=delete_id)
                problem.delete()    
                
            return Response(status=status.HTTP_204_NO_CONTENT)
         
#储存图片
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'problem', 'image', 'name']
        
class ImageView(APIView):
    permission_classes = [IsAuthenticated]
    
    @is_teacher_or_administrator    
    @is_in_group
    def post(self, request, *args, **kwargs):
        """
        上传图片
        权限：teacher，administrator
        路由：home/<str:coursename>/<str:assignmentname>/image/<int:problem_id>/
        api编号：27
        """
        # 将 QueryDict 转换为列表格式
        images_data = []
        for problem_id, image_file, names in zip(request.data.getlist('problem'), request.data.getlist('image'), request.data.getlist('name')):
            images_data.append({'problem': problem_id, 'image': image_file, 'name': names})
        
        serializer = ImageSerializer(data=images_data, many=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    @is_in_group
    def get(self, request, *args, **kwargs):
        """
        查看图片
        权限：all
        路由：home/<str:coursename>/<str:assignmentname>/image/<int:problem_id>/
        api编号：28
        """
        problem_id = kwargs.get('problem_id')
        try:
            problem = Problem.objects.get(id=problem_id)
            images = Image.objects.filter(problem=problem)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @is_teacher_or_administrator    
    @is_in_group
    def delete(self, request, *args, **kwargs):
        """
        删除图片
        权限：teacher，administrator
        路由：home/<str:coursename>/<str:assignmentname>/image/<int:problem_id>/
        api编号：29
        """
        try:
            problem = Problem.objects.get(id=kwargs.get('problem_id'))
        
            for image_id in request.data.get('image_id'):
                if not problem.image_set.filter(id=image_id).exists():
                    return Response(status=status.HTTP_404_NOT_FOUND)
            
            for image_id in request.data.get('image_id'):
                image = problem.image_set.get(id=image_id)
                image.delete()
                
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
            
#储存代码答案
class CodeAnswerSerializer(serializers.ModelSerializer):
        class Meta:
            model = CodeAnswer
            fields = ['id', 'command_line_arguments', 'standard_input', 'standard_output', 'time_limit', 'space_limit', 'score']
            extra_kwargs= {
            'id':{'read_only':True},
        }

class CodeAnswerView(APIView):
    
        permission_classes = [IsAuthenticated]       
        
        @is_teacher_or_administrator    
        @is_in_group
        def post(self,request, *args, **kwargs): #布置代码作业答案
            """
            设置编程题的判例
            权限：teacher，administrator
            路由：home/<str:coursename>/<str:assignmentname>/programming/<int:problem_id>/
            api编号：30
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
                assignment = course.assignments.get(name=kwargs.get('assignmentname'))
                problem = assignment.problems.get(id = kwargs.get('problem_id'))
            except:
                return Response(status=status.HTTP_404_NOT_FOUND) 
            if problem.type != "programming":
                return Response({"error":"this problem is not programming"},status=status.HTTP_400_BAD_REQUEST)
            
            serializer = CodeAnswerSerializer(data=request.data, many=True)
            if serializer.is_valid():
                # sum_score = 0
                # for new_code_answer in request.data:
                #     sum_score += new_code_answer.get('score')
                # old_code_answers = problem.codeanswer_set.all()
                # for old_code_answer in old_code_answer:
                #     sum_score += old_code_answer['score']
                # if sum_score != problem.score:
                #     return Response({"error":"score not match"}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save(problem=problem) 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        @is_teacher_or_administrator    
        @is_in_group
        def get(self, request, *args, **kwargs):
            """
            获取编程题的判例
            权限：teacher，administrator
            路由：home/<str:coursename>/<str:assignmentname>/programming/<int:problem_id>/
            api编号：31
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
                assignment = course.assignments.get(name=kwargs.get('assignmentname'))
                problem = assignment.problems.get(id = kwargs.get('problem_id'))
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if problem.type != "programming":
                return Response({"error":"this problem is not programming"},status=status.HTTP_400_BAD_REQUEST)
            code_answers = problem.codeanswer_set.all()
            serializer = CodeAnswerSerializer(code_answers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
         
        @is_teacher_or_administrator    
        @is_in_group        
        def put(self, request, *args, **kwargs):
            """
            修改编程题的判例
            权限：teacher，administrator
            路由：home/<str:coursename>/<str:assignmentname>/programming/<int:problem_id>/
            api编号：32
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
                assignment = course.assignments.get(name=kwargs.get('assignmentname'))
                problem = assignment.problems.get(id = kwargs.get('problem_id'))
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if problem.type != "programming":
                return Response({"error":"this problem is not programming"},status=status.HTTP_400_BAD_REQUEST)
            
            updated_code_answers = []
            
            for code_answer in request.data:
                code_answer_id = code_answer.get('id')
                if code_answer_id is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                if not problem.codeanswer_set.filter(id=code_answer_id).exists(): 
                    return Response(status=status.HTTP_404_NOT_FOUND)
                this_code_answer = problem.codeanswer_set.get(id=code_answer_id)
                serializer = CodeAnswerSerializer(this_code_answer, data=code_answer, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_code_answers.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            return Response(updated_code_answers, status=status.HTTP_200_OK)    
     
        @is_teacher_or_administrator    
        @is_in_group   
        def delete(self, request, *args, **kwargs):
            """
            删除编程题的判例
            权限：teacher，administrator
            路由：home/<str:coursename>/<str:assignmentname>/programming/<int:problem_id>/
            api编号：33
            """
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
                assignment = course.assignments.get(name=kwargs.get('assignmentname'))
                problem = assignment.problems.get(id = kwargs.get('problem_id'))
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if problem.type != "programming":
                return Response({"error":"this problem is not programming"},status=status.HTTP_400_BAD_REQUEST)
            
            delete_code_answer = request.data.get('delete_id')
            for delete_id in delete_code_answer:
                if not problem.codeanswer_set.filter(id=delete_id).exists():
                    return Response({"error":f"delete_id {delete_id} doesn't exist"},status = status.HTTP_404_NOT_FOUND)
            
            for delete_id in delete_code_answer:
                code_answer = problem.codeanswer_set.get(id=delete_id)
                code_answer.delete()

                return Response(status=status.HTTP_204_NO_CONTENT)
            
################### TOKEN相关 #####################################

class TokenSerializer(serializers.ModelSerializer):

    token_display = serializers.SerializerMethodField()
    created_time = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    def get_token_display(self, obj):
        """
        token只显示开头5个字符结尾4个字符
        """
        if obj.token and len(obj.token) > 8:
            return f"{obj.token[:5]}...{obj.token[-4:]}"
        return "Invalid Token"
    
    class Meta:
        model = Token
        fields = ['id', 'name', 'token', 'platform', 'token_display', 'created_time']
        extra_kwargs = {
            'token': {'write_only': True}
        }

        

class TokenView(APIView):

    permission_classes = [IsAuthenticated]

    @is_teacher_or_administrator
    def get(self, request, *args, **kwargs):
        """
        获取当前登录用户的所有Token
        """
        tokens = Token.objects.filter(user=request.user)
        serializer = TokenSerializer(tokens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_teacher_or_administrator
    def post(self, request, *args, **kwargs):
        """
        为当前登录用户添加一个新Token
        """
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TokenDetailView(APIView):
    """
    处理单个Token的更新和删除
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, id, user):
        try:
            return Token.objects.get(id=id, user=user)
        except Token.DoesNotExist:
            return None

    @is_teacher_or_administrator
    def get(self, request, id, *args, **kwargs):
        """
        获取单个Token信息
        """
        token = self.get_object(id, request.user)
        if token is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = TokenSerializer(token)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @is_teacher_or_administrator
    def put(self, request, id, *args, **kwargs):
        """
        更新单个Token信息
        """
        password = request.data.get('password')

        if not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.check_password(password):
            return Response(status=status.HTTP_403_FORBIDDEN)

        token = self.get_object(id, request.user)
        if token is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = TokenSerializer(instance=token, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @is_teacher_or_administrator
    def delete(self, request, id, *args, **kwargs):
        """
        根据URL中id删除单个Token
        """

        password = request.data.get('password')
        if not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.check_password(password):
            return Response(status=status.HTTP_403_FORBIDDEN)

        token = self.get_object(id, request.user)
        if token is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


################### AI相关API #####################################

class ProblemAISettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['sample', 'sample_explanation', 'style_criteria', 'implement_criteria', 'additional']

class ProblemAISettingsView(APIView):

    permission_classes = [IsAuthenticated]

    @is_teacher_or_administrator
    @is_in_group
    def get(self, request, *args, **kwargs):
        """
        获取一个题目的AI设置
        路由: home/<str:coursename>/<str:assignmentname>/ai/<int:problem_id>/
        """
        try:
            problem = Problem.objects.get(id=kwargs.get('problem_id'))
        except Problem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProblemAISettingsSerializer(problem)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_teacher_or_administrator
    @is_in_group
    def put(self, request, *args, **kwargs):
        """
        更新一个题目的AI设置 (主要更新方法)
        路由: home/<str:coursename>/<str:assignmentname>/ai/<int:problem_id>/
        """
        try:
            problem = Problem.objects.get(id=kwargs.get('problem_id'))
        except Problem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProblemAISettingsSerializer(problem, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()  # 保存到数据库
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @is_teacher_or_administrator
    @is_in_group
    def post(self, request, *args, **kwargs):
        """
        处理POST请求，直接调用PUT方法来更新AI设置。
        路由: home/<str:coursename>/<str:assignmentname>/ai/<int:problem_id>/
        """
        return self.put(request, *args, **kwargs)

    @is_teacher_or_administrator
    @is_in_group
    def delete(self, request, *args, **kwargs):
        """
        清空一个题目的AI设置
        路由: home/<str:coursename>/<str:assignmentname>/ai/<int:problem_id>/
        """
        try:
            problem = Problem.objects.get(id=kwargs.get('problem_id'))
        except Problem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        problem.sample = ""
        problem.sample_explanation = ""
        problem.style_criteria = ""
        problem.implement_criteria = ""
        problem.additional = ""
        
        problem.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

###################答题与判题操作###################################

class SubmissionView(APIView):
        permission_classes=[IsAuthenticated]
        
        @is_in_group
        def post(self, request, *args, **kwargs):
            """
            回答题目
            权限：all
            路由：home/<str:coursename>/<str:assignmentname>/submit/
            api编号：34
            """
            try:
                problem = Problem.objects.get(id = request.data.get('id'))
                this_user = User.objects.get(username = request.session.get('username'))
            except:
                return Response(status = status.HTTP_404_NOT_FOUND)
            
            if problem.assignment.name != kwargs.get('assignmentname'):
                return Response({"error":"problem not in assignment"},status=status.HTTP_400_BAD_REQUEST)
            
            if(problem.assignment.due_date <= timezone.now()):
                return Response({"error":"assignment out due"},status=status.HTTP_400_BAD_REQUEST)
                
            if(problem.response_limit is not None and Submission.objects.filter(user=this_user,problem=problem).count() >= problem.response_limit):
                return Response({"error":"You've exceeded the limit of answers"},status=status.HTTP_400_BAD_REQUEST)
            
            result = {
                "id":request.data.get('id'),
            }
               
            if problem.type == "choice":
                content_answer = request.data.get('content_answer')
                choice_student = re.findall(r"<-&(.*?)&->", content_answer, re.DOTALL)
                choice_answer = re.findall(r"<-&(.*?)&->", problem.non_programming_answer, re.DOTALL)
    
                choice_student = [item.lower() for item in choice_student]
                choice_answer = [item.lower() for item in choice_answer]
                
                if Counter(choice_student) == Counter(choice_answer):
                    score = problem.score
                else:
                    score = 0
                submission = Submission()
                submission.content_answer = content_answer
                submission.score = score
                submission.user = this_user
                submission.problem = problem
                submission.save()
                result["score"] = score

            elif problem.type == "text":
                score = None
                comment = None
                content_answer = request.data.get('content_answer')
                
                submission = Submission()
                submission.content_answer = content_answer
                submission.score = score
                submission.user = this_user
                submission.problem = problem
                submission.comment = "Wait for grading"
                submission.save()
                result["score"] = score
                result["comment"] = "Wait for grading"
                   
            else:
                score = 0
                comment = ""
                content_answer = request.data.get('content_answer')
                files = re.findall(r"<-&(.*?)&->", content_answer, re.DOTALL)

                # 创建临时目录
                with tempfile.TemporaryDirectory(dir=os.getcwd()+"/files/") as temp_dir:
                    temp_dir_name = os.path.basename(temp_dir)
                    
                    #生成代码文件
                    for i in range((len(files)-1)//2):
                        temp_file_path = os.path.join(temp_dir, files[2*(i+1)-1])
                        with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                            temp_file.write(files[2*(i+1)])
                    
                    #识别语言，不同语言处理方式不同,现在只开发了cpp和java
              
                    codeanswers = CodeAnswer.objects.filter(problem = problem)
                    for codeanswer in codeanswers:
                        data = {
                            "dir": f"/{temp_dir_name}/",
                            "kb": codeanswer.space_limit if codeanswer.space_limit is not None else 10000,
                            "args":codeanswer.command_line_arguments if codeanswer.command_line_arguments is not None else "",
                            "time_limit_in_ms": codeanswer.time_limit if codeanswer.time_limit is not None else 10000,
                            "stdin_data":codeanswer.standard_input if codeanswer.standard_input is not None else ""
                        }

                        # 准备请求头    
                        headers = {
                            'Content-Type': 'application/json'
                        }

                        # 创建连接,根据语言不同连接不同的container
                        if files[0] == "cpp":
                            conn = http.client.HTTPConnection("localhost", 8001)
                        elif files[0] == "java":
                            conn = http.client.HTTPConnection("localhost", 8002)
                        elif files[0] == "python":
                            pass
                        else:
                            return Response({"error":"language not found"},status=status.HTTP_400_BAD_REQUEST)

                        # 将数据转换为JSON格式
                        json_data = json.dumps(data)

                        # 发送POST请求
                        try:
                            conn.request("POST", "/sandbox/", json_data, headers)
                            response = conn.getresponse()
                            body = response.read()
                            status_code = response.status
                            json_data =  json.loads(body.decode("utf-8"))
                        except Exception as e:
                            print("An error occurred:", e)
                        finally:
                            conn.close()

                        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                        # print(json_data)

                        #检验输出
                        if status_code != 200:
                            comment += json.dumps(json_data, indent=4)+"\n"
                        else:
                            if json_data["Status"] != "0":
                                comment += json_data["Runtime"]+" "+json_data["Runspace"]+" "+json_data["Output"]+"\n"
                            elif json_data["Output"].strip() != codeanswer.standard_output.strip():
                                comment +=  json_data["Runtime"]+" "+json_data["Runspace"]+" "+"Output false\n"
                            else:
                                score += codeanswer.score
                                comment +=  json_data["Runtime"]+" "+json_data["Runspace"]+" "+"Output true\n"
                    
                    s_match = 0
                    i_match = 0
                        
                    if problem.allow_ai == True:

                        selected_token = None
                        if problem.selected_token:
                            selected_token = problem.selected_token
                        else:
                            print("Invalid token issolated with problem")
                            comment += "Invalid token. Fail to AI review."

                        if selected_token:

                            # 1. 构建 system_content (messages)
                            system_content = "假如你是一名经验丰富的大学计算机教授，你需要慢慢地、仔细地为一道作业给出评分。下面是这道作业，学生需要阅读以下题面严格按照其中的输入、输出格式编写结构清晰、可读性高的代码，使之在尽可能优秀的时间与空间实现下完成题面要求：" + "\n"
                            system_content += re.search(r"<-&\^stem\s*(.*?)\s*stem\$&->", problem.content_problem, re.DOTALL).group(1) + "\n"

                            if problem.sample:
                                system_content += "下面我将给出示例代码：" + "\n"
                                system_content += problem.sample + "\n"
                            
                            if problem.sample_explanation:
                                system_content += "这是示例代码具体实现的解释：" + "\n"
                                system_content += problem.sample_explanation + "\n"
                            
                            system_content += "下面我将给出很多学生的作业，请你完成以下任务：" + "\n"
                            system_content += "1.就学生作业的代码风格进行评分，以示例代码为模板，满分为100分。" + "\n"

                            if problem.style_criteria:
                                system_content += "下面是代码风格的具体要求：" + "\n"
                                system_content += problem.style_criteria + "\n"
                                                        
                            system_content += "2.就学生作业的代码实现进行评分，以示例代码的具体实现为模板，满分为100分。" + "\n"

                            if problem.implement_criteria:
                                system_content += "下面是代码实现的具体要求：" + "\n"
                                system_content += problem.implement_criteria + "\n"
                            
                            if problem.additional:
                                system_content += "下面我将给出一些可能的实现以及分值：" + "\n"
                                system_content += problem.additional + "\n"
                            
                            system_content += "3. 就代码风格、代码实现两方面给出简短的评价和详细的修改意见。注意字数控制在400字以内，不需要援引原代码只需要指出哪里有问题以及修改意见，不要输出类似**或者`的markdown语法。" + "\n"
                            system_content += "在输出时，请不要输出其他内容，仅按照我下面给出的格式输出三行内容：" + "\n"
                            system_content += "S: 代码风格评分" + "\n"
                            system_content += "I: 代码实现评分" + "\n"
                            system_content += "N: 简短的评价和详细的的修改意见" + "\n"
                            system_content += "如果收到的请求不是代码，S项为0分；如果与题目要求实现区别过大，S项正常评分，I项为0分；N项正常输出。" + "\n"

                            messages = [
                                {
                                    "role": "system",
                                    "content": system_content
                                }
                            ]

                            # print("\n######### CONT ###############\n" + content_answer)

                            # 2. 加入历史消息
                            for each_history in problem.ai_histories.all():
                                if each_history.history:
                                    try:
                                        history_dict = json.loads(each_history.history)
                                        if isinstance(history_dict, dict) and "role" in history_dict and "content" in history_dict:
                                            messages.append(history_dict)
                                        else:
                                            print(f"Warning: AIHistory ID {each_history.id} format incorrect.")
                                    except json.JSONDecodeError:
                                        print(f"Warning: AIHistory ID {each_history.id} invalid.")

                            
                            # 3. 匹配学生代码
                            # student_code_match = re.search(r"<-&.*?&->\s*<-&.*?&->\s*<-&(.*?)&->", content_answer, re.DOTALL)
                            # student_code = ""

                            # if student_code_match:
                            #     student_code = student_code_match.group(1)
                            # else:
                            #     print(f"Warning: cannot extract student code")
                            
                            messages.append({"role": "user", "content": content_answer})

                            # 4. 构建发送的最终payload
                            payload_for_ai = {
                                "platform": selected_token.platform,
                                "token": selected_token.token,
                                "messages": messages
                            }
                            
                            # 准备连接
                            conn = http.client.HTTPConnection("localhost", 8302)

                            try:
                                conn.request("POST", "/aigrading/", json.dumps(payload_for_ai), headers)
                                response = conn.getresponse()
                                body = response.read()
                                status_code = response.status
                                json_data = json.loads(body.decode("utf-8"))
                            except Exception as e:
                                print("An error occurred:", e)
                            finally:
                                conn.close()

                            # 获得AI回复
                            assistant_reply = ""
                            
                            if status_code != 200:
                                comment += json.dumps(json_data, indent=4)+"\n"
                            elif status_code == 200 and json_data and "response" in json_data:
                                assistant_reply = json_data.get("response")
                            
                            if content_answer and assistant_reply:
                                problem.ai_histories.create(history = json.dumps({"role": "user", "content": content_answer}))
                                problem.ai_histories.create(history = json.dumps({"role": "assistant", "content": assistant_reply}))
                            
                            # print("\n######### ASSI ###############\n" + json_data.get("response"))

                            s_match_obj = re.search(r"S:\s*(\d+)", assistant_reply)
                            i_match_obj = re.search(r"I:\s*(\d+)", assistant_reply)
                            n_match_obj = re.search(r"N:\s*(.*)", assistant_reply, re.DOTALL)

                            s_match = s_match_obj.group(1) if s_match_obj else "0"
                            i_match = i_match_obj.group(1) if i_match_obj else "0"
                            n_match = n_match_obj.group(1) if n_match_obj else "Error: AI comment not found"

                            # print("S"+s_match)
                            # print("I"+i_match)
                            
                            result["stylescore"] = s_match
                            result["implescore"] = i_match
                            comment += "代码风格分: "+s_match + "\n代码实现分: " + i_match + "\n" + n_match

                
                submission = Submission()
                submission.content_answer = content_answer
                submission.score = score
                submission.user = this_user
                submission.problem = problem
                submission.comment = comment
                submission.stylescore = int(s_match)
                submission.implescore = int(i_match)
                submission.save()
                result["score"] = score
                result["comment"] = comment

            return Response(result, status=status.HTTP_200_OK)
            
            

###########################################题目批改与信息获取##############################################
class QuestionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @is_in_group
    def get(self, request, *args, **kwargs):
        """
        1.查看全班成员在特定题目的最新提交记录
        权限：teacher，administrator
        路由：home/<str:coursename>/<str:assignmentname>/<int:problem_id>/all/
        api编号：35
        
        2.查看特定学生在某题目的全部提交记录
        权限：teacher，administrator，student（只能看自己的）
        路由：home/<str:coursename>/<str:assignmentname>/<int:problem_id>/<str:student>/
        阿皮编号：36
        """
        try:
            course = Group.objects.get(name=kwargs.get('coursename'))
            assignment = course.assignments.get(name = kwargs.get('assignmentname'))
            problem = assignment.problems.get(id=kwargs.get('problem_id'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if(kwargs.get('student') == 'all'):
            if not (request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher'):
                return Response(status=status.HTTP_403_FORBIDDEN)
            students = User.objects.filter(groups = course)
            submission_list = []
            for student in students:
                try:
                    this_submission = Submission.objects.filter(user=student, problem=problem).latest('submit_time')
                    submission_data = {
                        # 获取字段值
                        'id': this_submission.id,
                        'problem_id': this_submission.problem_id,
                        'submit_time': this_submission.submit_time,
                        'content_answer': this_submission.content_answer,
                        'score': this_submission.score,
                        'comment': this_submission.comment,
                        'username': student.username,
                        'first_name': student.first_name
                    }
                except Submission.DoesNotExist:
                    submission_data = {
                        'id': None,
                        'problem_id': None,
                        'submit_time': None,
                        'content_answer': None,
                        'score': None,
                        'comment': None,
                        'username': student.username,
                        'first_name': student.first_name
                    }
                submission_list.append(submission_data)
                
            return JsonResponse(submission_list ,status=status.HTTP_200_OK, safe=False)
            
        else:
            try:
                student = User.objects.get(username = kwargs.get('student'))
                submission = Submission.objects.filter(user = student, problem = problem).values()
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            if not (request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher'):
                if(student.username != request.session.get('username')):
                    return Response(status=status.HTTP_403_FORBIDDEN)
            return Response(submission, status=status.HTTP_200_OK)
        
    @is_teacher_or_administrator    
    @is_in_group
    def put(self, request, *args, **kwargs):
        """
        为题目评分
        权限：teacher，administrator
        路由：home/<str:coursename>/<str:assignmentname>/<int:problem_id>/
        api编号：37
        """
        try:
            course = Group.objects.get(name=kwargs.get('coursename'))
            assignment = course.assignments.get(name = kwargs.get('assignmentname'))
            problem = assignment.problems.get(id=kwargs.get('problem_id'))
            submission = problem.submission_set.get(id=request.data.get('submission_id'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        submission.score = request.data.get('score')
        submission.comment = request.data.get('comment')
        submission.save()
        return Response({'success':'score and comment updated'}, status=status.HTTP_200_OK)
    
    @is_teacher_or_administrator    
    @is_in_group
    def delete(self, request, *args, **kwargs):
        """
        删除答题记录
        权限：teacher，administrator
        路由：home/<str:coursename>/<str:assignmentname>/<int:problem_id>/
        api编号：38
        """
        try:
            course = Group.objects.get(name=kwargs.get('coursename'))
            assignment = course.assignments.get(name = kwargs.get('assignmentname'))
            problem = assignment.problems.get(id=kwargs.get('problem_id'))
            for delete_id in request.data.get('delete_id'):
                submission = problem.submission_set.get(id = delete_id)
                submission.delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class GetAssignmentScoreView(APIView):
    
    permission_classes=[IsAuthenticated]
    
    @is_in_group
    def get(self, request, *args, **kwargs):
        """
        1.获取作业中所有题目得分细则（每道题的得分）
        权限：all
        路由：home/<str:coursename>/<str:assignmentname>/getscore/<str:student>/
        api编号：39
        
        2.获取作业设定的总分（由所有problem组成）
        权限：all
        路由：home/<str:coursename>/<str:assignmentname>/getscore/
        api编号：40
        """
        if kwargs.get('student') == None:
            try:
                course = Group.objects.filter(name=kwargs.get('coursename')).first()
                assignment = course.assignments.get(name = kwargs.get('assignmentname'))
                problems = list(assignment.problems.all().values())
                
                sum_score = 0
                for problem in problems:
                    sum_score += problem['score']
                    
                return Response({"sumscore":sum_score},status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if request.session.get('role') == 'student' and kwargs.get('student') != request.session.get('username'):
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            try:
                course = Group.objects.filter(name=kwargs.get('coursename')).first()
                assignment = course.assignments.get(name = kwargs.get('assignmentname'))
                problems = list(assignment.problems.all().values())
                problem_score_list = []
                for problem in problems:
                   
                    this_problem = assignment.problems.get(id = problem["id"])
                    if not this_problem.submission_set.filter(user = User.objects.get(username = kwargs.get('student'))).exists():
                        score_list = {
                        "problem_id":this_problem.id,
                        "title":this_problem.title,
                        "score":0
                        }
                    else:
                        submission = this_problem.submission_set.filter(user=User.objects.get(username=kwargs.get('student'))).order_by('-score').first()
                        score_list = {
                        "problem_id":this_problem.id,
                        "title":this_problem.title,
                        "score":submission.score
                        }
                    
                    problem_score_list.append(score_list)
                
                return JsonResponse(problem_score_list,status=status.HTTP_200_OK, safe=False)
            except:     
                return Response(status=status.HTTP_404_NOT_FOUND)
            
class GetStuScoreView(APIView): #获取作业总得分
    permission_classes = [IsAuthenticated]
    
    @is_in_group
    def get(self, request, *args, **kwargs):
        """
        1.获取特定学生的作业总得分
        权限：teacher，administrator，student（学生只能查看自己）
        路由：home/<str:coursename>/<str:assignmentname>/getstuscore/<str:student>/
        api编号：41
        
        2.获取所有学生作业总得分
        权限：teacher，administrator
        路由：home/<str:coursename>/<str:assignmentname>/getstuscore/all/
        api编号：42
        """
        if kwargs.get('student') == "all":
            if request.session.get('role') == 'student':
                return Response(status=status.HTTP_403_FORBIDDEN)
            course = Group.objects.filter(name=kwargs.get('coursename')).first()
            assignment = course.assignments.get(name = kwargs.get('assignmentname'))
            problems = list(assignment.problems.all().values())
            students = User.objects.filter(groups = course).values()
            studnet_list = []
            for student in students:
                score = 0
                for problem in problems:
                    this_problem = assignment.problems.get(id = problem["id"])
                    if not this_problem.submission_set.filter(user_id = student['id']).exists():
                        score +=0
                    else:
                        submission = this_problem.submission_set.filter(user_id = student['id']).order_by('-score').first()
                        if submission.score is not None:
                            score+=submission.score
                        
                this_stulist = {
                'assignment_id': assignment.id,
                'assignment_name': assignment.name,
                'username':student['username'],
                'first_name':student['first_name'],
                'score': score
                }
                studnet_list.append(this_stulist)

            return JsonResponse(studnet_list ,status=status.HTTP_200_OK, safe=False)    
        else:
            if request.session.get('role') == 'student' and request.session.get('username') != kwargs.get('student'):
                return Response(status=status.HTTP_403_FORBIDDEN)
            try:
                course = Group.objects.filter(name=kwargs.get('coursename')).first()
                assignment = course.assignments.get(name = kwargs.get('assignmentname'))
                problems = list(assignment.problems.all().values())
                score = 0
                for problem in problems:
                    this_problem = assignment.problems.get(id = problem["id"])
                    if not this_problem.submission_set.filter(user = User.objects.get(username = kwargs.get('student'))).exists():
                        score +=0
                    else:
                        submission = this_problem.submission_set.filter(user=User.objects.get(username=kwargs.get('student'))).order_by('-score').first()
                        if submission.score is not None:
                            score+=submission.score
  
                return Response({
                    'assignment_id': assignment.id,
                    'assignment_name': assignment.name,
                    'score': score
                    },status=status.HTTP_200_OK)
            except:     
                return Response(status=status.HTTP_404_NOT_FOUND)
            
class RunCodeView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        运行代码
        权限：all
        路由：runcode/
        api编号：43
        """
        code = request.data.get('code')
        files = re.findall(r"<-&(.*?)&->", code, re.DOTALL)

        # 创建临时目录
        with tempfile.TemporaryDirectory(dir=os.getcwd()+"/files/") as temp_dir:
            temp_dir_name = os.path.basename(temp_dir)
            
            #生成代码文件
            for i in range((len(files)-1)//2):
                temp_file_path = os.path.join(temp_dir, files[2*(i+1)-1])
                with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                    temp_file.write(files[2*(i+1)])
            
            #识别语言，不同语言处理方式不同,现在只开发了cpp和java
            if request.data.get('space_limit') > 100000 or request.data.get('time_limit') > 100000:
                return Response({"error":"don't allow space_limit or time_limit which is greater than 100000"}, status= status.HTTP_406_NOT_ACCEPTABLE )

            data = {
                "dir": f"/{temp_dir_name}/",
                "kb": request.data.get('space_limit') if request.data.get('space_limit') is not None else 10000,
                "args": request.data.get('command_line_arguments') if request.data.get('command_line_arguments') is not None else "",
                "time_limit_in_ms": request.data.get('time_limit') if request.data.get('time_limit') is not None else 10000,
                "stdin_data": request.data.get('standard_input') if request.data.get('standard_input') is not None else ""
            }

            # 准备请求头
            headers = {
                'Content-Type': 'application/json'
            }

            # 创建连接,根据语言不同连接不同的container
            if files[0] == "cpp":
                conn = http.client.HTTPConnection("localhost", 8001)
            elif files[0] == "java":
                conn = http.client.HTTPConnection("localhost", 8002)
            elif files[0] == "python":
                pass
            else:
                return Response({"error":"language not found"},status=status.HTTP_400_BAD_REQUEST)

            # 将数据转换为JSON格式
            json_data = json.dumps(data)

            # 发送POST请求
            try:
                conn.request("POST", "/sandbox/", json_data, headers)
                response = conn.getresponse()
                body = response.read()
                status_code = response.status
                json_data =  json.loads(body.decode("utf-8"))
            except Exception as e:
                print("An error occurred:", e)
            finally:
                conn.close()
            #检验输出
            if status_code != 200:
                return Response({'return_value':None,
                             'output':json.dumps(json_data, indent=4),
                             'run_time':None,
                             'run_space':None},status = status.HTTP_200_OK)
            
            return Response({'return_value':json_data["Status"],
                             'output':json_data["Output"],
                             'run_time':json_data["Runtime"],
                             'run_space':json_data["Runspace"]},status = status.HTTP_200_OK)
