# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Team
from .forms import TeamForm, AddTeamMemberForm
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db.models import Q
User = get_user_model()

@login_required
def add_team_member(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.user != team.creator:
        messages.error(request, "Only the team creator can add members.")
        return redirect('team_detail', pk=team.pk)

    if request.method == 'POST':
        form = AddTeamMemberForm(request.POST, instance=team, team=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Members added successfully.")
            return redirect('team_detail', pk=team.pk)
    else:
        form = AddTeamMemberForm(instance=team, team=team)
    return render(request, 'teams/add_team_member.html', {'team': team, 'form': form})

@login_required
def team_list(request):
    teams = Team.objects.filter(members=request.user)
    return render(request, 'teams/team_list.html', {'teams': teams})

@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    members = team.members.all()
    projects = team.projects.all()  # Get only projects related to this team
    return render(request, 'teams/team_detail.html', {'team': team, 'members': members, 'projects': projects})


@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, creator=request.user, is_creation=True)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user  # Set the creator
            team.save()
            team.members.add(request.user)  # Add the creator as a member
            messages.success(request, "Team created successfully.")
            return redirect('team_list')
    else:
        form = TeamForm(creator=request.user, is_creation=True)
    return render(request, 'teams/team_form.html', {'form': form})

@login_required
def team_update(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team, creator=team.creator)
        if form.is_valid():
            # Use commit=False to modify before the save
            team = form.save(commit=False)
            team.save()  # Save changes to the team instance
            form.save_m2m()  # Save many-to-many data (members)
            team.members.add(team.creator)  # Ensure the creator is part of the team
            messages.success(request, "Team updated successfully.")
            return redirect('team_detail', pk=team.pk)
    else:
        form = TeamForm(instance=team, creator=team.creator)
    return render(request, 'teams/team_form.html', {'form': form, 'team': team})


from django.http import HttpResponseForbidden

@login_required
@require_POST
def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.user == team.creator:
        print("Deleting team:", team)  # Debugging output
        team.delete()
        messages.success(request, "Team deleted successfully.")
    else:
        print("User not authorized to delete this team.")  # Debugging output
        messages.error(request, "Only the team creator can delete this team.")
        return HttpResponseForbidden("You do not have permission to delete this team.")
    return redirect('team_list')


@login_required
def team_edit(request, pk):
    team = get_object_or_404(Team, pk=pk)
    
    # Check if the current user is the creator of the team
    if request.user != team.creator:
        messages.error(request, "Only the team creator can edit the team.")
        return HttpResponseForbidden("You do not have permission to edit this team.")
    
    if request.method == 'POST':
        # Pass is_edit=True to exclude the members field
        form = TeamForm(request.POST, instance=team, is_edit=True)
        if form.is_valid():
            form.save()
            messages.success(request, "Team updated successfully.")
            return redirect('team_detail', pk=team.pk)
    else:
        # Pass is_edit=True to exclude the members field
        form = TeamForm(instance=team, is_edit=True)
    
    return render(request, 'teams/team_edit_form.html', {'form': form, 'team': team})

@login_required
def search_member(request):
    query = request.GET.get('q', '').strip()
    team_id = request.GET.get('team_id', '').strip()
    
    # Log the inputs for debugging
    print(f"Search query: '{query}', Team ID: '{team_id}'")

    if not query:
        return JsonResponse([], safe=False)

    # Validate the team ID
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        print(f"Team with ID {team_id} does not exist.")  # Debugging
        return JsonResponse({'error': 'Invalid team ID'}, status=400)

    # Exclude current team members and the requesting user from the results
    existing_member_ids = team.members.values_list('id', flat=True)
    users = User.objects.filter(
        Q(username__icontains=query) & ~Q(id__in=existing_member_ids)
    ).exclude(id=request.user.id)[:10]  # Limit results to 10

    # Prepare data for the response
    user_data = [{'id': user.id, 'username': user.username} for user in users]

    # Return the JSON response
    return JsonResponse(user_data, safe=False)



@login_required
def remove_team_member(request, team_id, member_id):
    team = get_object_or_404(Team, pk=team_id)
    member = get_object_or_404(User, pk=member_id)

    # Ensure the user is the creator (owner) of the team
    if request.user == team.creator:
        # Remove the member from the team
        team.members.remove(member)
        # Optionally, redirect back to the team details page
        return redirect('team_detail', pk=team.id)
    else:
        # If the user is not the creator, redirect or show an error
        return redirect('team_detail', pk=team.id)
    


from django.http import HttpResponseForbidden

@login_required
def transfer_ownership(request, team_id, member_id):
    """Allows the team creator to transfer ownership to another member."""
    team = get_object_or_404(Team, pk=team_id)
    new_owner = get_object_or_404(User, pk=member_id)

    # Ensure the requesting user is the current creator
    if request.user != team.creator:
        messages.error(request, "Only the team owner can transfer ownership.")
        return HttpResponseForbidden("You do not have permission to transfer ownership.")
    
    # Ensure the new owner is already a team member
    if new_owner not in team.members.all():
        messages.error(request, "The selected user is not a team member.")
        return redirect('team_detail', pk=team.pk)

    # Transfer ownership
    team.creator = new_owner
    team.save()

    messages.success(request, f"Ownership successfully transferred to {new_owner.username}.")
    return redirect('team_detail', pk=team.pk)

@login_required
def leave_team(request, team_id):
    """Allows a user to leave a team. If the team owner leaves, reassign ownership if members exist."""
    team = get_object_or_404(Team, pk=team_id)

    # Check if the leaving user is the creator
    if request.user == team.creator:
        # Prevent the owner from leaving if the team has no other members
        remaining_members = team.members.exclude(id=request.user.id)
        if remaining_members.exists():
            # Assign the first remaining member as the new creator
            new_creator = remaining_members.first()
            team.creator = new_creator
            team.save()
            messages.success(
                request,
                f"Ownership transferred to {new_creator.username} as you have left the team."
            )
        else:
            # If no members remain, prevent the owner from leaving
            messages.error(
                request,
                "You cannot leave the team as the owner if there are no other members."
            )
            return redirect('team_detail', pk=team.pk)

    # Remove the user from the team
    team.members.remove(request.user)
    messages.success(request, f"You have left the team '{team.team_name}'.")
    return redirect('team_list')
