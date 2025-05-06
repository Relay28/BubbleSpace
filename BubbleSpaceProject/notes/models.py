# models.py in the application with Note model
from django.db import models
from Login.models import Users_Account  # Replace 'user_app' with the actual app name where Users_Account is defined

class Note(models.Model):
    user = models.ForeignKey(Users_Account, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title
