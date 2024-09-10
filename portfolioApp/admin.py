from django.contrib import admin
from .models import property


# class property(admin.ModelAdmin):
#     list_display = ("name", "image", "video", "dunker", "prereq")
#     list_filter = ("dunker",)

admin.site.register(property)