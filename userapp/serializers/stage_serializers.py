from app import models
from rest_framework import serializers, generics
from app.serializers.question_serializer import QuestionListSerializer
from rest_framework import permissions

class RecursiveSerializer(serializers.Serializer):
    
    def to_representation(self, instance):

        serializer=self.parent.parent.__class__(instance)

        return serializer.data
    
class StageQuestionListSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True, read_only=True) 
    
    permission_classes = [""]

    class Meta:
        model = models.Stage
        exclude = ["parent"]

class StageParentListSerializer(serializers.ModelSerializer):
    child_count = serializers.SerializerMethodField()
    stage_children = RecursiveSerializer(many = True, read_only = True)
    class Meta:
        model = models.Stage
        fields = "__all__"

    def get_child_count(self,obj):
        return obj.stage_children.count()

class StageChildListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Stage
        fields = "__all__"



# class StageQuestionListSerializer(serializers.ModelSerializer):
#     questions = QuestionListSerializer(many=True, read_only=True) 
#     stage_children=RecursiveSerializer(many=True, read_only=True)
    
#     permission_classes = [""]

#     class Meta:
#         model = models.Stage
#         exclude = ["parent"]