from rest_framework import serializers
from .answer_serializer import AnswerListSerializer
from userapp import models

class QuestionListSerializer(serializers.ModelSerializer):
    answers = AnswerListSerializer(many=True, read_only=True) 
    
    class Meta:
        model = models.Question
        exclude = ['created_at', 'updated_at', 'stage']



