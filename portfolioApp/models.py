from django.db import models
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery


class property(models.Model):
    flight_id = models.AutoField(primary_key=True)
    flight_date = models.DateField()
    property_name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)

    owner_poc_name = models.CharField(max_length=150, blank=True, null=True)
    owner_poc_phone_number = models.CharField(max_length=20, blank=True, null=True)
    owner_poc_email = models.EmailField(max_length=255, blank=True, null=True)
    
    loc_city = models.CharField(max_length=100, blank=True, null=True)
    loc_state = models.CharField(max_length=100, blank=True, null=True)
    loc_country = models.CharField(max_length=150, blank=True, null=True)
    loc_lat = models.CharField(max_length=255, blank=True, null=True)
    loc_long = models.CharField(max_length=255, blank=True, null=True)

    loc_poc_name = models.CharField(max_length=150, blank=True, null=True)
    loc_poc_phone_number = models.CharField(max_length=20, blank=True, null=True)
    loc_poc_email = models.EmailField(max_length=255, blank=True, null=True)
    
    top_image_link1 = models.URLField(max_length=500, blank=True, null=True)
    top_image_link2 = models.URLField(max_length=500, blank=True, null=True)
    top_image_link3 = models.URLField(max_length=500, blank=True, null=True)
    
    overflight_video_link = models.URLField(max_length=500, blank=True, null=True)
    exterior_model_link = models.URLField(max_length=500, blank=True, null=True)
    interior_model_link = models.URLField(max_length=500, blank=True, null=True)
    
    overflight_image_link = models.URLField(max_length=500, blank=True, null=True)
    exterior_image_link = models.URLField(max_length=500, blank=True, null=True)
    interior_image_link = models.URLField(max_length=500, blank=True, null=True)
   
     
    def __str__(self):
        return self.property_name

    class Meta:
        db_table = "properties"