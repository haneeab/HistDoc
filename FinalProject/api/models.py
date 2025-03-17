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

class UserFile(models.Model):
    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('pdf', 'PDF'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="user_files/")
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type.capitalize()} by {self.user.username}"
