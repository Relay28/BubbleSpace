from django.db import models
# models.py

from django.conf import settings

class Task(models.Model):
    title = models.CharField(max_length=255)
    CATEGORY_CHOICES = [
        ('Category 1', 'Category 1'),
        ('Category 2', 'Category 2'),
        ('Category 3', 'Category 3'),
        ('Category 4', 'Category 4'),
        ('Category 5', 'Category 5'),
    ]
    STATUS_CHOICES = [
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
    ]
    task_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    due_date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    assigned_to = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='tasks',
        
    )

    def __str__(self):
        return self.title

