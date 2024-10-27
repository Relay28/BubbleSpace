# models.py
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title
