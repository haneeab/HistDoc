from rest_framework.decorators import api_view
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

def create_default_groups():
    groups = ["Researcher", "User"]
    i=0
    for group_name in groups:
        Group.objects.get_or_create(name=group_name ,id= 1+i)
        i=i+1

# create_default_groups()
from rest_framework.views import APIView
from .serializers import RegisterUserSerializer,DeveloperFileSerializer
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserView(APIView):
    """
      Handles user registration.
      - Validates input with serializer.
      - Checks for existing username/email.
      - Creates user and adds to 'User' group.
      - Returns success or error response.
      """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer
    def post(self, request, format=None):
        # Ensure the default User group exists
        group_name = "User"
        group, created = Group.objects.get_or_create(name=group_name)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            first_name = serializer.validated_data.get("first_name", "")
            last_name = serializer.validated_data.get("last_name", "")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
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
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user.groups.add(group)
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
    """
       Handles user login using username or email.

       - Accepts identifier (username/email) and password.
       - Authenticates user and logs them in.
       - Returns user type and redirect path based on group.
       - Supports 'User' and 'Researcher' groups.
       """
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

        login(request, user)

        # Determine user's group
        try:
            if Group.objects.get(name="User") in user.groups.all():
                return Response(
                    {
                        "message": "Login successful!",
                        "redirect": "ManuscriptListPage",
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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout

class LogoutView(APIView):
    """
       Logs out the currently authenticated user.

       - Accepts POST request.
       - Clears session and returns success message.
       """
    def post(self, request, format=None):
        logout(request)
        return Response(
            {"message": "Logged out successfully!", "redirect": "/"},
            status=status.HTTP_200_OK
        )

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

class UploadDeveloperFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        name = request.data.get('name')
        description = request.data.get('description')
        parameters_raw = request.data.get('parameters')

        print("🟢 Incoming upload:")
        print("Name:", name)
        print("Description:", description)
        print("File:", file)
        print("Parameters (raw):", parameters_raw)

        if not file:
            return Response({'error': '❌ No file provided.'}, status=400)

        # Create DeveloperFile first
        dev_file = DeveloperFile.objects.create(
            user=request.user,
            file=file,
            name=name,
            description=description
        )

        # Parse and store parameters
        try:
            parameters = json.loads(parameters_raw)
            for param in parameters:
                DeveloperParameter.objects.create(
                    model=dev_file,
                    name=param.get("name", "").strip(),
                    param_type=param.get("type", "").strip(),
                    choices=[choice.strip() for choice in param.get("choices", "").split(",") if choice.strip()] or None,
                    default=param.get("default", "").strip()
                )
        except Exception as e:
            dev_file.delete()  # rollback if params fail
            return Response({'error': f'❌ Invalid parameters format. {str(e)}'}, status=400)

        return Response({'message': '✅ File uploaded successfully!', 'id': dev_file.id}, status=200)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import DeveloperFileListSerializer  # use the list serializer

class DeveloperModelListView(APIView):
    """
        Uploads a Python model file and its parameters.

        - Accepts multipart POST with file, name, description, and parameters (as JSON string).
        - Saves the DeveloperFile and linked DeveloperParameter entries.
        - Returns success message or error if parsing fails.
        """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_files = DeveloperFile.objects.filter(user=request.user)
        serializer = DeveloperFileListSerializer(user_files, many=True)
        return Response(serializer.data)
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

class DeleteDeveloperModelView(APIView):
    """
       Deletes a developer model file by its ID (pk).

       - Only deletes if the model belongs to the authenticated user.
       - Returns 404 if not found.
       """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            model_file = DeveloperFile.objects.get(pk=pk, user=request.user)
            model_file.delete()
            return Response({"message": "Model deleted!"}, status=status.HTTP_200_OK)
        except DeveloperFile.DoesNotExist:
            return Response({"error": "Model not found"}, status=status.HTTP_404_NOT_FOUND)


class AllDeveloperModelsView(APIView):
    """
       Returns a list of all developer models (regardless of user).

       - Requires authentication.
       - Returns serialized data of all DeveloperFile objects.
       """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_models = DeveloperFile.objects.all()
        serializer = DeveloperFileListSerializer(all_models, many=True)
        return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_feedback_view(request):
    """
       Allows authenticated users to submit feedback for a model.

       - Requires model_id, rating, and feedback text.
       - Validates existence of the model.
       - Saves feedback linked to the user and model.
       """
    print(" Incoming data:", request.data)  # Add this line for debugging

    rating = request.data.get('rating')
    feedback_text = request.data.get('feedback')
    model_id = request.data.get('model_id')

    if not (rating and feedback_text and model_id):
        return Response({"error": "Missing required fields."}, status=400)

    try:
        model = DeveloperFile.objects.get(id=model_id)
    except DeveloperFile.DoesNotExist:
        return Response({"error": "Model not found."}, status=404)

    Feedback.objects.create(
        user=request.user,
        model=model,
        feedback=feedback_text,
        rating=int(rating),
    )

    return Response({"message": "✅ Feedback submitted successfully!"}, status=201)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_model_feedbacks(request):
    """
        Returns all feedback for a specific model.

        - Requires ?model_id= in the query params.
        - Returns feedback list, average rating, and model name.
        """
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

from django.db.models import Avg

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DeveloperFile, Feedback
from .serializers import FeedbackSerializer
from django.db.models import Avg

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_models_feedback_summary(request):
    """
       Returns a summary of all models.

       - Includes model ID, name, average rating, and 2 latest feedbacks.
       """
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
    """
       Returns all models sorted by average feedback rating (highest first).
       """
    models = DeveloperFile.objects.annotate(avg_rating=Avg('feedbacks__rating')).order_by('-avg_rating')

    data = []
    for model in models:
        data.append({
            'id': model.id,
            'name': model.file.name,
            'average_rating': round(model.avg_rating or 0, 2),
        })

    return Response(data)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Manuscript, ManuscriptFile
from .serializers import ManuscriptSerializer, ManuscriptFileSerializer
# /////////////////////////////////////////////////////// tilll here
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manuscript_list_create(request):
    """
      GET: Return all manuscripts belonging to the authenticated user.
      POST: Create a new manuscript for the authenticated user.
      """
    if request.method == 'GET':
        manuscripts = Manuscript.objects.filter(user=request.user)
        serializer = ManuscriptSerializer(manuscripts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ManuscriptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_manuscript(request, pk):
    """
     Delete a manuscript by ID if it belongs to the authenticated user.
     Returns 404 if the manuscript does not exist.
     """
    try:
        manuscript = Manuscript.objects.get(pk=pk, user=request.user)
    except Manuscript.DoesNotExist:
        return Response({"error": "Manuscript not found"}, status=404)

    manuscript.delete()
    return Response({"message": "Manuscript deleted"}, status=204)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manuscript_files(request, manuscript_id):
    """
        GET: Return all files associated with the specified manuscript (if owned by user).
        POST: Upload a new file to the specified manuscript.
        """
    try:
        manuscript = Manuscript.objects.get(id=manuscript_id, user=request.user)
    except Manuscript.DoesNotExist:
        return Response({'error': 'Manuscript not found'}, status=404)

    if request.method == 'GET':
        files = manuscript.files.all()
        serializer = ManuscriptFileSerializer(files, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        file = request.FILES.get('file')
        file_type = request.data.get('file_type', 'image')

        if not file:
            return Response({'error': 'No file uploaded'}, status=400)

        manuscript_file = ManuscriptFile.objects.create(
            manuscript=manuscript,
            file=file,
            file_type=file_type
        )
        serializer = ManuscriptFileSerializer(manuscript_file)
        return Response(serializer.data, status=201)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_manuscript_file(request, file_id):
    """
       Delete a manuscript file by ID if it belongs to a manuscript owned by the user.
       Returns 404 if the file is not found.
       """
    try:
        file = ManuscriptFile.objects.get(pk=file_id, manuscript__user=request.user)
    except ManuscriptFile.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

    file.delete()
    return Response({"message": "File deleted"}, status=204)
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def rename_file(request, file_id):
    """
        Rename an uploaded manuscript file.

        Only the owner of the file can perform this action.
        The new name is provided in the request body as 'new_name'.
        The file is renamed both on the filesystem and in the database.
        Returns the new file path and accessible URL.
        """
    try:
        file_obj = ManuscriptFile.objects.get(pk=file_id, manuscript__user=request.user)
    except ManuscriptFile.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

    new_name = request.data.get("new_name")
    if not new_name:
        return Response({"error": "New name is required"}, status=400)

    # Get the current full path
    old_path = file_obj.file.path
    file_ext = os.path.splitext(old_path)[1]  # Keep the extension
    new_filename = new_name + file_ext

    new_relative_path = os.path.join("manuscript_files", new_filename)
    new_full_path = os.path.join(settings.MEDIA_ROOT, new_relative_path)

    # Rename the file on disk
    try:
        os.rename(old_path, new_full_path)
    except Exception as e:
        return Response({"error": f"Rename failed: {str(e)}"}, status=500)

    # Update the file field in the model
    file_obj.file.name = new_relative_path
    file_obj.save()

    return Response({
        "message": "File renamed successfully",
        "new_file_path": file_obj.file.name,
        "new_url": request.build_absolute_uri(file_obj.file.url)
    })

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def rename_manuscript(request, pk):
    """
       Rename a manuscript owned by the authenticated user.

       Expects a 'new_name' in the request body.
       Returns a success message and the updated name if successful.
       """
    try:
        manuscript = Manuscript.objects.get(pk=pk, user=request.user)
    except Manuscript.DoesNotExist:
        return Response({"error": "Manuscript not found"}, status=404)

    new_name = request.data.get("new_name")
    if not new_name:
        return Response({"error": "New name is required"}, status=400)

    manuscript.name = new_name
    manuscript.save()
    return Response({"message": "Manuscript renamed", "new_name": new_name})
from django.http import FileResponse
import os

def serve_manuscript_image(request, filename):
    """
       Serve an image file from the 'manuscript_files' directory.

       Looks for the image by filename in the MEDIA_ROOT/manuscript_files/ folder.
       Returns the image with the correct content type if found.
       Raises a 404 error if the file does not exist.
       """
    file_path = os.path.join(settings.MEDIA_ROOT, 'manuscript_files', filename)

    if os.path.exists(file_path):
        ext = filename.lower().split('.')[-1]
        content_type = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif"
        }.get(ext, "application/octet-stream")

        return FileResponse(open(file_path, 'rb'), content_type=content_type)
    else:
        raise Http404("Image not found")

def serve_uploaded_image(request, filename):
    """
          Serve an image file from the 'manuscript_files' directory.

          Looks for the image by filename in the MEDIA_ROOT/manuscript_files/ folder.
          Returns the image with the correct content type if found.
          Raises a 404 error if the file does not exist.
          """
    file_path = os.path.join(settings.MEDIA_ROOT, 'manuscript_files', filename)

    if not os.path.exists(file_path):
        raise Http404("Image not found")

    ext = filename.lower().split('.')[-1]
    content_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif"
    }.get(ext, "application/octet-stream")

    return FileResponse(open(file_path, 'rb'), content_type=content_type)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_manuscript_files(request, manuscript_id):
    """
       Retrieve all files related to a specific manuscript owned by the authenticated user.

       Returns a list of serialized files.
       Responds with 404 if the manuscript is not found or does not belong to the user.
       """
    try:
        manuscript = Manuscript.objects.get(id=manuscript_id, user=request.user)
    except Manuscript.DoesNotExist:
        return Response({"error": "Manuscript not found"}, status=404)

    files = manuscript.files.all()
    serializer = ManuscriptFileSerializer(files, many=True, context={"request": request})
    return Response(serializer.data)


def serve_image_by_filename(request, filename):
    """
          Serve an image file from the 'manuscript_files' directory.

          Looks for the image by filename in the MEDIA_ROOT/manuscript_files/ folder.
          Returns the image with the correct content type if found.
          Raises a 404 error if the file does not exist.
          """
    file_path = os.path.join(settings.MEDIA_ROOT, 'manuscript_files', filename)
    if not os.path.exists(file_path):
        raise Http404("Image not found")
    ext = filename.lower().split('.')[-1]
    content_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif"
    }.get(ext, "application/octet-stream")
    return FileResponse(open(file_path, 'rb'), content_type=content_type)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Manuscript, ManuscriptFile
from .serializers import ManuscriptFileSerializer,GroundFolderSerializer,GroundXMLFileSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_files(request, manuscript_id):
    """
        Fetch all files associated with a given manuscript belonging to the logged-in user.

        Returns a list of files if found.
        Responds with 404 if the manuscript does not exist or is not owned by the user.
        """
    manuscript = Manuscript.objects.get(pk=manuscript_id, user=request.user)
    files = manuscript.files.all()
    serializer = ManuscriptFileSerializer(files, many=True, context={'request': request})
    return Response(serializer.data)


def serve_image(request, filename):
    path = os.path.join(settings.MEDIA_ROOT, 'manuscript_files', filename)
    if os.path.exists(path):
        return FileResponse(open(path, 'rb'), content_type='image/jpeg')
    raise Http404("Image not found")

from rest_framework.permissions import IsAuthenticated
# ////////////////////////////////////////////////////////////////////////////////tellll here
from .models import GroundFolder, GroundXMLFile, Manuscript
from rest_framework.decorators import api_view, permission_classes
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def manuscript_grounds(request, manuscript_id):
    """
       GET: Returns all ground folders associated with the specified manuscript.
       POST: Creates a new ground folder under the given manuscript using the 'name' provided.
       Requires authentication and manuscript ownership.
       """
    try:
        manuscript = Manuscript.objects.get(id=manuscript_id, user=request.user)
        print(" Manuscript found:", manuscript.name)
    except Manuscript.DoesNotExist:
        print(" Manuscript not found or not owned by user")
        return Response({"error": "Manuscript not found"}, status=404)

    if request.method == 'GET':
        folders = manuscript.ground_folders.all()
        serializer = GroundFolderSerializer(folders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        name = request.data.get('name')
        if not name:
            return Response({"error": "Folder name is required"}, status=400)

        folder = GroundFolder.objects.create(
            manuscript=manuscript,
            name=name,
            created_by=request.user.username
        )
        serializer = GroundFolderSerializer(folder)
        return Response(serializer.data)

    return Response({"error": "Method not allowed"}, status=405)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ground_folder_xmls(request, folder_id):
    """
        GET: Lists all XML files under the specified ground folder.
        POST: Uploads a new XML file and links it to a manuscript image whose base name matches the provided 'base_name'.
        Requires authentication.
        """
    try:
        folder = GroundFolder.objects.get(id=folder_id)
    except GroundFolder.DoesNotExist:
        return Response({"error": "Folder not found"}, status=404)

    if request.method == 'GET':
        xmls = folder.xml_files.all()
        serializer = GroundXMLFileSerializer(xmls, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        file = request.FILES.get('file')
        base_name = request.data.get('base_name')  # from FormData

        if not file or not base_name:
            return Response({'error': 'Missing file or base_name'}, status=400)

        base_name = base_name.strip().lower()
        manuscript = folder.manuscript

        # Force: Match base name with any image filename stem in manuscript
        linked_image = None
        for img in manuscript.files.all():
            img_stem = Path(img.file.name).stem.lower()
            if img_stem == base_name:
                linked_image = img
                break

        if not linked_image:
            return Response({'error': f"No image file matches '{base_name}' in this manuscript."}, status=400)

        # Create the XML file and link the image (if your model supports that)
        xml_file = GroundXMLFile.objects.create(
            folder=folder,
            file=file,
            linked_image=linked_image  # Only if your model supports this
        )

        serializer = GroundXMLFileSerializer(xml_file, context={'request': request})
        return Response(serializer.data, status=201)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ground_folder(request, folder_id):
    """
        Deletes the specified ground folder if it belongs to a manuscript owned by the authenticated user.
        All associated XML files are also deleted due to cascading.
        """
    try:
        folder = GroundFolder.objects.get(id=folder_id, manuscript__user=request.user)
    except GroundFolder.DoesNotExist:
        return Response({"error": "Folder not found"}, status=404)

    folder.delete()  # Will also delete related GroundXMLFile due to ForeignKey
    return Response({"success": True, "message": "Folder deleted successfully!"}, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ground_xml(request, xml_id):
    """
        Deletes the specified XML file from a ground folder.
        Only works if the XML file exists.
        """
    try:
        xml_file = GroundXMLFile.objects.get(id=xml_id)
    except GroundXMLFile.DoesNotExist:
        return Response({"error": "XML not found"}, status=404)

    xml_file.delete()
    return Response({"success": True})
# //////////////////////////////////////////////////////////////////
from django.utils.text import slugify
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import GroundXMLFile
from .serializers import GroundXMLFileSerializer
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def rename_ground_xml(request, xml_id):
    """
        Renames a Ground XML file, ensuring the new name matches the base name of an image in the same manuscript.
        Reconnects the XML file to the matching image and renames the physical file on disk.
        """
    try:
        xml_file = GroundXMLFile.objects.get(id=xml_id)
    except GroundXMLFile.DoesNotExist:
        return Response({"error": "XML not found"}, status=404)

    new_name = request.data.get("new_name")
    if not new_name:
        return Response({"error": "New name required"}, status=400)

    # Check against image names in the same manuscript
    base_name = Path(new_name).stem.strip().lower()
    manuscript = xml_file.folder.manuscript
    image_names = [Path(f.file.name).stem.lower() for f in manuscript.files.all()]

    if base_name not in image_names:
        return Response({
            "error": f"New name must match the base name of an image in the manuscript (e.g. {', '.join(image_names)})"
        }, status=400)

    # Reconnect the linked image
    linked_image = None
    for f in manuscript.files.all():
        if Path(f.file.name).stem.lower() == base_name:
            linked_image = f
            break

    old_path = xml_file.file.name
    ext = Path(old_path).suffix
    safe_name = slugify(new_name) + ext
    new_path = f"ground_xmls/{safe_name}"

    if old_path == new_path:
        return Response({"message": "Name unchanged"})

    content = xml_file.file.read()
    xml_file.file.close()
    default_storage.delete(old_path)

    xml_file.file.name = new_path
    xml_file.linked_image = linked_image  # 🔗 Reconnect
    default_storage.save(new_path, ContentFile(content))
    xml_file.save()

    serializer = GroundXMLFileSerializer(xml_file, context={'request': request})
    return Response(serializer.data)
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def annotator_view(request, xml_id):
    """
       Handles XML annotation editing:
       - GET: Returns the XML content as a string for the annotator to load.
       - PATCH: Saves new XML content to the file, overwriting the old one.
       """
    try:
        xml_file = GroundXMLFile.objects.get(id=xml_id)
    except GroundXMLFile.DoesNotExist:
        return Response({"error": "XML not found"}, status=404)

    if request.method == 'GET':
        content = xml_file.file.read().decode('utf-8')
        xml_file.file.seek(0)
        return Response({"xml": content})

    if request.method == 'PATCH':
        new_content = request.data.get("xml")
        if not new_content:
            return Response({"error": "No XML content provided"}, status=400)

        old_path = xml_file.file.name  # example: "ground_xmls/example1.xml"
        filename = Path(old_path).name
        new_path = f"ground_xmls/{filename}"  # Ensure it's only one layer

        default_storage.delete(old_path)

        xml_file.file.name = new_path
        default_storage.save(new_path, ContentFile(new_content))
        xml_file.save()

        return Response({"message": "XML updated successfully"})
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def rename_ground_folder(request, folder_id):
    """
        Renames a Ground Folder (which groups XML files) by updating its `name` field.
        Requires a new name in the request body.
        """
    try:
        folder = GroundFolder.objects.get(id=folder_id)
    except GroundFolder.DoesNotExist:
        return Response({"error": "Folder not found"}, status=404)

    new_name = request.data.get("new_name")
    if not new_name:
        return Response({"error": "New name required"}, status=400)

    folder.name = new_name
    folder.save()

    return Response({"id": folder.id, "name": folder.name, "created_at": folder.created_at})

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# /////////////////////////////////////////////////////////////////////////////
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def run_uploaded_script_on_image(request, file_id):
    """
       Executes a developer-uploaded Python script on a specific manuscript image.

       - Requires `model_id` in POST data to specify the developer script (.py).
       - Optional `parameters` dictionary can be passed to the script.
       - The image is identified by `file_id` and must belong to the authenticated user.
       - The output is saved to `processed_outputs/` and returned as a URL.

       Returns:
           - 200 with `output_image` URL on success
           - 404 if image or model not found
           - 400 for invalid parameters
           - 500 if script execution fails
       """
    print(f"Request received for file_id: {file_id}")

    try:
        image_file = ManuscriptFile.objects.get(id=file_id, file_type="image", manuscript__user=request.user)
        print(f"Found image file: {image_file}")
    except ManuscriptFile.DoesNotExist:
        return Response({"error": "Image not found"}, status=404)

    try:
        model = DeveloperFile.objects.get(id=request.data.get("model_id"))
        print(f"Using model file: {model}")
    except DeveloperFile.DoesNotExist:
        return Response({"error": "Model not found"}, status=404)

    parameters = request.data.get("parameters", {})
    print(f"Received parameters: {parameters}")
    if not isinstance(parameters, dict):
        return Response({"error": "Invalid parameters format"}, status=400)

    image_path = os.path.join(settings.MEDIA_ROOT, image_file.file.name)
    script_path = os.path.join(settings.MEDIA_ROOT, model.file.name)
    output_dir = os.path.join(settings.MEDIA_ROOT, 'processed_outputs')
    os.makedirs(output_dir, exist_ok=True)
    output_file_name = f"image_{file_id}_bin.png"
    output_path = os.path.join(output_dir, output_file_name)

    command = [sys.executable, script_path, image_path]
    for key, value in parameters.items():
        command.append(str(value))
    command += ['--output', output_path]

    print(f"Executing command: {command}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Script failed with error: {e}")
        return Response({"error": "Script execution failed", "details": str(e)}, status=500)

    output_url = request.build_absolute_uri(f"/api/media/processed/{output_file_name}")
    return Response({"success": True, "output_image": output_url})
def serve_processed_image(request, filename):
    """
    give the output images of the model
        """
    path = os.path.join(settings.MEDIA_ROOT, "processed_outputs", filename)
    if os.path.exists(path):
        return FileResponse(open(path, 'rb'), content_type='image/png')
    raise Http404("Processed image not found")
# ///////////////////////////////////////////////////////////done
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_developer_models(request):
    """
       Returns a list of all developer models available in the system.

       Only authenticated users can access this endpoint.
       Useful for allowing researchers to choose from all uploaded models.
       """
    from .models import DeveloperFile
    from .serializers import DeveloperFileSerializer

    models = DeveloperFile.objects.all()
    serializer = DeveloperFileSerializer(models, many=True)
    return Response(serializer.data)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ManuscriptFile
from .serializers import ManuscriptFileSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_manuscript_file(request, file_id):
    """
        Retrieves a specific manuscript file (image or otherwise) by its ID,
        only if the file belongs to the currently authenticated user.
        """
    try:
        file = ManuscriptFile.objects.get(id=file_id, manuscript__user=request.user)
    except ManuscriptFile.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

    serializer = ManuscriptFileSerializer(file, context={'request': request})
    return Response(serializer.data)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.files.base import ContentFile
from pathlib import Path
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def annotate_model_file(request, model_id):
    """
        Allows a developer to view (GET) or update (PATCH) the contents of a model (.py file).

        - GET returns the source code of the script.
        - PATCH replaces the file content with new source code.
        """
    try:
        model = DeveloperFile.objects.get(id=model_id, user=request.user)
    except DeveloperFile.DoesNotExist:
        return Response({"error": "Model not found."}, status=404)

    if request.method == 'GET':
        content = model.file.read().decode('utf-8')
        model.file.seek(0)
        return Response({"code": content})

    if request.method == 'PATCH':
        new_code = request.data.get("code")
        if not new_code:
            return Response({"error": "No code provided."}, status=400)

        # Save new content under the same filename
        old_path = model.file.name
        filename = Path(old_path).name
        new_path = f"researcher_files/{filename}"

        default_storage.delete(old_path)
        model.file.name = new_path
        default_storage.save(new_path, ContentFile(new_code))
        model.save()

        return Response({"message": "Model updated successfully."})
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_developer_model(request, model_id):
    """
       Allows a developer to update the name and description of their model.

       Only the owner (authenticated user) can update their model.
       Returns the updated model information.
       """
    try:
        model = DeveloperFile.objects.get(id=model_id, user=request.user)
    except DeveloperFile.DoesNotExist:
        return Response({"error": "Model not found."}, status=404)

    name = request.data.get("name")
    description = request.data.get("description")

    if name is not None:
        model.name = name.strip()
    if description is not None:
        model.description = description.strip()
    model.save()
    return Response({
        "id": model.id,
        "name": model.name,
        "description": model.description,
        "message": "Model updated successfully"
    })
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def developer_model_parameters_view(request, model_id):
    """
       - GET: Retrieves all parameters for a developer's model.
       - PATCH: Replaces the model's parameters with a new set.

       Only the model owner can access and modify the parameters.
       """
    try:
        model = DeveloperFile.objects.get(id=model_id, user=request.user)
    except DeveloperFile.DoesNotExist:
        return Response({'error': 'Model not found'}, status=404)

    if request.method == 'GET':
        params = DeveloperParameter.objects.filter(model=model)
        return Response([
            {
                'name': p.name,
                'param_type': p.param_type,
                'choices': ",".join(p.choices) if p.choices else "",
                'default': p.default
            } for p in params
        ])

    if request.method == 'PATCH':
        DeveloperParameter.objects.filter(model=model).delete()
        parameters = request.data.get("parameters", [])
        for param in parameters:
            DeveloperParameter.objects.create(
                model=model,
                name=param.get("name"),
                param_type=param.get("param_type"),
                choices=[c.strip() for c in param.get("choices", "").split(",")] if param.get("choices") else None,
                default=param.get("default", "")
            )
        return Response({'message': 'Parameters updated'})
#     ////////////////////////////////////////////////////////
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import DeveloperFile, DeveloperParameter

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_model_parameters(request, model_id):
    """
        Retrieves all parameters of a specific developer model by ID.

        Useful for public or cross-user viewing when ownership is not enforced.
        """
    try:
        developer_file = DeveloperFile.objects.get(pk=model_id)
    except DeveloperFile.DoesNotExist:
        return Response({"error": "Model not found"}, status=404)

    parameters = developer_file.parameters.all()
    serialized = []
    for p in parameters:
        serialized.append({
            "name": p.name,
            "param_type": p.param_type,
            "default": p.default,
            "choices": p.choices if p.choices else []
        })

    return Response(serialized)

from django.core.files.storage import default_storage

import sys
import json
import uuid
import subprocess
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# ////////////////////////////////////////////////////////////// done
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def developer_test_model(request):
    """
       Executes a developer-uploaded Python script on a specific manuscript image.

       - Requires `model_id` in POST data to specify the developer script (.py).
       - Optional `parameters` dictionary can be passed to the script.
       - The image is identified by `file_id` and must belong to the authenticated user.
       - The output is saved to `processed_outputs/` and returned as a URL.

       Returns:
           - 200 with `output_image` URL on success
           - 404 if image or model not found
           - 400 for invalid parameters
           - 500 if script execution fails
       """
    model_id = request.data.get("model_id")
    image = request.FILES.get("image")
    raw_params = request.data.get("parameters", "{}")

    try:
        params = json.loads(raw_params) if isinstance(raw_params, str) else raw_params
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON for parameters"}, status=400)

    if not model_id or not image:
        return Response({"error": "Missing model ID or image"}, status=400)

    try:
        model = DeveloperFile.objects.get(id=model_id)
    except DeveloperFile.DoesNotExist:
        return Response({"error": "Model not found"}, status=404)

    # Save the uploaded image temporarily
    unique_name = uuid.uuid4().hex + "_" + image.name
    input_path = os.path.join(settings.MEDIA_ROOT, 'temp_inputs', unique_name)
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    with open(input_path, 'wb+') as f:
        for chunk in image.chunks():
            f.write(chunk)

    input_url = f"/api/media/temp_inputs/{unique_name}"

    # Define output path
    output_name = "output_" + unique_name
    output_path = os.path.join(settings.MEDIA_ROOT, 'temp_outputs', output_name)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result_url = f"/api/media/temp_outputs/{output_name}"
    script_path = os.path.join(settings.MEDIA_ROOT, model.file.name)
    cmd = [sys.executable, script_path, input_path]
    if params:
        first_key = list(params.keys())[0]
        cmd.append(str(params[first_key]))

    # Add remaining parameters as --key value
    for key, value in list(params.items())[1:]:
        cmd.append(f"--{key}")
        cmd.append(str(value))

    cmd.extend(["--output", output_path])

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        return Response({"error": "Script execution failed", "details": str(e)}, status=500)

    return Response({
        "success": True,
        "result_image": request.build_absolute_uri(result_url),
        "input_image": request.build_absolute_uri(input_url)
    })
from django.http import FileResponse, Http404
from django.conf import settings
import os

def serve_tmp_input_image(request, filename):
    """
    return the images for test model for the develper
       """
    path = os.path.join(settings.MEDIA_ROOT, "temp_inputs", filename)
    if os.path.exists(path):
        return FileResponse(open(path, 'rb'), content_type='image/png')
    raise Http404("Temp input image not found")
def serve_tmp_output_image(request, filename):
    """
       return the images for test model for the develper
    """
    path = os.path.join(settings.MEDIA_ROOT, "temp_outputs", filename)
    if os.path.exists(path):
        return FileResponse(open(path, 'rb'), content_type='image/png')
    raise Http404("Temp output image not found")
