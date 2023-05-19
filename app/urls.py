from django.urls import path, include
from app.api import question_views, user_views, answer_views, stage_views

from django.contrib import admin
urlpatterns = [
    path('login/', user_views.loginView),
    path('register/', user_views.registerView),
    path('refresh-token/', user_views.CookieTokenRefreshView.as_view()),
    path('logout/', user_views.logoutView),
    path("user/", user_views.user),
    #path("question-lists/<slug:slug>/",stage_views.StageQuestionApiView.as_view()),
    path("question-lists/<slug:slug>/",stage_views.StageQuestionViewSet.as_view({'get':'list'})),
    path("question-lists/<slug:slug>/<int:pk>/",stage_views.StageQuestionViewSet.as_view({'get':'retrieve'})),
    path('stage-parent-lists/', stage_views.StageParentListApiView.as_view()),
    path('stage-child-lists/', stage_views.StageChildListApiView.as_view()),
]
