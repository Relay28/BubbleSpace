from django import forms
from .models import Task
from Teams.models import Team 
from django.contrib.auth import get_user_model
User = get_user_model()
from Login.models import Users_Account 

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
                    'flex: 2; font-size: 14px; padding: 8px; border-radius: 5px; '
                    'border: 1px solid #ddd; box-shadow: none; height: 150px;'
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
    
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)  # Extract the project from kwargs
        super().__init__(*args, **kwargs)

        if project:
            self.fields['assigned_to'].queryset = Users_Account.objects.filter(
                teams__projects=project
            ).distinct()
        else:
            self.fields['assigned_to'].queryset = Users_Account.objects.none()

    
def clean_assigned_to(self):
    assigned_to = self.cleaned_data.get('assigned_to')
    project = self.initial.get('project')  # Retrieve the project passed during initialization

    if project and not Users_Account.objects.filter(pk=assigned_to.pk, teams__projects=project).exists():
        raise forms.ValidationError("This user is not part of the project's team.")
    
    return assigned_to
