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
class ProblemStudentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Problem
            fields = ['id', 'title', 'content_problem', 'score', 'type', 'response_limit']
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
            if(request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher'):
                serializer = ProblemSerializer(problems, many=True)
            else:
                serializer = ProblemStudentSerializer(problems, many=True)
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
        
        def post(self,request, *args, **kwargs): #布置代码作业答案
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
                
            if request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher':
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
                    serializer.save(problem=problem) 
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
            
        def get(self, request, *args, **kwargs):
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN)
            if request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher':
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
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
                
        def put(self, request, *args, **kwargs):
            this_user = User.objects.filter(username=request.session.get('username')).first()
            if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
                return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
            
            if request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher':
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
            
            if problem.assignment.name != kwargs.get('assignmentname'):
                return Response({"error":"problem not in assignment"},status=status.HTTP_400_BAD_REQUEST)
            
            if(problem.assignment.due_date <= timezone.now()):
                return Response({"error":"assignment out due"},status=status.HTTP_400_BAD_REQUEST)
                
            if(problem.response_limit is not None and Submission.objects.filter(user=this_user,problem=problem).count() >= problem.response_limit):
                return Response({"error":"You've exceeded the limit of answers"},status=status.HTTP_400_BAD_REQUEST)
               
            if problem.type == "choice":
                content_answer = request.data.get('content_answer')
                choice_student = re.findall(r"<-&(.*?)&->", content_answer, re.DOTALL)
                choice_answer = re.findall(r"<-&(.*?)&->", problem.non_programming_answer, re.DOTALL)
    
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
                score = 0
                comment = ""
                content_answer = request.data.get('content_answer')
                files = re.findall(r"<-&(.*?)&->", content_answer, re.DOTALL)
            
                # 创建临时目录
                with tempfile.TemporaryDirectory(dir=os.getcwd()+"/files/") as temp_dir:
                    temp_dir_name = os.path.basename(temp_dir)
                    
                    #识别语言，不同语言处理方式不同,现在只开发了cpp
                    if files[0] == "cpp":
                        for i in range((len(files)-1)//2):
                            temp_file_path = os.path.join(temp_dir, files[2*(i+1)-1])
                            with open(temp_file_path, 'w') as temp_file:
                                temp_file.write(files[2*(i+1)])
                        
                        codeanswers = CodeAnswer.objects.filter(problem = problem)
                        for codeanswer in codeanswers:
                            data = {
                                "dir": f"/cpp_files/{temp_dir_name}/",
                                "kb": codeanswer.space_limit if codeanswer.space_limit is not None else 10000,
                                "args":codeanswer.command_line_arguments if codeanswer.command_line_arguments is not None else "",
                                "time_limit_in_ms": codeanswer.time_limit if codeanswer.time_limit is not None else 10000,
                                "stdin_data":codeanswer.standard_input if codeanswer.standard_input is not None else ""
                            }

                            # 准备请求头
                            headers = {
                                'Content-Type': 'application/json'
                            }

                            # 创建连接
                            conn = http.client.HTTPConnection("localhost", 8001)

                            # 将数据转换为JSON格式
                            json_data = json.dumps(data)

                            # 发送POST请求
                            try:
                                conn.request("POST", "/cppsandbox/", json_data, headers)
                                response = conn.getresponse()
                                body = response.read()
                                status_code = response.status
                                json_data =  json.loads(body.decode("utf-8"))
                            except Exception as e:
                                print("An error occurred:", e)
                            finally:
                                conn.close()
                            
                            if status_code != 200:
                                comment += json.dumps(json_data, indent=4)+"\n"
                                continue
                            
                            if json_data["Status"] != "0":
                                comment += json_data["Runtime"]+" "+json_data["Runspace"]+" "+json_data["Output"]+"\n"
                            elif json_data["Output"].strip() != codeanswer.standard_output.strip():
                                comment +=  json_data["Runtime"]+" "+json_data["Runspace"]+" "+"Output false\n"
                            else:
                                score += codeanswer.score
                                comment +=  json_data["Runtime"]+" "+json_data["Runspace"]+" "+"Output true\n"
                                #下一步把docker挂载后检验
                    elif files[0] == "java":
                        pass
                    elif files[0] == "python":
                        pass
                    else:
                        return Response({"error":"language not found"},status=status.HTTP_400_BAD_REQUEST)
                         
                submission = Submission()
                submission.content_answer = content_answer
                submission.score = score
                submission.user = this_user
                submission.problem = problem
                submission.comment = comment
                submission.save()
                return Response({
                "id":request.data.get('id'),
                "score":score,
                "comment":comment
                }, status=status.HTTP_200_OK)
###########################################题目批改与信息获取##############################################
class SubmissionSerializer(serializers.Serializer):
    course_name = serializers.CharField(required=True, max_length=100)
    students_list = serializers.ListField(child=serializers.CharField(max_length=20))
class QuestionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
            return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
        
        this_user = this_user = User.objects.get(username = request.session.get('username'))
       
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
        
    def put(self, request, *args, **kwargs):
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
            return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
        
        if not (request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher'):
                return Response(status=status.HTTP_403_FORBIDDEN)
            
        this_user = this_user = User.objects.get(username = request.session.get('username'))
    
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
    
    def delete(self, request, *args, **kwargs):
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
            return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
        
        if not (request.session.get('role')  == 'administrator' or request.session.get('role')  == 'teacher'):
                return Response(status=status.HTTP_403_FORBIDDEN)
            
        this_user = this_user = User.objects.get(username = request.session.get('username'))
    
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
    
    def get(self, request, *args, **kwargs):
        this_user = User.objects.filter(username=request.session.get('username')).first()
        if not this_user.groups.filter(name=kwargs.get('coursename')).exists() and request.session.get('role') != 'administrator':
            return Response(status=status.HTTP_403_FORBIDDEN) #判断此人是否在组中
 
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
            
            
            
        
        
        
            
            