from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Person, Owner, Property, Flight, ScriptExterior, ScriptInterior, File, PersonFlightAccess
from .forms import PersonForm 
# aws asset management for property files
import boto3
from secretas import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_REGION
from botocore.exceptions import ClientError
from urllib.parse import urlparse
# zipstream 
import json
import zipstream
from django.http import StreamingHttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST

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




def propertyPageView(request, person_uuid, owner_url_name, property_url_name):
   
    person = get_object_or_404(Person, uuid=person_uuid)
    owner = get_object_or_404(Owner, url_name=owner_url_name, person=person)
    property = get_object_or_404(Property, url_name=property_url_name, person=person)
    flights = Flight.objects.filter(property=property).order_by('-date')
    nav_properties = Property.objects.filter(person=person)
    
    selected_date = request.GET.get('date')
    if not selected_date:
        selected_date = flights.first().date 

    selected_flight = Flight.objects.filter(property=property, date=selected_date).first()

    script_exterior = selected_flight.script_exterior if selected_flight else None
    script_interior = selected_flight.script_interior if selected_flight else None
    notice = selected_flight.notice if selected_flight else None

    access_contract = None
    access_files = None
    if selected_flight:
        try:
            person_flight_access = PersonFlightAccess.objects.get(person=person, flight=selected_flight)
            access_contract = person_flight_access.access_contract
            access_files = person_flight_access.access_files
        except ObjectDoesNotExist:
            pass
    
    files = []
    if selected_flight and selected_flight.s3_prefix and access_files:
        for subdir in ['photos/', 'videos/', 'models/', 'maps/', 'zips/', 'other/']:
            files.extend(list_s3_files(f"{selected_flight.s3_prefix}{subdir}"))



    context = {
        'person': person,
        'owner': owner,
        'owner_url_name' : owner_url_name,
        'property': property,
        'property_url_name': property_url_name,
        'nav_properties': nav_properties,
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

def list_s3_files(prefix):
    """
    List all objects under a given S3 prefix.
    Returns a list of dicts with keys: name, size_in_mb, file_type, direct_download_link, thumbnail, preview
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )
    
    try:
        response = s3.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix=prefix)
        contents = response.get('Contents', [])
    except ClientError:
        return []

    files = []
    cdn_base = "https://cdn.balancedrockimaging.com/"
    
    for obj in contents:
        key = obj['Key']
        if key.endswith('/'):
            continue
        
        file_type = "Unknown"
        if any(key.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.tif']):
            file_type = "Image"
        elif any(key.lower().endswith(ext) for ext in ['.mp4', '.mov', '.avi']):
            file_type = "Video"
        elif key.lower().endswith('.zip'):
            file_type = "Zip"
        elif any(key.lower().endswith(ext) for ext in ['.glb', '.obj', '.gltf']):
            file_type = "3D Model"
        else:
            file_type = "Unknown"
        
        s3_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"
        cdn_url = cdn_base + key

        files.append({
            "name": key.split('/')[-1],
            "size_in_mb": round(obj['Size'] / (1024 * 1024), 2),
            "file_type": file_type,
            "direct_download_link": s3_url,
            "thumbnail": cdn_url,
            "preview": cdn_url,
            "key": key
        })
    
    return files

@require_POST
def download_zip(request):
    try:
        data = json.loads(request.body)
        keys = data.get("files", [])
        flight_id = data.get("flight_id")
    except:
        return HttpResponseForbidden("Invalid request.")

    if not keys or not flight_id:
        return HttpResponseForbidden("Missing data.")

    person_uuid = request.session.get("person_uuid")
    if not person_uuid:
        return HttpResponseForbidden("Not authenticated.")

    person = get_object_or_404(Person, uuid=person_uuid)
    flight = get_object_or_404(Flight, id=flight_id)

    try:
        access = PersonFlightAccess.objects.get(person=person, flight=flight)
        if not access.access_files:
            return HttpResponseForbidden("No file access.")
    except PersonFlightAccess.DoesNotExist:
        return HttpResponseForbidden("No permission.")

    allowed_prefix = flight.s3_prefix
    for key in keys:
        if not key.startswith(allowed_prefix):
            return HttpResponseForbidden("Invalid file requested.")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    z = zipstream.ZipFile(mode="w", compression=zipstream.ZIP_DEFLATED)

    for key in keys:
        try:
            s3_object = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)
            filename = key.split("/")[-1]

            # Correct streaming of file body
            def file_iter():
                for chunk in iter(lambda: s3_object['Body'].read(8192), b''):
                    yield chunk

            z.write_iter(filename, file_iter())
        except Exception as e:
            print(f"Skipping {key}: {e}")
            continue

    response = StreamingHttpResponse(z, content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="flight_{flight.id}_files.zip"'
    return response