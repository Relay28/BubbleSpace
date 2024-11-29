# forms.py
from django import forms
from .models import Team
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator', None)
        self.is_creation = kwargs.pop('is_creation', False)  # Flag to check if it's a creation form
        self.is_edit = kwargs.pop('is_edit', False)  # Flag to check if it's an edit form
        super().__init__(*args, **kwargs)
        
        if self.creator and 'members' in self.fields:
            self.fields['members'].queryset = User.objects.exclude(id=self.creator.id)
        
        if self.is_creation:  # Remove the members field if creating a team
            self.fields.pop('members', None)

        if self.is_edit:  # Remove the members field for editing
            self.fields.pop('members', None)

    def save(self, commit=True):
        team = super().save(commit=False)
        if commit:
            team.save()
            if self.is_creation and self.creator:
                team.members.add(self.creator)  # Ensure creator is always a member
        return team

    class Meta:
        model = Team
        fields = ['team_name','team_picture' ,'members']

      
class AddTeamMemberForm(forms.ModelForm):
    members = forms.CharField(required=False)  # Use CharField to accept a comma-separated string

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)
        self.team = team

    def clean_members(self):
        member_ids = self.cleaned_data['members']
        if member_ids:
            ids = member_ids.split(',')
            users = User.objects.filter(id__in=ids).exclude(id__in=self.team.members.values_list('id', flat=True))
            if len(users) != len(ids):
                raise forms.ValidationError("One or more users are invalid or already in the team.")
            return users
        return []

    def save(self, commit=True):
        team = self.team
        new_members = self.cleaned_data.get('members', [])
        if commit:
            for member in new_members:
                team.members.add(member)
        return team

    class Meta:
        model = Team
        fields = []
