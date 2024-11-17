# forms.py
from django import forms
from .models import Team
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,  # Make the field optional
    )

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop('creator', None)
        self.is_creation = kwargs.pop('is_creation', False)  # Flag to check if it's a creation form
        super().__init__(*args, **kwargs)
        
        if self.creator:
            self.fields['members'].queryset = User.objects.exclude(id=self.creator.id)
        
        if self.is_creation:  # Remove the members field if creating a team
            self.fields.pop('members', None)

    def save(self, commit=True):
        team = super().save(commit=False)
        if commit:
            team.save()
            if not self.is_creation:  # Save members only if it's not a creation form
                self.save_m2m()
            if self.creator:
                team.members.add(self.creator)  # Ensure creator is always a member
        return team

    class Meta:
        model = Team
        fields = ['team_name', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
        }

class AddTeamMemberForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)
        if team:
            self.fields['members'].queryset = User.objects.exclude(id=team.creator.id)
        self.team = team  # Save the team instance for later use in save()

    def save(self, commit=True):
        team = super().save(commit=False)
        if commit:
            team.save()
            self.save_m2m()
            # Ensure creator is always part of the team
            if self.team and self.team.creator:
                team.members.add(self.team.creator)
        return team

    class Meta:
        model = Team
        fields = ['members']
