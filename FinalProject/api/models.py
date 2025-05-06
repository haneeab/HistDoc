from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Model for Python script files uploaded by developers
class DeveloperFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The developer who uploaded the file
    file = models.FileField(upload_to='researcher_files/')  # Path to the uploaded model file (.py)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp when file was uploaded
    name = models.CharField(max_length=100, blank=True)  # Optional name for the model
    description = models.TextField(blank=True)  # Optional description of the model purpose

# Model for parameters that a DeveloperFile (model) can accept
class DeveloperParameter(models.Model):
    model = models.ForeignKey(DeveloperFile, on_delete=models.CASCADE, related_name="parameters")  # Associated model
    name = models.CharField(max_length=100)  # Parameter name (e.g., "method")
    param_type = models.CharField(max_length=50)  # Type of parameter: string, int, float
    choices = models.JSONField(blank=True, null=True)  # Optional list of allowed values
    default = models.CharField(max_length=100, blank=True)  # Optional default value

# Model for user feedback on a DeveloperFile
class Feedback(models.Model):
    RATING_CHOICES = [
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Okay'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')  # Who gave the feedback
    model = models.ForeignKey(DeveloperFile, on_delete=models.CASCADE, related_name='feedbacks')  # Model being rated
    feedback = models.TextField(blank=True)  # Optional text feedback
    rating = models.IntegerField(choices=RATING_CHOICES)  # Rating score (1 to 5)
    created_at = models.DateTimeField(auto_now_add=True)  # When the feedback was submitted

    def __str__(self):
        return f"{self.user.username} → {self.model.file.name} ({self.rating}⭐)"

# Model representing a collection of manuscript files owned by a user
class Manuscript(models.Model):
    name = models.CharField(max_length=100)  # Name of the manuscript
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manuscripts")  # Owner of the manuscript
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created

    def __str__(self):
        return f"{self.name} ({self.user.username})"

# Model representing a single file inside a manuscript (image or ground-truth)
class ManuscriptFile(models.Model):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name="files")  # Parent manuscript
    file = models.FileField(upload_to="manuscript_files/")  # Actual file uploaded
    file_type = models.CharField(max_length=50, choices=[("image", "Image"), ("ground_truth", "Ground Truth")])  # Type of file
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Upload timestamp

    def __str__(self):
        return f"{self.file.name}"

# Model representing a folder for storing ground-truth (XML) files
class GroundFolder(models.Model):
    manuscript = models.ForeignKey(Manuscript, on_delete=models.CASCADE, related_name='ground_folders')  # Related manuscript
    name = models.CharField(max_length=100)  # Folder name
    created_by = models.CharField(max_length=100)  # Name of person who created the folder
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"{self.name} - {self.manuscript.name}"

# Model representing a single ground-truth XML file
class GroundXMLFile(models.Model):
    folder = models.ForeignKey(GroundFolder, on_delete=models.CASCADE, related_name='xml_files')  # Folder it belongs to
    file = models.FileField(upload_to='ground_xmls/', validators=[FileExtensionValidator(['xml'])])  # XML file
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp
    linked_image = models.ForeignKey(
        ManuscriptFile,  # Image file this XML is linked to (optional)
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="linked_xmls"
    )

    def __str__(self):
        return self.file.name
