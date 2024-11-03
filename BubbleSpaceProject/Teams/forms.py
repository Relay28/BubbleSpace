# forms.py
from django import forms
from .models import Team
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        # Take the creator from kwargs and filter them out of the members list
        self.creator = kwargs.pop('creator', None)
        super().__init__(*args, **kwargs)
        if self.creator:
            self.fields['members'].queryset = User.objects.exclude(id=self.creator.id)

    def save(self, commit=True):
        # Call the parent save method, and add the creator to the members
        team = super().save(commit=False)
        if commit:
            team.save()
            self.save_m2m()  # Save many-to-many data for members
            if self.creator:
                team.members.add(self.creator)  # Ensure creator is always a member
        return team

    class Meta:
        model = Team
        fields = ['team_name', 'members',]
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

    class Meta:
        model = Team
        fields = ['members']
