from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Person, Owner, Property, Flight, ScriptExterior, ScriptInterior, File
from django.core.mail import send_mail
from django.conf import settings
from .forms import FeedbackForm

# Create your views here.

def basePageView(request):
    person_uuid = request.session.get('person_uuid', None)
    person = None
    if person_uuid:
        person = get_object_or_404(Person, uuid=person_uuid)


    owners = Owner.objects.filter(person=person)

    nav_properties = Property.objects.filter(person=person)

    
    context = {
        'person': person,
        'owners' : owners,
        'nav_properties': nav_properties
    }

    return render(request, 'portfolioApp/index.html', context)





def indexPageView(request):
   
    context = {}

    return render(request, 'portfolioApp/index.html', context)


def testPageView(request):
   

    return render(request, 'portfolioApp/test.html')



def ownerPageView(request, person_uuid):
    
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
        'nav_properties': nav_properties
    }

    return render(request, 'portfolioApp/owner.html', context)




def propertyPageView(request, person_uuid, owner_name, property_name):
   
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
    files = selected_flight.files.all() if selected_flight else None

    context = {
        'person': person,
        'owner': owner,
        'owner_name': owner_name,
        'property': property,
        'nav_properties': nav_properties,
        'flights': flights,
        'selected_flight': selected_flight,
        'script_exterior': script_exterior,
        'script_interior': script_interior,
        'files': files,
    }

    return render(request, 'portfolioApp/property.html', context)


def feedbackPageView(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()

            send_mail(
                subject=f"New {feedback.feedback_type.capitalize()}",
                message=(
                    f"Name: {feedback.name or 'Anonymous'}\n"
                    f"Email: {feedback.email or 'Not provided'}\n"
                    f"Number: {feedback.number or 'Not provided'}\n\n"
                    f"Message:\n{feedback.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['evan@thecarters.com'],
            )
            return redirect('feedback_success')
    else:
        form = FeedbackForm()
    
    return render(request, 'portfolioApp/form.html', {'form': form})
