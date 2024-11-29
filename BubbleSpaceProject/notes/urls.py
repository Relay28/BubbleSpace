# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_list, name='notes_list'),
    path('add/', views.add_note, name='add_note'),
    path('note-detail/<int:pk>/', views.note_detail_api, name='note_detail_api'),
    # path('note-detail/<int:pk>/edit/', views.edit_note, name='edit_note'),
    # path('note-detail/<int:pk>/delete/', views.delete_note, name='delete_note'),
]
