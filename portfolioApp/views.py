from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

# Create your views here.

def indexPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/index.html', context)

def ownerPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/owner.html', context)

def propertyPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/property.html', context)


def overflightPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/overflight.html', context)


def threeDexteriorPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/threeDexterior.html', context)


def threeDinteriorPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/threeDinterior.html', context)

def sideprojectPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/sideprojects.html', context)

def sunrisePageView(request):
    
    context = {}

    return render(request, 'portfolioApp/sunrise.html', context)

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
