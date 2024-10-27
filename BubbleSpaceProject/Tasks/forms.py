from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'category', 'due_date', 'description', 'status', 'assigned_to']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.RadioSelect(choices=Task.STATUS_CHOICES),
            'description': forms.Textarea(attrs={'rows': 4}),
        }