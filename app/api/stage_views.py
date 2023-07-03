from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db import connection
from django.db import reset_queries

from app.models import Question,  Stage, Answer
from app.serializers import StageQuestionListSerializer, StageParentListSerializer, StageChildListSerializer

def database_debug(func):
    def inner_func(*args, **kwargs):
        reset_queries()
        results = func(*args, **kwargs)
        query_info = connection.queries
        print('function_name: {}'.format(func.__name__))
        print('query_count: {}'.format(len(query_info)))
        queries = ['{}\n'.format(query['sql']) for query in query_info]
        print('queries: \n{}'.format(''.join(queries)))
        return results
    return inner_func


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
    
