from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Task
from Projects.models import Project
from .forms import TaskForm
from django.http import JsonResponse
## views.py
from django.shortcuts import render
from .models import Task

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def task_list(request):
    tasks = Task.objects.filter(created_by=request.user, project__isnull=True)
    form = TaskForm()
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter) 
    return render(request, 'tasks/task_list.html', {'tasks': tasks,'status_filter': status_filter,'form':form})



@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()

            # If the request is AJAX, send a JSON response
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
                    'status': task.status,
                }, status=201)
            
            # Redirect for non-AJAX requests
            return redirect('task_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create New Task'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Update Task'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
def update_task_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id)
        
        # Get the new status from the request body (assuming it comes in JSON format)
        status = request.POST.get('status')
        
        # Validate the status
        if status in ['green', 'yellow', 'red']:
            task.status = status
            task.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid status'})
