from django.contrib import admin
from .models import Person, Owner, Property, Flight, ScriptExterior, ScriptInterior, File


class PersonID(admin.ModelAdmin):
    readonly_fields = ('uuid',)

class FilterFlight(admin.ModelAdmin):
    list_display = ("id", "date", "property", "get_owner_name", "get_person_names")
    list_filter = ("date", "property__name", "property__owner__name", "person__name")
    
    def get_owner_name(self, obj):
        return obj.property.owner.name
    get_owner_name.short_description = 'Owner'
    
    def get_person_names(self, obj):
        return ", ".join([person.name for person in obj.person.all()])
    get_person_names.short_description = 'Persons'


class FilterProperty(admin.ModelAdmin):
    list_display = ("name", "loc_city", "loc_state", "loc_country", "person", "owner")
    list_filter = ("name", "loc_city", "loc_state", "loc_country", "person", "owner")

class FilterFile(admin.ModelAdmin):
    list_display = ("name", "link", "thumbnail", "direct_download_link", "size_in_mb", "file_type", "flight")
    list_filter = ("flight", "file_type", "name", "size_in_mb")

admin.site.register(Person, PersonID)
admin.site.register(Owner)
admin.site.register(Property, FilterProperty)
admin.site.register(ScriptExterior)
admin.site.register(ScriptInterior)
admin.site.register(File, FilterFile)
admin.site.register(Flight, FilterFlight)
