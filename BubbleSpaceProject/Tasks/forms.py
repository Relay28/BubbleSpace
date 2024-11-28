from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status']
        widgets = {
            'title': 
            forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Task title',
                'style': (
                    'flex: 2; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none;'
                ),
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description (optional)',
                'style': (
                    'flex: 3; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none;'
                ),
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': (
                    'flex: 1; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none;'
                ),
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'style': (
                    'flex: 1; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none;'
                ),
            }),
        }



class ProjectTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'assigned_to', 'due_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Task title',
                'style': (
                    'flex: 2; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none;'
                ),
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description (optional)',
                'style': (
                    'flex: 3; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none; height: 100px;'
                ),
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'style': (
                    'flex: 1; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none;'
                ),
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-control',
                'style': (
                    'flex: 1; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none;'
                ),
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'style': (
                    'flex: 1; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none;'
                ),
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'style': (
                    'flex: 1; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none;'
                ),
            }),
        }