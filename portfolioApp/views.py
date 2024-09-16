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


    owner = Owner.objects.filter(person=person)

    if owner.exists():
        if owner.count() > 1:
            owner_name = "Owner View"
        else:
            owner_name = owner.first().name
    else:
        owner_name = "Owner View"

    
    context = {
        'person': person,
        'owner_name': owner_name,
        'owner' : owner
    }

    return render(request, 'portfolioApp/index.html', context)

def indexPageView(request):
   
    context = {}

    return render(request, 'portfolioApp/index.html', context)

def ownerPageView(request, person_uuid):
    
    person = get_object_or_404(Person, uuid=person_uuid)
    owner = Owner.objects.filter(person=person)
    properties = Property.objects.filter(person=person, owner=owner)

    for prop in properties:
        prop.latest_flight = Flight.objects.filter(property=prop).order_by('-date').first()

    if owner.exists():
        if owner.count() > 1:
            owner_name = "Owner View"
            owner_palette1 = "(179, 9, 56, 1)"
        else:
            owner_name = owner.first().name + " Properties"
            owner_palette1 = owner.first().palette1
    else:
        owner_name = "Owner View"
        owner_palette1 = "(179, 9, 56, 1)"

    context = {
        'person': person,
        'owner': owner,
        'owner_name': owner_name,
        'owner_palette1': owner_palette1,
        'properties': properties
    }

    return render(request, 'portfolioApp/owner.html', context)

def propertyPageView(request, person_uuid, property_name):
   
    person = get_object_or_404(Person, uuid=person_uuid)
    owner = Owner.objects.filter(person=person)
    property = get_object_or_404(Property, name=property_name, person=person)
    flights = Flight.objects.filter(property=property).order_by('-date')
    
    selected_date = request.GET.get('date')
    if not selected_date:
        selected_date = flights.first().date 

    selected_flight = Flight.objects.filter(property=property, date=selected_date).first()

    if owner.exists():
        if owner.count() > 1:
            owner_name = "Owner View"
            owner_palette1 = "(179, 9, 56, 1)"
        else:
            owner_name = owner.first().name
            owner_palette1 = owner.first().palette1
    else:
        owner_name = "Owner View"
        owner_palette1 = "(179, 9, 56, 1)"


    context = {
        'person': person,
        'owner': owner,
        'owner_name': owner_name,
        'owner_palette1': owner_palette1,
        'property': property,
        'flights': flights,
        'selected_flight': selected_flight
    }

    return render(request, 'portfolioApp/property.html', context)

