#from django.db.models import Prefetch
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Question
from app.serializers import QuestionListSerializer

class QuestionListApiView(APIView): 

    def get(self, request):
        question = Question.objects.prefetch_related('answers')

        serializer =  QuestionListSerializer(question, many = True)

        return Response({"questions": serializer.data})
    
class GetQuestionApiView(APIView):
    def get(self, request):
        query = Q()
        for index in request.data['data']:
            query.add(Q(question_dependens_on_answer=index), Q.OR)

        questions = Question.objects.filter(query).values("id", "question_title", "question_type")
        question_list = [question for question in questions]
        return JsonResponse({"questions": question_list})