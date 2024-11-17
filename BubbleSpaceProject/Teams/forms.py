# forms.py
from django import forms
from .models import Team
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamForm(forms.ModelForm):
   

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
        fields = ['team_name',]
      
class AddTeamMemberForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super().__init__(*args, **kwargs)
        if team:
            # Exclude the creator and current team members from the queryset
            self.fields['members'].queryset = User.objects.exclude(id__in=team.members.values_list('id', flat=True))
        self.team = team  # Save the team instance for later use in save()

    def save(self, commit=True):
        team = self.team  # Use the provided team instance
        new_members = self.cleaned_data.get('members', [])

        # Add the new members to the team without removing existing ones
        if commit:
            for member in new_members:
                team.members.add(member)

        # Ensure creator is always part of the team
        if team.creator and team.creator not in team.members.all():
            team.members.add(team.creator)

        return team

    class Meta:
        model = Team
        fields = ['members']
