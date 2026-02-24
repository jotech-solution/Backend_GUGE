from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def logIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=username, password=pwd)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Identifiants incorrects")
    return render(request, 'login.html')

def ask_logout(request):
    return render(request, 'logout.html')

def logOut(request):
    logout(request)
    return redirect('login')