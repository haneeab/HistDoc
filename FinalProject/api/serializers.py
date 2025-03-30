from rest_framework import serializers


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
# serializers.py
from rest_framework import serializers
from .models import UserFile,DeveloperFile
class UserFileSerializer(serializers.ModelSerializer):
    file_type = serializers.CharField(required=True)

    class Meta:
        model = UserFile
        fields = ['id', 'file', 'file_type', 'user']
        read_only_fields = ['user']  # ✅ Important
# serializers.py
class DeveloperFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperFile
        fields = ['id', 'file', 'file_type', 'user']
        read_only_fields = ['user']
