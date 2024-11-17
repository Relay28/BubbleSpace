from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/create/<int:team_id>/', views.project_create, name='project_create'),  # Note: ',
    path('project/<int:pk>/edit/', views.project_update, name='project_update'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('project/<int:project_id>/tasks/new/', views.task_create_for_project, name='task_create_for_project'),
    path('<int:pk>/tasks/', views.project_tasks, name='project_tasks'),
]