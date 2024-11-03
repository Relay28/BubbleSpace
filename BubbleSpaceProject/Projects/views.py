from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from Teams.models import Team
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'Projects/project_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    team = Team.objects.filter(projects=project).first()  # Get the first team associated with this project
    return render(request, 'Projects/project_detail.html', {'project': project, 'team': team})


@login_required
def project_create(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            team.projects.add(project)  # Add the project to the team's projects
            return redirect('team_detail', pk=team.pk)
    else:
        form = ProjectForm()

    return render(request, 'Projects/project_form.html', {'form': form, 'team': team})

def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)  # Redirect to project detail or list
    else:
        form = ProjectForm(instance=project)
    return render(request, 'Projects/project_form.html', {'form': form, 'project': project})


def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
   # team = project.team  # Get the associated team before deleting the project
    
    if request.method == 'POST':
        project.delete()
        return redirect('team_list')  # Redirect to the team's detail page
    
    return render(request, 'Projects/project_confirm_delete.html', {'project': project})