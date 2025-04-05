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
# serializers.py

class DeveloperFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperFile
        fields = ['id', 'file']
from rest_framework import serializers
from .models import UserFile
# serializers.py
from rest_framework import serializers
from .models import UserFile, ExtractionRecord
class UserFileSerializer1(serializers.ModelSerializer):
    extraction_id = serializers.SerializerMethodField()
    model_used = serializers.SerializerMethodField()

    class Meta:
        model = UserFile
        fields = ['id', 'file', 'extracted_text', 'extraction_id', 'model_used']

    def get_extraction_id(self, obj):
        last_extraction = obj.extractions.last()
        return last_extraction.id if last_extraction else None

    def get_model_used(self, obj):
        last_extraction = obj.extractions.last()
        return last_extraction.model_used.file.name if last_extraction else None

from rest_framework import serializers
from .models import Feedback
class FeedbackSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'username', 'feedback', 'rating', 'created_at']
