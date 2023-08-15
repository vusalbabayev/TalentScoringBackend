from rest_framework import serializers
from userapp import models

class AnswerListSerializer(serializers.ModelSerializer):
    
    #stage_fit = serializers.CharField(source = 'get_stage_slug')
    class Meta:
        model = models.Answer
        exclude = ["questionIdd", "created_at", "updated_at", "stage_fit", "answer_weight_for_hashing"]








