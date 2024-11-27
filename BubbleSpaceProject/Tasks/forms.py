from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title',
                'style': (
                    'width: 100%; font-size: 16px; padding: 10px; border-radius: 5px; '
                    'border: 1px solid #eaeaea; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);'
                ),
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a short description of the task...',
                'rows': 3,
                'style': (
                    'width: 100%; font-size: 14px; padding: 10px; border-radius: 5px; '
                    'border: 1px solid #eaeaea; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); resize: none;'
                ),
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': (
                    'width: 100%; font-size: 14px; padding: 10px; border-radius: 5px; '
                    'border: 1px solid #eaeaea; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);'
                ),
            }),
            'status': forms.RadioSelect(attrs={
                'class': 'form-radio-group',
                'style': (
                    'display: flex; gap: 15px; padding: 10px;'
                ),
            }),
        }
