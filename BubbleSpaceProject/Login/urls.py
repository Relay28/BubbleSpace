from django.urls import include, path
from .views import register_view, login_view, home_view, profile_view, edit_profile_view, logout_view, delete_account_view, help_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
     path('help/', help_view, name='help'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('logout/', logout_view, name='logout'),
    path('delete-account/', delete_account_view, name='delete_account'),  
    path('notes/', include('notes.urls'), name="notes"), # Notes App
    path('tasks/', include('Tasks.urls')), #Tasks App
    path('messages/', include('Messages.urls')), #messages App
    path('projects/', include('Projects.urls')), #projects App
    path('teams/',include("Teams.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
