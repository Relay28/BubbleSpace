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
    return render(request, 'Projects/project_detail.html', {'project': project})
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
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'Projects/project_form.html', {'form': form})    

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'Projects/project_confirm_delete.html', {'project': project})