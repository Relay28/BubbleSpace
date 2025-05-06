from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    ProjectId = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Description = models.CharField(max_length=1000)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    @property
    def status_color(self):
        """Returns a color based on the status."""
        if self.Status == 'Ongoing':
            return 'yellow'
        elif self.Status == 'Completed':
            return 'green'
        elif self.Status == 'Cancelled':
            return 'red'
        elif self.Status == 'Pending':
            return 'grey'

    def start_project(self):
        """Set project status to 'Ongoing'."""
        if self.Status == 'Pending':
            self.Status = 'Ongoing'
            self.save()

    def cancel_project(self):
        """Set project status to 'Cancelled'."""
        if self.Status in ['Pending', 'Ongoing']:
            self.Status = 'Cancelled'
            self.save()

    def complete_project(self):
        """Set project status to 'Completed'."""
        if self.Status == 'Ongoing':
            self.Status = 'Completed'
            self.save()

    def __str__(self):
        return self.Title