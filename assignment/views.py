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
from .models import Assignment, Problem, Submission
import re
from django.utils import timezone
###################作业操作###################################
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['name', 'description', 'created_time', 'due_date', 'allow_ai']
        extra_kwargs = {
            'created_time': {'read_only': True},
        }
        
class AssignmentView(APIView):
        
        permission_classes = [IsAuthenticated]
        
        def get(self, request, *args, **kwargs):
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
            except Group.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            assignments = course.assignments.all()
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        
        def post(self, request, *args, **kwargs):
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
            
            if request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher':
                try:
                    course = Group.objects.get(name=kwargs.get('coursename'))
                except Group.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
              
                if course.assignments.filter(name=request.data.get('name')).exists():  #判断作业是否存在
                    return Response({'error':'assignment exist'},status=status.HTTP_400_BAD_REQUEST)
            
                serializer = AssignmentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(course=course) 
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        
        def put(self, request, *args, **kwargs):
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
            
            if request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher':
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
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        
        def delete(self, request, *args, **kwargs):
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
            
            if request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher':
                try:
                    course = Group.objects.get(name=kwargs.get('coursename'))
                except Group.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                try:
                    assignment = course.assignments.get(name=request.data['name'])
                except Assignment.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                assignment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        
###################题目操作###################################
class ProblemSerializer(serializers.ModelSerializer):
        class Meta:
            model = Problem
            fields = ['id', 'title', 'content_problem', 'score', 'type', 'response_limit', 'non_programming_answer']
            extra_kwargs= {
            'id':{'read_only':True},
        }
class ProblemView(APIView):
    
        permission_classes = [IsAuthenticated]       
        
        def post(self,request, *args, **kwargs): #在作业中布置题目
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
                
            if request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher':
                try:
                    course = Group.objects.get(name=kwargs.get('coursename'))
                    assignment = course.assignments.get(name=kwargs.get('assignmentname'))
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND) #检查班级与作业是否存在
                
                serializer = ProblemSerializer(data=request.data, many=True)
                if serializer.is_valid():
                    serializer.save(assignment=assignment) 
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
        def get(self, request, *args, **kwargs):
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN)
            
            try:
                course = Group.objects.get(name=kwargs.get('coursename'))
                assignment = course.assignments.get(name=kwargs.get('assignmentname'))
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            problems = assignment.problems.all()
            serializer = ProblemSerializer(problems, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        def put(self, request, *args, **kwargs):
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
            
            if request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher':
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
                    if serializer.is_valid():
                        serializer.save()
                        updated_problems.append(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
                    
                return Response(updated_problems, status=status.HTTP_200_OK)    
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
        def delete(self, request, *args, **kwargs):
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
            
            if request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher':
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
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

###################答题与判题操作###################################

class SubmissionView(APIView):
        permission_classes=[IsAuthenticated]

        def post(self, request, *args, **kwargs):
            try:
                problem = Problem.objects.get(id = request.data.get('id'))
                this_user = User.objects.get(username = request.session.get('username'))
            except:
                return Response(status = status.HTTP_404_NOT_FOUND)
            
            if(problem.assignment.due_date <= timezone.now()):
                return Response({"error":"assignment out due"},status=status.HTTP_400_BAD_REQUEST)
                
            if(problem.response_limit is not None and Submission.objects.filter(user=this_user,problem=problem).count() >= problem.response_limit):
                return Response({"error":"You've exceeded the limit of answers"},status=status.HTTP_400_BAD_REQUEST)
               
            if problem.type == "choice":
                content_answer = request.data.get('content_answer')
                choice_student = re.findall(r"<-&(.*?)&->", content_answer)
                choice_answer = re.findall(r"<-&(.*?)&->", problem.non_programming_answer)
    
                choice_student = [item.lower() for item in choice_student]
                choice_answer = [item.lower() for item in choice_answer]
                
                if len(choice_student) == len(choice_answer) and all(elem in choice_answer for elem in choice_student):
                    score = problem.score
                else:
                    score = 0
                submission = Submission()
                submission.content_answer = content_answer
                submission.score = score
                submission.user = this_user
                submission.problem = problem
                submission.save()
                return Response({
                    "id":request.data.get('id'),
                    "score":score
                    }, status=status.HTTP_200_OK)
            elif problem.type == "text":
                score = None
                comment = None
                content_answer = request.data.get('content_answer')
                
                if problem.assignment.allow_ai == True:
                    #ai 判题未开发
                    submission = Submission()
                    submission.content_answer = content_answer
                    submission.score = score
                    submission.user = this_user
                    submission.problem = problem
                    submission.comment = "ai grading undeveloped"
                    submission.save()
                    return Response({
                    "id":request.data.get('id'),
                    "score":score,
                    "comment":comment
                    }, status=status.HTTP_200_OK)
                else:
                    submission = Submission()
                    submission.content_answer = content_answer
                    submission.score = score
                    submission.user = this_user
                    submission.problem = problem
                    submission.comment = "Wait for grading"
                    submission.save()
                    return Response({
                    "id":request.data.get('id'),
                    "score":score,
                    "comment":"Wait for grading"
                    }, status=status.HTTP_200_OK)
                   
            else:
                pass
        