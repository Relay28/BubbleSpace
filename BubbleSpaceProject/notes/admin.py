# admin.py in notes_app
from django.contrib import admin
from .models import Note

admin.site.register(Note)
