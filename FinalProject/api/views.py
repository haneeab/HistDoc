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

# Function to create default groups
def create_default_groups():
    groups = ["Researcher", "User"]
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

# Ensure groups are created when the server starts
create_default_groups()

# User registration API
class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        group_name = request.data.get("group")  # Either 'Researcher' or 'User'

        if not username or not password or not group_name:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User.objects.create_user(username=username, password=password)

        # Assign user to group
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist:
            return Response({"error": f"Group '{group_name}' does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "User registered and added to group successfully!"}, status=status.HTTP_201_CREATED)
