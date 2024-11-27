from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/new/<int:project_id>/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    # path('task/update_status/<int:pk>/', views.task_update_status, name='task_update_status'),
    # path('task/update_status/<int:pk>/', views.update_task_status, name='update_task_status'),
]