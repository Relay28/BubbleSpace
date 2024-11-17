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
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Team updated successfully.")
            return redirect('team_detail', pk=team.pk)
    else:
        form = TeamForm(instance=team)
    
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
