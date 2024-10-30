from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('/')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:    
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists! Please try another.")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists! Please try another.")
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1, email=email)
                user.save()
                messages.info(request, "User created.")
                return redirect('login')
        else:
            messages.info(request, "Passwords do not match!")
            return redirect('register')
    else:
        return render(request, 'register.html')

@csrf_exempt  # This decorator is necessary to allow non-POST methods in development
def update_profile(request):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            user = request.user  # Get the currently logged-in user
            
            # Update user fields
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.email = data.get('email', user.email)
            
            # Save changes
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')  # Redirect to a profile page or wherever you want
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('profile')  # Handle error by redirecting

    return render(request, 'profile.html')  # GET request renders the profile page
