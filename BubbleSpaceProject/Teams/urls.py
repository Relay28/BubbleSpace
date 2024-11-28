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
    path('search-members/', views.search_member, name='search_member'),
    path('team/<int:team_id>/remove_member/<int:member_id>/', views.remove_team_member, name='remove_team_member'),
    path('teams/<int:team_id>/transfer/<int:member_id>/', views.transfer_ownership, name='transfer_ownership'),
    path('teams/<int:team_id>/leave/', views.leave_team, name='leave_team'),
   
]
