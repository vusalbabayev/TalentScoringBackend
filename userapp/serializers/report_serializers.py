from app.models import UserProfile
from rest_framework import serializers

class ReportUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'report_file')