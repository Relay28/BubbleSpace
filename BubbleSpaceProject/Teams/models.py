from django.db import models
from django.conf import settings

from Projects.models import Project

class Team(models.Model):
    team_name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams')
    projects = models.ManyToManyField(Project, related_name='teams', blank=True)
    team_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.team_name
