from rest_framework.test import APITestCase
from django.urls import reverse
from app.models import Stage
from app.serializers.stage_serializers import StageParentListSerializer
class AnswerTest(APITestCase):
    def test_parent_stage_serializer(self):
        url = reverse('parent-api')
        stage1 = Stage.objects.create(stage_name = "First Stage")
        stage2 = Stage.objects.create(stage_name = "Second Stage")
        stages = Stage.objects.all()
        response = self.client.get(url)
        expected_data = StageParentListSerializer(stages, many=True).data
        self.assertEqual(response.data, expected_data)