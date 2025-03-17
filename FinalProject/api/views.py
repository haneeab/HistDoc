from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
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
from .serializers import RegisterUserSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(APIView):
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

class LoginUserView(APIView):
    def post(self, request, format=None):
        identifier = request.data.get("identifier")  # Accepts email or username
        password = request.data.get("password")

        if not identifier or not password:
            return Response(
                {"error": "Username/Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Determine if the identifier is an email
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

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Invalid username/email or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user belongs to the "User" group
        if user.groups.filter(name="User").exists():
            return Response(
                {
                    "message": "Login successful!",
                    "redirect": "/homepage-user",  # Frontend route for HomepageUser
                    "user": {
                        "username": user.username,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )

        # If the user is not in the "User" group
        return Response(
            {"error": "Access denied. Only users in the 'User' group can log in."},
            status=status.HTTP_403_FORBIDDEN,
        )
# 1111111111111111111111111111111111111111111111111111
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import UserFile
from .serializers import UserFileSerializer

class UploadFileView(APIView):
    # permission_classes = [permissions.IsAuthenticated]  # Only allow authenticated users

    def post(self, request, format=None):
        # Include the authenticated user in the data
        data = request.data.copy()
        data['user'] = request.user.id  # Automatically associate the file with the logged-in user

        serializer = UserFileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "File uploaded successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ListUserFilesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        files = UserFile.objects.filter(user=user)
        serializer = UserFileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import UserFile

class UploadFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        uploaded_file = request.FILES.get("file")

        if not uploaded_file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Determine file type
        if uploaded_file.content_type.startswith("image"):
            file_type = "image"
        elif uploaded_file.content_type == "application/pdf":
            file_type = "pdf"
        else:
            return Response(
                {"error": "Unsupported file type. Only images and PDFs are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_file = UserFile.objects.create(user=user, file=uploaded_file, file_type=file_type)
        return Response(
            {"message": "File uploaded successfully!", "id": user_file.id, "file_type": file_type},
            status=status.HTTP_201_CREATED,
        )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from django.shortcuts import redirect

class LogoutView(APIView):
    def post(self, request, format=None):
        # Logout the user
        logout(request)
        # Redirect to the home page
        return Response(
            {"message": "Logged out successfully!", "redirect": ""},
            status=status.HTTP_200_OK
        )

