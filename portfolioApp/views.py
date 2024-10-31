from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Person, Owner, Property, Flight, ScriptExterior, ScriptInterior, File, PersonFlightAccess
from .forms import PersonForm 

# Create your views here.

def basePageView(request):
    person_uuid = request.GET.get('person_uuid') or request.session.get('person_uuid')
    person = None
    if person_uuid:
        person = get_object_or_404(Person, uuid=person_uuid)
        request.session['person_uuid'] = person_uuid


    owners = Owner.objects.filter(person=person)

    nav_properties = Property.objects.filter(person=person)

    
    context = {
        'person': person,
        'owners' : owners,
        'nav_properties': nav_properties
    }

    return render(request, 'portfolioApp/index.html', context)





def indexPageView(request):
    
    person_uuid = request.GET.get('person_uuid') or request.session.get('person_uuid')
    person = None
    if person_uuid:
        person = get_object_or_404(Person, uuid=person_uuid)
        # Store UUID in session to persist it for navigation
        request.session['person_uuid'] = person_uuid


    property = get_object_or_404(Property, name='Herndon Community Center')
    flights = Flight.objects.filter(property=property).order_by('-date')

    selected_date = request.GET.get('date')
    if not selected_date:
        selected_date = flights.first().date 

    selected_flight = Flight.objects.filter(property=property, date=selected_date).first()

    script_exterior = selected_flight.script_exterior if selected_flight else None
    script_interior = selected_flight.script_interior if selected_flight else None
    notice = selected_flight.notice if selected_flight else None
    files = selected_flight.files.all() if selected_flight else None
   
    context = {
        'person': person,
        'flights': flights,
        'selected_flight': selected_flight,
        'script_exterior': script_exterior,
        'script_interior': script_interior,
        'files': files,
        'notice': notice,
        }

    return render(request, 'portfolioApp/index.html', context)


def testPageView(request):
   

    return render(request, 'portfolioApp/test.html')



def ownerPageView(request, person_uuid):
    
    request.session['person_uuid'] = person_uuid

    person = get_object_or_404(Person, uuid=person_uuid)
    owners = Owner.objects.filter(person=person)
    nav_properties = Property.objects.filter(person=person)
    
    properties_by_owner = []
    for owner in owners:
        properties = Property.objects.filter(owner=owner, person=person)

        for prop in properties:
            prop.latest_flight = Flight.objects.filter(property=prop).order_by('-date').first()
        properties_by_owner.append((owner, properties))

    if owners.exists():
        if owners.count() > 1:
            owner_name = "Owner Suite"
            owner_palette1 = "(174,225,174,1)"
        else:
            owner_name = owners.first().name + " Properties"
            owner_palette1 = owners.first().palette1
    else:
        owner_name = "Owner Suite"
        owner_palette1 = "(174,225,174,1)"

    context = {
        'person': person,
        'owners': owners,
        'owner_name': owner_name,
        'owner_palette1': owner_palette1,
        'properties_by_owner': properties_by_owner,
        'nav_properties': nav_properties,
        'person_uuid': str(person.uuid),
    }

    return render(request, 'portfolioApp/owner.html', context)




def propertyPageView(request, person_uuid, owner_name, property_name):

    request.session['person_uuid'] = person_uuid
   
    person = get_object_or_404(Person, uuid=person_uuid)
    owner = get_object_or_404(Owner, name=owner_name, person=person)
    property = get_object_or_404(Property, name=property_name, person=person)
    flights = Flight.objects.filter(property=property).order_by('-date')
    nav_properties = Property.objects.filter(person=person)
    
    selected_date = request.GET.get('date')
    if not selected_date:
        selected_date = flights.first().date 

    selected_flight = Flight.objects.filter(property=property, date=selected_date).first()

    script_exterior = selected_flight.script_exterior if selected_flight else None
    script_interior = selected_flight.script_interior if selected_flight else None
    notice = selected_flight.notice if selected_flight else None
    files = selected_flight.files.all() if selected_flight else None

    access_contract = None
    access_files = None
    if selected_flight:
        try:
            person_flight_access = PersonFlightAccess.objects.get(person=person, flight=selected_flight)
            access_contract = person_flight_access.access_contract
            access_files = person_flight_access.access_files
        except ObjectDoesNotExist:
            pass

    context = {
        'person': person,
        'owner': owner,
        'owner_name': owner_name,
        'property': property,
        'nav_properties': nav_properties,
        'person_uuid': str(person.uuid),
        'flights': flights,
        'selected_flight': selected_flight,
        'script_exterior': script_exterior,
        'script_interior': script_interior,
        'access_contract': access_contract,
        'access_files': access_files,
        'files': files,
        'notice': notice,
    }

    return render(request, 'portfolioApp/property.html', context)


def feedbackPageView(request):
    
    context = {}
    
    return render(request, 'portfolioApp/form.html')


def managementPageView(request, person_uuid=None):
    # If person_uuid is provided, fetch the person; otherwise create a new instance
    person = get_object_or_404(Person, uuid=person_uuid) if person_uuid else None
    person_form = PersonForm(instance=person)

    # Filter accessible data based on the person identified by uuid
    accessible_owners = Owner.objects.filter(person=person) if person else Owner.objects.all()
    accessible_properties = Property.objects.filter(owner__in=accessible_owners) if person else Property.objects.all()
    accessible_flights = Flight.objects.filter(property__in=accessible_properties) if person else Flight.objects.all()

    # Update form field querysets
    person_form.fields['owners'].queryset = accessible_owners
    person_form.fields['properties'].queryset = accessible_properties
    person_form.fields['flights'].queryset = accessible_flights

    if request.method == "POST":
        # Handle form submission
        person_form = PersonForm(request.POST, instance=person)
        if person_form.is_valid():
            new_person = person_form.save()
            return redirect('management', person_uuid=new_person.uuid)

    context = {
        'persons': Person.objects.all(),
        'person_form': person_form,
        'person': person,
    }
    
    return render(request, 'portfolioApp/management.html', context)