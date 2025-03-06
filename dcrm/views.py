# dcrm/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from website.forms import SignupForm

def home(request):
    return render(request, 'website/home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('dashboard')  # Redirect to home page after login
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'website/home.html')

    return render(request, 'website/home.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'website/dashboard.html')



def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = SignupForm()

    return render(request, 'website/register.html', {'form': form})
