from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from Tasks.models import Task
from Teams.models import Team
from .forms import ProjectForm
from Tasks.forms import TaskForm,ProjectTaskForm
from django.contrib.auth.decorators import login_required

# Create your views here.

# Project List View
def project_list(request):
    project_id = request.GET.get('project_id')  # Get project_id from query parameters
    if project_id:
        project = get_object_or_404(Project, pk=project_id)
    else:
        project = Project.objects.first()  # Default to the first project if no ID is provided
    
    tasks = project.tasks.all()  # Get tasks for the specific project
    return render(request, 'Projects/project_list.html', {'project': project, 'tasks': tasks})

# Project Detail View
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    team = Team.objects.filter(projects=project).first()  # Get the first team associated with this project
    return render(request, 'Projects/project_detail.html', {'project': project, 'tasks': tasks, 'team': team})


# Create Project View
@login_required
def project_create(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            team.projects.add(project)  # Add the project to the team's projects
            return redirect('team_detail', pk=team.pk)  # Redirect to the team's detail page after creating the project
    else:
        form = ProjectForm()

    return render(request, 'teams/team_detail.html', {'form': form, 'team': team})

# Task Create for a Specific Project
@login_required
def task_create_for_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = ProjectTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project  # Assign the task to the specified project
            task.created_by = request.user  # Assign the currently logged-in user
            task.save()
            # After saving the task, redirect to the project form for the same project
            return redirect('project_form', pk=project.pk)  # Use project.pk instead of project.id
    else:
        form = ProjectTaskForm()

    return render(request, 'Projects/task_form.html', {'form': form, 'project': project})

def project_tasks(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=project)
    return render(request, 'Projects/project_list.html', {'project': project, 'tasks': tasks})

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    team = Team.objects.filter(projects=project).first()  # Get the associated team
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('team_detail', pk=team.pk)  # Redirect to the team's detail page after updating the project
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'Projects/project_form.html', {'form': form, 'project': project, 'team': team})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Get the associated team before deleting the project
    team = Team.objects.filter(projects=project).first()

    if request.method == 'POST':
        project.delete()
        # Redirect to the associated team's detail page
        return redirect('team_detail', pk=team.pk)  # Redirect to team_detail view
    
    return render(request, 'Projects/project_confirm_delete.html', {'project': project})

@login_required
def task_update(request, pk):
    # Fetch the task and its associated project
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    project = task.project  # Get the associated project

    if request.method == 'POST':
        form = ProjectTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            # Redirect back to project_list with the specific project context
            return redirect('project_list') + f"?project_id={project.id}"
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Update Task', 'project': project})

@login_required
def task_delete(request, pk):
    # Fetch the task and its associated project
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    project = task.project  # Get the associated project

    if request.method == 'POST':
        task.delete()
        # Redirect back to project_list with the specific project context
        return redirect('project_list') + f"?project_id={project.id}"
    
    return render(request, 'Projects/task_confirm_delete.html', {'task': task, 'project': project})

def start_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST" and project.Status == "Pending":
        project.start_project()
    return redirect('project_detail', pk=pk)

def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST" and project.Status == "Ongoing":
        project.complete_project()
    return redirect('project_detail', pk=pk)

def cancel_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST" and project.Status == "Ongoing":
        project.cancel_project()
    return redirect('project_detail', pk=pk)