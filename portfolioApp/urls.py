from django.urls import path
from .views import indexPageView, ownerPageView, propertyPageView

urlpatterns = [
    path('services/', indexPageView, name = "index"),
    path('<uuid:person_uuid>/', ownerPageView, name='owner'),
    path('<uuid:person_uuid>/<str:property_name>/', propertyPageView, name='property'),    
]