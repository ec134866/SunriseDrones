from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# Create your views here.

def indexPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/index.html', context)

def analystPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/analyst.html', context)

def dunkerPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/dunker.html', context)

def sideprojectPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/sideprojects.html', context)

def threeDPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/threeD.html', context)


def translationPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/translation.html', context)

def oceanCleanupPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/oceancleanup.html', context)

def loginPageView(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('character')
        else:
            error_message = "Invalid Username or Password" 

    return render(request, 'portfolioApp/login.html', {'error_message': error_message})

# @login_required

def characterView(request):
    return render(request, 'portfolioApp/character.html')
