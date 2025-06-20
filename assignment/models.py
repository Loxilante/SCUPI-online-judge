import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group, User
from django.utils import timezone

class Token(models.Model):
    PLATFORM_CHOICES = [
        ('ChatGPT', 'ChatGPT'),
        ('DeepSeek', 'DeepSeek'),
        ('Gemini', 'Gemini'),
        ('Claude', 'Claude'),
        ('Grok', 'Grok'),
        ('Doubao', 'Doubao'),
        ('KIMI', 'KIMI'),
        ('Qwen', 'Qwen'),
        ('Hunyuan', 'Hunyuan')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_tokens')
    name = models.CharField(max_length=255)
    token = models.TextField()
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True) 

class Assignment(models.Model):
    course = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='assignments')
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.name
    
class Problem(models.Model):
    PROGRAMMING = 'programming' #编程题
    CHOICE = 'choice' #选择题
    TEXT = 'text' #简答题或填空题
    
    PROBLEM_TYPE_CHOICES = [
        (PROGRAMMING, 'Programming'),
        (CHOICE, 'Choice'),
        (TEXT, 'Text')
    ]
    
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='problems')
    title = models.CharField(max_length=255)
    content_problem = models.TextField()
    score = models.IntegerField()
    type = models.CharField(max_length=165, choices=PROBLEM_TYPE_CHOICES)
    response_limit = models.IntegerField(null=True, blank=True)
    non_programming_answer = models.TextField(null=True, blank=True)
    
    allow_ai = models.BooleanField(default=False)
    selected_token = models.ForeignKey(Token, on_delete=models.SET_NULL, null=True, blank=True)
    # prompt相关
    sample = models.TextField(null=True, blank=True)
    sample_explanation = models.TextField(null=True, blank=True)
    style_criteria = models.TextField(null=True, blank=True)
    implement_criteria = models.TextField(null=True, blank=True)
    additional = models.TextField(null=True, blank=True)

class AIHistory(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='ai_histories')
    history = models.TextField(null=True, blank=True) 

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    submit_time = models.DateTimeField(default=timezone.now)
    content_answer = models.TextField()
    score = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    # AI判题得分
    stylescore = models.IntegerField(null=True, blank=True)
    implescore = models.IntegerField(null=True, blank=True)
    
class CodeAnswer(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    command_line_arguments = models.CharField(max_length= 100, null=True, blank=True, default = None)
    standard_input = models.TextField(null=True, blank=True, default = None)
    standard_output = models.TextField()
    time_limit = models.IntegerField(default = 10000) #时间单位为ms
    space_limit = models.IntegerField(default = 10000) #内存单位为kb
    score = models.IntegerField()
    
class Image(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.CharField(max_length= 100)
    image = models.ImageField(upload_to='images/')
    
    def delete(self, *args, **kwargs):
        # 删除文件系统中的文件
        if self.image:
            image_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            if os.path.isfile(image_path):
                os.remove(image_path)
        super(Image, self).delete(*args, **kwargs)
    