from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/create/<int:team_id>/', views.project_create, name='project_create'),  # Note: ',
    path('project/<int:pk>/edit/', views.project_update, name='project_update'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    # path('project/<int:project_id>/tasks/new/', views.task_create_for_project, name='task_create_for_project'),
    path('<int:pk>/tasks/', views.project_tasks, name='project_tasks'),
    path('project/<int:pk>/start/', views.start_project, name='project_start'),
    path('project/<int:pk>/complete/', views.complete_project, name='project_complete'),
    path('project/<int:pk>/cancel/', views.cancel_project, name='project_cancel'),

path('project_tasks/create/<int:ProjectId>/', views.project_task_create, name='project_task_create'),
    path('project_tasks/edit/<int:task_id>/', views.project_task_edit, name='project_task_edit'),
    path('project_tasks/delete/<int:task_id>/', views.project_task_delete, name='project_task_delete'),
]