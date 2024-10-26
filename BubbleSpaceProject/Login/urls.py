from django.urls import path
from .views import register_view, login_view, profile_view, logout_view,home_view,edit_profile_view

urlpatterns = [
     path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path("home/",home_view,name="home"),
    path('profile/', profile_view, name="profile"),
     path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('logout/', logout_view, name="logout"),
]
    