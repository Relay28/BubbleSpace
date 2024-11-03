from django.db import models

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

    @property
    def status_color(self):
        """Returns a color based on the status."""
        if self.Status == 'Ongoing':
            return 'yellow'
        elif self.Status == 'Completed':
            return 'green'
        elif self.Status == 'Cancelled':
            return 'red'

    def __str__(self):
        return self.Title
