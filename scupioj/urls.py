"""
URL configuration for scupioj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import LoginView, logoutView, TokenRefreshView, UserView
from course.views import CourseView,MessageView
from assignment.views import AssignmentView, ProblemView, SubmissionView, CodeAnswerView, QuestionDetailView, GetAssignmentScoreView, GetStuScoreView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('logout/', logoutView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('home/user/', UserView.as_view()),
    path('message/',MessageView.as_view()),
    path('message/<int:received>/',MessageView.as_view()),
    path('home/user/<int:username>/', UserView.as_view()), 
    path('home/', CourseView.as_view()), 
    path('home/<str:coursename>/member/', CourseView.as_view()),
    path('home/<str:coursename>/', AssignmentView.as_view()),
    path('home/<str:coursename>/<str:assignmentname>/', ProblemView.as_view()),
    path('home/<str:coursename>/<str:assignmentname>/programming/<int:problem_id>/', CodeAnswerView.as_view()),
    path('home/<str:coursename>/<str:assignmentname>/submit/', SubmissionView.as_view()),
    path('home/<str:coursename>/<str:assignmentname>/<int:problem_id>/<str:student>/', QuestionDetailView.as_view()),
    path('home/<str:coursename>/<str:assignmentname>/<int:problem_id>/', QuestionDetailView.as_view()),
    path('home/<str:coursename>/<str:assignmentname>/getscore/',GetAssignmentScoreView.as_view()),
    path('home/<str:coursename>/<str:assignmentname>/getscore/<str:student>/',GetAssignmentScoreView.as_view()),
    path('home/<str:coursename>/<str:assignmentname>/getstuscore/<str:student>/', GetStuScoreView.as_view())
]
