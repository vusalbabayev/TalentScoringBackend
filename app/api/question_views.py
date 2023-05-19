from rest_framework.response import Response
from django.db.models import Prefetch
from rest_framework.views import APIView
from app.models import Question
from app.serializers import QuestionListSerializer

class QuestionListApiView(APIView):

    def get(self, request):
        question = Question.objects.prefetch_related('answers')

        serializer =  QuestionListSerializer(question, many = True)

        return Response({"questions": serializer.data})