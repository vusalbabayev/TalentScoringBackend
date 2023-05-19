from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from app.models import UserAccount
UserAccount=get_user_model()
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = UserAccount
        fields=('username', 'first_name', 'last_name', 'age', 'password', 'password2')
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }
    def save(self):
        user = UserAccount(
            username = self.validated_data['username'],
            age = self.validated_data['age']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"password": "Passwords do not match!"})
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)
    
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ("username", "age")