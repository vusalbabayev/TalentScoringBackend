from rest_framework import serializers
from app import models

class AnswerListSerializer(serializers.ModelSerializer):
    
    stage_fit = serializers.CharField(source = 'get_stage_slug')
    class Meta:
        model = models.Answer
        exclude = ["question_id", "created_at", "updated_at"]








