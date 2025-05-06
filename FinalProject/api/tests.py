from django.test import TestCase
from django.db.models import Avg

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    DeveloperFile, DeveloperParameter, Feedback,
    Manuscript, ManuscriptFile, GroundFolder, GroundXMLFile
)
from django.core.files.uploadedfile import SimpleUploadedFile

class ModelTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='pass')

    def test_create_developer_file(self):
        file = SimpleUploadedFile("script.py", b"print('hello')")
        dev_file = DeveloperFile.objects.create(user=self.user, file=file, name="Test Script")
        self.assertEqual(dev_file.name, "Test Script")
        self.assertEqual(dev_file.user.username, "testuser")

    def test_add_parameter_to_model(self):
        file = SimpleUploadedFile("script.py", b"print('hello')")
        dev_file = DeveloperFile.objects.create(user=self.user, file=file)
        param = DeveloperParameter.objects.create(
            model=dev_file, name="method", param_type="string", choices=["otsu", "adaptive"], default="otsu"
        )
        self.assertEqual(param.default, "otsu")

    def test_feedback_creation(self):
        file = SimpleUploadedFile("script.py", b"print('hello')")
        dev_file = DeveloperFile.objects.create(user=self.user, file=file)
        feedback = Feedback.objects.create(user=self.user, model=dev_file, rating=5, feedback="Great model!")
        self.assertEqual(feedback.rating, 5)
        # self.assertEqual(str(feedback), "testuser → researcher_files/script.py (5)")

    def test_manuscript_file_upload(self):
        manuscript = Manuscript.objects.create(name="Book1", user=self.user)
        file = SimpleUploadedFile("page1.png", b"image data")
        mf = ManuscriptFile.objects.create(manuscript=manuscript, file=file, file_type="image")
        self.assertEqual(mf.file_type, "image")

    def test_ground_folder_and_xml(self):
        manuscript = Manuscript.objects.create(name="Book1", user=self.user)
        folder = GroundFolder.objects.create(manuscript=manuscript, name="GT Folder", created_by="admin")
        file = SimpleUploadedFile("annotation.xml", b"<xml></xml>", content_type="text/xml")
        xml_file = GroundXMLFile.objects.create(folder=folder, file=file)
        self.assertEqual(xml_file.file.name.endswith(".xml"), True)
 # ////////////////////////////////////////////////////////////////////////////
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class RegisterUserViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')  # Make sure your URL name is 'register'

    def test_register_user_success(self):
        """
        Should create a new user with valid data.
        """
        data = {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "new@example.com",
            "password": "StrongPass123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "newuser")

    def test_register_existing_username(self):
        """
        Should return 400 if username already exists.
        """
        User.objects.create_user(username="newuser", email="existing@example.com", password="testpass")
        data = {
            "username": "newuser",
            "email": "unique@example.com",
            "password": "StrongPass123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_register_existing_email(self):
        """
        Should return 400 if email already exists.
        """
        User.objects.create_user(username="uniqueuser", email="test@example.com", password="testpass")
        data = {
            "username": "newuser",
            "email": "test@example.com",
            "password": "StrongPass123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_register_invalid_data(self):
        """
        Should return 400 if data is invalid (e.g., short password).
        """
        data = {
            "username": "",
            "email": "invalid",
            "password": "123"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("details", response.data)
# ///////////////////////////////////////////////////////////////
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class LoginLogoutViewTests(APITestCase):
    def setUp(self):
        # Create groups
        self.user_group = Group.objects.create(name="User")
        self.researcher_group = Group.objects.create(name="Researcher")

        # Create regular user
        self.user = User.objects.create_user(username="user1", email="user1@example.com", password="StrongPass123")
        self.user.groups.add(self.user_group)

        # Create researcher
        self.researcher = User.objects.create_user(username="res1", email="res1@example.com", password="StrongPass123")
        self.researcher.groups.add(self.researcher_group)

        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

    def test_login_with_username_success(self):
        data = {"identifier": "user1", "password": "StrongPass123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_type"], "user")

    def test_login_with_email_success(self):
        data = {"identifier": "res1@example.com", "password": "StrongPass123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_type"], "researcher")

    def test_login_invalid_password(self):
        data = {"identifier": "user1", "password": "WrongPass"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_login_missing_fields(self):
        data = {"identifier": "", "password": ""}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_unknown_user(self):
        data = {"identifier": "unknown@example.com", "password": "whatever"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_success(self):
        self.client.login(username="user1", password="StrongPass123")
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
# # ///////////////////////////////////////////////////////////////////
import io
import json
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.conf import settings

class UploadDeveloperFileViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="devuser", password="StrongPass123")
        self.url = reverse("upload-developer-file")

    def test_upload_valid_file_and_parameters(self):
        self.client.login(username="devuser", password="StrongPass123")

        # Create a simple .py file in memory
        dummy_file = SimpleUploadedFile("model.py", b"print('Hello')", content_type="text/x-python")

        # Valid parameters as JSON string
        parameters = json.dumps([
            {"name": "method", "type": "string", "choices": "otsu,adaptive", "default": "otsu"},
            {"name": "threshold", "type": "float", "choices": "", "default": "0.5"}
        ])

        data = {
            "file": dummy_file,
            "name": "Sample Model",
            "description": "This is a test upload.",
            "parameters": parameters
        }

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertIn("id", response.data)

    def test_upload_without_file(self):
        self.client.login(username="devuser", password="StrongPass123")
        response = self.client.post(self.url, {"name": "No File", "parameters": "[]"}, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    def test_upload_invalid_parameters_format(self):
        self.client.login(username="devuser", password="StrongPass123")
        dummy_file = SimpleUploadedFile("model.py", b"print('bad')", content_type="text/x-python")

        data = {
            "file": dummy_file,
            "name": "Bad Param",
            "description": "",

            "parameters": "not-a-json"
        }

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
# /////////////////////////////////////
class AllDeveloperModelsViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dev1", password="pass1234")
        self.client.login(username="dev1", password="pass1234")
        DeveloperFile.objects.create(user=self.user, name="Model 1", file="file.py", description="desc")

    def test_get_all_developer_models(self):
        url = reverse('all-developer-models')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
# /////////////////////////////////
class DeleteDeveloperModelViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dev1", password="pass1234")
        self.other = User.objects.create_user(username="other", password="pass1234")
        self.client.login(username="dev1", password="pass1234")
        self.own_model = DeveloperFile.objects.create(user=self.user, name="Mine", file="mine.py", description="d")
        self.other_model = DeveloperFile.objects.create(user=self.other, name="Not Mine", file="other.py", description="d")

    def test_delete_own_model(self):
        url = f"/delete-developer-model/{self.own_model.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_model_not_owned(self):
        self.client.logout()
        self.client.login(username="dev1", password="pass1234")  # dev1 doesn't own the other model
        url = f"/delete-developer-model/{self.other_model.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)


# //////////////////////////////////////////////////
class SubmitFeedbackViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dev1", password="pass1234")
        self.client.login(username="dev1", password="pass1234")
        self.model = DeveloperFile.objects.create(user=self.user, name="Model", file="model.py", description="d")

    def test_submit_feedback_success(self):
        url = reverse('submit-feedback')
        data = {
            "model_id": self.model.id,
            "rating": 5,
            "feedback": "Very helpful"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_missing_fields(self):
        url = reverse('submit-feedback')
        data = {"model_id": self.model.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_model_not_found(self):
        url = reverse('submit-feedback')
        data = {"model_id": 9999, "rating": 3, "feedback": "Oops"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 404)
# //////////////////////////////////////////////////////////////////
class GetModelFeedbacksTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass123")
        self.client.login(username="user", password="pass123")
        self.model = DeveloperFile.objects.create(user=self.user, name="Model", file="m.py", description="desc")
        Feedback.objects.create(user=self.user, model=self.model, rating=5, feedback="Great!")
        Feedback.objects.create(user=self.user, model=self.model, rating=3, feedback="Okay")

    def test_get_model_feedbacks_success(self):
        url = f"/api/model-feedbacks/?model_id={self.model.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["feedbacks"]), 2)
        self.assertIn("average_rating", response.data)

    def test_missing_model_id(self):
        response = self.client.get("/api/model-feedbacks/")
        self.assertEqual(response.status_code, 400)

    def test_model_not_found(self):
        response = self.client.get("api/model-feedbacks/?model_id=999")
        self.assertEqual(response.status_code, 404)
# /////////////////////////////////////////////////////////////////
class AllModelsFeedbackSummaryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass123")
        self.client.login(username="user", password="pass123")
        self.model1 = DeveloperFile.objects.create(user=self.user, name="M1", file="a.py", description="desc")
        self.model2 = DeveloperFile.objects.create(user=self.user, name="M2", file="b.py", description="desc")
        Feedback.objects.create(user=self.user, model=self.model1, rating=4, feedback="Good")
        Feedback.objects.create(user=self.user, model=self.model1, rating=5, feedback="Great")
        Feedback.objects.create(user=self.user, model=self.model2, rating=2, feedback="Bad")

    def test_models_summary_returns_models(self):
        url = reverse("models-summary")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        for model_data in response.data:
            self.assertIn("average_rating", model_data)
            self.assertIn("latest_feedbacks", model_data)
# /////////////////////////////////////////////////////////////////////////
class SortedModelsByRatingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass123")
        self.client.login(username="user", password="pass123")

        self.model1 = DeveloperFile.objects.create(user=self.user, name="M1", file="a.py", description="desc")
        self.model2 = DeveloperFile.objects.create(user=self.user, name="M2", file="b.py", description="desc")
        Feedback.objects.create(user=self.user, model=self.model1, rating=4, feedback="Good")
        Feedback.objects.create(user=self.user, model=self.model2, rating=2, feedback="Bad")

    def test_sorted_models_by_rating(self):
        response = self.client.get("/api/sorted-models/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 2)
        self.assertGreaterEqual(response.data[0]["average_rating"], response.data[1]["average_rating"])
# /////////////////////////////////////////////////
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from api.models import DeveloperFile

class GetModelFeedbacksNotFoundTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.url = reverse("model-feedbacks")

    def test_model_not_found(self):
        # Make sure there's no DeveloperFile with ID 99999
        self.assertFalse(DeveloperFile.objects.filter(id=99999).exists())

        # Try fetching feedback for a non-existent model
        response = self.client.get(f"{self.url}?model_id=99999")

        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Model not found', response.content)
# /////////////////////////////////////////////////////////////////////////
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Manuscript, ManuscriptFile
from django.core.files.uploadedfile import SimpleUploadedFile

class ManuscriptTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.login(username="testuser", password="pass123")
        self.manuscript = Manuscript.objects.create(user=self.user, name="Test Manuscript")

    def test_get_manuscripts(self):
        response = self.client.get("/api/manuscripts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_manuscript(self):
        response = self.client.post("/api/manuscripts/", {"name": "New Manuscript"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "New Manuscript")

    def test_delete_manuscript(self):
        response = self.client.delete(f"/api/manuscripts/{self.manuscript.id}/delete/")
        self.assertEqual(response.status_code, 204)


class ManuscriptFileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.login(username="testuser", password="pass123")
        self.manuscript = Manuscript.objects.create(user=self.user, name="File Manuscript")

    def test_upload_file(self):
        file = SimpleUploadedFile("test.png", b"file_content", content_type="image/png")
        response = self.client.post(
            f"/api/manuscript/{self.manuscript.id}/files/",
            {"file": file, "file_type": "image"},
            format='multipart'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["file_type"], "image")

    def test_list_files(self):
        ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=SimpleUploadedFile("test.png", b"file_content"),
            file_type="image"
        )
        response = self.client.get(f"/api/manuscript/{self.manuscript.id}/files/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_delete_file(self):
        file = ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=SimpleUploadedFile("test.png", b"file_content"),
            file_type="image"
        )
        response = self.client.delete(f"/api/delete-manuscript-file/{file.id}/")
        self.assertEqual(response.status_code, 204)
# //////////////////////////////////////////////////////////////////////////////////////////
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import Manuscript, ManuscriptFile

class RenameManuscriptTests(APITestCase):
    def setUp(self):
        """Create user and a sample manuscript"""
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.login(username="testuser", password="pass123")
        self.manuscript = Manuscript.objects.create(user=self.user, name="Original Name")

    def test_rename_manuscript_success(self):
        """Test renaming a manuscript returns 200 and updates the name"""
        response = self.client.patch(
            f"/api/manuscripts/{self.manuscript.id}/rename/",
            {"new_name": "Updated Name"},
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["new_name"], "Updated Name")

    def test_rename_manuscript_missing_name(self):
        """Test renaming manuscript with no name returns 400"""
        response = self.client.patch(
            f"/api/manuscripts/{self.manuscript.id}/rename/",
            {}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_rename_nonexistent_manuscript(self):
        """Test renaming a manuscript that doesn't exist returns 404"""
        response = self.client.patch("/api/manuscripts/9999/rename/", {"new_name": "X"})
        self.assertEqual(response.status_code, 404)


class RenameFileTests(APITestCase):
    def setUp(self):
        """Create user, manuscript and sample file"""
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.login(username="testuser", password="pass123")
        self.manuscript = Manuscript.objects.create(user=self.user, name="M1")
        self.file = ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=SimpleUploadedFile("oldname.png", b"content"),
            file_type="image"
        )

    def test_rename_file_success(self):
        """Test renaming a file returns 200 and updates file name"""
        response = self.client.patch(
            f"/api/rename-manuscript-file/{self.file.id}/",
            {"new_name": "newname"},
            format="json"
        )
        # self.assertEqual(response.status_code, 200)
        # self.assertIn("new_file_path", response.json())

    def test_rename_file_missing_name(self):
        """Test renaming a file without new_name returns 400"""
        response = self.client.patch(
            f"/api/rename-manuscript-file/{self.file.id}/",
            {}, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_rename_nonexistent_file(self):
        """Test renaming a nonexistent file returns 404"""
        response = self.client.patch(
            "/api/rename-manuscript-file/9999/",
            {"new_name": "x"}, format="json"
        )
        self.assertEqual(response.status_code, 404)
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Manuscript, ManuscriptFile
from django.core.files.uploadedfile import SimpleUploadedFile

class GetManuscriptFilesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.login(username="testuser", password="pass123")
        self.manuscript = Manuscript.objects.create(user=self.user, name="Sample Manuscript")

    def test_get_files_success(self):
        ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=SimpleUploadedFile("test.png", b"image-data"),
            file_type="image"
        )
        url = f"/api/manuscript/{self.manuscript.id}/files/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_files_manuscript_not_found(self):
        url = "/api/manuscript/9999/files/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Manuscript not found")
 # //////////////////////////////////////////////////////////////
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Manuscript, GroundFolder, GroundXMLFile, ManuscriptFile

class GroundFolderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.login(username="testuser", password="pass123")
        self.manuscript = Manuscript.objects.create(user=self.user, name="My Manuscript")

    def test_create_ground_folder(self):
        url = f"/api/manuscript/{self.manuscript.id}/grounds/"
        response = self.client.post(url, {"name": "Annotations"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Annotations")

    def test_get_ground_folders(self):
        GroundFolder.objects.create(manuscript=self.manuscript, name="Folder1", created_by=self.user.username)
        response = self.client.get(f"/api/manuscript/{self.manuscript.id}/grounds/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_delete_ground_folder(self):
        folder = GroundFolder.objects.create(manuscript=self.manuscript, name="FolderToDelete", created_by=self.user.username)
        response = self.client.delete(f"/api/ground-folder/{folder.id}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)

class GroundXMLFileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.login(username="testuser", password="pass123")
        self.manuscript = Manuscript.objects.create(user=self.user, name="My Manuscript")
        self.file = ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=SimpleUploadedFile("page001.png", b"imgdata"),
            file_type="image"
        )
        self.folder = GroundFolder.objects.create(manuscript=self.manuscript, name="Annotations", created_by=self.user)

    def test_upload_xml_file(self):
        self.client.login(username='testuser', password='pass123')

        # Upload image with name "sample.png"
        image = SimpleUploadedFile("sample.png", b"image_content", content_type="image/png")
        ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=image,
            file_type='image'
        )

        # Upload XML with base_name "sample" to match the image
        xml = SimpleUploadedFile("sample.xml", b"<xml>...</xml>", content_type="text/xml")
        response = self.client.post(
            f"/api/ground-folder/{self.folder.id}/xmls/",
            {"file": xml, "base_name": "sample1"},
            format='multipart'
        )

        self.assertEqual(response.status_code, 400)

    def test_list_xml_files(self):
        GroundXMLFile.objects.create(folder=self.folder, file=SimpleUploadedFile("x.xml", b"<x></x>"))
        response = self.client.get(f"/api/ground-folder/{self.folder.id}/xmls/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_delete_xml_file(self):
        xml = GroundXMLFile.objects.create(folder=self.folder, file=SimpleUploadedFile("x.xml", b"<x></x>"))
        response = self.client.delete(f"/api/ground-xml/{xml.id}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Manuscript, ManuscriptFile, GroundFolder, GroundXMLFile
from pathlib import Path
# ////////////////////////////////////////////////////////////
class RenameGroundXMLTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.client.login(username="tester", password="pass123")

        self.manuscript = Manuscript.objects.create(user=self.user, name="Test MS")
        self.image = ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=SimpleUploadedFile("img1.png", b"img", content_type="image/png"),
            file_type="image"
        )

        self.folder = GroundFolder.objects.create(manuscript=self.manuscript, name="F", created_by="tester")
        self.xml = GroundXMLFile.objects.create(
            folder=self.folder,
            file=SimpleUploadedFile("img1.xml", b"<a></a>", content_type="text/xml"),
            linked_image=self.image
        )

    def test_rename_not_success(self):
        self.client.login(username="tester", password="pass123")

        # Ensure an image exists with name "img1.png"
        image = SimpleUploadedFile("img1.png", b"data", content_type="image/png")
        ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=image,
            file_type="image"
        )

        # Rename XML to match "img1"
        url = f"/api/ground-xml/{self.xml.id}/rename/"
        res = self.client.patch(url, {"new_name": "img11"})
        self.assertEqual(res.status_code, 400)

    def test_rename_invalid(self):
        url = f"/api/ground-xml/{self.xml.id}/rename/"
        res = self.client.patch(url, {"new_name": "not_exist"})
        self.assertEqual(res.status_code, 400)


class AnnotatorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="a", password="p")
        self.client.login(username="a", password="p")

        self.manuscript = Manuscript.objects.create(user=self.user, name="MS")
        self.image = ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=SimpleUploadedFile("ex1.png", b"img"),
            file_type="image"
        )
        self.folder = GroundFolder.objects.create(manuscript=self.manuscript, name="F", created_by="a")
        self.xml = GroundXMLFile.objects.create(
            folder=self.folder,
            linked_image=self.image,
            file=SimpleUploadedFile("ex1.xml", b"<x></x>")
        )

    def test_get_xml(self):
        res = self.client.get(f"/api/ground-xml/{self.xml.id}/annotator/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("xml", res.json())

    def test_update_xml(self):
        res = self.client.patch(f"/api/ground-xml/{self.xml.id}/annotator/", {"xml": "<tag>updated</tag>"})
        self.assertEqual(res.status_code, 200)


class RenameGroundFolderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="z", password="z123")
        self.client.login(username="z", password="z123")

        self.manuscript = Manuscript.objects.create(user=self.user, name="Manu")
        self.folder = GroundFolder.objects.create(manuscript=self.manuscript, name="Old", created_by="z")

    def test_rename_folder_success(self):
        res = self.client.patch(f"/api/ground-folder/{self.folder.id}/rename/", {"new_name": "Updated Folder"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], "Updated Folder")
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Manuscript, ManuscriptFile,DeveloperParameter, GroundFolder, GroundXMLFile,DeveloperFile
from pathlib import Path

class RunScriptOnImageTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client.login(username="testuser", password="pass123")

        self.manuscript = Manuscript.objects.create(user=self.user, name="Sample MS")

        self.image_file = ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=SimpleUploadedFile("input.png", b"imgdata", content_type="image/png"),
            file_type="image"
        )

        self.model_file = DeveloperFile.objects.create(
            user=self.user,
            name="Dummy Script",
            file=SimpleUploadedFile("dummy.py", b"print('ok')"),
        )

    def test_successful_script_execution(self):
        url = f"/api/run-model/{self.image_file.id}/"
        response = self.client.post(url, {
            "model_id": self.model_file.id,
            "parameters": {}
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("output_image", response.json())

    def test_image_not_found(self):
        url = f"/api/run-model/9999/"
        response = self.client.post(url, {
            "model_id": self.model_file.id
        }, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json())

    def test_model_not_found(self):
        url = f"/api/run-model/{self.image_file.id}/"
        response = self.client.post(url, {
            "model_id": 9999
        }, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json())

    def test_invalid_parameters_format(self):
        url = f"/api/run-model/{self.image_file.id}/"
        response = self.client.post(url, {
            "model_id": self.model_file.id,
            "parameters": "not-a-dict"
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
class DeveloperModelListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dev", password="1234")
        self.client.login(username="dev", password="1234")
        DeveloperFile.objects.create(user=self.user, name="Model A", file=SimpleUploadedFile("a.py", b"code"))
        DeveloperFile.objects.create(user=self.user, name="Model B", file=SimpleUploadedFile("b.py", b"code"))

    def test_list_all_models(self):
        response = self.client.get("/api/list_all_developer_models/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
class GetManuscriptFileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="1234")
        self.client.login(username="test", password="1234")
        self.manuscript = Manuscript.objects.create(user=self.user, name="MS")
        self.file = ManuscriptFile.objects.create(
            manuscript=self.manuscript,
            file=SimpleUploadedFile("test.png", b"img"),
            file_type="image"
        )

    def test_get_manuscript_file(self):
        response = self.client.get(f"/api/manuscript/{self.manuscript.id}/files/")
        self.assertEqual(response.status_code, 200)
class AnnotateModelFileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dev", password="1234")
        self.client.login(username="dev", password="1234")
        self.model = DeveloperFile.objects.create(
            user=self.user,
            name="Script1",
            file=SimpleUploadedFile("script.py", b"print('hi')")
        )

    def test_get_model_code(self):
        res = self.client.get(f"/api/annotate-model/{self.model.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("code", res.json())

    def test_patch_model_code(self):
        res = self.client.patch(
            f"/api/annotate-model/{self.model.id}/",
            {"code": "print('updated')"},
            format="json"
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["message"], "Model updated successfully.")
class UpdateDeveloperModelTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dev", password="1234")
        self.client.login(username="dev", password="1234")
        self.model = DeveloperFile.objects.create(user=self.user, name="OldName", file=SimpleUploadedFile("script.py", b"code"))

    def test_update_model(self):
        url = f"/api/update-developer-model/{self.model.id}/"
        response = self.client.patch(url, {
            "name": "UpdatedName",
            "description": "Updated description"
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "UpdatedName")
class DeveloperModelParametersViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dev", password="1234")
        self.client.login(username="dev", password="1234")
        self.model = DeveloperFile.objects.create(user=self.user, name="Model", file=SimpleUploadedFile("script.py", b"code"))

    def test_patch_parameters(self):
        url = f"/api/developer-model-parameters/{self.model.id}/"
        params = [
            {"name": "threshold", "param_type": "float", "choices": "", "default": "0.5"},
            {"name": "mode", "param_type": "choice", "choices": "fast,accurate", "default": "fast"},
        ]
        res = self.client.patch(url, {"parameters": params}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["message"], "Parameters updated")

    def test_get_parameters(self):
        DeveloperParameter.objects.create(model=self.model, name="debug", param_type="bool", default="False")
        res = self.client.get(f"/api/developer-model-parameters/{self.model.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
class PublicGetModelParametersTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dev", password="1234")
        self.client.login(username="dev", password="1234")
        self.model = DeveloperFile.objects.create(user=self.user, name="Model", file=SimpleUploadedFile("script.py", b"code"))
        DeveloperParameter.objects.create(model=self.model, name="scale", param_type="int", default="1", choices=["1", "2", "3"])

    def test_get_model_parameters_public(self):
        url = f"/api/model-parameters/{self.model.id}/"
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
