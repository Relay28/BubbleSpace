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
from django.shortcuts import render
from django.template.loader import render_to_string
from Projects.forms import ProjectForm
from django.conf import settings
from django.http import HttpResponseForbidden
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
    form = ProjectForm() 
    members = team.members.all()
    projects = team.projects.all()  # Get only projects related to this team
    return render(request, 'teams/team_detail.html', {'team': team, 'members': members, 'projects': projects,'form':form})

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, creator=request.user, is_creation=True)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user 
            team.save()
            team.members.add(request.user)  
            
            # Render the updated team list to include the new team
            team_list_html = render_to_string('teams/team_list.html', {'teams': Team.objects.all()}, request=request)

            return JsonResponse({
                'success': True,
                'message': "Team created successfully.",
                'team_list_html': team_list_html,
            })

        return JsonResponse({
            'success': False,
            'error': "Invalid form data.",
            'errors': form.errors,
        }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)





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

    
    if request.user != team.creator:
        messages.error(request, "Only the team creator can edit the team.")
        return HttpResponseForbidden("You do not have permission to edit this team.")

    if request.method == 'POST':
        
        form = TeamForm(request.POST, request.FILES, instance=team, is_edit=True)
        if form.is_valid():
            team = form.save()
            messages.success(request, "Team updated successfully.")
            return redirect('team_detail', pk=team.pk)
    else:
       
        form = TeamForm(instance=team, is_edit=True)

    return render(request, 'teams/team_details.html', {'form': form, 'team': team})



@login_required
def search_member(request):
    query = request.GET.get('q', '').strip()
    team_id = request.GET.get('team_id', '').strip()
    
   
    if not query:
        return JsonResponse([], safe=False)

    
    try:
        team = Team.objects.get(id=team_id)
    except Team.DoesNotExist:
        print(f"Team with ID {team_id} does not exist.")  
        return JsonResponse({'error': 'Invalid team ID'}, status=400)

  
    existing_member_ids = team.members.values_list('id', flat=True)
    users = User.objects.filter(
        Q(username__icontains=query) & ~Q(id__in=existing_member_ids)
    ).exclude(id=request.user.id)[:10] 
    default_profile_picture = f"{settings.MEDIA_URL}profile_pictures/default.svg"
    

    user_data = [{'id': user.id, 'username': user.username,'profile_picture':user.profile_picture.url if user.profile_picture else default_profile_picture} for user in users]

    
    return JsonResponse(user_data, safe=False)



@login_required
def remove_team_member(request, team_id, member_id):
    team = get_object_or_404(Team, pk=team_id)
    member = get_object_or_404(User, pk=member_id)

    
    if request.user == team.creator:
        team.members.remove(member)
        return redirect('team_detail', pk=team.id)
    else:
        # If the user is not the creator, redirect or show an error
        return redirect('team_detail', pk=team.id)
    

@login_required
def transfer_ownership(request, team_id, member_id):
    """Allows the team creator to transfer ownership to another member."""
    team = get_object_or_404(Team, pk=team_id)
    new_owner = get_object_or_404(User, pk=member_id)

    if request.user != team.creator:
        messages.error(request, "Only the team owner can transfer ownership.")
        return HttpResponseForbidden("You do not have permission to transfer ownership.")
    
    if new_owner not in team.members.all():
        messages.error(request, "The selected user is not a team member.")
        return redirect('team_detail', pk=team.pk)

    team.creator = new_owner
    team.save()

    messages.success(request, f"Ownership successfully transferred to {new_owner.username}.")
    return redirect('team_detail', pk=team.pk)

@login_required
def leave_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.user == team.creator:
        remaining_members = team.members.exclude(id=request.user.id)
        if remaining_members.exists():
            new_creator = remaining_members.first()
            team.creator = new_creator
            team.save()
            messages.success(
                request,
                f"Ownership transferred to {new_creator.username} as you have left the team."
            )
        else:
            team.delete()
            messages.success(
                request,
                f"The team '{team.team_name}' has been deleted as you were the last member."
            )
            return redirect('team_list')

    team.members.remove(request.user)
    messages.success(request, f"You have left the team '{team.team_name}'.")
    return redirect('team_list')

