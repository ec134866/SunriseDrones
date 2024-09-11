from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
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
    
    selected_date = request.GET.get('date')

    if selected_date:
        try:
            parsed_date = parse_date(selected_date)
            if parsed_date:
                flights = Flight.objects.filter(property=property, date=parsed_date).order_by('-date')
            else:
                flights = Flight.objects.filter(property=property).order_by('-date')
        except ValueError:
            flights = Flight.objects.filter(property=property).order_by('-date')
    else:
        flights = Flight.objects.filter(property=property).order_by('-date')

    context = {
        'person': person,
        'property': property,
        'flights': flights,
        'latest_flight': flights.first(),
        'selected_date': selected_date,
    }

    return render(request, 'portfolioApp/property.html', context)

