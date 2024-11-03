# urls.py
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('detail/<int:pk>/', views.team_detail, name='team_detail'),
    path('create/', views.team_create, name='team_create'),
    path('teams/<int:pk>/delete/', views.team_delete, name='team_delete'),
    path('detail/<int:pk>/add_member/', views.add_team_member, name='add_team_member'), 
      path('team/<int:pk>/edit/', views.team_edit, name='team_edit'), 
    # path('search-users/', views.search_users, name='search_users'),# New URL
   
]
