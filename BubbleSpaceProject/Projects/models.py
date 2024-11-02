from django.db import models

# Create your models here.
class Project(models.Model):
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    ProjectId = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Description = models.CharField(max_length=1000)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def status_color(self):
        """Returns a color based on the status."""
        if self.status == 'Ongoing':
            return 'Yellow'
        elif self.status == 'Completed':
            return 'Green'
        elif self.status == 'Cancelled':
            return 'Red'
        
    def __str__(self):
        return self.Title