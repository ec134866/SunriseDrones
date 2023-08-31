from django.shortcuts import render
from django.http import HttpResponse

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
