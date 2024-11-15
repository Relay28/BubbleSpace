# notes/urls.py
from django.urls import path
from . import views  # Import views module

urlpatterns = [
    path('', views.notes_list, name='notes_list'),  # Reference notes_list from views
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('add/', views.add_note, name='add_note'),  # URL pattern for adding a note
    path('note/<int:pk>/edit/', views.edit_note, name='edit_note'),
    path('note/<int:pk>/delete/', views.delete_note, name='delete_note'),
]