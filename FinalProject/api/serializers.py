from rest_framework import serializers


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
# serializers.py
from rest_framework import serializers
class UserFileSerializer(serializers.ModelSerializer):
    file_type = serializers.CharField(required=True)


# serializers.py
from rest_framework import serializers
from .models import DeveloperFile, DeveloperParameter

class DeveloperParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperParameter
        fields = ['id', 'name', 'param_type', 'choices', 'default']

class DeveloperFileSerializer(serializers.ModelSerializer):
    parameters = DeveloperParameterSerializer(many=True, read_only=True)

    class Meta:
        model = DeveloperFile
        fields = ['id', 'file', 'user','uploaded_at','description','name', 'parameters']
        read_only_fields = ['user']
# serializers.py
# serializers.py

class DeveloperFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperFile
        fields = ['id', 'file', 'uploaded_at','description','name']  # ✅ Only fields that exist in the model
from rest_framework import serializers
# # serializers.py
# from rest_framework import serializers
# class UserFileSerializer1(serializers.ModelSerializer):
#     extraction_id = serializers.SerializerMethodField()
#     model_used = serializers.SerializerMethodField()
#
#     class Meta:
#         model = UserFile
#         fields = ['id', 'file', 'extracted_text', 'extraction_id', 'model_used']
#
#     def get_extraction_id(self, obj):
#         last_extraction = obj.extractions.last()
#         return last_extraction.id if last_extraction else None
#
#     def get_model_used(self, obj):
#         last_extraction = obj.extractions.last()
#         return last_extraction.model_used.file.name if last_extraction else None

from rest_framework import serializers
from .models import Feedback
class FeedbackSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'username', 'feedback', 'rating', 'created_at']
# /////////////////////////////////////////////////////////////////////////////////////////////////

from .models import Manuscript, ManuscriptFile

from rest_framework import serializers
from .models import ManuscriptFile
from django.conf import settings
import os
class ManuscriptFileSerializer(serializers.ModelSerializer):
    result_image = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ManuscriptFile
        fields = ['id', 'file', 'file_type', 'uploaded_at', 'result_image', 'file_url']

    def get_result_image(self, obj):
        file_id = obj.id
        filename = f"image_{file_id}_bin.png"
        processed_path = os.path.join(settings.MEDIA_ROOT, "processed_outputs", filename)
        if os.path.exists(processed_path):
            return filename
        return None

    def get_file_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url



class ManuscriptSerializer(serializers.ModelSerializer):
    files = ManuscriptFileSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Manuscript
        fields = ['id', 'name', 'created_at', 'files', 'username']  # 🔁 removed 'user'
        read_only_fields = ['created_at']
from rest_framework import serializers
from .models import GroundFolder

class GroundFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroundFolder
        fields = ['id', 'name', 'created_at']
from rest_framework import serializers
from .models import GroundXMLFile
class GroundXMLFileSerializer(serializers.ModelSerializer):
    linked_image_name = serializers.SerializerMethodField()

    class Meta:
        model = GroundXMLFile
        fields = ['id', 'file', 'uploaded_at', 'linked_image_name']  # include it here

    def get_linked_image_name(self, obj):
        if obj.linked_image:
            return os.path.basename(obj.linked_image.file.name)
        return None
