from django.urls import path, include
from app.api import stage_views, repot_views

from django.contrib import admin
urlpatterns = [
    
    path('question-lists/<slug:slug>/',stage_views.StageQuestionViewSet.as_view({'get':'list'})),
    path('question-lists/<slug:slug>/<int:pk>/',stage_views.StageQuestionViewSet.as_view({'get':'retrieve'})),
    
    path('stage-parent-lists/', stage_views.StageParentListApiView.as_view(), name = 'parent-stage-api'),
    path('stage-child-lists/', stage_views.StageChildListApiView.as_view(), name = 'child-stage-api'),

    path('upload-report/', repot_views.ReportUploadAPIView.as_view())

]
