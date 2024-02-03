from django.db import models
from django.contrib.auth.models import Group, User
from django.utils import timezone

class Assignment(models.Model):
    course = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='assignments')
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_time = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    allow_ai = models.BooleanField(default=False)

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
    
class Submission(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    submit_time = models.DateTimeField(default=timezone.now)
    content_answer = models.TextField()
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    
    