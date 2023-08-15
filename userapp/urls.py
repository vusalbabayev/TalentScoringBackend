from django.urls import path, include
from . import question_views, user_views, answer_views

from django.contrib import admin

urlpatterns = [
    path('login/', user_views.loginView),
    path('register/', user_views.registerView),
    path('refresh-token/', user_views.CookieTokenRefreshView.as_view()),
    path('logout/', user_views.logoutView),
    path('user/', user_views.user),
    path('user-education-score/<str:username>/', user_views.UserScoreAPIView.as_view()),
    path('get-summry-prompt/', user_views.SummryPromptAPIView.as_view()),
    path('get-experiance-prompt/', user_views.ExperiancePromptAPIView.as_view()),
    path('get-job-title-prompt/', user_views.JobTitleAPIView.as_view()),

    path('get-question/', question_views.GetQuestionApiView.as_view()),
  
]