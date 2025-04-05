from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponse
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        return Response({"message": "Login successful", "username": user.username})
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
def main(requset):
    return HttpResponse("hello")


from django.contrib.auth.models import Group, User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Ensure groups are created when the server starts
def create_default_groups():
    groups = ["Researcher", "User"]
    i=0
    for group_name in groups:
        Group.objects.get_or_create(name=group_name ,id= 1+i)
        i=i+1

create_default_groups()

# User registration API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from .serializers import RegisterUserSerializer,UserFileSerializer,DeveloperFileSerializer
from rest_framework import permissions

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(APIView):
    permission_classes = [permissions.AllowAny]  # ✅ Add this line

    serializer_class = RegisterUserSerializer

    def post(self, request, format=None):
        # Ensure the default User group exists
        group_name = "User"
        group, created = Group.objects.get_or_create(name=group_name)  # Use name instead of id

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            first_name = serializer.validated_data.get("first_name", "")
            last_name = serializer.validated_data.get("last_name", "")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": "A user with this username already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if User.objects.filter(email=email).exists():
                return Response(
                    {"error": "A user with this email already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create the user
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )

            # Assign the user to the default User group
            user.groups.add(group)  # Add the user to the group

            return Response(
                {
                    "message": "User registered successfully!",
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": "Invalid data provided.", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib.auth import login  # Add this import
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class LoginUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        identifier = request.data.get("identifier")
        password = request.data.get("password")

        if not identifier or not password:
            return Response(
                {"error": "Username/Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            if "@" in identifier:
                user = User.objects.get(email=identifier)
                username = user.username
            else:
                username = identifier
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid username/email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username/email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login(request, user)  # ✅ Start session

        # Determine user's group
        try:
            if Group.objects.get(name="User") in user.groups.all():
                return Response(
                    {
                        "message": "Login successful!",
                        "redirect": "homepage-user",
                        "user_type": "user",
                        "user": {
                            "username": user.username,
                            "email": user.email,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            elif Group.objects.get(name="Researcher") in user.groups.all():
                return Response(
                    {
                        "message": "Login successful!",
                        "redirect": "researcher-homepage",
                        "user_type": "researcher",
                        "user": {
                            "username": user.username,
                            "email": user.email,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Access denied. User group not recognized."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Group.DoesNotExist:
            return Response(
                {"error": "User groups not configured properly."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserFileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import UserFile

class UploadFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        try:
            file = request.FILES.get('file')
            file_type = request.data.get('file_type')

            # if not file or not file_type:
            #     return Response({"error": "File and file_type are required."}, status=400)

            obj = UserFile.objects.create(
                user=request.user,
                file=file,
                file_type="Image"
            )

            return Response({
                "message": "✅ File uploaded successfully!",
                "id": obj.id,
                "file_url": request.build_absolute_uri(obj.file.url),
            }, status=201)


        except Exception as e:
            return Response({"error": str(e)}, status=500)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout

class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response(
            {"message": "Logged out successfully!", "redirect": "/"},
            status=status.HTTP_200_OK
        )

from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import UserFile
from django.contrib.auth.models import User
import base64


class DebugUploadTestView(APIView):
    def get(self, request):
        try:
            # Get a user (you can change the username)
            user = User.objects.first()
            if not user:
                return Response({"error": "No user exists"}, status=400)

            # Create fake image content
            image_data = base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAUA"
                "AAAFCAYAAACNbyblAAAAHElEQVQI12P4"
                "//8/w38GIAXDIBKE0DHxgljNBAAO"
                "9TXL0Y4OHwAAAABJRU5ErkJggg=="
            )  # this is a 1x1 pixel PNG

            file = ContentFile(image_data, name="test.png")

            # Create file entry
            obj = UserFile.objects.create(
                user=user,
                file=file,
                file_type="image"
            )

            return Response({
                "message": "✅ File uploaded successfully",
                "id": obj.id,
                "url": obj.file.url,
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
# views.py
from .models import DeveloperFile

class UploadDeveloperFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get('file')
        if file:
            DeveloperFile.objects.create(user=request.user, file=file)
            return Response({'message': '✅ File uploaded successfully!'}, status=200)
        return Response({'error': '❌ No file provided.'}, status=400)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
import os
from django.conf import settings
from .models import UserFile, DeveloperFile
# from inference.inferenceVis import main as run_inference
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserFile, DeveloperFile, ExtractionRecord


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_inference_view(request, image_id):
    user = request.user
    model_id = request.data.get("model_id")

    if not model_id:
        return Response({"error": "Model ID is required."}, status=400)

    try:
        user_file = UserFile.objects.get(id=image_id, user=user)
    except UserFile.DoesNotExist:
        return Response({"error": "User image not found."}, status=404)

    try:
        model_file = DeveloperFile.objects.get(id=model_id)
    except DeveloperFile.DoesNotExist:
        return Response({"error": "Developer model not found."}, status=404)

    # ✅ Simulate inference with fake text
    random_text = random.choice([
        "Random extract: Lorem ipsum dolor sittttttttttttttttttttttttttttttttttttttttttttt amet.",
        "Extracted: The quick brown fox jumpedttttttttttttttttttttttttttttttt over the lazy dog.",
        "Test extract: AI extractedtttttttttttttttttttttttt this text.",
        "Output: Document text nottttttttttttttttttttt recognized fully.",
    ])

    # ✅ Save a new record
    ExtractionRecord.objects.create(
        user_file=user_file,
        model_used=model_file,
        extracted_text=random_text
    )

    # ✅ Update UserFile with the latest result
    user_file.extracted_text = random_text
    user_file.save()

    return Response({
        "original_image": request.build_absolute_uri(user_file.file.url),
        "output_image": request.build_absolute_uri(user_file.file.url),  # Replace with actual output path if needed
        "extracted_text": random_text,
    }, status=200)

# @api_view(['POST'])
# @permission_classes([permissions.IsAuthenticated])
# def run_inference_view(request, image_id):
#     return Response({'error': '❌ No file provided.'}, status=400)

    # try:
    #     user_file = UserFile.objects.get(id=image_id, user=request.user)
    #     image_path = user_file.file.path
    # except UserFile.DoesNotExist:
    #     return Response({"error": "User image not found."}, status=404)
    #
    # try:
    #     model_file = DeveloperFile.objects.filter(user=request.user).last()
    #     if not model_file:
    #         return Response({"error": "Model file not found."}, status=404)
    #     model_path = model_file.file.path
    # except DeveloperFile.DoesNotExist:
    #     return Response({"error": "Model file missing."}, status=404)
    #
    # output_dir = os.path.join(settings.MEDIA_ROOT, 'outputs')
    # os.makedirs(output_dir, exist_ok=True)
    #
    # output_path = os.path.join(output_dir, f"output_{user_file.id}.png")
    # try:
    #     run_inference(model_path, image_path, output_path)
    # except Exception as e:
    #     return Response({"error": str(e)}, status=500)
    #
    # return Response({
    #     "original_image": request.build_absolute_uri(user_file.file.url),
    #     "output_image": request.build_absolute_uri(
    #         os.path.join(settings.MEDIA_URL, 'outputs', f"output_{user_file.id}.png")
    #     ),
    # }, status=200)
# views.py

from .serializers import DeveloperFileListSerializer,UserFileSerializer1  # use the list serializer

class DeveloperModelListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_files = DeveloperFile.objects.filter(user=request.user)
        serializer = DeveloperFileListSerializer(user_files, many=True)
        return Response(serializer.data)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import DeveloperFile,Feedback

class DeleteDeveloperModelView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            model_file = DeveloperFile.objects.get(pk=pk, user=request.user)
            model_file.delete()
            return Response({"message": "Model deleted!"}, status=status.HTTP_200_OK)
        except DeveloperFile.DoesNotExist:
            return Response({"error": "Model not found"}, status=status.HTTP_404_NOT_FOUND)

class UserImageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        images = UserFile.objects.filter(user=user, file_type="Image")
        serializer = UserFileSerializer1(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllDeveloperModelsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_models = DeveloperFile.objects.all()
        serializer = DeveloperFileListSerializer(all_models, many=True)
        return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_feedback_view(request):
    rating = request.data.get('rating')
    feedback_text = request.data.get('feedback')
    extraction_id = request.data.get('extraction_id')

    if not (rating and feedback_text and extraction_id):
        return Response({"error": "Missing required fields."}, status=400)

    try:
        extraction = ExtractionRecord.objects.get(id=extraction_id, user_file__user=request.user)
    except ExtractionRecord.DoesNotExist:
        return Response({"error": "Extraction record not found."}, status=404)

    Feedback.objects.create(
        user=request.user,
        model=extraction.model_used,  # ✅ Pulls the correct DeveloperFile
        feedback=feedback_text,
        rating=int(rating),
    )

    return Response({"message": "✅ Feedback submitted successfully!"}, status=201)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Feedback, DeveloperFile
from .serializers import FeedbackSerializer
from django.db.models import Avg

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_model_feedbacks(request):
    model_id = request.GET.get('model_id')
    if not model_id:
        return Response({'error': 'Missing model_id'}, status=400)

    try:
        model = DeveloperFile.objects.get(id=model_id)
    except DeveloperFile.DoesNotExist:
        return Response({'error': 'Model not found'}, status=404)

    feedbacks = Feedback.objects.filter(model=model)
    avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']

    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response({
        'feedbacks': serializer.data,
        'average_rating': round(avg_rating, 2) if avg_rating else None,
        'model_name': model.file.name.split("/")[-1]
    })


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DeveloperFile, Feedback
from .serializers import FeedbackSerializer
from django.db.models import Avg

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_models_feedback_summary(request):
    all_models = DeveloperFile.objects.all()
    result = []

    for model in all_models:
        feedbacks = model.feedbacks.order_by('-created_at')[:2]
        average_rating = model.feedbacks.aggregate(avg=Avg('rating'))['avg']
        result.append({
            'model_id': model.id,
            'model_name': model.file.name,
            'average_rating': round(average_rating, 2) if average_rating else None,
            'latest_feedbacks': FeedbackSerializer(feedbacks, many=True).data
        })

    return Response(result)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg
from .models import DeveloperFile


@api_view(['GET'])
def sorted_models_by_rating(request):
    models = DeveloperFile.objects.annotate(avg_rating=Avg('feedbacks__rating')).order_by('-avg_rating')

    data = []
    for model in models:
        data.append({
            'id': model.id,
            'name': model.file.name,
            'average_rating': round(model.avg_rating or 0, 2),
        })

    return Response(data)
