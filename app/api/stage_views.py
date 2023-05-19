from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from app.models import Question,  Stage#, Answer
from app.serializers import StageQuestionListSerializer, StageParentListSerializer, StageChildListSerializer


class StageQuestionApiView(APIView):

    def get(self, request, slug):

        stage = Stage.objects.filter(slug=slug)
        serializer =  StageQuestionListSerializer(stage, many = True)

        return Response(serializer.data)

class StageQuestionViewSet(ViewSet):
    queryset = Stage.objects.all()

    def list(self, request, slug):
        item = Stage.objects.filter(slug=slug)
        
        serializer = StageQuestionListSerializer(item, many = True)

        return Response(serializer.data)
    
    def retrieve(self, request, slug, pk):

        item = Stage.objects.filter(slug=slug).prefetch_related(
            Prefetch("questions", queryset=Question.objects.filter(question_dependens_on_answer=pk)))
        serializer = StageQuestionListSerializer(item, many = True)
        return Response(serializer.data)  

class StageParentListApiView(APIView):

    def get(self, request):

        stage = Stage.objects.filter(parent=None)
        serializer = StageParentListSerializer(stage, many = True)

        return Response(serializer.data)
    
class StageChildListApiView(APIView):

    def get(self, request):

        stage = Stage.objects.exclude(parent=None)
        serializer = StageParentListSerializer(stage, many = True)

        return Response(serializer.data)