from django.contrib import admin
from .models import Person, Owner, Property, Flight


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

admin.site.register(Person, PersonID)
admin.site.register(Owner)
admin.site.register(Property)
admin.site.register(Flight, FilterFlight)
