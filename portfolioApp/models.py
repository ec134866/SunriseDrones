from django.db import models
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery
import uuid
from django.utils import timezone


# Person Model
class Person(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    view = models.BooleanField(default=False)
    accessAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.name
      


# Owner Model
class Owner(models.Model):
    name = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255, blank=True, null=True)
    palette1 = models.CharField(max_length=50)
    palette2 = models.CharField(max_length=50)
    palette3 = models.CharField(max_length=50)
    logo = models.CharField(max_length=255, blank=True, null=True)
    person = models.ManyToManyField(Person, related_name='owners')

    def __str__(self):
        return self.name
    


# Property Model
class Property(models.Model):
    name = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255, blank=True, null=True)
    loc_city = models.CharField(max_length=255, blank=True, null=True)
    loc_state = models.CharField(max_length=255, blank=True, null=True)
    loc_country = models.CharField(max_length=255, blank=True, null=True)
    loc_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    loc_long = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    person = models.ManyToManyField(Person, related_name='properties')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='properties') 


    def __str__(self):
        return self.name
    class Meta:
        db_table = "properties"


# ScriptExterior Model
class ScriptExterior(models.Model):
    camera_far = models.CharField(max_length=20, blank=True, null=True, default="50000")
    camera_position = models.CharField(max_length=20, blank=True, null=True, default="75, 20, 100")
    camera_rotation = models.CharField(max_length=20, blank=True, null=True, default="-0.20, 0.63, 0.12")
    camera_axis = models.CharField(max_length=20, blank=True, null=True, default="0, 1, 0")
    model_position = models.CharField(max_length=20, blank=True, null=True, default="1,1,1")
    model_rotation_x = models.CharField(max_length=20, blank=True, null=True, default="-50")
    model_rotation_y = models.CharField(max_length=20, blank=True, null=True, default="22")
    model_rotation_z = models.CharField(max_length=20, blank=True, null=True, default="0")
    total_tiles = models.CharField(max_length=20, blank=True, null=True, default="100")
    max_distance = models.CharField(max_length=20, blank=True, null=True, default="1000")
    distance_increment = models.CharField(max_length=20, blank=True, null=True, default="0.06")
    height_increment = models.CharField(max_length=20, blank=True, null=True, default="0.04")

    def __str__(self):
        return f"Exterior Script {self.id}"


# ScriptInterior Model
class ScriptInterior(models.Model):
    camera_far = models.CharField(max_length=20, blank=True, null=True)
    camera_position = models.CharField(max_length=20, blank=True, null=True)
    camera_axis = models.CharField(max_length=20, blank=True, null=True)
    model_position = models.CharField(max_length=20, blank=True, null=True, default="1,1,1")
    model_rotation_x = models.CharField(max_length=20, blank=True, null=True, default="-50")
    model_rotation_y = models.CharField(max_length=20, blank=True, null=True, default="22")
    model_rotation_z = models.CharField(max_length=20, blank=True, null=True, default="0")
    max_camera_zoom = models.CharField(max_length=20, blank=True, null=True, default="100")

    def __str__(self):
        return f"Interior Script {self.id}"


# Flight Model
class Flight(models.Model):
    id = models.CharField(primary_key=True, max_length=7)  # format AA0001-ZZ9999
    date = models.DateField()
    overflight_link = models.CharField(max_length=500, blank=True, null=True)
    overflight_thumbnail_link = models.CharField(max_length=500, blank=True, null=True, default='https://drive.google.com/thumbnail?sz=w1000&id=1DrvmZ7DIML7RloNvJhN3EJXkeUhjBQL4')
    orthophoto_thumbnail_link = models.CharField(max_length=500, blank=True, null=True, default='https://drive.google.com/thumbnail?sz=w1000&id=1GTwESt8Gv4cXAQ_1VlpZOLZ4F9N4I-TR')
    # mapoverlay_thumbnail_link = models.CharField(max_length=500, blank=True, null=True, default='https://drive.google.com/thumbnail?sz=w1000&id=11aeANpVeqSGwX09q4HHAlQaa1TbdFbwk')
    # mapoverlay_link = models.CharField(max_length=500, blank=True, null=True)
    exterior_link = models.CharField(max_length=500, blank=True, null=True)
    exterior_thumbnail_link = models.CharField(max_length=500, blank=True, null=True, default='https://drive.google.com/thumbnail?sz=w1000&id=1Ya5AsuE7-DnTiz23hcqEtQOeOFZRqMsK')
    interior_link = models.CharField(max_length=500, blank=True, null=True)
    interior_thumbnail_link = models.CharField(max_length=500, blank=True, null=True, default='https://drive.google.com/thumbnail?sz=w1000&id=1e1izphrchnVWN7MZxa-BVffLZbDNAqvd')
    top_image_link_1 = models.CharField(max_length=500, blank=True, null=True, default='https://drive.google.com/thumbnail?sz=w1000&id=1Ya5AsuE7-DnTiz23hcqEtQOeOFZRqMsK')
    top_image_link_2 = models.CharField(max_length=500, blank=True, null=True, default='https://drive.google.com/thumbnail?sz=w1000&id=1Ya5AsuE7-DnTiz23hcqEtQOeOFZRqMsK')
    contractSigned = models.DateField(default=timezone.now)
    contractFlightDate = models.DateField(default=timezone.now)
    contractProcessingDate = models.DateField(default=timezone.now)
    contractFinalTouches = models.DateField(default=timezone.now)
    contractPublishDate = models.DateField(default=timezone.now)
    script_exterior = models.ForeignKey(ScriptExterior, on_delete=models.CASCADE, related_name='flights', blank=True, null=True)
    script_interior = models.ForeignKey(ScriptInterior, on_delete=models.CASCADE, related_name='flights', blank=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='flights')
    person = models.ManyToManyField(Person, related_name='flights')
    photo_content_btn_1 = models.CharField(max_length=6, blank=True, null=True, default="d-none")
    video_content_btn_1 = models.CharField(max_length=6, blank=True, null=True, default="d-none")
    # orthophoto_content_btn_1 = models.CharField(max_length=6, blank=True, null=True, default="d-none")
    # mapoverlay_content_btn_1 = models.CharField(max_length=6, blank=True, null=True, default="d-none")
    of_content_btn_1 = models.CharField(max_length=6, blank=True, null=True, default="d-none")
    of_content_btn_2 = models.CharField(max_length=6, blank=True, null=True, default="d-none")
    ext_content_btn_1 = models.CharField(max_length=6, blank=True, null=True, default="d-none")
    ext_content_btn_2 = models.CharField(max_length=6, blank=True, null=True, default="d-none")
    int_content_btn_1 = models.CharField(max_length=6, blank=True, null=True, default="d-none")
    int_content_btn_2 = models.CharField(max_length=6, blank=True, null=True, default="d-none")
    notice = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.id
    

class File(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    thumbnail = models.URLField()
    preview = models.URLField()
    direct_download_link = models.URLField()
    size_in_mb = models.DecimalField(max_digits=10, decimal_places=2)
    file_type = models.CharField(max_length=10)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return f"File {self.id}"
    


class PersonFlightAccess(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="flight_accesses")
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="person_accesses")
    access_contract = models.BooleanField(default=True)  
    access_files = models.BooleanField(default=True)     

    class Meta:
        unique_together = ("person", "flight") 

    def __str__(self):
        return f"{self.person.name} access for {self.flight.id}"