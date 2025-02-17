from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt

def signup(request):
    if request.method == "POST":

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():


            user = form.save()

            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
