from django.contrib import admin
from .models import Person, Owner, Property, Flight, ScriptMapOverlay, ScriptExterior, ScriptInterior, File, PersonFlightAccess


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
    list_display = ("name", "loc_city", "loc_state", "loc_country", "get_person", "owner")
    list_filter = ("name", "loc_city", "loc_state", "loc_country", "person", "owner")

    # Custom method to display related person names
    def get_person(self, obj):
        return ", ".join([p.name for p in obj.person.all()])

    get_person.short_description = 'Person'


class FilterFile(admin.ModelAdmin):
    list_display = ("name", "link", "thumbnail", "direct_download_link", "size_in_mb", "file_type", "flight")
    list_filter = ("flight", "file_type", "name", "size_in_mb")

admin.site.register(Person, PersonID)
admin.site.register(Owner)
admin.site.register(Property, FilterProperty)
admin.site.register(ScriptMapOverlay)
admin.site.register(ScriptExterior)
admin.site.register(ScriptInterior)
admin.site.register(File, FilterFile)
admin.site.register(Flight, FilterFlight)
admin.site.register(PersonFlightAccess)