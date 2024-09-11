from django.contrib import admin
from .models import Person, Owner, Property, Flight


class PersonID(admin.ModelAdmin):
    readonly_fields = ('uuid',)

admin.site.register(Person, PersonID)
admin.site.register(Owner)
admin.site.register(Property)
admin.site.register(Flight)