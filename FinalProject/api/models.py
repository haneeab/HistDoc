from django.db import models

# Create your models here.
from django.db import models

class TestData(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    age = models.IntegerField()

    def __str__(self):
        return self.name
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class UserFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('pdf', 'PDF'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="user_files/")  # Files go to backend/media/user_files/
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type.capitalize()} by {self.user.username}"


# models.py
class DeveloperFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='researcher_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExtractionRecord(models.Model):
    user_file = models.ForeignKey(UserFile, on_delete=models.CASCADE, related_name='extractions')
    model_used = models.ForeignKey(DeveloperFile, on_delete=models.CASCADE, related_name='used_in_extractions')
    extracted_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_file.id} extracted with {self.model_used.id}"
from django.db import models
from django.contrib.auth.models import User
from .models import DeveloperFile  # Assuming DeveloperFile is already defined

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Okay'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    model = models.ForeignKey(DeveloperFile, on_delete=models.CASCADE, related_name='feedbacks')
    feedback = models.TextField(blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.model.file.name} ({self.rating}⭐)"
