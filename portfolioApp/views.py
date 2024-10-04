from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Person, Owner, Property, Flight, ScriptExterior, ScriptInterior, File

# Create your views here.

def basePageView(request):
    person_uuid = request.session.get('person_uuid', None)
    person = None
    if person_uuid:
        person = get_object_or_404(Person, uuid=person_uuid)


    owners = Owner.objects.filter(person=person)

    properties_by_owner = []
    for owner in owners:
        properties = Property.objects.filter(owner=owner, person=person)
        properties_by_owner.append((owner, properties))
    
    context = {
        'person': person,
        'owners' : owners,
        'properties_by_owner': properties_by_owner
    }

    return render(request, 'portfolioApp/index.html', context)





def indexPageView(request):
   
    context = {}

    return render(request, 'portfolioApp/index.html', context)




def ownerPageView(request, person_uuid):
    
    person = get_object_or_404(Person, uuid=person_uuid)
    owners = Owner.objects.filter(person=person)
    
    properties_by_owner = []
    for owner in owners:
        properties = Property.objects.filter(owner=owner, person=person)

        for prop in properties:
            prop.latest_flight = Flight.objects.filter(property=prop).order_by('-date').first()
        properties_by_owner.append((owner, properties))

    if owners.exists():
        if owners.count() > 1:
            owner_name = "The Owner Suite"
            owner_palette1 = "(174,225,174,1)"
        else:
            owner_name = owners.first().name + " Properties"
            owner_palette1 = owners.first().palette1
    else:
        owner_name = "The Owner Suite"
        owner_palette1 = "(174,225,174,1)"

    context = {
        'person': person,
        'owners': owners,
        'owner_name': owner_name,
        'owner_palette1': owner_palette1,
        'properties_by_owner': properties_by_owner
    }

    return render(request, 'portfolioApp/owner.html', context)




def propertyPageView(request, person_uuid, owner_name, property_name):
   
    person = get_object_or_404(Person, uuid=person_uuid)
    owner = get_object_or_404(Owner, name=owner_name, person=person)
    property = get_object_or_404(Property, name=property_name, person=person)
    flights = Flight.objects.filter(property=property).order_by('-date')
    
    selected_date = request.GET.get('date')
    if not selected_date:
        selected_date = flights.first().date 

    selected_flight = Flight.objects.filter(property=property, date=selected_date).first()

    script_exterior = selected_flight.script_exterior if selected_flight else None
    script_interior = selected_flight.script_interior if selected_flight else None
    files = selected_flight.files.all() if selected_flight else None

    context = {
        'person': person,
        'owner': owner,
        'owner_name': owner_name,
        'property': property,
        'flights': flights,
        'selected_flight': selected_flight,
        'script_exterior': script_exterior,
        'script_interior': script_interior,
        'files': files,
    }

    return render(request, 'portfolioApp/property.html', context)

