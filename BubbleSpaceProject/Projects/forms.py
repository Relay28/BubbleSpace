from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['Title', 'Description', 'Status']
        widgets = {
            'Status': forms.Select(attrs={'class': 'form-control'}),
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': forms.Textarea(attrs={'class': 'form-control', 'maxlength': 1000}),
        }