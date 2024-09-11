from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Person, Owner, Property, Flight

# Create your views here.

def indexPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/index.html', context)

def ownerPageView(request, person_uuid):
    
    person = get_object_or_404(Person, uuid=person_uuid)
    
    properties = Property.objects.filter(person=person)

    owners = Owner.objects.filter(person=person)

    context = {
        'person': person,
        'properties': properties,
        'owners': owners
    }

    return render(request, 'portfolioApp/owner.html', context)

def propertyPageView(request, person_uuid, property_name):
   
    person = get_object_or_404(Person, uuid=person_uuid)
    
    property = get_object_or_404(Property, name=property_name, person=person)
    
    flight = Flight.objects.filter(property=property).first()
    
    context = {
        'person': person,
        'property': property,
        'flight': flight
    }

    return render(request, 'portfolioApp/property.html', context)




# delete below


def overflightPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/overflight.html', context)


def threeDexteriorPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/exterior.html', context)


def threeDinteriorPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/interior.html', context)

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

