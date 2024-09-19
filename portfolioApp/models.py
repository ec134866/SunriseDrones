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

    def __str__(self):
        return self.name
    


# Owner Model
class Owner(models.Model):
    name = models.CharField(max_length=255)
    palette1 = models.CharField(max_length=50)
    palette2 = models.CharField(max_length=50)
    palette3 = models.CharField(max_length=50)
    logo = models.CharField(max_length=255)
    person = models.ManyToManyField(Person, related_name='owners')

    def __str__(self):
        return self.name
    


# Property Model
class Property(models.Model):
    name = models.CharField(max_length=255)
    loc_city = models.CharField(max_length=255, blank=True, null=True)
    loc_state = models.CharField(max_length=255, blank=True, null=True)
    loc_country = models.CharField(max_length=255, blank=True, null=True)
    loc_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    loc_long = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    person = models.ManyToManyField(Person, related_name='properties')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='properties')  # Updated


    def __str__(self):
        return self.name
    class Meta:
        db_table = "properties"

# Flight Model
class Flight(models.Model):
    id = models.CharField(primary_key=True, max_length=7)  # format AA0001-ZZ9999
    date = models.DateField()
    overflight_link = models.CharField(max_length=500, blank=True, null=True)
    overflight_thumbnail_link = models.CharField(max_length=500, blank=True, null=True, default='https://i.imgur.com/sdwvzXY.png')
    exterior_link = models.CharField(max_length=500, blank=True, null=True)
    exterior_thumbnail_link = models.CharField(max_length=500, blank=True, null=True, default='https://i.imgur.com/ygVbLkU.png')
    interior_link = models.CharField(max_length=500, blank=True, null=True)
    interior_thumbnail_link = models.CharField(max_length=500, blank=True, null=True, default='https://i.imgur.com/nS0QSnM.png')
    top_image_link_1 = models.CharField(max_length=500, blank=True, null=True)
    top_image_link_2 = models.CharField(max_length=500, blank=True, null=True)
    contractSigned = models.DateField(default=timezone.now)
    contractFlightDate = models.DateField(default=timezone.now)
    contractProcessingDate = models.DateField(default=timezone.now)
    contractPublishDate = models.DateField(default=timezone.now)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='flight')
    person = models.ManyToManyField(Person, related_name='flights')

    def __str__(self):
        return self.id
    

    # maybe fix? 
    
