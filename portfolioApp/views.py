from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Person, Owner, Property, Flight

# Create your views here.

def basePageView(request):
    person_uuid = request.session.get('person_uuid', None)
    person = None
    if person_uuid:
        person = get_object_or_404(Person, uuid=person_uuid)
    
    context = {
        'person': person
    }

    return render(request, 'portfolioApp/index.html', context)

def indexPageView(request):
   
    context = {}

    return render(request, 'portfolioApp/index.html', context)

def ownerPageView(request, person_uuid):
    
    person = get_object_or_404(Person, uuid=person_uuid)
    owners = Owner.objects.filter(person=person)
    properties = Property.objects.filter(person=person)

    context = {
        'person': person,
        'owners': owners,
        'properties': properties
    }

    return render(request, 'portfolioApp/owner.html', context)

def propertyPageView(request, person_uuid, property_name):
   
    person = get_object_or_404(Person, uuid=person_uuid)
    owners = Owner.objects.filter(person=person)
    property = get_object_or_404(Property, name=property_name, person=person)
    flights = Flight.objects.filter(property=property).order_by('-date')
    
    selected_date = request.GET.get('date')
    if not selected_date:
        selected_date = flights.last().date 

    selected_flight = Flight.objects.filter(property=property, date=selected_date).first()


    context = {
        'person': person,
        'owners': owners,
        'property': property,
        'flights': flights,
        'selected_flight': selected_flight,
        'latest_flight': flights.last()
    }

    return render(request, 'portfolioApp/property.html', context)

