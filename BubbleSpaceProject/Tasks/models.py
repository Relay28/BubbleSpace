from django.db import models
# models.py

from django.conf import settings
from Login.models import Users_Account 
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
        ('green', 'Completed'),
        ('yellow', 'Ongoing'),
        ('red', 'Todo'),
    ]
    task_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    due_date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    assigned_to = models.ForeignKey(Users_Account, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False) 
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='tasks',
        
    )
    project = models.ForeignKey(
        'Projects.Project',
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title