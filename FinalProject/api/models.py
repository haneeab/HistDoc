from django.db import models

# Create your models here.
from django.db import models

class TestData(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    age = models.IntegerField()

    def __str__(self):
        return self.name
