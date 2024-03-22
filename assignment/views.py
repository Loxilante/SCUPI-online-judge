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
from .models import Assignment, Problem, Submission, CodeAnswer, Image
import re
from django.utils import timezone
import tempfile
from django.http import JsonResponse
from .utils import is_in_group, is_teacher_or_administrator
###################作业操作####################################################
"""
作业系统
作业的增删改查
"""
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['name', 'description', 'created_time', 'due_date', 'allow_ai']
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
                problems = assignment.problems.all() if problem_id is None else assignment.problems.get(id=problem_id)
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
                        #检验输出
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
