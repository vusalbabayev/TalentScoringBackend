from rest_framework import serializers
from app.serializers.answer_serializer import AnswerListSerializer
from app import models

class QuestionListSerializer(serializers.ModelSerializer):
    answers = AnswerListSerializer(many=True, read_only=True) 
    
    class Meta:
        model = models.Question
        exclude = ['created_at', 'updated_at', 'stage', 'question_dependens_on_answer']



