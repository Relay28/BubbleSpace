from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users_Account
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST

            username = data.get('username')
            password = data.get('password')
            fname = data.get('fname')
            lname = data.get('lname')
            gender = data.get('gender')
            birthDate = data.get('birthDate')

            # Check if the username already exists
            if Users_Account.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            # Create and save the new user
            user = Users_Account(username=username, fname=fname, lname=lname, gender=gender, birthDate=birthDate)
            user.set_password(password)
            user.save()
            return redirect('login') 

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return render(request, 'Register/register_account.html')

def custom_authenticate(username, password):
    try:
        user = Users_Account.objects.get(username=username)
        if check_password(password, user.password):
            return user
    except Users_Account.DoesNotExist:
        return None
    return None

def login_view(request):
    errors = {"username": None, "password": None}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after login
        else:
            # Set error messages for invalid fields
            if not username:
                errors["username"] = "Username is required."
            if not password:
                errors["password"] = "Password is required."
            else:
                errors["username"] = "Invalid credentials."  # Generic error for invalid username/password

    return render(request, 'Login/login_account.html', {"errors": errors})



def home_view(request):
    return render(request, 'Home/Home.html')

@login_required
def appbar_view(request):
    return render(request, 'base.html', {
        'user': request.user  # Ensure user data is passed
    })

def help_view(request):
    return render(request, 'Help/helppage.html')

def profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        user_data = {
            "username": user.username,
            "fname": user.fname,
            "lname": user.lname,
            "gender": user.gender,
            "birthDate": user.birthDate.strftime('%d/%m/%Y'),  # Format as needed
            "age": user.age,
             "profile_picture": user.profile_picture.url if user.profile_picture else None  # Add profile picture URL
        }
        return render(request, 'Profile/profile_account.html', user_data)
    return redirect('login')

@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        birthDate = request.POST.get('birthDate')
        password = request.POST.get('password')

        profile_picture = request.FILES.get('profile_picture')

        user.fname = fname
        user.lname = lname
        user.gender = gender
        user.birthDate = birthDate
        if password:
            user.set_password(password)
        if profile_picture:
            user.profile_picture = profile_picture
        user.save()

        return redirect('profile')

    context = {
        'username': user.username,
        'fname': user.fname,
        'lname': user.lname,
        'gender': user.gender,
        'birthDate': user.birthDate,
        'profile_picture': user.profile_picture.url if user.profile_picture else None,
    }
    return render(request, 'Profile/edit_profile.html', context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return JsonResponse({"error": "User not authenticated or invalid request method"}, status=403)
    
@login_required
@require_POST
def delete_account_view(request):
    user = request.user
    user.delete()  # Delete the user account
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page