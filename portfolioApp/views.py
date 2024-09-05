import json
from django.conf import settings
from plaid import Client
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required


client = Client(client_id=settings.PLAID_CLIENT_ID,
                secret=settings.PLAID_SECRET,
                environment=settings.PLAID_ENV)

def get_link_token(request):
    response = client.LinkToken.create({
        'user': {
            'client_user_id': 'unique_user_id',
        },
        'client_name': 'Your App Name',
        'products': ['auth'],
        'country_codes': ['US'],
        'language': 'en',
    })
    return JsonResponse(response)

def exchange_public_token(request):
    public_token = request.POST.get('public_token')
    exchange_response = client.Item.public_token.exchange(public_token)
    access_token = exchange_response['access_token']
    request.session['access_token'] = access_token
    return HttpResponse(status=200)

def get_balances(request):
    access_token = request.session['access_token']
    balance_response = client.Accounts.balance.get(access_token)
    accounts = balance_response['accounts']
    return render(request, 'balances.html', {'accounts': accounts})


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

def sunrisePageView(request):
    
    context = {}

    return render(request, 'portfolioApp/sunrise.html', context)

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
