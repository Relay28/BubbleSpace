from django.urls import include, path
from .views import register_view, login_view, home_view, profile_view, edit_profile_view, logout_view, delete_account_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('logout/', logout_view, name='logout'),
    path('delete-account/', delete_account_view, name='delete_account'),  
    path('notes/', include('notes.urls'), name="notes"), # Notes App
    path('tasks/', include('Tasks.urls')), #Tasks App
    path('messages/', include('Messages.urls')), #messages App
    path('projects/', include('Projects.urls')), #projects App
]
