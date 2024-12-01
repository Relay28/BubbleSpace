from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from Tasks.models import Task
from Teams.models import Team
from Login.models import Users_Account
from .forms import ProjectForm
from Tasks.forms import TaskForm,ProjectTaskForm
from django.contrib.auth.decorators import login_required
from Login.models import Users_Account 
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
# @login_required
# def project_list(request):
#     project_id = request.GET.get('project_id')  # Get project_id from query parameters
#     project = get_object_or_404(Project, pk=project_id) if project_id else Project.objects.first()

#     if not project:
#         return render(request, 'Projects/no_projects.html')  # Handle case where no projects exist

#     tasks = project.tasks.all()  # Get tasks for the specific project

    # Handle task creation
@login_required
def project_list(request, project_id):
    
    project = get_object_or_404(Project, pk=project_id)
    tasks = project.tasks.all()  # Assuming a related name for tasks in the Project model
    users = Users_Account.objects.all()
    form = ProjectTaskForm()

    return render(request, 'Projects/project_list.html', {
        'project': project,
        'tasks': tasks,
        'users': users,
        'form': form,  # Pass the task form
    })
def project_tasks(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=project)
    form = ProjectTaskForm(project=project)
    users = Users_Account.objects.all()
    return render(request, 'Projects/project_list.html', {'project': project, 'tasks': tasks , 'form':form , 'users': users})
@login_required
def project_task_create(request, ProjectId):
    project = get_object_or_404(Project, pk=ProjectId)

    if request.method == 'POST':
        form = ProjectTaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.created_by = request.user
            task.assigned_to = form.cleaned_data['assigned_to']
            task.save()
            return JsonResponse({'success': True, 'message': 'Task created successfully!'})

        # If form is invalid, return errors
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@login_required
def project_task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "Task updated successfully."})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = TaskForm(instance=task)
    return render(request, "edit_task.html", {"form": form, "task": task})

@login_required
def project_task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.delete()
        return JsonResponse({'success': True, 'message': 'Task deleted successfully.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)



# Project Detail View
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    team = Team.objects.filter(projects=project).first()  # Get the first team associated with this project
    return render(request, 'Projects/project_detail.html', {'project': project, 'tasks': tasks, 'team': team})


# Create Project View
@login_required
def project_create(request, team_id):
    print(f"Received team_id: {team_id}")  # Debugging line
    team = get_object_or_404(Team, pk=team_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            team.projects.add(project)
            return redirect('team_detail', pk=team.pk)
    else:
        form = ProjectForm()

    return render(request, 'teams/team_detail.html', {'form': form, 'team': team})


# Task Create for a Specific Project




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


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_list') + f"?project_id={task.project.id}"
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('project_list') + f"?project_id={task.project.id}"
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})