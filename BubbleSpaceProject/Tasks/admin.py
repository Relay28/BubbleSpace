from django.contrib import admin
from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'category', 'due_date', 'status', 'assigned_to')
    list_filter = ('category', 'status')
    search_fields = ('description', 'assigned_to')