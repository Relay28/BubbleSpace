from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Users_Account
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'Login/login_account.html', {"error": "Invalid credentials"})
    
    return render(request, 'Login/login_account.html')

def home_view(request):
    return render(request, 'Home/Home.html')

def profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        user_data = {
            "username": user.username,
            "fname": user.fname,
            "lname": user.lname,
            "gender": user.gender,
            "birthDate": user.birthDate.strftime('%d/%m/%Y'),  # Format as needed
            "age": user.age
        }
        return render(request, 'Profile/profile_account.html', user_data)
    return redirect('login')

@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        # Get updated data from the form
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        birthDate = request.POST.get('birthDate')
        password = request.POST.get('password')

        # Update the user's data
        user.fname = fname
        user.lname = lname
        user.gender = gender
        user.birthDate = birthDate
        if password:
            user.set_password(password)
        user.save()

        # Redirect back to profile page after saving changes
        return redirect('profile')

    # Pass user data to the template
    context = {
        'username': user.username,
        'fname': user.fname,
        'lname': user.lname,
        'gender': user.gender,
        'birthDate': user.birthDate
    }
    return render(request, 'Profile/edit_profile.html', context)

def logout_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        logout(request)
        return redirect('login')
    return JsonResponse({"error": "User not authenticated or invalid request method"}, status=403)
